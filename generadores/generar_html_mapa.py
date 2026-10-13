#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/mapa_oportunidades.html desde datos/mapa_oportunidades_chile.json.
Estilo CONECTA: bg #f8fafc, accent #2563eb, sin rojos."""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(BASE, 'datos/mapa_oportunidades_chile.json')))
html = []
A = html.append

A('''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mapa de oportunidades geográficas — SUPCON en Chile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706;--ams:#fffbeb;--ok:#047857;--oks:#ecfdf5}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}
.wrap{max-width:1040px;margin:0 auto}
h1{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}
.sub{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:880px}
h2{font-size:20px;font-weight:660;margin:38px 0 10px;letter-spacing:-.2px}
h3{font-size:16.5px;font-weight:650;margin:0 0 7px}
p{margin-bottom:11px}
ul{list-style:none;margin:9px 0 12px}
ul li{position:relative;padding-left:17px;margin-bottom:6px}
ul li:before{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}
code{background:#f1f5f9;padding:1px 6px;border-radius:4px;font-size:13px;font-family:ui-monospace,monospace}
table{width:100%;border-collapse:collapse;margin:13px 0;font-size:14px}
th{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--bd)}
td{padding:9px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}
tr:last-child td{border-bottom:none}
.num{text-align:right;font-variant-numeric:tabular-nums}
.box{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:15px 18px;margin:14px 0}
.aviso{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:15px 0;font-size:14px}
.aviso b{color:#92400e}
.ok{background:var(--oks);border:1px solid #a7f3d0;border-left:4px solid var(--ok);border-radius:9px;padding:14px 17px;margin:15px 0;font-size:14px}
.ok b{color:var(--ok)}
.zona{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:18px 21px;margin-bottom:15px;border-left:4px solid #64748b}
.zona.p1{border-left-color:#047857}.zona.p2{border-left-color:#2563eb}
.zona.p3{border-left-color:#d97706}.zona.p4{border-left-color:#0891b2}
.zona.p5{border-left-color:#94a3b8}.zona.p6{border-left-color:#cbd5e1}
.zh{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;margin-bottom:9px}
.zh h3{margin:0}
.pri{font-size:11px;border-radius:5px;padding:2px 9px;font-weight:700;text-transform:uppercase;letter-spacing:.3px}
.pri.a{background:var(--oks);color:var(--ok)}.pri.b{background:var(--acs);color:var(--ac)}
.pri.c{background:var(--ams);color:var(--am)}.pri.d{background:#f1f5f9;color:#475569}
.dos{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:11px}
@media(max-width:720px){.dos{grid-template-columns:1fr}}
.dos h4{font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;margin-bottom:5px}
.celda{background:#fbfdff;border:1px solid var(--bd);border-radius:8px;padding:11px 13px;font-size:13.5px}
.bar{display:flex;align-items:center;gap:8px}
.bar .fill{height:13px;border-radius:3px;background:var(--ac);min-width:2px}
.bar .fill.g{background:#047857}.bar .fill.s{background:#94a3b8}
.et{font-size:10.5px;border-radius:5px;padding:1px 7px;font-weight:700;text-transform:uppercase;letter-spacing:.3px;white-space:nowrap}
.et.m{background:var(--oks);color:var(--ok)}.et.i{background:var(--ams);color:var(--am)}
footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}
footer a{color:var(--ac)}
.mono{font-family:ui-monospace,monospace;font-size:12.5px}
.sub2{font-size:12.5px;color:var(--mu);margin-bottom:10px}
</style></head><body><div class="wrap">''')

A('<h1>Mapa geográfico de oportunidades</h1>')
A('<p class="sub">Dónde está la demanda industrial y dónde está el canal importador del rubro automatización en Chile, cruzados para concentrar el esfuerzo comercial del portafolio SUPCON/Hobré. Datos 2025 de InfoTécnica CEN, RETC/MMA, SEIA y el registro de importaciones de Aduanas.</p>')

