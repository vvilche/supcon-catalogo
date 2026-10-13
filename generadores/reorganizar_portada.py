#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reorganiza el sitio: la PORTADA pasa a ser el catalogo de fichas de producto.

Antes la portada mezclaba 13 tarjetas (estudio de mercado, mockups, JSON internos,
generadores). Ahora:
  index.html        -> redirige/abre el catalogo de fichas (la portada util)
  index_otros.html  -> los demas documentos del proyecto (material, estudios, datos)

Asi el vendedor que entra al sitio ve las fichas, no un menu de cosas tecnicas.
"""
import os, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(BASE, "artefactos")

# 1) mover la portada actual a index_otros.html
idx = os.path.join(BASE, "index.html")
otros = os.path.join(BASE, "index_otros.html")
if os.path.exists(idx) and not os.path.exists(otros):
    shutil.move(idx, otros)
    print("portada anterior movida a index_otros.html")

# 2) la nueva portada = el catalogo de fichas
catalogo = os.path.join(ART, "fichas_vendedores.html")
if os.path.exists(catalogo):
    shutil.copyfile(catalogo, idx)
    print(f"index.html ahora es el catalogo de fichas ({os.path.getsize(idx):,} bytes)")

# 3) arreglar enlaces: dentro de index.html (raiz) las rutas son artefactos/..., no ../artefactos/
s = open(idx, encoding="utf-8").read()
s = s.replace('href="catalogo_supcon.html"', 'href="artefactos/catalogo_supcon.html"')
s = s.replace('href="perfiles_importador_2025.html"', 'href="artefactos/perfiles_importador_2025.html"')
s = s.replace('href="../index_otros.html"', 'href="index_otros.html"')
s = s.replace('<br>Otros documentos del proyecto:',
              '<br>Otros documentos del proyecto (material técnico, estudios de mercado, datos):')
open(idx, "w", encoding="utf-8").write(s)
print("enlaces de la portada corregidos para la raiz")

# 4) en index_otros.html, agregar una vuelta al catalogo
if os.path.exists(otros):
    o = open(otros, encoding="utf-8").read()
    aviso = '''<div style="background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid #2563eb;
border-radius:10px;padding:14px 18px;margin-bottom:22px;font-size:14.5px">
<b>Este es el material de respaldo del proyecto.</b>
Si vienes a vender, entra al <a href="index.html" style="color:#2563eb;font-weight:650">catálogo de
fichas de producto →</a>
</div>'''
    # insertar despues del primer <body...> o al inicio del contenedor
    if "<body" in o:
        i = o.index(">", o.index("<body")) + 1
        o = o[:i] + "\n" + aviso + o[i:]
    else:
        o = aviso + o
    open(otros, "w", encoding="utf-8").write(o)
    print("aviso agregado en index_otros.html")

print("\nlisto. Portada = catalogo de fichas · Secundaria = index_otros.html")
