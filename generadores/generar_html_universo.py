#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/universo_prospeccion.html — 3.157 empresas con dolor RETC real."""
import os, json, html, collections
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"artefactos","universo_prospeccion.html")
d=json.load(open(os.path.join(D,"universo_prospeccion_supcon.json"),encoding="utf-8"))
r=json.load(open(os.path.join(D,"retc_empresas.json"),encoding="utf-8"))
emp=d["empresas"]
con_dolor=[e for e in emp if e["dolor"]>0]
res=d["resumen"]

ZN={"Z1":"Santiago (RM)","Z2":"Norte minero","Z3":"Valparaíso","Z4":"Concepción-Biobío",
    "Z5":"Sur acuícola","Z6":"Coquimbo-Atacama","Z7":"Maule-O'Higgins"}
COL={"Z1":"#2563eb","Z2":"#d97706","Z3":"#0891b2","Z4":"#7c3aed","Z5":"#059669","Z6":"#64748b","Z7":"#b45309"}

# top 60 con dolor
top=con_dolor[:60]
filas=""
for i,e in enumerate(top,1):
    sen=" · ".join(e["senales_dolor"]) or "—"
    lineas=", ".join(e["lineas_supcon"][:4])
    filas+=f'''<tr>
  <td class="r">{i}</td>
  <td><b>{html.escape(str(e["empresa"])[:46])}</b><span class="sub">{html.escape(e["comuna"] or "")}</span></td>
  <td>{html.escape(e["rubro"][:26])}</td>
  <td><span class="zz" style="background:{COL.get(e['zona'],'#94a3b8')}1a;color:{COL.get(e['zona'],'#64748b')}">{e["zona"] or "-"}</span></td>
  <td class="n">{e["dolor"]:.0f}</td>
  <td class="n"><b>{e["prioridad"]:.0f}</b></td>
  <td class="sen">{html.escape(sen)}</td>
  <td class="lin">{html.escape(lineas)}</td>
</tr>'''

# zonas
zonas=""
for z,n in sorted(res["por_zona"].items(), key=lambda x:-x[1]):
    if z=="sin zona" or not n: continue
    pct=n/len(emp)*100
    zonas+=f'''<div class="part"><div class="ph2"><span>{z} · {ZN.get(z,"")}</span><span class="pv">{n:,}</span></div>
      <div class="bar"><div class="fill" style="width:{max(pct*1.6,2):.1f}%;background:{COL.get(z,'#94a3b8')}"></div></div>
      <div class="pp">{pct:.0f}% del padrón</div></div>'''

