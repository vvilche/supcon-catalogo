#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el dict FICHAS de generar_fichas_producto.py (1a entrega: analizadores)
a datos/fichas_1_datos.json, para poder consolidar las 4 entregas de forma uniforme.

Por que existe: la 1a entrega tiene las fichas embebidas en el generador en vez de
en un JSON aparte. El resto de las entregas si leen de datos/*.json, asi que esta
normalizacion es lo que permite consolidarlas sin duplicar codigo.
"""
import os, json, importlib.util, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

# cargar el generador como modulo para leer su dict FICHAS
gen = os.path.join(BASE, "generadores", "generar_fichas_producto.py")
src = open(gen, encoding="utf-8").read()
# aislar solo el bloque FICHAS = {...} y evaluarlo (el resto del script escribe HTML)
ini = src.index("FICHAS = {")
# buscar el cierre: linea con solo "}" a nivel 0 despues del inicio
lineas = src[ini:].split("\n")
prof = 0
fin = None
for i, ln in enumerate(lineas):
    prof += ln.count("{") - ln.count("}")
    if i > 0 and prof == 0:
        fin = i
        break
bloque = "\n".join(lineas[:fin + 1]) if fin is not None else src[ini:]
ns = {"json": json}
exec(bloque, ns)
F = ns["FICHAS"]

# Las fichas propias (CEMS 5000, Flare CEMS) NO estan dentro del dict inicial:
# se agregan despues con FICHAS["..."] = {...}. Hay que capturarlas aparte.
# Se busca cada asignacion posterior a nivel 0 y se evalua su bloque.
resto = src[src.index(bloque) + len(bloque):] if bloque in src else ""
for m in re.finditer(r'FICHAS\["([^"]+)"\]\s*=\s*\{', resto):
    nombre = m.group(1)
    sub = resto[m.end() - 1:]
    prof2, fin2 = 0, None
    for i, ln in enumerate(sub.split("\n")):
        prof2 += ln.count("{") - ln.count("}")
        if i > 0 and prof2 == 0:
            fin2 = i
            break
    if fin2 is None:
        continue
    ns2 = {}
    exec("_X = " + "\n".join(sub.split("\n")[:fin2 + 1]), ns2)
    F[nombre] = ns2["_X"]
    print(f"   + ficha propia capturada: {nombre}")

# normalizar a las claves estandar de las otras entregas
norm = {}
for nombre, x in F.items():
    norm[nombre] = {
      "familia": x.get("familia", "Analizadores Hobre"),
      "descripcion": x.get("descripción") or x.get("descripcion") or "",
      "beneficios": x.get("beneficios", []),
      "clientes_target": x.get("clientes_target") or x.get("clientes") or [],
      "competencia": x.get("competencia", ""),
      "argumentos_venta": x.get("argumentos_venta") or x.get("argumentos") or [],
      "objeciones": x.get("objeciones", []),
      "preguntas_tecnicas": x.get("preguntas_tecnicas") or x.get("preguntas") or [],
      "fuente": x.get("fuente", ""),
    }

out = os.path.join(D, "fichas_1_datos.json")
json.dump(norm, open(out, "w"), ensure_ascii=False, indent=1)
print(f"extraidas {len(norm)} fichas de la 1a entrega -> {out}")
for n, f in norm.items():
    campos = sum(1 for k in ("descripcion","beneficios","clientes_target","competencia",
                             "argumentos_venta","objeciones","preguntas_tecnicas","fuente") if f.get(k))
    print(f"   {n:42s} {campos}/8 campos  (objeciones={len(f['objeciones'])}, preguntas={len(f['preguntas_tecnicas'])})")
