#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BARRIDO DE PERSONAS POR ÁREA — busca el responsable de cada área en cada empresa.

QUÉ RESUELVE (y por qué NO es buscar correos)
------------------------------------------------------------------------------
Medido: de 3.157 empresas, 2.606 NO tienen ninguna persona identificada, y las áreas que
importan están casi vacías (Instrumentación y Control en 35 empresas, Calidad en 29, Medio
Ambiente en 13). Sin la persona a cargo del área no hay a quién venderle la línea: la matriz
de productos identifica QUÉ necesita la planta, pero falta QUIÉN lo compra.

Y el patrón, medido en las 438 empresas que sí tienen tomadores: tienen Mantenimiento e I&C
(las áreas que ya se venden) y les falta Calidad y Medio Ambiente (las que compran Analítica,
la línea del dolor ambiental). Por eso se busca por ÁREA, no "un contacto por empresa".

CÓMO CORRE
------------------------------------------------------------------------------
Por lotes, con el avance en disco (JSONL). Si se corta, retoma desde donde iba: cada lote
apunta a datos/personas_barrido.jsonl y el progreso a datos/personas_barrido_progreso.json.
La búsqueda usa el atajo que la skill contact-enrichment documenta como el que mejor rinde:
`web_search("Nombre Apellido linkedin")`, que devuelve el perfil ESTRUCTURADO en el snippet
(nombre, headline, empresa) y esquiva el bloqueo de LinkedIn.

PEDIDO DE VICTOR: nombre y cargo. Nada más. Se guarda también el linkedin cuando aparece,
porque viene en el mismo snippet y no cuesta.

USO
  python3 generadores/barrido_personas.py --limite 50          # procesa 50 empresas
  python3 generadores/barrido_personas.py --limite 50 --desde 50
  python3 generadores/barrido_personas.py --estado             # ver el avance
