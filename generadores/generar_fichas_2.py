#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renderiza las fichas comerciales de la 2a entrega (SIS, PLC, CCS, Software, Plataforma, Ciber).
Lee datos/fichas_2_datos.json (lo produce fichas_2_datos.py) y datos/fichas_extraidas.json.

Uso:  python3 generar_fichas_2.py
Salida: artefactos/fichas_producto_2.html
"""
import os, json, html as H, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")
SALIDA = os.path.join(BASE, "artefactos")

F = json.load(open(os.path.join(DATOS, "fichas_2_datos.json"), encoding="utf-8"))

def esc(s): return H.escape(str(s))

def fila(k, v):
    if isinstance(v, list):
        v = "".join(f'<div class="li">{esc(x)}</div>' for x in v)
    return f'<tr><td class="k">{esc(k)}</td><td class="v">{v}</td></tr>'

def ficha(nombre, f):
    obj = "".join(
        f'<div class="obj"><div class="q">{esc(o[0])}</div>'
        f'<div class="r">{esc(o[1]) if o[1] else "&mdash;"}</div></div>'
        for o in f["objeciones"])
    return f"""
<div class="ficha" id="f-{esc(nombre).replace(' ','-').replace('(','').replace(')','')}">
  <div class="fh"><h3>{esc(nombre)}</h3><span class="fam">{esc(f["familia"])}</span></div>
  <table>
    {fila("Nombre de Producto o Servicio", nombre)}
    {fila("Descripción del Servicio", f["descripcion"])}
    {fila("Beneficios", f["beneficios"])}
    {fila("Clientes Target", f["clientes_target"])}
    {fila("Competencia", f["competencia"])}
    {fila("Argumentos de Venta", f["argumentos_venta"])}
    <tr><td class="k">Manejo de Objeciones</td><td class="v">{obj}</td></tr>
    {fila("Preguntas Técnicas", f["preguntas_tecnicas"])}
  </table>
  <div class="fuente">Fuente: {esc(f["fuente"])}</div>
</div>"""

# agrupar por familia
por_fam = collections.defaultdict(list)
for n, f in F.items():
    por_fam[f["familia"]].append(n)

# chips de navegacion
chips = "".join(f'<a class="chip" href="#f-{esc(n).replace(" ","-").replace("(","").replace(")","")}">{esc(n)}</a>'
                for n in F)

cuerpo = ""
for fam, items in por_fam.items():
    cuerpo += f'<div class="bloque"><div class="bh">{esc(fam)} <span>{len(items)} ficha{"s" if len(items)!=1 else ""}</span></div>'
    for n in items:
        cuerpo += ficha(n, F[n])
    cuerpo += '</div>'

porc = sum(1 for f in F.values() if "POR COMPLETAR" in json.dumps(f, ensure_ascii=False))

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fichas de Producto SUPCON — Segunda entrega</title><style>
:root{{--bg:#f8fafc;--card:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--tx);font-family:Inter,-apple-system,sans-serif;font-size:14.5px;line-height:1.55;padding:30px 26px 80px}}
.wrap{{max-width:1200px;margin:0 auto}}
.hero{{background:var(--card);border:1px solid var(--bd);border-radius:20px;padding:26px 30px;margin-bottom:20px}}
.hero h1{{font-size:24px;font-weight:650;letter-spacing:-.4px;margin-bottom:6px}}
.hero p{{color:var(--mu);font-size:14px;max-width:860px}}
.idx{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}}
.chip{{border:1px solid var(--bd);background:var(--card);border-radius:100px;padding:7px 15px;font-size:13px;color:var(--ac);text-decoration:none;font-weight:550}}
.chip:hover{{background:var(--acs)}}
.bloque{{margin-bottom:26px}}
.bh{{font-size:12px;font-weight:650;text-transform:uppercase;letter-spacing:.8px;color:var(--mu);margin:22px 0 11px;display:flex;gap:9px;align-items:baseline}}
.bh span{{background:var(--acs);color:var(--ac);border-radius:100px;padding:2px 9px;font-size:11px;letter-spacing:0;text-transform:none}}
.ficha{{background:var(--card);border:1px solid var(--bd);border-radius:20px;padding:22px 24px;margin-bottom:16px}}
.fh{{display:flex;align-items:baseline;gap:12px;margin-bottom:14px;padding-bottom:12px;border-bottom:2px solid var(--ac)}}
.fh h3{{font-size:18.5px;font-weight:650}}
.fam{{font-size:11.5px;background:var(--acs);color:var(--ac);border-radius:100px;padding:3px 11px;font-weight:550}}
table{{width:100%;border-collapse:collapse}}
td{{padding:9px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top;font-size:13.5px}}
tr:last-child td{{border-bottom:none}}
td.k{{width:190px;color:var(--mu);font-size:11.5px;font-weight:600;text-transform:uppercase;letter-spacing:.4px;padding-top:11px}}
td.v{{color:var(--tx)}}
.li{{position:relative;padding-left:14px;margin-bottom:4px}}
.li:before{{content:"·";position:absolute;left:3px;color:var(--ac);font-weight:700}}
.obj{{margin-bottom:9px;padding-left:12px;border-left:2px solid var(--bd)}}
.obj .q{{font-weight:600;font-size:13px;color:#334155}}
.obj .r{{font-size:13px;color:var(--mu)}}
.fuente{{margin-top:14px;padding-top:11px;border-top:1px solid var(--bd);font-size:11px;color:var(--mu);font-family:"IBM Plex Mono",monospace}}
.foot{{margin-top:24px;text-align:center;font-size:12px;color:var(--mu)}}
</style></head><body><div class="wrap">
<div class="hero"><h1>Fichas de Producto SUPCON — Segunda entrega</h1>
<p>Seguridad (SIS), PLC, control de compresores, software de proceso, plataforma y ciberseguridad OT.
Mismo formato de 8 campos que la primera entrega de analizadores. Los campos sin respaldo en el
material del fabricante quedan marcados <b>POR COMPLETAR</b> &mdash; no se inventan datos.</p></div>
<div class="idx">{chips}</div>
{cuerpo}
<div class="foot">{len(F)} fichas &middot; {porc} con campos POR COMPLETAR &middot; Primera entrega (analizadores) en fichas_producto_supcon.html</div>
</div></body></html>"""

OUT = os.path.join(SALIDA, "fichas_producto_2.html")
open(OUT, "w", encoding="utf-8").write(HTML)

import re
tr_o = len(re.findall(r'<tr\b', HTML)); tr_c = len(re.findall(r'</tr>', HTML))
print("escrito:", OUT, len(HTML.encode()), "bytes")
print("fichas:", len(F), "| familias:", len(por_fam))
print(f"tr {tr_o}/{tr_c}", "OK" if tr_o==tr_c else "DESCUADRE")
for fam, items in por_fam.items():
    print(f"   {fam}: {', '.join(items)}")
