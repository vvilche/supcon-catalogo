#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CÓMO USARLO — la rutina operativa, con el caso ENAMI resuelto paso a paso.

LA PREGUNTA
------------------------------------------------------------------------------
"Ok pero cómo usamos esto". Todo lo construido es un mapa; falta la rutina. Este script arma el
flujo concreto: qué se hace con cada pieza, en qué orden, y muestra el ciclo COMPLETO resuelto
sobre un caso real (ENAMI → Fundición Hernán Videla Lira, US$1.700M, deadline 25-11).

EL FLUJO (4 pasos, siempre igual)
------------------------------------------------------------------------------
  1. ELEGIR de la campaña    -> planta target con proyecto y monto (hoja Targets/Proyectos)
  2. LLENAR el contacto      -> buscar los decisores de esa planta (buscador multi-fuente)
  3. ELEGIR la línea         -> qué producto según el cargo y el dolor medido (matriz)
  4. CONTACTAR con el guion  -> teléfono de central + nombre + dato real (plan de acción)

Salida: artefactos/como_usarlo.html
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "como_usarlo.html")


def load(p, d=None):
    fp = os.path.join(D, p)
    return json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else d


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


# ALIAS: en el archivo ENAMI figura como "EMPRESA NACIONAL DE MINERIA" (sin "ENAMI"), y el mismo
# problema pasa con Codelco ("CORP NACIONAL DEL COBRE DE CHILE"). Sin alias, buscar el nombre
# comercial devuelve 0 y parece que la empresa no está.
ALIAS = {
    "enami": ["empresa nacional de mineria", "nacional de mineria"],
    "codelco": ["corp nacional del cobre", "nacional del cobre"],
    "mlp": ["minera los pelambres", "pelambres"],
    "cmpc": ["cia minera del pacifico", "cartulinas cmpc", "minera del pacifico"],
    "collahuasi": ["comp a minera do a in s de collahuasi", "collahuasi"],
    "escondida": ["minera escondida"],
    "sqm": ["soc quimica y minera"],
    "enap": ["empresa nacional del petroleo"],
}


def coincide_busqueda(nombre_buscado, empresa_archivo):
    """True si el nombre buscado (o su alias) está contenido en el de la empresa del archivo."""
    nb, ea = norm(nombre_buscado), norm(empresa_archivo)
    if not nb or not ea:
        return False
    if nb in ea or ea in nb:
        return True
    for comercial, formas in ALIAS.items():
        if comercial in nb or nb in [norm(f) for f in formas]:
            if ea in [norm(f) for f in formas] or comercial in ea:
                return True
    return False


