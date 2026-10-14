#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEDUPLICA el inventario: la misma empresa aparece con varios nombres (razón social vs comercial),
y contarla dos veces infla el total.

Medido: "Minera Las Cenizas" (28) y "MINERA LAS CENIZAS S A" (31) son la MISMA empresa; igual
"Minera Valle Central" (19) y "MINERA VALLE CENTRAL S A" (18); "Codelco" (27) y "CORP NACIONAL DEL
COBRE DE CHILE" (32).

REGLA: clave = el token distintivo (el más largo no genérico) de la razón social. Si dos entradas
comparten la clave distintiva, se fusionan tomando la UNIÓN de los decisores (sin repetir personas
por nombre+cargo).

Salida: reescribe datos/inventario_final.json con "empresas_unicas"
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

GENERICOS = {"empresa", "empresas", "sociedad", "anonima", "compania", "companias", "chile",
             "nacional", "minera", "minero", "mineria", "industria", "industrial", "servicios",
             "productos", "produccion", "comercial", "agricola", "forestal", "pesquera",
             "alimentos", "generacion", "energia", "electrica", "limitada", "ltda", "spa",
             "grupo", "holding", "inversiones", "del", "las", "los", "san", "santa", "planta", "scm",
             "sac", "saic", "s a"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def clave(nombre):
    toks = [t for t in norm(nombre).split() if len(t) > 3 and t not in GENERICOS]
    return max(toks, key=len) if toks else norm(nombre)


inv = json.load(open(os.path.join(D, "inventario_final.json"), encoding="utf-8"))
det = inv["detalle"]

# cargar los decisores de cada empresa desde las fuentes auditadas
def load(p, k=None):
    fp = os.path.join(D, p)
    if not os.path.exists(fp):
        return None
    d = json.load(open(fp, encoding="utf-8"))
    return d[k] if k else d

personas_por_empresa = {}
for x in load("buscador_decisores.json", "resultados") or []:
    personas_por_empresa[norm(x["empresa"])] = [
        (h["nombre"], h["cargo"]) for h in x["hallazgos"]]
for a in load("barrido_campana_auditado.json") or []:
    personas_por_empresa.setdefault(norm(a["empresa"]), []).extend(
        [(h["nombre"], h["cargo"]) for h in a["validos"]])
bu = load("barrido_universo_auditado.json") or {}
for a in bu.get("empresas", []):
    personas_por_empresa.setdefault(norm(a["empresa"]), []).extend(
        [(h["nombre"], h["cargo"]) for h in a["validos"]])

# agrupar por NOMBRE NORMALIZADO, no por token distintivo.
# OJO: agrupar por el token más largo FUSIONA empresas distintas (medido): "Minera Valle Central"
# con "Central Yungay" (por "central"), "Universidad de Antofagasta" con "Universidad Austral"
# (por "universidad"), "GNL Quintero" con "Pesquera Quintero" (por "quintero"). Eso borra empresas
# reales. Lo único seguro es unir cuando el nombre COMPLETO normalizado coincide.
grupos = collections.defaultdict(lambda: {"nombres": [], "personas": set(), "rubro": None, "tier": "—"})
for d in det:
    c = norm(d["empresa"])
    g = grupos[c]
    g["nombres"].append(d["empresa"])
    g["rubro"] = g["rubro"] or d["rubro"]
    if g["tier"] == "—":
        g["tier"] = d["tier"]
    for p in personas_por_empresa.get(norm(d["empresa"]), []):
        g["personas"].add(p)

print("=" * 100)
print("DEDUPLICACIÓN DEL INVENTARIO")
print("=" * 100)
print(f"  entradas antes:  {len(det)}")
print(f"  empresas ÚNICAS: {len(grupos)}")

fusionadas = [(c, g) for c, g in grupos.items() if len(g["nombres"]) > 1]
print(f"  grupos con más de un nombre: {len(fusionadas)}")
print(f"\n=== FUSIONES (las que inflaban el conteo) ===")
for c, g in sorted(fusionadas, key=lambda x: -len(x[1]["nombres"]))[:20]:
    print(f"  {' / '.join(n[:30] for n in g['nombres'][:3])[:72]:74s} {len(g['personas'])} personas")

tot_u = sum(len(g["personas"]) for g in grupos.values())
print(f"\n  decisores totales (sin repetir persona): {tot_u:,}")

por_rubro = collections.defaultdict(lambda: {"empresas": 0, "decisores": 0})
for g in grupos.values():
    r = g["rubro"] or "(sin rubro)"
    por_rubro[r]["empresas"] += 1
    por_rubro[r]["decisores"] += len(g["personas"])

print(f"\n=== POR RUBRO (deduplicado) ===")
print(f"  {'rubro':46s} {'empresas':>9s} {'decisores':>10s}")
for r, c in sorted(por_rubro.items(), key=lambda x: -x[1]["decisores"]):
    print(f"  {r[:44]:46s} {c['empresas']:>9} {c['decisores']:>10}")

salida = {
    "totales": {"empresas_unicas": len(grupos), "decisores": tot_u,
                "entradas_sin_dedup": len(det)},
    "por_rubro": [{"rubro": r, "empresas": c["empresas"], "decisores": c["decisores"]}
                  for r, c in sorted(por_rubro.items(), key=lambda x: -x[1]["decisores"])],
    "empresas": [{"clave": c, "nombres": g["nombres"], "rubro": g["rubro"] or "(sin rubro)",
                  "tier": g["tier"], "n_decisores": len(g["personas"]),
                  "personas": [{"nombre": p[0], "cargo": p[1]} for p in sorted(g["personas"])]}
                 for c, g in grupos.items()],
}
json.dump(salida, open(os.path.join(D, "inventario_final.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/inventario_final.json")
