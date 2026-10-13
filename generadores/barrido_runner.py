#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BARRIDO DE PERSONAS — runner reanudable.

POR QUÉ ASÍ
------------------------------------------------------------------------------
Medido: cada empresa cuesta 4 consultas (una por área), y el buscador de Hermes se invoca desde
execute_code (hermes_tools solo vive ahí; el fallback DDG devuelve "anomaly detection"). En la
práctica son ~50 llamadas por bloque de ~24 empresas.

Con 3.157 empresas eso son ~6.500 llamadas: NO cabe en una sesión de chat. Por eso el barrido
se guarda en JSONL y este runner es REANUDABLE: cada bloque lee el progreso y sigue donde iba.
Así se puede correr por tandas, cuantas veces haga falta, sin repetir trabajo.

RENDIMIENTO MEDIDO (44 empresas)
  ~2,5 personas útiles por empresa (108 personas en 44 empresas)
  ~8-14 personas en las cuentas grandes (Codelco 14, Arauco 9, Escondida 8)
  0 personas en varias empresas chicas (el valor se concentra arriba)
  Áreas que estaban vacías y ahora se llenan: Medio Ambiente 22, Calidad 14

USO (desde execute_code, que es donde hay web_search)
    from hermes_tools import web_search
    exec(open("generadores/barrido_runner.py").read())
    correr_bloque(web_search, n_empresas=24)

ESTADO
    python3 generadores/barrido_personas.py --estado
"""
import json, os, re, time

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
SAL = os.path.join(D, "personas_barrido.jsonl")
PROG = os.path.join(D, "personas_barrido_progreso.json")

import sys
sys.path.insert(0, os.path.join(BASE, "generadores"))
from personas_motor import AREAS_CONSULTA, parsear_snippet, limpiar_persona, fusionar


def _cola():
    """Empresas ordenadas por prioridad (dolor primero)."""
    emp = json.load(open(os.path.join(D, "universo_senales_completas.json"), encoding="utf-8"))
    da = json.load(open(os.path.join(D, "dolor_ambiental_empresas.json"), encoding="utf-8"))
    prio = {e["empresa"].upper(): e.get("carga_peligrosa_t") or 0 for e in da["empresas"]}
    lista = []
    for e in emp["empresas"]:
        n = re.sub(r"\s+", " ", (e.get("empresa") or "").replace("\n", " ")).strip()
        if n:
            lista.append({"empresa": n, "rubro": e.get("rubro"),
                          "prio": prio.get(n.upper(), e.get("prioridad") or 0)})
    lista.sort(key=lambda x: -(x["prio"] or 0))
    return lista


def _dedupe(path):
    seen = {}
    if os.path.exists(path):
        for l in open(path, encoding="utf-8"):
            try:
                r = json.loads(l)
            except Exception:
                continue
            k = (r["nombre"].lower(), r["empresa"].upper())
            if k not in seen or len(r.get("cargo", "")) > len(seen[k].get("cargo", "")):
                seen[k] = r
    return list(seen.values())


def estado():
    lista = _cola()
    pr = json.load(open(PROG, encoding="utf-8")) if os.path.exists(PROG) else {"hechas": []}
    per = _dedupe(SAL)
    from collections import Counter
    print(f"empresas en cola:     {len(lista):,}")
    print(f"empresas procesadas:  {len(pr.get('hechas', [])):,}")
    print(f"empresas pendientes:  {len(lista) - len(pr.get('hechas', [])):,}")
    print(f"personas:             {len(per):,}")
    print(f"empresas con dato:    {len({r['empresa'] for r in per}):,}")
    print(f"\npor área:")
    for k, v in Counter(r["area"] for r in per).most_common():
        print(f"   {k:28s} {v}")
    print(f"\npersonas por empresa (top 10):")
    for e, n in Counter(r["empresa"] for r in per).most_common(10):
        print(f"   {e[:46]:48s} {n}")


def correr_bloque(web_search, n_empresas=24, verbose=True):
    """Procesa n_empresas y devuelve las personas nuevas. Reanudable."""
    lista = _cola()
    pr = json.load(open(PROG, encoding="utf-8")) if os.path.exists(PROG) else \
        {"hechas": [], "personas": 0, "con_dato": 0}
    hechas = set(pr["hechas"])
    cola = [e for e in lista if e["empresa"] not in hechas]
    lote_total = cola[:n_empresas]
    t0 = time.time()
    nuevas = []

    for e in lote_total:
        enc = []
        for area, cons in AREAS_CONSULTA:
            q = f'"{e["empresa"]}" {cons} linkedin'
            try:
                r = web_search(query=q, limit=4)
            except Exception:
                continue
            for w in r.get("data", {}).get("web", []):
                u = w.get("url", "") or ""
                d = w.get("description", "") or ""
                link = ""
                m = re.match(r"(https?://[a-z]{0,3}\.?linkedin\.com/in/[^/?#]+)", u)
                if m:
                    link = m.group(1)
                for p in parsear_snippet(d):
                    cl = limpiar_persona(p["nombre"], p["cargo"], e["empresa"])
                    if cl:
                        cl.update({"rubro": e.get("rubro"), "linkedin": link,
                                   "encontrado_por": area})
                        enc.append(cl)
        uniq = fusionar(enc)
        for p in uniq:
            p["empresa"] = e["empresa"]
            p["rubro"] = e.get("rubro")
            nuevas.append(p)
        pr["hechas"].append(e["empresa"])
        if uniq:
            pr["con_dato"] = pr.get("con_dato", 0) + 1

    # escribir y deduplicar el archivo completo
    todos = _dedupe(SAL)
    vistos = {(r["nombre"].lower(), r["empresa"].upper()) for r in todos}
    for p in nuevas:
        k = (p["nombre"].lower(), p["empresa"].upper())
        if k not in vistos:
            todos.append(p)
            vistos.add(k)
    with open(SAL, "w", encoding="utf-8") as fh:
        for r in todos:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    pr["personas"] = len(todos)
    json.dump(pr, open(PROG, "w"), ensure_ascii=False)

    if verbose:
        print(f"[{len(pr['hechas'])}/{len(lista)}] +{len(nuevas)} nuevas | "
              f"{len(todos)} personas | {pr['con_dato']} empresas con dato | "
              f"{time.time()-t0:.0f}s")
    return nuevas


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--estado", action="store_true")
    a = ap.parse_args()
    if a.estado:
        estado()
    else:
        print("Correr desde execute_code con: correr_bloque(web_search, n_empresas=24)")
        print("(web_search no existe como comando de terminal: hermes_tools solo vive en el sandbox)")
        estado()
