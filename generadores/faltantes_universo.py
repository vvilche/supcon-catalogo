#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mide CUÁNTAS empresas del universo RETC faltan de verdad en el buscador de decisores.

EL PROBLEMA QUE RESUELVE
------------------------------------------------------------------------------
Medir "faltantes" con match por tokens da un número FALSO: el match por 2 tokens comunes
matchea cualquier cosa.
  - SOC PESQUERA LANDES -> "granero sociedad anonima"      (por "sociedad"+"anonima")
  - EMPRESA NACIONAL DE MINERIA -> "empresa nacional del petroleo"  (por "empresa"+"nacional")
  - COMPANIA DE PETROLEOS DE CHILE COPEC -> "compania minera cordillera"  (por "compania"+"chile")
Los tokens "sociedad", "anonima", "empresa", "nacional", "compania", "chile" NO son distintivos.

LA REGLA: un match vale solo si comparten el token MÁS LARGO (el distintivo) o la marca principal,
descartando los genéricos. Igual que el match de slug de Direcmin.

Salida: datos/faltantes_universo.json + conteo por rubro/tier
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

GENERICOS = {
    "empresa", "empresas", "sociedad", "anonima", "compania", "companias", "chile", "nacional",
    "minera", "minero", "mineria", "industria", "industrial", "industriales", "servicios",
    "servicio", "productos", "produccion", "comercial", "comercializadora", "agricola", "agro",
    "forestal", "pesquera", "pesca", "acuicultura", "alimentos", "generacion", "energia",
    "electrica", "limitada", "ltda", "spa", "sac", "grupo", "holding", "inversiones", "norte",
    "sur", "central", "pacifico", "andina", "del", "las", "los", "san", "santa", "planta",
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def distintivo(nombre):
    """El token más largo que no es genérico: la marca real de la empresa."""
    toks = [t for t in norm(nombre).split() if len(t) > 3 and t not in GENERICOS]
    return max(toks, key=len) if toks else None


u = json.load(open(os.path.join(D, "universo_prospeccion_supcon.json"), encoding="utf-8"))["empresas"]
bdr = json.load(open(os.path.join(D, "buscador_decisores.json"), encoding="utf-8"))["resultados"]

# índice del buscador por token distintivo
idx_bd = {}
for x in bdr:
    d = distintivo(x["empresa"])
    if d:
        idx_bd.setdefault(d, []).append(x["empresa"])

# también por nombre normalizado exacto
nombres_bd = {norm(x["empresa"]) for x in bdr}


def en_buscador(nombre):
    n = norm(nombre)
    if n in nombres_bd:
        return n
    d = distintivo(nombre)
    if d and d in idx_bd:
        return idx_bd[d][0]
    return None


grandes_med = [e for e in u if e.get("tier") in ("GRANDE", "MEDIANA")]
ya, faltan = [], []
for e in grandes_med:
    m = en_buscador(e["empresa"])
    (ya if m else faltan).append(e)

print("=" * 100)
print("FALTANTES REALES (match por token DISTINTIVO, no por tokens comunes)")
print("=" * 100)
print(f"  GRANDES + MEDIANAS del universo: {len(grandes_med)}")
print(f"  ya en el buscador:               {len(ya)}")
print(f"  FALTAN de verdad:                {len(faltan)}")

print(f"\n=== LAS QUE FALTAN, POR TIER ===")
for k, v in collections.Counter(e.get("tier") for e in faltan).most_common():
    print(f"  {k:12s} {v:5d}")

print(f"\n=== LAS QUE FALTAN, POR RUBRO (grandes primero) ===")
print(f"  {'rubro':46s} {'GRANDE':>7s} {'MEDIANA':>8s} {'total':>7s}")
por_rubro = collections.defaultdict(lambda: {"GRANDE": 0, "MEDIANA": 0})
for e in faltan:
    por_rubro[e.get("rubro", "—")][e.get("tier")] += 1
for r, c in sorted(por_rubro.items(), key=lambda x: -(x[1]["GRANDE"] + x[1]["MEDIANA"])):
    print(f"  {str(r)[:44]:46s} {c['GRANDE']:>7} {c['MEDIANA']:>8} {c['GRANDE']+c['MEDIANA']:>7}")

# las GRANDES son el target prioritario
grandes = [e for e in faltan if e.get("tier") == "GRANDE"]
print(f"\n=== LAS {len(grandes)} GRANDES QUE FALTAN (nombre para buscar) ===")
for e in sorted(grandes, key=lambda x: -(x.get("residuos_t") or 0))[:40]:
    rt = e.get("residuos_t") or 0
    print(f"  {e['empresa'][:46]:48s} {str(e.get('rubro'))[:26]:28s} {rt:>12,.0f} t")

json.dump({
    "metodo": ("Match por token DISTINTIVO (el más largo no genérico), no por tokens comunes. "
               "El match por tokens comunes daba falsos: Pesquera Landes -> 'granero sociedad "
               "anonima'; ENAMI -> ENAP; Copec -> Minera Cordillera."),
    "grandes_medianas": len(grandes_med), "ya_en_buscador": len(ya), "faltan": len(faltan),
    "por_rubro": {r: c for r, c in por_rubro.items()},
    "faltantes": [{"empresa": e["empresa"], "rubro": e.get("rubro"), "tier": e.get("tier"),
                   "region": e.get("region"), "residuos_t": e.get("residuos_t") or 0}
                  for e in faltan],
}, open(os.path.join(D, "faltantes_universo.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/faltantes_universo.json")
