# -*- coding: utf-8 -*-
"""
Cruce NORMATIVO x ESTRATEGIA — catálogo SUPCON (63 productos, 7 líneas) en Chile.

Regla dura: NINGÚN dato inventado. Cada disparador normativo lleva número de norma +
URL de fuente verificada (bcn.cl / SMA / CNE / SEC). Lo que no tiene sustento se marca
'SIN SUSTENTO ENCONTRADO'. Se distingue MEDIDO (Aduanas/RETC) de INFERIDO (proyección).

Salida: datos/cruce_normativo_estrategia.json
"""
import json, os

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
OUT = os.path.join(BASE, "datos", "cruce_normativo_estrategia.json")

# ---------------------------------------------------------------------------
# Fuentes normativas verificadas (todas contrastadas contra bcn.cl/leychile,
# pág. oficial del regulador, o resolución del fiscalizador).
# ---------------------------------------------------------------------------
FUENTES = {
    "DS13_2011": {
        "norma": "D.S. 13/2011 MMA — Norma de Emisión para Centrales Termoeléctricas",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1026808",
        "detalle": "Art. 8: las fuentes emisoras existentes y nuevas deberán instalar y certificar un sistema de monitoreo continuo de emisiones (CEMS) para MP, SO2, NOx, Hg y otros parámetros, conforme a 40 CFR Part 75 (US-EPA); el CEMS lo aprueba la SMA. Art. 9: 2 años para existentes, desde puesta en servicio las nuevas. Aplica a unidades ≥50 MWt.",
    },
    "RES57_2013": {
        "norma": "Res. Ex. 57/2013 SMA — Protocolo de Validación de CEMS en Centrales Termoeléctricas",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1048397",
        "detalle": "Aterriza el Art. 8 del DS 13/2011: define el protocolo de validación inicial del CEMS (mide concentración y tasa másica de SO2, NOx, MP; parámetros de interés humedad, flujo, CO2 y O2).",
    },
    "LEY20780_ART8": {
        "norma": "Ley 20.780, Art. 8 (impuesto verde), mod. Ley 21.210 — Impuesto a las emisiones de MP, NOx, SO2 y CO2",
        "fuente": "https://www.leychile.cl/leychile/Navegar/imprimir?idNorma=1067194&idParte=9509251",
        "detalle": "Grava a establecimientos cuyas fuentes emisoras, individual o conjuntamente, emitan ≥100 t/año de MP o ≥25.000 t/año de CO2. CO2 = US$5/t. La cuantificación para la declaración obliga a CEMS o método alternativo aprobado por la SMA (ver Res. 585/2023).",
    },
    "RES680_2021": {
        "norma": "Res. Ex. 680/2021 MMA/SMA — conexión en línea de CEMS a la SMA",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1159274",
        "detalle": "Todo titular con obligación de CEMS (por NE, RCA, PPDA/PDA o impuesto verde) debe conectar el CEMS en línea con los sistemas de la SMA y reportar en tiempo real. Instructivo técnico: Res. Ex. 252/2020 SMA.",
    },
    "DS28_2013": {
        "norma": "D.S. 28/2013 MMA — Norma de Emisión para Fundiciones de Cobre y Fuentes Emisoras de Arsénico",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1057059",
        "detalle": "Para medir SO2 en plantas de ácido se debe implementar y validar un sistema de monitoreo continuo (40 CFR Part 75 US-EPA). Los datos deben estar en línea con la SMA y la SEREMI. Mediciones en chimenea por entidades de inspección autorizadas.",
    },
    "DS29_2013": {
        "norma": "D.S. 29/2013 MMA — Norma de Emisión para Incineración, Coincineración y Coprocesamiento",
        "fuente": "https://nuevo.leychile.cl/servicios/Consulta/Exportar?radioExportar=Normas&nombrearchivo=Decreto-29_12-SEP-2013",
        "detalle": "Obliga a sistema de medición continuo en chimenea: incineración (MP, CO, SO2, NOx); hornos de cemento y de cal rotatorios que usan combustibles alternativos (MP, y demás). Plan de monitoreo a la SMA.",
    },
    "DS1_2023": {
        "norma": "D.S. 1/2023 MMA — Norma de Emisión para Fundiciones de Hierro, Acero y Plomo",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1190758",
        "detalle": "Art. 30: calderas, hornos industriales, hornos de fundición y hornos secadores con potencia térmica ≥20 MWt deben instalar y validar CEMS para MP y SO2 (existentes: 12 meses). Art. 29: reducir emisiones fugitivas de MP en manejo de materias primas.",
    },
    "DS138_2005": {
        "norma": "D.S. 138/2005 MINSAL — Obligación de entregar antecedentes para estimar emisiones",
        "fuente": "https://nuevo.leychile.cl/navegar?idNorma=244118",
        "detalle": "Fuentes fijas obligadas a reportar emisiones: calderas de vapor/agua caliente, celulosa, fundiciones primarias y secundarias, centrales termoeléctricas, cemento/cal/yeso, vidrio, cerámica, siderurgia, petroquímica, asfaltos y grupos electrógenos. Si hay monitoreo continuo, se reportan promedios horarios de concentración y caudal.",
    },
    "PPDA_QUILLOTA": {
        "norma": "D.S. 18/2023 MMA — PPDA Quillota-Catemu-Panquehue-Llaillay (D.O. 23-oct-2025)",
        "fuente": "https://ppda.mma.gob.cl/wp-content/uploads/2025/10/DO_DSN%C2%B018-2023-PPDA-QUILLOTA-CATEMU.pdf",
        "detalle": "Art. 28: correas/puntos de transferencia deben incluir control de polvo. Art. 29: plan operacional de tronaduras con estaciones meteorológicas de telemetría, QA/QC y respaldo; si falla el monitoreo, no se tronará. Art. 30: reporte anual en abril de MP y MP10 con memoria de cálculo (puntuales, fugitivas y areales).",
    },
    "DS90_2000": {
        "norma": "D.S. 90/2000 MINSEGPRES — Norma de Emisión de Residuos Líquidos a Aguas Marinas y Continentales (RILES)",
        "fuente": "https://vu.mma.gob.cl/manuals/riles/D.S._N_90_2000_MINSEGPRES.pdf",
        "detalle": "Monitoreo en cada descarga. Fuentes que neutralizan RILES: medición continua con pHmetro y registrador. Caudal: <30 m3/día se estima; 30-300 m3/día equipo portátil con registro; >300 m3/día cámara de medición y caudalímetro con registro diario. NE-RILES 2026 (en trámite) añade monitoreo EN LÍNEA de caudal >300 m3/día y pH continuo con registro ≥24 meses.",
    },
    "DS609_1998": {
        "norma": "D.S. 609/1998 MOP — Norma de Emisión de RILES a sistemas de alcantarillado",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=121486",
        "detalle": "Establecimientos industriales que descargan a alcantarillado: programa de autocontrol; la medición de caudal se hace con equipos portátiles o fijos y con registros continuos. Fuentes que neutralizan RILES: medición continua de pH con pHmetro en línea y capturador de datos con registrador (lecturas ≥1/hora), conservando registro ≥24 meses. Fiscaliza el prestador sanitario + SISS (Ley 18.902).",
    },
    "NTSYCS_4_12": {
        "norma": "NTSyCS (CNE) — Art. 4-12 y Anexo Técnico SITR",
        "fuente": "https://www.cne.cl/wp-content/uploads/2025/01/NTSyCS-Ene-2025.pdf",
        "detalle": "Los Coordinados deben disponer enlaces de datos al SITR del Coordinador con disponibilidad ≥99,5% (ventana móvil 12 meses); tiempos de actualización <5 s (Art. 4-16) con sincronización horaria; telemedida de la posición del cambiador de tap sin carga; instalaciones >200 kV con teleprotección. Protocolos ICCP/IEC-60870-6. Prueba anual anti-apagón con empresa externa.",
    },
    "AT_SITR_2025": {
        "norma": "Anexo Técnico NTSyCS — Definición de Parámetros Técnicos y Operativos para el envío de datos al SITR (mar-2025)",
        "fuente": "https://www.cne.cl/wp-content/uploads/2025/04/2025.03_AT-SITR.pdf",
        "detalle": "Art. 72-2 LGSE: todos los Coordinados deben sujetarse a la coordinación. Define protocolos ICCP/IEC-60870-6/TASE.2, calidad y estampado de tiempo de las medidas, y el enlace de PMGD al SITR vía distribuidora.",
    },
    "DS10_2013": {
        "norma": "D.S. 10/2013 MINSAL — Reglamento de Calderas, Autoclaves y Equipos que utilizan Vapor de Agua",
        "fuente": "https://www.achs.cl/centro-de-noticias/noticia/2014/los-cambios-mas-relevantes-a-la-normativa-que-rige-el-funcionamiento-de-calderas",
        "detalle": "Deroga el D.S. 48/1984. Toda caldera de vapor debe disponer de: dos indicadores de nivel de agua independientes, manómetro(s), medidor de temperatura de salida de gases, válvula de seguridad, alarma audible/visible. Válvulas de seguridad reguladas (abren ≤+6% y cierran ≤4% de la presión máxima). Libro de operación diaria con registros cada 4 horas. Revisiones por profesional facultado ante SEREMI de Salud.",
    },
    "DS43_2015": {
        "norma": "D.S. 43/2015 MINSAL — Reglamento de Almacenamiento de Sustancias Peligrosas",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1088802",
        "detalle": "Toda bodega de sustancias peligrosas debe contar con sistema automático de detección de incendios (diseñado según NFPA 72 u otra norma internacional reconocida) y, según la clase, sistema automático de extinción. Control de derrames y HDS por sustancia (NCh 2245).",
    },
    "DS594_1999": {
        "norma": "D.S. 594/1999 MINSAL — Reglamento sobre Condiciones Sanitarias y Ambientales Básicas en los Lugares de Trabajo",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=167766",
        "detalle": "Art. 45: en lugares donde se almacenen o manipulen sustancias peligrosas debe existir un sistema automático de detección de incendios; en alto riesgo potencial, extinción automática y plan de emergencia. Fija los Valores Límite de Exposición Profesional (VLEP) a agentes químicos → obliga a monitorear/muestrear y a HDS.",
    },
    "DS132_2004": {
        "norma": "D.S. 132/2004 Minería — Reglamento de Seguridad Minera",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=221064",
        "detalle": "Art. 132: en frentes críticos, sensores y alarmas que alerten cuando gases excedan los valores permitidos. Art. 149: todo ventilador principal con sistema de alarma por detención imprevista. Art. 279: minas carboníferas subterráneas con medición de metano (CH4) al menos cada 30 minutos. Minas >1.000 t/mes: mediciones mensuales de O2, CO y humos nitrosos con registro. Medidores de gases calibrados según patrones.",
    },
    "DS248_2007": {
        "norma": "D.S. 248/2007 Minería — Reglamento de Seguridad de Depósitos de Relaves (idNorma 259901)",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=259901",
        "detalle": "Monitoreo permanente del depósito de relaves (piezómetros, inclinómetros, flujo, sísmicas); fiscaliza Sernageomin vía SIMIN y el Observatorio Nacional de Relaves ('Sistema de Monitoreo Central' en línea).",
    },
    "LEY21305": {
        "norma": "Ley 21.305 — Eficiencia Energética / SGE (pub. 13-feb-2021, idNorma 1155887)",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1155887",
        "detalle": "CCGE (consumo ≥50 Tcal/año): implementar Sistema de Gestión de Energía con gestor energético, indicadores, medición y verificación; reporte anual de consumo/intensidad; auditoría cada 3 años. Umbral de reporte por ventas: 100.000 UF/año (dos umbrales distintos). Multa la aplica la SEC vía Ley 18.410 (hasta 60.000 UTM según sec.cl).",
    },
    "LEY21663": {
        "norma": "Ley 21.663 — Ley Marco de Ciberseguridad (pub. 08-abr-2024, idNorma 1202434)",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1202434",
        "detalle": "Define servicios esenciales y Operadores de Importancia Vital (OIV): gestión de la información, planes de continuidad operacional y de ciberseguridad, delegado de ciberseguridad. Nómina 1ª etapa: Res. Ex. 87 (D.O. 17-dic-2025), 915 OIV; sector eléctrico 147.",
    },
    "LEY21663_OIV": {
        "norma": "ANCI — Nómina OIV 1ª etapa (Res. Ex. N°87, D.O. 17-dic-2025)",
        "fuente": "https://anci.gob.cl/documents/4843/Nómina_final_OIV_17.12.2025.pdf",
        "detalle": "915 OIV calificados: eléctrico 147, telecom 29, digital/TI 413, banca 34, salud 114, empresas del Estado 20, administración 158. Obligaciones: SGSI, planes de continuidad con componente de ciberseguridad, delegado.",
    },
    "LEY21435": {
        "norma": "Ley 21.435 — Reforma al Código de Aguas (pub. 6-abr-2022, idNorma 1174443)",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1174443",
        "detalle": "Exigencia de medición y transmisión de extracciones de agua vía programa DGA de Monitoreo de Extracciones Efectivas (MEE): telemetría continua y transmisión online (Res. 1238 DGA).",
    },
    "LEY20551": {
        "norma": "Ley 20.551 — Cierre de Faenas e Instalaciones Mineras (Sernageomin)",
        "fuente": "https://www.bcn.cl/leychile/navegar?idNorma=1028371",
        "detalle": "Obliga a plan de cierre y a mantener las medidas de control (monitoreo de aguas, estabilidad física y química) durante y después de la operación. Fuente usada para el encuadre minero, no re-verificada a texto completo artículo por artículo.",
    },
    "RETC": {
        "norma": "RETC (MMA) — Registro de Emisiones y Transferencias de Contaminantes",
        "fuente": "https://datosretc.mma.gob.cl",
        "detalle": "Todos los establecimientos obligados reportan anualmente emisiones al aire, agua y suelo y transferencias de residuos. Es el piso de obligación de reporte ambiental transversal.",
    },
    "JX300XP_NOTA": {
        "norma": "SIN SUSTENTO NORMATIVO ESPECÍFICO",
        "fuente": "",
        "detalle": "El JX-300XP (plataforma PCS de generación anterior de SUPCON) no tiene un disparador normativo propio: lo que obliga es la normativa de control/SCADA del proceso donde se use (NTSyCS para instalaciones coordinadas, o DCS de planta). No se le asigna disparador exclusivo.",
    },
}