"""
import json, os, re, sys, csv, time, unicodedata, argparse

# `hermes_tools` solo existe dentro del sandbox de execute_code, no como script de terminal.
# Para que esto corra desde la terminal se resuelve un buscador propio: el web_search de Hermes
# via CLI, o en su defecto el endpoint html de DuckDuckGo (que la skill contact-enrichment
# documenta como el que NO tira captcha).
try:
    from hermes_tools import web_search  # type: ignore
    _TIENE_HERMES = True
except Exception:
    _TIENE_HERMES = False

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
SALIDA = os.path.join(D, "personas_barrido.jsonl")
PROGRESO = os.path.join(D, "personas_barrido_progreso.json")

# Áreas y la consulta con la que se busca a su responsable. El orden importa: primero las que
# la matriz de productos necesita y que están vacías (Calidad, Medio Ambiente), después las
# que ya se cubren.
AREAS = [
    ("Medio Ambiente", "jefe de medio ambiente"),
    ("Calidad", "jefe de calidad"),
    ("Instrumentacion y Control", "jefe de instrumentacion y control"),
    ("Mantenimiento", "jefe de mantenimiento"),
    ("Electrico", "jefe electrico"),
    ("Produccion", "jefe de produccion operaciones"),
]

# Limpieza de nombres de empresa que rompen la búsqueda (saltos de línea del scraping).
def limpiar(s):
    return re.sub(r"\s+", " ", (s or "").replace("\n", " ")).strip()


# Empresas a procesar: las que tienen dolor MEDIDO primero (son las que importan), después
# el resto del universo. Se ordena por prioridad para que lo primero que se recorra sea lo útil.
def cargar_empresas():
    emp = []
    # 1) dolor ambiental medido (carga tóxica) — las que importan comercialmente
    p = os.path.join(D, "dolor_ambiental_empresas.json")
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        for e in d["empresas"]:
            emp.append({"empresa": limpiar(e["empresa"]), "rubro": e.get("rubro"),
                        "prioridad": e.get("carga_peligrosa_t") or 0, "origen": "dolor_ambiental"})
    # 2) el resto del universo de prospección
    p2 = os.path.join(D, "universo_senales_completas.json")
    if os.path.exists(p2):
        u = json.load(open(p2, encoding="utf-8"))
        vistos = {x["empresa"].upper() for x in emp}
        for e in u["empresas"]:
            n = limpiar(e.get("empresa"))
            if n.upper() in vistos:
                continue
            vistos.add(n.upper())
            emp.append({"empresa": n, "rubro": e.get("rubro"),
                        "prioridad": e.get("prioridad") or 0, "origen": "universo"})
    # dedupe y orden por prioridad
    emp.sort(key=lambda x: -(x["prioridad"] or 0))
    return emp


def parsear_snippet(desc, empresa):
    """Extrae (nombre, cargo, linkedin) de un snippet de perfil de LinkedIn.

    Los backends devuelven el perfil estructurado con `**Nombre**` y `**Cargo**`.
    """
    out = []
    if not desc:
        return out
    # nombres en negrita de markdown
    bold = re.findall(r"\*\*([^*]{3,60})\*\*", desc)
    if len(bold) < 2:
        return out
    # heurística: el nombre suele ser el primer bold que NO parece cargo,
    # y el cargo el primer bold que SI lo parece
    CARGOS = re.compile(r"jefe|gerente|supervisor|ingenier|coordinador|encargad|director|"
                        r"subgerente|especialista|analista|t[eé]cnico|prevenci[oó]n|"
                        r"instrument|mantenim|mantenci|calidad|ambiente|operacion|producci|"
                        r"electric|control|automatiz|proceso", re.I)
    nombre = None
    cargo = None
    for b in bold:
        b = b.strip()
        if CARGOS.search(b):
            if cargo is None and b.lower() != "experience" and b.lower() != "about":
                cargo = b
            continue
        if nombre is None and len(b.split()) >= 2 and not CARGOS.search(b) \
           and b.lower() not in ("experience", "about", "education", "chile", "santiago"):
            nombre = b
    if nombre and cargo:
        out.append({"nombre": nombre, "cargo": cargo, "fuente": "snippet"})
    return out


def _buscar_ddg(q, limit=4):
    """Fallback sin Hermes: endpoint HTML de DuckDuckGo (el Lite tira CAPTCHA)."""
    import urllib.request, urllib.parse
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"})
    try:
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    except Exception as ex:
        return {"data": {"web": []}, "_err": str(ex)}
    out = []
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?'
                         r'class="result__snippet"[^>]*>(.*?)</a>', html, re.S):
        href, title, snip = m.group(1), m.group(2), m.group(3)
        # DDG envuelve la url real en /l/?uddg=
        if "uddg=" in href:
            try:
                href = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)["uddg"][0]
            except Exception:
                pass
        limpia = lambda s: re.sub(r"<[^>]+>", "", s)
        out.append({"url": href, "title": limpia(title), "description": limpia(snip)})
        if len(out) >= limit:
            break
    return {"data": {"web": out}}


def buscar(empresa, area, consulta):
    """Una consulta. Devuelve personas encontradas."""
    q = f'"{empresa}" {consulta} linkedin'
    try:
        if _TIENE_HERMES:
            r = web_search(query=q, limit=4)
        else:
            r = _buscar_ddg(q, limit=4)
    except Exception as ex:
        return [], f"error: {ex}"
    res = []
    for w in r.get("data", {}).get("web", []):
        u = w.get("url", "")
        d = w.get("description", "") or ""
        if "linkedin.com/in/" in u:
            # limpiar la url canonica
            m = re.match(r"(https?://[a-z]{0,3}\.?linkedin\.com/in/[^/?#]+)", u)
            link = m.group(1) if m else u
            for p in parsear_snippet(d, empresa):
                p["linkedin"] = link
                res.append(p)
        else:
            # snippet sin URL de LinkedIn: puede traer el cargo igual
            for p in parsear_snippet(d, empresa):
                p["linkedin"] = ""
                res.append(p)
    return res, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=25)
    ap.add_argument("--desde", type=int, default=0)
    ap.add_argument("--estado", action="store_true")
    ap.add_argument("--areas", default="", help="solo estas areas, separadas por coma")
    a = ap.parse_args()

    if os.path.exists(PROGRESO):
        pr = json.load(open(PROGRESO, encoding="utf-8"))
    else:
        pr = {"empresas_hechas": [], "empresas_con_personas": 0, "personas": 0}

    if a.estado:
        emp = cargar_empresas()
        print(f"empresas en cola:      {len(emp):,}")
        print(f"empresas procesadas:   {len(pr['empresas_hechas']):,}")
        print(f"empresas con personas: {pr['empresas_con_personas']:,}")
        print(f"personas encontradas:  {pr['personas']:,}")
        if pr["empresas_hechas"]:
            print(f"ultima: {pr['empresas_hechas'][-1]}")
        return

    emp = cargar_empresas()
    hechas = set(pr["empresas_hechas"])
    cola = [e for e in emp if e["empresa"] not in hechas]
    lote = cola[a.desde:a.desde + a.limite]
    print(f"cola: {len(cola):,} empresas | procesando {len(lote)}")

    areas = AREAS
    if a.areas:
        sel = {x.strip().lower() for x in a.areas.split(",")}
        areas = [x for x in AREAS if x[0].lower() in sel]

    fh = open(SALIDA, "a", encoding="utf-8")
    t0 = time.time()
    for i, e in enumerate(lote, 1):
        emp_n = e["empresa"]
        encontrados = []
        for area, consulta in areas:
            ps, err = buscar(emp_n, area, consulta)
            for p in ps:
                p.update({"empresa": emp_n, "area": area, "rubro": e.get("rubro"),
                          "origen_empresa": e.get("origen")})
                encontrados.append(p)
        # dedupe por (nombre, cargo)
        vistos = set()
        uniq = []
        for p in encontrados:
            k = (p["nombre"].lower(), p["cargo"].lower())
            if k in vistos:
                continue
            vistos.add(k)
            uniq.append(p)
        for p in uniq:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")
        fh.flush()
        pr["empresas_hechas"].append(emp_n)
        if uniq:
            pr["empresas_con_personas"] += 1
        pr["personas"] += len(uniq)
        if i % 5 == 0 or i == len(lote):
            json.dump(pr, open(PROGRESO, "w"), ensure_ascii=False)
            el = time.time() - t0
            print(f"  [{i}/{len(lote)}] {pr['personas']} personas | "
                  f"{pr['empresas_con_personas']} empresas con dato | {el:.0f}s")
    fh.close()
    json.dump(pr, open(PROGRESO, "w"), ensure_ascii=False)
    print(f"\nhecho: {len(lote)} empresas, {pr['personas']} personas acumuladas")


if __name__ == "__main__":
    main()
