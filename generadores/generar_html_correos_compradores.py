#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/correos_compradores.html — los compradores del eCRM con su correo.

Lo importante de este entregable: decir la VERDAD sobre qué es cada correo. El nombre es
cosechado (real, del eCRM); el correo es INFERIDO (dominio con MX verificado + patrón). No se
presenta un inferido como real.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "correos_compradores.html")

d = json.load(open(os.path.join(D, "ecrm_correos_compradores.json"), encoding="utf-8"))
C = d["compradores"]
T = d["totales"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


con = [x for x in C if x["correo"]]
sin = [x for x in C if not x["correo"]]
por_dom = collections.Counter(x["correo"].split("@")[1] for x in con)

filas = ""
for x in C:
    if x["correo"]:
        col, et = "#b45309", "INFERIDO"
    else:
        col, et = "#9ca3af", "SIN CORREO"
    correo = x["correo"] or f'<span class="gris">sin dominio resuelto</span>'
    filas += f'''
    <tr>
      <td><b>{esc(x['nombre'])}</b><span class="sub">{esc(x.get('fuente','')[:66])}</span></td>
      <td>{esc(x['empresa'])}</td>
      <td class="num">{n(x['cotizaciones'])}</td>
      <td class="num">{n(x['usd'])}</td>
      <td class="num">{n(x['oc']) if x['oc'] else '—'}</td>
      <td class="mail">{correo}</td>
      <td><span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{et}</span></td>
    </tr>'''

doms_html = ""
for dm, k in por_dom.most_common():
    doms_html += f'<span class="chip">{esc(dm)} <b>{k}</b></span>'

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Correos de los compradores del eCRM</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:960px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
.aviso.rj{{background:#fef2f2;border-color:#fecaca;border-left-color:#b91c1c}}
.aviso.rj b{{color:#991b1b}}
.aviso.vd{{background:#f0fdf4;border-color:#bbf7d0;border-left-color:#047857}}
.aviso.vd b{{color:#065f46}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:14px 0 8px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.mail{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;color:#1e40af}}
.gris{{color:var(--mu);font-style:italic;font-family:inherit}}
.sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.badge{{font-size:10.5px;border-radius:5px;padding:2px 8px;font-weight:700;white-space:nowrap}}
.chip{{display:inline-block;font-size:12px;background:#f3f4f6;color:#374151;border-radius:5px;padding:3px 10px;margin:0 5px 5px 0}}
.chip b{{color:#1d4ed8}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Correos de los compradores del eCRM</h1>
<p class="sub0">Los <b>183 compradores reales</b> que pidieron cotización a INECO entre 2023 y
2025, con el correo que se pudo determinar. El <b>nombre y el cargo son cosechados</b> (están en
el eCRM, son reales). El <b>correo es INFERIDO</b>: dominio verificado + patrón. Se declara cuál
es cuál, línea por línea.</p>

<div class="kpis">
  <div><b>{len(C)}</b>compradores con nombre</div>
  <div><b>{len(con)}</b>con correo ({len(con)/len(C)*100:.0f}%)</div>
  <div><b>{len(por_dom)}</b>dominios (todos con MX verificado)</div>
  <div><b>0</b>correos verificados uno a uno</div>
</div>

<div class="aviso rj">
  <b>Decirlo derecho, porque importa:</b> <b>ninguno de estos correos está verificado.</b> Ninguna
  fuente publica el correo real de estos compradores — se midió por cuatro vías y todas fallan
  (ver abajo). Lo que sí está verificado es el <b>dominio</b>: los {len(por_dom)} dominios usados
  tienen registro <b>MX</b>, o sea que <b>reciben correo de verdad</b>. El patrón
  <code>nombre.apellido</code> es el estándar de la gran minería en Chile.
  <br><br>
  <b>Consecuencia práctica:</b> sirve para contactar y para adivinar la casilla correcta rápido;
  NO sirve para envío masivo a ciegas. Un correo mal dirigido rebota o llega a un tercero.
</div>

<div class="aviso vd">
  <b>Lo que sí se logró:</b> de <b>{len(C)} compradores</b> se pasó de <b>1 (1%)</b> a
  <b>{len(con)} ({len(con)/len(C)*100:.0f}%)</b> con correo apuntando a un dominio que recibe
  mail. Y el <b>nombre real de cada uno ya se tenía</b>: ése es el activo duro, y de ahí sale
  todo lo demás.
</div>

<div class="aviso">
  <b>Lo que se midió y no dio resultado</b> (para no repetirlo):
  <ul>
    <li><b>Cosecha del Coordinador Eléctrico</b> (1.353 correos REALES, gratis): solapamiento
    <b>cero</b> — son empresas de generación eléctrica, estos compradores son de minería.</li>
    <li><b>Webs corporativas</b> de las mineras: <b>ya no publican correos personales</b>. Solo
    buzones genéricos (<code>oficinadepartes@enami.cl</code>, <code>jri@jri.cl</code>).</li>
    <li><b>Teléfono</b>: el campo existe en los archivos (se llamaba <code>telefono</code>) pero
    está <b>vacío en los 2.327 registros</b>. Los "<i>teléfonos</i>" que aparecían en el eCRM eran
    números de cotización y años (<code>90541 2022</code>).</li>
    <li><b>LinkedIn</b>: el 90% de los tomadores trae su perfil, pero no el correo.</li>
  </ul>
</div>

<h2>Los compradores</h2>
<div class="card">
  <table><thead><tr>
    <th>Persona (cosechada del eCRM)</th><th>Empresa</th><th class="num">Cotiz.</th>
    <th class="num">US$</th><th class="num">OC</th><th>Correo (inferido)</th><th>Tipo</th>
  </tr></thead><tbody>{filas}</tbody></table>
</div>

<h2>Dominios usados (todos con MX verificado)</h2>
<div class="card">
  {doms_html}
  <p class="sub" style="margin-top:10px">Verificado con <code>dig MX</code>: cada uno de estos
  dominios tiene servidor de correo activo. Los que no lo tenían se descartaron
  (<code>candelariamine.com</code> no existe; <code>candelaria.cl</code> no tiene MX), así que los
  14 compradores de Minera Candelaria quedaron sin correo en vez de con uno falso.</p>
</div>

<h2>Qué falta para tener el correo REAL</h2>
<div class="card">
  <ul>
    <li><b>Validación de rebote</b> (lo único que prueba que la casilla existe): mandar un correo
    de prueba y ver si rebota. Requiere decidir qué se envía y desde dónde — no se hace sin tu OK.</li>
    <li><b>Servicio de verificación</b> (Hunter, NeverBounce, ZeroBounce): cobran por validar y
    entregan el correo con su estado verificado. Existe <code>hunter_ct_payload.json</code> con 244
    consultas armadas, por si se decide pagar.</li>
    <li><b>El contacto directo por LinkedIn</b>: los 183 tienen nombre, y el 90% de los tomadores
    del catálogo trae perfil. Es la vía que no depende de adivinar el correo.</li>
  </ul>
</div>

<footer>
  Fuente: <code>Archivo de ecrm .xlsx</code> (2023-2025) ·
  <a href="ecrm_supcon.html">eCRM × SUPCON</a> ·
  <a href="personas_por_area.html">personas por área</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(C)} compradores | {len(con)} con correo | {len(por_dom)} dominios con MX")