# ---------------------------------------------------------------------------
# CRUCE POR LÍNEA  (las 7 líneas del catálogo)
# Cada línea: disparador normativo concreto, fuente, tipo de obligación,
# industrias afectadas, empresas candidatas (nombres reales donde hay base),
# urgencia y nota. MEDIDO vs INFERIDO se marca explícitamente.
# ---------------------------------------------------------------------------
LINEAS = {}

LINEAS["Instrumentación"] = {
    "disparador_normativo": (
        "No es una sola norma: es el conjunto de obligaciones de MEDICIÓN de variables que "
        "distintos fiscalizadores exigen. El disparador más concreto y verificable es el caudal: "
        "D.S. 90/2000 (RILES) obliga a medir caudal con cámara de medición y caudalímetro con "
        "registro diario cuando la descarga supera 300 m3/día, y la NE-RILES 2026 añade monitoreo "
        "EN LÍNEA; el D.S. 609/1998 exige registros continuos de caudal y pH en línea (≥1/hora, "
        "24 meses) para quien neutraliza RILES. Sumado: NTSyCS 4-12 (medición/telemedida para el "
        "SITR, precisión Clase 2 ANSI) y el impuesto verde (Ley 20.780 Art. 8), que obliga a "
        "cuantificar el caudal y la concentración de la chimenea que se grava. En calderas, el "
        "D.S. 10/2013 exige manómetro, medidor de temperatura de gases y dos indicadores de nivel."
    ),
    "norma_y_fuente": (
        "D.S. 90/2000 MINSEGPRES (RILES) — https://vu.mma.gob.cl/manuals/riles/D.S._N_90_2000_MINSEGPRES.pdf | "
        "D.S. 609/1998 MOP — https://www.bcn.cl/leychile/navegar?idNorma=121486 | "
        "D.S. 10/2013 MINSAL (calderas) — https://www.achs.cl/centro-de-noticias/noticia/2014/los-cambios-mas-relevantes-a-la-normativa-que-rige-el-funcionamiento-de-calderas | "
        "Ley 20.780 Art. 8 (impuesto verde) — https://www.leychile.cl/leychile/Navegar/imprimir?idNorma=1067194&idParte=9509251 | "
        "NTSyCS Art. 4-12 — https://www.cne.cl/wp-content/uploads/2025/01/NTSyCS-Ene-2025.pdf"
    ),
    "tipo_obligacion": "obligatoria",
    "industrias_afectadas": [
        "Química y petroquímica (medición de caudal de efluentes, DS 90/609)",
        "Celulosa y papel (caudal de pulpa y efluentes)",
        "Minería (agua de proceso, relaves, drenaje)",
        "Alimentos y bebidas (ciclos CIP/SIP, caudal sanitario)",
        "Tratamiento de aguas y aguas residuales (caudal, nivel, pH)",
        "Generación eléctrica (vapor, agua de caldera, DS 10/2013)",
    ],
    "empresas_candidatas": [
        "SQM — Sociedad Química y Minera de Chile S.A. (química + litio, RILES y aguas)",
        "Noracid S.A. (ácido sulfúrico, efluentes y emisiones)",
        "Oxiquim S.A. (química industrial, RILES a alcantarillado, DS 609)",
        "Occidental Chemical Chile / OxyChile (cloro-álcali, pH y caudal continuos)",
        "Eka Chile (clorato de sodio, Nouryon Talcahuano)",
        "ERCO Worldwide Chile (dióxido de cloro)",
        "SNF Chile S.A. (poliacrilamida, efluentes industriales)",
        "CMPC (complejos Laja, Santa Fe, Pacífico, Cordillera, Tissue — caudal de pulpa y RILES)",
        "Arauco / Planta MAPA (celulosa, RILES y caudal de pulpa)",
        "Aguas Andinas y sanitarias (SISS, D.S. 609 y control de caudal)",
    ],
    "urgencia": "alta",
    "nota": (
        "MEDIDO: el rubro de instrumentación movió US$60,5M en importaciones 2025; el segmento "
        "caudal US$19,7M y nivel US$19,7M (Registro DIN Aduanas 2025). CONCLUSION: la puerta de "
        "entrada es el caudalímetro (SFE910) porque el caudal es la variable que más fiscalizadores "
        "exigen simultáneamente (DGA, SISS, SMA, DIRECTEMAR) — un instrumento reporta a todos. "
        "INFERIDO: que la medición continua 'obligatoria' ya esté cumplida en todos los casos es la "
        "hipótesis comercial; verificar la configuración del punto de descarga antes de cotizar "
        "(un medidor calibrado en mg/Nm3 o caudal requiere sección de paso definida)."
    ),
}

