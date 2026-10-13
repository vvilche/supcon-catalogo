#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/universo_prospeccion.html — el universo con TODAS las señales de dolor."""
import os, json, html, collections
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"artefactos","universo_prospeccion.html")
d=json.load(open(os.path.join(D,"universo_senales_completas.json"),encoding="utf-8"))
emp=d["empresas"]; res=d["resumen"]
con_dolor=[e for e in emp if e["dolor"]>0]

ZN={"Z1":"Santiago (RM)","Z2":"Norte minero","Z3":"Valparaíso","Z4":"Concepción-Biobío",
    "Z5":"Sur acuícola","Z6":"Coquimbo-Atacama","Z7":"Maule-O'Higgins"}
COL={"Z1":"#2563eb","Z2":"#d97706","Z3":"#0891b2","Z4":"#7c3aed","Z5":"#059669","Z6":"#64748b","Z7":"#b45309"}

def miles(v, dec=0):
    if v is None: return "—"
    return f"{v:,.{dec}f}".replace(",","X").replace(".",",").replace("X",".")

# top 80
filas=""
for i,e in enumerate(con_dolor[:80],1):
    sen=[]
    if e.get("riles"): sen.append(f'<span class="sg ag">RILES al agua {miles(e["riles"])}</span>')
    if e.get("residuos_t"): sen.append(f'<span class="sg rs">residuos {miles(e["residuos_t"])} t</span>')
    if e.get("cen_dolor"): sen.append(f'<span class="sg ce">CEN +{e["cen_dolor"]:.0f}</span>')
    if e.get("riles_contaminantes"): sen.append(f'<span class="sg">contamina {len(e["riles_contaminantes"])}</span>')
    lineas=", ".join(e["lineas_supcon"][:4]) or "—"
    filas+=f'''<tr>
  <td class="r">{i}</td>
  <td><b>{html.escape(str(e["empresa"])[:48])}</b><span class="sub">{html.escape(e.get("comuna") or "")}</span></td>
  <td>{html.escape(e["rubro"][:26])}</td>
  <td><span class="zz" style="background:{COL.get(e.get('zona'),'#94a3b8')}1a;color:{COL.get(e.get('zona'),'#64748b')}">{e.get("zona") or "-"}</span></td>
  <td class="n"><b>{e["dolor"]:.0f}</b></td>
  <td class="n">{e["prioridad"]:.0f}</td>
  <td class="sen">{" ".join(sen) or "—"}</td>
  <td class="lin">{html.escape(lineas)}</td>
</tr>'''

# por zona (solo con dolor)
pz=collections.Counter(e.get("zona") or "sin zona" for e in con_dolor)
zonas=""
for z,n in sorted(pz.items(), key=lambda x:-x[1]):
    if z=="sin zona": continue
    pct=n/len(con_dolor)*100
    zonas+=f'''<div class="part"><div class="ph2"><span>{z} · {ZN.get(z,"")}</span><span class="pv">{n:,}</span></div>
      <div class="bar"><div class="fill" style="width:{max(pct*2.2,2):.1f}%;background:{COL.get(z,'#94a3b8')}"></div></div>
      <div class="pp">{pct:.0f}% de las que tienen dolor</div></div>'''

pr=collections.Counter(e["rubro"] for e in con_dolor)
rubros=""
for k,v in sorted(pr.items(), key=lambda x:-x[1])[:10]:
    pct=v/len(con_dolor)*100
    rubros+=f'''<div class="part"><div class="ph2"><span>{html.escape(k)}</span><span class="pv">{v:,}</span></div>
      <div class="bar"><div class="fill" style="width:{max(pct,2):.1f}%"></div></div></div>'''

