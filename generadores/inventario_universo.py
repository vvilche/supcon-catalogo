#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INVENTARIO DEL UNIVERSO: cuántas empresas hay, por industria, y en qué estado está cada una.

Responde: "cuántas empresas tienes y por tipo de industria".

LAS CAPAS (cada una es un universo distinto, y NO son el mismo conjunto):
------------------------------------------------------------------------------
  A. Universo RETC               3.157  el padrón completo (rubro + señal de dolor)
  B. Con dolor medido              370  de esas, las que tienen carga peligrosa/RILES
  C. Mineras del RETC              220  las que el cruce había perdido
  D. Plan de acción                198  con personas mapeadas
  E. Buscador de decisores         488  barridas, con decisores
  F. Campaña Process                75  el target del cliente

REGLA: reportar POR RUBRO siempre. Un total agregado esconde dónde está el hueco.

Salida: datos/inventario_universo.json + artefactos/inventario_universo.html
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def load(p, k=None):
    fp = os.path.join(D, p)
    if not os.path.exists(fp):
        return None
    d = json.load(open(fp, encoding="utf-8"))
    return d[k] if k else d


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


# --- capas
universo = load("universo_prospeccion_supcon.json", "empresas") or []
dolor = load("dolor_ambiental_empresas.json", "empresas") or []
mineras = load("mineras_retc.json", "mineras") or []
plan = load("plan_accion.json", "plan") or []
buscador = load("buscador_decisores.json", "resultados") or []
cruce = load("cruce_campana.json", "filas") or []

print("=" * 100)
print("INVENTARIO DEL UNIVERSO")
print("=" * 100)
print(f"  A. Universo RETC (padrón completo)      {len(universo):>6,}")
print(f"  B. Con dolor medido                     {len(dolor):>6,}")
print(f"  C. Mineras del RETC                     {len(mineras):>6,}")
print(f"  D. Plan de acción (con personas)        {len(plan):>6,}")
print(f"  E. Buscador de decisores                {len(buscador):>6,}")
print(f"  F. Campaña Process (target del cliente) {len(cruce):>6,}")

# --- por rubro (la capa A es la que tiene rubro para todas)
por_rubro = collections.Counter(e.get("rubro", "(sin rubro)") for e in universo)

# --- decisores por rubro: cruzar el buscador al universo
idx_uni = {}
for e in universo:
    idx_uni[norm(e["empresa"])] = e


def rubro_de(nombre):
    n = norm(nombre)
    if n in idx_uni:
        return idx_uni[n].get("rubro")
    toks = set(t for t in n.split() if len(t) > 4)
    for k, e in idx_uni.items():
        if len(toks & set(k.split())) >= 2:
            return e.get("rubro")
    return None


dec_por_rubro = collections.Counter()
sin_rubro = 0
for x in buscador:
    r = rubro_de(x["empresa"])
    if r:
        dec_por_rubro[r] += 1
    else:
        sin_rubro += 1

# --- por tier (priorización del universo)
por_tier = collections.Counter(e.get("tier", "—") for e in universo)
# --- por region
por_region = collections.Counter(e.get("region", "—") for e in universo)

print("\n" + "=" * 100)
print("POR TIPO DE INDUSTRIA (universo RETC: 3.157 empresas)")
print("=" * 100)
print(f"  {'industria':46s} {'empresas':>9s} {'con decisores':>14s}")
tot_dec = 0
filas_ind = []
for r, v in por_rubro.most_common():
    nd = dec_por_rubro.get(r, 0)
    tot_dec += nd
    filas_ind.append((r, v, nd))
    print(f"  {r[:44]:46s} {v:>9,} {nd:>14,}")
print(f"  {'TOTAL':46s} {sum(por_rubro.values()):>9,} {tot_dec:>14,}")
if sin_rubro:
    print(f"  (empresas del buscador sin rubro identificado: {sin_rubro})")

print("\n=== POR TIER (priorización) ===")
for k, v in por_tier.most_common():
    print(f"  {str(k)[:30]:32s} {v:>6,}")

print("\n=== POR REGIÓN (top 12) ===")
for k, v in por_region.most_common(12):
    print(f"  {str(k)[:32]:34s} {v:>6,}")

json.dump({
    "capas": {"universo_retc": len(universo), "con_dolor": len(dolor), "mineras_retc": len(mineras),
              "plan_accion": len(plan), "buscador_decisores": len(buscador),
              "campana_process": len(cruce)},
    "por_industria": [{"industria": r, "empresas": v, "con_decisores": nd} for r, v, nd in filas_ind],
    "por_tier": dict(por_tier), "por_region": dict(por_region.most_common(20)),
}, open(os.path.join(D, "inventario_universo.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/inventario_universo.json")
