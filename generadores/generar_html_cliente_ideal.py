#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/cliente_ideal_linea.html — CLIENTE IDEAL POR LÍNEA DE NEGOCIO.

Al derecho: para cada cosa que vendemos, quién es el cliente ideal, con qué señal se califica
y cuántos hay. Un solo documento, las 7 líneas.

Lee datos/cliente_ideal_linea.json.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "cliente_ideal_linea.html")

d = json.load(open(os.path.join(D, "cliente_ideal_linea.json"), encoding="utf-8"))
L = d["lineas"]

COLOR = {"Analítica": "#b91c1c", "Instrumentación": "#7c3aed", "Válvulas": "#047857",
         "DCS": "#0891b2", "SIS": "#c2410c", "PLC": "#4b5563",
         "Software y plataforma": "#1d4ed8"}
ORDEN = ["DCS", "SIS", "Analítica", "Software y plataforma", "Válvulas",
         "Instrumentación", "PLC"]


def e(s):
    return html.escape(str(s if s is not None else ""))


def n(v):
    try:
        return f"{int(v):,}"
    except Exception:
        return "—"


# ---- resumen comparativo ----
filas = ""
for lin in ORDEN:
    if lin not in L:
        continue
    v = L[lin]
    cl = v["clientes"]
    tam = collections.Counter(c["tamano"] or "sin dato" for c in cl)
    emp = sorted(c["empleados"] for c in cl if c["empleados"])
    med = emp[len(emp) // 2] if emp else None
    col = COLOR.get(lin, "#475569")
    filas += f'''
    <tr data-l="{e(lin).lower()}">
      <td><span class="dot" style="background:{col}"></span><b>{e(lin)}</b></td>
      <td class="num"><b>{n(v['n_clientes'])}</b></td>
      <td class="num">{n(med) if med else '—'}</td>
      <td class="ct">{e(v['compra'])}</td>
      <td><span class="tk">{e(v['ticket'])}</span></td>
    </tr>'''

# ---- fichas por linea ----
fichas = ""
for lin in ORDEN:
    if lin not in L:
        continue
    v = L[lin]
    cl = sorted(v["clientes"], key=lambda x: -(x.get("prioridad") or 0))
    col = COLOR.get(lin, "#475569")
    tam = collections.Counter(c["tamano"] or "sin dato" for c in cl)
    emp = sorted(c["empleados"] for c in cl if c["empleados"])
    chips_tam = "".join(
        f'<span class="chip">{e(k)} <b>{n(cnt)}</b></span>' for k, cnt in tam.most_common())
    stat_emp = (f'mediana {n(emp[len(emp)//2])} empleados · min {n(emp[0])} · max {n(emp[-1])}'
                if emp else "sin dotación verificada")

    filas_cl = ""
    for c in cl[:25]:
        filas_cl += f'''
        <tr>
          <td class="emp"><b>{e(c['empresa'])}</b><span class="sub">{e(c['rubro'] or '')}</span></td>
          <td class="num">{n(c['empleados']) if c['empleados'] else '—'}</td>
          <td>{e(c['tamano'] or '—')}</td>
          <td class="ct">{e(c['motivo'])}</td>
        </tr>'''
    mas = len(cl) - 25 if len(cl) > 25 else 0

    fichas += f'''
    <section class="linea" id="L-{e(lin).replace(' ','_')}" data-l="{e(lin).lower()}">
      <div class="lh">
        <span class="dot big" style="background:{col}"></span>
        <h2>{e(lin)}</h2>
        <span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{n(v['n_clientes'])} clientes</span>
        <span class="tk big">{e(v['ticket'])}</span>
      </div>
      <div class="grid">
        <div class="blk"><span class="lab">QUÉ VENDE</span>{e(v['vende'])}</div>
        <div class="blk"><span class="lab">QUIÉN LO COMPRA</span><b>{e(v['compra'])}</b></div>
        <div class="blk"><span class="lab">SEÑAL QUE LO ACTIVA</span>{e(v['senal'])}</div>
      </div>
      <div class="tams"><span class="lab">TAMAÑO DE LOS CLIENTES</span>{chips_tam}
        <div class="stemp">{e(stat_emp)}</div>
      </div>
      <table class="cli"><thead><tr>
        <th>Empresa</th><th class="num">Empleados</th><th>Tamaño</th><th>Por qué califica</th>
      </tr></thead><tbody>{filas_cl}</tbody></table>
      {'<div class="mas">…y '+str(mas)+' más en el JSON</div>' if mas else ''}
    </section>'''


HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cliente ideal por línea de negocio</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.62;padding:26px 18px 70px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:920px}}
h2{{font-size:19px;font-weight:660;letter-spacing:-.2px}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd);position:sticky;top:0;background:var(--cd);z-index:2}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:7px;vertical-align:middle}}
.dot.big{{width:11px;height:11px}}
.tk{{font-size:11px;font-weight:700;color:#475569;background:#f1f5f9;border-radius:5px;padding:2px 8px}}
.tk.big{{font-size:11.5px;margin-left:auto}}
.badge{{font-size:11.5px;border-radius:6px;padding:2px 10px;font-weight:700}}
.barra{{display:flex;gap:9px;align-items:center;margin-bottom:12px;flex-wrap:wrap}}
input[type=search]{{flex:1;min-width:230px;padding:9px 13px;border:1px solid var(--bd);border-radius:8px;font-size:14px;font-family:inherit}}
input[type=search]:focus{{outline:none;border-color:var(--ac);box-shadow:0 0 0 3px #1d4ed814}}
.cuenta{{font-size:12.5px;color:var(--mu);white-space:nowrap}}
.linea{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:17px 20px;margin-bottom:15px}}
.lh{{display:flex;align-items:center;gap:11px;margin-bottom:13px;flex-wrap:wrap}}
.grid{{display:grid;grid-template-columns:1fr 1fr 1.4fr;gap:11px;margin-bottom:13px}}
@media(max-width:820px){{.grid{{grid-template-columns:1fr}}}}
.blk{{background:#fbfcfd;border:1px solid #eef1f4;border-radius:9px;padding:10px 13px;font-size:13px}}
.lab{{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin-bottom:4px}}
.tams{{background:#fbfcfd;border:1px solid #eef1f4;border-radius:9px;padding:10px 13px;margin-bottom:14px}}
.chip{{display:inline-block;font-size:11.5px;background:#f3f4f6;color:#374151;border-radius:5px;padding:2px 8px;margin:0 4px 4px 0}}
.chip b{{font-weight:700}}
.stemp{{font-size:11.5px;color:var(--mu);margin-top:5px}}
table.cli{{font-size:13px}}
.emp b{{font-size:13px}} .sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.ct{{font-size:12.5px;color:#374151;max-width:420px}}
.mas{{font-size:12px;color:var(--mu);margin-top:8px;font-style:italic}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:5px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Cliente ideal, por cada cosa que vendemos</h1>
<p class="sub0">Al derecho: en vez de partir del dolor y buscar a quién venderle, acá está cada
línea de negocio con <b>la señal que la activa</b>, <b>quién la compra</b>, y <b>cuántos
clientes reales</b> hay contados en el universo de 3.157 empresas. Todo con señal dura: norma
aplicable, registro RETC, dato del Coordinador y dotación verificada con fuente.</p>

<div class="aviso">
  <b>Se calificó solo con señales duras, y eso bajó los números a propósito.</b> La primera
  versión calificaba por rubro y por el campo "tier", y daba Instrumentación en 3.136 de 3.157
  empresas (99%) y PLC en 93%: un cliente ideal que es el universo entero no sirve. Los dos
  campos estaban mal — <b>el rubro mezcla planta con punto de venta</b> ("Combustibles" tiene
  343 empresas, e incluye estaciones de servicio como Abastible o Lipigas) y <b>el tier es una
  heurística que falla</b> (Minera Escondida aparece MEDIANA, Teck Quebrada Blanca PEQUEÑA, CCU
  MEDIANA). Se reemplazó por la <b>dotación de las fichas, con cita</b>.
</div>

<h2>El cuadro comparativo</h2>
<div class="card">
  <table><thead><tr>
    <th>Línea de negocio</th><th class="num">Clientes</th><th class="num">Dotación mediana</th>
    <th>Quién lo compra</th><th>Ticket</th>
  </tr></thead><tbody>{filas}</tbody></table>
</div>

<h2>Una ficha por línea</h2>
<div class="card">
  <div class="barra">
    <input type="search" id="q" placeholder="Filtrar líneas o empresas…">
    <span class="cuenta" id="c"></span>
  </div>
</div>
{fichas}

<h2>Cómo se califica, y qué no dice</h2>
<div class="card">
  <ul>
    <li><b>La señal tiene que ser dura:</b> norma aplicable declarada (DS 13/2011 para CEMS,
    NTSyCS y Ley 21.305 para el coordinado, DS 132 para seguridad minera), registro RETC con
    masa declarada, o dato de completitud/calidad del Coordinador. El rubro no califica.</li>
    <li><b>Solo cuenta el contaminante con masa mayor que cero.</b> El DS 90 obliga a reportar
    todos los parámetros de su tabla: declarar cadmio no significa nada si está en cero.</li>
    <li><b>El tamaño sale de la dotación de la ficha, con cita.</b> Es dato de la empresa
    ("aproximadamente 9.600 empleados", "más de 19.000 trabajadores"), no una inferencia. Pero
    <b>solo 199 fichas lo traen</b>: en el resto el tamaño aparece como "sin dato", y eso es lo
    que es.</li>
    <li><b>No dice que estas empresas vayan a comprar.</b> Dice que tienen la obligación o el
    dolor que el producto resuelve, medido en un registro oficial, y que hay un perfil que
    compra ese tipo de producto. La disposición a comprar no se mide con datos públicos.</li>
    <li><b>El dolor del Coordinador es la señal más limpia del catálogo</b> —dato oficial del
    CEN, 115 empresas con incumplimiento medido— y por eso es la que más conviene usar para
    SCADA y plataforma.</li>
  </ul>
</div>

<footer>
  Fuentes: RETC del MMA (RILES 2024, residuos peligrosos 2025) · API InfoTécnica del Coordinador
  Eléctrico (completitud y calidad) · fichas de las 3.157 empresas con dotación citada ·
  líneas y productos de <code>escalera_exito_v3</code>.
  <br>Ver también <a href="matriz_dolor_perfil.html">matriz dolor·línea·perfil</a> ·
  <a href="dolor_ambiental.html">dolor ambiental</a> ·
  <a href="escalera_exito.html">escalera de productos</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div>
<script>
const inp = document.getElementById('q');
const cuenta = document.getElementById('c');
function filtrar() {{
  const v = inp.value.toLowerCase().trim();
  let vis = 0;
  document.querySelectorAll('.linea').forEach(s => {{
    const hay = (s.dataset.l || '') + ' ' + s.textContent.toLowerCase();
    const ok = !v || hay.includes(v);
    s.hidden = !ok;
    if (ok) vis++;
  }});
  cuenta.textContent = vis + ' de ' + document.querySelectorAll('.linea').length + ' líneas visibles';
}}
inp.addEventListener('input', filtrar);
filtrar();
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  líneas: {len([l for l in ORDEN if l in L])}")
