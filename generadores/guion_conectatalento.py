#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guion de exposición — Workshop ConectaTalento 2026, Facultad de Ingeniería PUCV.

Audiencia: estudiantes de ingeniería próximos a práctica profesional / primer empleo.
Objetivo real: atraer talento. CONECTA pretende crecer aceleradamente y necesita mucha gente.
Duración: 15 minutos (la PUCV da 15-20).

Estructura pedida por Victor:
  - Áreas de la empresa separadas en DOS líneas: POWER y PROCESOS (SUPCON).
  - Énfasis en tendencias de los próximos 10-20 años.
  - 1-2 slides sobre que lo que importa es la ACTITUD y el LIDERAZGO.
"""
import os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "artefactos", "guion_conectatalento_2026.html")


def esc(x):
    return html.escape(str(x if x is not None else ""))


# (n, titulo, minutos, [lineas de guion], nota_escena)
SLIDES = [
    (1, "Portada — CONECTA", 0.3, [
        "Buenos días. Soy Víctor Vilche, ingeniero eléctrico, CEO de CONECTA.",
        "Vengo a hablarles de dos cosas: del mundo al que van a entrar cuando se titulen,",
        "y de qué buscamos nosotros en la gente que va a entrar con nosotros.",
    ], "Sin diapositiva de logos. Solo el nombre y el año: 2026→2046."),
    (2, "La práctica no es el primer empleo: es la primera decisión de carrera", 0.6, [
        "Varios de ustedes están a punto de titularse. La práctica y el primer trabajo",
        "son las próximas decisiones grandes que van a tomar.",
        "Y esa decisión no la define solo el primer sueldo: la define dónde van a estar parados",
        "en diez o veinte años. Porque les quedan cuarenta años de carrera.",
        "Entonces la pregunta no es '¿hay trabajo hoy?'. La pregunta es",
        "¿dónde está el trabajo que va a seguir existiendo en 2046?",
    ], "Decirlo mirando a los que están por titularse. Esta slide cambia el marco: no es una charla de empresa."),
    (3, "Tendencia 1: la demanda eléctrica se duplica (2035-2043)", 1.2, [
        "Según el Coordinador Eléctrico Nacional, en el escenario medio la demanda pasa a",
        "106 TWh al 2035. En el escenario alto, 117. Y si el hidrógeno verde despega: 149 TWh.",
        "Es prácticamente el doble de lo que consumimos hoy.",
        "Duplicar la demanda eléctrica de un país no se hace con más cables solamente:",
        "se hace con más generación, más subestaciones, más control, y gente que sepa operarlo.",
        "Y esos TWh no los opera un algoritmo: los opera gente que sabe. Gente que se titula ahora.",
    ], "Cifra dura del Coordinador. Es la tendencia madre: las otras dos cuelgan de esta."),
    (4, "Tendencia 2: US$104.549 millones en minería a 2034", 1.2, [
        "Cochilco proyecta la cartera minera 2025-2034 en 104.549 millones de dólares.",
        "Eso son plantas, moliendas, fundiciones, relaves, puertos, líneas eléctricas.",
        "Cada uno de esos proyectos tiene un DCS, un sistema de protección, instrumentación,",
        "una subestación y un equipo que lo pone en marcha.",
        "Cuando dicen 'Chile es un país minero', ese es el tamaño del número.",
    ], "Segunda tendencia. Conecta directo con la línea PROCESOS."),
    (5, "Tendencia 3: faltan 37.000 trabajadores, y 75% en 4 perfiles", 1.5, [
        "El estudio de fuerza laboral minera proyecta unos 37.000 nuevos trabajadores al 2034.",
        "Pero el dato que a ustedes les importa es otro: el 73 al 75% de esa demanda",
        "está en CUATRO perfiles: mantenedores mecánicos, mantenedores ELÉCTRICOS,",
        "operadores de equipos móviles y operadores de equipos fijos.",
        "O sea: falta gente exactamente en lo que ustedes están estudiando.",
        "El 88% de esa demanda NO son proyectos nuevos: es reemplazo por gente que se jubila.",
        "Y ojo con la fecha: esa demanda no empieza en 2034. Corre desde ahora.",
        "Los que se jubilan se jubilan este año. El reemplazo se contrata antes.",
    ], "Tercera tendencia. Esta les habla HOY: el reemplazo se contrata antes de que el anterior se jubile."),
    (6, "Y la tendencia que falta nombrar: el ingeniero que ya no trabaja solo", 0.4, [
        "Hay una cuarta, que no está en ningún informe oficial y es la más importante para ustedes:",
        "el trabajo del ingeniero cambió. Antes el dato estaba en un tablero y en un papel.",
        "Hoy, en cada planta, hay miles de señales que nadie ocupa.",
        "La diferencia entre un ingeniero bueno y uno muy bueno ya no es saber calcular:",
        "es saber qué preguntar, qué dato importa y qué hacer con él.",
    ], "Puente entre tendencias y el trabajo real de CONECTA. Sin esto, las cifras quedan flotando."),
    (7, "CONECTA: dos líneas, dos mundos", 1.9, [
        "Y eso es lo que hacemos nosotros, en dos líneas distintas.",
        "Una es POWER, la de la energía: subestaciones, protección, control.",
        "La otra es PROCESOS, con SUPCON: el interior de la planta.",
        "Son dos ingenierías hermanas, pero no son el mismo trabajo.",
    ], "Slide de bisagra. Avisa que vienen dos áreas y que son distintas."),
    (8, "Línea POWER — la red, la subestación, la protección", 1.9, [
        "En POWER trabajamos lo que hace que la energía llegue: subestaciones, protecciones",
        "eléctricas, medición de calidad de energía, sincronización, comunicaciones industriales.",
        "Trabajamos con NovaTech, Vizimax y Belden/Hirschmann: relés, RTU, PMU, relojes,",
        "switches industriales.",
        "El día a día es calcular un ajuste de protección, probar un relé, comisionar una",
        "subestación, leer un unilineal, y responder al Coordinador Eléctrico cuando pide datos.",
        "Y es un trabajo donde el error se paga caro: un ajuste mal puesto apaga media ciudad.",
    ], "Aquí es donde entran los eléctricos puros. Perfiles: eléctrico, electrónico, control."),
    (9, "Línea PROCESOS — el interior de la planta, con SUPCON", 0.7, [
        "En PROCESOS trabajamos adentro: el DCS, el sistema de seguridad, la instrumentación,",
        "las válvulas de control, la analítica, la optimización avanzada, y la capa de datos.",
        "SUPCON es el fabricante que representamos: DCS ECS-700, SIS TCS-500, transmisores,",
        "válvulas, posicionadores, y plataformas de diagnóstico predictivo.",
        "El día a día es configurar un lazo, levantar una planta, sintonizar un controlador,",
        "dimensionar una válvula, o sacar el histórico de un molino para ver por qué se rompe.",
        "Aquí entran mecánicos, químicos, electrónicos, y también eléctricos que se quieran meter",
        "en el proceso.",
    ], "Aquí el perfil es más ancho. Resaltar que se aprende la planta, no solo el equipo."),
    (10, "Lo que se aprende en CONECTA (y dónde se aprende)", 0.8, [
        "Y se aprende en terreno, no en un PowerPoint.",
        "Los primeros meses uno va a planta: a la minera, a la generadora, a la subestación.",
        "Se ve el equipo real, se ve el ruido, se ve el turno de noche, se ve cuando algo falla.",
        "Eso no lo enseña la universidad y no se aprende leyendo.",
    ], "Hablar de terreno real. Mencionar clientes por tipo (mineras, generadoras, transmisoras)."),
    (11, "Cómo crecemos: acelerado, y por eso los necesitamos", 1.0, [
        "Nosotros estamos en una etapa de crecimiento acelerado, hoy.",
        "Eso tiene una consecuencia concreta para ustedes: la gente que entra ahora",
        "no entra a un puesto que ya existe: entra a construir el puesto que va a existir.",
        "En una empresa grande llegan a un organigrama. En una que crece, el organigrama",
        "se escribe con los que llegan.",
        "Y eso es más difícil. Y es la mejor escuela que hay.",
    ], "Aquí se dice la verdad: se trabaja fuerte, y se aprende mucho más rápido."),
    (12, "Lo que buscamos: no buscamos el mejor promedio", 1.0, [
        "Y ahora lo que de verdad importa.",
        "No buscamos el mejor promedio del curso. El promedio dice que alguien sabe memorizar.",
        "Buscamos algo distinto: que le importe hacer bien las cosas, que pregunte cuando no entiende,",
        "que se haga cargo cuando algo sale mal, y que no ande buscando quién tiene la culpa.",
        "En diez años, el que se destacó no fue el que sabía más.",
        "Fue el que se hizo cargo.",
    ], "Slide del cambio de tono. Victor pidió énfasis acá: actitud y liderazgo."),
    (13, "El liderazgo se aprende haciendo, no en un cargo", 0.5, [
        "Y el liderazgo no empieza cuando uno es gerente. Empieza el primer día.",
        "Liderazgo es anotar el dato que se te pidió aunque nadie te esté mirando.",
        "Es decir 'esto no lo sé, lo averiguo y te aviso' en vez de inventar.",
        "Es llegar a la planta a la hora que corresponde, con el EPP puesto y el plano leído.",
        "Nadie sigue a alguien que no cumple lo que dice. El liderazgo es eso, al principio:",
        "que tu palabra valga.",
    ], "Segunda slide de actitud. Aquí se puede contar una anécdota real corta (30 seg)."),
    (14, "Por qué CONECTA", 1.2, [
        "Somos una empresa chica que hace cosas grandes: subestaciones, plantas mineras,",
        "proyectos ante el Coordinador. Trabajamos con los fabricantes que están en la frontera,",
        "y hacemos la pega de punta a punta: vendemos, diseñamos, instalamos y ponemos en marcha.",
        "No tercerizamos el problema: nos hacemos cargo del resultado.",
        "Y eso enseña más que cualquier manual.",
    ], "Cierre institucional breve. Sin adjetivos inflados."),
    (15, "Cierre: la práctica es la primera decisión de carrera", 0.8, [
        "Así que la invitación es simple: hagan la práctica acá.",
        "No para que se queden para siempre: para que sepan lo que es la ingeniería de verdad,",
        "con el equipo delante y el cliente esperando.",
        "Varios de ustedes están a punto de titularse. Esta es la semana en que pueden elegir",
        "dónde empezar, y no es lo mismo empezar en un lugar que en otro.",
        "Acá hay trabajo para muchos años, en dos áreas distintas, en un país que necesita",
        "miles de ingenieros como ustedes en los próximos veinte.",
        "En el MatchUp los espero con un desafío real. Gracias.",
    ], "CTA: práctica / MatchUp. Nada de 'postulen a nuestra oferta laboral'."),
]

TEND = [
    ("Demanda eléctrica", "106 TWh", "2035, escenario medio", "Coordinador Eléctrico Nacional"),
    ("...escenario alto", "117 TWh", "2035", "Coordinador Eléctrico Nacional"),
    ("...con hidrógeno verde", "149 TWh", "2035", "Coordinador Eléctrico Nacional"),
    ("Inversión minera", "US$ 104.549 M", "cartera 2025-2034", "Cochilco"),
    ("Nuevos trabajadores", "~37.000", "al 2034", "CCM-Eleva / Consejo Minero"),
    ("Concentración de la demanda", "73-75%", "en 4 perfiles", "CCM-Eleva"),
    ("De esa demanda, por reemplazo", "88%", "jubilaciones", "CCM-Eleva"),
]

LINEAS = [
    ("POWER", "La red, la subestación, la protección",
     ["Subestaciones eléctricas", "Protecciones y ajustes", "RTU y SCADA",
      "Medición de calidad de energía", "Sincronización por satélite",
      "Comunicaciones industriales y ciberseguridad OT"],
     "NovaTech · Vizimax · Belden/Hirschmann",
     ["Ingeniería Eléctrica", "Electrónica", "Control e Instrumentación"],
     "El error se paga caro: un ajuste mal puesto apaga media ciudad."),
    ("PROCESOS", "El interior de la planta, con SUPCON",
     ["DCS ECS-700 y SIS TCS-500", "Instrumentación (transmisores, flujómetros)",
      "Válvulas de control y posicionadores", "Analizadores y CEMS",
      "Optimización avanzada (APC)", "Diagnóstico predictivo y capa de datos"],
     "SUPCON",
     ["Ejecución en Mecánica", "Química / Procesos", "Electrónica",
      "Eléctrica orientada a proceso"],
     "Se aprende la planta, no solo el equipo: por qué se rompe un molino, no solo que se rompió."),
]

ACTITUD = [
    ("Se hace cargo", "Cuando algo sale mal, la primera frase no es 'fue el otro'. Es 'qué hago ahora'. "
                      "En terreno nadie recuerda quién tuvo la culpa; todos recuerdan quién lo arregló."),
    ("Pregunta cuando no entiende", "'No lo sé, lo averiguo y te aviso' vale infinitamente más que una "
                                    "respuesta inventada. En una planta, el invento se detecta en 5 minutos."),
    ("Cumple lo que dice", "Si dijiste que a las 8, a las 7:50 estás. El liderazgo no empieza en un cargo: "
                           "empieza cuando tu palabra vale."),
    ("Le importa el detalle", "Anotar el dato que te pidieron aunque nadie te esté mirando. Ahí se separa "
                              "la gente que va a llegar lejos de la que se queda."),
    ("No se achica", "En una empresa que crece, no hay puesto que ya exista: uno construye el puesto. "
                     "Eso asusta, y es exactamente la oportunidad."),
]

FILAS_TEND = "".join(
    f'<tr><td>{esc(t[0])}</td><td class="num">{esc(t[1])}</td><td class="per">{esc(t[2])}</td>'
    f'<td class="fuen">{esc(t[3])}</td></tr>' for t in TEND)

TARJ_LIN = "".join(f'''
  <div class="lin {c[0].lower()}">
    <div class="lh"><span class="lt">{esc(c[0])}</span><span class="ls">{esc(c[1])}</span></div>
    <ul>{"".join(f"<li>{esc(x)}</li>" for x in c[2])}</ul>
    <div class="lf"><b>Representamos:</b> {esc(c[3])}</div>
    <div class="lf"><b>Perfiles:</b> {esc(", ".join(c[4]))}</div>
    <div class="lc">{esc(c[5])}</div>
  </div>''' for c in LINEAS)

ACT = "".join(f'<div class="act"><b>{i+1}. {esc(a[0])}</b><p>{esc(a[1])}</p></div>'
              for i, a in enumerate(ACTITUD))

TOTAL = sum(s[2] for s in SLIDES)
TABLA_SLIDES = "".join(
    f'<tr><td class="n">{s[0]}</td><td><b>{esc(s[1])}</b></td><td class="num">{s[2]:.1f}′</td></tr>'
    for s in SLIDES)

HTML_SLIDES = "".join(
    f'''
<div class="sl">
  <div class="sh"><span class="sn">{s[0]}</span><span class="st">{esc(s[1])}</span><span class="sm">{s[2]:.1f}′</span></div>
  <div class="say">{chr(10).join("<br>" + esc(l) for l in s[3]).lstrip()}</div>
  <div class="nota"><b>Escena:</b> {esc(s[4])}</div>
</div>''' for s in SLIDES)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guion — Workshop ConectaTalento 2026 · CONECTA</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--vd:#16a34a;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.65;padding:26px 18px 70px}}
.wrap{{max-width:1100px;margin:0 auto}}
h1{{font-size:27px;font-weight:700;letter-spacing:-.5px}}
.sub0{{color:var(--mu);font-size:14.5px;margin:6px 0 20px;max-width:900px}}
h2{{font-size:20px;font-weight:680;margin:32px 0 12px;padding-bottom:7px;border-bottom:2px solid var(--bd)}}
h3{{font-size:16px;font-weight:660;margin-bottom:6px}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:18px 22px;margin-bottom:14px}}
.ficha{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:9px;margin-bottom:18px}}
.fi{{background:#fff;border:1px solid var(--bd);border-left:4px solid var(--ac);border-radius:10px;padding:11px 15px}}
.fi b{{font-size:10.5px;color:var(--mu);text-transform:uppercase;letter-spacing:.5px;display:block}}
.fi span{{font-size:14.5px;font-weight:650}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;padding:9px 10px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 10px;border-bottom:1px solid #f1f5f9}}
.num{{font-weight:700;font-variant-numeric:tabular-nums;color:var(--ac);white-space:nowrap}}
.n{{font-weight:700;color:var(--mu);width:34px}}
.per{{color:#475569;font-size:13.5px}}
.fuen{{color:#94a3b8;font-size:12px;font-style:italic}}
.plan{{background:#eff6ff;border-left:4px solid var(--ac);border-radius:0 8px 8px 0;padding:12px 18px;margin-bottom:18px;font-size:14px}}
.sl{{background:#fff;border:1px solid var(--bd);border-radius:12px;padding:16px 20px;margin-bottom:11px;page-break-inside:avoid}}
.sh{{display:flex;gap:12px;align-items:baseline;margin-bottom:9px;flex-wrap:wrap}}
.sn{{background:var(--ac);color:#fff;font-size:12.5px;font-weight:700;border-radius:6px;padding:2px 9px}}
.st{{font-size:16px;font-weight:680;flex:1}}
.sm{{font-size:12.5px;color:var(--mu);font-variant-numeric:tabular-nums;background:#f1f5f9;border-radius:5px;padding:2px 8px}}
.say{{border-left:3px solid var(--vd);padding-left:14px;margin:9px 0;font-size:15px;color:#1e293b}}
.nota{{font-size:13px;color:#92400e;background:#fffbeb;border-radius:7px;padding:8px 13px;margin-top:9px}}
.nota b{{color:#b45309}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.lin{{border-radius:11px;padding:16px 19px;border:1px solid var(--bd);background:#fff;border-top:4px solid}}
.lin.power{{border-top-color:#2563eb}}
.lin.procesos{{border-top-color:#16a34a}}
.lh{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:9px}}
.lt{{font-size:17px;font-weight:750;letter-spacing:.5px}}
.power .lt{{color:#1d4ed8}} .procesos .lt{{color:#15803d}}
.ls{{font-size:13px;color:var(--mu)}}
.lin ul{{margin:0 0 10px 17px}}
.lin li{{font-size:13.5px;margin-bottom:2px}}
.lf{{font-size:12.5px;color:#475569;margin-top:3px}}
.lc{{font-size:12.5px;color:#7c2d12;background:#fff7ed;border-radius:6px;padding:6px 10px;margin-top:9px}}
.act{{background:#fff;border:1px solid var(--bd);border-left:4px solid var(--am);border-radius:10px;padding:12px 17px;margin-bottom:8px}}
.act b{{font-size:14.5px;color:#92400e}}
.act p{{font-size:13.5px;color:#374151;margin-top:3px}}
.grande{{background:#0f172a;color:#f1f5f9;border-radius:12px;padding:22px 26px;margin:16px 0;text-align:center}}
.grande b{{font-size:19px;font-weight:650;display:block;line-height:1.5}}
.grande span{{font-size:13px;color:#94a3b8;display:block;margin-top:8px}}
footer{{margin-top:30px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
@media print{{body{{padding:0;font-size:12px}} .sl{{page-break-inside:avoid}}}}
</style></head><body><div class="wrap">

<h1>Guion — Workshop ConectaTalento 2026</h1>
<p class="sub0">Facultad de Ingeniería PUCV · Auditorio Aulario de Ingeniería, Brasil 2162, Valparaíso ·
<b>martes 20 de octubre de 2026, 09:30</b>. Bloque de exposición: CONECTA, 15 minutos.<br>
Audiencia: estudiantes de ingeniería próximos a práctica profesional o primer empleo.
<b>Objetivo: atraer talento.</b></p>

<div class="ficha">
  <div class="fi"><b>Duración</b><span>{TOTAL:.1f} min</span></div>
  <div class="fi"><b>Slides</b><span>{len(SLIDES)}</span></div>
  <div class="fi"><b>Foco</b><span>Talento, no venta</span></div>
  <div class="fi"><b>Después</b><span>MatchUp 45 min</span></div>
</div>

<div class="plan">
  <b>La tesis, en una frase:</b> no vengas a decir que CONECTA es buena empresa.
  Ven a mostrarles <b>el tamaño del mundo al que van a entrar</b> — duplicar la demanda eléctrica,
  US$104 mil millones en minería, 37.000 trabajadores faltantes — y después decirles
  <b>que en CONECTA ese mundo se toca con las manos desde la práctica</b>, en dos líneas distintas,
  y que lo que más pesa para entrar no es el promedio sino cómo se hace cargo de las cosas.
</div>

<h2>1. Las cifras duras (para no improvisar)</h2>
<div class="card">
<p style="font-size:13.5px;color:#475569;margin-bottom:11px">Todo lo que se diga de tendencias sale de
acá. Si alguien pregunta la fuente en el MatchUp, se responde con nombre propio.</p>
<table><thead><tr><th>Indicador</th><th>Cifra</th><th>Horizonte</th><th>Fuente</th></tr></thead>
<tbody>{FILAS_TEND}</tbody></table>
</div>

<h2>2. Las dos líneas de CONECTA (esto es lo que se les tiene que quedar)</h2>
<div class="grid2">{TARJ_LIN}</div>

<h2>3. Actitud y liderazgo — lo que de verdad se evalúa</h2>
{ACT}
<div class="grande">
  <b>"En diez años, el que se destacó no fue el que sabía más.<br>Fue el que se hizo cargo."</b>
  <span>Frase de cierre de la slide 12. Decirla despacio y callarse dos segundos.</span>
</div>

<h2>4. El guion, slide por slide</h2>
<p class="sub0" style="margin-bottom:14px">Los textos en verde son <b>lo que se dice</b>, casi
literal. No leerlos: decirlos. Las notas en ámbar son de escena.</p>
{HTML_SLIDES}

<h2>5. Resumen de tiempos</h2>
<div class="card" style="padding:10px 16px">
<table><thead><tr><th>#</th><th>Slide</th><th>Tiempo</th></tr></thead><tbody>{TABLA_SLIDES}
<tr><td></td><td><b>TOTAL</b></td><td class="num">{TOTAL:.1f}′</td></tr></tbody></table>
</div>

<h2>6. El MatchUp (45 min, después de la charla)</h2>
<div class="card">
  <h3>Qué llevar</h3>
  <p style="font-size:14px;color:#374151">La PUCV dice que <b>no hay que llevar nada preparado</b>,
  solo el tiempo. Pero conviene tener un desafío real corto en la cabeza, porque la dinámica es
  resolver un problema con los estudiantes.</p>
  <h3 style="margin-top:13px">Un desafío real de CONECTA que sirve para esto</h3>
  <p style="font-size:14px;color:#374151">"En una planta hay 945 señales y 10 pantallas donde
  nadie encuentra nada. ¿Cómo las ordenamos para que un operador encuentre en 5 segundos lo que
  necesita?" — es real, es de un proyecto hecho, y no requiere que sepan nada previo.</p>
  <h3 style="margin-top:13px">Lo que se hace en la mesa</h3>
  <p style="font-size:14px;color:#374151">Escuchar más que hablar. Preguntar qué quieren hacer:
  ¿red, planta, datos, diseño? Anotar nombres. <b>El objetivo del MatchUp es una lista de
  candidatos, no una clase.</b></p>
</div>

<h2>7. Riesgos de la charla (y cómo evitarlos)</h2>
<div class="card">
  <div class="nota" style="margin-bottom:8px"><b>Riesgo 1 · Sonar a reclutamiento genérico.</b>
  Se evita con las cifras: nadie más va a decir que faltan 37.000 trabajadores y 75% en 4 perfiles.</div>
  <div class="nota" style="margin-bottom:8px"><b>Riesgo 2 · Que las dos líneas se confundan.</b>
  La slide 7 es bisagra explícita: "son dos ingenierías hermanas, pero no es el mismo trabajo".
  Si se mezclan, el estudiante no sabe a cuál apuntar.</div>
  <div class="nota" style="margin-bottom:8px"><b>Riesgo 3 · Prometer de más.</b> No decir cifras de
  sueldos que no se van a cumplir ni "crecemos 300% al año". Decir "crecimiento acelerado" y que lo
  demás lo deduzcan.</div>
  <div class="nota" style="margin-bottom:8px"><b>Riesgo 4 · Hablarles como si recién empiezan.</b>
  Están <b>a punto de titularse</b>: la práctica y el primer empleo son decisiones inminentes, no
  futuras. Nada de "cuando sean ingenieros" ni de proyectar su titulación a 2031.
  Todas las cifras de tendencia se conectan con <b>el trabajo que van a buscar este año</b>.</div>
  <div class="nota"><b>Riesgo 5 · Pasarse de los 15 minutos.</b> Con 15 slides y ~1,5 min cada una
  no hay margen. Si el reloj aprieta, lo que se recorta es la slide 10 (lo que se aprende) y la 14
  (por qué CONECTA) — nunca las de tendencias ni las de actitud.</div>
</div>

<footer>
  Fuentes: Coordinador Eléctrico Nacional (proyección de demanda SEN) · Cochilco (cartera de
  proyectos mineros 2025-2034) · CCM-Eleva / Consejo Minero (estudio de fuerza laboral).<br>
  Evento: Workshop ConectaTalento 2026, Facultad de Ingeniería PUCV, 3ª edición.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"slides: {len(SLIDES)} · total: {TOTAL:.1f} min")