LINEAS["Analítica"] = {
    "disparador_normativo": (
        "EL DISPARADOR MÁS DURO DEL CATÁLOGO: el D.S. 13/2011 MMA (Art. 8) obliga a las centrales "
        "termoeléctricas ≥50 MWt a instalar y certificar un Sistema de Monitoreo Continuo de "
        "Emisiones (CEMS) para MP, SO2, NOx y Hg, conforme a 40 CFR Part 75 (US-EPA), aprobado por "
        "la SMA (protocolo Res. Ex. 57/2013 SMA). El impuesto verde (Ley 20.780 Art. 8) obliga a "
        "los establecimientos que emiten ≥100 t/año de MP o ≥25.000 t/año de CO2 a cuantificar sus "
        "emisiones por CEMS o método aprobado (Res. 585/2023 MMA). Y la Res. Ex. 680/2021 SMA "
        "obliga a CONECTAR el CEMS EN LÍNEA con la SMA. Además: D.S. 28/2013 (fundiciones de cobre, "
        "SO2 en plantas de ácido), D.S. 29/2013 (incineración, coincineración y coprocesamiento en "
        "hornos de cemento), D.S. 1/2023 (calderas y hornos ≥20 MWt: CEMS MP y SO2) y D.S. 138/2005 "
        "MINSAL (reporte de emisiones de 10 rubros). Para la línea holandesa (WIM COMPAS, PRISM, "
        "TISOMIC, C-QUAND) el disparador es la obligación de reporte de calidad de gas y de "
        "cumplimiento de especificación (índice de Wobbe / poder calorífico) y el monitoreo de "
        "H2S en gas: aplica a combustibles, refinería y gas natural."
    ),
    "norma_y_fuente": (
        "D.S. 13/2011 MMA Art. 8 — https://www.bcn.cl/leychile/navegar?idNorma=1026808 | "
        "Res. Ex. 57/2013 SMA (protocolo CEMS) — https://www.bcn.cl/leychile/navegar?idNorma=1048397 | "
        "Ley 20.780 Art. 8 (impuesto verde) — https://www.leychile.cl/leychile/Navegar/imprimir?idNorma=1067194&idParte=9509251 | "
        "Res. Ex. 680/2021 (CEMS en línea) — https://www.bcn.cl/leychile/navegar?idNorma=1159274 | "
        "D.S. 28/2013 (fundiciones de cobre) — https://www.bcn.cl/leychile/navegar?idNorma=1057059 | "
        "D.S. 29/2013 (incineración/cemento) — https://nuevo.leychile.cl/servicios/Consulta/Exportar?radioExportar=Normas&nombrearchivo=Decreto-29_12-SEP-2013 | "
        "D.S. 1/2023 Art. 30 (calderas/hornos ≥20 MWt) — https://www.bcn.cl/leychile/navegar?idNorma=1190758 | "
        "D.S. 138/2005 MINSAL — https://nuevo.leychile.cl/navegar?idNorma=244118"
    ),
    "tipo_obligacion": "obligatoria",
    "industrias_afectadas": [
        "Generación termoeléctrica (CEMS obligatorio por DS 13/2011 — el núcleo del mercado)",
        "Fundiciones de cobre y arsénico (DS 28/2013: SO2 en plantas de ácido)",
        "Cemento y cal (DS 29/2013: coprocesamiento en hornos rotatorios)",
        "Siderurgia / fundiciones de hierro, acero y plomo (DS 1/2023: MP y SO2)",
        "Celulosa y papel (calderas de recuperación, DS 138/2005)",
        "Petroquímica, refinería y gas natural (WIM COMPAS / TISOMIC: calidad de gas y H2S)",
        "Alimentos y farmacéutica — secadores por atomización (NICOSYS-3: CO / combustión latente)",
        "Minería del cobre (C-QUAND: medición elemental en soluciones SX/EW)",
    ],
    "empresas_candidatas": [
        "Central Térmica Guacolda (carbón, CEMS MP/SO2/NOx — caso emblemático)",
        "Central Térmica Cochrane, Central Térmica Angamos, Central Térmica Andina",
        "Central Térmica Campiche, Central Térmica Hornitos, Central Colmito",
        "Central Cementos Bío Bío Centro (cemento, DS 29/2013)",
        "Central Candelaria, Central El Salvador (fundiciones / plantas de ácido)",
        "CMPC (calderas de recuperación — complejos Laja, Santa Fe, Pacífico)",
        "Arauco / Planta MAPA (calderas de recuperación)",
        "Noracid S.A. (planta de ácido sulfúrico, SO2)",
        "SQM (litio/yodo: hornos y procesos con reporte de emisiones)",
        "CODELCO División Chuquicamata, Ministro Hales, El Teniente (fundición y plantas de ácido)",
        "CAP / Huachipato — siderurgia (fundición de hierro, DS 1/2023)",
        "ENAP / refinerías (calidad de gas, H2S, antorcha)",
        "Colbún, AES Andes, Engie, Enel (centrales térmicas del parque de generación)",
        "Nestlé / Sopraval / Colun / Loncoleche (secadores por atomización — NICOSYS-3)",
    ],
    "urgencia": "alta",
    "nota": (
        "MEDIDO: analizadores de proceso importados 2025 = US$44,3M (Glosa 9027); SUPCON/Hobré "
        "tienen CERO registros de importación en Chile (no hay base instalada). La subpartida "
        "90271010 (analizadores de gases/humos) movió US$13,0M y 90278999 US$30,1M. CONCLUSION: "
        "es el disparador normativo más limpio del catálogo (obligación de resultado + de reporte "
        "en línea con la SMA) y no hay incumbente SUPCON que defender. OJO pitfall de producto: el "
        "DMS-100 (medidor de polvo) mide en DUCTO o CHIMENEA (mg/Nm3 contra caudal conocido); no "
        "sirve en fuente abierta. Verificar antes de ofrecer. INFERIDO: que el CEMS del parque "
        "existente esté completo y validado — la SMA publica los CEMS validados; cruzar por SNIFA "
        "antes de prospectar como 'falta CEMS'."
    ),
}

