#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera estudio-mercado/dcs_sistemas_2025.html"""
import os, json
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"estudio-mercado","dcs_sistemas_2025.html")
d=json.load(open(os.path.join(D,"mercado_dcs_sistemas.json"),encoding="utf-8"))
def usd(v):
    """Acepta USD crudos o millones segun la magnitud, y formatea es-CL.
    El JSON mezcla escalas: desglose_verificado viene en millones, marcas/origen en USD."""
    if v >= 1_000_000:          # viene en USD crudos
        v = v / 1e6
    return "US$" + f"{v:,.1f}".replace(",","X").replace(".",",").replace("X",".") + "M"
g=d["desglose_verificado"]
ctrl=g["control_proceso_confirmado_usd"]

filas=""
for nom,v,pct,nota,col in [
 ("Alta tensión — subestaciones y aparamenta (GIS, celdas, 220 kV)",g["alta_tension_subestaciones_usd"],38,"Siemens Energy, Hitachi Energy (ELK-3/ELK-14), Alstom, Sterlite, Hyosung. Es transmisión eléctrica.","#94a3b8"),
 ("Baja tensión — distribución eléctrica",g["baja_tension_distribucion_usd"],4,"Tableros de distribución, centros de carga, correctores de factor de potencia.","#94a3b8"),
 ("Partes de tableros y de conexión",g["partes_tableros_usd"],23,"Componentes y partes. No es un sistema completo.","#94a3b8"),
 ("Baja tensión — sin glosa clasificable",g["baja_tension_sin_glosa_usd"],24,"El límite del dato: no se puede saber si es control o distribución.","#d97706"),
 ("Baja tensión — CONTROL confirmado",g["baja_tension_control_proceso_usd"],11,"Glosa de control de proceso: sistema de control, PLC, ICSS, panel de control.","#2563eb"),
]:
    filas+=f'''<div class="part"><div class="ph2"><span>{nom}</span><span class="pv">{usd(v)}</span></div>
      <div class="bar"><div class="fill" style="width:{max(pct,2):.1f}%;background:{col}"></div></div>
      <div class="pp">{pct}% de las partidas 8537/8538 — {nota}</div></div>'''

