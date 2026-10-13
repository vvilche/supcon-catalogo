#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/ecrm_supcon.html — eCRM 2023-2025 de INECO cruzado con las líneas SUPCON.

Qué muestra: las 681 oportunidades reales del eCRM (cliente, contacto, línea, monto, resultado)
traducidas a producto SUPCON, con la cobertura medida sobre el total y los clientes cruzados
contra el catálogo de hoy.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "ecrm_supcon.html")

s = json.load(open(os.path.join(D, "ecrm_supcon.json"), encoding="utf-8"))
e = json.load(open(os.path.join(D, "ecrm_extraido.json"), encoding="utf-8"))
opp = e["oportunidades"]
BU, SUP, CR, CT = s["bu_descifradas"], s["supcon_cubre"], s["clientes_hoy"], s["contactos"]
T = s["totales"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


# --- BU ---
filas_bu = ""
for bu, x in sorted(s["por_bu"].items(), key=lambda y: -y[1]["usd"]):
    sup = SUP.get(bu, {"linea": "—", "nota": ""})
    fuera = sup["linea"] == "—"
    col = "#6b7280" if fuera else "#047857"
    filas_bu += f'''
    <tr>
      <td><b>{esc(bu)}</b><span class="sub">{esc(BU.get(bu, '?')[:64])}</span></td>
      <td class="num">{n(x['oportunidades'])}</td>
      <td class="num"><b>{n(x['usd'])}</b></td>
      <td><span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{esc(sup['linea'])}</span>
          <span class="sub">{esc(sup['nota'])}</span></td>
    </tr>'''

# --- clientes del eCRM x hoy ---
filas_cr = ""
for c, x in sorted(CR.items(), key=lambda y: -y[1]["usd_cotizado"]):
    tox = x.get("carga_toxica")
    pob = x["personas"]
    col = "#047857" if pob else ("#b45309" if tox else "#9ca3af")
    est = ("MAPEADO" if pob else ("SOLO DOLOR" if tox else "HUECO"))
    tx = f"{tox:,.1f}" if tox is not None else "—"
    filas_cr += f'''
    <tr>
      <td><b>{esc(c)}</b><span class="sub">{esc(x.get('empresa_hoy') or '—')}</span></td>
      <td class="num">{n(x['cotizaciones'])}</td>
      <td class="num"><b>{n(x['usd_cotizado'])}</b></td>
      <td class="num">{n(x['oc'])}</td>
      <td class="num">{n(x['usd_oc'])}</td>
      <td class="num">{n(pob) if pob else '—'}</td>
      <td class="num">{tx}</td>
      <td><span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{est}</span></td>
    </tr>'''

# --- contactos ---
filas_ct = ""
for c, x in sorted(CT.items(), key=lambda y: -y[1]["cotizaciones"]):
    filas_ct += (f'<tr><td><b>{esc(c)}</b></td><td class="num">{n(x["cotizaciones"])}</td>'
                 f'<td class="num">{n(x["usd"])}</td></tr>')

# --- estados / embudo ---
EMB = {
    "con OC (ganada)": "Ganada (llegó orden de compra)",
    "cotizada": "Cotización enviada al cliente",
    "en proceso ecrm": "En proceso interno (creada en ecrm)",
    "sin estado": "Sin estado registrado",
    "adjudicada": "Adjudicada",
    "otro": "Otro detalle",
}


def etapa(x):
    t = (x.get("estado_ecrm") or x.get("estado") or "").lower()
    if not t.strip():
        return "sin estado"
    if "oc " in t or t.startswith("oc") or "orden de compra" in t:
        return "con OC (ganada)"
    if "adjudicad" in t:
        return "adjudicada"
    if "perdid" in t or "no adjudicad" in t:
        return "otro"
    if "cotizacion" in t or "cotización" in t:
        return "cotizada"
    if "ecrm" in t:
        return "en proceso ecrm"
    return "otro"


emb = collections.Counter(etapa(x) for x in opp)
tot_opp = sum(emb.values())
filas_emb = ""
for k, v in emb.most_common():
    pct = v / tot_opp * 100
    filas_emb += f'''
    <div class="bar"><span class="lb">{esc(EMB.get(k, k))}</span>
      <div class="tr"><div class="fl" style="width:{pct:.1f}%"></div></div>
      <span class="vl">{v}</span></div>'''

# --- por año ---
filas_anio = ""
for a in ["2023", "2024", "2025"]:
    sub = [x for x in opp if x["anio"] == a]
    oc = [x for x in sub if (x.get("oc") or "").strip()]
    vu = sum(x.get("valor_num") or 0 for x in oc)
    vt = sum(x.get("valor_num") or 0 for x in sub)
    filas_anio += f'''
    <tr><td><b>{a}</b></td><td class="num">{n(len(sub))}</td>
      <td class="num">{n(vt)}</td><td class="num">{n(len(oc))}</td>
      <td class="num"><b>{n(vu)}</b></td>
      <td class="num">{len(oc)/len(sub)*100:.0f}%</td></tr>'''

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>eCRM 2023-2025 x SUPCON</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1220px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:960px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid var(--ac);border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#1e40af}}
.aviso.am{{background:#fffbeb;border-color:#fde68a;border-left-color:var(--am)}}
.aviso.am b{{color:#92400e}}
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
.sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.badge{{font-size:11px;border-radius:5px;padding:2px 8px;font-weight:700;white-space:nowrap}}
.bar{{display:flex;align-items:center;gap:10px;margin-bottom:7px;font-size:13px}}
.lb{{width:250px;flex-shrink:0;color:#374151}}
.tr{{flex:1;height:9px;background:#f1f5f9;border-radius:5px;overflow:hidden}}
.fl{{height:100%;background:linear-gradient(90deg,#1d4ed8,#60a5fa);border-radius:5px}}
.vl{{width:46px;text-align:right;font-variant-numeric:tabular-nums;color:var(--mu);font-size:12px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:860px){{.grid2{{grid-template-columns:1fr}}}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>El eCRM de INECO: 3 años de cotizaciones reales, cruzados con SUPCON</h1>
<p class="sub0">El registro de <b>todas las cotizaciones de INECO entre 2023 y 2025</b> —cliente,
contacto, línea de negocio (BU), monto y en qué quedó cada una—. No es estrategia: es la
operación. Dice <b>dónde está la plata y a quién volver</b> con producto SUPCON.</p>

<div class="kpis">
  <div><b>{n(T['oportunidades'])}</b>oportunidades reales</div>
  <div><b>US${n(T['valor_cotizado_usd']/1e6,1)}M</b>cotizado 2023-2025</div>
  <div><b>US${n(T['valor_cubierto_supcon_usd']/1e6,1)}M</b>cubierto por línea SUPCON ({T['pct_cubierto']:.0f}%)</div>
  <div><b>{n(len(CR))}</b>clientes activos</div>
  <div><b>{n(len(CT))}</b>contactos con nombre</div>
</div>

<div class="aviso vd">
  <b>El hallazgo principal:</b> el <b>{T['pct_cubierto']:.0f}% de lo que INECO cotizaba es línea
  SUPCON</b> — US${n(T['valor_cubierto_supcon_usd'])} de US${n(T['valor_total'] if 'valor_total' in T else T['valor_cotizado_usd'])}.
  Las dos líneas más grandes (válvulas de aislamiento y válvulas de control, US$11,2M juntas) son
  exactamente <b>SUPCON Valves</b>. No hay que inventar un mercado: hay que volver a los mismos
  clientes con el catálogo que sí se puede vender.
</div>

<div class="aviso am">
  <b>Y el hueco más grande:</b> <b>MLP (Minera Los Pelambres)</b> es el cliente #1 del eCRM —
  248 cotizaciones, US$7,8M, 122 órdenes de compra— y en el mapa de personas de hoy tiene solo
  <b>3 personas en 2 áreas</b>. Es la cuenta con más plata probada y menos cobertura comercial.
</div>

<h2>Las líneas del eCRM (BU) y qué SUPCON las cubre</h2>
<div class="card">
  <table><thead><tr>
    <th>Línea (BU)</th><th class="num">Oportunidades</th><th class="num">US$</th>
    <th>Línea SUPCON que la cubre</th>
  </tr></thead><tbody>{filas_bu}</tbody></table>
  <p class="sub" style="margin-top:10px">Los montos de BU compuestas ("FCS/ISV/RMD") se reparten
  entre sus partes para no contarlos dos veces. <b>RQ</b> (bombas y equipos rotativos) es la única
  línea que queda fuera del catálogo SUPCON: US$2,63M.</p>
</div>

<h2>Clientes del eCRM, y su cobertura hoy</h2>
<div class="card">
  <table><thead><tr>
    <th>Cliente</th><th class="num">Cotiz.</th><th class="num">US$ cotizado</th>
    <th class="num">OC</th><th class="num">US$ ganado</th><th class="num">Personas hoy</th>
    <th class="num">Tóxicas t</th><th>Cobertura</th>
  </tr></thead><tbody>{filas_cr}</tbody></table>
  <p class="sub" style="margin-top:10px"><b>HUECO</b> = cotiza fuerte pero no tiene ninguna
  persona mapeada hoy. Son las cuentas donde el trabajo de "buscar personas a cargo" rinde más.</p>
</div>

<div class="grid2">
  <div class="card">
    <h3>En qué quedó cada cotización (las 681)</h3>
    {filas_emb}
    <p class="sub" style="margin-top:10px">La tasa de conversión real es <b>32%</b>
    (218 ganadas / 681). Ojo: "sin estado" (70) son cotizaciones cuyo resultado no se registró,
    no necesariamente perdidas.</p>
  </div>
  <div class="card">
    <h3>Por año</h3>
    <table><thead><tr><th>Año</th><th class="num">Oport.</th><th class="num">US$ cotizado</th>
    <th class="num">OC</th><th class="num">US$ ganado</th><th class="num">Conv.</th></tr></thead>
    <tbody>{filas_anio}</tbody></table>
    <h3 style="margin-top:16px">Contactos con nombre (los que piden)</h3>
    <table><thead><tr><th>Persona</th><th class="num">Cotiz.</th><th class="num">US$</th></tr></thead>
    <tbody>{filas_ct}</tbody></table>
  </div>
</div>

<h2>Qué aporta al trabajo de hoy</h2>
<div class="card">
  <ul>
    <li><b>Clientes con plata PROBADA, no potencial.</b> MLP US$7,8M, Andina US$3,9M, Candelaria
    US$2,5M, Salvador US$1,3M, Enami US$1,3M, Caserones US$1,0M. Estas cuentas ya compraban
    válvulas e instrumentación de forma recurrente.</li>
    <li><b>Los contactos reales, con nombre y apellido.</b> German Díaz (32 cotizaciones),
    Leonid Carrizo (29), Manuel Rojas (20, US$940K), Patricia Adriazola (18), Javiera Reyes (17).
    Son las personas que piden, no cargos genéricos: el "contacto" del eCRM es un activo directo.</li>
    <li><b>Las líneas a atacar están claras:</b> ISV + FCS (válvulas) = US$11,2M de US$20,8M.
    SUPCON Valves y el posicionador CVP2000 entran ahí directo.</li>
    <li><b>Los contratos marco y licitaciones por folio</b> (Codelco 7000209560, MLP 4642000997,
    Candelaria PR 10327072, Salvador 7000313999) son relaciones de suministro continuo: el
    vehículo de entrada ya existe.</li>
    <li><b>Aviso de ciclo:</b> 2025 tiene 194 oportunidades contra 241 de 2023 (−19%), pero el
    valor cotizado sube (US$7,5M vs US$6,6M): menos cotizaciones, más grandes. Es el patrón de
    mercado que conviene confirmar con el usuario.</li>
  </ul>
</div>

<h2>Fuente, y qué no dice</h2>
<div class="card">
  <ul>
    <li><b>Fuente:</b> <code>Archivo de ecrm .xlsx</code>, hojas 2023 (241), 2024 (246) y 2025
    (194). Convertido a <code>datos/ecrm_oportunidades.csv</code> y
    <code>datos/ecrm_extraido.json</code>.</li>
    <li><b>Se eliminaron las filas de totales</b> ("Total USD", "Cantidad de Negocios") que venían
    mezcladas en la hoja: sin eso, el conteo y el valor salían inflados (686 y US$24,0M contra
    681 y US$20,8M reales).</li>
    <li><b>152 oportunidades no traen valor</b> (22%): el monto total está subestimado en esa
    proporción.</li>
    <li><b>Las siglas BU se descifraron por evidencia</b> (las descripciones reales de cada
    línea, no por suposición): FCS = Fisher Control Solutions, ISV = Isolation Valves,
    RMD = Rosemount Measurement, RFD = Flow Devices, RAI = Analytical, PRV = Pressure Relief
    Valves. La cobertura SUPCON es un mapeo comercial, no una equivalencia técnica validada
    producto por producto.</li>
    <li><b>Esto es INECO, no CONECTA.</b> Son ventas de Emerson hechas por INECO. Que el producto
    sea reemplazable por SUPCON no significa que el cliente acepte el cambio: eso se valida
    técnicamente caso a caso.</li>
  </ul>
</div>

<footer>
  Fuente: <code>Archivo de ecrm .xlsx</code> (2023-2025) ·
  <a href="historia_ineco.html">historia comercial INECO</a> ·
  <a href="plan2009_valvulas.html">plan 2009 válvulas</a> ·
  <a href="personas_por_area.html">personas por área</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(s['por_bu'])} líneas BU | {len(CR)} clientes | {len(CT)} contactos")
