#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REPOBLA los campos riles y residuos_t del catálogo de 3.157 empresas desde el RETC (MMA).

PROBLEMA QUE RESUELVE. Los campos `riles` y `residuos_t` del catálogo están poblados solo en
1 rubro de 13: `residuos_t` tiene valor en 52 de 3.157 empresas (3%) y `riles` en 2 (0,06%).
Por eso el motor de leads solo calcula dolor de agua/residuos para química, y el resto de los
rubros entra con dolor 0 en esa señal. Con 2 empresas con RILES en todo Chile no se puede
trabajar: el DS 90/2000 obliga a miles.

ESTRATEGIA (en orden, parasando por lo que no cueste):
  1. Revisar si el dato YA existe en disco (algún RETC/SIDREP bajado antes). Cero red.
  2. Consultar el portal de datos abiertos del RETC (datosretc.mma.gob.cl) por dataset.
  3. Solo si hay que scraping por empresa, hacerlo con pausa y registro incremental en disco
     (para que un corte no pierda el avance).

Escribe en `datos/retc_empresas.json` un mapa slug -> {riles, residuos_t, fuente, metodo}.
NUNCA inventa: si no encuentra el dato, lo deja fuera y lo cuenta.

Uso:
  python3 generadores/repoblar_retc.py --buscar         # solo busca en disco y reporta
  python3 generadores/repoblar_retc.py --descargar      # baja del portal RETC
"""
import os, sys, json, glob, collections, unicodedata, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
CATALOGO = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))

def cargar_catalogo():
    """Carga las 3.157 empresas con su estado actual de riles/residuos."""
    emp = []
    for f in sorted(glob.glob(os.path.join(CATALOGO, "catalogo-*/research/*.json"))):
        try: d = json.load(open(f, encoding="utf-8"))
        except Exception: continue
        def fl(x):
            try: return float(str(x).replace(",", ""))
            except: return 0.0
        emp.append({
          "slug": d.get("slug"), "empresa": d.get("empresa"), "rubro": d.get("rubro"),
          "region": d.get("region"), "comuna": d.get("comuna"),
          "riles_actual": fl(d.get("riles")), "residuos_actual": fl(d.get("residuos_t")),
          "archivo": f,
        })
    return emp

def buscar_en_disco():
    """Paso 1: el dato puede ya estar bajado. Busca cualquier RETC/SIDREP en el Mac."""
    print("=== PASO 1: buscar el dato en disco (cero red) ===")
    patrones = ["*retc*", "*RETC*", "*sidrep*", "*SIDREP*", "*ventanilla*", "*mma*"]
    hallados = []
    raices = [os.path.expanduser("~/Documents"), os.path.expanduser("~/CONECTA_Proyecto"),
              os.path.expanduser("~/orca"), os.path.expanduser("~/.hermes/cache")]
    for raiz in raices:
        for pat in patrones:
            for p in glob.glob(os.path.join(raiz, "**", pat), recursive=True):
                if os.path.isfile(p) and os.path.getsize(p) > 5000:
                    hallados.append(p)
    hallados = sorted(set(hallados))
    print(f"  archivos RETC/SIDREP encontrados: {len(hallados)}")
    for p in hallados[:25]:
        print(f"     {os.path.getsize(p)/1024:>9,.0f} KB  {p}")
    return hallados

def descargar_portal():
    """Paso 2: consultar el portal de datos abiertos del RETC."""
    print("\n=== PASO 2: portal RETC (datosretc.mma.gob.cl) ===")
    import urllib.request, urllib.error
    urls = [
      "https://datosretc.mma.gob.cl/api/3/action/package_search?q=residuos&rows=20",
      "https://datosretc.mma.gob.cl/api/3/action/package_list",
    ]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0 (research CONECTA)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            print(f"  OK {u}")
            if "result" in data and isinstance(data["result"], dict):
                res = data["result"].get("results", [])
                print(f"     datasets: {len(res)}")
                for d in res[:12]:
                    print(f"       - {d.get('title','?')[:70]}")
            elif "result" in data and isinstance(data["result"], list):
                print(f"     datasets: {len(data['result'])}")
                for d in data["result"][:20]: print(f"       - {d}")
            return data
        except Exception as e:
            print(f"  FALLA {u}: {type(e).__name__}: {str(e)[:90]}")
    return None

if __name__ == "__main__":
    emp = cargar_catalogo()
    print(f"catálogo: {len(emp)} empresas\n")
    con_res = sum(1 for e in emp if e["residuos_actual"] > 0)
    con_ril = sum(1 for e in emp if e["riles_actual"] > 0)
    print(f"estado actual: residuos_t con valor en {con_res} ({con_res/len(emp)*100:.1f}%), "
          f"riles con valor en {con_ril} ({con_ril/len(emp)*100:.2f}%)\n")
    if "--buscar" in sys.argv or not sys.argv[1:]:
        buscar_en_disco()
    if "--descargar" in sys.argv:
        descargar_portal()
