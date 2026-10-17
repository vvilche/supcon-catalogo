#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/itl_rfp.html — la postulación correcta a la RFP del ITL (cierre 30-nov-2026).

CORRECCIÓN DEL ENTREGABLE ANTERIOR: se había analizado el RFI (cerró el 31-jul-2026). La etapa
vigente es la RFP, abierta el 30-sep-2026 y con cierre el 30-nov-2026. Bases distintas.

La jugada: E2 (energías remotas) con PUCV — que YA GANÓ ese desafío en el RFI — y el usuario final
son los OBSERVATORIOS ASTRONÓMICOS del norte.
"""
import os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "artefactos", "itl_rfp.html")


def esc(x):
    return html.escape(str(x if x is not None else ""))


# ---------------------------------------------------------------- datos duros RFP
DUROS = [
    ("Etapa vigente", "RFP (Request for Proposal)", "ADJUDICA dinero. La anterior (RFI) era exploratoria y ya cerró"),
    ("Apertura", "30 de septiembre 2026", ""),
    ("Cierre", "30 de noviembre 2026, 23:59 h", "Quedan ~6 semanas desde el 17-oct"),
    ("Duración máxima", "48 meses corridos", "desde la firma del contrato de coinversión"),
    ("Requisito duro", "Identificar al menos 4 INCERTIDUMBRES relevantes", "Anexo 5. Sin eso, inadmisible"),
    ("Requisito duro", "Carta de interés o compromiso industrial", "identificando rol y aportes comprometidos"),
]

# ---------------------------------------------------------------- la tabla que define todo
COINV = [
    ("Con Socios ITL (PUCV)", "máximo 60%", "mínimo 40%", "de esa contrapartida, al menos 60% debe ser PECUNIARIA", True),
    ("Sin socios ITL", "máximo 40%", "mínimo 60%", "de esa contrapartida, al menos 60% debe ser PECUNIARIA", False),
]

# ---------------------------------------------------------------- E2 y los observatorios
PORQUE = [
    ("E2 nombra la astronomía",
     "La ficha de E2 lista entre las industrias a las que afecta: 'Minería de menor escala, agroindustria, "
     "pesca, turismo, ASTRONOMÍA, logística, entre otros'. No hay que justificar el encaje: está escrito."),
    ("La PUCV ya ganó E2 en el RFI",
     "No se arranca de cero. El desafío ya tiene un proponente que pasó la etapa anterior y sabe cómo se "
     "arma. Entrar como socio técnico es la vía más corta."),
    ("El caso de negocio existe y es medible",
     "Paranal consume ~1.200 kW y los observatorios están a ~150 km de la red. ESO viene migrando de "
     "generación propia a renovables + conexión: La Silla ya tiene planta solar. Es un cliente con el "
     "problema real y con la disposición a resolverlo."),
    ("Pide exactamente lo que CONECTA hace",
     "E2 pide 'algoritmos y sistemas inteligentes para la gestión de la energía' como contribución de "
     "capacidades al ITL. Eso es la capa de datos + analítica + control, que es el negocio."),
]

# ---------------------------------------------------------------- arquitectura propuesta
CAPAS = [
    ("1. Medición", "Instrumentación y medidores de calidad de energía en los puntos de suministro: consumo por telescopio, por planta de generación, por sistema de respaldo.",
     "Da la línea base que E2 exige para demostrar reducción de fósiles."),
    ("2. Adquisición y red", "Adquisición del dato desde los sistemas que YA existen (SCADA, generación, medidores) y red OT segmentada con ciberseguridad.",
     "El observatorio no reemplaza su sistema: se le agrega la capa de lectura."),
    ("3. Capa de datos (UNS)", "Un árbol de datos con histórico de generación, consumo y estado de activos. Base de todo cálculo posterior.",
     "Habilita el 'sistema de gestión de la energía' que pide E2."),
    ("4. Gestión inteligente", "Algoritmos de despacho y predicción: cuánta renovable, cuánto respaldo, cuándo. Optimización del costo nivelado.",
     "Es la contribución de capacidades que el ITL quiere para sí."),
    ("5. Decisión", "Tablero operativo con el estado energético del sitio y alertas. El operador decide con dato en línea.",
     "Cierra la brecha entre captura y acción que el ITL declara como problema."),
]

# ---------------------------------------------------------------- incertidumbres (4 obligatorias)
INCERT = [
    ("Técnica", "¿Se puede mantener la calidad de energía que exige un telescopio (estabilidad, armónicos) con una matriz de renovable + respaldo mayor que la actual?",
     "Riesgo para el instrumento astronómico."),
    ("De integración", "¿Los sistemas de generación, respaldo y consumo existentes exponen datos suficientes y con la calidad necesaria para construir el modelo de gestión?",
     "Riesgo de que la base de datos no exista."),
    ("De operación", "¿Un despacho optimizado automáticamente es aceptable para la operación del observatorio, que prioriza la continuidad del instrumento sobre el costo?",
     "Riesgo de rechazo operativo."),
    ("Económica", "¿El ahorro de combustible y la reducción de costo nivelado superan la inversión en sensorización y automatización dentro del horizonte del proyecto?",
     "Riesgo de caso de negocio."),
]

# ---------------------------------------------------------------- qué falta
FALTA = [
    ("Confirmar el estado de la PUCV en la RFP",
     "¿Presentan propuesta a E2 en esta etapa? Si sí, CONECTA entra como entidad asociada; si no, se "
     "postula como proponente con la PUCV de asociada. Las dos rutas dan el 60% de aporte ITL."),
    ("La carta de interés del observatorio",
     "E2 y las bases la exigen ('identificando rol y aportes comprometidos'). Sin observatorio, hay que "
     "conseguirla de un operador antes del 30-nov. Es el anexo que no se puede simular."),
    ("El detalle de la propuesta que ganó la PUCV",
     "Para no duplicar lo que ellos ya comprometieron y presentar CONECTA como la capa que les falta, "
     "no como un proyecto paralelo."),
    ("La valorización de la PI como contrapartida",
     "La PI preexistente entra como aporte valorizado y 'podrá requerir valorización independiente'. "
     "Hay que tener la memoria de cálculo del método."),
]

filas_duros = "".join(
    f'<div class="dd"><b>{esc(k)}</b><span class="v">{esc(v)}</span><span class="n">{esc(nn)}</span></div>'
    for k, v, nn in DUROS)

filas_coinv = "".join(f'''
  <tr class="{'si' if c[4] else 'no'}">
    <td><b>{esc(c[0])}</b></td>
    <td class="num">{esc(c[1])}</td>
    <td class="num">{esc(c[2])}</td>
    <td class="sub2">{esc(c[3])}</td>
  </tr>''' for c in COINV)

porque = "".join(f'<div class="of"><b>{esc(p[0])}</b><p>{esc(p[1])}</p></div>' for p in PORQUE)
capas = "".join(
    f'<div class="capa"><span class="cn">{esc(c[0])}</span><div class="cb"><p>{esc(c[1])}</p>'
    f'<span class="cd">{esc(c[2])}</span></div></div>' for c in CAPAS)
incert = "".join(
    f'<div class="inc"><span class="it">{esc(i[0])}</span><p>{esc(i[1])}</p>'
    f'<span class="ir">Riesgo: {esc(i[2])}</span></div>' for i in INCERT)
falta = "".join(f'<div class="falt"><b>{esc(f[0])}</b><p>{esc(f[1])}</p></div>' for f in FALTA)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ITL RFP 2026: E2 con la PUCV y los observatorios</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309;--ro:#b91c1c}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1120px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:4px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:18px;max-width:960px}}
h2{{font-size:19px;font-weight:660;margin:30px 0 11px}}
h3{{font-size:16px;font-weight:660;margin-bottom:6px}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 19px;margin-bottom:13px}}
.corr{{background:#fef2f2;border:1px solid #fecaca;border-left:4px solid var(--ro);border-radius:10px;padding:13px 17px;margin-bottom:16px;font-size:13.5px;color:#7f1d1d}}
.corr b{{color:var(--ro)}}
.datos{{display:grid;grid-template-columns:repeat(auto-fill,minmax(225px,1fr));gap:9px;margin-bottom:15px}}
.dd{{background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--ac);border-radius:10px;padding:10px 14px}}
.dd b{{font-size:10.5px;color:var(--mu);text-transform:uppercase;letter-spacing:.4px;display:block}}
.dd .v{{font-size:15px;font-weight:700;display:block;margin:2px 0}}
.dd .n{{font-size:11.5px;color:var(--mu)}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:9px;border-bottom:2px solid var(--bd)}}
td{{padding:10px 9px;border-bottom:1px solid #f3f4f6}}
tr.si{{background:#f0fdf4}}
tr.no{{opacity:.6}}
.num{{font-weight:700;font-variant-numeric:tabular-nums}}
.sub2{{font-size:12.5px;color:#4b5563}}
.ofs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:9px}}
.of{{background:#f9fafb;border-radius:9px;padding:11px 14px}}
.of b{{font-size:13px;color:#065f46}}
.of p{{font-size:12.5px;color:#374151;margin-top:3px}}
.capa{{display:flex;gap:13px;align-items:flex-start;background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--vd);border-radius:10px;padding:11px 16px;margin-bottom:7px}}
.cn{{font-size:12.5px;font-weight:700;color:var(--vd);min-width:118px}}
.cb p{{font-size:13px}}
.cd{{font-size:11.5px;color:var(--mu);display:block;margin-top:3px}}
.inc{{background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--am);border-radius:10px;padding:11px 16px;margin-bottom:8px}}
.it{{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--am)}}
.inc p{{font-size:13px;margin-top:3px}}
.ir{{font-size:11.5px;color:var(--mu);display:block;margin-top:3px}}
.falt{{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:11px 16px;margin-bottom:8px}}
.falt b{{font-size:13.5px;color:#92400e}}
.falt p{{font-size:12.5px;color:#78350f;margin-top:3px}}
footer{{margin-top:28px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>ITL RFP 2026 — E2 con la PUCV y los observatorios</h1>
<p class="sub0">La etapa que <b>sí adjudica</b>. Desafío <b>E2: suministro energético sostenible para
industrias aisladas</b>, con la PUCV (que ya ganó E2 en el RFI) y los <b>observatorios astronómicos</b>
del norte como usuario final.</p>

<div class="corr">
  <b>Corrección del análisis anterior:</b> se había leído el <b>RFI</b>, que cerró el 31-jul-2026
  (hace dos meses). La etapa vigente es la <b>RFP</b>, abierta el 30-sep-2026 y con cierre el
  <b>30-nov-2026</b>. Las bases son otras y esta etapa <b>sí reparte plata</b>.
</div>

<h2>1. Los datos duros de la RFP</h2>
<div class="datos">{filas_duros}</div>

<h2>2. La ventaja de entrar con la PUCV (está en las bases)</h2>
<div class="card">
  <h3>Punto 4.5 de las bases: "Derechos especiales de los Socios ITL"</h3>
  <p class="sub2" style="margin:6px 0 12px"><i>"En igualdad de evaluación, el ITL priorizará los
  proyectos que contemplen la participación de sus socios en el desarrollo o validación de las
  soluciones tecnológicas."</i></p>
  <table><thead><tr><th>Modalidad</th><th>Aporte ITL</th><th>Contrapartida</th><th>Condición</th></tr></thead>
  <tbody>{filas_coinv}</tbody></table>
  <div class="corr" style="margin:13px 0 0;background:#f0fdf4;border-color:#bbf7d0;border-left-color:var(--vd);color:#065f46">
    <b>Veinte puntos de diferencia.</b> Postular con un socio ITL sube el aporte máximo del 40% al 60%,
    y baja la contrapartida exigida del 60% al 40%. Es la diferencia entre poner 60 o 40 pesos por
    cada 100 del proyecto.
  </div>
</div>

<h2>3. Por qué E2 con observatorios</h2>
<div class="ofs">{porque}</div>

<h2>4. Lo que se propone construir</h2>
<div class="card">
  {capas}
  <p class="sub2" style="margin-top:11px">La misma arquitectura de A3/A4/M1, aplicada al activo
  energético. Cambia el dominio, no la plataforma: es la prueba de que el método es propio y
  transferible — que es lo que el ITL compra.</p>
</div>

<h2>5. Las 4 incertidumbres (requisito de admisibilidad)</h2>
<p class="sub0" style="margin-bottom:10px">Las bases excluyen las propuestas que <b>no identifiquen al
menos cuatro incertidumbres relevantes</b> (Anexo 5). Estas cuatro son reales y atacan el proyecto,
no lo decoran.</p>
{incert}

<h2>6. Lo que falta resolver (y bloquea)</h2>
{falta}

<footer>
  Fuente: <a href="https://itlchile.com/desafios/">itlchile.com/desafios</a> · Bases RFP 2026 (sept)
  · ficha E2 · ESO (consumo y suministro de Paranal/La Silla).<br>
  Cierre: <b>30 de noviembre 2026, 23:59</b>. Referencia: el RFI recibió <b>64 iniciativas</b> de 5
  países por <b>US$104,4M</b>; agua fue la cartera más disputada (25).
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
