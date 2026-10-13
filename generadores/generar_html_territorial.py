#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/estrategia_territorial.html — dónde y qué vender, por zona."""
import os, json, html
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"artefactos","estrategia_territorial.html")
d=json.load(open(os.path.join(D,"estrategia_territorial.json"),encoding="utf-8"))
Z=d["zonas"]; orden=d["orden_por_atractivo"]; PROD=d["producto_por_linea"]
NORM=d["disparador_normativo"]; MER=d["mercado_por_linea_usd"]

def usd(v):
    if not v: return "—"
    return "US$" + f"{v/1e6:,.1f}".replace(",","X").replace(".",",").replace("X",".")

# por qué cada línea entra en cada zona (la norma que la empuja)
RAZON_LINEA = {
 "Instrumentación": "Medición obligatoria de variables: caudal y pH en efluentes (DS 90/2000 y DS 609/1998), NTSyCS 4-12 en instalaciones coordinadas.",
 "Analítica": "CEMS obligatorio sobre 50 MWt (DS 13/2011) y monitoreo de emisiones: la línea con el disparador más directo y sin incumbente instalado.",
 "Válvulas": "Válvulas de seguridad y control en calderas (DS 10/2013) y corte de corrientes corrosivas en proceso continuo.",
 "DCS": "Proceso continuo que debe sostener disponibilidad: NTSyCS 4-12/4-16 exige SITR ≥99,5% y arranque antes de 5 s.",
 "PLC": "Control local y telemetría de instalaciones coordinadas; va dentro del proyecto de control, no se mide aparte.",
 "SIS": "Detección y extinción automática (DS 594 Art. 45, DS 43/2015, NFPA 72) y parada de emergencia en refinería y química.",
 "Software y plataforma": "Ciberseguridad de operadores críticos (Ley 21.663, 147 OIV eléctricos nombrados) y eficiencia (Ley 21.305).",
}
MER_LINEA = {"Instrumentación":MER.get("Instrumentación"),"Analítica":MER.get("Analítica"),
             "Válvulas":MER.get("Válvulas"),"DCS":MER.get("DCS y control"),
             "PLC":None,"SIS":None,"Software y plataforma":None}

bloques=""
for i,z in enumerate(orden,1):
    v=Z[z]
    puerta="".join(f'<span class="pu">{html.escape(p)}</span>' for p in v["lineas_puerta"])
    razones=""
    for p in v["lineas_puerta"]:
        m=MER_LINEA.get(p)
        mm=f'<span class="mm">{usd(m)}</span>' if m else '<span class="mm nm">no medible aparte</span>'
        razones+=f'''<div class="rz"><div class="rzh"><b>{html.escape(p)}</b>{mm}</div>
          <p>{html.escape(RAZON_LINEA.get(p,""))}</p></div>'''
    anclas="".join(f'''<tr><td><b>{html.escape(str(a["empresa"])[:44])}</b><span class="sub">{html.escape(a.get("comuna") or "")}</span></td>
      <td class="sen">{html.escape(a["rubro"][:24])}</td><td class="n">{a["dolor"]:.0f}</td></tr>''' for a in v["anclas"][:6])
    rubros="".join(f'''<div class="part"><div class="ph"><span>{html.escape(k[:30])}</span><span class="pv">{n}</span></div>
      <div class="bar"><div class="fill" style="width:{max(n/v["empresas_con_dolor"]*100,2):.0f}%"></div></div></div>'''
      for k,n in v["rubros"][:5])
    bloques+=f'''
<section class="zona">
  <div class="zh">
    <span class="rank">{i}</span>
    <h2>{z} · {html.escape(v["nombre"])}</h2>
    <span class="atr">atractivo {v["atractivo"]:,.0f}</span>
  </div>
  <div class="kz">
    <div><b>{v["empresas_con_dolor"]:,}</b>empresas con dolor</div>
    <div><b>{v["dolor_promedio"]:.0f}</b>dolor promedio</div>
    <div><b>{v["concentracion_rubro"]*100:.0f}%</b>en {html.escape(str(v["rubro_dominante"])[:22])}</div>
  </div>
  <h3>Puerta de entrada</h3>
  <div class="puertas">{puerta}</div>
  <div class="razones">{razones}</div>
  <div class="dos">
    <div>
      <h3>Rubros dominantes</h3>
      {rubros}
    </div>
    <div>
      <h3>Cuentas ancla</h3>
      <table>{anclas}</table>
    </div>
  </div>
</section>'''

