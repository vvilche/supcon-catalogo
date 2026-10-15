#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruye la GEO (región + industria) para el plan de acción LIMPIO.

La región sale del RETC crudo (`datos/retc/respeligrosos_2025.xlsx`, hoja `Generador`): cada
declaración trae razon_social + region. Se toma la región DOMINANTE por empresa.

Por qué no sirve el match por nombre: 90 de 166 empresas del plan quedaban "sin región" porque el
nombre del catálogo no coincide con la razón social del RETC. Hay que normalizar de los dos lados.

Salida: datos/plan_geo_limpio.json
"""
import json, os, re, unicodedata, collections
import openpyxl

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
RETC = os.path.join(D, "retc", "respeligrosos_2025.xlsx")

GENERICOS = {"minera", "minero", "mineria", "compania", "compañia", "sociedad", "anonima", "chile",
             "empresa", "empresas", "grupo", "holding", "nacional", "sur", "norte", "central", "del",
             "las", "los", "san", "santa", "servicios", "industrial", "industria", "spa", "ltda",
             "limitada", "s", "a"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def marca(n):
    toks = [t for t in norm(n).split() if len(t) > 3 and t not in GENERICOS]
    return max(toks, key=len) if toks else None


# --- 1. región por razón social del RETC
wb = openpyxl.load_workbook(RETC, read_only=True, data_only=True)
ws = wb["Generador"]
rows = list(ws.iter_rows(values_only=True))
hdr = {str(c).strip().lower().replace(" ", "_"): i
       for i, c in enumerate(rows[0]) if c}
j_rs, j_reg = hdr.get("razon_social"), hdr.get("region")
if j_rs is None or j_reg is None:
    raise SystemExit(f"no encontré razon_social/region en el RETC. columnas: {list(hdr)[:20]}")
print(f"columnas RETC: razon_social={j_rs}, region={j_reg}")

reg_por_emp = collections.defaultdict(collections.Counter)
for r in rows[1:]:
    if len(r) <= max(j_rs, j_reg):
        continue
    rs, reg = r[j_rs], r[j_reg]
    if rs and reg:
        reg_por_emp[norm(rs)][str(reg).strip()] += 1
wb.close()
print(f"empresas con región en el RETC: {len(reg_por_emp)}")

# índice por marca distintiva para el match tolerante
reg_por_marca = collections.defaultdict(collections.Counter)
for k, c in reg_por_emp.items():
    m = marca(k)
    if m:
        reg_por_marca[m].update(c)


def region_de(nombre):
    n = norm(nombre)
    if n in reg_por_emp:
        return reg_por_emp[n].most_common(1)[0][0]
    m = marca(nombre)
    if m and m in reg_por_marca:
        return reg_por_marca[m].most_common(1)[0][0]
    # último recurso: buscar la marca dentro de alguna razón social
    if m:
        for k, c in reg_por_emp.items():
            if m in k.split():
                return c.most_common(1)[0][0]
    return None


# --- 2. mapear rubro -> industria legible (unificar las dos taxonomías)
MAP_RUBRO = {
    "Extracción de minerales": "Minería", "Producción de metal": "Minería / metalurgia",
    "Minería": "Minería",
    "Industria manufacturera": "Manufactura", "Producción de alimentos": "Alimentos",
    "Industria agropecuaria y silvicultura": "Agro y forestal", "Pesca": "Pesca y acuicultura",
    "Combustibles": "Combustibles y gas", "Producción química": "Química",
    "Generación de energía": "Generación eléctrica",
    "Transmision y distribucion de energía eléctrica": "Transmisión eléctrica",
    "Suministro y tratamiento de aguas": "Aguas", "Papel y celulosa": "Papel y celulosa",
    "Gestor de residuos": "Gestión de residuos",
}

plan = json.load(open(os.path.join(D, "plan_accion_limpio.json"), encoding="utf-8"))["plan"]
universo = json.load(open(os.path.join(D, "universo_prospeccion_supcon.json"), encoding="utf-8"))["empresas"]
idx_u = {norm(e["empresa"]): e for e in universo}
rubro_por_marca = {}
for k, e in idx_u.items():
    m = marca(k)
    if m:
        rubro_por_marca.setdefault(m, e.get("rubro"))


def ind_de(nombre, rubro_actual):
    n = norm(nombre)
    if n in idx_u:
        return MAP_RUBRO.get(idx_u[n].get("rubro"), idx_u[n].get("rubro"))
    m = marca(nombre)
    if m and m in rubro_por_marca:
        return MAP_RUBRO.get(rubro_por_marca[m], rubro_por_marca[m])
    return MAP_RUBRO.get(rubro_actual, rubro_actual) or "Sin industria"


geo = {"por_region": collections.defaultdict(lambda: {"empresas": [], "contactos": 0}),
       "por_industria": collections.defaultdict(lambda: {"empresas": [], "contactos": 0})}
sin_reg = 0
for p in plan:
    reg = p.get("region") if p.get("region") not in (None, "", "Sin región") else region_de(p["empresa"])
    reg = reg or "Sin región"
    if reg == "Sin región":
        sin_reg += 1
    ind = ind_de(p["empresa"], p.get("industria", ""))
    p["region"], p["industria"] = reg, ind
    n_c = len(p["contactos"])
    geo["por_region"][reg]["empresas"].append(p["empresa"])
    geo["por_region"][reg]["contactos"] += n_c
    geo["por_industria"][ind]["empresas"].append(p["empresa"])
    geo["por_industria"][ind]["contactos"] += n_c

print(f"\n=== POR REGIÓN ===")
for k, v in sorted(geo["por_region"].items(), key=lambda x: -x[1]["contactos"]):
    print(f"  {k[:38]:40s} {len(v['empresas']):3d} emp  {v['contactos']:4d} contactos")
print(f"\n=== POR INDUSTRIA ===")
for k, v in sorted(geo["por_industria"].items(), key=lambda x: -x[1]["contactos"]):
    print(f"  {k[:38]:40s} {len(v['empresas']):3d} emp  {v['contactos']:4d} contactos")
print(f"\nsin región: {sin_reg}")

json.dump({"que_es": "Plan de acción limpio (533 contactos validados) en 2 vistas: región e industria. "
                     "Región del RETC hoja Generador (declaración por faena).",
           "totales": {"empresas": len(plan), "contactos": sum(len(p["contactos"]) for p in plan),
                       "con_telefono": sum(1 for p in plan if p.get("telefono_central")),
                       "regiones": len(geo["por_region"]), "industrias": len(geo["por_industria"]),
                       "sin_region": sin_reg},
           "por_region": {k: {"n_empresas": len(v["empresas"]), "contactos": v["contactos"],
                              "empresas": v["empresas"]} for k, v in geo["por_region"].items()},
           "por_industria": {k: {"n_empresas": len(v["empresas"]), "contactos": v["contactos"],
                                 "empresas": v["empresas"]} for k, v in geo["por_industria"].items()},
           "plan": plan},
          open(os.path.join(D, "plan_geo_limpio.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/plan_geo_limpio.json")