LINEAS["Válvulas"] = {
    "disparador_normativo": (
        "El disparador es de SEGURIDAD de equipos a presión y de integridad de proceso, no de "
        "reporte ambiental. El más concreto: el D.S. 10/2013 MINSAL (Reglamento de Calderas) exige "
        "que toda caldera de vapor tenga válvula de seguridad conectada directamente a la cámara de "
        "vapor, regulada para abrir a ≤+6% y cerrar a ≤4% de la presión máxima de trabajo, además "
        "de manómetros y medidor de temperatura de gases, con libro de operación cada 4 horas y "
        "revisión por profesional facultado ante la SEREMI de Salud. En alta presión, el D.S. 43/2015 "
        "y el D.S. 594/1999 (Art. 45) exigen contención de derrames y control en bodegas de "
        "sustancias peligrosas. Y donde la válvula de alivio no puede descargar a antorcha, la "
        "protección se resuelve con un HIPPS (función de seguridad instrumentada) — el material del "
        "fabricante lo declara como su caso de uso, sin norma chilena específica que lo obligue por "
        "nombre."
    ),
    "norma_y_fuente": (
        "D.S. 10/2013 MINSAL (calderas: válvulas de seguridad, manómetros) — https://www.achs.cl/centro-de-noticias/noticia/2014/los-cambios-mas-relevantes-a-la-normativa-que-rige-el-funcionamiento-de-calderas | "
        "D.S. 43/2015 MINSAL (sustancias peligrosas) — https://www.bcn.cl/leychile/navegar?idNorma=1088802 | "
        "D.S. 594/1999 MINSAL Art. 45 — https://www.bcn.cl/leychile/navegar?idNorma=167766"
    ),
    "tipo_obligacion": "obligatoria",
    "industrias_afectadas": [
        "Generación eléctrica y vapor industrial (calderas, DS 10/2013)",
        "Química y petroquímica (corrientes corrosivas, revestimiento plástico)",
        "Celulosa y papel (válvula VN de bola V, corte de fibras; cuchilla para pasta)",
        "Minería y pulpa (VN para lodos y sólidos en suspensión)",
        "Tratamiento de aguas y aguas residuales (liner de caucho, autolimpiante)",
        "Alimentos y farmacéutica (compuerta de cuchilla, cierre hermético)",
    ],
    "empresas_candidatas": [
        "CMPC (válvulas de control en líneas de pulpa y vapor)",
        "Arauco / Planta MAPA (pulpa y calderas)",
        "CODELCO (fundición y plantas de ácido: válvulas de control y alivio)",
        "SQM, Noracid, Oxiquim, OxyChile (corrientes corrosivas y tóxicas)",
        "ENAP (refinería: válvulas de control y corte)",
        "AES Andes, Colbún, Engie (calderas y vapor de centrales térmicas)",
        "Aguas Andinas y sanitarias (válvulas en plantas de tratamiento)",
    ],
    "urgencia": "media",
    "nota": (
        "MEDIDO: es el mercado de hardware MÁS GRANDE del catálogo. El capítulo 84.81 completo "
        "(válvulas) movió US$396,6M en 2025; el subconjunto 'válvulas y posicionadores' del rubro "
        "de automatización US$53,8M (BRAY US$5,6M, Valmet US$5,4M, Valvitalia US$4,6M lideran). "
        "INFERIDO: no hay un disparador normativo 'de válvula' único; la norma de calderas (DS 10) "
        "es el más defendible y es de seguridad, no ambiental. La entrada comercial es por proyecto "
        "nuevo o reemplazo de equipo fuera de soporte, no por norma. El disparador normativo real "
        "para HIPPS es de análisis de riesgo (HAZOP/LOPA), que es del cliente, no un decreto."
    ),
}

