#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/historia_ineco.html — HISTORIA COMERCIAL INECO (2003-2014) x HOY.

Qué muestra: las cuentas que INECO atendía como Local Business Partner de Emerson/Rosemount
entre 2003 y 2014, cuántas veces se nombran en sus planes de negocio, y su estado HOY en el
trabajo de CONECTA (personas por área, dolor ambiental medido, prioridad en el plan).

El valor: ver qué cuenta lleva 20 años comprando, y qué competidor sigue siendo el mismo.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "historia_ineco.html")

h = json.load(open(os.path.join(D, "historia_comercial_ineco.json"), encoding="utf-8"))
CR = h["cruces_hoy"]
MEN = {k: v["menciones"] for k, v in h["cuentas"].items()}


def e(s):
    return html.escape(str(s if s is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


# filas ordenadas: primero las que tienen registro hoy y más menciones
filas = []
for nombre, c in CR.items():
    if not c:
        # cuentas del plan que hoy no tienen ningún registro en los datos
        filas.append((nombre, MEN.get(nombre, 0), {"empresa_hoy": "", "areas": 0, "personas": 0,
                                                  "carga_toxica": None, "respel_t": None,
                                                  "en_plan": False, "prio": None, "dolor": None}))
        continue
    filas.append((nombre, MEN.get(nombre, 0), c))
filas.sort(key=lambda x: (-(x[2]["personas"] > 0), -(x[2].get("carga_toxica") or 0), -x[1]))

rows = ""
for nombre, menc, c in filas:
    tox = c.get("carga_toxica")
    tiene_hoy = bool(c["personas"] or tox is not None)
    col = "#047857" if (tox is not None and tox > 100) else ("#b45309" if tiene_hoy else "#9ca3af")
    badge = ("CON DOLOR ALTO" if (tox is not None and tox > 100)
             else "EN EL MAPA" if tiene_hoy else "SIN REGISTRO HOY")
    rows += f'''
    <tr>
      <td class="emp"><b>{e(nombre)}</b>
        <span class="sub">{e(c.get('empresa_hoy') or '')}</span></td>
      <td class="num">{menc}</td>
      <td class="num">{n(c['areas']) if c['areas'] else '—'}</td>
      <td class="num">{n(c['personas']) if c['personas'] else '—'}</td>
      <td class="num"><b>{n(tox,1) if tox is not None else '—'}</b></td>
      <td class="num">{n(c.get('prio')) if c.get('en_plan') else '—'}</td>
      <td><span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{badge}</span></td>
    </tr>'''

# competidores
comp = sorted(h["competidores"].items(), key=lambda x: -x[1])
mx = comp[0][1] if comp else 1
comp_html = ""
for k, v in comp:
    comp_html += f'''
    <div class="bar">
      <span class="lb">{e(k)}</span>
      <div class="tr"><div class="fl" style="width:{v/mx*100:.0f}%"></div></div>
      <span class="vl">{v}</span>
    </div>'''

# productos
prod = sorted(h["productos"].items(), key=lambda x: -x[1])
mxp = prod[0][1] if prod else 1
prod_html = ""
for k, v in prod:
    prod_html += f'''
    <div class="bar">
      <span class="lb">{e(k)}</span>
      <div class="tr"><div class="fl p" style="width:{v/mxp*100:.0f}%"></div></div>
      <span class="vl">{v}</span>
    </div>'''

con_dato = sum(1 for _, _, c in filas if c["personas"] or c.get("carga_toxica") is not None)
con_gente = sum(1 for _, _, c in filas if c["personas"])
con_dolor = sum(1 for _, _, c in filas if (c.get("carga_toxica") or 0) > 100)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Historia comercial INECO 2003-2014 x hoy</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:940px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid var(--ac);border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#1e40af}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:14px 0 8px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.emp b{{font-size:13.5px}} .sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.badge{{font-size:10.5px;border-radius:5px;padding:2px 8px;font-weight:700;white-space:nowrap}}
.bar{{display:flex;align-items:center;gap:10px;margin-bottom:7px;font-size:13px}}
.lb{{width:210px;flex-shrink:0;color:#374151}}
.tr{{flex:1;height:9px;background:#f1f5f9;border-radius:5px;overflow:hidden}}
.fl{{height:100%;background:linear-gradient(90deg,#b91c1c,#f87171);border-radius:5px}}
.fl.p{{background:linear-gradient(90deg,#1d4ed8,#60a5fa)}}
.vl{{width:42px;text-align:right;font-variant-numeric:tabular-nums;color:var(--mu);font-size:12px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:820px){{.grid2{{grid-template-columns:1fr}}}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Historia comercial INECO (2003-2014), cruzada con hoy</h1>
<p class="sub0">INECO fue el <b>Local Business Partner de Emerson/Rosemount en Chile</b> durante
más de 28 años. Sus planes de negocio (2004, FY08, FY09, FY14) listan las cuentas, los
productos, los competidores y los EPC de esos años. Acá están cruzados con el trabajo actual de
CONECTA: qué cuenta lleva 20 años comprando, y en cuáles ya hay personas y dolor mapeados.</p>

<div class="kpis">
  <div><b>{len(filas)}</b>cuentas en los planes</div>
  <div><b>{con_dato}</b>con registro hoy</div>
  <div><b>{con_gente}</b>con personas por área</div>
  <div><b>{con_dolor}</b>con carga tóxica alta</div>
</div>

<div class="aviso">
  <b>Lo que dice el cruce:</b> las cuentas clave del plan de 2004 — <b>Codelco, Arauco, CMPC y
  ENAP</b> — siguen vivas hoy, con dolor ambiental medido y personas mapeadas por área. Arauco
  aparece 79 veces en los planes y hoy tiene 6 áreas cubiertas; ENAP 20 veces, con 397,7 t de
  carga tóxica y prioridad 361 en el plan de contacto. <b>No hay que buscar mercado nuevo en
  esas cuentas: hay que volver con otro producto.</b>
</div>

<h2>Las cuentas, entonces y hoy</h2>
<div class="card">
  <table><thead><tr>
    <th>Cuenta</th><th class="num">Veces en los planes</th><th class="num">Áreas hoy</th>
    <th class="num">Personas hoy</th><th class="num">Tóxicas t</th><th class="num">Prioridad</th>
    <th>Estado hoy</th>
  </tr></thead><tbody>{rows}</tbody></table>
</div>

<div class="grid2">
  <div class="card">
    <h3>Competidores nombrados entonces</h3>
    {comp_html}
    <p class="ct" style="font-size:12.5px;color:var(--mu);margin-top:10px">
    Endress+Hauser con "campaña agresiva" en FY08 y Yokogawa abriendo oficina tras ganar LNG
    Quinteros. Los mismos nombres siguen en el mercado de instrumentación hoy.</p>
  </div>
  <div class="card">
    <h3>Líneas que se vendían</h3>
    {prod_html}
    <p class="ct" style="font-size:12.5px;color:var(--mu);margin-top:10px">
    Sistemas (DeltaV) y gestión de activos (AMS) eran el 40% de las menciones: la venta era de
    solución, no de equipo suelto.</p>
  </div>
</div>

<h2>Qué aporta esto al trabajo de hoy</h2>
<div class="card">
  <ul>
    <li><b>Las cuentas clave se mantienen 20 años.</b> Codelco, Arauco, CMPC y ENAP están en el
    plan de 2004 y siguen en el mapa de 2026. La relación comercial no se reinicia.</li>
    <li><b>El RAIDS ya existía.</b> El plan de 2003 (§4.3.4) define "responsables por tipos de
    plantas (<b>Process Manager</b>: Celulosa, minería, gas natural)" — el mismo concepto que hoy
    usa la metodología de venta.</li>
    <li><b>La política de precios está documentada.</b> Cinco tipos de venta con su descuento:
    Oferta Paquete 30-50% (sacar base instalada de la competencia), MRO 5% máximo, Soluciones 10%,
    Nuevas Aplicaciones y Nuevas Plantas según proyecto y grado de influencia en la ingeniería.</li>
    <li><b>El modelo de fábrica con metas por producto</b> (IAS de Emerson: Pressure 3051S
    US$165K, Temp US$100K, cuentas claves, certificación de la fuerza de ventas) es el antecedente
    de lo que SUPCON pide hoy.</li>
    <li><b>El EPC era el canal de influencia.</b> Fluor, Bechtel, Aker, AMEC, SNC Lavalin, Hatch:
    entrar en la ingeniería conceptual para influenciar las bases de licitación.</li>
  </ul>
</div>

<h2>Fuentes, y qué no dice</h2>
<div class="card">
  <ul>
    <li><b>Fuentes:</b> <code>Plan de Negocios 2004 V5.doc</code> (División Instrumentos, INECO),
    <code>Business Plan FY08_Ineco.ppt</code>, <code>PSS INECO Business Review 2009.ppt</code> y
    <code>EMERSON Business Plan FY14- INECO.pptx</code>. Extraídos a texto; las menciones son
    conteos sobre ese texto.</li>
    <li><b>"Veces en los planes" no mide importancia comercial</b>, mide cuánto se habló de esa
    cuenta en esos documentos. Arauco aparece 79 veces porque tiene varias plantas nombradas una
    por una.</li>
    <li><b>El "Libro negro Ineco.pdf" NO es de cuentas:</b> es el <i>Fisher Control Valve
    Handbook</i> (4ª edición, ~700 páginas), el manual técnico de válvulas de control de Emerson.
    Sirve como material técnico, no como historia comercial.</li>
    <li><b>Las cuentas "sin registro hoy"</b> pueden existir con otro nombre en el catálogo, o no
    estar en el universo de prospección. No significa que no existan.</li>
    <li><b>Las personas y sus cargos son al momento del dato</b>, no verificados hoy: las personas
    se mueven (ver el caso Balbontín en el documento de personas por área).</li>
  </ul>
</div>

<footer>
  Fuentes: planes de negocio INECO 2004 / FY08 / FY09 / FY14 ·
  <a href="personas_por_area.html">personas por área</a> ·
  <a href="dolor_ambiental.html">dolor ambiental</a> ·
  <a href="matriz_dolor_perfil.html">matriz dolor·línea·perfil</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(filas)} cuentas | {con_dato} con registro | {con_gente} con personas | {con_dolor} con dolor alto")
