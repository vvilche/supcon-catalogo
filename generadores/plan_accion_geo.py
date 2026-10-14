#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO DEL PLAN DE ACCIÓN — separar los contactos por REGIÓN y CIUDAD.

POR QUÉ IMPORTA: la región decide el viaje (una gira a Antofagasta vale si hay 15 cuentas
juntas), el horario y con quién conviene juntarse en la misma visita. Sin el dato geográfico, la
lista de 899 contactos es un archivo plano.

DE DÓNDE SALE EL DATO
------------------------------------------------------------------------------
`datos/retc/respeligrosos_2025.xlsx`, hoja 'Generador': cada declaración trae `region`, `comuna`
y coordenadas. Se toma la región DOMINANTE por empresa (la faena principal) y sus comunas.

OJO: 5.320 empresas declarantes en el RETC, pero el plan de acción tiene 198 con decisores.
Se cruza por razón social; lo que no cruza queda marcado "sin región" (no se inventa).

Salida: datos/plan_accion_geo.json
"""
import openpyxl, os, re, json, collections, unicodedata

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
RETC = os.path.join(D, "retc")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


# ---------------------------------------------------------------------------
# 1. extraer region/comuna por empresa del RETC
# ---------------------------------------------------------------------------
wb = openpyxl.load_workbook(os.path.join(RETC, "respeligrosos_2025.xlsx"),
                            read_only=True, data_only=True)
ws = wb["Generador"]
hdr = None
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        hdr = {str(c).strip(): j for j, c in enumerate(row) if c is not None}
        break
j_rs, j_reg = hdr.get("razon_social"), hdr.get("region")
j_com, j_prov = hdr.get("comuna"), hdr.get("provincia")
j_lat, j_lon = hdr.get("lat"), hdr.get("long")

reg_por_emp = collections.defaultdict(collections.Counter)
com_por_emp = collections.defaultdict(collections.Counter)
prov_por_emp = collections.defaultdict(collections.Counter)
coord_por_emp = collections.defaultdict(list)


def coord(v, es_lat):
    try:
        x = float(v)
    except Exception:
        return None
    while abs(x) > 1000:
        x /= 10.0
    if es_lat and not (-56 < x < -17):
        return None
    if not es_lat and not (-76 < x < -66):
        return None
    return round(x, 4)


for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        continue
    rs = row[j_rs] if j_rs is not None else None
    if not rs:
        continue
    rs = str(rs).strip()
    if row[j_reg]:
        reg_por_emp[rs][str(row[j_reg]).strip()] += 1
    if j_com is not None and row[j_com]:
        com_por_emp[rs][str(row[j_com]).strip()] += 1
    if j_prov is not None and row[j_prov]:
        prov_por_emp[rs][str(row[j_prov]).strip()] += 1
    la = coord(row[j_lat], True) if j_lat is not None and row[j_lat] else None
    lo = coord(row[j_lon], False) if j_lon is not None and row[j_lon] else None
    if la and lo:
        coord_por_emp[rs].append((la, lo))
wb.close()
print(f"RETC: {len(reg_por_emp):,} empresas con región")

# ---------------------------------------------------------------------------
# 2. cruzar con el plan de acción
# ---------------------------------------------------------------------------
plan = json.load(open(os.path.join(D, "plan_accion.json"), encoding="utf-8"))
idx_geo = {norm(k): k for k in reg_por_emp}


def geo_de(empresa):
    n = norm(empresa)
    # match exacto, luego por token distintivo
    if n in idx_geo:
        k = idx_geo[n]
    else:
        toks = set(t for t in n.split() if len(t) > 3)
        k = None
        mejor = 0
        for kn, korig in idx_geo.items():
            c = len(toks & set(kn.split()))
            if c > mejor and c >= 2:
                mejor, k = c, korig
    if not k:
        # probar dentro de la misma razón (el plan trae nombres truncados)
        for kn, korig in idx_geo.items():
            if n and (n in kn or kn in n) and len(n) > 8:
                k = korig
                break
    if not k:
        return None
    return {
        "region": reg_por_emp[k].most_common(1)[0][0] if reg_por_emp[k] else "",
        "comuna": com_por_emp[k].most_common(1)[0][0] if com_por_emp[k] else "",
        "comunas": [x for x, _ in com_por_emp[k].most_common(4)],
        "provincia": prov_por_emp[k].most_common(1)[0][0] if prov_por_emp[k] else "",
        "coords": coord_por_emp[k][:1],
    }


con_geo = 0
for p in plan["plan"]:
    g = geo_de(p["empresa"])
    if g:
        p.update(g)
        con_geo += 1
    else:
        p.update({"region": "", "comuna": "", "comunas": [], "provincia": "", "coords": []})

# ---------------------------------------------------------------------------
# 2b. INDUSTRIA: rubro del RETC + tipo (operador/proveedor) desde mineras_retc
# ---------------------------------------------------------------------------
mineras_rubro = {norm(m["empresa"]): m for m in
                 (json.load(open(os.path.join(D, "mineras_retc.json"), encoding="utf-8"))
                  ).get("mineras", [])}


def industria_de(empresa):
    """Rubro de la empresa, del RETC. Se limpia a una etiqueta corta y comparable."""
    n = norm(empresa)
    m = mineras_rubro.get(n)
    if not m:
        toks = set(t for t in n.split() if len(t) > 3)
        mejor, sc = None, 0
        for kn, k in mineras_rubro.items():
            c = len(toks & set(kn.split()))
            if c > sc and c >= 2:
                mejor, sc = k, c
        m = mejor
    if not m:
        return {"industria": "Sin clasificar", "tipo": ""}
    r = (m.get("rubro") or "").strip()
    # normalizar a etiquetas cortas
    if "miner" in r.lower():
        ind = "Minería"
    elif "manufactur" in r.lower():
        ind = "Manufactura / servicios mineros"
    elif "madera" in r.lower() or "silvicultura" in r.lower():
        ind = "Forestal / madera"
    elif "química" in r.lower() or "pl" in r.lower():
        ind = "Química"
    elif "pesca" in r.lower() or "acuicultura" in r.lower():
        ind = "Pesca / acuicultura"
    elif "cemento" in r.lower():
        ind = "Cemento"
    elif "comercio" in r.lower():
        ind = "Comercio"
    elif "agropecuaria" in r.lower():
        ind = "Agropecuario"
    else:
        ind = r[:34] if r else "Sin clasificar"
    return {"industria": ind, "tipo": m.get("tipo", ""),
            "ciiu6": m.get("ciiu6", "")[:40]}


for p in plan["plan"]:
    p.update(industria_de(p["empresa"]))

# ---------------------------------------------------------------------------
# 3. agrupar
# ---------------------------------------------------------------------------
por_region = collections.defaultdict(lambda: {"empresas": [], "contactos": 0,
                                              "usd_cotizado": 0.0, "dolor_t": 0.0})
for p in plan["plan"]:
    r = p["region"] or "SIN REGIÓN (no cruzó con el RETC)"
    por_region[r]["empresas"].append(p)
    por_region[r]["contactos"] += p["n_contactos"]
    por_region[r]["usd_cotizado"] += p["usd_cotizado"] or 0
    por_region[r]["dolor_t"] += p["dolor_t"] or 0

orden = sorted(por_region.items(),
               key=lambda kv: (-kv[1]["usd_cotizado"], -kv[1]["contactos"]))

# agrupar también por INDUSTRIA y por TIPO (operador / proveedor minero)
por_industria = collections.defaultdict(lambda: {"empresas": [], "contactos": 0,
                                                 "usd_cotizado": 0.0, "dolor_t": 0.0})
por_tipo = collections.defaultdict(lambda: {"empresas": [], "contactos": 0})
for p in plan["plan"]:
    ind = p.get("industria") or "Sin clasificar"
    por_industria[ind]["empresas"].append(p)
    por_industria[ind]["contactos"] += p["n_contactos"]
    por_industria[ind]["usd_cotizado"] += p["usd_cotizado"] or 0
    por_industria[ind]["dolor_t"] += p["dolor_t"] or 0
    tp = {"operador": "Operadores mineros", "proveedor_minero": "Proveedores mineros"}.get(
        p.get("tipo", ""), "Sin tipo")
    por_tipo[tp]["empresas"].append(p)
    por_tipo[tp]["contactos"] += p["n_contactos"]

orden_ind = sorted(por_industria.items(), key=lambda kv: -kv[1]["contactos"])
print(f"\nplan: {len(plan['plan'])} empresas | con región: {con_geo} "
      f"({con_geo/len(plan['plan'])*100:.0f}%)")
print(f"\n{'='*96}")
print("PLAN DE ACCIÓN POR REGIÓN")
print(f"{'='*96}")
for r, v in orden:
    print(f"\n  {r}  —  {len(v['empresas'])} empresas · {v['contactos']} contactos · "
          f"US${v['usd_cotizado']:,.0f} cotizado")
    for p in sorted(v["empresas"], key=lambda x: -(x["usd_cotizado"] or 0))[:4]:
        com = p["comuna"] or "—"
        print(f"      {p['empresa'][:38]:40s} {com[:16]:18s} {p['n_contactos']:>2} cont")

print(f"\n{'='*96}")
print("PLAN DE ACCIÓN POR INDUSTRIA")
print(f"{'='*96}")
for ind, v in orden_ind:
    print(f"  {ind[:40]:42s} {len(v['empresas']):>3} emp · {v['contactos']:>3} cont · "
          f"US${v['usd_cotizado']:>11,.0f}")

json.dump({
    "que_es": ("Plan de acción agrupado por REGIÓN, CIUDAD e INDUSTRIA. El dato geográfico sale "
               "del RETC (hoja Generador: region/comuna/provincia/coordenadas por declaración); la "
               "industria, del rubro del RETC y del tipo (operador vs proveedor minero)."),
    "fuente": "datos/retc/respeligrosos_2025.xlsx + datos/plan_accion.json + datos/mineras_retc.json",
    "totales": {"empresas": len(plan["plan"]), "con_region": con_geo,
                "regiones": len(por_region), "industrias": len(por_industria),
                "contactos": plan["totales"]["contactos"]},
    "por_region": {r: {"n_empresas": len(v["empresas"]), "contactos": v["contactos"],
                       "usd_cotizado": round(v["usd_cotizado"], 2),
                       "dolor_t": round(v["dolor_t"], 2),
                       "empresas": v["empresas"]} for r, v in orden},
    "por_industria": {ind: {"n_empresas": len(v["empresas"]), "contactos": v["contactos"],
                            "usd_cotizado": round(v["usd_cotizado"], 2),
                            "dolor_t": round(v["dolor_t"], 2),
                            "empresas": v["empresas"]} for ind, v in orden_ind},
    "por_tipo": {t: {"n_empresas": len(v["empresas"]), "contactos": v["contactos"]}
                 for t, v in por_tipo.items()},
}, open(os.path.join(D, "plan_accion_geo.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/plan_accion_geo.json")
