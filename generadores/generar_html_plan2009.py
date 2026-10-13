#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/plan2009_valvulas.html — PLAN 2009 DE VÁLVULAS cruzado con hoy.

Qué muestra: el plan de válvulas de control (Fisher) de INECO para 2009 — clientes por
segmento con sus plantas, proyectos con monto y probabilidad, competencia específica de
válvulas y resultados por planta — cruzado con el mercado de válvulas de hoy y las personas
mapeadas.
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "plan2009_valvulas.html")

p = json.load(open(os.path.join(D, "plan2009_valvulas.json"), encoding="utf-8"))
SEG, COMP, CR = p["segmentos"], p["competencia_valvulas"], p["cruces_hoy"]
PV, PP, PR = p["proyectos_valvulas_2009"], p["proyectos_power_2009"], p["proyectos_refineria_2009"]
PL = p["resultados_por_planta_2008"]
AN = p["analisis_del_documento"]


def e(s):
    return html.escape(str(s if s is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


# --- segmentos con su cruce ---
seg_html = ""
for nombre, s in SEG.items():
    cli = "".join(f'<span class="chip">{e(c)}</span>' for c in s["clientes"])
    seg_html += f'''
    <div class="seg">
      <div class="segh"><b>{e(nombre)}</b><span class="meta">{e(s['meta_2009'])}</span></div>
      <div class="chips">{cli}</div>
      <div class="crec">{e(s['crecimiento'])}</div>
    </div>'''

# --- competencia ---
comp_html = ""
for k, v in COMP.items():
    comp_html += f'''
    <div class="cmp"><b>{e(k)}</b><p>{e(v)}</p></div>'''

# --- proyectos válvulas (con monto × prob = estimado) ---
filas_pv = ""
tot_est = 0
for x in PV:
    est = x["monto_k"] * x["prob"] / 100
    tot_est += est
    filas_pv += f'''
    <tr><td>{e(x['proyecto'])}</td><td class="num">{n(x['monto_k'])}</td>
        <td class="num">{x['prob']}%</td><td class="num">{n(est)}</td></tr>'''
filas_pv += f'''
    <tr class="tot"><td><b>Total</b></td><td class="num"><b>1.800</b></td>
        <td class="num">—</td><td class="num"><b>{n(tot_est)}</b></td></tr>'''

# --- resultados por planta ---
filas_pl = ""
for x in PL:
    filas_pl += f'''
    <tr><td><b>{e(x['planta'])}</b><span class="sub">{e(x['grupo'])}</span></td>
        <td class="num">{n(x['venta_total_k'],1)}</td>
        <td class="num">{n(x['valvulas_k'],1)}</td>
        <td class="num">{n(x['margen_vv_k'],1)}</td>
        <td class="num">{n(x['repuestos_k'],1)}</td>
        <td class="num">{n(x['margen_rep_k'],1)}</td></tr>'''

# --- cruce hoy ---
filas_cr = ""
for nombre, c in sorted(CR.items(), key=lambda x: -(x[1]["personas"] or 0)):
    tox = c.get("carga_toxica")
    col = "#047857" if (tox is not None and tox > 100) else ("#b45309" if c["personas"] else "#9ca3af")
    est = ("CON DOLOR ALTO" if (tox is not None and tox > 100)
           else "EN EL MAPA" if c["personas"] else "SIN REGISTRO HOY")
    filas_cr += f'''
    <tr><td class="emp"><b>{e(nombre)}</b><span class="sub">{e(c.get('empresa_hoy') or '')}</span></td>
      <td class="num">{n(c['areas']) if c['areas'] else '—'}</td>
      <td class="num">{n(c['personas']) if c['personas'] else '—'}</td>
      <td class="num"><b>{n(tox,1) if tox is not None else '—'}</b></td>
      <td><span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{est}</span></td>
    </tr>'''

con_personas = sum(1 for c in CR.values() if c["personas"])
con_dolor = sum(1 for c in CR.values() if (c.get("carga_toxica") or 0) > 100)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Plan 2009 válvulas (Fisher) x hoy</title><style>
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
.aviso.am{{background:#fffbeb;border-color:#fde68a;border-left-color:var(--am)}}
.aviso.am b{{color:#92400e}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:14px 0 8px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
tr.tot td{{background:#fbfdff;border-top:2px solid var(--bd)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.emp b{{font-size:13.5px}} .sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.badge{{font-size:10.5px;border-radius:5px;padding:2px 8px;font-weight:700;white-space:nowrap}}
.seg{{border:1px solid var(--bd);border-radius:10px;padding:12px 15px;margin-bottom:9px;background:var(--cd)}}
.segh{{display:flex;align-items:baseline;gap:12px;margin-bottom:7px;flex-wrap:wrap}}
.segh b{{font-size:14.5px}}
.meta{{font-size:12px;color:var(--ac);font-weight:600;margin-left:auto}}
.chips{{margin-bottom:5px}}
.chip{{display:inline-block;font-size:12px;background:#f3f4f6;color:#374151;border-radius:5px;padding:2px 9px;margin:0 4px 4px 0}}
.crec{{font-size:12px;color:var(--mu)}}
.cmp{{border-left:3px solid #b91c1c;background:#fbfcfd;border-radius:8px;padding:10px 13px;margin-bottom:8px}}
.cmp b{{font-size:13.5px;color:#991b1b}} .cmp p{{font-size:12.5px;color:#374151;margin-top:3px}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:820px){{.grid2{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">

<h1>Plan 2009 de válvulas de control, cruzado con el mercado de hoy</h1>
<p class="sub0">El plan anual de la línea de <b>válvulas de control (Fisher)</b> de INECO,
noviembre 2008. Es el documento más accionable de la serie INECO para un producto puntual:
clientes por segmento con sus plantas, proyectos con monto y probabilidad, competencia
específica de válvulas, y resultados por planta. CONECTA vende válvulas de control SUPCON: el
comprador y el argumento son los mismos.</p>

<div class="kpis">
  <div><b>6</b>segmentos con meta</div>
  <div><b>5</b>competidores con su debilidad</div>
  <div><b>10</b>plantas con resultado 2008</div>
  <div><b>{con_personas}</b>clientes con personas hoy</div>
</div>

<div class="aviso">
  <b>El argumento que vale hoy, textual del documento:</b> "el desarrollo a futuro debiera estar
  dirigido a <b>manejo de diagnósticos y nuevas tecnologías</b>, este es un mercado poco
  explotado y del que debiéramos ser pioneros, pero el crecimiento adicional se debe producir en
  el <b>área de servicios, que reportará márgenes distintos</b>". Eso es exactamente lo que
  CONECTA vende hoy con diagnóstico de válvulas y posicionador inteligente (CVP2000).
</div>

<div class="aviso am">
  <b>Ojo con comparar mercados.</b> El documento dice "mercado de válvulas US$10M a US$12M" —
  eso es el mercado de <i>válvulas de control</i> en Chile en 2008. La medición de hoy por
  partida arancelaria da <b>US$454,9M</b>, pero mide <b>todo</b> el universo de válvulas
  (incluye grifería, oleohidráulica, repuestos de vehículos). No son la misma canasta: el
  primero es el segmento de proceso, el segundo es el total importado.
</div>

<h2>Clientes principales por segmento (textual del plan 2009)</h2>
{seg_html}

<h2>Clientes de válvulas: estado hoy</h2>
<div class="card">
  <table><thead><tr>
    <th>Cliente</th><th class="num">Áreas hoy</th><th class="num">Personas hoy</th>
    <th class="num">Carga tóxica t</th><th>Estado</th>
  </tr></thead><tbody>{filas_cr}</tbody></table>
</div>

<h2>Proyectos de válvulas 2009 (monto × probabilidad)</h2>
<div class="card">
  <table><thead><tr>
    <th>Proyecto</th><th class="num">Monto US$K</th><th class="num">Prob. win</th>
    <th class="num">Estimado US$K</th>
  </tr></thead><tbody>{filas_pv}</tbody></table>
  <p class="sub" style="margin-top:10px">La meta de fábrica era MRO US$3.100K + Proyectos
  US$1.800K = US$4.900K. Cierre real 2008 según Emerson: <b>US$5.029K</b> (correo de
  Carlos Rodríguez, 18-nov-2008).</p>
</div>

<h2>Resultados por planta 2008 (el dato más concreto del documento)</h2>
<div class="card">
  <table><thead><tr>
    <th>Planta</th><th class="num">Venta total K</th><th class="num">Válvulas K</th>
    <th class="num">Margen vv K</th><th class="num">Repuestos K</th><th class="num">Margen rep K</th>
  </tr></thead><tbody>{filas_pl}</tbody></table>
  <p class="sub" style="margin-top:10px">CMPC Pacífico es el caso más elocuente: solo US$57,7K en
  válvulas pero <b>US$287,3K en repuestos</b> con 98,8 de margen. El negocio real estaba en el
  repuesto, no en el equipo.</p>
</div>

<div class="grid2">
  <div class="card">
    <h3>Competencia de válvulas, con su debilidad</h3>
    {comp_html}
  </div>
  <div class="card">
    <h3>Proyectos de refinación 2009 (llave en mano)</h3>
    <table><thead><tr><th>Proyecto</th><th class="num">Válvulas K</th><th>EPC</th></tr></thead>
    <tbody>{"".join(f'<tr><td>{e(x["proyecto"])}</td><td class="num">{n(x["inversion_vv_k"])}</td><td class="sub">{e(x["epc"])}</td></tr>' for x in PR)}</tbody></table>
    <h3 style="margin-top:16px">Power: 10 proyectos con inversión (US$M)</h3>
    <table><thead><tr><th>Central</th><th>Empresa</th><th class="num">US$M</th></tr></thead>
    <tbody>{"".join(f'<tr><td>{e(x["proyecto"])}</td><td class="sub">{e(x["empresa"])}</td><td class="num">{n(x["inversion_us_m"])}</td></tr>' for x in PP)}</tbody></table>
    <p class="sub" style="margin-top:8px">El documento concluye que ese mercado no se captura:
    <b>"los proyectos son manejados por empresas internacionales"</b> y solo se manifiesta en
    repuestos.</p>
  </div>
</div>

<h2>Qué aporta al trabajo de hoy</h2>
<div class="card">
  <ul>
    <li><b>Los clientes de válvulas son los mismos de hoy, con sus plantas identificadas:</b>
    Arauco (Arauco y Nueva Aldea), CMPC (Pacífico y Laja), ENAP (Aconcagua, Bio Bio, Magallanes),
    Codelco (Norte y Teniente), Escondida, Anglo (Chagres y Los Bronces), Collahuasi.</li>
    <li><b>El mercado de válvulas es de repuesto, no de equipo.</b> CMPC Pacífico: US$57,7K de
    válvulas contra US$287,3K de repuestos. El plan de 2009 medía además que <b>74% del margen
    venía de operaciones en plaza</b> (2006: 71%, 2007: 80%) — la venta es de servicio local.</li>
    <li><b>La competencia tiene debilidades concretas y accionables:</b> Metso perdiendo su
    departamento de servicios, Dezurik terminando contrato con Escondida, Masoneilan con 2
    vendedores y sin servicios, Samson entrando por precio + entrega en 4-6 semanas.</li>
    <li><b>El argumento de venta ya estaba escrito:</b> el crecimiento estaba en diagnóstico y
    nuevas tecnologías, "mercado poco explotado del que debiéramos ser pioneros". CONECTA lo
    vende hoy como CVP2000 y diagnóstico de válvulas.</li>
    <li><b>La meta por segmento y el desglose por planta</b> es el formato que falta en el
    trabajo actual: metas separadas de MRO y proyecto, por segmento, con cliente y planta.</li>
  </ul>
</div>

<h2>Fuente, y qué no dice</h2>
<div class="card">
  <ul>
    <li><b>Fuente:</b> <code>Plan 2009 vvs.ppt</code> (INECO Ltda, 73 slides, nov-2008). Convertido
    con LibreOffice y extraído con python-pptx; los montos y clientes son textuales del
    documento.</li>
    <li><b>No dice que estos clientes sigan comprando válvulas a la misma marca.</b> Dice quiénes
    eran sus clientes de válvulas en 2009 y qué plantas tenían. La relación comercial se mantiene
    (ver la historia INECO), pero el proveedor pudo cambiar.</li>
    <li><b>Las cifras de mercado no son comparables entre 2008 y hoy:</b> una mide el segmento de
    válvulas de control, la otra todo el universo arancelario de válvulas.</li>
    <li><b>Los proyectos 2009 son históricos.</b> Se listan porque muestran el patrón de cómo se
    dimensionaba una oportunidad (monto × probabilidad de adjudicación), no porque sigan vigentes.</li>
  </ul>
</div>

<footer>
  Fuente: <code>Plan 2009 vvs.ppt</code> (INECO) ·
  <a href="historia_ineco.html">historia comercial INECO</a> ·
  <a href="personas_por_area.html">personas por área</a> ·
  <a href="dolor_ambiental.html">dolor ambiental</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(SEG)} segmentos | {len(COMP)} competidores | {len(PL)} plantas | {con_personas} clientes con personas")