# ---- Resumen ejecutivo ----
c = D['canal_resumen']
A('<h2>1 · El hallazgo central: la demanda y el canal están en lugares distintos</h2>')
A(f'''<div class="aviso"><b>Asimetría estructural (MEDIDO).</b> El canal importador del rubro está
hiperconcentrado en Santiago: <b>{c["n_importadores_rubro"]:,} importadores</b> mueven
<b>US${c["usd_rubro_2025"]/1e6:,.1f}M</b> al año, de los cuales
<b>{c["pct_region_metropolitana_n"]}% (por número)</b> y <b>{c["pct_region_metropolitana_usd"]}% (por volumen)</b>
operan desde la Región Metropolitana. Una sola comuna, <b>Las Condes</b>, concentra el
<b>{c["pct_las_condes_usd"]}% de todo el dinero</b> importado del rubro en Chile.
La demanda industrial de proceso, en cambio, está en las regiones: Antofagasta, Biobío y Valparaíso,
donde el canal local es mínimo (24, 28 y 76 importadores respectivamente).</div>''')

# ---- Mapa de demanda por region ----
A('<h2>2 · Mapa de demanda: dónde están los clientes</h2>')
A('<p>Conteo de establecimientos industriales por región (RETC/MMA, 26.649 establecimientos industriales en el país), centrales generadoras coordinadas al SEN (InfoTécnica CEN, 1.218 totales) y proyectos en el SEIA. Las columnas de industria cuentan establecimientos del rubro RETC correspondiente.</p>')
A('<table><thead><tr><th>Región</th><th class="num">Centrales CEN</th><th class="num">Establec. RETC (rubros clave)</th><th class="num">Proyectos SEIA</th><th class="num">Canal: importadores</th><th class="num">Canal: US$ rubro</th></tr></thead><tbody>')
for d in D['demanda_por_region']:
    n_ind = sum(x['establecimientos_retc'] for x in d['establecimientos_por_industria'])
    cr = next((x for x in D['canal_por_region'] if x['region'] == d['region']), None)
    cn = cr['n_importadores'] if cr else 0
    cu = cr['usd_rubro'] if cr else 0
    A(f'<tr><td><b>{d["region"]}</b></td><td class="num">{d["centrales_cen"]}</td><td class="num">{n_ind}</td><td class="num">{d["n_proyectos_seia"]}</td><td class="num">{cn}</td><td class="num">{cu/1e6:,.2f}M</td></tr>')
A('</tbody></table>')

A('<h3>Detalle industrial por región (empresas y plantas con nombre)</h3>')
for d in D['demanda_por_region']:
    A(f'<div class="box"><h3>Región de {d["region"]}</h3>')
    if d['establecimientos_por_industria']:
        inds = ' · '.join(f'{x["industria"]} ({x["establecimientos_retc"]})' for x in d['establecimientos_por_industria'][:6])
        A(f'<p class="sub2"><b>Establecimientos por industria (RETC):</b> {inds}</p>')
    if d['empresas']:
        A(f'<p class="sub2"><b>Empresas presentes:</b> {", ".join(d["empresas"])}</p>')
    if d['plantas_principales']:
        A('<p class="sub2"><b>Proyectos/plantas principales (SEIA, por inversión):</b></p><ul>')
        for p in d['plantas_principales'][:5]:
            A(f'<li>{p}</li>')
        A('</ul>')
    A(f'<p class="sub2">{d["nota"]}</p></div>')

# ---- Mapa de canal ----
A('<h2>3 · Mapa de canal: dónde están los que venden</h2>')
A('<p>Distribución geográfica de los 1.946 importadores del rubro automatización/instrumentación (Aduanas 2025). Comuna de despacho del importador. El 88,4% está en la Región Metropolitana.</p>')
A('<table><thead><tr><th>#</th><th>Comuna</th><th>Región</th><th class="num">Importadores</th><th class="num">US$ rubro 2025</th><th class="num">% volumen</th><th>Participación</th></tr></thead><tbody>')
maxp = D['canal_por_comuna'][0]['pct'] if D['canal_por_comuna'] else 1
for i, x in enumerate(D['canal_por_comuna'][:25], 1):
    w = max(2, int(x['pct'] / maxp * 260))
    cls = 'g' if x['pct'] >= 20 else ('' if x['pct'] >= 3 else 's')
    A(f'<tr><td class="num">{i}</td><td><b>{x["comuna"]}</b></td><td>{x["region"]}</td>'
      f'<td class="num">{x["n_importadores"]}</td><td class="num">{x["usd_rubro"]/1e6:,.2f}M</td>'
      f'<td class="num">{x["pct"]}%</td>'
      f'<td><div class="bar"><div class="fill {cls}" style="width:{w}px"></div><span class="mono">{x["pct"]}%</span></div></td></tr>')