marcas_ctrl="".join(f'<tr><td>{m}</td><td class="num">{usd(v)}</td></tr>' for m,v in d["marcas_control"][:10] if m)
orig="".join(f'<tr><td>{p}</td><td class="num">{usd(v)}</td></tr>' for p,v in d["origen_control"][:7])

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DCS y sistemas de control — Chile 2025</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:980px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:850px}}
h2{{font-size:20px;font-weight:660;margin:34px 0 10px;letter-spacing:-.2px}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:18px 0 9px}}
p{{margin-bottom:11px}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px}}
th{{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--bd)}}
td{{padding:8px 10px;border-bottom:1px solid #f1f5f9}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.corr{{background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid var(--ac);border-radius:9px;padding:15px 18px;margin:15px 0;font-size:14px}}
.corr b{{color:#1d4ed8}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:15px 18px;margin:15px 0;font-size:14px}}
.aviso b{{color:#92400e}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:17px 20px;margin-bottom:14px}}
.part{{margin-bottom:12px}}
.ph2{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:5px;font-size:14px}}
.pv{{font-weight:700;font-size:15px;font-variant-numeric:tabular-nums}}
.bar{{height:6px;background:#f1f5f9;border-radius:3px;overflow:hidden}}
.fill{{height:100%;border-radius:3px}}
.pp{{font-size:11.5px;color:var(--mu);margin-top:3px}}
.dos{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:700px){{.dos{{grid-template-columns:1fr}}}}
ul{{list-style:none}}
ul li{{position:relative;padding-left:17px;margin-bottom:7px}}
ul li:before{{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>DCS y sistemas de control</h1>
<p class="sub">Chile 2025. Dónde está realmente el mercado de control de proceso, y qué parte de lo
que las partidas arancelarias llaman "tableros de control" no lo es.</p>

<div class="kpi">
  <div><b>{usd(ctrl)}</b>control de proceso medido</div>
  <div><b>{usd(g["alta_tension_subestaciones_usd"])}</b>que no es de SUPCON</div>
  <div><b>{usd(g["baja_tension_sin_glosa_usd"])}</b>no clasificable</div>
  <div><b>3.340</b>importadores de control</div>
</div>

<div class="corr">
  <b>Corrección de un número anterior.</b> Este estudio había reportado el mercado de DCS en
  US$341,5M tomando las partidas 8537/8538 completas. <b>Estaba mal, inflado 8,6 veces.</b>
  Al abrir los ítems más grandes de esas partidas se ve que son <b>subestaciones y aparamenta
  eléctrica</b>: GIS de Siemens Energy y Hitachi Energy (modelos ELK-3 y ELK-14), celdas Alstom,
  interruptores de 220 kV, seccionadoras de Sterlite y Hyosung Heavy. Eso es negocio de
  <b>transmisión eléctrica</b>, no automatización de proceso. El control de proceso medido es
  <b>{usd(ctrl)}</b>.
</div>

<h2>Qué hay dentro de las partidas 8537/8538</h2>
<p>Estas partidas son el "cajón" donde cae cualquier tablero. Desglosadas por la glosa del ítem:</p>
<div class="card">{filas}</div>

<div class="aviso">
  <b>Dos advertencias sobre este desglose.</b>
  <b>Primero:</b> el {g["baja_tension_sin_glosa_usd"]/ (g["alta_tension_subestaciones_usd"]+g["baja_tension_distribucion_usd"]+g["partes_tableros_usd"]+g["baja_tension_sin_glosa_usd"]+g["baja_tension_control_proceso_usd"])*100:.0f}%
  en "baja tensión sin glosa" es el límite del dato: el importador no declaró si es control o
  distribución, y no se puede saber. No se reparte, se declara.
  <b>Segundo:</b> un DCS <b>no tiene partida arancelaria propia</b>. Entra como "tablero con
  aparato eléctrico de control" o como "regulador automático", según cómo lo declare quien
  importa. Por eso hay que mirar las dos partes.
</div>

<h2>La otra mitad del DCS: reguladores automáticos</h2>
<p>La partida 9032 es donde aparecen los DCS declarados como tales. Ahí están los sistemas de
control de ABB y las estaciones de operación C300 de Honeywell, que son DCS de proceso reales:</p>
<table>
  <tr><th>Partida</th><th class="num">Valor</th><th>Qué incluye</th></tr>
  <tr><td>90328900 — Los demás reguladores automáticos</td><td class="num">{usd(g["reguladores_automaticos_usd"]-16.1-4.2-2.4)}</td>
      <td>Aquí están los DCS y sistemas de control declarados como reguladores</td></tr>
  <tr><td>90329000 — Partes de reguladores</td><td class="num">US$16,1M</td><td>Componentes</td></tr>
  <tr><td>90328100 / 90322000 — Hidráulicos y presostatos</td><td class="num">US$6,6M</td><td>Instrumentación de control asociada</td></tr>
</table>

<h2>El mercado de control de proceso</h2>
<div class="card" style="border-left:4px solid #2563eb">
  <div class="ph2"><span style="font-size:15px;font-weight:600">Control de proceso confirmado</span>
  <span class="pv" style="font-size:22px">{usd(ctrl)}</span></div>
  <p style="font-size:13.5px;color:#64748b;margin-top:8px">
  {usd(g["baja_tension_control_proceso_usd"])} en tableros de baja tensión con glosa de control
  (sistema de control, PLC, ICSS, panel de control) · {usd(g["reguladores_automaticos_usd"]-16.1-4.2-2.4)} en reguladores automáticos.
  Con {len(d.get("por_categoria",{}))} categorías identificadas y 3.340 importadores activos.</p>
</div>

<div class="dos">
  <div class="card">
    <h3>Quién vende control en Chile</h3>
    <table>{marcas_ctrl}</table>
    <p style="font-size:12.5px;color:#64748b;margin-top:8px">Siemens, ABB, Hitachi Energy y
    Rockwell dominan. <b>No hay ningún fabricante chino de DCS entre los primeros.</b></p>
  </div>
  <div class="card">
    <h3>De dónde viene el control</h3>
    <table>{orig}</table>
    <p style="font-size:12.5px;color:#64748b;margin-top:8px">Alemania lidera con Holanda como
    puerta de entrada europea. <b>China ya es el segundo origen</b> (US$15,7M), pero vía
    productos de terceros, no de sistemas completos de control.</p>
  </div>
</div>

<h2>Qué significa para vender el ECS-700</h2>
<ul>
  <li><b>El mercado es de US$83,0M, no de US$341,5M.</b> Es noble saberlo: evita prometer una
      meta que no existe y evita competir donde no se juega.</li>
  <li><b>El DCS compite contra Siemens, ABB, Hitachi y Rockwell establecidos.</b> Ninguno es
      chino, así que no hay el prejuicio de origen que sí hay en válvulas manuales.</li>
  <li><b>La puerta de entrada no es el DCS solo.</b> El ECS-700 entra donde ya se vendió
      instrumentación o analítica: es la línea que cierra el proyecto completo.</li>
  <li><b>El SIS no se vende aparte.</b> El TCS-900 va dentro del proyecto de control, porque no
      existe un mercado separado que lo mida.</li>
  <li><b>Y el negocio eléctrico de las mismas partidas (US$139,5M) no es de SUPCON:</b> son
      subestaciones. Ahí CONECTA compite con su propia línea eléctrica, no con esto.</li>
</ul>

<footer>
  Fuente: Registro DIN de importaciones, Servicio Nacional de Aduanas de Chile, año 2025.
  Partidas 8537, 8538 y 9032. Separación por glosa del ítem y marca del fabricante.
  El valor no clasificable se declara como tal, no se reparte.
  <br>Ver <a href="hardware_partidas_2025.html">hardware por partida</a> ·
  <a href="valvulas_manual_control_2025.html">válvulas: manuales vs control</a> ·
  <a href="../artefactos/metodologia_mercado.html">metodología</a> ·
  <a href="../artefactos/estrategia_normativa.html">estrategia normativa</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
