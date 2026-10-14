#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barrido de decisores para las 370 empresas del universo RETC que faltan
(159 GRANDES + 211 MEDIANAS; los duplicados del RETC —misma razón social en varias plantas—
se barren una vez por razón social única, pero se registran todas las variantes).

Guarda empresa por empresa. Uso: python3 generadores/barrido_universo.py
"""
import json, os, re, subprocess, sys, time, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
LOGF = "/tmp/barrido_universo.log"


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def log(m):
    print(m, flush=True)
    with open(LOGF, "a") as f:
        f.write(m + "\n")


falt = json.load(open(os.path.join(D, "faltantes_universo.json"), encoding="utf-8"))["faltantes"]
procesadas = set()
estado = os.path.join(D, "barrido_universo_estado.json")
if os.path.exists(estado):
    procesadas = set(json.load(open(estado, encoding="utf-8")))

# ordenar: grandes primero por carga peligrosa
falt.sort(key=lambda x: (x["tier"] != "GRANDE", -(x["residuos_t"] or 0)))
# únicas por razón social (los duplicados del RETC son la misma empresa en otra planta)
vistas, lista = set(), []
for e in falt:
    k = norm(e["empresa"])
    if k in vistas or k in procesadas:
        continue
    vistas.add(k)
    lista.append(e["empresa"])

log(f"=== BARRIDO UNIVERSO: {len(lista)} empresas únicas (de {len(falt)} registros del RETC) ===")
log(f"    grandes primero, luego medianas | ya procesadas antes: {len(procesadas)}")

ok, fail = 0, 0
for i, emp in enumerate(lista, 1):
    log(f"\n[{i}/{len(lista)}] {emp}")
    try:
        r = subprocess.run(
            [sys.executable, "-B", os.path.join(BASE, "generadores", "buscador_decisores.py"),
             "--empresa", emp, "--web"],
            capture_output=True, text=True, timeout=280)
        salida = (r.stdout or "")
        log(salida.strip()[-300:])
        if "decisores:" in salida:
            ok += 1
        else:
            fail += 1
    except subprocess.TimeoutExpired:
        log("  TIMEOUT")
        fail += 1
    except Exception as ex:
        log(f"  ERROR: {ex}")
        fail += 1
    procesadas.add(norm(emp))
    json.dump(sorted(procesadas), open(estado, "w"), ensure_ascii=False, indent=1)
    time.sleep(1)

log(f"\n=== FIN: {ok} con resultado, {fail} sin resultado ===")
