#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Busca en LinkedIn los contactos de Direcmin que NO traían perfil.

POR QUÉ
------------------------------------------------------------------------------
Direcmin publica nombre y cargo pero NO el LinkedIn. De los 518 contactos validados, 210 vienen de
Direcmin y quedan sin perfil. Con nombre + empresa + cargo se puede buscar el perfil en la web
(AIsa/Tavily), que además devuelve la HISTORIA LABORAL: eso permite verificar si la persona sigue
en la empresa o se fue (medido: Christian Caviedes figuraba en Codelco y hoy está en Capstone Copper).

GUARDA EMPRESA POR EMPRESA (no al final): una corrida cortada pierde todo si guarda al final.

Salida: datos/linkedin_direcmin.json
"""
import json, os, re, subprocess, sys, time, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(D, "linkedin_direcmin.json")
LOGF = "/tmp/linkedin_direcmin.log"


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def log(m):
    print(m, flush=True)
    with open(LOGF, "a") as f:
        f.write(m + "\n")


plan = json.load(open(os.path.join(D, "plan_accion_limpio.json"), encoding="utf-8"))["plan"]

# los que no tienen linkedin (todos de Direcmin) -> la lista de trabajo
pend = []
for p in plan:
    for c in p["contactos"]:
        if c.get("linkedin"):
            continue
        pend.append({"empresa": p["empresa"], "nombre": c["nombre"], "cargo": c["cargo"],
                     "region": p.get("region", ""), "linea": c.get("linea", ""),
                     "que_ofrecer": c.get("que_ofrecer", "")})

# estado (reanudable)
hechos = {}
if os.path.exists(OUT):
    hechos = {k: v for k, v in json.load(open(OUT, encoding="utf-8")).get("contactos", {}).items()}

log(f"=== BUSCAR LINKEDIN DE DIRECMIN: {len(pend)} contactos (ya hechos: {len(hechos)}) ===")


def buscar(nombre, empresa, cargo):
    """Busca el perfil con AIsa web-search y devuelve (url, evidencia)."""
    q = f'"{nombre}" {empresa} linkedin'
    try:
        r = subprocess.run(["aisa", "web-search", q, "--limit", "3"],
                           capture_output=True, text=True, timeout=120)
        raw = r.stdout or ""
    except Exception as e:
        return None, f"error: {e}"
    # buscar URLs de linkedin en la salida
    urls = re.findall(r'"url":\s*"(https?://[a-z]{0,3}\.?linkedin\.com/in/[^"]+)"', raw)
    if not urls:
        urls = re.findall(r'(https?://[a-z]{0,3}\.?linkedin\.com/in/[^\s"\\]+)', raw)
    if not urls:
        return None, ""
    url = urls[0].replace("\\u00e1", "á").replace("\\u00e9", "é").replace("\\u00ed", "í")
    # evidencia: el bloque de experiencia de la misma salida
    ev = ""
    m = re.search(r'"content":\s*"(.{0,900})', raw, re.S)
    if m:
        ev = m.group(1)[:900].replace("\\n", " ")
    return url, ev


ok, fail = 0, 0
for i, p in enumerate(pend, 1):
    clave = f"{norm(p['empresa'])}|{norm(p['nombre'])}"
    if clave in hechos:
        continue
    log(f"\n[{i}/{len(pend)}] {p['nombre']} | {p['empresa'][:30]}")
    url, ev = buscar(p["nombre"], p["empresa"], p["cargo"])
    # ¿la evidencia menciona la empresa? (para no dar por bueno un homónimo)
    pert = bool(url) and (norm(p["empresa"]).split()[0] in norm(ev) if p["empresa"] else False)
    hechos[clave] = {"nombre": p["nombre"], "empresa": p["empresa"], "cargo": p["cargo"],
                     "region": p["region"], "linea": p["linea"], "que_ofrecer": p["que_ofrecer"],
                     "linkedin": url or "", "evidencia": ev[:400],
                     "pertenece": pert, "buscado": True}
    if url:
        ok += 1
        log(f"   {'✓' if pert else '~'} {url[:70]}")
    else:
        fail += 1
        log("   sin resultado")
    # GUARDADO INCREMENTAL
    json.dump({"que_es": "LinkedIn hallado para los contactos de Direcmin (que no traen perfil).",
               "totales": {"buscados": len(hechos), "con_url": ok, "sin_url": fail},
               "contactos": hechos},
              open(OUT, "w"), ensure_ascii=False, indent=1)
    time.sleep(1)

log(f"\n=== FIN: {ok} con perfil, {fail} sin resultado ===")
