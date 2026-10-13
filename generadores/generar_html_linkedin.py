#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/compradores_linkedin.html — los compradores del eCRM con su LinkedIn.

El nombre es dato cosechado del eCRM. El LinkedIn se halló por búsqueda y se VALIDÓ por match del
nombre del perfil. Cada línea declara su confianza:
  ALTA  = el perfil trae el nombre completo (3+ palabras) y coincide
  MEDIA = coincide el nombre y un apellido, pero el slug es corto: puede ser homónimo
"""
import os, json, html, collections, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "compradores_linkedin.html")

d = json.load(open(os.path.join(D, "ecrm_linkedin.json"), encoding="utf-8"))
C = d["compradores"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v):
    try:
        return f"{v:,.0f}"
    except Exception:
        return "—"


con = [x for x in C if x["linkedin"]]
cnt = collections.Counter(x["confianza"] for x in C)
por_emp = collections.Counter(x["empresa"] for x in con)

# tabla ordenada por monto
filas = ""
for x in sorted(C, key=lambda y: -y["usd"]):
    if x["linkedin"]:
        alta = x["confianza"].startswith("ALTA")
        col = "#047857" if alta else "#b45309"
        et = "ALTA" if alta else "MEDIA"
        link = f'<a href="{esc(x["linkedin"])}" target="_blank">ver perfil</a>'
        titulo = esc(x["titulo"][:58])
    else:
        col, et, link, titulo = "#9ca3af", "SIN PERFIL", '<span class="gris">no encontrado</span>', ""
    filas += f'''
    <tr>
      <td><b>{esc(x['nombre'])}</b><span class="sub">{titulo}</span></td>
      <td>{esc(x['empresa'])}</td>
      <td class="num">{n(x['cotizaciones'])}</td>
      <td class="num">{n(x['usd'])}</td>
      <td>{link}</td>
      <td><span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{et}</span></td>
    </tr>'''

emp_html = ""
for e, k in por_emp.most_common(14):
    emp_html += f'<span class="chip">{esc(e)} <b>{k}</b></span>'

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compradores del eCRM en LinkedIn</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:960px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#f0fdf4;border:1px solid #bbf7d0;border-left:4px solid #047857;border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#065f46}}
.aviso.am{{background:#fffbeb;border-color:#fde68a;border-left-color:var(--am)}}
.aviso.am b{{color:#92400e}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.gris{{color:var(--mu);font-style:italic}}
.badge{{font-size:10.5px;border-radius:5px;padding:2px 8px;font-weight:700;white-space:nowrap}}
.chip{{display:inline-block;font-size:12px;background:#f3f4f6;color:#374151;border-radius:5px;padding:3px 10px;margin:0 5px 5px 0}}
.chip b{{color:#1d4ed8}}
a{{color:var(--ac);text-decoration:none}} a:hover{{text-decoration:underline}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Los compradores del eCRM, en LinkedIn</h1>
<p class="sub0">Los <b>{len(C)} compradores reales</b> que pidieron cotización a INECO entre 2023 y
2025 (nombre y monto tomados del eCRM; son datos reales), con su perfil de LinkedIn. Es el canal
de contacto directo: <b>no depende de adivinar el correo</b>.</p>

<div class="kpis">
  <div><b>{len(C)}</b>compradores del eCRM</div>
  <div><b>{len(con)}</b>con LinkedIn ({len(con)/len(C)*100:.0f}%)</div>
  <div><b>{cnt.get('ALTA (nombre completo)',0)}</b>de confianza ALTA</div>
  <div><b>{cnt.get('MEDIA (verificar homónimo)',0)}</b>a verificar (posible homónimo)</div>
  <div><b>{cnt.get('SIN PERFIL',0)}</b>sin perfil encontrado</div>
</div>

<div class="aviso">
  <b>Esto reemplaza la validación de correos.</b> Validar un correo exige enviar (irreversible) o
  sondear servidores ajenos por SMTP — y los servidores de estas mineras están detrás de
  Proofpoint/Mimecast, que responden cualquier cosa. En cambio el <b>nombre del comprador es dato
  real</b>, y con nombre + empresa se llega a su perfil. De 1% de cobertura a <b>{len(con)/len(C)*100:.0f}%</b>.
</div>

<div class="aviso am">
  <b>Ojo con los de confianza MEDIA ({cnt.get('MEDIA (verificar homónimo)',0)}).</b> El perfil coincide
  en nombre y un apellido, pero el identificador es corto (<code>mario-aguilera</code>,
  <code>pablo-aguilera</code>): puede ser un homónimo. Los de confianza <b>ALTA</b>
  ({cnt.get('ALTA (nombre completo)',0)}) traen el nombre completo en el perfil
  (<code>jhonny-guamparito-caceres</code>, <code>german-diaz-tapia</code>): el match es sólido.
  Antes de escribir a un MEDIA, abrir el perfil y confirmar que es la empresa correcta.
</div>

<h2>Compradores, por monto cotizado</h2>
<div class="card">
  <table><thead><tr>
    <th>Persona (del eCRM)</th><th>Empresa</th><th class="num">Cotiz.</th><th class="num">US$</th>
    <th>LinkedIn</th><th>Confianza</th>
  </tr></thead><tbody>{filas}</tbody></table>
</div>

<h2>Empresas cubiertas</h2>
<div class="card">
  {emp_html}
  <p class="sub" style="margin-top:10px">Las cuentas con más gente identificada son las que más
  cotizaban: MLP (Minera Los Pelambres), Andina, Candelaria, Codelco y Caserones.</p>
</div>

<h2>Cómo se hizo (y qué no se pudo)</h2>
<div class="card">
  <ul>
    <li><b>Método:</b> por cada comprador, <code>web_search("nombre" + empresa + linkedin)</code>.
    Se acepta el resultado <b>solo</b> si la URL es un perfil <code>/in/</code> de LinkedIn y el
    nombre del perfil comparte tokens con el comprador. Si no matchea, se deja vacío: mejor un
    hueco que un perfil ajeno.</li>
    <li><b>Lo que no funcionó:</b> abrir LinkedIn desde el navegador pide login (authwall);
    Google y DuckDuckGo bloquean por CAPTCHA desde esta IP. La búsqueda de Hermes sí funciona.</li>
    <li><b>Los {cnt.get('SIN PERFIL',0)} sin perfil</b> son personas reales sin LinkedIn hallable
    (o con el nombre escrito distinto en el eCRM, ej. <code>Sebastean Paez</code>). Se declaran.</li>
    <li><b>El cargo no se toma del perfil:</b> el perfil puede estar desactualizado. El cargo real
    es el del eCRM (lo que esa persona hacía en la cotización).</li>
  </ul>
</div>

<footer>
  Fuente: <code>Archivo de ecrm .xlsx</code> (2023-2025) + búsqueda de LinkedIn ·
  <a href="ecrm_supcon.html">eCRM × SUPCON</a> ·
  <a href="correos_compradores.html">correos inferidos</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(C)} compradores | {len(con)} con LinkedIn | {cnt.get('ALTA (nombre completo)',0)} ALTA")