# tabla resumen
resu=""
for i,z in enumerate(orden,1):
    v=Z[z]
    resu+=f'''<tr><td class="r">{i}</td><td><b>{z}</b> <span class="sub">{html.escape(v["nombre"][:34])}</span></td>
      <td class="n">{v["empresas_con_dolor"]:,}</td><td class="n">{v["dolor_promedio"]:.0f}</td>
      <td class="n">{v["atractivo"]:,.0f}</td><td>{html.escape(str(v["rubro_dominante"])[:26])}</td>
      <td class="lin">{html.escape(", ".join(v["lineas_puerta"][:3]))}</td></tr>'''

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Estrategia territorial — SUPCON Chile</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:1080px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:880px}}
h2{{font-size:20px;font-weight:660;letter-spacing:-.2px;flex:1}}
h3{{font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:16px 0 8px}}
p{{margin-bottom:10px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:16px 19px;margin:16px 0;font-size:14px}}
.warn{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:14px 0;font-size:14px}}
.warn b{{color:#92400e}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--cd);border-radius:12px;overflow:hidden;border:1px solid var(--bd)}}
th{{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:9px 10px;background:#fbfdff;border-bottom:2px solid var(--bd)}}
td{{padding:8px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.r{{color:#94a3b8;font-size:12px;font-variant-numeric:tabular-nums}}
.n{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}}
.sub{{display:block;font-size:11.5px;color:#94a3b8;font-weight:400}}
.sen{{font-size:12px;color:#475569}}
.lin{{font-size:12px;color:#64748b}}
.zona{{background:var(--cd);border:1px solid var(--bd);border-radius:14px;padding:20px 23px;margin-bottom:16px}}
.zh{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:12px}}
.rank{{background:#eff6ff;color:#2563eb;font-weight:700;font-size:13px;border-radius:7px;padding:3px 10px}}
.atr{{font-size:12px;color:#64748b;background:#f8fafc;border:1px solid var(--bd);border-radius:6px;padding:3px 10px}}
.kz{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:6px}}
.kz div{{background:#fbfdff;border:1px solid var(--bd);border-radius:9px;padding:9px 14px;font-size:11.5px;color:var(--mu)}}
.kz b{{display:block;font-size:18px;font-weight:700;color:var(--tx)}}
.puertas{{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:4px}}
.pu{{background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;border-radius:7px;padding:4px 12px;font-weight:650;font-size:13px}}
.razones{{margin:10px 0 14px}}
.rz{{border-left:3px solid #e2e8f0;padding:6px 0 6px 12px;margin-bottom:9px}}
.rzh{{display:flex;align-items:baseline;gap:10px}}
.rzh b{{font-size:13.5px}}
.mm{{font-size:11.5px;color:#047857;font-weight:600;background:#ecfdf5;border-radius:5px;padding:1px 7px}}
.mm.nm{{color:#64748b;background:#f1f5f9}}
.rz p{{font-size:12.5px;color:#64748b;margin:3px 0 0}}
.dos{{display:grid;grid-template-columns:1fr 1.3fr;gap:22px}}
@media(max-width:760px){{.dos{{grid-template-columns:1fr}}}}
.part{{margin-bottom:9px}}
.ph{{display:flex;justify-content:space-between;gap:10px;margin-bottom:4px;font-size:12.5px}}
.pv{{font-weight:700;font-variant-numeric:tabular-nums}}
.bar{{height:5px;background:#f1f5f9;border-radius:3px;overflow:hidden}}
.fill{{height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:3px}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Estrategia territorial: dónde poner el esfuerzo</h1>
<p class="sub">Las 1.496 empresas con dolor verificado repartidas en 7 zonas, con el rubro que domina
cada una y la línea de producto que entra por la puerta. El orden no es por tamaño: es por
atractivo comercial.</p>

<div class="kpi">
  <div><b>7</b>zonas priorizadas</div>
  <div><b>1.496</b>empresas con dolor</div>
  <div><b>42</b>dolor promedio más alto (Z2)</div>
  <div><b>7</b>líneas de producto</div>
</div>

<div class="metodo">
  <b>Cómo se ordena.</b> El atractivo pondera tres cosas medidas:
  <b>tamaño</b> (cuántas empresas con dolor), <b>intensidad</b> (el dolor promedio — una zona con
  pocas empresas y dolor alto convierte mejor que una con muchas y dolor bajo) y
  <b>concentración</b> (qué tan dominante es el rubro principal: una zona homogénea replica el
  mismo argumento en cada cuenta, sin rearmar el discurso cada vez).
  <br><br>
  <b>Por qué el orden no sigue el volumen.</b> Santiago tiene 479 empresas con dolor — el triple
  que el norte minero — pero su dolor promedio es 19 contra 42. En Santiago compites con todos y
  contra un canal ya saturado; en Antofagasta la demanda es intensa y el canal local es mínimo.
</div>

<div class="warn">
  <b>Una advertencia sobre estos números.</b> El dolor mide <b>obligación verificada</b>
  (emisiones al agua, residuos peligrosos, incumplimiento ante el Coordinador Eléctrico), no
  intención de compra. Una empresa con dolor alto <i>debe</i> medir algo que hoy no mide en línea
  — eso es el gancho, pero la venta depende de llegar en el momento de su ciclo de inversión.
  <br><br>
  <b>Y las multas SEC no están incorporadas</b>: la SEC no publica ese dataset. Sumarlas subiría
  el dolor del sector eléctrico en todas las zonas.
</div>

<h2>El orden de ataque</h2>
<table>
  <tr><th>#</th><th>Zona</th><th class="n">Empresas</th><th class="n">Dolor prom.</th>
      <th class="n">Atractivo</th><th>Rubro dominante</th><th>Puerta de entrada</th></tr>
  {resu}
</table>

{bloques}

<h2>Qué producto va en cada línea</h2>
<table>
  <tr><th>Línea</th><th class="n">Productos</th><th class="n">Mercado</th><th>Disparador normativo</th></tr>
  {"".join(f'<tr><td><b>{html.escape(k)}</b></td><td class="n">{v["n_productos"]}</td><td class="n">{usd(v["mercado_corregido_usd"])}</td><td class="sen">{html.escape(RAZON_LINEA.get(k,"")[:120])}</td></tr>' for k,v in PROD.items())}
</table>

<h2>La lectura del conjunto</h2>
<ul style="list-style:none">
  <li style="position:relative;padding-left:17px;margin-bottom:7px"><b style="color:#2563eb">·</b>
    <b>Z2 (norte minero) es la zona más rentable por viaje</b>: 91 empresas con el dolor promedio
    más alto del país (42) y sin canal local. No se atiende con distribuidor: exige presencia propia.</li>
  <li style="position:relative;padding-left:17px;margin-bottom:7px"><b style="color:#2563eb">·</b>
    <b>Z5 (sur acuícola) es la zona más replicable</b>: 218 empresas, 41% en pesca, todas con el
    mismo problema de RILES. Un caso de referencia sirve para todo el clúster.</li>
  <li style="position:relative;padding-left:17px;margin-bottom:7px"><b style="color:#2563eb">·</b>
    <b>Z4 (Biobío) es donde está el proyecto grande</b>: Arauco, ENAP, Colbún, Enel. Pocas cuentas
    pero de ticket alto — celulosa, refinería y generación.</li>
  <li style="position:relative;padding-left:17px;margin-bottom:7px"><b style="color:#2563eb">·</b>
    <b>Z1 (Santiago) entra pero no primero</b>: es donde está el canal y las casas matrices, así
    que sirve para abrir puertas, no para concentrar la venta técnica.</li>
  <li style="position:relative;padding-left:17px;margin-bottom:7px"><b style="color:#2563eb">·</b>
    <b>Z7 (Maule-O'Higgins) es la más dispersa</b>: dolor promedio 13, el más bajo. Agroindustria
    y manufactura liviana: sin urgencia normativa, sin ticket.</li>
</ul>

<footer>
  Fuentes: <b>RETC del MMA</b> (emisiones al agua y residuos peligrosos) + <b>Coordinador
  Eléctrico Nacional</b> (completitud y calidad) para el dolor; <b>mapa de oportunidades</b> para
  las zonas; <b>Aduanas 2025 por partida arancelaria</b> para el mercado de cada línea;
  <b>catálogo de 63 fichas</b> para los productos. Nada estimado.
  <br>Ver <a href="universo_prospeccion.html">universo de prospección</a> ·
  <a href="objetivos_priorizados.html">objetivos priorizados</a> ·
  <a href="escalera_exito.html">escalera al éxito</a> ·
  <a href="mapa_oportunidades.html">mapa geográfico</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print("zonas:", len(orden), "| filas resumen:", resu.count("<tr>"))
