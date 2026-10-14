#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barrido de decisores para las 52 empresas del target de la campaña que NO estaban en el buscador.

Cubre los rubros que el barrido anterior no tocó: alimentos, celulosa/papel, química y
combustibles, aguas, construcción y GENERACIÓN (31 plantas, el hueco más grande).

Guarda empresa por empresa (el buscador murió una vez guardando solo al final y se perdieron 130).

Uso: python3 generadores/barrido_campana.py
"""
import json, os, subprocess, sys, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMPRESAS = json.load(open("/tmp/empresas_final.json", encoding="utf-8"))
LOGF = "/tmp/barrido_campana.log"


def log(m):
    print(m, flush=True)
    with open(LOGF, "a") as f:
        f.write(m + "\n")


log(f"=== BARRIDO CAMPAÑA: {len(EMPRESAS)} empresas ===")
ok, fail = 0, 0
for i, emp in enumerate(EMPRESAS, 1):
    log(f"\n[{i}/{len(EMPRESAS)}] {emp}")
    try:
        r = subprocess.run(
            [sys.executable, "-B", os.path.join(BASE, "generadores", "buscador_decisores.py"),
             "--empresa", emp, "--web"],
            capture_output=True, text=True, timeout=280)
        salida = (r.stdout or "")[-400:]
        log(salida.strip()[:400])
        if "decisores:" in (r.stdout or ""):
            ok += 1
        else:
            fail += 1
    except subprocess.TimeoutExpired:
        log("  TIMEOUT")
        fail += 1
    except Exception as e:
        log(f"  ERROR: {e}")
        fail += 1
    time.sleep(1)

log(f"\n=== FIN: {ok} ok, {fail} sin resultado ===")