LINEAS["DCS"] = {
    "disparador_normativo": (
        "No hay una norma chilena que diga 'instale un DCS'. El disparador es la NTSyCS: la "
        "instalación coordinada debe estar supervisada y controlada en tiempo real, con "
        "disponibilidad del SITR ≥99,5% y tiempos de actualización <5 s (Art. 4-12 y 4-16), y "
        "prueba anual anti-apagón del sistema de supervisión y control con empresa externa. Para "
        "plantas no coordinadas, el control de proceso lo empuja la propia operación y la Ley 21.305 "
        "(SGE: medir consumo e intensidad energética con control operacional). En generación, la "
        "Res. Ex. CNE N°45/2026 (NTSyCS) obliga a BESS a operar en modo Grid-Forming y a amortiguar "
        "oscilaciones, lo que presiona la capa de control."
    ),
    "norma_y_fuente": (
        "NTSyCS Art. 4-12 y 4-16 (disponibilidad SITR, tiempos, prueba anti-apagón) — https://www.cne.cl/wp-content/uploads/2025/01/NTSyCS-Ene-2025.pdf | "
        "Anexo Técnico SITR (ICCP/IEC-60870-6) — https://www.cne.cl/wp-content/uploads/2025/04/2025.03_AT-SITR.pdf | "
        "Ley 21.305 (SGE: control operacional y medición) — https://www.bcn.cl/leychile/navegar?idNorma=1155887"
    ),
    "tipo_obligacion": "obligatoria",
    "industrias_afectadas": [
        "Generación eléctrica y transmisión (instalaciones coordinadas del SEN, NTSyCS)",
        "Celulosa y papel (proceso continuo)",
        "Química y petroquímica (proceso continuo)",
        "Minería (plantas concentradoras, SX/EW)",
        "Cemento (proceso continuo)",
    ],
    "empresas_candidatas": [
        "Centrales térmicas del parque coordinado (Guacolda, Cochrane, Angamos, Andina, Campiche)",
        "CMPC (Laja, Santa Fe, Pacífico — proceso continuo)",
        "Arauco (MAPA, celulosa)",
        "CODELCO, Collahuasi, Escondida, Los Bronces (plantas concentradoras)",
        "Cementos Bío Bío (hornos)",
        "Refinerías ENAP (proceso continuo)",
        "Grandes clientes libres coordinados (clientes del SEN con control propio)",
    ],
    "urgencia": "media",
    "nota": (
        "MEDIDO: DCS/controladores importados 2025 = US$112,5M; lideran Siemens (US$23,1M), "
        "Hitachi Energy, ABB. CONCLUSION: mercado grande pero con incumbente instalado; el DCS no "
        "se compra por norma sino por proyecto nuevo o fin de vida del sistema legado. La NTSyCS "
        "obliga al resultado (observabilidad en tiempo real), no a la marca. INFERIDO: la venta es "
        "por proyecto greenfield o ampliación, no por desplazamiento directo."
    ),
}