def esc(x):
    import html
    return html.escape(str(x if x is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


camp = load("campana_process.json") or {}
cr = load("cruce_campana.json") or {}
buscador = (load("buscador_decisores.json") or {}).get("resultados", [])
plan = (load("plan_accion.json") or {}).get("plan", [])

# ---------------------------------------------------------------- EL CASO ENAMI
# Proyecto de la campaña: Fundición Hernán Videla Lira, US$1.700M, Aprobado, Atacama.
# Deadline del punto clave: coordinar visita antes del 25-11-2025.
enami_bd = None
for x in buscador:
    if "enami" in norm(x["empresa"]) or coincide_busqueda("ENAMI", x["empresa"]):
        enami_bd = x
        break
enami_plan = None
for p in plan:
    if "enami" in norm(p["empresa"]) or coincide_busqueda("ENAMI", p["empresa"]):
        enami_plan = p
        break

# el decisor CLAVE: el gerente de la planta EXACTA del proyecto.
# OJO con el orden: buscar primero el nombre propio de la planta ("fundición Hernán Videla Lira"),
# porque un patrón genérico como /planta/ matchea antes "Gerente de Plantas" (que es corporativo)
# y devuelve el contacto equivocado.
gerente_planta = None
if enami_bd:
    for patron in (r"videla|hern[aá]n videla", r"fundici[oó]n", r"gerente de planta"):
        for h in enami_bd["hallazgos"]:
            if re.search(patron, h["cargo"], re.I):
                gerente_planta = h
                break
        if gerente_planta:
            break

print("=" * 100)
print("CÓMO USARLO — el flujo, resuelto sobre el caso ENAMI")
print("=" * 100)
print(f"\n  PASO 1 — DE LA CAMPAÑA: Fundición Hernán Videla Lira (ENAMI)")
print(f"    proyecto: modernización | US$1.700M | Aprobado | Atacama | línea Process")
print(f"    deadline: coordinar visita antes del 25-11-2025")
print(f"\n  PASO 2 — CONTACTO (buscador): {enami_bd['n_decisores'] if enami_bd else 0} decisores")
if gerente_planta:
    print(f"    ★ EL CLAVE: {gerente_planta['nombre']} — {gerente_planta['cargo']}")
    print(f"      (es el gerente de la MISMA planta del proyecto)")
if enami_bd:
    for h in enami_bd["hallazgos"][:8]:
        print(f"      {'★' if h.get('relevante') else ' '} {h['nombre'][:28]:30s} {h['cargo'][:44]}")
print(f"\n  PASO 3 — LÍNEA: según cargo + dolor")
if enami_plan:
    print(f"    líneas de la empresa: {', '.join(enami_plan.get('lineas_empresa', [])) or '—'}")
    print(f"    teléfono central: {enami_plan.get('telefono_central') or '—'}")
print(f"\n  PASO 4 — GUION:")
print(f'    "Hola, llamo de CONECTA por la modernización de la Fundición Hernán Videla Lira.')
print(f'     Vi que la aprobación ambiental salió y que son US$1.700M. Busco a '
      f'{gerente_planta["nombre"] if gerente_planta else "el gerente de fundición"} para ver '
      f'si les sirve instrumentación y válvulas para el proyecto."')

# ---------------------------------------------------------------- EL FLUJO GENERICO
flujo = [
    {"paso": "1. ELEGIR", "de": "Campaña Process (Excel)",
     "que": "Abrir la pestaña Targets + Proyectos. Elegir la planta por monto del proyecto y estado.",
     "criterio": "Aprobado = listo para especificar · EIA = todavía se entra en las bases técnicas",
     "salida": "Una planta target con su monto y su siguiente paso",
     "herramienta": "campana_process.html"},
    {"paso": "2. LLENAR", "de": "Buscador de decisores",
     "que": "Buscar esa planta/empresa. Devuelve nombre, cargo y LinkedIn de cada decisor.",
     "criterio": "Priorizar el que tenga el cargo de la PLANTA del proyecto (no solo el corporativo)",
     "salida": "Los decisores con nombre y cargo",
     "herramienta": "buscador_decisores.html · y para correrlo: buscador_decisores.py --empresa X"},
    {"paso": "3. ELEGIR LA LÍNEA", "de": "Matriz dolor × producto × perfil",
     "que": "Cruzar el dolor medido (RETC) con la línea que lo resuelve, y verificar que el cargo "
            "del decisor sea comprador de ESA línea.",
     "criterio": "Al jefe de I&C no se le vende analítica: eso lo compra Calidad/Medio Ambiente.",
     "salida": "Qué ofrecerle a cada persona",
     "herramienta": "cliente_producto_persona.html"},
    {"paso": "4. CONTACTAR", "de": "Plan de acción",
     "que": "Llamar al conmutador, pedir por nombre y cargo, y usar el guion con el dato real.",
     "criterio": "El teléfono es de la CENTRAL: hay que pedir a la persona por nombre.",
     "salida": "La reunión",
     "herramienta": "plan_accion_geo.html (por región) · plan_accion.html"},
]

# ---------------------------------------------------------------- LAS 4 REGLAS DE USO
reglas = [
    ("El Excel es la lista; el buscador es el contacto",
     "No buscar los decisores de las 370 empresas del RETC: buscar los de las 75 plantas que la "
     "campaña ya eligió. El Excel manda el QUÉ, el buscador completa el QUIÉN."),
    ("Por el cargo de la PLANTA, no el corporativo",
     "El caso ENAMI lo enseña: hay un <b>Gerente de la Fundición Hernán Videla Lira</b> — el "
     "gerente de la planta exacta del proyecto. Ese vale más que el Vicepresidente Ejecutivo."),
    ("La línea depende del cargo, no del gusto",
     "Al de I&C se le vende instrumentación; al de Medio Ambiente, analítica; al de Abastecimiento, "
     "todo. Llegar con el argumento que el interlocutor no puede decidir quema la reunión."),
    ("Una planta sin contacto es una planta sin vender",
     "Hoy hay 65 de 75 así, casi todas de generación. Correr el buscador sobre ellas es la tarea "
     "con mayor retorno pendiente."),
]

flujo_html = "".join(f'''
  <div class="paso">
    <div class="ph"><span class="pn">{esc(f["paso"])}</span>
      <span class="pd">desde: <b>{esc(f["de"])}</b></span>
      <span class="ph2">{esc(f["herramienta"])}</span></div>
    <p class="pq">{f["que"]}</p>
    <p class="pc"><b>Criterio:</b> {f["criterio"]}</p>
    <p class="ps"><b>Salida:</b> {esc(f["salida"])}</p>
  </div>''' for f in flujo)

reglas_html = "".join(f'<div class="regla"><b>{esc(t)}</b><p>{c}</p></div>' for t, c in reglas)

# decisores de enami para la tabla del ejemplo
enami_rows = ""
if enami_bd:
    for h in enami_bd["hallazgos"][:12]:
        li = (f'<a href="{esc(h["linkedin"])}" target="_blank">in</a>' if h.get("linkedin") else "")
        marca = ('<span class="clave">CLAVE</span>'
                 if gerente_planta and h["nombre"] == gerente_planta["nombre"] else "")
        enami_rows += (f'<tr><td><b>{esc(h["nombre"])}</b> {marca}</td>'
                       f'<td class="sub2">{esc(h["cargo"])}</td><td>{li}</td></tr>')

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cómo usar todo esto</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1080px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:940px}}
h2{{font-size:19px;font-weight:660;margin:28px 0 11px;letter-spacing:-.2px}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 19px;margin-bottom:13px}}
.paso{{background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--ac);border-radius:11px;padding:13px 17px;margin-bottom:10px}}
.ph{{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:5px}}
.pn{{font-size:15px;font-weight:700;color:var(--ac)}}
.pd{{font-size:12.5px;color:var(--mu)}}
.ph2{{font-size:11.5px;color:var(--mu);margin-left:auto;font-family:ui-monospace,Menlo,monospace;background:#f3f4f6;border-radius:5px;padding:1px 7px}}
.pq{{font-size:13.5px;margin-bottom:5px}}
.pc{{font-size:12.5px;color:#4b5563;margin-bottom:3px}}
.ps{{font-size:12.5px;color:var(--vd)}}
.regla{{border-left:3px solid var(--vd);background:#f9fafb;border-radius:8px;padding:9px 14px;margin-bottom:8px}}
.regla b{{font-size:13.5px;color:#065f46}}
.regla p{{font-size:12.5px;color:#374151;margin-top:2px}}
.aviso{{background:#f0fdf4;border:1px solid #bbf7d0;border-left:4px solid var(--vd);border-radius:9px;padding:13px 16px;margin:14px 0;font-size:13.5px}}
.aviso b{{color:#065f46}}
.ejemplo{{background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid var(--ac);border-radius:10px;padding:15px 18px;margin:16px 0}}
.ejemplo h3{{font-size:15px;margin-bottom:8px;color:#1e40af}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:7px 8px;border-bottom:2px solid var(--bd)}}
td{{padding:7px 8px;border-bottom:1px solid #f3f4f6}}
tr:last-child td{{border-bottom:none}}
.sub2{{font-size:12.5px;color:#4b5563}}
.clave{{font-size:10px;background:#047857;color:#fff;border-radius:4px;padding:1px 6px;font-weight:700;margin-left:5px}}
.guion{{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;background:#fffbeb;border-left:3px solid var(--am);border-radius:7px;padding:11px 14px;margin-top:9px;color:#78350f;white-space:pre-wrap}}
a{{color:var(--ac);text-decoration:none;font-size:12.5px}} a:hover{{text-decoration:underline}}
footer{{margin-top:28px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Cómo usar todo esto</h1>
<p class="sub0">El flujo operativo, en 4 pasos, siempre igual. Cada paso dice de qué herramienta sale
y con qué criterio se decide. Abajo está el <b>ciclo completo resuelto sobre un caso real</b>
(ENAMI → Fundición Hernán Videla Lira, US$1.700M, deadline 25-11).</p>

<h2>El flujo: 4 pasos</h2>
{flujo_html}

<h2>Las 4 reglas que hacen que funcione</h2>
<div class="card">{reglas_html}</div>

<h2>El ciclo completo, resuelto: ENAMI</h2>
<div class="ejemplo">
  <h3>Fundición Hernán Videla Lira — modernización, US$1.700M, Aprobado, Atacama</h3>
  <p class="sub2">Es el caso con deadline del propio archivo: <i>"Hacer presentación presencial en
  Paipote, traer a Supcon, falta la respuesta de Viera"</i> — antes del 25-11-2025.</p>

  <h3 style="margin-top:14px">Paso 2 — los decisores (los encontró el buscador)</h3>
  <table><thead><tr><th>Persona</th><th>Cargo</th><th>LinkedIn</th></tr></thead>
  <tbody>{enami_rows or '<tr><td colspan="3" class="sub2">correr el buscador sobre ENAMI</td></tr>'}</tbody></table>

  <h3 style="margin-top:14px">Paso 4 — el guion con el dato real</h3>
  <div class="guion">Hola, llamo de CONECTA por la modernización de la Fundición Hernán Videla Lira.
Vi que la aprobación ambiental salió y que son US$1.700M.
Busco a {esc(gerente_planta["nombre"]) if gerente_planta else "el gerente de fundición"}, \
{esc(gerente_planta["cargo"]) if gerente_planta else ""}, para ver si les sirve instrumentación y \
válvulas de control para el proyecto.</div>
</div>

<div class="aviso">
  <b>Por qué este caso importa:</b> el buscador encontró a <b>Hernán Santander González, Gerente
  de Fundición Hernán Videla Lira</b> — el gerente de <b>la planta exacta del proyecto</b>. No es el
  contacto genérico de ENAMI: es el dueño de esa fundición. Y también a <b>María Cristina Vallejos
  Cox, Gerente de Proyectos</b>, que maneja la modernización. Eso es lo que el Excel no tenía y el
  buscador sí.
</div>

<h2>Qué hacer, en orden, esta semana</h2>
<div class="card">
  <ol style="margin-left:19px">
    <li style="margin-bottom:6px"><b>ENAMI primero</b> — tiene deadline (25-11) y ya tiene los
    decisores con nombre. Llamar a la central y pedir por <b>Hernán Santander</b> (Fundición) y
    <b>María Cristina Vallejos</b> (Proyectos).</li>
    <li style="margin-bottom:6px"><b>Las otras 2 con siguiente paso</b>: Dominga (buscar contactos)
    y CMPC Talagante (visita del 19 de octubre).</li>
    <li style="margin-bottom:6px"><b>Cargar los {cr.get("totales", {}).get("decisores_disponibles", 0)}
    contactos</b> en el Excel: las 10 plantas que ya tienen decisores, de un pegado.</li>
    <li style="margin-bottom:6px"><b>Correr el buscador sobre las 65 plantas sin cobertura</b>
    (generación: ENEL GP, Statkraft, parques eólicos) — es la tarea de mayor retorno pendiente.</li>
    <li><b>Marcar las columnas de línea</b> del Excel con lo que el cruce de producto ya resolvió.</li>
  </ol>
</div>

<footer>
  <a href="campana_process.html">la campaña y su plan</a> ·
  <a href="buscador_decisores.html">buscador de decisores</a> ·
  <a href="cliente_producto_persona.html">empresa→producto→persona</a> ·
  <a href="plan_accion_geo.html">plan de acción por región</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"\nescrito: {OUT} ({len(HTML.encode()):,} bytes)")
