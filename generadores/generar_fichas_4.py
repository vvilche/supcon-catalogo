#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renderiza las fichas comerciales de la 4a entrega (software de proceso y plataforma).
Lee datos/fichas_4_datos.json (lo produce fichas_4_datos.py).

Uso:  python3 generar_fichas_4.py
Salida: artefactos/fichas_producto_4.html
"""
import os, json, html as H, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")
SALIDA = os.path.join(BASE, "artefactos")

D = json.load(open(os.path.join(DATOS, "fichas_4_datos.json"), encoding="utf-8"))
F = D["fichas"]

def esc(s): return H.escape(str(s))

def fila(k, v):
    if isinstance(v, list):
        v = "".join(f'<div class="li">{esc(x)}</div>' for x in v)
    return f'<tr><td class="k">{esc(k)}</td><td class="v">{v}</td></tr>'

def ancla(n):
    return "f-" + esc(n).replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-").replace("&", "y").replace(".", "")

def ficha(nombre, f):
    obj = "".join(
        f'<div class="obj"><div class="q">{esc(o[0])}</div>'
        f'<div class="r">{esc(o[1]) if o[1] else "&mdash;"}</div></div>'
        for o in f["objeciones"])
    return f"""
<div class="ficha" id="{ancla(nombre)}">
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

chips = "".join(f'<a class="chip" data-fam="{esc(F[n]["familia"])}" href="#{ancla(n)}">{esc(n)}</a>' for n in F)

fam_botones = "".join(
    f'<label class="fbtn"><input type="radio" name="fam" value="{esc(f)}">'
    f'<span>{esc(f)} <b>{len(i)}</b></span></label>'
    for f, i in sorted(por_fam.items()))

cuerpo = ""
for fam, items in por_fam.items():
    cuerpo += f'<div class="bloque" data-fam="{esc(fam)}"><div class="bh">{esc(fam)} <span>{len(items)} ficha{"s" if len(items)!=1 else ""}</span></div>'
    for n in items:
        cuerpo += ficha(n, F[n])
    cuerpo += '</div>'

porc = sum(1 for f in F.values() if "POR COMPLETAR" in json.dumps(f, ensure_ascii=False))

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fichas de Producto SUPCON — Software y plataforma</title><style>
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
.fbar{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}}
.fbtn{{cursor:pointer}}
.fbtn input{{display:none}}
.fbtn span{{display:inline-block;border:1px solid #cbd5e1;background:var(--card);color:#334155;border-radius:8px;padding:6px 12px;font-size:13px;font-weight:550}}
.fbtn input:checked+span{{background:var(--ac);border-color:var(--ac);color:#fff}}
.fbtn b{{font-weight:600;opacity:.72}}
.oculto{{display:none !important}}
.foot{{margin-top:24px;text-align:center;font-size:12px;color:var(--mu)}}
</style></head><body><div class="wrap">
<div class="hero"><h1>Fichas de Producto SUPCON — Software y plataforma</h1>
<p>Software de proceso (APC, RTO, OTS, Blend, SCO, PID, TAS, TPT, APEX), plataforma y gestión (supOS, Nyx/UCS, OMC,
PRIDE, MP3000, EAM, PLS, IFEM, ESP-iSYS) y ciberseguridad OT. Mismo formato de 8 campos.
Datos tomados de los one-pagers, brochures y manuales técnicos del fabricante. Los campos sin respaldo en el
material del fabricante quedan marcados <b>POR COMPLETAR</b> &mdash; no se inventan datos. Cuando el competidor de un
segmento se agrega desde conocimiento general y no del material, se rotula explícitamente como <b>INFERENCIA</b>.</p></div>
<div class="idx">{chips}</div>
<div class="fbar">
  <label class="fbtn"><input type="radio" name="fam" value="" checked><span>Todas <b>{len(F)}</b></span></label>
  {fam_botones}
</div>
{cuerpo}
<div class="foot">{len(F)} fichas &middot; {porc} con campos POR COMPLETAR &middot; Instrumentación y analítica en fichas_producto_3.html · SIS/PLC/CCS en fichas_producto_2.html</div>
</div>
<script>
  var bloques = Array.prototype.slice.call(document.querySelectorAll('.bloque'));
  var radios = Array.prototype.slice.call(document.querySelectorAll('input[name=fam]'));
  function aplicarFam() {{
    var v = (radios.filter(function(r){{return r.checked;}})[0] || {{}}).value || '';
    bloques.forEach(function(b) {{
      b.classList.toggle('oculto', !!v && b.getAttribute('data-fam') !== v);
    }});
    Array.prototype.slice.call(document.querySelectorAll('.chip')).forEach(function(c) {{
      c.classList.toggle('oculto', !!v && c.getAttribute('data-fam') !== v);
    }});
  }}
  radios.forEach(function(r) {{ r.addEventListener('change', aplicarFam); }});
  aplicarFam();
</script>
</body></html>"""

OUT = os.path.join(SALIDA, "fichas_producto_4.html")
open(OUT, "w", encoding="utf-8").write(HTML)

import re
tr_o = len(re.findall(r'<tr\b', HTML)); tr_c = len(re.findall(r'</tr>', HTML))
div_o = len(re.findall(r'<div\b', HTML)); div_c = len(re.findall(r'</div>', HTML))
print("escrito:", OUT, len(HTML.encode()), "bytes")
print("fichas:", len(F), "| familias:", len(por_fam))
print(f"tr {tr_o}/{tr_c}", "OK" if tr_o == tr_c else "DESCUADRE")
print(f"div {div_o}/{div_c}", "OK" if div_o == div_c else "DESCUADRE")
for fam, items in por_fam.items():
    print(f"   {fam}: {len(items)} -> {', '.join(items)}")
