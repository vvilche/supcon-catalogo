#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baja las fuentes de dolor que faltan: multas SEC y proyectos SEIA.

CEN (completitud y calidad) ya esta en disco:
  /Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo/cen_*.json

Salidas: datos/fuentes/multas_sec.json, datos/fuentes/seia_proyectos.json
"""
import os, json, urllib.request, urllib.parse, re, html as H

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "datos", "fuentes")
os.makedirs(OUT, exist_ok=True)

def get(u, timeout=60):
    req = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0 (research CONECTA)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def get_text(u, timeout=60):
    return get(u, timeout).decode("utf-8", "replace")

# ---------- 1. MULTAS SEC ----------
# sec.cl publica "Resoluciones de sancion" en su portal de datos/transparencia.
print("=== multas SEC ===")
candidatas = [
  "https://www.sec.cl/noticias/",
  "https://www.sec.cl/sala-de-prensa/",
  "https://datos.gob.cl/api/3/action/package_search?q=multas%20SEC&rows=10",
  "https://datos.gob.cl/api/3/action/package_search?q=sanciones%20electricas&rows=10",
]
for u in candidatas:
    try:
        t = get_text(u, 40)
        print(f"  OK  {u[:70]}  ({len(t):,} chars)")
        if "datos.gob.cl" in u:
            d = json.loads(t)
            for ds in d.get("result",{}).get("results",[])[:6]:
                print(f"      dataset: {ds.get('title','')[:66]}")
                for r in ds.get("resources",[])[:3]:
                    print(f"        {r.get('format','?'):6s} {r.get('url','')[:100]}")
    except Exception as e:
        print(f"  FALLA {u[:60]}: {type(e).__name__}: {str(e)[:60]}")

# ---------- 2. SEIA ----------
# El SEIA tiene API publica de proyectos.
print("\n=== SEIA ===")
seia = [
  "https://seia.sea.gob.cl/expediente/expedientes.php?modo=ficha&id_expediente=",
  "https://api.sea.gob.cl/v1/proyectos?page=1",
  "https://seia.sea.gob.cl/buscarExpedientesAjax.php",
]
for u in seia:
    try:
        t = get_text(u, 40)
        print(f"  OK  {u[:70]}  ({len(t):,} chars)")
        print(f"      inicio: {t[:160]}")
    except Exception as e:
        print(f"  FALLA {u[:60]}: {type(e).__name__}: {str(e)[:70]}")
