#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/estrategia_penetracion.html

Estrategia de entrada al mercado chileno con el catálogo SUPCON, ordenada de lo MÁS FÁCIL a lo
MÁS DIFÍCIL. El orden NO es por tamaño de mercado: es por dificultad real de entrar.

Los cuatro ejes que definen la dificultad, y de dónde sale cada uno:
  1. Base instalada / incumbente  -> Registro DIN de Aduanas 2025 (quién ya está vendiendo)
  2. Capacidad de responder (R)   -> material del fabricante (campos sin respaldo, battlecard)
  3. Complejidad de la venta      -> cuántos actores deciden, si es producto o proyecto
  4. Riesgo para el cliente       -> qué pierde si el producto falla

Salida: artefactos/estrategia_penetracion.html
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
ART = os.path.join(BASE, "artefactos")

E = json.load(open(os.path.join(D, "escalera_exito.json"), encoding="utf-8"))
PERF = json.load(open(os.path.join(D, "perfilado_74_integradores.json"), encoding="utf-8"))

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706;--ams:#fffbeb;--ok:#047857;--oks:#ecfdf5}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}
.wrap{max-width:1000px;margin:0 auto}
h1{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}
.sub{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:860px}
h2{font-size:20px;font-weight:660;margin:36px 0 10px;letter-spacing:-.2px}
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
.paso{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:18px 21px;margin-bottom:14px;border-left:4px solid #64748b}
.paso.n1{border-left-color:#047857}.paso.n2{border-left-color:#2563eb}
.paso.n3{border-left-color:#d97706}.paso.n4{border-left-color:#94a3b8}
.ph{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;margin-bottom:8px}
.pn{font-size:22px;font-weight:700;color:#cbd5e1;min-width:34px}
.et{font-size:11px;border-radius:5px;padding:2px 9px;font-weight:700;text-transform:uppercase;letter-spacing:.3px}
.e1{background:var(--oks);color:var(--ok)}.e2{background:var(--acs);color:var(--ac)}
.e3{background:var(--ams);color:var(--am)}.e4{background:#f1f5f9;color:#475569}
.sub2{font-size:12.5px;color:var(--mu);margin-bottom:10px}
.sub2 b{color:var(--tx)}
.dos{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:11px}
@media(max-width:720px){.dos{grid-template-columns:1fr}}
.dos h4{font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;margin-bottom:5px}
.riesgo{background:#fbfdff;border:1px solid var(--bd);border-radius:8px;padding:11px 13px;font-size:13.5px}
footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}
footer a{color:var(--ac)}
"""

PASOS = [
 {
  "n":"1", "cls":"n1", "et":"et e1", "etq":"El más fácil",
  "titulo":"Entrar por donde no hay incumbente ni riesgo de parada",
  "linea":"Analítica · Instrumentación",
  "mercado":"US$44,3M analizadores · US$60,5M instrumentación",
  "porque":"<b>El mercado está vacío y el riesgo del cliente es bajo.</b> No hay un solo analizador "
     "SUPCON ni Hobré importado en Chile: no existe base instalada que defender ni comparación "
     "directa con un incumbente. Además, varios de estos productos no detienen la producción si "
     "fallan — miden, informan, optimizan. Son la venta más fácil de justificar.",
  "que":"CEMS 5000 (monitoreo de emisiones) · NICOSYS-3 (detección de CO en secadores) · "
     "WIM COMPAS (índice de Wobbe) · PRISM (Raman) · HIFISC (acondicionamiento de muestra) · "
     "SFE910 (caudal electromagnético) · SL903 (radar de nivel 80 GHz)",
  "entrada":"El argumento no es reemplazar nada: es resolver un problema que hoy no se mide. "
     "En CEMS, el argumento es normativo (monitoreo de emisiones). En NICOSYS-3, es el costo del "
     "seguro y la continuidad de la planta (detecta 30 minutos antes del incendio). En HIFISC, es "
     "que el analizador que el cliente YA tiene mida bien.",
  "objecion":"«No conozco la marca» — es real y hay que responderla con datos técnicos concretos, "
     "no con marca. Estos productos tienen especificaciones verificables.",
  "riesgo":"Bajo. Si el equipo falla, la planta sigue produciendo.",
 },
 {
  "n":"2", "cls":"n2", "et":"et e2", "etq":"Fácil con argumento",
  "titulo":"Entrar por donde el incumbente tiene una debilidad concreta y medible",
  "linea":"Software y plataforma",
  "mercado":"No medible con Aduanas (se vende dentro del proyecto)",
  "porque":"<b>Acá el material del fabricante SÍ trae el argumento competitivo.</b> Es la única "
     "línea donde SUPCON documentó battlecards: el RTO declara a Aspen y AVEVA con su desventaja de "
     "licencia única; OMS declara Honeywell y Yokogawa. Y SolisSCADA tiene el argumento más fuerte "
     "del portafolio: 50.000 tags gratis contra el cobro por tag de los incumbentes.",
  "que":"SolisSCADA (SCADA) · InPlant APC · InPlant RTO · APEX · InPlant OTS · InPlant PID",
  "entrada":"<b>SolisSCADA es la mejor puerta de entrada del catálogo completo.</b> Es lo más "
     "cercano a una venta sin riesgo: software con licencia gratuita hasta 50.000 tags, más de 100 "
     "protocolos soportados, y el cliente puede probarlo sin comprometer presupuesto. No obliga a "
     "cambiar hardware. Si funciona, abre la puerta al APC, al RTO y al resto.",
  "objecion":"«¿Quién da soporte?» — es la objeción central del software y hay que responderla con "
     "el modelo comercial del fabricante, que todavía está por completar.",
  "riesgo":"Medio-bajo. El software no detiene la planta si falla, pero el cliente sí lo evalúa.",
 },
 {
  "n":"3", "cls":"n3", "et":"et e3", "etq":"Difícil pero medible",
  "titulo":"Entrar por el hardware donde ya hay marca instalada y el volumen es grande",
  "linea":"Válvulas · SIS · PLC · DCS",
  "mercado":"US$396,6M válvulas · US$112,5M DCS · US$83,9M PLC · US$52,8M SIS",
  "porque":"<b>Mercados grandes, pero ocupados por marcas con base instalada.</b> "
     "Las válvulas son, de hecho, el mercado de hardware más grande del catálogo (US$396,6M), "
     "más que el DCS. Acá el cliente "
     "ya compra a alguien: Siemens (US$23,0M importados), Hitachi, Hyosung en control; BRAY, "
     "Valmet, Valvitalia en válvulas. Cambiar de proveedor significa cambiar un sistema del que "
     "depende la producción. La venta es por proyecto nuevo, ampliación o reemplazo de equipo "
     "fuera de soporte — nunca por desplazamiento directo.",
  "que":"TCS-900 y TCS-500 (SIS SIL3) · G5Pro y G5Pro Safety (PLC) · ECS-700 (DCS) · "
     "UCS Nyx (control definido por software) · línea completa de válvulas SUPCON FLUID",
  "entrada":"<b>Por proyecto nuevo, no por reemplazo.</b> En una planta que se está construyendo "
     "no hay base instalada que vencer. El argumento de entrada es el precio y la integración entre "
     "líneas del mismo proveedor (DCS + instrumentación + válvulas cotizados juntos). Y en válvulas, "
     "hay un nicho real: la serie VN de bola V corta fibras, para pulpa y sólidos en suspensión.",
  "objecion":"«¿Quién da soporte en Chile y qué pasa con los repuestos?» — <b>es la objeción que "
     "hay que resolver con el fabricante antes de ofrecer.</b> Quedó marcada como POR COMPLETAR en "
     "todas las fichas de estas líneas.",
  "riesgo":"Alto. Es infraestructura crítica: si falla, se para la producción.",
 },
 {
  "n":"4", "cls":"n4", "et":"et e4", "etq":"El más difícil",
  "titulo":"Entrar por donde competimos contra el estándar de facto de la industria",
  "linea":"Analítica de laboratorio · instrumentos especializados",
  "mercado":"Dentro de los mercados ya medidos, en los nichos más defendidos",
  "porque":"<b>Hay incumbentes con tecnología propia y décadas de ventaja.</b> No es que el "
     "producto sea malo: es que el competidor tiene el estándar y el cliente no tiene razón para "
     "cambiar. Y en varios casos el propio material del fabricante no entrega el argumento necesario.",
  "que":"SFM800 (caudal másico, contra Micro Motion de Emerson) · X600 (calibrador, contra Fluke "
     "y Omicron) · LUGB y YHLW (vortex y turbina, sin battlecard y con material escaso) · "
     "JX-300XP (plataforma de generación anterior, sin documentación local)",
  "entrada":"<b>Entrar solo si el cliente pide comparación.</b> En estos casos no conviene atacar "
     "de frente: hay que esperar la licitación donde el incumbente no califique, o el equipo fuera "
     "de soporte. Fluke domina los calibradores (US$3,7M) y Micro Motion el caudal másico "
     "(US$1,2M): son posiciones construidas, no precios.",
  "objecion":"«Ya uso X y funciona» — en estos productos no hay respuesta buena todavía. SFM800 y "
     "X600 quedaron con R en ROJO en la escalera: falta material de base para cotizar. <b>La "
     "recomendación es no ofrecerlos hasta tener la documentación del fabricante.</b>",
  "riesgo":"Muy alto, con el agravante de que no tenemos el material para responder.",
 },
]

pasos_html = ""
for p in PASOS:
    pasos_html += f"""
<div class="paso {p['cls']}">
  <div class="ph"><span class="pn">{p['n']}</span><h3>{p['titulo']}</h3>
    <span class="{p['et']}">{p['etq']}</span></div>
  <div class="sub2"><b>Línea:</b> {p['linea']} &nbsp;·&nbsp; <b>Mercado:</b> {p['mercado']}</div>
  <p>{p['porque']}</p>
  <div class="dos">
    <div><h4>Productos de este escalón</h4><div class="riesgo">{p['que']}</div></div>
    <div><h4>Argumento de entrada</h4><div class="riesgo">{p['entrada']}</div></div>
  </div>
  <div class="dos">
    <div><h4>Objeción principal</h4><div class="riesgo">{p['objecion']}</div></div>
    <div><h4>Riesgo para el cliente</h4><div class="riesgo">{p['riesgo']}</div></div>
  </div>
</div>"""

# canal: los 74 integradores
canal = PERF
top10 = canal.get("concentracion", {}).get("top10_individual", [])
filas_top = ""
for t in top10[:8]:
    filas_top += (f'<tr><td>ID {t["id"]}</td><td class="num">US${t["usd"]/1e6:,.2f}M</td>'
                  f'<td class="num">{t["pct_del_subtotal"]}%</td></tr>')

HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Estrategia de penetración — SUPCON en Chile</title><style>{CSS}</style></head>
<body><div class="wrap">

<h1>Estrategia de penetración de mercado</h1>
<p class="sub">Cómo entrar con el catálogo SUPCON en Chile, ordenado de lo más fácil a lo más difícil.
El orden no sigue el tamaño del mercado: sigue la dificultad real de entrar.</p>

<div class="box">
  <b>El punto de partida, en tres datos.</b>
  <ul style="margin-top:10px">
    <li>El mercado de automatización e instrumentación en Chile mueve <b>US$316,9M al año</b> (importaciones
        2025, rubro filtrado por partida y marca).</li>
    <li>SUPCON y Hobré tienen <b>cero presencia registrada</b> en ese mercado. No hay base instalada
        ni canal comprometido.</li>
    <li>Pero <b>64% de los integradores del rubro ya traen alguna marca competidora</b>, y Siemens
        es la más representada: US$31,1M entre los 74 integradores del canal técnico.</li>
  </ul>
  Conclusión: el mercado está abierto pero el canal ya está alineado con el estándar europeo.
  La entrada tiene que ser por donde el cliente no tenga que cambiar nada.
</div>

<h2>Los cuatro escalones de dificultad</h2>
<p>La dificultad de entrar depende de cuatro cosas, y las cuatro se midieron:</p>
<table>
  <tr><th>Eje</th><th>Qué mide</th><th>De dónde sale el dato</th></tr>
  <tr><td><b>Base instalada</b></td><td>¿Cuánta marca competidora ya está vendiendo?</td>
      <td>Registro de Aduanas 2025</td></tr>
  <tr><td><b>Capacidad de responder</b></td><td>¿Podemos cotizar y defender el producto hoy?</td>
      <td>Material del fabricante: campos sin respaldo y battlecard</td></tr>
  <tr><td><b>Complejidad de la venta</b></td><td>¿Es producto o proyecto? ¿Cuántos deciden?</td>
      <td>Tipo de producto y etapas del proyecto</td></tr>
  <tr><td><b>Riesgo para el cliente</b></td><td>¿Qué pierde si el producto falla?</td>
      <td>Función del producto en la planta</td></tr>
</table>

{pasos_html}

<h2>Por qué este orden y no otro</h2>
<div class="ok">
  <b>La regla que ordena todo.</b> Se entra por donde el cliente <u>no tiene que cambiar nada</u> y
  <u>no arriesga su producción</u>. El escalón 1 son productos que hoy no tiene y que no le pueden
  parar la planta. El escalón 4 son productos donde ya compra a alguien con tecnología propia y donde
  además nos falta material para responder.
</div>
<p>Es tentador ir directo a los mercados grandes: DCS (US$112,5M) y PLC (US$83,9M) son los números
más altos de la tabla. Pero son justamente los más difíciles: son sistemas de los que depende la
producción, con incumbentes instalados y ningún proyecto nuevo garantizado. Empezar ahí significa
gastar el primer año en licitaciones que se pierden por falta de referencia local.</p>

<h2>El canal: dónde está la puerta real</h2>
<p>El canal técnico de instrumentación en Chile son <b>74 integradores</b> que mueven
<b>US$108,6M</b> al año. Los datos que importan para elegir a quién tocar:</p>
<ul>
  <li><b>Están concentrados:</b> los 10 primeros mueven el 31,7% del volumen del canal.</li>
  <li><b>Están en el barrio alto:</b> 41 de 74 (55%) despachan desde Las Condes.</li>
  <li><b>No son especialistas:</b> 45 de 74 (61%) dedican menos del 40% de su importación al rubro.
      La instrumentación es una línea más entre muchas.</li>
  <li><b>El 64% ya trae marca competidora</b> de SUPCON en su top 10. Cero traen SUPCON.</li>
</ul>
<div class="aviso">
  <b>El hallazgo que define a quién tocar primero.</b> Los integradores con una sola marca en el
  rubro son probablemente el representante exclusivo de esa marca: moverlos es casi imposible. Los
  multirrubro con más de 3 marcas son permeables a incorporar una línea nueva. <b>Ahí hay que
  apuntar.</b> Y el mejor candidato de todos es el que combina instrumentación con capítulos no
  eléctricos (alimentos, química, papel): ese arma solución de planta completa y puede comprar el
  portafolio entero (DCS + instrumentación + válvulas), no un producto suelto.
</div>
<table>
  <tr><th>Los 10 mayores integradores del canal</th><th class="num">Volumen del rubro</th><th class="num">% del canal</th></tr>
  {filas_top}
</table>

<h2>Qué hacer antes de vender</h2>
<p>Tres cosas están bloqueadas hoy, y las tres dependen del fabricante, no del esfuerzo comercial:</p>
<table>
  <tr><th>Bloqueo</th><th>Qué falta</th><th>Por qué importa</th></tr>
  <tr><td><b>Soporte y repuestos en Chile</b></td>
      <td>No hay estructura de servicio documentada para ninguna línea</td>
      <td>Es la primera objeción de un cliente chileno ante una marca sin presencia local</td></tr>
  <tr><td><b>Battlecard en 53 de 63 productos</b></td>
      <td>El fabricante no entregó el argumento de competencia</td>
      <td>Sin eso, cada vendedor compite con lo que sabe de memoria, no con un argumento validado</td></tr>
  <tr><td><b>Documentación de 5 productos</b></td>
      <td>SFM800, X600, LUGB, YHLW y JX-300XP tienen material escaso</td>
      <td>Quedaron con R en rojo: no se pueden cotizar ni defender</td></tr>
</table>
<p><b>El pedido concreto al fabricante</b> es material de soporte para Chile y los battlecards
faltantes. Con eso, el escalón 1 y 2 quedan listos para vender.</p>

<h2>El resumen operativo</h2>
<ol style="list-style:none;counter-reset:n">
  <li style="position:relative;padding-left:26px;margin-bottom:9px">
    <b style="position:absolute;left:0;color:var(--ok)">1.</b>
    <b>Arrancar con SolisSCADA y la línea de analítica.</b> SolisSCADA porque es gratis hasta
    50.000 tags y el cliente puede probarlo sin decidir nada. Analítica porque el mercado está
    vacío y no detiene la producción.</li>
  <li style="position:relative;padding-left:26px;margin-bottom:9px">
    <b style="position:absolute;left:0;color:var(--ac)">2.</b>
    <b>Tocar a los integradores multirrubro de Las Condes</b> — los que traen más de 3 marcas y
    combinan instrumentación con otros rubros. No a los representantes exclusivos.</li>
  <li style="position:relative;padding-left:26px;margin-bottom:9px">
    <b style="position:absolute;left:0;color:var(--am)">3.</b>
    <b>Buscar proyectos nuevos</b> para DCS, PLC, SIS y válvulas. No intentar desplazar a Siemens
    o BRAY en una planta en operación.</li>
  <li style="position:relative;padding-left:26px;margin-bottom:9px">
    <b style="position:absolute;left:0;color:var(--mu)">4.</b>
    <b>No ofrecer SFM800, X600, LUGB ni YHLW</b> hasta tener la documentación del fabricante.
    Competir contra Fluke y Micro Motion sin argumento técnico es regalar la reunión.</li>
</ol>

<footer>
  Estrategia elaborada por CONECTA. Mercado: Registro DIN de Aduanas de Chile 2025.
  Capacidad y battlecards: material del fabricante SUPCON y Hobré. Canal: perfilado de los 74
  integradores técnicos.
  <br>Ver <a href="metodologia_mercado.html">cómo se calcularon los números</a> ·
  <a href="escalera_exito.html">escalera al éxito</a> ·
  <a href="../index.html">catálogo de fichas</a>.
</footer>
</div></body></html>"""

open(os.path.join(ART, "estrategia_penetracion.html"), "w", encoding="utf-8").write(HTML)
print(f"escrito: estrategia_penetracion.html ({len(HTML.encode()):,} bytes)")
