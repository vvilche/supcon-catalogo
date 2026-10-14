#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/campana_process.html — LA CAMPAÑA Y CÓMO USARLA CON LO CONSTRUIDO.

Estructura:
  1. Qué es el archivo (las 5 hojas, con sus números reales)
  2. El diagnóstico: qué tiene y qué le falta
  3. El cruce: qué aporta cada pieza a la otra
  4. LAS 3 JUGADAS (el plan de uso)
  5. La tabla: las 75 plantas con decisores, teléfono y siguiente paso
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "campana_process.html")

camp = json.load(open(os.path.join(D, "campana_process.json"), encoding="utf-8"))
cr = json.load(open(os.path.join(D, "cruce_campana.json"), encoding="utf-8"))
F, T = cr["filas"], cr["totales"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


# --- diagnóstico
targets, proyectos, actividades, fuentes = (camp["targets"], camp["proyectos"],
                                            camp["actividades"], camp["fuentes"])
lin_marc = camp["totales"]["lineas_marcadas"]
con_dec = [f for f in F if f["decisores"]]
sin_dec = [f for f in F if not f["decisores"]]
con_proy = [f for f in F if f["n_proyectos"]]

# industrias del target
ind = collections.Counter(f["industria"] for f in F if f["industria"])

# --- tabla de plantas
def fila_tabla(f):
    d0 = f["decisores_detalle"][0] if f["decisores_detalle"] else {}
    dec_cell = (f'<b>{f["decisores"]}</b><span class="sub">{esc(d0.get("nombre","")[:24])}</span>'
                if f["decisores"] else '<span class="falta">0 — a cubrir</span>')
    tel = (f'<span class="tel">{esc(f["telefono"][:15])}</span>' if f["telefono"]
           else '<span class="gris">—</span>')
    proy = (f'<b>US${n(f["inv_proyectos_usd"]/1e6)}M</b>' if f["inv_proyectos_usd"]
            else '<span class="gris">—</span>')
    sig = esc(f["siguiente_paso"][:44]) if f["siguiente_paso"] else '<span class="gris">sin siguiente paso</span>'
    ext = (f'<span class="ext">{esc(f["contacto_excel"][:22])}</span>' if f["contacto_excel"]
           else '<span class="falta">falta</span>')
    return f'''
    <tr>
      <td><b>{esc(f["planta"])}</b><span class="sub">{esc(f["dueno"])[:34]}</span></td>
      <td class="sub2">{esc(f["industria"])}</td>
      <td>{dec_cell}</td>
      <td>{tel}</td>
      <td>{proy}</td>
      <td class="sub2">{ext}</td>
      <td class="sub2">{sig}</td>
    </tr>'''


filas = "".join(fila_tabla(f) for f in sorted(F, key=lambda x: (-x["decisores"], -x["inv_proyectos_usd"])))

ind_html = "".join(f'<span class="chip">{esc(k)} <b>{v}</b></span>'
                   for k, v in ind.most_common())

# puntos clave de la propia campaña (sección de la hoja Actividades)
puntos = camp.get("puntos_claves", [])
puntos_html = "".join(
    f'<tr><td><b>{esc(p["n"])}</b></td><td>{esc(p["tema"])}</td>'
    f'<td class="sub2">{esc(p["accion_pendiente"]) or "—"}</td>'
    f'<td class="sub2">{esc(p["proxima_accion"])[:56] or "—"}</td>'
    f'<td class="sub2">{esc(p["deadline"][:10]) if p["deadline"] else "sin fecha"}</td></tr>'
    for p in puntos) or '<tr><td colspan="5" class="gris">sin puntos clave cargados</td></tr>'

# top proyectos
proys = "".join(
    f'<tr><td>US$<b>{n(p["inv_usd"]/1e6)}M</b></td><td>{esc(p["proyecto"][:46])}</td>'
    f'<td class="sub2">{esc(p["dueno"][:22])}</td><td class="sub2">{esc(p["estado"][:14])}</td></tr>'
    for p in sorted(proyectos, key=lambda x: -x["inv_usd"])[:12])

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Campaña Process · plan de uso</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:18px;max-width:970px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:18px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:15px 18px;margin-bottom:13px}}
h2{{font-size:19px;font-weight:660;margin:26px 0 11px;letter-spacing:-.2px}}
h3{{font-size:14px;font-weight:660;margin:13px 0 7px}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:12px 16px;margin:14px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
.aviso.vd{{background:#f0fdf4;border-color:#bbf7d0;border-left-color:#047857}}
.aviso.vd b{{color:#065f46}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 8px;border-bottom:2px solid var(--bd)}}
td{{padding:7px 8px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.sub2{{font-size:12.5px;color:#4b5563}}
.tel{{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--vd)}}
.falta{{color:var(--am);font-weight:600;font-size:12.5px}}
.ext{{font-size:12px;color:#92400e;background:#fffbeb;border-radius:4px;padding:1px 6px}}
.gris{{color:var(--mu);font-style:italic}}
.chip{{display:inline-block;font-size:12px;background:#f3f4f6;color:#374151;border-radius:5px;padding:3px 9px;margin:0 4px 4px 0}}
.chip b{{color:#1d4ed8}}
.jugada{{background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--ac);border-radius:10px;padding:13px 17px;margin-bottom:11px}}
.jugada b.t{{color:var(--ac)}}
ul{{margin:7px 0 7px 19px}} li{{margin-bottom:5px}}
footer{{margin-top:28px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Campaña de Detección Process: análisis y plan de uso</h1>
<p class="sub0">El archivo <code>Campaña de Detección Process.xlsx</code> es el CRM de la campaña
para detectar oportunidades de la línea <b>Process</b>. Acá está qué contiene, qué le falta, y
<b>cómo se combina con el trabajo de prospección</b> ya hecho.</p>

<div class="kpis">
  <div><b>{len(targets)}</b>plantas target</div>
  <div><b>{len(proyectos)}</b>proyectos (US${n(sum(p['inv_usd'] for p in proyectos)/1e9,1)} mil M)</div>
  <div><b>{len(actividades)}</b>actividades</div>
  <div><b>{len(fuentes)}</b>fuentes</div>
  <div><b>{T['con_decisores']}</b>plantas ya con decisores</div>
</div>

<h2>1. Qué contiene el archivo (las 5 hojas)</h2>
<div class="card">
  <table><thead><tr><th>Hoja</th><th>Qué trae</th><th>Estado real</th></tr></thead><tbody>
    <tr><td><b>Plan</b></td><td>La estructura: Planta | Industria | Ubicación | Prioridad</td>
        <td class="sub2">solo el encabezado (es la plantilla)</td></tr>
    <tr><td><b>Targets</b></td><td>{len(targets)} plantas, con dueño, industria y 6 columnas de
        línea (BI, SYS, FDS, Válvulas, Analítica, Scada) para marcar lo detectado</td>
        <td class="falta">{T['con_contacto']} con contacto · {T['con_siguiente']} con siguiente paso
        · {lin_marc} marcas de línea de {len(targets)*6}</td></tr>
    <tr><td><b>Proyectos</b></td><td>{len(proyectos)} proyectos con inversión, estado (Aprobado/EIA),
        EPCM y <b>link a la fuente</b></td>
        <td class="sub2">completa y con fuente</td></tr>
    <tr><td><b>Actividades</b></td><td>Siguiente acción por cliente con responsable + una sección de
        <b>Puntos Claves</b> con deadlines (visitas KL, lanzamiento de marca, proceso de ventas)</td>
        <td class="sub2">parcial</td></tr>
    <tr><td><b>Fuentes</b></td><td>{len(fuentes)} URLs de seguimiento (LinkedIn, Coordinador,
        ReporteMinero, MCH, SEIA…)</td><td class="sub2">lista de trabajo</td></tr>
  </tbody></table>
</div>

<div class="aviso">
  <b>El diagnóstico, derecho:</b> el archivo tiene <b>el QUÉ</b> — las {len(targets)} plantas
  objetivo, {len(proyectos)} proyectos con su inversión y las fuentes — pero está <b>a medio
  hacer</b>: de {len(targets)} plantas hay <b>{T['con_contacto']} con contacto</b> y
  <b>{T['con_siguiente']} con siguiente paso</b>. Las seis columnas de línea están
  <b>casi vacías ({lin_marc} marcas)</b>: la detección no se hizo.
  <br><br>
  El trabajo de prospección tiene <b>el QUIÉN</b>: 2.691 decisores con cargo, LinkedIn y teléfono.
  Pero no sabía qué planta era target de esta campaña. <b>Cada uno cubre el hueco del otro.</b>
</div>

<h2>2. El cruce: qué se encontró</h2>
<div class="card">
  <ul>
    <li><b>{T['con_decisores']} de {len(F)} plantas ya tienen decisores mapeados</b> —
    y hay <b>{T['decisores_disponibles']} decisores disponibles</b> para las que el Excel dejó sin
    contacto.</li>
    <li><b>{T['sin_decisores']} plantas sin ningún decisor</b>: son en su mayoría
    <b>generación</b> (ENEL GP, Statkraft, parques eólicos, GAS SUR), que es justo el rubro que el
    barrido cubrió menos.</li>
    <li><b>{T['con_proyecto']} plantas tienen proyecto en carpeta</b> con su monto: ahí el Excel y
    los decisores ya convergen.</li>
    <li><b>{T['con_telefono']} con teléfono</b> de central (el cruce con el RETC lo aportó).</li>
  </ul>
  <h3>Industrias del target</h3>
  {ind_html}
</div>

<h2>3. Las 3 jugadas del uso combinado</h2>

<div class="jugada">
  <b class="t">JUGADA 1 — Llenar el contacto que falta (lo más rápido)</b>
  <p class="sub2">El Excel tiene <b>{T['con_contacto']}</b> contactos para {len(targets)} plantas.
  El buscador tiene decisores con cargo y LinkedIn para <b>{T['con_decisores']}</b> de esas plantas
  — <b>{T['decisores_disponibles']} personas</b>. Es pegar una columna en la otra.</p>
  <ul>
    <li><b>Minera Las Cenizas</b> (Explotación Mina Aguilucho, US$12,5M, Aprobado): 31 decisores
    mapeados — <i>Cristian Argandoña León, Gerente General</i>.</li>
    <li><b>Minera San Gerónimo</b>: 25 decisores — <i>Patricio Rendic Lazo, Director Ejecutivo</i>.</li>
    <li><b>Los Bronces / El Soldado / Fundición Chagres</b> (Anglo American): 21 decisores cada
    una, con teléfono de central.</li>
    <li><b>Minera Valle Central</b>: 18 — <i>Christian Cáceres Meneses</i>.</li>
  </ul>
</div>

<div class="jugada">
  <b class="t">JUGADA 2 — Priorizar por la plata del proyecto, no por la lista</b>
  <p class="sub2">El Excel tiene la inversión de cada proyecto. Eso permite ordenar el ataque por
  tamaño real y no por orden de carga. Los 12 mayores:</p>
  <table><thead><tr><th>Inversión</th><th>Proyecto</th><th>Dueño</th><th>Estado</th></tr></thead>
  <tbody>{proys}</tbody></table>
  <p class="sub2" style="margin-top:9px">Ojo con dos lecturas: <b>Aprobado</b> = listo para
  especificar; <b>EIA / En Calificación</b> = todavía se puede entrar en las bases técnicas
  (que es donde conviene influir).</p>
</div>

<div class="jugada">
  <b class="t">JUGADA 3 — Cerrar el hueco de generación</b>
  <p class="sub2">{T['sin_decisores']} plantas del target no tienen ningún decisor mapeado, y el
  patrón es claro: <b>generación</b> (ENEL GP, Statkeeper, parques eólicos, PUCLARO, GAS SUR,
  LIPIGAS). El barrido anterior se concentró en minería y acuicultura.</p>
  <ul>
    <li>Acción concreta: correr el buscador sobre esas {T['sin_decisores']} plantas con la capa
    LinkedIn — el mismo motor que rindió 89% en las mineras.</li>
    <li>Y usar las <b>{len(fuentes)} fuentes</b> que el propio Excel lista para encontrar los
    dueños de los parques que están sin dueño en la planilla.</li>
  </ul>
</div>

<h2>4. Las 75 plantas del target, con lo que ya se sabe de cada una</h2>
<div class="card">
  <table><thead><tr>
    <th>Planta / Dueño</th><th>Industria</th><th>Decisores mapeados</th><th>Teléfono</th>
    <th>Proyecto</th><th>Contacto en Excel</th><th>Siguiente paso</th>
  </tr></thead><tbody>{filas}</tbody></table>
  <p class="sub" style="margin-top:10px">Columna <b>Decisores mapeados</b>: los que ya existen en
  el buscador (nombre del primero y total). <b>Contacto en Excel</b>: lo que la campaña ya tenía
  cargado — naranjo = falta. <b>Proyecto</b>: inversión sumada de los proyectos del dueño.</p>
</div>

<h2>5. Qué hacer esta semana (ordenado)</h2>
<div class="card">
  <h3>Los 3 puntos clave de la propia campaña (con su deadline)</h3>
  <table><thead><tr><th>#</th><th>Tema</th><th>Acción pendiente</th><th>Próxima acción</th><th>Deadline</th></tr></thead>
  <tbody>{puntos_html}</tbody></table>
  <p class="sub" style="margin-top:9px">El único con deadline cargado es el <b>1</b>: coordinar la
  visita de ENAMI antes del <b>25-11-2025</b>. Los puntos 2 y 3 (lanzamiento de la marca y
  conceptos del proceso de ventas) están sin fecha.</p>

  <h3 style="margin-top:16px">El orden que propongo, cruzado con lo que ya existe</h3>
  <ul>
    <li><b>1.</b> Cargar en el Excel los decisores de las {T['con_decisores']} plantas que ya los
    tienen — <b>{T['decisores_disponibles']} contactos nuevos</b>, de un pegado.</li>
    <li><b>2.</b> Arrancar por las 3 con siguiente paso ya escrito: <b>ENAMI</b> (presentación
    presencial en Paipote, con deadline 25-11), <b>Dominga</b> (buscar contactos) y <b>CMPC
    Talagante</b> (visita del 19 de octubre). Las tres tienen decisores disponibles y teléfono.</li>
    <li><b>3.</b> Correr el buscador sobre las {T['sin_decisores']} plantas de generación — es el
    hueco más grande del target (ENEL GP, Statkraft, parques eólicos, GAS SUR, LIPIGAS).</li>
    <li><b>4.</b> Marcar las columnas de línea (BI/SYS/FDS/Válvulas/Analítica/Scada) con lo que el
    <a href="cliente_producto_persona.html">cruce de producto</a> ya resolvió por dolor medido.</li>
  </ul>
</div>

<footer>
  Fuentes: <code>Campaña de Detección Process.xlsx</code> (5 hojas) ·
  <a href="plan_accion_geo.html">plan de acción por región</a> ·
  <a href="cliente_producto_persona.html">empresa→producto→persona</a> ·
  <a href="buscador_decisores.html">buscador de decisores</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(targets)} targets | {len(proyectos)} proyectos | {T['con_decisores']} con decisores")
