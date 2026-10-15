#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruye el PLAN DE ACCIÓN con SOLO las personas validadas (533 de 899).

Además reconstruye la vista GEO (por región e industria) con las empresas del plan válido.

Salida: datos/plan_accion_limpio.json + datos/plan_geo_limpio.json
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
GENERICOS = {"minera", "minero", "mineria", "compania", "compañia", "sociedad", "anonima", "chile",
             "empresa", "empresas", "grupo", "holding", "nacional", "sur", "norte", "central", "del",
             "las", "los", "san", "santa", "servicios", "industrial", "industria", "spa", "ltda"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def marca_de(n):
    toks = [t for t in norm(n).split() if len(t) > 3 and t not in GENERICOS]
    return max(toks, key=len) if toks else None


val = json.load(open(os.path.join(D, "personas_validadas.json"), encoding="utf-8"))
plan = json.load(open(os.path.join(D, "plan_accion.json"), encoding="utf-8"))["plan"]
universo = json.load(open(os.path.join(D, "universo_prospeccion_supcon.json"), encoding="utf-8"))["empresas"]
mineras = json.load(open(os.path.join(D, "mineras_retc.json"), encoding="utf-8"))["mineras"]

# índice del universo para sacar región/industria
idx_u = {norm(e["empresa"]): e for e in universo}
idx_m = {norm(m["empresa"]): m for m in mineras}


def geo_de(empresa):
    n = norm(empresa)
    if n in idx_u:
        return idx_u[n].get("region"), idx_u[n].get("rubro")
    if n in idx_m:
        return idx_m[n].get("region"), "Minería"
    mk = marca_de(empresa)
    if mk:
        for k, e in idx_u.items():
            if mk in k.split():
                return e.get("region"), e.get("rubro")
        for k, m in idx_m.items():
            if mk in k.split():
                return m.get("region"), "Minería"
    return None, None


por_val = {norm(x["empresa"]): x for x in val["empresas"]}
limpio, geo = [], {"por_region": collections.defaultdict(lambda: {"empresas": 0, "contactos": 0}),
                   "por_industria": collections.defaultdict(lambda: {"empresas": 0, "contactos": 0})}
tot_c = 0
for e in plan:
    v = por_val.get(norm(e["empresa"]))
    if not v or not v["buenos"]:
        continue
    reg, rub = geo_de(e["empresa"])
    reg = reg or "Sin región"
    rub = rub or "Sin industria"
    limpio.append({**e, "contactos": v["buenos"], "n_contactos": len(v["buenos"]),
                   "region": reg, "industria": rub})
    geo["por_region"][reg]["empresas"] += 1
    geo["por_region"][reg]["contactos"] += len(v["buenos"])
    geo["por_industria"][rub]["empresas"] += 1
    geo["por_industria"][rub]["contactos"] += len(v["buenos"])
    tot_c += len(v["buenos"])

print("=" * 100)
print("PLAN DE ACCIÓN LIMPIO (solo personas validadas)")
print("=" * 100)
print(f"  empresas con contactos válidos: {len(limpio)}")
print(f"  contactos válidos:              {tot_c}")
print(f"  con teléfono:                   {sum(1 for e in limpio if e.get('telefono_central'))}")

print(f"\n=== POR REGIÓN ===")
for k, v in sorted(geo["por_region"].items(), key=lambda x: -x[1]["contactos"]):
    print(f"  {k[:36]:38s} {v['empresas']:3d} emp  {v['contactos']:4d} contactos")
print(f"\n=== POR INDUSTRIA ===")
for k, v in sorted(geo["por_industria"].items(), key=lambda x: -x[1]["contactos"]):
    print(f"  {k[:36]:38s} {v['empresas']:3d} emp  {v['contactos']:4d} contactos")

json.dump({"que_es": "Plan de acción con SOLO las personas validadas (fuente garantizada o LinkedIn "
                     "validado por headline). Se descartaron las ajenas, las de cargos que no compran "
                     "y las que el parser guardó con el cargo como nombre.",
           "totales": {"empresas": len(limpio), "contactos": tot_c,
                       "con_telefono": sum(1 for e in limpio if e.get("telefono_central"))},
           "plan": limpio}, open(os.path.join(D, "plan_accion_limpio.json"), "w"),
          ensure_ascii=False, indent=1)
json.dump({"que_es": "Vista geográfica del plan de acción limpio.",
           "totales": {"empresas": len(limpio), "contactos": tot_c,
                       "regiones": len(geo["por_region"]), "industrias": len(geo["por_industria"])},
           "por_region": {k: v for k, v in geo["por_region"].items()},
           "por_industria": {k: v for k, v in geo["por_industria"].items()}},
          open(os.path.join(D, "plan_geo_limpio.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/plan_accion_limpio.json + datos/plan_geo_limpio.json")
