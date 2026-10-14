#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/inventario_universo.html:
  1. cuántas empresas hay y POR INDUSTRIA (el inventario)
  2. el FORMATO del Excel de la campaña, para replicarlo
"""
import json, os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "inventario_universo.html")

inv = json.load(open(os.path.join(D, "inventario_universo.json"), encoding="utf-8"))
fmt = json.load(open(os.path.join(D, "formato_campana.json"), encoding="utf-8"))
cmp_ = json.load(open(os.path.join(D, "campana_process.json"), encoding="utf-8"))


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v):
    try:
        return f"{v:,}"
    except Exception:
        return "—"


cap = inv["capas"]
ind = inv["por_industria"]
maxe = max(x["empresas"] for x in ind)
maxd = max([x["con_decisores"] for x in ind] + [1])

filas_ind = "".join(f'''
  <tr>
    <td><b>{esc(x['industria'])}</b></td>
    <td class="num">{n(x['empresas'])}</td>
    <td class="bar"><span style="width:{x['empresas']/maxe*100:.0f}%"></span></td>
    <td class="num">{n(x['con_decisores'])}</td>
    <td class="bar b2"><span style="width:{x['con_decisores']/maxd*100:.0f}%"></span></td>
    <td class="num cob">{x['con_decisores']/x['empresas']*100:.0f}%</td>
  </tr>''' for x in ind)

tot_e = sum(x["empresas"] for x in ind)
tot_d = sum(x["con_decisores"] for x in ind)

# --- capas
capas_orden = [
    ("A", "Universo RETC — el padrón completo", cap["universo_retc"],
     "todas las empresas industriales con declaración ambiental (rubro + dolor)"),
    ("B", "Con dolor medido", cap["con_dolor"],
     "las que tienen carga peligrosa o RILES: el argumento de venta"),
    ("C", "Mineras del RETC", cap["mineras_retc"],
     "las que el cruce por intersección había perdido (161 operadores + 59 proveedores)"),
    ("D", "Plan de acción", cap["plan_accion"],
     "con personas mapeadas, línea a ofrecer y guion de llamada"),
    ("E", "Buscador de decisores", cap["buscador_decisores"],
     "barridas en 3 fuentes (Direcmin, Transparencia, LinkedIn) — con nombre y cargo"),
    ("F", "Campaña Process", cap["campana_process"],
     "el target que el propio cliente puso por escrito"),
]
capas_html = "".join(f'''
  <div class="capa">
    <span class="lt">{c[0]}</span>
    <div class="cb"><b>{esc(c[1])}</b><span class="cd">{esc(c[3])}</span></div>
    <span class="cn">{n(c[2])}</span>
  </div>''' for c in capas_orden)

# --- formato del excel
def tabla_hoja(h):
    filas = ""
    for e in h["encabezados"]:
        vp = e.get("valores_posibles") or []
        lista = ("<span class='lista'>" + " · ".join(esc(v) for v in vp[:6]) + "</span>") if vp else ""
        tipo = {"texto": "texto", "numero": "número", "fecha": "fecha"}.get(e.get("tipo"), "texto")
        filas += (f'<tr><td class="lt2">{esc(e["letra"])}</td>'
                  f'<td><b>{esc(e["titulo"])}</b></td>'
                  f'<td class="tipo">{tipo}</td>'
                  f'<td>{lista}'
                  + (f'<span class="ej">ej: {esc(", ".join(e.get("ejemplos", [])[:3]))}</span>' if not vp and e.get("ejemplos") else "")
                  + '</td></tr>')
    return f'''
    <div class="hoja">
      <div class="hh"><b>{esc(h["hoja"])}</b>
        <span class="hd">{n(h["filas"])} filas × {h["columnas"]} columnas
        {f'· encabezado en fila {h["fila_encabezado"]}' if h.get("fila_encabezado") else '· SIN encabezado (hoja de datos sueltos)'}</span>
      </div>
      {f'<table class="tf"><thead><tr><th></th><th>Columna</th><th>Tipo</th><th>Valores esperados</th></tr></thead><tbody>{filas}</tbody></table>' if filas else '<p class="vacia">Hoja sin estructura de tabla. Contiene las URLs de seguimiento en la columna B.</p>'}
    </div>'''


hojas_html = "".join(tabla_hoja(h) for h in fmt["hojas"])

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Inventario del universo y formato de la campaña</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:960px}}
h2{{font-size:19px;font-weight:660;margin:28px 0 11px;letter-spacing:-.2px}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 19px;margin-bottom:13px}}
.capa{{display:flex;align-items:center;gap:13px;background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 15px;margin-bottom:7px}}
.lt{{width:26px;height:26px;flex:0 0 26px;border-radius:7px;background:#eff6ff;color:var(--ac);font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}}
.cb b{{font-size:14px;display:block}}
.cd{{font-size:12px;color:var(--mu)}}
.cn{{margin-left:auto;font-size:20px;font-weight:700;font-variant-numeric:tabular-nums}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px;border-bottom:2px solid var(--bd)}}
td{{padding:7px 8px;border-bottom:1px solid #f3f4f6;vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}}
.cob{{color:var(--vd)}}
.bar{{width:120px;padding:0 10px}}
.bar span{{display:block;height:8px;border-radius:4px;background:#3b82f6}}
.bar.b2 span{{background:#10b981}}
.hoja{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:14px 17px;margin-bottom:12px}}
.hh{{margin-bottom:9px;padding-bottom:8px;border-bottom:1px solid #f3f4f6}}
.hh b{{font-size:15px}}
.hd{{display:block;font-size:12px;color:var(--mu);margin-top:2px}}
table.tf{{font-size:12.5px}}
.lt2{{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--mu);width:26px}}
.tipo{{font-size:11px;color:var(--mu);width:56px;text-transform:uppercase;letter-spacing:.3px}}
.lista{{display:inline-block;font-size:11.5px;background:#f0fdf4;color:#065f46;border:1px solid #bbf7d0;border-radius:5px;padding:1px 7px}}
.ej{{display:block;font-size:11.5px;color:var(--mu);margin-top:2px}}
.vacia{{font-size:12.5px;color:var(--mu);font-style:italic}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:12px 16px;margin:14px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
.aviso.vd{{background:#f0fdf4;border-color:#bbf7d0;border-left-color:#047857}}
.aviso.vd b{{color:#065f46}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
footer{{margin-top:28px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Inventario del universo y formato de la campaña</h1>
<p class="sub0"><b>Cuántas empresas hay, por industria</b> — y el <b>formato exacto del Excel</b> de
la campaña Process, con las columnas, los tipos de dato y las listas de valores válidos, para
replicarlo.</p>

<h2>1. Cuántas empresas hay (las 6 capas)</h2>
<p class="sub0" style="margin-bottom:11px">No son el mismo conjunto: cada capa es un universo
distinto y más trabajado que el anterior. Empezar por la correcta evita rehacer.</p>
{capas_html}

<h2>2. Por tipo de industria</h2>
<div class="card">
  <table><thead><tr>
    <th>Industria</th><th class="num">Empresas</th><th></th>
    <th class="num">Con decisores</th><th></th><th class="num">Cobertura</th>
  </tr></thead><tbody>{filas_ind}
  <tr style="border-top:2px solid var(--bd)">
    <td><b>TOTAL</b></td><td class="num"><b>{n(tot_e)}</b></td><td></td>
    <td class="num"><b>{n(tot_d)}</b></td><td></td><td class="num cob"><b>{tot_d/tot_e*100:.0f}%</b></td>
  </tr></tbody></table>
  <p class="sub0" style="margin:11px 0 0;font-size:12.5px">
  <b>Empresas</b>: el padrón del RETC. <b>Con decisores</b>: cuántas tienen al menos una persona
  con nombre y cargo mapeada. La última columna es lo que falta trabajar.</p>
</div>

<div class="aviso">
  <b>Leer la tabla, no el total:</b> la cobertura de decisores está concentrada. <b>Extracción de
  minerales</b> va 103/174 (59%) y <b>pesca</b> 79/193 (41%) porque son los rubros que se barrieron.
  <b>Manufactura</b> (690 empresas) tiene solo 27 y <b>agropecuario</b> (592) apenas 30: son el
  padrón grande sin trabajar. Un "10% de cobertura" agregado esconde que hay rubros al 0% y otros al 59%.
</div>

<h2>3. Por tamaño (tier)</h2>
<div class="card">
  <table><thead><tr><th>Tier</th><th class="num">Empresas</th><th>Qué significa</th></tr></thead><tbody>
  <tr><td><b>GRANDE</b></td><td class="num">{n(inv['por_tier'].get('GRANDE',0))}</td>
      <td>las que mueven el negocio: priorizar siempre</td></tr>
  <tr><td><b>MEDIANA</b></td><td class="num">{n(inv['por_tier'].get('MEDIANA',0))}</td>
      <td>segunda ola, con dolor medido</td></tr>
  <tr><td><b>PEQUEÑA</b></td><td class="num">{n(inv['por_tier'].get('PEQUEÑA',0))}</td>
      <td>volumen; se atacan por industria, no una por una</td></tr>
  </tbody></table>
</div>

<h2>4. Formato del Excel, para replicarlo</h2>
<p class="sub0" style="margin-bottom:11px">Cada hoja con sus columnas reales, el tipo de dato y los
<b>valores válidos observados</b> (las celdas verdes son listas: sirven para armar validación de
datos en el Excel nuevo).</p>
{hojas_html}

<div class="aviso vd">
  <b>Reglas del formato que importan al replicar:</b>
  <ul style="margin:7px 0 0 19px">
    <li><b>Los encabezados no arrancan en la fila 1.</b> <code>Targets</code> los tiene en la fila 3
    y <code>Actividades</code> en la 2. Si se replica en la fila 1, todas las fórmulas y referencias
    cambian.</li>
    <li><b>Las columnas de línea (BI/SYS/FDS/Válvulas/Analítica/Scada) aceptan variantes.</b> En el
    original conviven <code>Si</code>, <code>Sí</code>, <code>x</code> y <code>No</code> — vale la
    pena fijarlas a una sola (<code>SI/NO</code>) y validar la celda.</li>
    <li><b>Dos columnas se llaman "Area"</b> en <code>Proyectos</code> (H y L): una es el rubro y la
    otra la línea de negocio (Process/Power). Renombrarlas al replicar.</li>
    <li><b><code>Quien</code></b> en <code>Actividades</code> trae iniciales de personas
    (CAO, FTM, EQR): necesita una leyenda de a quién corresponde cada una.</li>
  </ul>
</div>

<footer>
  Fuente: <code>Campaña de Detección Process.xlsx</code> (formato) ·
  <code>universo_prospeccion_supcon.json</code> (3.157 empresas del RETC, rubro + tier) ·
  <a href="campana_process.html">la campaña y su plan</a> ·
  <a href="plan_accion_geo.html">plan de acción por región</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(ind)} industrias | {len(fmt['hojas'])} hojas | {len(capas_orden)} capas")
