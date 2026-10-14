#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INVENTARIO FINAL: cuántas empresas y decisores hay, por industria, con lo auditado.

Consolida las 3 fuentes de decisores:
  1. buscador_decisores.json        (488 empresas del barrido minero/plan)
  2. barrido_campana_auditado.json  (las 52 de la campaña Process)
  3. barrido_universo_auditado.json (las 356 del universo RETC, auditadas)

Y las clasifica por rubro del RETC.

Salida: datos/inventario_final.json + artefactos/inventario_final.html
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "inventario_final.html")


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


universo = load("universo_prospeccion_supcon.json", "empresas") or []
idx_uni = {norm(e["empresa"]): e for e in universo}


def rubro_de(nombre):
    n = norm(nombre)
    if n in idx_uni:
        return idx_uni[n].get("rubro"), idx_uni[n].get("tier")
    toks = [t for t in n.split() if len(t) > 4]
    if not toks:
        return None, None
    key = max(toks, key=len)
    for k, e in idx_uni.items():
        if key in k.split():
            return e.get("rubro"), e.get("tier")
    return None, None


# --- juntar decisores de las 3 fuentes, tomando los VÁLIDOS
empresas = {}   # norm(nombre) -> {empresa, decisores:[...], fuente}

# 1. el buscador base (los que ya venían auditados de antes)
for x in load("buscador_decisores.json", "resultados") or []:
    buenos = [h for h in x["hallazgos"] if h.get("relevante") or not h.get("descartado")]
    if buenos:
        empresas[norm(x["empresa"])] = {
            "empresa": x["empresa"], "decisores": buenos, "fuente": "buscador base"}

# 2. barrido de la campaña (auditado: solo válidos)
for a in load("barrido_campana_auditado.json") or []:
    if a["n_validos"]:
        k = norm(a["empresa"])
        empresas[k] = {"empresa": a["empresa"], "decisores": a["validos"], "fuente": "barrido campaña"}

# 3. barrido del universo (auditado: solo válidos)
bu = load("barrido_universo_auditado.json") or {}
for a in bu.get("empresas", []):
    if a["n_validos"]:
        k = norm(a["empresa"])
        if k not in empresas:
            empresas[k] = {"empresa": a["empresa"], "decisores": a["validos"], "fuente": "barrido universo"}

print(f"empresas con decisores: {len(empresas)}")
tot_dec = sum(len(v["decisores"]) for v in empresas.values())
print(f"decisores totales: {tot_dec:,}")

# --- clasificar por rubro
por_rubro = collections.defaultdict(lambda: {"empresas": 0, "decisores": 0})
sin_rubro = {"empresas": 0, "decisores": 0}
detalle = []
for v in empresas.values():
    r, t = rubro_de(v["empresa"])
    if r:
        por_rubro[r]["empresas"] += 1
        por_rubro[r]["decisores"] += len(v["decisores"])
    else:
        sin_rubro["empresas"] += 1
        sin_rubro["decisores"] += len(v["decisores"])
    detalle.append({"empresa": v["empresa"], "rubro": r or "(sin rubro)", "tier": t or "—",
                    "decisores": len(v["decisores"]), "fuente": v["fuente"]})

print(f"\n=== POR RUBRO ===")
print(f"  {'rubro':46s} {'empresas':>9s} {'decisores':>10s}")
for r, c in sorted(por_rubro.items(), key=lambda x: -x[1]["decisores"]):
    print(f"  {r[:44]:46s} {c['empresas']:>9} {c['decisores']:>10}")
print(f"  {'(sin rubro en el RETC)':46s} {sin_rubro['empresas']:>9} {sin_rubro['decisores']:>10}")

# --- top empresas
print(f"\n=== TOP 30 EMPRESAS POR DECISORES ===")
for d in sorted(detalle, key=lambda x: -x["decisores"])[:30]:
    print(f"  {d['empresa'][:44]:46s} {d['decisores']:2d}  {str(d['rubro'])[:24]:26s} {d['tier']}")

json.dump({
    "totales": {"empresas_con_decisores": len(empresas), "decisores": tot_dec},
    "por_rubro": [{"rubro": r, "empresas": c["empresas"], "decisores": c["decisores"]}
                  for r, c in sorted(por_rubro.items(), key=lambda x: -x[1]["decisores"])],
    "sin_rubro": sin_rubro,
    "detalle": sorted(detalle, key=lambda x: -x["decisores"]),
}, open(os.path.join(D, "inventario_final.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/inventario_final.json")