# rubros
rubros=""
for k,v in sorted(res["por_rubro"].items(), key=lambda x:-x[1])[:10]:
    pct=v/len(emp)*100
    rubros+=f'''<div class="part"><div class="ph2"><span>{html.escape(k)}</span><span class="pv">{v:,}</span></div>
      <div class="bar"><div class="fill" style="width:{max(pct,2):.1f}%"></div></div></div>'''

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universo de prospección — 3.157 empresas con dolor RETC</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:880px}}
h2{{font-size:20px;font-weight:660;margin:34px 0 12px;letter-spacing:-.2px}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:18px 0 9px}}
p{{margin-bottom:11px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:16px 19px;margin:16px 0;font-size:14px}}
.aviso{{background:#ecfdf5;border:1px solid #a7f3d0;border-left:4px solid #047857;border-radius:9px;padding:15px 18px;margin:15px 0;font-size:14px}}
.aviso b{{color:#047857}}
.warn{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:14px 0;font-size:14px}}
.warn b{{color:#92400e}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--cd);border-radius:12px;overflow:hidden;border:1px solid var(--bd)}}
th{{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:9px 10px;background:#fbfdff;border-bottom:2px solid var(--bd)}}
td{{padding:8px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.r{{color:#94a3b8;font-size:12px;font-variant-numeric:tabular-nums}}
.n{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}}
.sub{{display:block;font-size:11.5px;color:#94a3b8;font-weight:400}}
.zz{{font-size:11px;font-weight:700;border-radius:5px;padding:2px 7px}}
.sen{{font-size:12px;color:#475569}}
.lin{{font-size:11.5px;color:#64748b}}
.dos{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
@media(max-width:760px){{.dos{{grid-template-columns:1fr}}}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:17px 20px}}
.part{{margin-bottom:11px}}
.ph2{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:5px;font-size:13.5px}}
.pv{{font-weight:700;font-variant-numeric:tabular-nums}}
.bar{{height:6px;background:#f1f5f9;border-radius:3px;overflow:hidden}}
.fill{{height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:3px}}
.pp{{font-size:11px;color:var(--mu);margin-top:3px}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Universo de prospección: 3.157 empresas con dolor normativo real</h1>
<p class="sub">El catálogo industrial completo cruzado con el RETC del Ministerio del Medio Ambiente.
Cada empresa trae su dolor medido: cuántos residuos peligrosos genera y cuánto emite al agua.</p>

<div class="kpi">
  <div><b>3.157</b>empresas industriales</div>
  <div><b>1.481</b>con dolor verificado</div>
  <div><b>1.434</b>con residuos peligrosos</div>
  <div><b>292</b>que emiten al agua (RILES)</div>
  <div><b>13</b>rubros</div>
</div>

<div class="aviso">
  <b>Esto es lo que faltaba.</b> El catálogo traía los campos de residuos y RILES <b>vacíos en 12
  de sus 13 rubros</b> — solo 52 de 3.157 empresas tenían el dato, y apenas 2 declaraban RILES.
  Con eso el motor de leads no podía calcular dolor de agua en casi ningún rubro. Se bajó el
  RETC del Ministerio del Medio Ambiente y se cruzó por RUT: <b>ahora 1.481 empresas tienen su
  dolor medido</b>, 28 veces más que antes.
</div>

<div class="metodo">
  <b>Cómo se mide el dolor.</b> No es una estimación: son señales del registro oficial.
  <b>Residuos peligrosos</b> (DS 43/2015): toneladas transferidas por generador.
  <b>RILES</b> (DS 90/2000): emisión al agua por contaminante y punto de descarga — 10.870
  registros de la SMA. Y <b>más contaminantes distintos = más obligaciones de monitoreo</b>,
  que es justo lo que vende un sistema de medición en línea.
  <br><br>
  <b>Prioridad = dolor × capacidad</b> (tier GRANDE=3, MEDIANA=2, PEQUEÑA=1), y dentro del empate
  se ordena por <b>magnitud real</b>: no vale lo mismo una planta que emite 10 toneladas que una
  que emite 50.000.
</div>

<div class="warn">
  <b>Tres cosas que se corrigieron al verificar, y conviene saber.</b>
  <b>Uno:</b> el RUT del RETC viene como <code>61704000.0-K</code> — un <code>.0</code> espurio que
  hacía fallar <b>todo</b> el cruce por RUT en silencio (256 de 278 empresas cruzaban mal).
  <b>Dos:</b> el campo de cantidad del RILES se llama <code>emision_total</code>, no "cantidad":
  buscarlo por nombre obvio daba 0 empresas.
  <b>Tres:</b> los datos traen <b>RUT y razón social</b>, así que el cruce es determinista — no
  hubo que usar el nombre aproximado en la mayoría de los casos.
</div>

<h2>Las 60 cuentas con más dolor</h2>
<table>
  <tr><th>#</th><th>Empresa</th><th>Rubro</th><th>Zona</th><th class="n">Dolor</th>
      <th class="n">Prioridad</th><th>Señal medida</th><th>Líneas SUPCON</th></tr>
  {filas}
</table>

<div class="dos" style="margin-top:24px">
  <div class="card">
    <h3>Dónde están (por zona priorizada)</h3>
    {zonas}
    <p style="font-size:12.5px;color:#64748b;margin-top:10px">Santiago concentra el padrón
    administrativo, pero <b>Biobío (506)</b> y el <b>sur acuícola (369)</b> tienen la mayor
    densidad de proceso continuo con dolor.</p>
  </div>
  <div class="card">
    <h3>De qué rubros (top 10)</h3>
    {rubros}
    <p style="font-size:12.5px;color:#64748b;margin-top:10px">Manufacturera, agropecuaria y
    alimentos dominan por número; <b>pero el dolor se concentra en celulosa, minería, generación,
    combustibles y pesca</b>, que es donde hay proceso continuo que medir.</p>
  </div>
</div>

<h2>Qué hacer con esto</h2>
<p><b>El dolor medido es la puerta de entrada.</b> Una empresa que emite al agua por 5 puntos de
descarga con 8 contaminantes distintos tiene una obligación de monitoreo, no un interés
abstracto. Ese es el gancho: <i>"usted tiene que medir esto y hoy no lo mide en línea"</i>.</p>
<p>Y cruza con lo demás: <b>Colbún y AES Gener</b> ya aparecían en el cruce de capital chino y en
la escalera de generación; acá aparecen además con dolor de residuos. <b>Codelco</b> sale en dos
rubros (extracción y metalurgia) porque tiene plantas distintas.</p>

<footer>
  Fuente: catálogo industrial CONECTA (3.157 empresas, 13 rubros, RETC/ventanilla única) cruzado
  con el <b>RETC del Ministerio del Medio Ambiente</b> — datasets de Emisiones al agua y
  Generación de residuos peligrosos, vía el portal de datos abiertos
  (datosretc.mma.gob.cl). El cruce es por RUT; el dolor sale de señales verificadas del registro,
  no de una estimación.
  <br>Ver <a href="objetivos_priorizados.html">objetivos priorizados</a> ·
  <a href="escalera_exito.html">escalera al éxito</a> ·
  <a href="estrategia_normativa.html">dónde hay dolor normativo</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
nz = zonas.count("part")
nr = rubros.count("part")
print("top:", len(top), "filas | zonas:", nz, "| rubros:", nr)