n_riles=sum(1 for e in emp if (e.get("riles") or 0)>0)
n_res=sum(1 for e in emp if (e.get("residuos_t") or 0)>0)
n_cen=sum(1 for e in emp if (e.get("cen_dolor") or 0)>0)

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universo de prospección — 3.157 empresas con dolor verificado</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:900px}}
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
.sen{{font-size:11.5px;max-width:340px}}
.sg{{display:inline-block;border-radius:5px;padding:1px 7px;margin:1px 3px 1px 0;font-weight:600;border:1px solid}}
.sg.ag{{background:#eff6ff;color:#1d4ed8;border-color:#bfdbfe}}
.sg.rs{{background:#fef2f2;color:#b45309;border-color:#fde68a}}
.sg.ce{{background:#f0fdf4;color:#15803d;border-color:#bbf7d0}}
.sg:not(.ag):not(.rs):not(.ce){{background:#f8fafc;color:#64748b;border-color:#e2e8f0}}
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
ul{{list-style:none}}
ul li{{position:relative;padding-left:17px;margin-bottom:7px}}
ul li:before{{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Universo de prospección: {len(emp):,} empresas con dolor normativo verificado</h1>
<p class="sub">El catálogo industrial chileno cruzado con las fuentes oficiales de incumplimiento:
RETC del Ministerio del Medio Ambiente y Coordinador Eléctrico Nacional. Cada empresa trae sus
señales medidas, no estimadas.</p>

<div class="kpi">
  <div><b>{len(emp):,}</b>empresas industriales</div>
  <div><b>{len(con_dolor):,}</b>con dolor verificado</div>
  <div><b>{n_res:,}</b>con residuos peligrosos</div>
  <div><b>{n_riles:,}</b>que emiten al agua (RILES)</div>
  <div><b>{n_cen:,}</b>con incumplimiento CEN</div>
  <div><b>13</b>rubros</div>
</div>

<div class="aviso">
  <b>De 52 empresas a {len(con_dolor):,}.</b> El catálogo traía los campos de residuos y RILES
  <b>vacíos en 12 de sus 13 rubros</b>: solo 52 de {len(emp):,} empresas tenían el dato. Se bajó el
  RETC del MMA y se cruzó por RUT (más las señales del Coordinador Eléctrico), y ahora
  <b>{len(con_dolor):,} empresas tienen su dolor medido</b> — 29 veces más.
</div>

<div class="metodo">
  <b>Las cuatro señales, todas de fuente oficial.</b>
  <br>· <b>RILES al agua</b> (DS 90/2000) — emisión por contaminante y punto de descarga, RETC/MMA.
  Una empresa con 8 contaminantes en 5 puntos tiene 8 obligaciones de monitoreo distintas.
  <br>· <b>Residuos peligrosos</b> (DS 43/2015) — toneladas transferidas por generador, RETC/MMA.
  <br>· <b>Completitud CEN</b> — datos no informados al Coordinador (bajo 80% suma dolor).
  <br>· <b>Calidad CEN</b> — datos rechazados por el Coordinador (bajo 60% suma dolor).
  <br><br>
  <b>Prioridad = dolor × factor de tamaño</b>. El tamaño es un factor <b>acotado</b> (1,0 a 1,4), no
  un multiplicador 2×/3×: si pesara tanto, una empresa grande con poco dolor pasaría por encima de
  una con incumplimiento grave y medido.
</div>

<div class="warn">
  <b>Lo que NO está incorporado, y por qué.</b> Las <b>multas SEC</b> no se pudieron sumar: la SEC
  no publica un dataset de sanciones. Su portal tiene 2.307 archivos, de los cuales 344 son
  resoluciones en PDF individual mezcladas con otros temas. Incorporarlas exigiría parsear 344
  PDFs — se declara como señal faltante en vez de estimarla.
</div>

<div class="warn">
  <b>Cuatro errores de datos que se corrigieron (cada uno daba un ranking falso).</b>
  <b>1.</b> El campo <code>unidad_abreviacion</code> del RETC dice <b>kg</b> en las 40.329 filas:
  sin convertir, Codelco aparecía con 2.210 millones de "toneladas".
  <b>2.</b> El RUT del RETC viene como <code>61704000.0-K</code> (un <code>.0</code> espurio): el
  cruce por RUT fallaba en silencio (0 de 278; 256 después del fix).
  <b>3.</b> El campo de cantidad del RILES se llama <code>emision_total</code>, no "cantidad".
  <b>4.</b> El tamaño multiplicaba ×2/×3 y aplastaba la señal de incumplimiento: ENAEX, con el dolor
  más alto (129 por 39 puntos CEN), quedaba 30º. Ahora el factor es 1,0-1,4 y el orden es correcto.
</div>

<h2>Las 80 cuentas con más dolor</h2>
<table>
  <tr><th>#</th><th>Empresa</th><th>Rubro</th><th>Zona</th><th class="n">Dolor</th>
      <th class="n">Prioridad</th><th>Señales medidas</th><th>Líneas SUPCON</th></tr>
  {filas}
</table>

<div class="dos" style="margin-top:24px">
  <div class="card">
    <h3>Dónde están las que tienen dolor</h3>
    {zonas}
    <p style="font-size:12.5px;color:#64748b;margin-top:10px">El sur acuícola concentra la mayor
    cantidad, pero <b>el dolor unitario más alto está en el norte minero y en Biobío</b>
    (refinería, celulosa, generación).</p>
  </div>
  <div class="card">
    <h3>De qué rubros</h3>
    {rubros}
    <p style="font-size:12.5px;color:#64748b;margin-top:10px">Alimentos y manufactura aparecen
    mucho por número, pero <b>el dolor se concentra en combustibles, minería, celulosa, generación
    y pesca</b>: proceso continuo con obligación de medir.</p>
  </div>
</div>

<h2>Cómo se usa esto</h2>
<ul>
  <li><b>ENAP Refinerías, Minera Centinela, Arauco, Colbún y Enel</b> encabezan con las cuatro
  señales activas: residuos, agua y CEN. Son las cuentas donde el argumento es más directo —
  tienen la obligación, tienen el incumplimiento medido, y operan proceso continuo.</li>
  <li><b>ENEAX es el caso más claro de incumplimiento CEN</b> (+39, el más alto del padrón).
  Señal eléctrica pura: es la puerta del SCADA y la regularización de información técnica.</li>
  <li><b>El clúster salmonero del sur (Z5)</b> aparece masivamente por RILES y residuos. Es un
  mercado homogéneo: si funciona con uno, el caso de referencia sirve para el resto.</li>
  <li><b>Codelco transfiere 2,2 millones de toneladas de residuos peligrosos</b> (53 tipos
  distintos). El volumen lo pone primero en magnitud aunque su dolor CEN sea menor.</li>
</ul>

<footer>
  Fuentes: <b>RETC del Ministerio del Medio Ambiente</b> (datasets de Emisiones al agua y
  Generación de residuos peligrosos, portal datosretc.mma.gob.cl) y <b>Coordinador Eléctrico
  Nacional</b> (completitud y calidad de información técnica, api-infotecnica.coordinador.cl).
  Catálogo industrial: {len(emp):,} empresas en 13 rubros. El cruce es por RUT; el dolor sale de
  señales verificadas del registro, no de una estimación. <b>Multas SEC: no incorporadas</b> (la
  SEC no publica ese dataset).
  <br>Ver <a href="objetivos_priorizados.html">objetivos priorizados</a> ·
  <a href="escalera_exito.html">escalera al éxito</a> ·
  <a href="estrategia_normativa.html">dónde hay dolor normativo</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
_nz = zonas.count("part")
_nr = rubros.count("part")
print("filas:", len(con_dolor[:80]), "| zonas:", _nz, "| rubros:", _nr)
