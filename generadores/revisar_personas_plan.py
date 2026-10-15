#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REVISA las personas del plan según la FUENTE, que es lo que da (o no) la garantía de pertenencia.

EL CRITERIO CORRECTO (aprendido tras dos intentos fallidos)
------------------------------------------------------------------------------
La pertenencia NO se adivina del texto del cargo: la da la FUENTE.
  - fuente `direcmin.com/<slug>/ejecutivos` -> PERTENECE. Direcmin lista los ejecutivos BAJO el
    slug de esa empresa; es una garantía de la fuente, no una inferencia.
  - fuente `LinkedIn` -> NO garantiza. El keyword search devuelve el headline de cualquier persona
    que mencione el término; hay que validar contra el cargo.
  - fuente `Transparencia` -> PERTENECE (la empresa publica sus propios ejecutivos por ley).

Los dos intentos fallidos, para no repetirlos:
  1. Buscar la marca de la empresa DENTRO del cargo -> marcó "6 de 6 ajenos" en Los Pelambres y
     Codelco, cuyos cargos (de Direcmin) son correctos. Falso positivo masivo.
  2. Usar el `cargo` del barrido como headline -> el barrido guarda el cargo suelto ("Gerente
     General"), sin el "en <empresa>": no sirve para validar pertenencia.

Lo que SÍ se puede validar sin fuente: el CARGO es de compra técnica (no ventas/RRHH/marketing).

Salida: datos/personas_revisadas.json
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


NO_COMPRA = re.compile(
    r"ventas|sales|marketing|seo|digital|reclutamiento|selecci[oó]n|compensaci|recursos humanos|"
    r"rrhh|talento|people|comunicaci|legal|fiscal|abogad|finanz|contab|tesorer|auditor corporativo|"
    r"relaciones p[uú]blicas|asuntos p[uú]blicos|brand|publicidad|directorio|fiscal", re.I)

bdr = json.load(open(os.path.join(D, "buscador_decisores.json"), encoding="utf-8"))["resultados"]
plan = json.load(open(os.path.join(D, "plan_accion.json"), encoding="utf-8"))["plan"]

# índice: (empresa, nombre de persona) -> fuente y cargo del barrido
idx = {}
for x in bdr:
    for h in x["hallazgos"]:
        idx[(norm(x["empresa"]), norm(h["nombre"]))] = h

print("=" * 100)
print("REVISIÓN DE PERSONAS — por GARANTÍA DE LA FUENTE")
print("=" * 100)

tot, garant, linkedin, nc, sin_dato = 0, 0, 0, 0, 0
por_fuente = collections.Counter()
empresas_mal, revisado = [], []
for e in plan:
    ne = norm(e["empresa"])
    buenos, dudosos, no_compran, sin = [], [], [], []
    for c in e.get("contactos", []):
        tot += 1
        h = idx.get((ne, norm(c["nombre"])))
        f = (h or {}).get("fuente", "?")
        if h is None:
            sin.append(c); sin_dato += 1; por_fuente["sin dato"] += 1
            continue
        if f.startswith("direcmin.com") or "Transparencia" in f:
            por_fuente["garantizada (Direcmin/Transparencia)"] += 1
            if NO_COMPRA.search(c["cargo"]):
                no_compran.append(c); nc += 1
            else:
                buenos.append({**c, "fuente": f}); garant += 1
        elif f.startswith("LinkedIn"):
            por_fuente["LinkedIn (a validar)"] += 1
            if NO_COMPRA.search(c["cargo"]):
                no_compran.append(c); nc += 1
            else:
                dudosos.append({**c, "fuente": f}); linkedin += 1
        else:
            por_fuente["otra"] += 1
            dudosos.append(c)
    revisado.append({"empresa": e["empresa"], "garantizados": buenos, "linkedin": dudosos,
                     "no_compra": no_compran, "sin_dato": sin})

print(f"  personas en el plan:                    {tot:,}")
print(f"  GARANTIZADAS por la fuente:             {garant:,} ({garant/tot*100:.0f}%)")
print(f"  de LinkedIn (a validar con LinkedIn):   {linkedin:,} ({linkedin/tot*100:.0f}%)")
print(f"  cargo que NO compra (ventas/RRHH/legal):{nc:,} ({nc/tot*100:.0f}%)")
print(f"  sin dato en el barrido:                 {sin_dato:,} ({sin_dato/tot*100:.0f}%)")

print(f"\n=== POR FUENTE ===")
for k, v in por_fuente.most_common():
    print(f"  {k:40s} {v:5,}")

# las que el plan tiene cargadas y NO se pueden verificar = el riesgo real
print(f"\n=== EMPRESAS CON CONTACTOS SIN GARANTÍA (LinkedIn) — las que hay que revisar ===")
peor = sorted([r for r in revisado if r["linkedin"]], key=lambda z: -len(z["linkedin"]))
for x in peor[:15]:
    print(f"\n  {x['empresa'][:44]}  ({len(x['linkedin'])} de LinkedIn)")
    for c in x["linkedin"][:3]:
        print(f"      ~ {c['nombre'][:26]:28s} {c['cargo'][:44]}")

print(f"\n=== CARGOS QUE NO COMPRAN (se sacan de la lista de llamados) ===")
vistos = set()
for r in revisado:
    for c in r["no_compra"]:
        if c["cargo"] not in vistos:
            vistos.add(c["cargo"])
            print(f"  {r['empresa'][:34]:36s} {c['nombre'][:24]:26s} {c['cargo'][:44]}")

json.dump({"totales": {"personas": tot, "garantizadas": garant, "linkedin_a_validar": linkedin,
                       "no_compra": nc, "sin_dato": sin_dato},
           "por_fuente": dict(por_fuente), "empresas": revisado},
          open(os.path.join(D, "personas_revisadas.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/personas_revisadas.json")
