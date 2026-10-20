#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ficha de competencia: BLIIoT / Beilai Technology vs CONECTA.

Fuentes: es.bliiot.com (sitio oficial, leido en navegador real) + marketplaces
(Alibaba / Made-in-China / distribuidores) para precios de calle.

ORDEN DE LOS DATOS: todo precio de BLIIoT viene de marketplace o distribuidor, NO del
fabricante (el fabricante solo da "solicitar presupuesto"). Se declara como tal.
"""
import os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "artefactos", "competencia_bliiot.html")


def esc(x):
    return html.escape(str(x))


EMPRESA = [
    ("Razón social", "Beilai Technology Co., Ltd. (Shenzhen Beilai Tech.)"),
    ("Marca comercial", "BLIIoT"),
    ("Origen", "Shenzhen, China"),
    ("Fundación", "2005"),
    ("I+D", "60+ ingenieros"),
    ("Foco declarado", "Industrial AI + IT + OT — hardware de borde basado en ARM"),
    ("Certificaciones", "ISO 9001, CE, RoHS, FCC, KC (Corea)"),
    ("Membresías", "OPC UA Foundation · EtherCAT · Profinet · AWS Hardware Partner · "
                   "ThingsBoard · Ignition SCADA hardware access provider"),
]

# (categoria, bliiot, supcon/conecta, veredicto)
MATRIZ = [
    ("DCS (control de proceso)", "No tiene", "ECS-700 (SUPCON)", "NO COMPITE"),
    ("SIS (seguridad funcional)", "No tiene", "TCS-500, SIL 4", "NO COMPITE"),
    ("Instrumentación de proceso", "No tiene", "CXT, caudalímetros, radar 80 GHz", "NO COMPITE"),
    ("Válvulas y posicionadores", "No tiene", "SUPCON Fluid, CVP2000", "NO COMPITE"),
    ("Analítica / CEMS", "No tiene", "Analizadores, CEMS 5000", "NO COMPITE"),
    ("APC / optimización", "No tiene", "APC V11.2", "NO COMPITE"),
    ("Plataforma de datos / UNS", "Solo pasarela Node-RED (BL118)", "supOS, Tier0 UNS", "SOLAPE PARCIAL"),
    ("Gateway de protocolos", "BL101/BL102/BL118, Modbus→MQTT, Modbus→IEC 104", "OrionLX+ (NovaTech)", "COMPITE DIRECTO"),
    ("E/S distribuidas / I/O remoto", "BL190/BL191/BL192, M410E/M420E", "Orion I/O (NovaTech)", "COMPITE"),
    ("Edge computing industrial", "ARMxy BL3xx/BL4xx, Jetson EA230/EA250", "Tier0 Edge", "COMPITE PARCIAL"),
    ("PLC de borde (CODESYS)", "EdgePLC BL233/BL234/BL237/BL246", "—", "FUERA DE CATEGORÍA"),
    ("RTU / router 4G", "S272, R40B", "OrionMX (NovaTech)", "COMPITE (bajo)"),
    ("Switches industriales", "Línea propia", "Hirschmann (Belden)", "COMPITE (bajo)"),
    ("Protecciones eléctricas", "No tiene", "Vizimax, relés", "NO COMPITE"),
    ("PMU / sincrofasores", "No tiene", "Vizimax PMU", "NO COMPITE"),
    ("Sincronización GPS", "No tiene", "Kronos (NovaTech)", "NO COMPITE"),
    ("Cumplimiento CEN / SSCC", "No tiene", "ECAP (servicio CONECTA)", "NO COMPITE"),
    ("Ingeniería y puesta en marcha", "No tiene en Chile", "Core del negocio CONECTA", "NO COMPITE"),
]

# (modelo, que es, precio fuente marketplace)
PRECIOS = [
    ("BL102", "Gateway PLC → MQTT / OPC UA", "US$ 47 – 140", "Ethernet o 4G, múltiples protocolos"),
    ("BL118", "Gateway Edge con Node-RED", "US$ 80 – 246", "US$ 100 a 1-99 u.; US$ 80 sobre 100 u."),
    ("BL191", "E/S remota OPC UA, Ethernet + RS485", "US$ 65 – 126", "MOQ 1, AES-256 opcional"),
    ("BL335 / BL370", "Computadora industrial ARM", "No publicado", "18.878 a 58.302 combinaciones de E/S"),
]

# (criterio, bliiot, conecta)
COMPARA = [
    ("Precio del hardware", "Muy bajo (gateway desde ~US$ 50)", "Alto (equipo certificado + ingeniería)"),
    ("Soporte en Chile", "Ninguno. Fábrica en Shenzhen.", "Presencial, en terreno"),
    ("Responsabilidad ante el Coordinador", "Ninguna", "CONECTA firma y responde"),
    ("Certificación para subestación", "IEC genérico, no 61850-3", "Equipos IEC 61850-3 certificados"),
    ("Ciberseguridad", "No declara IEC 62443", "IEC 62443 / Ley 21.663 vía Hirschmann"),
    ("Ingeniería de integración", "El cliente la hace", "La hace CONECTA"),
    ("Garantía y reposición", "Logística desde China", "Stock y RMA local"),
    ("Documentación en español", "No", "Sí"),
    ("Plazo de entrega", "Semanas (importación)", "Días"),
]

RIESGOS = [
    ("Canibaliza tu hardware", "Si ofrecés un gateway BLIIoT a US$ 150 al lado de un OrionLX+ "
     "a US$ 3.000, el cliente pregunta por qué. Y tiene razón en preguntar."),
    ("Te convierte en revendedor", "Distribuir hardware genérico te pone en la fila de los "
     "revendedores, que compiten por precio. CONECTA no está en ese negocio: está en el de "
     "la ingeniería y la responsabilidad."),
    ("Margen real desconocido", "Sin lista de precios de distribuidor no hay forma de saber si "
     "el margen paga la importación, el stock, la garantía y el soporte. Hay que pedirla antes "
     "de decidir."),
    ("Sin respaldo de marca", "Si falla, el cliente te mira a vos. Y vos mirás a Shenzhen."),
    ("Conflicto con SUPCON", "SUPCON tiene su propia capa de borde (supOS, Tier0). Vender el "
     "hardware de un tercero que compite con esa capa puede incomodar la relación."),
]

VEREDICTOS = [
    ("¿Compite con SUPCON?", "No, salvo en gateway y E/S de borde.",
     "No fabrica DCS, SIS, instrumentación, válvulas, analítica, APC ni protecciones. "
     "Es otra categoría de producto: hardware de borde barato, sin ingeniería."),
    ("¿Compite con CONECTA?", "Sí, en la capa de integración.",
     "Si el negocio es vender un gateway para convertir Modbus a MQTT, BLIIoT lo hace por "
     "una décima parte. Ahí sí compite, y fuerte."),
    ("¿Conviene ser distribuidor?", "NO, como negocio principal.",
     "Ver el análisis abajo: el margen no paga el soporte, y desvía a CONECTA de su ventaja real."),
]

filas_emp = "".join(f'<div class="ei"><b>{esc(k)}</b><span>{esc(v)}</span></div>' for k, v in EMPRESA)

filas_mat = "".join(
    f'<tr class="v-{v.split()[0].lower()}"><td>{esc(c)}</td><td class="bl">{esc(b)}</td>'
    f'<td class="sc">{esc(s)}</td><td class="ver">{esc(v)}</td></tr>' for c, b, s, v in MATRIZ)

filas_pre = "".join(
    f'<tr><td><b>{esc(m)}</b></td><td>{esc(q)}</td><td class="num">{esc(p)}</td>'
    f'<td class="obs">{esc(o)}</td></tr>' for m, q, p, o in PRECIOS)

filas_cmp = "".join(
    f'<tr><td>{esc(c)}</td><td class="bl">{esc(b)}</td><td class="sc">{esc(s)}</td></tr>'
    for c, b, s in COMPARA)

riesgos = "".join(f'<div class="rie"><b>{esc(r[0])}</b><p>{esc(r[1])}</p></div>' for r in RIESGOS)

veredictos = "".join(
    f'<div class="ver-card"><b>{esc(v[0])}</b><span class="vc">{esc(v[1])}</span>'
    f'<p>{esc(v[2])}</p></div>' for v in VEREDICTOS)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BLIIoT vs SUPCON vs CONECTA — ficha de competencia</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#0A1628;--blue:#2563EB;--brand:#0A8439;--tx:#0F172A;--tx2:#475569;
--tx3:#94A3B8;--bd:#E2E8F0;--bg:#F8FAFC}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
font-size:14.5px;line-height:1.65;padding:26px 18px 70px}}
.wrap{{max-width:1150px;margin:0 auto}}
h1{{font-size:27px;font-weight:700;letter-spacing:-.6px}}
.sub0{{color:var(--tx2);font-size:14.5px;margin:6px 0 20px;max-width:900px}}
h2{{font-size:19px;font-weight:680;margin:30px 0 12px;padding-bottom:7px;border-bottom:2px solid var(--bd)}}
h3{{font-size:15.5px;font-weight:660;margin-bottom:8px}}
.card{{background:#fff;border:1px solid var(--bd);border-radius:12px;padding:17px 20px;margin-bottom:13px}}
.emp{{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:9px}}
.ei{{background:#fff;border:1px solid var(--bd);border-left:4px solid var(--blue);
border-radius:10px;padding:10px 14px}}
.ei b{{font-size:10.5px;color:var(--tx3);text-transform:uppercase;letter-spacing:.5px;display:block}}
.ei span{{font-size:13.5px;font-weight:600;display:block;margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--tx3);
font-weight:700;padding:9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px;border-bottom:1px solid #F1F5F9;vertical-align:top}}
.bl{{color:#b91c1c;font-size:13px}}
.sc{{color:#065f46;font-size:13px}}
.ver{{font-size:10.5px;font-weight:700;letter-spacing:.4px;white-space:nowrap}}
tr.v-no .ver{{color:#94A3B8}}
tr.v-compite .ver{{color:#b91c1c}}
tr.v-solape .ver{{color:#b45309}}
tr.v-fuera .ver{{color:#7C3AED}}
.num{{font-weight:700;font-variant-numeric:tabular-nums;color:var(--blue);white-space:nowrap}}
.obs{{color:var(--tx2);font-size:12.5px}}
.ver-card{{background:#fff;border:1px solid var(--bd);border-radius:11px;padding:14px 18px;margin-bottom:9px}}
.ver-card b{{display:block;font-size:14.5px;margin-bottom:2px}}
.vc{{display:inline-block;font-size:12px;font-weight:700;color:var(--blue);margin-bottom:5px}}
.ver-card p{{font-size:13.5px;color:var(--tx2)}}
.rie{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid #b45309;
border-radius:10px;padding:12px 16px;margin-bottom:8px}}
.rie b{{font-size:14px;color:#92400e}}
.rie p{{font-size:13px;color:#78350f;margin-top:3px}}
.big{{background:var(--navy);color:#F1F5F9;border-radius:13px;padding:22px 26px;margin:18px 0}}
.big .q{{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#60A5FA;font-weight:700;margin-bottom:8px}}
.big b{{font-size:21px;font-weight:700;display:block;line-height:1.45;color:#fff}}
.big p{{font-size:14px;color:#94A3B8;margin-top:10px;line-height:1.6}}
.nota{{font-size:12.5px;color:#94A3B8;font-style:italic;margin-top:7px}}
.alt{{background:#ecfdf5;border:1px solid #a7f3d0;border-left:4px solid var(--brand);
border-radius:10px;padding:13px 17px;margin-top:10px;font-size:13.5px;color:#065f46}}
.alt b{{color:#047857}}
footer{{margin-top:28px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--tx3)}}
</style></head><body><div class="wrap">

<h1>BLIIoT (Beilai) vs SUPCON vs CONECTA</h1>
<p class="sub0">Ficha de competencia. Fuente primaria: <b>es.bliiot.com</b>, leído en navegador real.
Los precios <b>no los publica el fabricante</b> (todo va a "solicitar presupuesto"): los valores
de abajo salen de marketplaces y distribuidores, y se declaran como tales.</p>

<h2>1. Quién es</h2>
<div class="emp">{filas_emp}</div>

<h2>2. Matriz producto a producto</h2>
<div class="card" style="padding:8px 12px">
<table><thead><tr><th>Categoría</th><th>BLIIoT</th><th>SUPCON / CONECTA</th><th></th></tr></thead>
<tbody>{filas_mat}</tbody></table>
</div>

<h2>3. Precios de calle (marketplace, NO lista del fabricante)</h2>
<div class="card" style="padding:8px 12px">
<table><thead><tr><th>Modelo</th><th>Qué es</th><th>Precio</th><th>Observación</th></tr></thead>
<tbody>{filas_pre}</tbody></table>
<p class="nota">Rango amplio porque varía por puertos, 4G/Ethernet y volumen. La lista de
distribuidor no es pública: hay que pedirla.</p>
</div>

<h2>4. Comparación de valor</h2>
<div class="card" style="padding:8px 12px">
<table><thead><tr><th>Criterio</th><th>BLIIoT</th><th>CONECTA</th></tr></thead>
<tbody>{filas_cmp}</tbody></table>
</div>

<h2>5. Los veredictos</h2>
{veredictos}

<h2>6. ¿Conviene ser distribuidor? — los riesgos</h2>
{riesgos}

<div class="big">
  <div class="q">La respuesta corta</div>
  <b>No como negocio principal. Sí como herramienta puntual.</b>
  <p>Distribuir BLIIoT te mete en el negocio de revender cajas por precio, que es exactamente
  donde CONECTA no gana. El margen de un gateway de US$ 100 no paga importación, stock, garantía
  ni soporte en terreno — y sobre todo, no paga la ingeniería que es lo que CONECTA vende.</p>
</div>

<div class="alt">
  <b>El uso que sí tiene sentido:</b> tenerlo como <b>alternativa de bajo costo para proyectos
  donde el cliente no puede pagar un OrionLX+</b> (un PMGD chico, una planta piloto, una
  integración interna). Se usa como herramienta, no como línea de producto. Y se cobra la
  ingeniería, no la caja: el hardware es el 10% del valor; la integración, el 90%.
</div>

<h2>7. Qué preguntar antes de decidir (si igual se quiere explorar)</h2>
<div class="card">
  <p style="font-size:14px;color:#374151;line-height:1.8">
  1. <b>Lista de precios de distribuidor</b> y descuento real por volumen.<br>
  2. <b>Exclusividad territorial</b> para Chile: sin eso, cualquiera importa y te rompe el precio.<br>
  3. <b>Plazo de reposición</b> y quién paga el flete de una garantía.<br>
  4. <b>Soporte técnico en español</b> y SLA de respuesta.<br>
  5. <b>Certificaciones reales</b> para el mercado chileno: ¿IEC 61850-3? ¿IEC 62443? Sin eso
  no entra a una subestación.<br>
  6. <b>Compatibilidad con el Coordinador</b>: ¿sirve para SSCC, PMU, EDAC? (respuesta esperable: no).<br>
  7. <b>Qué pasa si SUPCON se entera</b> de que se distribuye un competidor de su capa de borde.
  </p>
</div>

<footer>
  Fuentes: es.bliiot.com (sitio oficial, catálogo y "sobre nosotros") · marketplaces para precios
  (Alibaba, Made-in-China, distribuidores). Fecha de consulta: octubre 2026.<br>
  Documento interno CONECTA. No distribuir a clientes ni a terceros.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
