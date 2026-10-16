#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/itl_postulacion.html — la información de postulación al ITL:
  - la ficha de cada desafío elegido (A3, A4, M1)
  - la jugada de SISTEMA (una arquitectura, los tres desafíos)
  - el mapa de los 8 desafíos y por qué sí/no
  - los datos duros y el riesgo del TRL

Fuente: itlchile.com/desafios + las 8 fichas técnicas (PDF) + las bases RFI (Anexo 1).
"""
import json, os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "artefactos", "itl_postulacion.html")


def esc(x):
    return html.escape(str(x if x is not None else ""))


# ---------------------------------------------------------------- datos duros
DUROS = [
    ("Cierre", "31 de julio de 2026, 23:59 h", "Quedan ~2 semanas hábiles"),
    ("Etapa", "RFI (Request for Information)", "Exploratoria: NO adjudica dinero, recopila capacidades"),
    ("Quién postula", "Persona jurídica (no natural)", "Empresa, EBT, startup, universidad, centro. Nacional o internacional"),
    ("TRL de entrada", "mínimo 4, máximo 8", "Se piden antecedentes que lo acrediten"),
    ("TRL objetivo", "mínimo 5, máximo 9", ""),
    ("Coinversión ITL", "hasta 50%", "La contraparte puede ser pecuniaria o VALORIZADA (bienes, servicios, know-how)"),
    ("Escala de referencia", "8 proyectos y ~US$50M en el primer llamado", "No es un ejercicio académico"),
    ("Formulario", "14 secciones (Anexo 1 de las bases)", "Anexos: cartas de interés + certificado de vigencia (<90 días) + declaración jurada"),
]

# ---------------------------------------------------------------- los 8 desafíos
DESAFIOS = [
    ("A1", "Valorización de salmueras, ZLD", "no",
     "Química de membranas y cristalización. No es la capa de datos.",
     "Pide caracterización fisicoquímica y planta piloto de proceso."),
    ("A2", "Pérdida por evaporación en grandes superficies", "no",
     "Coberturas flotantes, sombreaderos, capas monomoleculares.",
     "Es obra física y materiales, no digitalización."),
    ("A3", "Eficiencia y monitoreo predictivo en impulsión de agua y relaves", "si",
     "Monitoreo predictivo, cavitación/fugas/desgaste en tiempo real, gemelo digital.",
     "EL MÁS FUERTE. Excluye reemplazar infraestructura de bombeo: solo la capa encima."),
    ("A4", "Gestión hídrica inteligente: digitalización y decisión en tiempo real", "si",
     "Interoperabilidad OT/IT, dashboards georreferenciados, gemelo digital del ciclo del agua.",
     "El más obvio y por eso el MÁS COMPETIDO. Todos los integradores postulan acá."),
    ("E1", "Reciclaje de paneles solares y palas (Ley REP)", "no",
     "Planta de valorización física de residuos.",
     "Requiere infraestructura de reciclaje, no es nuestro negocio."),
    ("E2", "Suministro para industrias aisladas", "parcial",
     "Microredes renovables + almacenamiento para zonas fuera del SEN.",
     "Solo con un socio de energía. La capa de control y monitoreo sí es nuestra."),
    ("L1", "Materiales catódicos y anódicos de litio", "no",
     "Laboratorio de baterías, escalamiento de materiales.",
     "Cero relación."),
    ("M1", "Optimización de flotación y lixiviación", "si",
     "Sistemas de CONTROL EN LÍNEA, recuperación metalúrgica, menos insumos.",
     "EL SLEEPER: casi todos los postulantes son metalurgistas. El que traiga la capa de control se diferencia solo."),
]

# ---------------------------------------------------------------- las 3 fichas + el sistema
FICHAS = [
    {
        "cod": "A3",
        "titulo": "Eficiencia Energética y de Monitoreo en Sistemas de Transporte e Impulsión",
        "macro": "Agua",
        "por_que": "Es el desafío donde CONECTA encaja con MÁS ventaja y MENOS competencia: pide exactamente instrumentación + diagnóstico predictivo + tiempo real, que es la línea de producto.",
        "excluye": "Reemplazo masivo de infraestructura de bombeo · Rediseño de redes u obras civiles",
        "excluye_por_que": "El freno comercial más grande (convencer al cliente de cambiar sus bombas) desaparece: el desafío pide una CAPA ENCIMA de lo instalado.",
        "piden": [
            "Prototipo de diagnóstico en TIEMPO REAL que detecte cavitación, fugas o desgaste prematuro ANTES de la falla",
            "Integración de digitalización y herramientas de monitoreo predictivo en el piloto",
            "Gemelo digital del sistema de impulsión (KPI: % de error respecto a mediciones reales)",
            "Programa de entrenamiento para operadores",
        ],
        "kpis": [
            "Consumo energético específico de impulsión (kWh/m³) — se mide con caudalímetros + analizadores de potencia",
            "Disponibilidad operacional de los activos de bombeo (%)",
            "MTBF — tiempo medio entre fallas (horas) — sale del histórico de vibración",
            "Tiempo de respuesta del sistema de monitoreo predictivo (minutos) — es el KPI de la capa UNS",
            "Precisión del gemelo digital vs mediciones reales (% error)",
        ],
        "ofrecer": [
            ("Sensórica de proceso", "Instrumentación de campo: caudalímetros, transmisores de presión y temperatura, sensores de vibración. Resuelve cavitación y transientes con medición, no con estimación."),
            ("Analítica de calidad de agua", "La línea que resuelve el problema que CAUSA la cavitación: sólidos, pH, conductividad. Sin calidad medida, el diagnóstico predictivo adivina."),
            ("Capa UNS + histórico", "Los datos de vibración y proceso a un árbol de datos con histórico. El KPI de 'tiempo de respuesta' se responde con arquitectura, no con promesa."),
            ("Diagnóstico predictivo", "Detección temprana por tendencia de vibración y firma espectral. Es el 'prototipo de diagnóstico en tiempo real' que el desafío pide."),
            ("Gemelo digital", "Modelo del sistema de impulsión alimentado por datos reales. El KPI de '% de error' es directamente medible."),
        ],
        "itl": [
            ("Capacidad de monitoreo predictivo instalada en el ITL como base de servicios al sector", "Sí"),
            ("Gemelos digitales de sistemas de impulsión, replicables en distintas configuraciones", "Muy Alta"),
            ("Laboratorio hidráulico con curvas de desempeño de bombas", "Alta"),
            ("Protocolos de mantenimiento predictivo como servicio", "Sí"),
        ],
        "industria": "Minería metálica/no metálica, Empresas Sanitarias, Operadores de desalinización",
        "kpi_que_ya_medimos": "Consumo específico (kWh/m³) · tiempo de respuesta del sistema · precisión del gemelo",
    },
    {
        "cod": "A4",
        "titulo": "Gestión Hídrica Inteligente: de la Digitalización a la Toma de Decisiones en Tiempo Real",
        "macro": "Agua",
        "por_que": "El problema que declara es TEXTUALMENTE nuestro argumento: 'fragmentación de datos y altas latencias en la toma de decisiones'. Se responde con arquitectura de datos, que es lo que ya se vende.",
        "excluye": "Reemplazo de sistemas SCADA o de control existentes · Obras civiles o modificaciones de infraestructura hídrica",
        "excluye_por_que": "Igual que en A3: el desafío pide la capa de integración ENCIMA del SCADA, no su reemplazo. Es la venta sin el obstáculo.",
        "piden": [
            "Plataforma operativa de datos hídricos con gobernanza, interoperabilidad y CIBERSEGURIDAD validados en un piloto",
            "Reducción DEMOSTRABLE de la latencia en la toma de decisiones (con métricas vs línea base)",
            "Tableros de control con visualización GEORREFERENCIADA del ciclo completo (captación, proceso, relave, retorno)",
            "Gemelos digitales del ciclo del agua para simular escasez, fallas de impulsión y cambios de calidad",
            "Ruta de despliegue multi-sitio a partir del piloto",
        ],
        "kpis": [
            "Latencia en la toma de decisiones operacionales (minutos) — el KPI central, y es de arquitectura",
            "Reducción del consumo de agua de reposición — make-up (%)",
            "Frecuencia de eventos fuera de especificación de calidad (N°/mes) — se mide con analítica en línea",
            "Eficiencia de recirculación del agua recuperada",
            "Consumo energético específico del sistema (kWh/m³)",
        ],
        "ofrecer": [
            ("Capa de interoperabilidad OT/IT", "El puente que el desafío pide: OPC UA / Modbus desde el SCADA que YA existe hacia un árbol de datos unificado. Con ciberseguridad industrial (segmentación, puertos por red de planta, nunca expuestos)."),
            ("UNS con histórico", "El argumento directo del KPI de latencia: el dato llega al que decide, no en una planilla días después. Histórico activable por variable."),
            ("Dashboards georreferenciados", "El alcance los pide explícitamente: visualización del ciclo completo (captación → proceso → relave → retorno) sobre el plano de la faena."),
            ("Gemelo digital del ciclo", "Simulación de escasez, falla de impulsión y cambio de calidad para planificación preventiva."),
            ("Analítica de calidad en línea", "Reemplaza el laboratorio externo que el problema declara faltante: eventos fuera de especificación detectados en el momento, no en el informe."),
        ],
        "itl": [
            ("Testbed de sensores y tecnologías de medición en tiempo real en el ITL", "Muy alto"),
            ("Rol articulador entre operadores, proveedores OT/IT y reguladores, con metodología TRL→IRL", "Muy alto"),
            ("Metodologías y protocolos de gobernanza de datos hídricos estandarizados", "Sí"),
            ("Estándares de interoperabilidad y ciberseguridad OT como referencia regional", "Sí"),
        ],
        "industria": "Empresas mineras, Empresas Agrícolas, Municipalidades, Industrias en general",
        "kpi_que_ya_medimos": "Latencia de decisión · eventos fuera de especificación · eficiencia de recirculación",
    },
    {
        "cod": "M1",
        "titulo": "Optimización de Flotación y Lixiviación para Reducir Residuos e Insumos",
        "macro": "Minería con menos residuos",
        "por_que": "Es el desafío con MENOS competencia y el encaje técnico más subestimado: pide 'sistemas de control en línea' y la estabilidad del control como KPI. Los postulantes van a ser metalurgistas hablando de reactivos.",
        "excluye": "(la ficha no lista exclusiones explícitas; el foco es control y proceso, no obra)",
        "excluye_por_que": "Al no pedir infraestructura nueva, el terreno es la instrumentación y el control: exactamente donde el metalurgista no llega.",
        "piden": [
            "Diseñar sistemas de CONTROL EN LÍNEA para optimizar condiciones operacionales en tiempo real",
            "Validar reactivos selectivos y formulaciones de bajo impacto (los metalurgistas cubren esto)",
            "Pilotos que midan eficiencia técnica, hídrica, energética y ambiental",
            "Lineamientos técnicos y protocolos de operación para adoptar la plataforma en faenas",
        ],
        "kpis": [
            "Mejora en recuperación metalúrgica (%)",
            "Reducción de residuos por tonelada procesada (%)",
            "Reducción de consumo de agua, energía y reactivos (%)",
            "Precisión y ESTABILIDAD del sistema de control en línea (% del tiempo en condiciones óptimas) — el KPI que es nuestro",
        ],
        "ofrecer": [
            ("Analítica de proceso en línea", "El habilitante que el desafío no nombra pero necesita: medir la variable que se quiere controlar (ley, densidad, granulometría, pH) sin esperar al laboratorio."),
            ("Control en línea", "El KPI #4 es literalmente 'precisión y estabilidad del sistema de control'. Se responde con lazo cerrado sobre medición en línea, no con receta fija."),
            ("Control avanzado / APC", "Optimización multivariable de la recuperación. Es la capa donde el proceso mejora sin cambiar el mineral."),
            ("UNS + histórico", "La base para que el control tenga dato confiable y para medir la mejora contra línea base."),
            ("Válvulas de control e instrumentación", "El actuador: sin válvula que responda, no hay control en línea que valga."),
        ],
        "itl": [
            ("Infraestructura para pruebas piloto de flotación y lixiviación optimizada", "—"),
            ("Protocolos de validación y certificación tecnológica en eficiencia metalúrgica", "—"),
            ("Capacidades en integración de control en línea", "—"),
        ],
        "industria": "Minería (cobre y no metálica)",
        "kpi_que_ya_medimos": "Estabilidad y precisión del control en línea · reducción de insumos",
    },
]

SISTEMA = {
    "titulo": "Una arquitectura, tres desafíos",
    "idea": ("A3, A4 y M1 no son tres proyectos: son el MISMO stack aplicado a tres activos distintos. "
             "Sensores → integración OT/IT → capa de datos con histórico (UNS) → analítica → decisión "
             "y control en línea. Cambia el activo (bombas / ciclo del agua / flotación), no la plataforma."),
    "por_que": ("Postular a uno solo es competir en el desafío más poblado. Postular a los tres con la "
                "MISMA arquitectura posiciona a CONECTA como 'el que tiene la capa de integración' — que "
                "es lo que los tres piden y ninguno de los competidores va a traer. El RFI es gratis y "
                "exploratorio: no compromete a tres proyectos, compromete UNA capacidad."),
    "capas": [
        ("1. Sensórica", "Instrumentación de campo + analítica de proceso. Es donde la medición hace la diferencia entre controlar y estimar.",
         "A3 (vibración, caudal, presión) · A4 (calidad de agua) · M1 (ley, densidad, pH)"),
        ("2. Integración OT/IT", "Puente desde el SCADA y los PLC que YA existen (OPC UA / Modbus) hacia un árbol de datos unificado, con ciberseguridad industrial.",
         "A3 y A4 lo piden explícito · M1 lo necesita para el control"),
        ("3. Capa de datos (UNS)", "Un solo árbol de datos con histórico por variable. El KPI de 'latencia de decisión' y el de 'tiempo de respuesta' se responden acá.",
         "Los tres: latencia (A4), tiempo de respuesta (A3), estabilidad (M1)"),
        ("4. Analítica y diagnóstico", "Tendencias, firmas de vibración, detección temprana. El 'prototipo de diagnóstico en tiempo real' que A3 pide.",
         "A3 (cavitación, fugas, desgaste) · A4 (eventos fuera de especificación)"),
        ("5. Decisión y control", "Dashboards georreferenciados, gemelo digital y lazo cerrado.",
         "A4 (dashboards + gemelo) · M1 (control en línea) · A3 (gemelo de impulsión)"),
    ],
    "ventaja": [
        ("La misma inversión sirve tres veces", "La arquitectura se construye una vez y se instancia en tres activos. El esfuerzo de ingeniería no se triplica."),
        ("El asiento en el ecosistema", "El ITL marcó 'Muy alto' querer ser el testbed de sensores y el articulador OT/IT. Ese rol se gana presentando la CAPA COMÚN, no un piloto suelto."),
        ("Menos competencia por diseño", "En A3 y M1 el postulante típico es de proceso/hidráulica. En A4 son integradores. Presentar los tres con la misma plataforma cubre ambos frentes con un solo mensaje."),
        ("El piloto sale de la cartera propia", "La lista de cuentas con decisores mapeados (nombre, cargo, LinkedIn) permite nombrar la faena en el formulario en vez de postular en abstracto."),
    ],
}

RIESGO = [
    ("El TRL 4 exige acreditar TECNOLOGÍA, no servicio",
     "Un 'hacemos integración a medida' se clasifica bajo. El expediente tiene que presentar la capa de "
     "integración como MÉTODO PROPIO con PI (que es como ya se vende: metodología, no producto de tercero). "
     "Si el TRL no se puede acreditar, la postulación no avanza por más que el encaje técnico sea bueno."),
    ("Es un RFI: no adjudica plata",
     "El valor real está en quedar dentro del ecosistema del ITL antes del llamado que sí adjudica. El "
     "primer llamado movió ~US$50M. No invertir semanas de ingeniería en esta fase: pide un formulario."),
    ("La cuenta piloto hay que comprometerla antes de escribir",
     "El formulario pide 'compromisos formales o conversaciones avanzadas'. Hay que definir QUÉ cuenta "
     "concreta se pone como piloto ANTES de redactar, no después."),
    ("El certificado de vigencia tiene vencimiento",
     "90 días de antigüedad máxima. Verificarlo vigente al momento de POSTULAR, no al de redactar."),
]


def chip(v):
    cls = {"si": "ok", "no": "no", "parcial": "mid"}.get(v, "")
    txt = {"si": "POSTULAR", "no": "no", "parcial": "solo con socio"}.get(v, v)
    return f'<span class="chip {cls}">{txt}</span>'


filas_des = "".join(f'''
  <tr class="{esc(d[2])}">
    <td class="cod">{esc(d[0])}</td>
    <td><b>{esc(d[1])}</b></td>
    <td>{chip(d[2])}</td>
    <td class="sub2">{esc(d[3])}<br><span class="gris">{esc(d[4])}</span></td>
  </tr>''' for d in DESAFIOS)

filas_duros = "".join(
    f'<tr><td><b>{esc(k)}</b></td><td class="v">{esc(v)}</td><td class="sub2">{esc(n)}</td></tr>'
    for k, v, n in DUROS)


def bloque_ficha(f):
    piden = "".join(f'<li>{esc(x)}</li>' for x in f["piden"])
    kpis = "".join(f'<li>{esc(x)}</li>' for x in f["kpis"])
    ofrecer = "".join(f'<div class="of"><b>{esc(o[0])}</b><p>{esc(o[1])}</p></div>' for o in f["ofrecer"])
    itl = "".join(f'<tr><td>{esc(i[0])}</td><td class="niv">{esc(i[1])}</td></tr>' for i in f["itl"])
    excl = ""
    if f["excluye"] and not f["excluye"].startswith("(la ficha"):
        excl = f'''
        <div class="dato"><span class="lb">EXCLUYE</span> {esc(f["excluye"])}</div>
        <div class="porq"><b>Por qué importa:</b> {esc(f["excluye_por_que"])}</div>'''
    return f'''
  <div class="ficha">
    <div class="fh"><span class="cod">{esc(f["cod"])}</span>
      <h3>{esc(f["titulo"])}</h3>
      <span class="macro">{esc(f["macro"])}</span></div>
    <p class="py">{esc(f["por_que"])}</p>
    {excl}
    <div class="dato"><span class="lb">INCLUYE</span></div>
    <div class="col2">
      <div><h4>Qué piden</h4><ul>{piden}</ul></div>
      <div><h4>Los KPI de la ficha</h4><ul>{kpis}</ul></div>
    </div>
    <h4>Qué ofrece CONECTA para este desafío</h4>
    <div class="ofs">{ofrecer}</div>
    <h4>Qué quiere el ITL para sí mismo</h4>
    <table class="titl"><tbody>{itl}</tbody></table>
    <div class="pie"><b>Industrias:</b> {esc(f["industria"])} &nbsp;·&nbsp;
      <b>KPI que ya medimos:</b> {esc(f["kpi_que_ya_medimos"])}</div>
  </div>'''


fichas_html = "".join(bloque_ficha(f) for f in FICHAS)

capas = "".join(
    f'<div class="capa"><span class="cn">{esc(c[0])}</span><p>{esc(c[1])}</p>'
    f'<span class="cd">dónde juega: {esc(c[2])}</span></div>' for c in SISTEMA["capas"])

ventajas = "".join(f'<div class="ven"><b>{esc(v[0])}</b><p>{esc(v[1])}</p></div>'
                   for v in SISTEMA["ventaja"])
riesgos = "".join(f'<div class="rie"><b>{esc(r[0])}</b><p>{esc(r[1])}</p></div>' for r in RIESGO)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ITL 2026: postulación por desafío y como sistema</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309;--ro:#b91c1c}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1150px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:950px}}
h2{{font-size:20px;font-weight:660;margin:32px 0 12px;letter-spacing:-.2px}}
h3{{font-size:17px;font-weight:660}}
h4{{font-size:12.5px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);margin:14px 0 7px}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 19px;margin-bottom:13px}}
.datos{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:9px;margin-bottom:16px}}
.dd{{background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--ac);border-radius:10px;padding:10px 14px}}
.dd b{{font-size:11px;color:var(--mu);text-transform:uppercase;letter-spacing:.4px;display:block}}
.dd .v{{font-size:16px;font-weight:700;display:block;margin:2px 0}}
.dd .n{{font-size:11.5px;color:var(--mu)}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px;border-bottom:2px solid var(--bd)}}
td{{padding:8px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.cod{{font-family:ui-monospace,Menlo,monospace;font-weight:700;color:var(--ac);font-size:14px}}
.sub2{{font-size:12.5px;color:#4b5563}}
.gris{{color:var(--mu);font-style:italic}}
.chip{{font-size:10.5px;font-weight:700;border-radius:5px;padding:2px 8px;white-space:nowrap}}
.chip.ok{{background:#f0fdf4;color:#065f46;border:1px solid #bbf7d0}}
.chip.no{{background:#f9fafb;color:#9ca3af;border:1px solid #e5e7eb}}
.chip.mid{{background:#fffbeb;color:#92400e;border:1px solid #fde68a}}
tr.no{{opacity:.55}}
.ficha{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:17px 20px;margin-bottom:14px}}
.fh{{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;padding-bottom:9px;border-bottom:1px solid #f3f4f6;margin-bottom:10px}}
.fh h3{{flex:1}}
.macro{{font-size:11px;background:#f3f4f6;border-radius:5px;padding:2px 9px;color:#374151}}
.py{{font-size:13.5px;color:#1f2937;margin-bottom:11px}}
.dato{{font-size:13.5px;background:#f9fafb;border-radius:8px;padding:9px 13px;margin-bottom:6px}}
.lb{{font-size:10.5px;font-weight:700;letter-spacing:.5px;color:var(--mu);margin-right:7px}}
.porq{{font-size:12.5px;background:#fffbeb;border-left:3px solid var(--am);border-radius:6px;padding:8px 13px;margin-bottom:11px;color:#78350f}}
.porq b{{color:#92400e}}
.col2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.col2 ul{{margin-left:17px}} .col2 li{{font-size:12.5px;margin-bottom:4px}}
.ofs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:9px}}
.of{{background:#f9fafb;border-radius:9px;padding:10px 13px}}
.of b{{font-size:13px;color:#065f46}}
.of p{{font-size:12.5px;color:#374151;margin-top:2px}}
table.titl{{font-size:12.5px}}
.niv{{font-weight:700;color:var(--vd);text-align:right;white-space:nowrap}}
.pie{{font-size:12.5px;color:var(--mu);margin-top:11px;padding-top:9px;border-top:1px solid #f3f4f6}}
.capa{{display:flex;gap:13px;align-items:baseline;background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--vd);border-radius:10px;padding:11px 16px;margin-bottom:7px;flex-wrap:wrap}}
.cn{{font-size:13px;font-weight:700;color:var(--vd);min-width:150px}}
.capa p{{font-size:13px;flex:1;min-width:260px}}
.cd{{font-size:11.5px;color:var(--mu);width:100%;padding-left:163px}}
.ven,.rie{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;margin-bottom:8px}}
.ven b{{font-size:13.5px;color:#065f46}}
.rie b{{font-size:13.5px;color:#92400e}}
.ven p,.rie p{{font-size:12.5px;color:#374151;margin-top:3px}}
.rie{{border-left:4px solid var(--am)}}
.ven{{border-left:4px solid var(--vd)}}
footer{{margin-top:30px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>ITL 2026: la postulación, por desafío y como sistema</h1>
<p class="sub0">Segundo Llamado de Innovación Abierta del <b>Instituto de Tecnologías Limpias</b>
(Antofagasta, Corfo–SQM). Acá está el mapa de los 8 desafíos, la ficha de los tres que le calzan a
CONECTA, y la jugada de presentarlos como <b>una sola arquitectura</b>.</p>

<h2>1. Los datos duros (antes de escribir nada)</h2>
<div class="datos">
  {''.join(f'<div class="dd"><b>{esc(k)}</b><span class="v">{esc(v)}</span><span class="n">{esc(nn)}</span></div>' for k, v, nn in DUROS)}
</div>

<h2>2. Los 8 desafíos: a cuáles sí y a cuáles no</h2>
<div class="card">
  <table><thead><tr><th>#</th><th>Desafío</th><th>Encaje</th><th>Por qué</th></tr></thead>
  <tbody>{filas_des}</tbody></table>
</div>

<h2>3. La jugada de sistema: una arquitectura, tres desafíos</h2>
<div class="card">
  <h3>{esc(SISTEMA["titulo"])}</h3>
  <p class="py" style="margin-top:7px">{esc(SISTEMA["idea"])}</p>
  <p class="porq"><b>Por qué conviene:</b> {esc(SISTEMA["por_que"])}</p>
  <h4>Las 5 capas (las mismas para los tres)</h4>
  {capas}
  <h4>Por qué presentarlo así</h4>
  {ventajas}
</div>

<h2>4. Ficha por desafío</h2>
{fichas_html}

<h2>5. Los riesgos, derecho</h2>
{riesgos}

<footer>
  Fuente: <a href="https://itlchile.com/desafios/">itlchile.com/desafios</a> · las 8 fichas técnicas (PDF) ·
  Bases RFI 2026 (Anexo 1: formulario de 14 secciones).
  Postulación: <code>desafiosdeinnovacionitl.vform.io</code> — cierra el <b>31-jul-2026 23:59</b>.<br>
  Lo que hay que resolver ANTES de escribir: <b>qué cuenta concreta se pone como piloto</b>, y
  <b>cómo se acredita el TRL 4</b> (tecnología propia, no servicio).
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(DESAFIOS)} desafíos mapeados | {len(FICHAS)} fichas | {len(SISTEMA['capas'])} capas")