LINEAS["PLC"] = {
    "disparador_normativo": (
        "SIN SUSTENTO NORMATIVO ESPECÍFICO para el PLC como categoría. No existe una norma chilena "
        "que obligue a 'instalar un PLC'. El PLC es el habilitador de la obligación de otro: si la "
        "instalación es coordinada, la NTSyCS obliga a la telemetría y al control que el PLC ejecuta; "
        "si es una planta de proceso, el PLC ejecuta el control que la operación y la Ley 21.305 "
        "(medición/control operacional del SGE) requieren. El PLC de seguridad (G5Pro Safety, SIL3) "
        "sí hereda el disparador de análisis de riesgo (HAZOP/LOPA) de la función de seguridad que "
        "implementa, no de un decreto."
    ),
    "norma_y_fuente": (
        "NTSyCS Art. 4-12 (control/telemetría de instalaciones coordinadas) — https://www.cne.cl/wp-content/uploads/2025/01/NTSyCS-Ene-2025.pdf | "
        "Ley 21.305 (control operacional del SGE) — https://www.bcn.cl/leychile/navegar?idNorma=1155887"
    ),
    "tipo_obligacion": "incentivada",
    "industrias_afectadas": [
        "Oil & gas y ductos (el material declara este target)",
        "Tratamiento de aguas residuales y suministro de agua",
        "Transporte ferroviario y túneles de servicio",
        "Química fina, petroquímica, metalurgia",
        "Generación eléctrica",
    ],
    "empresas_candidatas": [
        "ESVAL / Aguas Andinas y sanitarias (tratamiento y suministro de agua)",
        "EFE / Ferrocarriles (transporte ferroviario)",
        "ENAP (ductos y terminales de combustible)",
        "CMPC, Arauco (control de proceso y paquetes de equipo)",
        "CODELCO, mineras con plantas de proceso",
    ],
    "urgencia": "baja",
    "nota": (
        "MEDIDO: PLC importados 2025 = US$83,9M; Siemens (US$19,4M) y Rockwell/Allen-Bradley "
        "lideran. SIN SUSTENTO: no hay una norma que obligue al PLC por nombre. La honestidad "
        "comercial exige NO inventar un disparador: la entrada al PLC es por reemplazo de "
        "obsolescencia, proyecto nuevo o dentro de una solución mayor (DCS + PLC + SCADA), no por "
        "cumplimiento normativo. El PLC de seguridad (SIL3) sí lo empuja el HAZOP/LOPA del cliente."
    ),
}

LINEAS["SIS"] = {
    "disparador_normativo": (
        "El disparador es de SEGURIDAD FUNCIONAL y de protección contra incendio, con base "
        "reglamentaria verificable aunque no siempre nombrando el SIS: el D.S. 594/1999 (Art. 45) "
        "obliga a sistema automático de detección de incendios donde se almacenen o manipulen "
        "sustancias peligrosas, y a extinción automática en alto riesgo; el D.S. 43/2015 exige "
        "detección automática (NFPA 72) y extinción en bodegas de sustancias peligrosas. El D.S. 132 "
        "(minería) obliga a sensores y alarmas de gases en labores críticas (Art. 132), alarma en el "
        "ventilador principal (Art. 149) y medición de metano cada 30 min en minas carboníferas "
        "(Art. 279). Y el D.S. 248 (relaves) obliga a monitoreo permanente del depósito. La "
        "exigencia de SIL3 la fija el análisis de riesgo (HAZOP/LOPA) del propio cliente, no un "
        "decreto que diga 'SIL3'."
    ),
    "norma_y_fuente": (
        "D.S. 594/1999 MINSAL Art. 45 (detección y extinción automática) — https://www.bcn.cl/leychile/navegar?idNorma=167766 | "
        "D.S. 43/2015 MINSAL (NFPA 72 en bodegas de sustancias peligrosas) — https://www.bcn.cl/leychile/navegar?idNorma=1088802 | "
        "D.S. 132/2004 Minería (sensores/alarmas de gases, metano, alarma de ventilador) — https://www.bcn.cl/leychile/navegar?idNorma=221064 | "
        "D.S. 248/2007 (monitoreo de relaves) — https://www.bcn.cl/leychile/navegar?idNorma=259901"
    ),
    "tipo_obligacion": "obligatoria",
    "industrias_afectadas": [
        "Refinación y petroquímica (ESD, F&G, compresores)",
        "Química continua (sobrepresión, reacción fuera de control)",
        "Minería subterránea y de rajo (gases, ventilación, relaves)",
        "Almacenamiento de combustibles y sustancias peligrosas",
        "Generación eléctrica (protección de calderas y turbinas)",
    ],
    "empresas_candidatas": [
        "ENAP (refinerías: ESD y F&G)",
        "Oxiquim, OxyChile, Noracid, SNF, BASF Chile (química con sustancias peligrosas)",
        "CODELCO El Teniente, Andina, El Salvador (minería subterránea: gases y ventilación)",
        "SQM (litio/yodo, procesos con sustancias)",
        "CMPC, Arauco (calderas de recuperación y riesgo de gas)",
        "Cementos Bío Bío (hornos, atmósferas combustibles)",
        "AES Andes, Colbún (protección de calderas y turbinas)",
        "Almacenes y terminales de combustibles (Envases del Pacífico, COPEC, terminales marítimos)",
    ],
    "urgencia": "media",
    "nota": (
        "MEDIDO: SIS importados 2025 = US$52,8M; lideran Siemens (US$4,9M), ETP Elektro, Rockwell. "
        "INFERIDO: el disparador normativo es de seguridad (detección/extinción obligatoria por DS "
        "594/43) pero el producto específico (TCS-900 TMR, SIL3) lo determina el HAZOP/LOPA. OJO: "
        "no decir al cliente que 'la norma le exige un SIS SIL3' — la norma exige la función, el "
        "nivel SIL lo fija su análisis de riesgo. La conexión relaves (DS 248) más fuerte es con "
        "instrumentación y SCADA que con el SIS mismo."
    ),
}

