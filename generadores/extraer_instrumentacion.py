#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el texto de los manuales de INSTRUMENTACION de campo de SUPCON.
Dedupe por MD5. Salida: datos/instrumentacion_extraida.json
"""
import os, json, hashlib

RAIZ = os.path.expanduser("~/Documents/ConocimientoSupcon")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "datos", "instrumentacion_extraida.json")

def md5(p):
    h = hashlib.md5()
    with open(p,"rb") as fh:
        for c in iter(lambda: fh.read(1<<20), b""): h.update(c)
    return h.hexdigest()

def pdf(p):
    try:
        import fitz
        return "\n".join(pg.get_text() for pg in fitz.open(p))
    except Exception as e: return f"__ERROR__ {e}"

# recolectar: instrumentacion de campo, excluyendo certificados y fotos
vistos, docs = {}, []
for dp, dn, fn in os.walk(RAIZ):
    for f in fn:
        if f in ("desktop.ini",".DS_Store"): continue
        p = os.path.join(dp,f); rel = os.path.relpath(p,RAIZ)
        if not ("/Instrument" in rel or "APL Instruments" in rel or "/Instruments/" in rel): continue
        if any(k in f for k in ["Certificate","Proof","Test Report","RoHS","Registration"]): continue
        if f.endswith((".jpg",".png",".bmp",".JPG")): continue
        if not f.endswith(".pdf"): continue
        h = md5(p)
        if h in vistos: continue
        vistos[h] = p
        docs.append((f, rel, p))

print(f"documentos unicos: {len(docs)}")
res = {}
for f, rel, p in sorted(docs):
    t = pdf(p)
    res[f] = {"ruta": rel, "chars": len(t), "texto": t}
    flag = "VACIO" if len(t) < 100 else "ok"
    print(f"  [{flag:5s}] {len(t):>7,}c  {f[:76]}")

json.dump(res, open(OUT,"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: {OUT}")
print(f"documentos: {len(res)} | vacios: {sum(1 for v in res.values() if v['chars']<100)}")
