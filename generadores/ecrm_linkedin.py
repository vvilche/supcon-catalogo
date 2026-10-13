#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUSCA EL LINKEDIN de cada comprador del eCRM — por nombre + empresa.

POR QUÉ ASÍ (y no validando correos)
------------------------------------------------------------------------------
Validar correos por rebote exige enviar (irreversible) o sondear servidores ajenos por SMTP
(semi-abuso, IP sin reputación, y Proofpoint/Mimecast responden cualquier cosa). No vale.
El camino correcto: el NOMBRE del comprador es dato real y cosechado, y con nombre + empresa se
llega a su LinkedIn, que es un canal de contacto directo y verificable a ojo.

MÉTODO
------------------------------------------------------------------------------
Por cada comprador: web_search("nombre" + empresa + linkedin). Se acepta el resultado solo si:
  - la URL es un perfil /in/ de linkedin.com, y
  - el nombre del perfil comparte los apellidos/pila del comprador (match de tokens).
Se descarta si no matchea: mejor un hueco declarado que un perfil ajeno.

Reanudable: guarda progreso a disco (JSONL), así una corrida cortada no pierde trabajo.
Salida: datos/ecrm_linkedin.json
"""
import json, os, re, sys, time, unicodedata
from hermes_tools import web_search

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
PROG = os.path.join(D, "ecrm_linkedin_progreso.jsonl")

# nombre de búsqueda de la empresa (la sigla del eCRM no sirve para buscar)
EMPRESA_BUSQUEDA = {
    "MLP": "Minera Los Pelambres", "Andina": "Codelco Division Andina",
    "Salvador": "Codelco Division Salvador", "Codelco": "Codelco",
    "Candelaria": "Minera Candelaria", "Caserones": "Minera Caserones",
    "Enami": "ENAMI", "CMP": "Compania Minera del Pacifico", "Pucobre": "Pucobre",
    "Kinross": "Kinross Chile", "Anglo": "Anglo American Chile",
    "JRI": "JRI Ingenieria", "Verne SPA": "Minera Centinela",
    "SGS": "SGS Chile", "Molymetnos": "Molymet", "Ventana": "Minera Ventana",
    "Potrerillos": "Codelco Potrerillos", "Goldfields": "Gold Fields Chile",
    "Minera Tres Valles": "Minera Tres Valles", "Tecnasic": "Tecnasic",
    "Acciona": "Acciona Chile", "ASMAR": "ASMAR Chile", "Beachtel": "Bechtel",
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", " ", s.lower()).strip()


def tokens(nombre):
    return set(t for t in norm(nombre).split() if len(t) > 2)


def es_perfil_linkedin(url):
    return bool(re.search(r"linkedin\.com/(in|pub)/", url or "", re.I))


def nombre_de_url(url):
    """Saca el nombre del slug del perfil: /in/jhonny-guamparito-caceres-886380304"""
    m = re.search(r"linkedin\.com/(?:in|pub)/([^/?#]+)", url or "", re.I)
    if not m:
        return ""
    slug = m.group(1)
    slug = re.sub(r"[-_]\d+$", "", slug)          # quitar el hash final
    return slug.replace("-", " ").replace("_", " ")


def match(nombre_buscado, url):
    """El perfil es de esta persona? (comparte apellido o 2+ tokens)"""
    a = tokens(nombre_buscado)
    b = tokens(nombre_de_url(url))
    if not a or not b:
        return False
    comunes = a & b
    if len(comunes) >= 2:
        return True
    # 1 común alcanza si es raro (apellido poco frecuente) y la búsqueda lo confirma
    return len(comunes) == 1 and len(a) >= 2 and len(b) >= 2


def buscar(nombre, empresa, cargo=""):
    emp = EMPRESA_BUSQUEDA.get(empresa, empresa)
    tries = [f'"{nombre}" {emp} linkedin', f'"{nombre}" linkedin {emp}']
    for q in tries:
        try:
            r = web_search(q, limit=6)
        except Exception:
            time.sleep(2)
            continue
        for it in r.get("data", {}).get("web", []) or []:
            u = it.get("url", "")
            if es_perfil_linkedin(u) and match(nombre, u):
                return {"linkedin": u.split("?")[0], "titulo": it.get("title", "")[:90],
                        "query": q}
        time.sleep(1)
    return None


# ---- cargar compradores y progreso previo ----
d = json.load(open(os.path.join(D, "ecrm_correos_compradores.json"), encoding="utf-8"))
comp = d["compradores"]

hechos = {}
if os.path.exists(PROG):
    for line in open(PROG, encoding="utf-8"):
        try:
            o = json.loads(line)
            hechos[o["nombre"]] = o
        except Exception:
            pass
print(f"compradores: {len(comp)} | ya procesados: {len(hechos)}")

n = int(sys.argv[1]) if len(sys.argv) > 1 else 25
lote = [c for c in comp if c["nombre"] not in hechos][:n]
print(f"procesando lote de {len(lote)}...\n")

with open(PROG, "a", encoding="utf-8") as fh:
    for i, c in enumerate(lote, 1):
        hit = buscar(c["nombre"], c["empresa"])
        reg = {"nombre": c["nombre"], "empresa": c["empresa"], "usd": c["usd"],
               "cotizaciones": c["cotizaciones"],
               "linkedin": hit["linkedin"] if hit else "",
               "titulo": hit["titulo"] if hit else "",
               "correo_inferido": c["correo"]}
        fh.write(json.dumps(reg, ensure_ascii=False) + "\n")
        fh.flush()
        ok = "OK " if hit else "—  "
        print(f"  [{i}/{len(lote)}] {ok} {c['nombre'][:26]:28s} {hit['linkedin'][:62] if hit else ''}")

# resumen acumulado
todos = []
for line in open(PROG, encoding="utf-8"):
    try:
        todos.append(json.loads(line))
    except Exception:
        pass
con = [x for x in todos if x["linkedin"]]
print(f"\n=== ACUMULADO: {len(todos)} procesados | {len(con)} con LinkedIn ({len(con)/len(todos)*100:.0f}%) ===")
json.dump({
    "que_es": ("LinkedIn de los compradores del eCRM, encontrado por nombre + empresa con "
               "web_search. Se valida que el perfil comparta nombre/pila con el comprador."),
    "metodo": "web_search('nombre' + empresa + linkedin); se acepta solo perfil /in/ que matchee el nombre",
    "totales": {"procesados": len(todos), "con_linkedin": len(con),
                "pendientes": len(comp) - len(todos)},
    "compradores": todos,
}, open(os.path.join(D, "ecrm_linkedin.json"), "w"), ensure_ascii=False, indent=1)
print(f"guardado: datos/ecrm_linkedin.json")