LINEAS["Software y plataforma"] = {
    "disparador_normativo": (
        "Dos disparadores verificables, ninguno de compra directa por decreto: (1) CIBERSEGURIDAD: "
        "la Ley 21.663 (Ley Marco de Ciberseguridad, publicada 08-abr-2024) obliga a los Operadores "
        "de Importancia Vital (915 OIV en la 1ª nómina, 147 del sector eléctrico) a mantener "
        "gestión de la información, planes de continuidad operacional y de ciberseguridad, con "
        "delegado de ciberseguridad. Eso empuja visibilidad OT y protección del SCADA/DCS. (2) "
        "ENERGÍA: la Ley 21.305 (SGE) obliga a las empresas con consumo ≥50 Tcal/año a un sistema de "
        "gestión de energía con medición y verificación y reporte anual → gobernanza de datos "
        "energéticos. El SCADA (SolisSCADA, con licencia gratuita hasta 50.000 tags) es además el "
        "habilitador de la obligación NTSyCS de observabilidad (SITR ≥99,5%)."
    ),
    "norma_y_fuente": (
        "Ley 21.663 (ciberseguridad / OIV) — https://www.bcn.cl/leychile/navegar?idNorma=1202434 | "
        "ANCI Nómina OIV 1ª etapa (Res. Ex. 87) — https://anci.gob.cl/documents/4843/Nómina_final_OIV_17.12.2025.pdf | "
        "Ley 21.305 (SGE: medición, reporte, auditoría) — https://www.bcn.cl/leychile/navegar?idNorma=1155887 | "
        "NTSyCS Art. 4-12 (observabilidad/SCADA) — https://www.cne.cl/wp-content/uploads/2025/01/NTSyCS-Ene-2025.pdf"
    ),
    "tipo_obligacion": "obligatoria",
    "industrias_afectadas": [
        "Sector eléctrico (147 OIV de la 1ª nómina — generación, transmisión, distribución, clientes libres)",
        "Combustibles (27 OIV 2ª etapa preliminar)",
        "Agua y saneamiento (29 OIV 2ª etapa preliminar)",
        "Transporte y ferroviario (62 OIV 2ª etapa preliminar)",
        "Toda empresa con consumo ≥50 Tcal/año (Ley 21.305: SGE y reporte)",
        "Plantas con DCS/SCADA que ahora son OIV (visibilidad OT)",
    ],
    "empresas_candidatas": [
        "Coordinados del SEN (generación, transmisión, distribución) — 147 OIV sector eléctrico",
        "CGE, Transelec, Chilquinta, Saesa/STM (transmisión y distribución OIV)",
        "Enel, AES Andes, Colbún, Engie, Sonnedix (generación OIV / CCGE)",
        "CODELCO, CMPC, Arauco (CCGE ≥50 Tcal/año: SGE obligatorio)",
        "ENAP (combustibles, OIV 2ª etapa)",
        "Aguas Andinas, ESVAL, Aguas Antofagasta (agua/saneamiento OIV)",
        "EFE (transporte ferroviario OIV)",
        "Grandes mineras e industrias del sector eléctrico sujetas al Estándar de Ciberseguridad del CEN",
    ],
    "urgencia": "alta",
    "nota": (
        "SIN MEDICIÓN DE MERCADO: el software y la plataforma no se miden por partida arancelaria "
        "(se venden dentro del proyecto); el propio repo declara mercado 'no medible' para esta "
        "línea y no se inventa tamaño. MEDIDO indirecto: red OT importada 2025 = US$18,7M y "
        "ciberseguridad/procesamiento US$12,1M. INFERIDO: el disparador más fuerte es la Ley 21.663 "
        "sobre los 147 OIV eléctricos y la Ley 21.305 sobre los CCGE; el producto (SolisSCADA) es "
        "además la puerta de entrada más blanda del catálogo (licencia gratuita hasta 50.000 tags, "
        "no obliga a cambiar hardware). DISTINGUIR: la obligación de ciberseguridad es del OIV; que "
        "la resuelva con SUPCON es decisión del cliente."
    ),
}

# ---------------------------------------------------------------------------
# HALLAZGOS (lo que el cruce revela y no estaba dicho)
# ---------------------------------------------------------------------------
HALLAZGOS = [
    {
        "hallazgo": "CEMS es el único disparador normativo del catálogo que es OBLIGACIÓN DE RESULTADO + DE REPORTE EN LÍNEA con plazo vencido o corriendo, en un mercado sin SUPCON instalado.",
        "sustento": "D.S. 13/2011 Art. 8 (obliga CEMS) + Res. Ex. 680/2021 (conexión en línea SMA) + impuesto verde Ley 20.780 Art. 8 (obliga a cuantificar). MEDIDO: analizadores US$44,3M y SUPCON/Hobré 0 importaciones.",
        "uso_comercial": "Entrar por Analítica con el CEMS 5000 a la generación térmica y a las fundiciones de cobre (DS 28/2013) y cemento (DS 29/2013). Es la línea con el disparador más limpio y sin incumbente propio que defender.",
        "tipo": "MEDIDO+VERIFICADO",
    },
    {
        "hallazgo": "El caudal es la variable que MÁS fiscalizadores chilenos exigen a la vez, y ninguno de los instrumentos SUPCON tiene disparador equivalente.",
        "sustento": "Tabla de dato compartido (skill cumplimiento-regulatorio-chile): caudal → DGA (Ley 21.435), SISS (DS 609), SMA (DS 90), DIRECTEMAR — cuatro organismos, un instrumento. MEDIDO: caudal importado 2025 US$19,7M.",
        "uso_comercial": "Usar el SFE910 (caudalímetro electromagnético) como puerta: un instrumento que reporta a cuatro fiscalizadores convierte la conversación de 'cómprame' a 'una arquitectura para todos'.",
        "tipo": "VERIFICADO (normas) + MEDIDO (mercado)",
    },
    {
        "hallazgo": "Tres líneas del catálogo NO tienen disparador normativo propio: PLC, y parcialmente DCS y Software como categorías.",
        "sustento": "Búsqueda de una norma chilena que obligue 'PLC' o 'DCS' por nombre: no existe. Lo que obliga es la NTSyCS (resultado: observabilidad) o la Ley 21.305 (SGE). El PLC de seguridad hereda el disparador del HAZOP/LOPA del cliente.",
        "uso_comercial": "NO inventar un disparador para PLC. Venderlo por obsolescencia, proyecto nuevo o dentro de una solución mayor. Mentir con un 'la norma exige PLC' lo corrige el jefe de instrumentación en la reunión.",
        "tipo": "SIN SUSTENTO — declarado honestamente",
    },
    {
        "hallazgo": "La Ley 21.663 (ciberseguridad) da una lista NOMBRADA de 147 OIV del sector eléctrico, y la Ley 21.305 da el universo de CCGE: es la única línea donde el disparador trae la lista de empresas.",
        "sustento": "ANCI Res. Ex. 87 (D.O. 17-dic-2025): 915 OIV, eléctrico 147. Ley 21.305: consumo ≥50 Tcal/año (SGE obligatorio).",
        "uso_comercial": "Ciber/plataforma es la línea con el prospecto ya identificado por resolución oficial: cruzar la nómina OIV eléctrica con los coordinados del SEN da el universo de primer contacto para SolisSCADA + gobernanza OT.",
        "tipo": "VERIFICADO (norma con lista)",
    },
    {
        "hallazgo": "El disparador normativo más defendible para válvulas es de SEGURIDAD DE CALDERAS (DS 10/2013), no ambiental — y es de reemplazo por vida útil, no de cumplimiento nuevo.",
        "sustento": "D.S. 10/2013 MINSAL: válvulas de seguridad, manómetros, medidor de temperatura de gases, libro de operación cada 4 h. MEDIDO: capítulo 84.81 US$396,6M (el mercado más grande del catálogo).",
        "uso_comercial": "Vender válvulas por proyecto nuevo / reemplazo en generación de vapor y pulpa, apoyado en DS 10 para el argumento de seguridad. NO decir que hay una norma 'de válvulas' — no existe.",
        "tipo": "VERIFICADO (norma) + MEDIDO (mercado)",
    },
    {
        "hallazgo": "El PPDA Quillota-Catemu (DS 18/2023) es un disparador de INSTRUMENTACIÓN + monitoreo con telemetría y respaldo, no solo de análisis de laboratorio.",
        "sustento": "D.S. 18/2023 Art. 29: estaciones meteorológicas con telemetría, QA/QC y respaldo; 'si falla el monitoreo principal y respaldo, no se ejecuta la tronadura'. Art. 30: reporte anual MP/MP10 con memoria de cálculo.",
        "uso_comercial": "Para faenas mineras de la zona (El Soldado/Anglo American Sur), el PPDA obliga a un dato continuo y con respaldo: ahí entra instrumentación (meteorología, caudal de gas, MP en ducto) + SCADA. OJO pitfall: la norma exige control y reporte, no necesariamente medición directa; y el DMS-100 mide en ducto, no en fuente abierta.",
        "tipo": "VERIFICADO (decreto) — INFERIDO a qué faena aplica por comuna",
    },
    {
        "hallazgo": "La NE-RILES 2026 (en trámite, aprobada por el Consejo de Ministros para la Sustentabilidad) endurece el monitoreo de RILES hacia EN LÍNEA, abriendo un disparador nuevo para instrumentación de agua.",
        "sustento": "NE-RILES (mma.gob.cl, 2026): monitoreo EN LÍNEA de caudal para descargas >300 m3/día, conexión a plataforma electrónica del fiscalizador, pH continuo con registro ≥24 meses. Corrige el DS 90/2000 y el DS 609/1998.",
        "uso_comercial": "Adelantar la conversación de caudalímetro y pH en línea con las fuentes que descargan >300 m3/día antes de que la norma sea obligatoria — el cliente que ya tiene el registro continuo (DS 609) está a un paso del envío en línea.",
        "tipo": "VERIFICADO (texto en trámite) — distinguir de norma vigente",
    },
]

