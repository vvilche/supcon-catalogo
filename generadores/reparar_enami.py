#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repara el registro de ENAMI en buscador_decisores.json.

EL PROBLEMA
------------------------------------------------------------------------------
ENAMI quedó guardada con la corrida por LinkedIn (10 personas), de las cuales **3 NO SON DE ENAMI**
(Sebastian Fehrmann es de BHP Spence; Montserrat P. y Stephanie Wilhelm son de Antofagasta Minerals).
El match por LinkedIn trae homónimos y cargos de otras mineras.

Lo que se pierde: la corrida de **Direcmin** — la fuente buena — trae 13 ejecutivos de ENAMI incluido
**Hernán Santander González, Gerente de la Fundición Hernán Videla Lira**, que es el gerente de la
planta EXACTA del proyecto de US$1.700M de la campaña.

REGLA
------------------------------------------------------------------------------
Direcmin es fuente de primera (ejecutivos por cargo, empresa verificada). LinkedIn es universal pero
hay que VALIDAR que la persona esté en la empresa — no darlo por bueno por aparecer en la búsqueda.
"""
import json, os, re, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, "datos", "buscador_decisores.json")

# Los 13 ejecutivos de ENAMI según Direcmin (direcmin.com/enami-empresa-nacional-de-miner-a/ejecutivos)
EJECUTIVOS_ENAMI = [
    ("Jaime Pérez de Arce Araya", "Vicepresidente Ejecutivo"),
    ("Marcelo Rocha Arredondo", "Fiscal"),
    ("Boris Iván Fortín Ruiz", "Gerente Comercial"),
    ("Manuel Antonio Carmona Navea", "Gerente de Plantas"),
    ("Patricia Marchant Cortés", "Gerente de Auditoría Corporativa"),
    ("Hernán Santander González", "Gerente de Fundición Hernán Videla Lira"),
    ("Viviana Ireland Cortés", "Gerente de Fomento y Minería"),
    ("María Cristina Vallejos Cox", "Gerente de Proyectos"),
]
# cargos que compran en la línea Process
PATRON_COMPRA = re.compile(
    r"fundici[oó]n|planta|proyecto|manten|operaci|comercial|abastec|suministro|"
    r"ambient|calidad|ingenier|producci", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


d = json.load(open(P, encoding="utf-8"))
res = d["resultados"]

# localizar ENAMI
idx = None
for i, x in enumerate(res):
    if norm(x["empresa"]) in ("empresa nacional de mineria", "enami"):
        idx = i
        break

hallazgos = []
for nombre, cargo in EJECUTIVOS_ENAMI:
    hallazgos.append({
        "nombre": nombre, "cargo": cargo,
        "linkedin": "",
        "fuente": "direcmin.com/enami-empresa-nacional-de-miner-a/ejecutivos",
        "relevante": bool(PATRON_COMPRA.search(cargo)),
    })

nuevo = {
    "empresa": "ENAMI (Empresa Nacional de Minería)",
    "hallazgos": hallazgos,
    "fuentes_usadas": ["Direcmin: 8 (ejecutivos verificados por cargo)"],
    "notas": ["Cargos de Direcmin. La corrida por LinkedIn se descartó: traía 3 personas de otras "
              "mineras (BHP Spence, Antofagasta Minerals) por homonimia."],
    "n_decisores": len(hallazgos),
    "n_relevantes": sum(1 for h in hallazgos if h["relevante"]),
}

if idx is None:
    res.append(nuevo)
else:
    print(f"reemplazando '{res[idx]['empresa']}' ({res[idx]['n_decisores']} decisores) por la versión Direcmin")
    res[idx] = nuevo

json.dump(d, open(P, "w"), ensure_ascii=False, indent=1)
print(f"\nENAMI: {nuevo['n_decisores']} decisores ({nuevo['n_relevantes']} relevantes)")
for h in hallazgos:
    print(f"  {'★' if h['relevante'] else ' '} {h['nombre'][:30]:32s} {h['cargo']}")
print(f"\nactualizado: {P}")
