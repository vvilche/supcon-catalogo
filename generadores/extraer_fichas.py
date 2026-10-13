#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el texto de las 53 fichas 1-Pager (PDF y PPTX) + las fichas Hobre.
Determinista: cero LLM. Salida: fichas_extraidas.json con el texto crudo por ficha.
"""
# -*- coding: utf-8 -*-
"""Resuelve las rutas desde la ubicacion del propio archivo (autocontenido).
BASE = raiz del repo; DATOS = datos/; SALIDA = artefactos/.
El material fuente del fabricante NO vive en el repo: se lee de FUENTE_MATERIAL."""
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")
SALIDA = os.path.join(BASE, "artefactos")
# ruta del material del fabricante (PDF/PPTX), fuera del repo
FUENTE_MATERIAL = os.path.expanduser("~/Documents/ConocimientoSupcon")
import os, re, json, zipfile, html, hashlib

RAIZ = FUENTE_MATERIAL
OUT = os.path.join(DATOS, "fichas_extraidas.json")

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def extraer_pdf(p):
    try:
        import fitz
        d = fitz.open(p)
        return "\n".join(pg.get_text() for pg in d)
    except Exception as e:
        return f"__ERROR_PDF__ {e}"

def extraer_pptx(p):
    try:
        out = []
        with zipfile.ZipFile(p) as z:
            slides = sorted(
                [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                key=lambda x: int(re.findall(r"\d+", x)[0]))
            for n in slides:
                x = z.read(n).decode("utf-8", "ignore")
                ts = re.findall(r"<a:t>(.*?)</a:t>", x, re.S)
                txt = " ".join(html.unescape(t) for t in ts if t.strip())
                if txt: out.append(f"[slide {n.split('slide')[-1].replace('.xml','')}] {txt}")
        return "\n".join(out)
    except Exception as e:
        return f"__ERROR_PPTX__ {e}"

# Recolectar unicos
vistos, prod = {}, []
for dp, dn, fn in os.walk(RAIZ):
    for f in fn:
        if f in ("desktop.ini", ".DS_Store"): continue
        p = os.path.join(dp, f); rel = os.path.relpath(p, RAIZ)
        if "1-Pager" in rel or "Supcon Product information" in rel:
            h = md5(p)
            if h in vistos: continue
            vistos[h] = p; prod.append((rel, p))

# Las 53 fichas 1-Pager (las vendibles) + las Hobre
fichas = [(rel, p) for rel, p in prod if "1-Pager" in rel]
hobre = [(rel, p) for rel, p in prod if "Analyser(Hobre)" in rel]
sel = fichas + [x for x in hobre if x[0] not in {y[0] for y in fichas}]

# Dedupe por nombre de archivo (varias copias del mismo 1-Pager en carpetas distintas)
por_nombre = {}
for rel, p in sel:
    nombre = os.path.basename(rel)
    if nombre not in por_nombre:
        por_nombre[nombre] = (rel, p)
print("fichas unicas por nombre:", len(por_nombre))

res = {}
for i, (nombre, (rel, p)) in enumerate(sorted(por_nombre.items()), 1):
    ext = os.path.splitext(nombre)[1].lower()
    if ext == ".pdf":    txt = extraer_pdf(p)
    elif ext == ".pptx": txt = extraer_pptx(p)
    else:                txt = f"__FORMATO_NO_SOPORTADO__ {ext}"
    res[nombre] = {"ruta": rel, "ext": ext, "chars": len(txt), "texto": txt}
    flag = "VACIO" if len(txt) < 50 else ("ERROR" if txt.startswith("__ERROR") else "ok")
    print(f"{i:2d}. [{flag:5s}] {len(txt):6d} chars  {nombre[:78]}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("\nguardado:", OUT)
print("fichas:", len(res))
vacias = [k for k, v in res.items() if v["chars"] < 50]
print("vacias o con error:", len(vacias), vacias)