A('</tbody></table>')

A('<h3>Distribución por región</h3>')
A('<table><thead><tr><th>Región</th><th class="num">Importadores</th><th class="num">% n.º</th><th class="num">US$ rubro</th><th class="num">% volumen</th></tr></thead><tbody>')
for x in D['canal_por_region']:
    if x['n_importadores'] == 0:
        continue
    A(f'<tr><td>{x["region"]}</td><td class="num">{x["n_importadores"]}</td><td class="num">{x["pct_n"]}%</td>'
      f'<td class="num">{x["usd_rubro"]/1e6:,.2f}M</td><td class="num">{x["pct_usd"]}%</td></tr>')
A('</tbody></table>')

# ---- Zonas prioritarias ----
A('<h2>4 · Cruce geográfico: las zonas donde concentrar el esfuerzo</h2>')
A('<p>Zonas ordenadas por atractivo, cruzando la densidad de demanda industrial (RETC + CEN + SEIA) con la presencia de canal (Aduanas). La pregunta que responde: <b>si CONECTA puede tocar solo 3 o 4 zonas en el primer año, ¿cuáles y por qué?</b></p>')
for z in D['zonas_prioritarias']:
    pcl = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'd', 6: 'd'}[z['prioridad']]
    ptx = {1: 'Prioridad 1', 2: 'Prioridad 2', 3: 'Prioridad 3', 4: 'Prioridad 4', 5: 'Vigilar', 6: 'Vigilar'}[z['prioridad']]
    A(f'<div class="zona p{z["prioridad"]}"><div class="zh"><h3>{z["zona"]}</h3><span class="pri {pcl}">{ptx}</span></div>')
    A(f'<p class="sub2">Regiones: {", ".join(z["regiones"])}</p>')
    A('<div class="dos">')
    A(f'<div><h4>Demanda</h4><div class="celda">{z["demanda"]}</div></div>')
    A(f'<div><h4>Canal</h4><div class="celda">{z["canal"]}</div></div>')
    A('</div>')
    A(f'<p style="margin-top:11px"><b>Por qué esta zona:</b> {z["por_que"]}</p></div>')

# ---- Hallazgos ----
A('<h2>5 · Hallazgos (MEDIDO vs INFERIDO)</h2>')
A('<table><thead><tr><th>Hallazgo</th><th>Tipo</th><th>Fuente</th></tr></thead><tbody>')
for h in D['hallazgos']:
    et = 'm' if 'MEDIDO' in h['tipo'] else 'i'
    A(f'<tr><td>{h["hallazgo"]}</td><td><span class="et {et}">{h["tipo"]}</span></td><td class="sub2">{h.get("fuente","")}</td></tr>')
A('</tbody></table>')

A('<div class="ok"><b>Recomendación de foco (año 1):</b> atacar <b>Z1 Santiago</b> (canal + sede de decisión) y <b>Z2 Norte minero</b> (mayor demanda de proceso) como las dos zonas ancla, con <b>Z3 Valparaíso-Quintero</b> como tercera por ser la única donde demanda y canal coinciden fuera de Santiago. <b>Z4 Biobío</b> entra si se consigue un socio regional para celulosa/acero/refinería.</div>')

A('<footer><p><b>Fuentes:</b> InfoTécnica CEN (api-infotecnica.coordinador.cl) · RETC/MMA (datosretc.mma.gob.cl) · SEIA (seia.sea.gob.cl) · Aduanas de Chile, registro DIN 2025 (4.847.036 líneas).</p>')
A('<p>Generado por CONECTA — catálogo comercial SUPCON. Datos crudos en <span class="mono">datos/mapa_oportunidades_chile.json</span>. Cada cifra lleva su fuente; MEDIDO = dato directo, INFERIDO = interpretación del cruce.</p></footer>')
A('</div></body></html>')

out = os.path.join(BASE, 'artefactos/mapa_oportunidades.html')
open(out, 'w').write('\n'.join(html))
print('OK ->', out, len('\n'.join(html)), 'bytes')
