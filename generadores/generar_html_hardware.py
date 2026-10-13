#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera estudio-mercado/hardware_partidas_2025.html

El mercado de hardware de automatización medido POR PARTIDA ARANCELARIA, con el detalle de
cada partida. Es el método correcto: la partida es dato duro, la marca no (el campo DMARCA
trae siglas y truncamientos el 38% de las veces).

Lee datos/mercado_hardware_partida.json.

Salida: estudio-mercado/hardware_partidas_2025.html
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "estudio-mercado", "hardware_partidas_2025.html")

d = json.load(open(os.path.join(D, "mercado_hardware_partida.json"), encoding="utf-8"))
L = d["lineas"]

def usd(v): return f"US${v/1e6:,.1f}M"

# orden: DCS, Instrumentación, Analítica, Válvulas (SIS se muestra dentro de DCS)
ORDEN = ["DCS y control","Instrumentación","Analítica","Válvulas","SIS (seguridad)"]
TIPO = {"DCS y control":"MEDIDA","Instrumentación":"MEDIDA","Analítica":"TECHO",
        "Válvulas":"TECHO","SIS (seguridad)":"CONTENIDA EN DCS"}
COLOR = {"MEDIDA":"#047857","TECHO":"#d97706","CONTENIDA EN DCS":"#64748b"}

bloques = ""
for lin in ORDEN:
    if lin not in L: continue
    x = L[lin]
    tipo = TIPO[lin]
    col = COLOR[tipo]
    tot = x["mercado_usd"]
    filas = ""
    for p, val in x["por_partida"]:
        pct = val/tot*100
        ancho = max(pct, 1.5)
        filas += f'''
        <div class="part">
          <div class="ph2"><span class="pn2">{p}</span><span class="pv">{usd(val)}</span></div>
          <div class="bar"><div class="fill" style="width:{ancho:.1f}%"></div></div>
          <div class="pp">{pct:.1f}% de la línea</div>
        </div>'''
    marca_top = " · ".join(f"{m} ({usd(v)})" for m, v in x["top_marcas"][:5])
    pais_top = " · ".join(f"{p} ({usd(v)})" for p, v in x["top_paises"][:4])
    nota_sis = ('''
      <div class="aviso">
        <b>No sumar aparte.</b> SIS usa las mismas partidas que DCS: no existe una partida de
        "sistema instrumentado de seguridad", porque un SIS entra como tablero de control igual
        que un DCS. Este valor está <b>contenido</b> en los US$341,5M de DCS.
      </div>''' if lin == "SIS (seguridad)" else "")
    nota_techo = ('''
      <div class="aviso">
        <b>Es techo, no medida.</b> La partida principal es residual y mezcla categorías: incluye
        productos que no son de esta línea. El valor real está entre el segmento identificable
        y este total.
      </div>''' if tipo == "TECHO" else "")
    bloques += f'''
    <section class="linea">
      <div class="lh">
        <h2>{lin}</h2>
        <span class="badge" style="background:{col}1a;color:{col};border:1px solid {col}44">{tipo}</span>
      </div>
      <div class="kpis">
        <div><b>{usd(tot)}</b>mercado estimado</div>
        <div><b>{x["items"]:,}</b>ítems importados</div>
        <div><b>{x["n_importadores"]:,}</b>importadores</div>
        <div><b>{x["pct_ruido"]}%</b>ruido restado</div>
      </div>
      {nota_sis}{nota_techo}
      <h3>Detalle por partida arancelaria</h3>
      {filas}
      <div class="meta"><b>Marcas principales:</b> {marca_top or "sin dato"}</div>
      <div class="meta"><b>Orígenes:</b> {pais_top or "sin dato"}</div>
    </section>'''

TOTAL = 341.5 + 128.4 + 148.5 + 398.1

HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mercado de hardware por partida arancelaria — Chile 2025</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:1000px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:860px}}
h2{{font-size:21px;font-weight:660;letter-spacing:-.2px}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:16px 0 9px}}
p{{margin-bottom:11px}}
ul{{list-style:none;margin:9px 0 12px}}
ul li{{position:relative;padding-left:17px;margin-bottom:6px}}
ul li:before{{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}}
table{{width:100%;border-collapse:collapse;margin:13px 0;font-size:14px}}
th{{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 10px;border-bottom:1px solid #f1f5f9}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:14px 0 16px;font-size:14px}}
.aviso b{{color:#92400e}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:16px 19px;margin:16px 0;font-size:14px}}
.linea{{background:var(--cd);border:1px solid var(--bd);border-radius:14px;padding:19px 22px;margin-bottom:16px}}
.lh{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px}}
.badge{{font-size:11px;border-radius:6px;padding:3px 11px;font-weight:700;text-transform:uppercase;letter-spacing:.3px}}
.kpis{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:6px}}
.kpis div{{background:#fbfdff;border:1px solid var(--bd);border-radius:9px;padding:9px 14px;font-size:11.5px;color:var(--mu)}}
.kpis b{{display:block;font-size:17px;font-weight:700;color:var(--tx)}}
.part{{margin-bottom:11px}}
.ph2{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:5px}}
.pn2{{font-size:14px;font-weight:550}}
.pv{{font-weight:700;font-size:15px;letter-spacing:-.2px;font-variant-numeric:tabular-nums}}
.bar{{height:6px;background:#f1f5f9;border-radius:3px;overflow:hidden}}
.fill{{height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:3px}}
.pp{{font-size:11.5px;color:var(--mu);margin-top:3px}}
.meta{{font-size:12.5px;color:var(--mu);margin-top:8px;line-height:1.55}}
.meta b{{color:#475569}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Mercado de hardware por partida arancelaria</h1>
<p class="sub">Chile 2025. Todo el hardware de automatización e instrumentación medido con la partida
arancelaria —que es dato duro— y no con la marca, que no lo es.</p>

<div class="kpi">
  <div><b>US$1.016,5M</b>hardware de automatización</div>
  <div><b>4</b>líneas medibles</div>
  <div><b>231.000</b>ítems clasificados</div>
  <div><b>23.740</b>importadores activos</div>
</div>

<div class="metodo">
  <b>Cómo se mide, y por qué así.</b> El estudio partió filtrando por marca y eso estaba mal:
  el campo de marca del registro de Aduanas trae <b>siglas y nombres truncados el 38% de las
  veces</b> (aparecen cosas como <code>N.S.I.C.</code>, <code>E.R.D.</code> o
  <code>S + HAUSER</code> en vez de Endress+Hauser). Exigir una marca conocida para contar un
  ítem deja fuera valor real y subestima el mercado entre 2,7 y 36 veces según la línea.
  <br><br>
  <b>La partida arancelaria, en cambio, siempre está y siempre es correcta.</b> Se midió con la
  partida y se restó solo el ruido verificable: ítems cuya glosa declara otro rubro, y marcas
  de otro rubro comprobable (Caterpillar, Cummins y Komatsu en la partida de válvulas son
  repuestos de vehículos, no válvulas de proceso).
  <br><br>
  <b>Validación:</b> el método se probó contra el trabajo fino de válvulas, que se hizo a mano
  con evidencia. Diferencia: <b>0,4%</b>. El método queda validado.
  <br><br>
  <b>La marca se reporta aparte</b>, solo como indicador de competencia identificable. Nunca
  para medir tamaño.
</div>

<h2>El cuadro completo</h2>
<table>
  <tr><th>Línea</th><th class="num">Mercado 2025</th><th class="num">Importadores</th><th>Calidad de la medida</th></tr>
  <tr><td><b>Válvulas</b></td><td class="num">US$398,1M</td><td class="num">8.395</td>
      <td><span class="badge" style="background:#d977061a;color:#d97706;border:1px solid #d9770644">Techo</span></td></tr>
  <tr><td><b>DCS y control</b> <span style="font-size:12px;color:#94a3b8">(contiene SIS)</span></td>
      <td class="num">US$341,5M</td><td class="num">5.474</td>
      <td><span class="badge" style="background:#0478571a;color:#047857;border:1px solid #04785744">Medida</span></td></tr>
  <tr><td><b>Analítica</b></td><td class="num">US$148,5M</td><td class="num">3.369</td>
      <td><span class="badge" style="background:#d977061a;color:#d97706;border:1px solid #d9770644">Techo</span></td></tr>
  <tr><td><b>Instrumentación</b></td><td class="num">US$128,4M</td><td class="num">5.878</td>
      <td><span class="badge" style="background:#0478571a;color:#047857;border:1px solid #04785744">Medida</span></td></tr>
  <tr><td><b>SIS</b></td><td class="num">US$166,1M</td><td class="num">5.153</td>
      <td><span class="badge" style="background:#64748b1a;color:#64748b;border:1px solid #64748b44">Contenida en DCS</span></td></tr>
  <tr style="background:#fbfdff"><td><b>TOTAL hardware</b></td><td class="num"><b>US${TOTAL:,.1f}M</b></td>
      <td class="num">23.740</td><td style="font-size:12.5px;color:#64748b">SIS no se suma: está dentro de DCS</td></tr>
</table>

{bloques}

<h2>Qué cambia esto</h2>
<ul>
  <li><b>Válvulas es el mercado de hardware más grande</b> (US$398,1M), por encima del DCS
      (US$341,5M). En el estudio anterior estaba reportado como US$53,8M: la séptima parte.</li>
  <li><b>La instrumentación es ocho veces más grande</b> de lo que decía el estudio: US$128,4M
      contra los US$19,7M que se habían reportado para caudal y nivel.</li>
  <li><b>El SIS no se puede medir como mercado propio.</b> No existe una partida de sistema de
      seguridad: hay que venderlo dentro del proyecto de control, no como categoría aparte.</li>
  <li><b>Dos líneas son techo, no medida.</b> Válvulas y analítica tienen una partida residual
      que mezcla categorías. Ahí el número real está entre el segmento identificable y el total.
      Reportarlo como si fuera medida sería el mismo error que se corrigió, al revés.</li>
</ul>

<footer>
  Fuente: Registro DIN de importaciones, Servicio Nacional de Aduanas de Chile, año 2025
  (4.847.036 líneas, US$85.671M importados por el país).
  <br>Ver <a href="valvulas_2025.html">el detalle de válvulas</a> ·
  <a href="analizadores_2025.html">analizadores</a> ·
  <a href="../artefactos/metodologia_mercado.html">metodología</a> ·
  <a href="../artefactos/estrategia_penetracion.html">estrategia</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"lineas: {len(bloques.split('section class'))-1} | TOTAL: US${TOTAL:,.1f}M")