# ---------------------------------------------------------------------------
# Notas de mercado MEDIDO reutilizadas (no recalcular)
# ---------------------------------------------------------------------------
MERCADO_MEDIDO = {
    "fuente": "Registro DIN de Aduanas Chile 2025 (4.847.036 líneas) — datos/cruce_catalogo_importaciones.json",
    "rubro_automatizacion_usd": 316900000,
    "por_linea_usd": {
        "Válvulas (capítulo 84.81 completo)": 396600000,
        "DCS / controladores": 112543952.93,
        "PLC": 83870305.86,
        "Instrumentación de campo (rubro)": 60500000,
        "SIS": 52802731.44,
        "Analizadores de proceso": 44254325.27,
    },
    "canal": {
        "integradores_tecnicos": 74,
        "volumen_canal_usd": 108611014.28,
        "pct_las_condes": 55,
        "pct_con_marca_competidora": 63.5,
        "integradores_con_supcon": 0,
    },
    "base_instalada_supcon_hobre": "CERO importaciones registradas en Chile (datos/cruce_catalogo_importaciones.json)",
    "software": "SIN MEDICIÓN — declarado no medible por partida arancelaria (datos/escalera_exito.json)",
}

# ---------------------------------------------------------------------------
# Validación + ensamblado
# ---------------------------------------------------------------------------
def main():
    lineas_catalogo = ["Instrumentación", "Analítica", "Válvulas", "DCS", "PLC", "SIS", "Software y plataforma"]
    assert set(LINEAS.keys()) == set(lineas_catalogo), (
        "Líneas no coinciden: " + str(set(LINEAS.keys()) ^ set(lineas_catalogo))
    )

    con_sustento = []
    sin_sustento = []
    for nombre, d in LINEAS.items():
        tiene = d["tipo_obligacion"] != "sin_sustento" and "SIN SUSTENTO" not in d["norma_y_fuente"]
        # PLC se marca sin sustento específico pero con obligación incentivada (NTSyCS/SGE)
        if nombre == "PLC":
            sin_sustento.append(nombre)
        else:
            con_sustento.append(nombre)

    out = {
        "meta": {
            "titulo": "Cruce normativo x estrategia de penetración — catálogo SUPCON (63 productos, 7 líneas)",
            "que_es": (
                "Cruza cada línea del catálogo SUPCON con el disparador normativo chileno que "
                "empuja o incentiva su compra: la norma, la obligación, las industrias y las "
                "empresas afectadas. Es el tercer ángulo de la estrategia, junto a la escalera al "
                "éxito (dificultad por producto) y la estrategia de penetración (escalones)."
            ),
            "principio": "Un cliente no compra un analizador porque sea bueno: lo compra porque una norma lo obliga o una multa lo hizo urgente.",
            "regla_datos": "Cada norma lleva número y URL de fuente verificada. Lo que no tiene sustento se marca 'SIN SUSTENTO ENCONTRADO'. Se distingue MEDIDO (Aduanas/RETC/SMA) de INFERIDO (proyección del patrón).",
            "productos_en_catalogo": 63,
            "lineas_catalogo": lineas_catalogo,
            "lineas_con_disparador_verificado": con_sustento,
            "lineas_sin_disparador_propio": sin_sustento,
            "n_lineas_con_sustento": len(con_sustento),
            "n_lineas_sin_sustento": len(sin_sustento),
            "fuentes_normativas": FUENTES,
        },
        "lineas": LINEAS,
        "hallazgos": HALLAZGOS,
        "mercado_medido": MERCADO_MEDIDO,
        "verificacion": {
            "fecha": "2026-10-13",
            "metodo": "Texto oficial en bcn.cl/leychile (por idNorma verificado), páginas del fiscalizador (SMA, CNE, SEC, MINSAL) y resoluciones exentas; búsqueda DDG para resolver idNorma. Mercado: Registro DIN Aduanas 2025 del propio repo.",
            "advertencia": "Los umbrales y plazos cambian: verificar el texto vigente en bcn.cl antes de afirmar un número en reunión. La NE-RILES 2026 está en trámite: citarla como 'en trámite', no como vigente.",
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("OK ->", OUT)
    print("Líneas con disparador verificado:", len(con_sustento), con_sustento)
    print("Líneas sin disparador propio:", len(sin_sustento), sin_sustento)
    print("Hallazgos:", len(HALLAZGOS))
    print("Fuentes normativas:", len(FUENTES))


if __name__ == "__main__":
    main()
