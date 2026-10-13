#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATOS de las fichas de SOFTWARE DE PROCESO y PLATAFORMA de SUPCON (4a entrega).

Cada dato sale de un documento real del fabricante (ver campo 'fuente').
Lo que NO tiene respaldo en el material queda como 'POR COMPLETAR'.
En 'competencia' el material SUPCON casi nunca incluye battlecards: cuando no
existe respaldo se marca 'POR COMPLETAR — requiere validación' y, si se agrega
un competidor del mercado chileno, se rotula como INFERENCIA (conocimiento
general), nunca como dato del fabricante.

Datos crudos: datos/software_extraido.json (163 documentos, deduplicados por MD5).
Genera: datos/fichas_4_datos.json
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")

F = {}

# ======================= APC ===============================================
F["InPlant APC (control avanzado de procesos)"] = {
 "familia":"Software de proceso",
 "descripcion":"Paquete de control avanzado (Advanced Process Control) compuesto por la plataforma de control (APC-iSYS), el control predictivo multivariable (APC-Adcon), el control regulatorio ágil (APC-ARC), el monitoreo de desempeño (APC-Watch) y la optimización de desempeño (APC-PerfOpt). Hace control multivariable coordinado y optimización jerárquica multobjetivo sobre el DCS, con modelos que se autoaprenden y sensor virtual (soft sensor) para variables clave no medibles. Se implementa sobre distintos DCS, no solo el de SUPCON.",
 "beneficios":[
   "Más de 1.000 conjuntos de aplicación instalados en unidades de Sinopec, PetroChina y CNOOC",
   "Primer lugar de mercado doméstico en China por cinco años consecutivos",
   "Control multivariable predictivo (MIMO) con modelos en lazo abierto y cerrado",
   "Sensor virtual (soft sensor) para predicción en línea de indicadores clave no medibles",
   "Modelos autoadaptativos por condición operativa (autolearning) para cambios de carga y calidad de materia prima",
   "Monitoreo en línea del controlador y presentación del beneficio económico",
   "Se aplica sobre DCS de otras marcas (no requiere SUPCON)",
 ],
 "clientes_target":[
   "Refinería y petroquímica (destilación atmosférica y vacío, cracking catalítico, hidrocracking, coquización retardada, recuperación de azufre, reforma continua)",
   "Química y química fina (etileno, glicol de etileno, óxido de propileno, poliéster, cloro-álcali, carbón a químicos)",
   "Cemento y materiales de construcción (molino crudo, molino de cemento, horno rotatorio, molino de carbón)",
   "Generación eléctrica (desnitrificación, combustión)",
   "Metales",
 ],
 "competencia":"El material cita como competidores a AspenTech, Honeywell, YOKOGAWA, Rockwell e Invensys (software de control avanzado propio) y a ABB y Emerson (control avanzado integrado en su DCS). Menciona además oferentes chinos que usan software extranjero para dar servicio de ingeniería (Petro-CyberWorks, Beijing Tsinghua Huayi). En Chile el segmento APC en refinería y minería está dominado por AspenTech y Honeywell (INFERENCIA — conocimiento general, no del material).",
 "argumentos_venta":[
   "Es la única propuesta del material que reclama el primer lugar de mercado doméstico en China por 5 años consecutivos en control avanzado",
   "Se monta sobre el DCS existente del cliente, sea o no SUPCON: no obliga a cambiar el sistema de control",
   "El soft sensor resuelve el caso típico del indicador de calidad que no se puede medir en línea",
   "1.000+ aplicaciones en las mayores empresas chinas de refinería y petroquímica: cartera de referencia verificable",
   "SUPCON participa en la formulación de los estándares chinos de control avanzado GB/T 32854.1-2016 y GB/T 32854.2-2017",
   "El material incluye casos con beneficio económico medido (ahorro de crudo por tonelada, aumento de rendimiento de aromáticos)",
 ],
 "objeciones":[
   ("El APC no es un producto, es un proyecto eterno que nunca cierra", "El material define como entregables la evaluación de factibilidad, el diseño e implementación, la optimización y reingeniería, y la evaluación de desempeño, con monitoreo en línea del controlador (APC-Watch). El alcance se acota por unidad."),
   ("Nuestra gente no va a mantener el controlador una vez que ustedes se vayan", "El material contempla capacitación y consultoría en tecnologías APC y exige colaboración de las áreas de proceso, instrumentación y gestión. POR COMPLETAR: definir horas de capacitación y acompañamiento post-arranque."),
   ("AspenTech ya está instalado en la planta", "El material reconoce a AspenTech como líder del segmento. Como entrada se puede partir por una unidad no cubierta o por renovación de licencia, y comparar prestaciones. No hay battlecard formal: los diferenciales hay que levantarlos caso a caso."),
   ("¿Cuánto ahorra realmente?", "El material reporta casos con beneficio medido por unidad (por ejemplo, reforma continua con aumento de rendimiento de aromáticos), pero no publica una garantía de ahorro aplicable a cualquier planta. El ahorro se estima en el estudio de factibilidad de la unidad específica."),
 ],
 "preguntas_tecnicas":[
   "¿Qué unidad o unidades entran en el alcance del APC?",
   "¿Qué DCS tiene la planta y soporta interfaz OPC / bloques de función suficientes?",
   "¿Está disponible la instrumentación y actuación (válvulas, medidores) en estado operativo?",
   "¿Cuáles son las variables de calidad que hoy no se miden en línea y que se quieren predecir?",
   "¿Qué indicadores económicos se quieren optimizar (energía, rendimiento, calidad)?",
   "¿Cuántas variables controladas y manipuladas tiene la unidad?",
   "¿Con qué frecuencia cambia la condición operativa (materia prima, carga)?",
   "¿El cliente quiere solo la licencia de software o la solución con servicio de ingeniería?",
 ],
 "fuente":"InPlant APC V11.2 Sales Technical Manual 20250117.pdf + InPlant APC V11.02.00.00-M One Page Introduction 20240731.pptx + InPlant APC V11.2 One Page Introduction (for Customer) 20250117.pdf + [Conecta] APC Introduction.pdf",
}

# ======================= RTO ===============================================
F["InPlant RTO (optimización en tiempo real)"] = {
 "familia":"Software de proceso",
 "descripcion":"Sistema de optimización en tiempo real que conecta el modelo mecanístico (APEX) con el DCS y la base de datos histórica, hace calibración en línea del modelo y cálculo de optimización, y cierra el lazo en tiempo real a través del APC. Forma con APEX el paquete de optimización en tiempo real: APEX aporta el modelo de proceso y RTO lo ejecuta en línea contra la operación real.",
 "beneficios":[
   "Cierra el lazo entre el modelo mecanístico y el APC para optimización en línea",
   "Calibración automática del modelo con datos reales de operación (online model calibration)",
   "Licencia perpetua: una licencia de software cubre múltiples unidades RTO (los competidores venden una licencia por unidad)",
   "Respuesta automática a cambios externos e internos de la unidad",
   "Casos con beneficio económico declarado: unidad de vacío con aumento de utilidad de 4,95 CNY por tonelada de crudo (aprox. 24,74 millones CNY anuales); reforma continua con alza de rendimiento de aromáticos (BTX) de 0,58% y 0,88% según el caso",
 ],
 "clientes_target":[
   "Refinería y petroquímica de gran escala",
   "Plantas con cambio frecuente de materia prima y de carga",
   "Plantas con necesidad de ahorro energético y reducción de consumo",
   "Complejos con APC ya instalado o en instalación",
 ],
 "competencia":"El material trae battlecard explícita. Aspen (Plus+Online): producto maduro, alta participación de mercado y reconocimiento, pero licencia por unidad (un software = un sistema RTO) y precio alto (referencia del material: más de 1,8 millones de CNY por 5 años). AVEVA (ROMeo): maduro y con más casos, pero licencia por unidad y solo hace RTO en línea (no trae simulación ni análisis offline). Inferencia para Chile: AspenTech y AVEVA dominan el segmento de optimización en refinería (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "Localización: el material declara ser la única solución RTO-completa de origen chino",
   "Un licenciamiento perpetuo cubre varias unidades, lo que baja el costo de implementación frente a los competidores que licencian por unidad",
   "SUPCON declara ser pionero y líder del negocio RTO en China, con el mayor número de proyectos ejecutados o en ejecución",
   "RTO + APEX es el único paquete del material que integra simulación, calibración y optimización en línea sobre el mismo modelo",
   "Se vende como producto más servicio de ingeniería: no se recomienda vender la licencia suelta",
 ],
 "objeciones":[
   ("¿El beneficio es real o es una simulación bonita?", "El material reporta beneficios medidos en unidades específicas (por tonelada de crudo procesada, por punto de rendimiento de aromáticos). El número se estima sobre la unidad del cliente, no se copia de otro caso."),
   ("Aspen o AVEVA ya están en la casa matriz", "El material identifica como debilidades del competidor el licenciamiento por unidad, el precio y, en AVEVA, la ausencia de simulación offline. Se puede partir por una unidad no licenciada."),
   ("No queremos cambiar de simulador", "APEX soporta conversión de archivos de software de terceros según su propia one-page, para no remodelar. POR COMPLETAR: confirmar contra qué versiones de Aspen y AVEVA se ha hecho la conversión."),
   ("El RTO chino no está probado fuera de China", "El material lista proyectos domésticos y varios en ejecución, pero no lista implementaciones fuera de China en la documentación revisada. POR COMPLETAR: pedir referencias internacionales antes de prometerlas."),
 ],
 "preguntas_tecnicas":[
   "¿Cuál es la unidad objetivo y qué modelo de proceso existe hoy para ella?",
   "¿La planta tiene APC instalado? (RTO requiere APC para cerrar el lazo)",
   "¿Cada cuánto cambia la carga o la materia prima de la unidad?",
   "¿Qué función objetivo se optimiza: margen, energía, rendimiento?",
   "¿Hay datos históricos suficientes para calibrar el modelo?",
   "¿Se requiere también la simulación offline (paquete APEX)?",
   "¿Cuántas unidades se quieren cubrir bajo una misma licencia?",
 ],
 "fuente":"InPlant RTO V3.0.0-M One Page Introduction 20240918.pptx",
}

# ======================= OMS ===============================================
F["InPlant OMS (gestión de movimientos de petróleo)"] = {
 "familia":"Software de proceso",
 "descripcion":"Oil Movement System: paquete de software para operaciones de almacenamiento y transporte de petróleo y derivados. Actúa como 'navegador de proceso' y 'asistente de conducción' de las operaciones de movimiento de hidrocarburos. Incluye módulos de optimización de rutas y base de datos dinámica, identificación de líneas cerradas y alarma, sistema de información de estanques e interfaz con MES. Hace programación de tareas, gestión de órdenes, selección de ruta, ejecución y monitoreo en línea.",
 "beneficios":[
   "El material declara aumento de eficiencia laboral del 50% y reducción de costo de ingeniería del 60%",
   "Prevención de derrame, mezcla indebida, fuga y formación de vacío en estanques y sobrellenado",
   "Cálculo inteligente de ruta: selección automática de la mejor ruta con generación dinámica",
   "Soporta operaciones many-to-one complejas, reflujo, cambio de estanque en línea, cambio de bomba, adición y retiro de bomba, seguimiento de medio e identificación de líneas de alta viscosidad",
   "Trazabilidad completa de la operación ('audit tracking')",
 ],
 "clientes_target":[
   "Refinerías de gran escala en construcción o construidas",
   "Instalaciones de almacenamiento comercial",
   "Terminales de productos líquidos",
 ],
 "competencia":"El material declara explícitamente que los principales competidores de InPlant OMS son Honeywell y Yokogawa, y afirma que al momento del documento no hay productos similares en China. NO hay battlecard detallada (precios, licenciamiento ni comparación funcional) en el material revisado: POR COMPLETAR — requiere validación. En Chile, el segmento de oil movement en refinería está dominado por Honeywell y Yokogawa (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "El material lo posiciona como el único desarrollo propio de OMS en China, con prioridad de adopción de tecnología nueva sobre los competidores",
   "Reduce el error humano: es la causa típica de derrames, mezclas y sobrellenado en el movimiento de hidrocarburos",
   "Ataca la programación de camiones, trenes y buques con un mismo sistema, en vez de parches por operación",
   "Entra por la etapa temprana de diseño de la refinería o del terminal, con presentación técnica anticipada a usuarios y proyectistas",
   "La estrategia de venta declarada por el fabricante es acompañar el diseño desde el inicio y hacer visitas a casos ya instalados",
 ],
 "objeciones":[
   ("Ya tenemos un sistema de movimiento de estanques y funciona", "El material recomienda partir por instalaciones ya construidas con presentación del producto y organización de visitas a casos existentes. POR COMPLETAR: no hay estudio de migración ni de integración con sistemas existentes en este juego de documentos."),
   ("¿Es compatible con nuestro MES?", "El paquete incluye un módulo de interfaz con MES según su one-page, pero no se especifica de qué MES ni con qué estándar. POR COMPLETAR: confirmar protocolos y alcance de integración."),
   ("No hay casos de OMS SUPCON en Chile", "El material no lista referencias fuera de China para OMS. POR COMPLETAR — requiere validación: pedir la lista de referencias internacionales antes de prometerlas."),
   ("¿Cuánto cuesta?", "El material revisado no trae lista de precios ni esquema de licenciamiento de OMS. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos estanques, líneas y bombas entran en el alcance?",
   "¿Qué tipos de operación se requieren (camión, tren, buque, transferencia interna)?",
   "¿Qué MES o ERP hay que integrar?",
   "¿Hay líneas cerradas y de alta viscosidad en el trazado?",
   "¿Se requiere cambio de estanque y cambio de bomba en línea?",
   "¿Cuántos movimientos diarios y cuántos operadores los ejecutan?",
   "¿Se parte de una instalación nueva o se migra un sistema existente?",
 ],
 "fuente":"InPlant OMS V3.00.00.00-M One Page Introduction 20240712.pptx",
}

# ======================= OTS ===============================================
F["InPlant OTS (simulador de entrenamiento de operadores)"] = {
 "familia":"Software de proceso",
 "descripcion":"Operator Training Simulation System: solución de simulación que reproduce el arranque, la parada, la operación normal y distintos escenarios de accidente de una planta. Se usa tanto para entrenamiento de operadores como para verificación de diseño de proceso. Se compone de (recursos) + (plataforma) + (servicio): recursos de entrenamiento (OTS.2D para operación 2D, OTS.3D para seguridad en 3D, realidad mixta, cursos y bancos de preguntas), plataforma digital de administración (PC/APP, gestión de cursos, exámenes, aprendizaje en línea, planificación, personal, evaluación y simulacros) y servicios de entrenamiento y consultoría.",
 "beneficios":[
   "Simula arranque, parada, operación normal y accidentes: permite entrenar accidente sin exponer la planta real",
   "Recursos OTS.2D (operación de proceso), OTS.3D (seguridad y habilidades en 3D) y realidad mixta",
   "Plataforma de gestión con módulos de cursos, exámenes, aprendizaje en línea, planificación de entrenamiento, evaluación y simulacros de emergencia",
   "Permite verificar la lógica de control antes del arranque de la planta ('complete the control logic before driving')",
   "La construcción de escenarios virtuales no depende del espacio físico ni consume materiales: elimina el costo de una maqueta o un panel de entrenamiento",
   "El material declara 2 años de garantía y 5 años de upgrade de software gratuito (frente a 1 año de garantía del competidor citado)",
 ],
 "clientes_target":[
   "Refinería, petroquímica, química y química fina",
   "Generación eléctrica",
   "Petróleo y gas",
   "Plantas nuevas: verificación de diseño antes de la puesta en marcha",
   "Empresas con plan de entrenamiento de operadores, evaluación de competencias y simulacros de emergencia",
 ],
 "competencia":"El material trae comparación: Honeywell es el competidor con mayor participación de mercado extranjero, con la cotización promedio más alta del mercado, producto maduro y kit completo, pero garantía de solo 1 año y contrato de mantenimiento obligatorio después. El material declara a SUPCON primero en participación doméstica China, con precio medio y garantía de 2 años. Reconocimiento honesto del material: frente a Honeywell, SUPCON declara baja exactitud de cálculo y baja velocidad de performance en modelos grandes y sistemas especiales, y que la configuración debe hacerse junto con su DCS. En Chile, Honeywell y AspenTech son referencia en simulación de operadores (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "2 años de garantía y 5 años de upgrade gratuito, contra 1 año de garantía y mantención pagada del competidor citado",
   "El software de simulación en línea es desarrollo propio, según el material",
   "La construcción de la planta virtual no depende del espacio ni de consumibles: se evita el costo de una maqueta física",
   "Sirve dos propósitos con un mismo activo: entrenamiento de operadores y verificación de la lógica de control antes del arranque",
   "Modelos 2D, 3D y realidad mixta según el nivel de inmersión que pida el cliente",
   "El material define como estrategia romper el monopolio del competidor por precio y diferenciar por requisitos de performance y funcionalidad",
 ],
 "objeciones":[
   ("Los chinos no han hecho simuladores de plantas grandes", "El propio material reconoce como debilidad que en modelos grandes y sistemas especiales la exactitud de cálculo es baja y el performance lento. No lo niegues: acota el alcance a la unidad y valida el modelo con los datos de la propia planta antes de firmar."),
   ("Honeywell ya está instalado", "El argumento del material es precio y garantía (2 años vs 1 año). Se puede partir por una unidad no cubierta o por un simulador nuevo."),
   ("Necesitamos que funcione sin su DCS", "El material dice que la configuración se hace junto con el DCS de SUPCON, lo que es una restricción real. POR COMPLETAR: confirmar si opera sobre otras marcas de DCS y con qué esfuerzo."),
   ("¿Cuánto cuesta un simulador de este tipo?", "El material no publica precios ni esquema de licenciamiento de OTS. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Qué unidad o unidades se quieren simular?",
   "¿El objetivo es entrenamiento de operadores, verificación de diseño, o ambos?",
   "¿Se requiere OTS.2D, OTS.3D o realidad mixta?",
   "¿Cuántos operadores se entrenan y con qué frecuencia?",
   "¿Qué DCS tiene la planta y qué interfaz de simulación requiere?",
   "¿Se necesita acoplar el simulador a un entrenador de instructores (función instructor)?",
   "¿Se requiere integración con el sistema de gestión de competencias del cliente?",
   "¿Se requiere verificación de la lógica de control antes del arranque?",
 ],
 "fuente":"InPlant OTS V5.00.00.00-M Product One Page Introduction-Sales 20240815.pptx",
}

# ======================= EAM ===============================================
F["InPlant EAM (gestión de activos empresariales)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Enterprise Asset Management: software de gestión de activos con el libro mayor de equipos como base de conocimiento de mantenimiento. Guía el trabajo de mantención mediante gestión de arranque/parada, mantención preventiva, gestión de inspección, gestión de riesgos ocultos, órdenes de trabajo inteligentes y gestión de repuestos. Cubre el ciclo de vida completo del equipo (planificación, diseño, fabricación, selección, compra, instalación, mantención, actualización y baja), con base de datos de ciclo de vida, terminal móvil, panel electrónico y tablero de monitoreo, e integración con OA, ERP, inventario, gestión de trabajo, seguridad y ambiente, energía, producción, calidad e IoT (instrumentos, PLC/DCS, código de barras/RFID, SCADA).",
 "beneficios":[
   "El material declara reducción del costo de inventario de repuestos del 25% mediante avisos de reposición basados en datos históricos",
   "El material declara aumento de la vida útil del equipo del 10% al 20% con estrategias de mantención óptimas",
   "Recomendación automática de estrategias de inspección y mantención a partir de bases de conocimiento y análisis de datos",
   "Cubre el ciclo de vida completo del equipo e integra los documentos de compra e instalación con los registros de operación y mantención",
   "OEE de equipo y análisis de salud del equipo como indicadores nativos",
   "Terminal móvil para inspección en terreno y órdenes de trabajo fuera de la sala de control",
   "Se integra con OA, ERP, inventario, energía, producción y calidad, además de instrumentos, PLC/DCS, RFID y SCADA",
 ],
 "clientes_target":[
   "Refinería, petroquímica y química",
   "Industria de proceso en general con parque de equipos extenso",
   "Empresas con documentación de equipos en papel o Excel y sin trazabilidad de ciclo de vida",
   "Plantas con necesidad de bajar inventario de repuestos o de pasar de mantención correctiva a predictiva",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material revisado no trae battlecard de EAM (ni precios ni comparación funcional). En el mercado chileno el segmento de EAM/CMMS está dominado por IBM Maximo y SAP PM, con Infor y Maincare como alternativas (INFERENCIA — conocimiento general, no del material).",
 "argumentos_venta":[
   "Los dos beneficios del material son medibles y comprobables en el negocio: -25% de inventario de repuestos y +10% a +20% de vida útil de equipos",
   "Convierte los archivos de equipo (hoy en papel y Excel) en una base de conocimiento consultable",
   "No es solo un CMMS: incluye OEE, análisis de salud de equipo y evaluación de desempeño de personal",
   "Se integra con lo que el cliente ya tiene (OA, ERP, instrumentos, PLC/DCS, SCADA) en vez de reemplazarlo",
   "Aplica tanto en industria de proceso como en industria discreta, con una versión simplificada enfocada en OEE",
   "El material cita casos en Yulin Chemical y otros clientes industriales grandes",
 ],
 "objeciones":[
   ("Ya tenemos SAP PM / IBM Maximo", "El material no trae battlecard frente a SAP ni Maximo. El argumento disponible es la integración con ERP y sistemas existentes en vez del reemplazo. POR COMPLETAR — requiere validación de diferenciación funcional."),
   ("Nuestros datos de equipos están desordenados y en papel", "El material parte precisamente de ese escenario: equipos con documentos de compra y mantención en papel y Excel, sin sistematicidad y sin datos de calidad para análisis de confiabilidad. La estructuración del dato es parte del proyecto."),
   ("¿Funciona en terreno sin conexión?", "El material lista terminal móvil y aplicación móvil con inspección móvil. POR COMPLETAR: confirmar si opera offline y cómo sincroniza."),
   ("¿Cuánto cuesta la licencia?", "El material revisado no publica lista de precios ni esquema de licenciamiento de EAM. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos equipos y cuántas ubicaciones entran en el alcance?",
   "¿Qué ERP y qué OA hay que integrar?",
   "¿Qué datos de equipos existen hoy y en qué formato?",
   "¿El foco es ciclo de vida completo, inspección y mantención, o repuestos?",
   "¿Se requiere OEE y análisis de salud de equipo?",
   "¿Se requiere inspección móvil en terreno?",
   "¿Qué equipos tienen criticidad y requieren mantención predictiva?",
   "¿Se integra con SCADA, PLC/DCS o instrumentos existentes?",
 ],
 "fuente":"InPlant EAM V8.00.00.00-M One-page Product Introduction.pptx + Tier 0 EAM Sharing.pdf",
}

# ======================= PLS ===============================================
F["InPlant PLS (posicionamiento de personal)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Sistema de posicionamiento de personal de alta exactitud. Usa visualización 3D, Bluetooth, UWB, GPS, Beidou y ZigBee, con exactitud de posicionamiento que se adapta en un rango de 0,1 metros a 10 metros. Monitorea el número total de personas en el área de trabajo, su dinámica y distribución, el equipo o taller donde se encuentran, y la información del personal de inspección (hora, trayectoria). Sirve para control de personal por zona, operaciones internas y externas, gestión de riesgo en tiempo real y rescate preciso en caso de accidente.",
 "beneficios":[
   "Exactitud de posicionamiento de 0,1 m a 10 m según la tecnología usada",
   "Gateway de adquisición de datos unificado que recibe datos de Bluetooth, UWB, GPS, Beidou y ZigBee sin desarrollo a medida",
   "Visualización 3D con posición en tiempo real, trayectorias históricas y capturas de posición",
   "Análisis espacial para evaluación de posición y alerta temprana",
   "Caso citado: el proyecto IMI (astillero de Saudi Aramco, Hyundai, Bahri y Lamprell) controla más de 20.000 empleados y más de 10.000 activos y herramientas",
   "Caso citado: la Academia Corporativa de Saudi Aramco en Dalan cubre 187.420 m² y se monitoreó con InPlant PLS durante la construcción",
   "Reduce el costo de supervisión y mejora el nivel de seguridad de producción",
 ],
 "clientes_target":[
   "Refinería, petroquímica, química del carbón, química fina, petróleo y gas",
   "Generación eléctrica y metalurgia",
   "Celulosa y papel, materiales de construcción y farmacéutica",
   "Faenas con trabajo en zonas de riesgo y necesidad de rescate preciso",
   "Obras en construcción de gran tamaño con muchos contratistas en planta",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material revisado no trae battlecard de posicionamiento de personal. En Chile el segmento de posicionamiento en faena (UWB/ZigBee con control de acceso) suele estar cubierto por proveedores especializados de seguridad minera y por las plataformas de control de acceso de las propias faenas (INFERENCIA — conocimiento general, no del material).",
 "argumentos_venta":[
   "Es uno de los pocos productos del catálogo SUPCON con casos fuera de China: Arabia Saudita (Aramco e IMI), lo que sirve de referencia internacional verificable",
   "Un solo gateway recibe Bluetooth, UWB, GPS, Beidou y ZigBee: no obliga a estandarizar toda la faena en una tecnología",
   "El rango de exactitud (0,1 m a 10 m) permite calibrar el costo por zona en vez de tomar una sola tecnología para todo el recinto",
   "Cubre tres necesidades regulatorias de una vez: control de personal por zona, rescate y trazabilidad de inspecciones",
   "Caso IMI: más de 20.000 trabajadores y más de 10.000 activos y herramientas bajo un mismo sistema",
 ],
 "objeciones":[
   ("Ya tenemos control de acceso con tarjeta", "El control de acceso dice quién entró, no dónde está ni por dónde pasó. El material entrega posición en tiempo real, trayectoria histórica y ubicación por zona. POR COMPLETAR: definir el caso de uso concreto (rescate, control de zona, trazabilidad de inspección) antes de discutir tecnología."),
   ("Interferencia y cobertura en planta industrial", "El material declara cinco tecnologías de posicionamiento y adaptación de exactitud entre 0,1 m y 10 m, lo que permite elegir según el recinto. POR COMPLETAR — requiere validación en terreno: no hay estudio de interferencia ni de sitio en el material."),
   ("¿Se integra con gestión de contratistas y turnos?", "El material menciona control de personal interno y externo y gestión unificada. POR COMPLETAR: confirmar integración con sistemas de contratistas y turnos."),
   ("¿Cuánto cuesta?", "El material revisado no publica lista de precios de PLS. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos metros cuadrados y cuántas zonas se quieren monitorear?",
   "¿Cuántas personas y cuántos activos o herramientas se rastrean?",
   "¿Qué exactitud se requiere por zona: 0,1 m (UWB) o varios metros (ZigBee/GPS)?",
   "¿Es interior, exterior, o ambos?",
   "¿La instalación es en zona con atmósfera explosiva? (requiere equipos certificados Ex)",
   "¿Se requiere visualización 3D y trayectoria histórica?",
   "¿Se integra con control de acceso y gestión de contratistas del cliente?",
   "¿Se requiere botón de pánico o alerta en el dispositivo del trabajador?",
 ],
 "fuente":"InPlant PLS V8.00.00.00 One Page Introduction 20240806.pptx",
}

# ======================= Blend =============================================
F["InPlant Blend (optimización y mezcla en línea)"] = {
 "familia":"Software de proceso",
 "descripcion":"Software de optimización y mezcla en línea de productos de petróleo, parte de la solución de cadena de suministro (PSC). Se compone de tres submódulos: BOM (gestión de fórmula y descarga de órdenes, monitoreo remoto de tareas y generación automática de reportes de lote), BPC (control de propiedades de la mezcla por optimización en línea del ratio) y BRC (control proporcional en línea de la mezcla). Funciona combinado con el DCS, con analizador en línea, y logra el control de borde de la calidad (no sobrecalidad).",
 "beneficios":[
   "Tres objetivos de optimización seleccionables: económico, de equilibrio y de capacidad",
   "Un cabezal de mezcla controla hasta 16 líneas de mezcla y 3 líneas de despacho",
   "Compensación de calidad del aceite de fondo de estanque y seguimiento y compensación de calidad en línea de tubería",
   "Soporta múltiples objetivos de masa (octanaje, presión de vapor) con control de borde simultáneo",
   "El controlador de optimización de mezcla usa el controlador APC de desarrollo propio",
   "El material declara que toda la gasolina y parte del diésel de las refinerías nuevas adopta mezcla en línea, y que cerca del 30% ya completó la actualización: mercado con espacio de desarrollo amplio",
   "Compatible con repartición global de fórmulas para múltiples series de producto",
 ],
 "clientes_target":[
   "Refinerías con producción de gasolina y diésel",
   "Plantas con mezcla de componentes y analizador en línea disponible",
   "Refinerías nuevas (la tecnología viene en el diseño base)",
   "Refinerías existentes que quieren actualizar a mezcla en línea",
 ],
 "competencia":"El material declara que Yokogawa y Honeywell ocupan cerca del 70% de la participación de mercado en mezcla, y que el resto se reparte entre varias marcas domésticas chinas. No entrega tabla comparativa por función ni precios: POR COMPLETAR — requiere validación detallada. En refinería chilena la mezcla en línea está dominada por Honeywell y Yokogawa (INFERENCIA — conocimiento general, consistente con lo que dice el material).",
 "argumentos_venta":[
   "El software de optimización en línea es de propiedad intelectual propia y su versión 1.5 se liberó en diciembre de 2022",
   "Apunta directo al problema económico de la refinería: el objetivo declarado es el mínimo costo con el mínimo exceso de calidad",
   "El controlador de mezcla reutiliza el controlador APC de desarrollo propio: tecnología madura y probada por el fabricante",
   "Un cabezal controla hasta 16 líneas de mezcla y 3 de despacho: escala con la refinería",
   "El operador descarga y monitorea la orden de mezcla desde el navegador, con interfaz de operación también en el DCS",
   "El mercado de mezcla en línea está en proceso de actualización (el material estima cerca del 30% ya migrado), lo que abre la ventana de entrada",
 ],
 "objeciones":[
   ("Honeywell o Yokogawa ya tienen la mezcla y funcionan bien", "El material reconoce esa participación del 70%. Sin battlecard detallada la entrada hay que construirla con una medición de exceso de calidad de la planta: se mide cuánto sobrecalidad se está produciendo hoy y ese es el caso de negocio."),
   ("¿Se integra con cualquier DCS?", "El material describe el control proporcional en línea hecho por el módulo de control del DCS, lo que sugiere dependencia del DCS. POR COMPLETAR: confirmar si opera sobre DCS de otras marcas."),
   ("Necesitamos analizadores en línea de calidad", "El sistema se apoya en analizador en línea más el DCS. POR COMPLETAR: definir si el analizador es requisito obligatorio o si hay modo sin analizador (control por propiedades de laboratorio)."),
   ("¿Cuál es el retorno?", "El material no publica una cifra de retorno por planta, solo la descripción del objetivo de mínimo costo con mínimo exceso de calidad. POR COMPLETAR — requiere estimación caso a caso."),
 ],
 "preguntas_tecnicas":[
   "¿Qué productos se mezclan (gasolina, diésel, otros)?",
   "¿Cuántos componentes y cuántos cabezales de mezcla hay?",
   "¿Existe analizador en línea y de qué propiedades (octanaje, presión de vapor, otras)?",
   "¿Qué DCS tiene la planta?",
   "¿Cuál es el objetivo de optimización: económico, de equilibrio o de capacidad?",
   "¿Hay compensación de fondo de estanque y de tubería en el diseño actual?",
   "¿Se requiere gestión de órdenes y reporte de lote en línea (módulo BOM)?",
 ],
 "fuente":"InPlant Blend One Page Introduction 20240412.pptx + SDO - Smart Plant with Tank Farm.pptx",
}

# ======================= SCO ===============================================
F["InPlant SCO (optimización de cadena de suministro y scheduling)"] = {
 "familia":"Software de proceso",
 "descripcion":"Software de optimización de cadena de suministro y programación inteligente de producción, basado en algoritmos de investigación de operaciones e IA. Hace dos cosas: optimización del plan maestro (simulación oferta-demanda, optimización de plan, simulación de escenarios y cálculo de beneficio) y scheduling inteligente (programación con restricciones complejas y reprogramación dinámica en tiempo real). Se ofrece en versión Standard (para una planta o empresa única) y versión Group (para grupos con varias filiales).",
 "beneficios":[
   "Soporta restricciones complejas: capacidad de equipos, jornada de personal, suministro de materiales, secuencia de proceso y restricciones por cambio de especialidad de producto",
   "Scheduling inteligente con un clic y reprogramación dinámica en tiempo real",
   "Optimización del plan maestro con simulación de oferta-demanda, optimización de plan, simulación de escenarios y cálculo de beneficio",
   "Versión Standard: 50 usuarios concurrentes por empresa",
   "Versión Group: 1 grupo más 2 fábricas subsidiarias, con 200 usuarios concurrentes por empresa",
   "Cierra el lazo plan-ejecución: cubre todo el ciclo de vida del plan, desde la formulación hasta el cumplimiento",
 ],
 "clientes_target":[
   "Refinería de petróleo y química fina",
   "Baterías de litio, silicona orgánica y farmacéutica",
   "Celulosa y papel y metalurgia",
   "Empresas de producción continua y por lotes",
   "Grupos empresariales con varias plantas (versión Group)",
 ],
 "competencia":"El material trae comparación cualitativa: Blue Yonder se enfoca en optimización end-to-end y scheduling de producción, pero su nivel de integración de información es relativamente débil; SAP se enfoca en la gestión integral de recursos empresariales y carece de optimización especializada. NO hay tabla de precios ni licenciamiento: POR COMPLETAR — requiere validación. En Chile el segmento de planificación y scheduling está dominado por SAP APO/IBP y por soluciones de scheduling especializadas (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "Modelo de optimización basado en investigación de operaciones, no en reglas heurísticas simples: permite simular escenarios y calcular el beneficio antes de decidir",
   "Apunta a la brecha que el material atribuye a los competidores: SAP cubre el recurso empresarial pero no optimiza la operación; Blue Yonder optimiza pero integra poco",
   "Reprogramación dinámica en tiempo real: el plan se reajusta cuando cambia la realidad de la planta",
   "Dos versiones empaquetadas según tamaño (50 usuarios por empresa en Standard, 200 por empresa en Group): el alcance y el precio se definen por escala",
   "Industrias objetivo amplias: no es solo refinería, también baterías de litio, silicona, fármaco, celulosa y metalurgia",
 ],
 "objeciones":[
   ("Ya tenemos SAP y las órdenes de producción salen de ahí", "El material posiciona a SAP como gestión de recursos sin optimización especializada. El argumento es que SCO optimiza y simula escenarios dentro del plan de SAP, no que lo reemplace. POR COMPLETAR: confirmar el modo de integración con SAP (interfaz, frecuencia, alcance de datos)."),
   ("Nuestros planificadores no van a usar un optimizador", "El material declara scheduling inteligente con un clic y reprogramación en tiempo real como mecanismo de simplicidad. POR COMPLETAR: definir horas de capacitación y acompañamiento."),
   ("¿Cuál es el ahorro concreto?", "El material describe cálculo de beneficio y simulación de escenarios como funciones del producto, pero no publica una cifra de ahorro ni un caso con beneficio medido. POR COMPLETAR — requiere caso de negocio con datos del cliente."),
   ("¿Cuánto cuesta?", "El material revisado no publica lista de precios ni esquema de licenciamiento de SCO. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Es una planta única o un grupo con varias plantas?",
   "¿Cuántos usuarios concurrentes de planificación habrá?",
   "¿La producción es continua, por lotes, o mixta?",
   "¿Qué restricciones reales limitan hoy la programación (capacidad, personal, secuencia, cambio de producto)?",
   "¿Qué ERP hay que integrar y con qué frecuencia se sincroniza?",
   "¿Se requiere optimización de compra de materia prima, de inventario, o de la mezcla producción-venta?",
   "¿La reprogramación debe ser en línea o basta una frecuencia diaria o por turno?",
 ],
 "fuente":"InPlant SCO One Page Introduction-Sales.pptx",
}

# ======================= IFEM ==============================================
F["InPlant IFEM ProcessSuite (MES de producción continua)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Manufacturing Execution System diseñado para industrias de proceso (refinería, petroquímica y química). Integra los procesos de negocio de PCS, MES y ERP para dar una vista completa de la cadena de valor de producción. Incluye gestión de plan de programación, gestión de proceso, gestión operacional, gestión de materiales (balance de materias) y gestión de estanques. Hay además una variante para producción por lotes, InPlant IFEM BatchSuite, con versiones Básica, Estándar y Avanzada.",
 "beneficios":[
   "Integra PCS, MES y ERP: la cadena de valor de producción se ve en un solo lugar",
   "Balance de materiales de tres niveles: equipo, departamento y empresa",
   "Gestión de estanques con recepción y despacho, medición, monitoreo de estado, cambio de material y cálculo de volumen",
   "Gestión de órdenes de trabajo, comando de operación y cambio de turno para operadores de planta",
   "El material cita casos en Wanhua Chemical y Transfar Chemicals",
   "BatchSuite cierra el ciclo desde la confirmación de la orden de trabajo hasta el reporte de lote, con trazabilidad de calidad y sincronización de inventario con el ERP",
 ],
 "clientes_target":[
   "Refinería, petroquímica y química",
   "Industrias con balance de materiales y estanques relevantes",
   "Empresas que quieren conectar PCS con ERP y hoy operan con la información partida",
   "Producción por lotes: reactores y DCS con necesidad de trazabilidad (BatchSuite)",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material revisado no trae battlecard de MES (ni precios ni comparación funcional). En Chile el segmento MES de industria de proceso está dominado por AVEVA (Wonderware), Siemens y Rockwell, con SAP MII/MES como alternativa desde el mundo ERP (INFERENCIA — conocimiento general, no del material).",
 "argumentos_venta":[
   "El material lo posiciona como la pieza que conecta PCS con MES y ERP, no como una isla adicional de información",
   "Balance de materiales en tres niveles (equipo, departamento y empresa): responde a la pregunta de dónde se pierde el material",
   "Gestión de estanques dentro del mismo paquete: evita licenciar y mantener un sistema aparte",
   "BatchSuite tiene tres versiones según el punto de partida del cliente: solo órdenes de trabajo, MES más batch, o avanzada (útil cuando el cliente todavía no está listo para batch control)",
   "Casos citados en clientes químicos de gran tamaño (Wanhua Chemical, Transfar Chemicals, Kansai Paint, Teway Food)",
 ],
 "objeciones":[
   ("Nuestro MES actual ya cubre esto", "El material no trae battlecard de MES frente a AVEVA, Siemens o Rockwell. El punto de entrada disponible es el balance de materiales de tres niveles y la gestión de estanques. POR COMPLETAR — requiere validación de diferenciación funcional."),
   ("No queremos un sistema más en la planta", "El argumento del material es exactamente el opuesto: IFEM integra PCS, MES y ERP en lugar de agregar una capa desconectada. POR COMPLETAR: demostrar la integración con el ERP concreto del cliente."),
   ("En farmacéutica necesitamos validación CSV", "El material advierte que si la industria farmacéutica requiere certificados CSV, hay que contactar primero a la unidad de negocio farmacéutica de SUPCON para el servicio de consultoría. Es un servicio aparte, no viene incluido."),
   ("¿Cuánto cuesta?", "El material revisado no publica lista de precios ni esquema de licenciamiento de IFEM. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿La producción es continua o por lotes?",
   "¿Qué ERP hay que integrar y con qué estándar?",
   "¿Cuántos estanques y cuántas unidades entran en el balance de materiales?",
   "¿Se requiere balance de materiales en los tres niveles (equipo, departamento, empresa)?",
   "¿Se requiere gestión de órdenes de trabajo y cambio de turno?",
   "Si es por lotes: ¿qué sistema de batch hay instalado hoy (SUPCON o de terceros)?",
   "Si es farmacéutica: ¿se requiere validación CSV y quién la ejecuta?",
   "¿Cuántos usuarios de operación y de planificación habrá?",
 ],
 "fuente":"InPlant IFEM ProcessSuite V8.0 One-page Product Introduction 20240620.pptx + InPlant IFEM BatchSuite One Page Introduction 20240913.pptx",
}

# ======================= PID ===============================================
F["InPlant PID (evaluación y sintonización de lazos de control)"] = {
 "familia":"Software de proceso",
 "descripcion":"Solución de evaluación de desempeño y sintonización de lazos de control PID. Hace monitoreo automático, evaluación de desempeño, localización de problemas y optimización de parámetros sobre todos los lazos PID de la planta. Soporta comunicación OPC, por lo que opera tanto sobre DCS de SUPCON como sobre DCS de otros fabricantes (previa confirmación de versión de software y hardware y de licencia de interfaz OPC).",
 "beneficios":[
   "Caso citado en planta de olefinas de un millón de toneladas: 873 lazos evaluados y diagnosticados, 540 lazos sintonizados y 41 grupos de lazos complejos optimizados",
   "En ese mismo caso la estabilidad de operación subió a cerca del 99%, la frecuencia de alarmas bajó 50% y la frecuencia de operación manual bajó 80%",
   "El material declara tasa de control cerrado de 97% tras la aplicación",
   "Recomendación del fabricante: máximo de 2.000 lazos de control por licencia de InPlant PID",
   "Se vende en dos modalidades: software con instalación, despliegue y capacitación, o software más servicio de sintonización de lazos",
   "Opera sobre DCS de otras marcas vía OPC, no exige DCS SUPCON",
 ],
 "clientes_target":[
   "Refinería, petroquímica y química",
   "Plantas de olefinas y unidades con muchos lazos de control",
   "Plantas con alta frecuencia de alarmas o de operación manual",
   "Plantas que quieren cerrar la gestión de mantenimiento de lazos sin intervenir la lógica de control",
 ],
 "competencia":"El material trae comparación: Honeywell tiene índice de evaluación completo y buena presentación, con algoritmo de sintonización regular mejor, pero poca localización, poca experiencia en proyectos de optimización de lazos básicos y el precio más alto del mercado con menor desempeño relativo; SinoControl tiene muchos proyectos y buena capacidad de implementación pero le faltan funciones profesionales de evaluación y diagnóstico; Hollysys no tiene productos de desarrollo propio. El material posiciona a SUPCON con cobertura completa de índices, diagnóstico completo, múltiples modos de sintonización y precio medio. En Chile el segmento de evaluación de lazos de control está dominado por Honeywell y por herramientas especializadas (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "Los beneficios del material son cifras de un caso real y grande (planta de olefinas de un millón de toneladas): 873 lazos, 540 sintonizados, alarmas -50%, operación manual -80%",
   "Se puede vender como diagnóstico puro sin tocar la lógica de control: riesgo bajo para el cliente y entrada rápida",
   "Opera sobre DCS de otras marcas por OPC, así que no obliga a cambiar el sistema de control",
   "La modalidad con servicio de sintonización convierte el software en un resultado medible (lazos sintonizados), no en una licencia más",
   "Localización: el material marca la falta de localización como debilidad del competidor que él sí resuelve (en su mercado de origen; en Chile esto hay que validarlo)",
 ],
 "objeciones":[
   ("Honeywell tiene mejor algoritmo de sintonización", "El propio material reconoce esa ventaja del competidor. El argumento es precio y cobertura de índices, más la modalidad de servicio. No prometas superioridad de algoritmo."),
   ("¿Sirve en nuestro DCS?", "Sí, con comunicación OPC según el material, pero antes de vender hay que confirmar tipo de DCS, versión de software y hardware, y licencia de interfaz OPC en el sitio del cliente. Es el primer paso obligatorio del fabricante."),
   ("¿Cuántos lazos cubre la licencia?", "El material recomienda no superar 2.000 lazos de control por licencia. Se dimensiona por número de lazos."),
   ("¿Cuánto cuesta?", "El material revisado no publica lista de precios. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Qué tipo y versión de DCS tiene la planta?",
   "¿Hay licencia de interfaz OPC disponible en el DCS?",
   "¿Cuántos lazos de control hay en total? (límite recomendado: 2.000 por licencia)",
   "¿Cuántos lazos se quieren evaluar y cuántos sintonizar?",
   "¿Cuál es la tasa de control cerrado actual y la frecuencia de alarmas?",
   "¿Se quiere solo evaluación y diagnóstico, o también servicio de sintonización?",
   "¿Hay grupos de lazos complejos identificados (columnas, temperaturas acopladas)?",
 ],
 "fuente":"InPlant PID V4.02.00.00.01-M One Page Introduction(Sale) 20240628.pptx + PID Performance Evaluation Software User Manual(1).pdf + PID Self-Tuning User Manual.pdf",
}

# ======================= TAS ===============================================
F["InPlant TAS (carga y descarga inteligente)"] = {
 "familia":"Software de proceso",
 "descripcion":"Sistema inteligente de carga y descarga de camiones, trenes y buques. Gestiona el proceso completo de camiones que entran y salen de la planta: auto registro y recepción de tarjeta, cola de vehículos, llamada para entrar, reconocimiento de patente, control de puerta logístico, pesaje automático, carga y descarga cuantitativa, control de flujo, interbloqueo y alarma, confirmación de recepción y despacho, y autoservicio de liquidación e impresión de documentos. Cubre capas de hardware, adquisición de datos, aplicación y presentación.",
 "beneficios":[
   "El material declara aumento del 20% al 30% en el número promedio de vehículos atendidos por día",
   "El material declara reducción de la carga de trabajo en 20% y reducción de la tasa de error a 0,1%",
   "Control cuantitativo de carga y descarga: evita el engaño en la medición y las pérdidas por error humano",
   "Operación desatendida en registro, cola, ingreso y salida de planta y pesaje",
   "Trazabilidad y certificado digital en todo el proceso, con gestión de autorizaciones y monitoreo de llenado",
   "Se integra con InPlant WMS, LMS, OMS y DCS para una solución integrada de una sola parada",
 ],
 "clientes_target":[
   "Petroquímica: carga y descarga de crudo, derivados y químicos",
   "Química fina, química del carbón y cloro-álcali",
   "Farmacéutica: materias primas y medicamentos",
   "Materiales de construcción: áridos y materiales diversos",
   "Terminales y plantas con flujo alto de camiones, trenes o buques",
 ],
 "competencia":"El material trae comparación de competidores chinos: Jiangsu Deda (fabricante de primera línea en China, marca reconocida, productos livianos y de buena apariencia, buena capacidad de servicio de ingeniería) y Chongqing Endurance (productos con controladores de batch, caudalímetros, brazos de carga, bombas y válvulas, foco en hardware). El diferencial que reclama SUPCON es la integración con WMS, LMS, OMS y DCS y el diseño de interfaz de software. No hay competidores internacionales ni precios en el material: POR COMPLETAR — requiere validación. En Chile el segmento de carga y descarga de camiones y trenes está cubierto por integradores locales y por los proveedores de básculas y hardware de carga (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "Los beneficios vienen cuantificados en el material: +20% a +30% de vehículos/día, -20% de carga de trabajo y tasa de error 0,1%",
   "Ataca el engaño en la medición, que es la fuga clásica de plata en carga de camiones: el sistema cuantifica y controla",
   "Se integra con WMS, LMS, OMS y DCS del cliente, en lugar de ser un sistema aislado de pesaje",
   "Operación desatendida en registro, cola, puerta y pesaje: menos personas y menos error humano",
   "Aplica a camión, tren y buque con el mismo sistema, en seis industrias distintas",
   "Certificado digital y gestión de autorizaciones: sirve de evidencia ante auditoría",
 ],
 "objeciones":[
   ("Nuestro proceso de carga es muy particular", "El material lista operaciones básicas soportadas (cola, llamada, salto de número, reconocimiento de patente, pesaje, carga cuantitativa, interbloqueo) y el material de introducción incluye el flujograma completo de operación. Se acota levantando el flujo real del cliente."),
   ("Ya tenemos básculas y controladores de batch funcionando", "El argumento del material es que TAS integra el proceso completo con WMS, LMS, OMS y DCS. Los competidores citados vienen del hardware. POR COMPLETAR: definir si el proyecto reemplaza el hardware existente o solo agrega la capa de gestión."),
   ("¿Sirve para trenes y buques o solo camiones?", "El material lo declara para camiones, trenes y buques. POR COMPLETAR: confirmar el alcance real del módulo de tren y de buque, porque los casos citados son de camiones."),
   ("¿Cuánto cuesta?", "El material revisado no publica lista de precios ni esquema de licenciamiento de TAS. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Se carga por camión, tren, buque o combinación?",
   "¿Cuántos vehículos por día y cuántos puntos de carga y descarga?",
   "¿Qué productos se cargan (líquidos, sólidos, ambos)?",
   "¿Hay básculas, controladores de batch o sistemas de pesaje existentes que deban integrarse?",
   "¿Se requiere integración con WMS, LMS u OMS del cliente?",
   "¿Cuántos operadores y cuántas personas se quieren retirar del proceso?",
   "¿Se requiere certificado digital y firma electrónica?",
 ],
 "fuente":"InPlant TAS V3.20.00.00-M One Page Introduction 20240820.pptx + InPlant TAS Introduction .pptx + SDO - Smart Plant with Tank Farm.pptx",
}

# ======================= PRIDE =============================================
F["PRIDE (diagnóstico predictivo y monitoreo de equipos)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Perception of Readable Instruments, Devices and Equipment: plataforma de sensado inteligente y gestión de desempeño de activos (APM) construida sobre supOS. Recolecta datos de equipos rotativos, estáticos, eléctricos, instrumentación y sistemas de control de toda la planta y los almacena en un data lake especializado. Con big data, aprendizaje profundo y modelos de redes neuronales hace monitoreo en tiempo real, diagnóstico de salud, predicción de fallas y recomendación de mantención, con aplicaciones por equipo (vibración de equipos rotativos, válvulas de control, válvulas solenoides, medidores de flujo másico, detección de fuga en tuberías, falla de calderas, contaminación de cabinas, salud de sistemas de control).",
 "beneficios":[
   "Base de datos de fallas del material: más de 31.000 estrategias de mantenimiento y más de 11.000 casos de falla",
   "Diagnóstico de 1.566 tipos de fallas con modelos de predicción por IA (según la one-page de monitoreo de vibración)",
   "Monitoreo 24/7 automatizado de unidades y bombas con alerta temprana para reducir paradas no programadas",
   "Smart ICS: reduce los ítems de inspección de 10 a 5, con 50% más de eficiencia, y ahorra 1 a 2 personas de inspección manual por año",
   "Reemplaza la inspección manual de equipos, da ubicación precisa de falla y extiende la vida útil del equipo",
   "Conectividad amplia con equipos, instrumentos y válvulas de distintos fabricantes",
   "Corre sobre supOS V5.00.02.00-M; si el cliente ya tiene la versión estándar de supOS, se actualiza a esta versión",
   "Casos citados: Sinopec Zhenhai Refinery y Sinopec Maoming Petrochemical",
 ],
 "clientes_target":[
   "Petroquímica, química, energía, metalurgia y farmacéutica de nivel A/B/C",
   "Proyectos de integridad de equipos",
   "Proyectos de planta inteligente",
   "Plantas con inspección manual intensiva en salas de gabinetes y en unidades rotativas",
   "Plantas con bombas, compresores, ventiladores y motores críticos",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material revisado no trae battlecard de PRIDE frente a competidores de monitoreo de condición (ni precios ni comparación). En el mercado chileno el monitoreo de condición de equipos rotativos está dominado por SKF, Emerson (CSI/AMS) y Bently Nevada, con servicio de análisis por especialistas externos (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "Las cifras del material son duras y verificables como referencia: 31.000+ estrategias de mantenimiento, 11.000+ casos de falla y 1.566 tipos de fallas diagnosticables",
   "El ahorro de personal es explícito: 1 a 2 personas de inspección al año y 50% de eficiencia en los ítems de inspección",
   "Cubre instrumentación, válvulas, válvulas solenoides, sistemas de control y equipo estático y rotativo, no solo bombas",
   "Se apoya en supOS, así que si el cliente ya tiene supOS, PRIDE es una extensión y no una plataforma nueva",
   "La mantención pasa de correctiva o programada a predictiva, con recomendaciones de mantención en vez de solo alarmas",
   "Caso citado: reemplaza la inspección manual de sala de gabinetes (que hoy se hace hasta 2 veces al día) por monitoreo 24/7",
 ],
 "objeciones":[
   ("Ya tenemos especialistas en análisis de vibración", "El material apunta a lo que la inspección manual no alcanza: fallas esporádicas, anomalías internas que la inspección superficial no detecta y el seguimiento 24/7. No reemplaza al especialista, le quita el trabajo repetitivo. POR COMPLETAR: definir el rol del especialista en la operación con PRIDE."),
   ("Nuestra instrumentación es de varias marcas", "El material declara alta compatibilidad y conectividad con instrumentos y válvulas de distintos fabricantes, con soporte de protocolos mayores. POR COMPLETAR: validar la lista de marcas y protocolos concretos de la planta antes de prometerlo."),
   ("¿Requiere hardware especial?", "Sí. El material lista NeuroLink (hardware y software de recolección y cómputo en el borde), sensores inalámbricos WS Series, sistema de protección de vibración MPS5000 y colectores de datos. POR COMPLETAR: dimensionar el hardware del caso, que en el material viene como ejemplo de configuración (un servidor supOS y un servidor NeuroLink)."),
   ("¿Los modelos de IA son entrenables con nuestros datos?", "El material declara diagnóstico por modelos de IA y base de fallas propia del fabricante, con capacidades de autoadaptación y análisis de tendencia de los competidores. POR COMPLETAR — requiere validación: confirmar si el modelo se reentrena con datos del cliente y con qué esfuerzo."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos equipos rotativos, estáticos y eléctricos entran en el alcance?",
   "¿Qué criticidad tienen y cuáles son los equipos con más paradas no programadas?",
   "¿Qué marcas de instrumentos y válvulas hay que conectar y con qué protocolos?",
   "¿Ya existe supOS instalado en la planta? (PRIDE corre sobre supOS)",
   "¿Cuántas personas hacen hoy la inspección manual y cuántas horas dedican?",
   "¿Se requiere solo monitoreo y alerta, o también diagnóstico y recomendación de mantención?",
   "¿Se requiere hardware en el borde (NeuroLink) y sensores inalámbricos?",
   "¿Se van a aportar datos históricos de falla para entrenar o ajustar los modelos?",
 ],
 "fuente":"PRIDE Poster Foldout 20240524.pdf + PRIDE Solution-Vibration Monitoring and Early Warning of Rotating Equipment One Page Introduction 20240929.pdf + PRIDE Solution-Instruments Control One Page Introduction 20240929.pdf + PRIDE Solution for Instrumentation & Valve Introduction Slides 20240425.pptx",
}

# ======================= MP3000 ============================================
F["InPlant MP3000 (monitoreo y diagnóstico de equipos rotativos)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Software de monitoreo de condición y diagnóstico de equipos rotativos (unidades grandes, bombas y grupos de máquinas). Hace monitoreo inteligente y mantención predictiva, y busca digitalizar el ciclo de vida completo del equipo dinámico. Requiere ser soportado por los productos de hardware de monitoreo de SUPCON: sistema de protección de vibración MPS5000, colector de datos cableado con sus sensores cableados, gateway inteligente con sensores y transmisores inalámbricos, y cubiertas inteligentes.",
 "beneficios":[
   "Conexión directa con el sistema de control, el software industrial y la plataforma de información de SUPCON",
   "Interbloqueo de protección por vibración, monitoreo de estado en línea y diagnóstico de falla para unidades grandes",
   "Reduce la intensidad de inspección y mantención en grupos de máquinas y bombas y evita pérdidas por parada no programada",
   "Permite pasar de mantención programada y por falla a mantención predictiva y a gestión del ciclo de vida completo del equipo",
   "Procesamiento de datos robusto, análisis de falla profesional, modelo de licenciamiento flexible y soporte remoto de diagnóstico de falla",
   "Se puede embeber en plataformas de planta inteligente",
   "Casos citados: Sinopec Shanghai, Wanhua Chemical, Inner Mongolia Xingfa",
 ],
 "clientes_target":[
   "Petroquímica y química",
   "Energía y metalurgia",
   "Plantas con unidades grandes, bombas y grupos de máquinas críticos",
   "Plantas que quieren llevar la gestión de equipos a mantención predictiva",
 ],
 "competencia":"El material trae una comparación técnica por tipo de instrumento, no por marca de software: el tipo 'medidor de bastidor' (frame meter) monitorea fase clave, vibración y desplazamiento y manda la orden de parada al SIS por relé, con ventaja de procesamiento de señal rápido, alta precisión y amplia aplicabilidad, pero costo alto, configuración y gestión separadas y mucho espacio de instalación, con marcas típicas Bently, Emerson, Wuxi Houde, Jiangyin Zhonghe y Beijing Bohua; el tipo transmisor convierte fase clave, vibración y desplazamiento a 4-20 mA y lo manda al SIS, con ventaja de menor costo, aplicación simple y poco espacio, pero procesamiento lento, menor exactitud y aplicabilidad limitada, con marcas típicas Provibtech, Metrix, Wuxi Houde y Jiangyin Zhonghe. En Chile el segmento está dominado por Bently Nevada y Emerson (INFERENCIA — conocimiento general, consistente con las marcas típicas que cita el material).",
 "argumentos_venta":[
   "Se integra nativamente con el DCS, el software industrial y la plataforma de información de SUPCON, sin middleware adicional",
   "Resuelve el interbloqueo de protección por vibración, no solo el monitoreo: en unidades grandes eso es lo que exige el cliente",
   "Soporta hardware cableado e inalámbrico: se puede partir por lo inalámbrico en equipos secundarios y crecer a cableado en los críticos",
   "Modelo de licenciamiento flexible y soporte remoto de diagnóstico",
   "Casos citados en Sinopec Shanghai, Wanhua Chemical e Inner Mongolia Xingfa",
   "Requiere hardware de monitoreo SUPCON (MPS5000, colector, gateway y sensores WS Series): el proyecto se dimensiona junto con la instrumentación",
 ],
 "objeciones":[
   ("Ya tenemos Bently Nevada o Emerson en las unidades grandes", "El material reconoce a Bently y Emerson como marcas típicas del segmento de bastidor, y también reconoce sus desventajas: costo alto, configuración separada y espacio. La entrada realista es en bombas y equipos secundarios, no en la unidad grande ya instrumentada. POR COMPLETAR — requiere validación de integración con hardware de terceros."),
   ("¿Sirve con hardware que ya está instalado?", "El material dice que MP3000 V2.1 requiere ser soportado por los productos de hardware de monitoreo de SUPCON. Hay que revisar cuánto del hardware existente se reutiliza. POR COMPLETAR: confirmar alcance de hardware obligatorio."),
   ("¿Reemplaza a un especialista en vibraciones?", "El material declara análisis de falla profesional y soporte remoto de diagnóstico. No menciona reemplazo del especialista. POR COMPLETAR: definir el rol de soporte de diagnóstico remoto y sus tiempos."),
   ("¿Cuánto cuesta?", "El material revisado no publica lista de precios ni esquema de licenciamiento de MP3000. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos equipos rotativos entran en el alcance y de qué tipo (unidad grande, bomba, grupo)?",
   "¿Se requiere interbloqueo de protección por vibración sobre el SIS, o solo monitoreo?",
   "¿Qué hardware de monitoreo existe hoy y de qué marca?",
   "¿Se usará hardware cableado o inalámbrico?",
   "¿Se requiere integración con el DCS o el sistema de control existente?",
   "¿Cuáles son los eventos de parada no programada que se quieren evitar?",
   "¿Qué fase clave, vibración y desplazamiento se requiere medir por equipo?",
 ],
 "fuente":"InPlant MP3000 V2.10.00.00-M One-page Introduction 20231027.pdf + MPS5000 One Page Introduction-Sales 20241008.pptx",
}

# ======================= ESP-iSYS ==========================================
F["ESP-iSYS (base de datos en tiempo real)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Base de datos en tiempo real que actúa de puente entre la red de producción y la red de información. Entrega recolección de datos, almacenamiento, monitoreo por diagrama de flujo, alarma de proceso, reporte en tiempo real y cálculo estadístico. Se vende en versión Standard (recolección, almacenamiento y despliegue para pymes con presupuesto limitado) y versión Advanced (recolección, almacenamiento, cálculo, despliegue y alta disponibilidad, orientada a empresas medianas y grandes como alternativa de menor costo frente a PI/PHD).",
 "beneficios":[
   "La versión Standard opera con un solo servidor de 4 núcleos y 8 GB",
   "La versión Advanced con alta disponibilidad (hot standby) opera con dos servidores de 4 núcleos y 8 GB",
   "Almacena años de datos de producción de forma continua: permite extraer variaciones estacionales del proceso y analizar ciclos de producción",
   "Cálculo avanzado que convierte datos crudos en KPI de negocio (por ejemplo, tiempo de operación y de detención de equipos)",
   "Monitoreo por diagrama de flujo y tendencias en tiempo real para que la jefatura vea el proceso",
   "Es la capa de datos base para control avanzado, simulación de proceso, gestión de producción, gestión de energía y gestión de seguridad",
   "Autorización por puntos (TAG) y por tiempo de uso, con opción de suscripción anual o licencia perpetua",
 ],
 "clientes_target":[
   "Petroquímica y química",
   "Plantas que hoy no tienen base de datos histórica y necesitan una capa de datos",
   "Empresas medianas y grandes que quieren una alternativa de menor costo a PI/PHD",
   "Plantas que van a implementar APC, simulación, gestión de energía o gestión de seguridad y necesitan la base",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material revisado no trae battlecard de ESP-iSYS. Sí declara su posicionamiento como alternativa de menor costo frente a PI (OSIsoft/AVEVA PI) y PHD (Honeywell), que es una afirmación del fabricante y no una comparación con cifras. En el mercado chileno el segmento de historiador está dominado por AVEVA PI System y Honeywell PHD (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "Costo de infraestructura bajo y explícito: un servidor de 4 núcleos y 8 GB en la versión Standard, dos en la Advanced con hot standby",
   "Se posiciona como la alternativa económica a PI/PHD, sin licencia por tag de gran volumen ni servidores de gran porte",
   "Licenciamiento flexible: puntos (TAG) más tiempo de uso efectivo, con opción de suscripción anual o perpetuidad",
   "Es la puerta de entrada al resto del portafolio: sin historial de datos no hay APC, RTO ni gestión de energía",
   "Convierte datos crudos en KPI calculados (horas de operación, de detención) sin necesidad de un sistema adicional",
 ],
 "objeciones":[
   ("Ya tenemos PI System", "El material se posiciona como alternativa de menor costo, pero no trae comparación por función. El argumento es el costo de licencia e infraestructura. POR COMPLETAR — requiere validación de paridad funcional con PI y de esfuerzo de migración."),
   ("¿Aguanta el volumen de tags de toda la planta?", "El material no publica el número máximo de tags ni el rendimiento en la documentación revisada. POR COMPLETAR — requiere validación: pedir la cifra de tags soportados y el dimensionamiento por proyecto."),
   ("¿Cuántos servidores necesitamos?", "El material entrega dos configuraciones de referencia: un servidor de 4 núcleos y 8 GB para la versión Standard, y dos para la Advanced con hot standby. El dimensionamiento final depende de las tags."),
   ("¿Cuánto cuesta?", "El material revisado no publica lista de precios. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántas tags hay que recolectar y a qué frecuencia?",
   "¿Cuántos años de historia se deben almacenar?",
   "¿Qué fuentes de datos hay que recolectar (DCS, PLC, otros sistemas)?",
   "¿Se requiere alta disponibilidad con hot standby?",
   "¿Se requiere cálculo avanzado de KPI o solo recolección y despliegue?",
   "¿Se requiere integración con APC, simulación o gestión de energía a futuro?",
   "¿Se prefiere suscripción anual o licencia perpetua?",
 ],
 "fuente":"ESP i-SYS One Page Introduction 20240722.pptx",
}

# ======================= supOS =============================================
F["supOS (plataforma industrial / sistema operativo industrial)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Plataforma para la transformación digital industrial: conecta la infraestructura, gestiona y analiza el flujo de datos y permite construir aplicaciones. Incluye IoT industrial, big data e IA, y desarrollo de aplicaciones low-code, con casos en fábrica digital, centro de operación unificado (UOC), seguridad de producción, EAM y eficiencia de servicios. Se compone de módulos X-Collector (recolección), Data Lake distribuido, X-ETL (pipeline de datos), X-IDE (desarrollo de aplicaciones), X-DAM, X-BD y servicios de algoritmos X-AI.",
 "beneficios":[
   "Soporta más de 355 protocolos principales (OPC-DA/UA/AE, IEC104, Modbus TCP/RTU, SQL, ODBC/JDBC, MQTT, RESTful API, Web Service y otros) en la versión Professional",
   "Recepción unificada de datos heterogéneos: protocolos industriales, MQTT/gRPC, ODBC/JDBC, RESTful API, Kafka/MQ, archivos locales y Hive/HBase",
   "Conectores a sistemas de terceros: SAP, PI, MES, ERP, OA, SCM y CRM",
   "Modelamiento orientado a objetos de la fábrica digital: talleres, equipos, proceso, personas, productos, materias primas, vehículos y bodegas",
   "Servicio unificado de IA/ML: clasificación, clustering, regresión, predicción, optimización, más RNN/CNN/BP/LSTM, con pipeline de arrastrar y soltar y posibilidad de importar algoritmos propios de terceros",
   "Desarrollo de aplicaciones low-code con IDE configurable, biblioteca gráfica y flujo de trabajo basado en BPMN",
   "Acceso unificado con AD Sync, SSO y OIDC/OAuth2, con gestión de usuarios, roles y permisos",
   "Base tecnológica de otros productos del portafolio: PRIDE y Q-Lab corren sobre supOS",
 ],
 "clientes_target":[
   "Petroquímica, química y manufactura de proceso",
   "Plantas que quieren construir aplicaciones propias sobre una plataforma de datos unificada",
   "Clientes que ya invirtieron en MES, ERP y EMS y siguen con datos fragmentados",
   "Faenas con múltiples plantas o sitios que requieren una capa de datos común",
   "Proyectos de centro de operación unificado (UOC)",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material revisado no trae battlecard de supOS frente a plataformas IIoT de otros fabricantes. En Chile el espacio de plataforma industrial está disputado por AVEVA, PTC/ThingWorx, Siemens (MindSphere/Insights Hub) y AWS/Azure IoT (INFERENCIA — conocimiento general, no del material).",
 "argumentos_venta":[
   "355+ protocolos soportados en la versión Professional: cubre la mayoría del parque instalado sin desarrollo a medida",
   "Un solo punto de recolección para datos industriales, bases de datos, colas de mensajes y sistemas de terceros (SAP, PI, MES, ERP)",
   "Modelamiento por objetos de la fábrica: el dato queda con contexto, no como tag suelto",
   "Desarrollo low-code: el cliente construye sus propias aplicaciones sin depender del proveedor para cada cambio",
   "Importa algoritmos propios de terceros y permite entrenamiento offline de modelos de IA",
   "No es solo una plataforma: es la base sobre la que corren PRIDE y Q-Lab, así que la inversión se reutiliza",
   "El material lo posiciona como la capa que resuelve la fragmentación de datos que hace fracasar las iniciativas de IA (documento Tier 0: los sistemas existen, los datos no están conectados)",
 ],
 "objeciones":[
   ("Ya tenemos Azure IoT o AWS IoT", "El material no trae battlecard frente a nubes públicas. El argumento disponible es la orientación industrial (355+ protocolos, modelamiento por objetos de planta, conexión a SAP/PI/MES) frente a una plataforma genérica. POR COMPLETAR — requiere validación de arquitectura híbrida y despliegue on-premise."),
   ("¿Los datos salen de la planta?", "El material describe componentes desplegables (X-Collector, Data Lake, X-Edge para cómputo en el borde) y no obliga a nube pública en todos los casos, pero no se lee una declaración explícita de despliegue 100% on-premise para supOS. POR COMPLETAR — requiere validación con el fabricante."),
   ("No tenemos gente para desarrollar aplicaciones", "El material ofrece IDE configurable, herramientas gráficas y componentes, con entorno tipo asistente para bajar el umbral de TI del negocio. La promesa concreta es el desarrollo low-code, no que no haga falta nadie. POR COMPLETAR: definir horas de capacitación."),
   ("¿Cuánto cuesta la licencia?", "El material revisado no publica precios ni esquema de licenciamiento de supOS (sí lista los indicadores de performance de la versión Professional). POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Qué fuentes de datos hay que conectar y con qué protocolos?",
   "¿Cuál es el volumen de datos y la frecuencia de muestreo?",
   "¿El despliegue es on-premise, en nube o híbrido?",
   "¿Cuántos usuarios y cuántas aplicaciones se esperan construir?",
   "¿Se requiere modelamiento de objetos de la planta y de qué profundidad?",
   "¿Se requiere entrenamiento de modelos de IA propios?",
   "¿Qué sistemas de terceros hay que integrar (SAP, PI, MES, ERP, OA)?",
   "¿Se requiere SSO y directorio activo corporativo?",
 ],
 "fuente":"supOS Brochure.pdf (Process - Supcon1 y Process - Supcon4) + Tier 0 EAM Sharing.pdf + PRIDE Solution-Vibration Monitoring and Early Warning of Rotating Equipment One Page Introduction 20240929.pdf",
}

# ======================= Nyx / UCS =========================================
F["UCS Nyx (sistema de control universal)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Nyx es el primer producto basado en la arquitectura Universal Control System (UCS): un sistema de control definido por software, totalmente digitalizado y cloud-native, que reemplaza la arquitectura DCS tradicional. Se compone de un Control Data Center (con NyxOS, motor de control, monitoreo, herramientas de ingeniería y base de datos de series de tiempo), red óptica industrial Ethernet de 10 GB determinista y un ecosistema de campo digital con APL y SmartEIO. No tiene controlador ni IO dedicado: los recursos de control se definen por software en contenedores.",
 "beneficios":[
   "Elimina controlador y IO dedicados: 'software-defined' sobre servicios de control en contenedores",
   "Reduce 90% el cable de cobre, 80% la huella física y 50% el tiempo de proyecto (cifras del folleto Nyx)",
   "Retardo de planificación en tiempo real menor a 100 microsegundos sobre Linux endurecido",
   "Redundancia de 1:1 a 1:N y cobertura de falla del 99% con auto-recuperación de servicios de control",
   "Aplicaciones de IA incluidas: lazos PID con IA, predicción de eventos dentro de los próximos 5 minutos, generación de código y de gráficos por IA",
   "Conectividad APL: 2 hilos con alimentación, 10 MBit/s y 1000 m de cable, diseñado para seguridad intrínseca; un junction box APL de 96 puntos y un gabinete SmartEIO de 96 puntos",
   "Modelo de suscripción: para un proyecto típico de 10.000 puntos el material indica 398.000 CNY anuales, más 100.000 CNY por cada 10.000 puntos adicionales, con mínimo de 5 años y pago anual; el primer año es 12 meses pagados más 6 meses gratis",
   "Derechos del suscriptor: garantía de hardware del Control Data Center y actualizaciones de software gratis durante la suscripción, una evaluación de seguridad y diagnóstico de confiabilidad al año, y 10 días-persona de servicio de ingeniería al año (no acumulables)",
   "Estándar SmartEIO: 96 puntos por gabinete, con señales APL y convencionales",
 ],
 "clientes_target":[
   "Clientes innovadores y de alto valor, abiertos al modelo de licencia por suscripción",
   "Plantas nuevas o remodeladas con más de 5.000 puntos de IO",
   "Plantas con necesidad de escalabilidad",
   "Proyectos con plazo ajustado y requerimiento de eficiencia de ingeniería",
   "Plantas piloto o con posibles cambios de puntos de IO",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material revisado no trae battlecard de Nyx frente a un competidor equivalente. La comparación que hace el material es contra la arquitectura DCS tradicional en general (reemplaza un diseño de 50 años, elimina gabinetes de control y cuarto de control). No hay ningún otro fabricante con un producto comparable en el material. En Chile no hay sistema universal de control equivalente desplegado por los incumbentes (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "El argumento de arquitectura es radical y medible: -90% de cable de cobre, -80% de huella física y -50% de tiempo de proyecto según el folleto del fabricante",
   "No hay gabinetes de control ni cuarto de control ni cable de cobre: cambia el costo de infraestructura, no solo el de hardware",
   "Modelo de suscripción con cifra pública en el material: 398.000 CNY anuales para 10.000 puntos, con derechos del suscriptor incluidos (garantía, actualizaciones, evaluación anual y 10 días-persona de ingeniería)",
   "IA embebida: predicción de eventos dentro de los próximos 5 minutos y generación de código y gráficos por IA",
   "Se apunta a clientes abiertos al modelo de suscripción y a proyectos con escala sobre 5.000 puntos",
   "Nyx es el producto de mayor diferenciación tecnológica del catálogo: sirve para posicionar a SUPCON frente a cualquier DCS tradicional",
 ],
 "objeciones":[
   ("No voy a poner el control de mi planta en una nube", "El material describe el Control Data Center como centro de datos en sitio (con enfriamiento integrado, UPS y distribución de potencia, y cumplimiento de requisitos de data center), no como nube pública. Aclara este punto antes de discutir arquitectura. POR COMPLETAR: confirmar despliegue on-premise con el fabricante."),
   ("Sin controlador físico no hay control confiable", "El material declara redundancia de 1:1 a 1:N, cobertura de falla del 99%, auto-recuperación de servicios y retardo de planificación menor a 100 microsegundos sobre Linux endurecido. Son afirmaciones del fabricante, no de un despliegue chileno: pide referencias antes de comprometer."),
   ("El modelo de suscripción no nos sirve, queremos comprar", "El material ya separa el modelo: el hardware APL y SmartEIO se paga una vez con las mismas condiciones que un DCS, y la suscripción aplica al Control Data Center. Se puede licitar la parte de hardware tradicional."),
   ("¿Qué pasa si dejo de pagar la suscripción?", "El material declara mínimo de 5 años y pago anual, pero no describe el estado del sistema al término del contrato. POR COMPLETAR — requiere validación contractual, punto crítico."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos puntos de IO tiene el proyecto? (el modelo de suscripción se calcula por puntos)",
   "¿Es planta nueva o remodelación?",
   "¿El cliente acepta un modelo de suscripción de al menos 5 años?",
   "¿Se requiere seguridad intrínseca en campo? (APL está diseñado para ello)",
   "¿Cuántos gabinetes SmartEIO y junction box APL se requieren?",
   "¿Se requiere redundancia de 1:1 o de 1:N?",
   "¿Qué funciones de IA se quieren activar (PID con IA, predicción a 5 minutos, generación de código)?",
   "¿Se requiere integración con el DCS o sistemas existentes en la planta?",
 ],
 "fuente":"UCS Nyx Brochure 20240730.pdf + UCS Nyx One Page Introduction 20240730.pptx + UCS Nyx Introduction Slides - A Universal Way to Future Plant (Technics) 20240730.pptx + Next Gen Control System - Nyx UCS.pdf",
}

# ======================= TPT ===============================================
F["TPT (modelo de series de tiempo de industria de proceso)"] = {
 "familia":"Software de proceso",
 "descripcion":"Time-series Pre-trained Transformer: modelo de lenguaje grande de series de tiempo para la industria de proceso, desarrollado por SUPCON. Tiene doble capacidad de simulación y predicción: pronostica parámetros de proceso (temperatura, presión, caudal) y tendencias futuras de los equipos. Se divide en Production Supervisor Toolbox (TPT Supervisor, versión estándar): supervisión autónoma, predicción y alarma de parámetros de proceso, identificación de estado anormal de equipos, evaluación de eficiencia de producción en tiempo real, cálculo flexible de objetivos, y generación de información (chat IA, análisis de datos de producción, generación de reporte de planta); y Operation Optimization Toolbox (TPT Optimizer, versión premium): optimización autónoma, optimización y control de procesos complejos, optimización de parámetros PID, control inteligente, verificación de proceso y entrenamiento operacional.",
 "beneficios":[
   "El material declara ser el primer modelo grande de series de tiempo de la industria de proceso",
   "Cubre más de 10 tipos de aplicaciones de software industrial de la capa PA",
   "El material declara reducción de costo de software de 50% a 80%",
   "El material declara aumento de utilidad de 1% a 3%",
   "El material declara ahorro de costo laboral de 30% a 50%",
   "Predicción de eventos: supervisión autónoma con alarma predictiva de parámetros de proceso, salud de equipos, demanda de producción y consumo de energía",
   "Se reutiliza entre distintas unidades y condiciones con solo algo de dato histórico (capacidad de migración)",
   "Interacción en lenguaje natural: consulta de conocimiento (manuales, guías de operación, registros de mantención), reporte en tiempo real, análisis de datos cargados y entrenamiento de producción/operaciones",
 ],
 "clientes_target":[
   "Refinería, petroquímica y química",
   "Unidades donde el modelado tradicional es complejo o caro",
   "Plantas que quieren supervisión autónoma sin montar un proyecto de modelado por unidad",
   "Clientes que ya usan software industrial de la capa PA y quieren reducirlo",
   "Plantas con objetivos de reducción de costo de software y de personal",
 ],
 "competencia":"El material trae comparación: Huawei tiene fortalezas en reconocimiento de imagen y video pero sin historial en predicción de datos y sin experiencia en modelos grandes fuera de minería y química del carbón; Aliyun se concentra en la plataforma y deja el modelado al cliente o a expertos; Zhonggong Internet se enfoca en plataformas de IA y modelos de lenguaje generativos (generación de código, base de conocimiento de expertos) pero sin capacidad de predicción de datos ni de supervisión y optimización autónoma. En Chile el espacio de modelos de IA para industria de proceso está disputado por proveedores de hiperescaladores y consultoras, más las herramientas de los propios fabricantes de automatización (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "El material declara ser el primer modelo grande de series de tiempo de la industria de proceso: diferenciación clara frente a plataformas genéricas",
   "Beneficios cuantificados por el fabricante: -50% a -80% de costo de software, +1% a +3% de utilidad y -30% a -50% de costo laboral",
   "Un solo modelo para múltiples escenarios y unidades: evita un proyecto de modelado por unidad, que es el costo que el material atribuye a Aliyun",
   "Los competidores que cita el material no hacen predicción de datos ni supervisión y optimización autónoma; Huawei y Zhonggong están en otros nichos",
   "La versión estándar (Supervisor) ya entrega supervisión autónoma y reporte de planta sin necesidad de proyecto de optimización",
   "Interacción en lenguaje natural: el operador consulta en lenguaje normal, no en código",
 ],
 "objeciones":[
   ("¿Un modelo de IA va a operar mi planta?", "La versión estándar solo supervisa y alerta; la optimización (y el lazo cerrado) está en la versión premium. Se puede partir por supervisión y decidir después."),
   ("Nuestros datos son malos, el modelo va a fallar", "El material declara que el modelo se preentrena con datos masivos y aprende leyes de operación industrial, con capacidad de migración entre unidades. No elimina el requisito de datos: se necesita historial. POR COMPLETAR: definir el mínimo de datos históricos requerido por caso."),
   ("Los porcentajes de ahorro del material son de China", "Los beneficios declarados (-50% a -80% de costo de software, +1% a +3% de utilidad, -30% a -50% de costo laboral) son estimaciones del fabricante y no están ligados a un caso chileno. POR COMPLETAR — requiere caso de negocio local antes de prometerlos."),
   ("¿Se puede desplegar en nuestra infraestructura?", "El material describe TPT como software sobre el modelo TPT con interacción multimodal, pero no detalla el despliegue. POR COMPLETAR — requiere validación de requisitos de infraestructura."),
 ],
 "preguntas_tecnicas":[
   "¿Qué unidad o proceso se quiere supervisar?",
   "¿Cuántos años de datos históricos de proceso hay disponibles?",
   "¿El objetivo es supervisión y alerta, o optimización y lazo cerrado?",
   "¿Se requiere optimización de parámetros PID?",
   "¿Se requiere consultar documentación técnica en lenguaje natural?",
   "¿Qué infraestructura se usará (on-premise o nube)?",
   "¿Qué parámetros de proceso se quieren predecir (presión, temperatura, caudal, salud de equipo)?",
   "¿Se quiere integración con el DCS o con supOS?",
 ],
 "fuente":"TPT One Page Introduction V1.1.pptx + TPT Brochure.pdf + TPT Introduction Slides v6.1.pptx + TPT Sales Technical Manual 20240806.docx + TPT Introduction Slides 20240918.pptx",
}

# ======================= APEX ==============================================
F["APEX (simulación y diseño de procesos)"] = {
 "familia":"Software de proceso",
 "descripcion":"Advanced Process Engineering eXpert: software de simulación de proceso de nueva generación basado en tecnología orientada a ecuaciones, que modela y calcula procesos de la industria según primeros principios. Cubre el ciclo de vida completo desde la I+D de proceso hasta el diseño de ingeniería y la operación de planta, y es el modelo base para entrega digital, gemelo digital, planta inteligente y aplicaciones de IA. Es la pieza de modelado del paquete RTO.",
 "beneficios":[
   "Arquitectura B/S: no requiere instalación y permite modelado colaborativo",
   "Un mismo modelo central soporta cuatro modos de operación: simulación, calibración, reconciliación y optimización",
   "Modelado integrado estacionario y dinámico, con cambio suave entre ambos modelos",
   "Soporta conversión mutua con archivos de software de terceros para no remodelar desde cero",
   "Cubre refinería (destilación atmosférica, reforma continua, hidrocracking, cracking catalítico), petroquímica (PX, PTA, etileno, PO/SM), petróleo y gas, polímeros y química (amoníaco, carbón, metanol)",
   "Cubre el ciclo de vida completo: I+D de proceso, diseño de ingeniería y operación de planta",
   "Es la base de modelo del gemelo digital y del RTO",
 ],
 "clientes_target":[
   "Empresas de ingeniería (EPC) e institutos de investigación y universidades",
   "Empresas de manufactura de proceso que quieren gemelo digital",
   "Plantas que quieren verificar diseño o validar esquemas de control antes de invertir",
   "Proyectos de RTO (APEX es el modelo base del RTO)",
 ],
 "competencia":"El material trae la comparación de precios más completa del set: APEX se ofrece por niveles (Standard de 18 tokens, Professional de 98 tokens, Advanced de 208 tokens y RTO de 43 tokens); Aspen tiene licencia básica de 36 tokens a aproximadamente US$40.000 por usuario al año, unos US$1,75 millones a 5 años, enfocada en venta de producto sin equipo de ingeniería y con piratería extendida; ROMeo tiene licencia básica de 1,5 millones de CNY por usuario por 20 años. El material reconoce que APEX está en etapa de incubación, con madurez baja y funciones todavía en desarrollo. En Chile Aspen HYSYS y Aspen Plus son el estándar de facto en simulación de proceso (INFERENCIA — conocimiento general, consistente con el precio que cita el material).",
 "argumentos_venta":[
   "El diferencial de precio es enorme y está documentado en el material: frente a una licencia Aspen de aproximadamente US$40.000 por usuario al año, APEX se vende por niveles (Standard, Professional, Advanced y RTO)",
   "Un solo modelo central para cuatro modos (simulación, calibración, reconciliación y optimización): no hay que comprar ni mantener modelos separados",
   "Modelado integrado estacionario y dinámico: sirve para entrenamiento de operación, análisis de seguridad y validación de esquemas de control",
   "Arquitectura B/S sin instalación: facilita el modelado colaborativo entre EPC, cliente y fabricante",
   "Conversión de archivos de software de terceros: baja el costo de adopción desde Aspen",
   "Se vende como producto a EPC, institutos y universidades, y como solución a plantas, o en co-creación con el cliente",
 ],
 "objeciones":[
   ("APEX es nuevo y no está probado", "Es verdad y el propio material lo dice: APEX está en etapa de incubación, con madurez baja y algunas funciones en desarrollo. No lo ocultes: propone un piloto acotado y compara los resultados con el simulador que el cliente ya usa."),
   ("Nuestros modelos están todos en Aspen HYSYS", "El material declara conversión mutua con archivos de terceros. POR COMPLETAR: confirmar contra qué versiones de Aspen y de ROMeo se ha validado la conversión y con cuánta pérdida de fidelidad."),
   ("Aspen es el estándar de la industria y todos lo conocen", "El costo es el argumento del material: Aspen cobra por usuario y por año. APEX por niveles. El cálculo se hace con las cifras que el propio material publica. No prometas superioridad funcional: promete costo y modo de licenciamiento."),
   ("Necesitamos los bancos de propiedades de Aspen", "El material no hace ninguna afirmación sobre bancos de propiedades ni componentes. POR COMPLETAR — requiere validación con el fabricante antes de ofrecer el producto para casos con química compleja."),
 ],
 "preguntas_tecnicas":[
   "¿El uso es diseño de ingeniería (EPC), operación de planta, o ambos?",
   "¿Qué procesos hay que modelar (refinería, petroquímica, polímeros, química)?",
   "¿Se requiere modo dinámico además de estacionario?",
   "¿Se requiere calibración y reconciliación con datos de planta?",
   "¿Qué simulador usan hoy y en qué versiones?",
   "¿Cuántos usuarios de modelado habrá?",
   "¿Se requiere el banco de propiedades para componentes y mezclas específicas?",
   "¿El objetivo incluye RTO (y por tanto la integración con APC)?",
 ],
 "fuente":"Advanced Process Engineering eXpert APEX V3.0 Product One Page Introduction - Sales.pptx + APEX V2.01.00.00-M Sales Technical Manual 20240603.pdf + APEX Poster Foldout 20240528.pdf",
}

# ======================= OMC ===============================================
F["OMC (Intelligent Operation Management & Control System)"] = {
 "familia":"Plataforma y gestión",
 "descripcion":"Intelligent Operation Management & Control System: producto de nivel plataforma que integra profundamente el DCS con el software industrial. Su Centro de Aplicaciones Inteligentes actúa como hub de servicios de distintos softwares industriales (IDM, AAS, Pilot, APC y otros), administra el arranque y la parada de los servicios de aplicación y el almacenamiento de datos, y transmite datos entre el DCS y el software por un bus suave cifrado y seguro, en lugar de OPC tradicional. La estación de operación inteligente reemplaza la estación de operador tradicional y los clientes de software múltiples, con cuenta, permisos de configuración de ingeniería y acceso a pantallas bajo un mismo físico. Tiene versiones Standard, Enhanced y Advanced, todas con upgrade sin discontinuidad: Standard incluye todas las capacidades del ECS-700; Enhanced habilita operación autónoma, eficiencia y menor consumo; Advanced logra optimización en tiempo real, operacional y de programación.",
 "beneficios":[
   "Integra DCS y software industrial por un bus suave cifrado en lugar de OPC: el material lo presenta como más eficiente y más seguro que el modelo tradicional",
   "La versión Standard incluye todas las capacidades del ECS-700 a costo comparable",
   "Las tres versiones tienen upgrade sin discontinuidad (Standard, Enhanced y Advanced)",
   "Estación de operación única con cuenta unificada, permisos de ingeniería y entrada a pantallas de monitoreo en un mismo computador físico",
   "Se ubica en las capas L2 y L2.5, cerca de instrumentación, producción y proceso",
   "Apunta a reducción de costo, eficiencia y autonomía operativa según la versión",
 ],
 "clientes_target":[
   "Petroquímica y química como industrias clave, con promoción a toda la industria",
   "Versiones Enhanced y Advanced: alta dirección (gerente general, vicepresidente de producción y abastecimiento, jefe de ingeniería), para hablar de costo, eficiencia e indicadores económicos",
   "Versión Standard: clientes con aspiraciones de desarrollo muy bajas, presupuesto muy pequeño y solo automatización básica",
   "Clientes que quieren que la estructura OMC quede escrita en las bases de licitación",
 ],
 "competencia":"El material es explícito: la ventaja del arquitectura OMC frente a competidores es la integración software más hardware. Reconoce que los componentes individuales pueden ser inferiores a los de competidores internacionales, pero que el software extranjero se desarrolla y mantiene de forma independiente a través de adquisiciones de filiales, por lo que no puede lograr esa integración. Sobre competidores domésticos chinos dice que no tienen un sistema de software industrial tan completo y que la mayoría son contratistas generales o agentes de software de otros fabricantes, con costo alto y servicio inconsistente. Es una afirmación de posicionamiento, sin cifras: POR COMPLETAR — requiere validación. En Chile los incumbentes (Emerson, Honeywell, ABB, Siemens, Yokogawa) venden DCS más suites propias con integración, lo que debilita este argumento localmente (INFERENCIA — conocimiento general).",
 "argumentos_venta":[
   "El argumento es integración, no mejor componente: el material reconoce honestamente que los componentes individuales pueden ser inferiores a los competidores internacionales",
   "El bus suave cifrado entre DCS y software reemplaza el OPC tradicional: menos puntos de integración y menos superficie de falla",
   "La versión Standard es el ECS-700 completo a costo comparable: para el cliente que solo quiere automatización básica no hay que argumentar arquitectura",
   "Estación de operación única: menos computadores, menos clientes de software, cuenta y permisos unificados en sala de control",
   "El upgrade entre versiones no tiene discontinuidad: se puede entrar por Standard y crecer a Enhanced o Advanced sin cambiar de producto",
   "El material define explícitamente con quién hablar en cada versión: con la alta dirección para Enhanced y Advanced (costo, eficiencia, indicadores) y no con el jefe de taller sobre reducción de personal",
 ],
 "objeciones":[
   ("Emerson y Honeywell ya venden DCS más software integrado", "El material sostiene que el software de los competidores internacionales viene de filiales adquiridas y no logra integración real. Es una afirmación del fabricante, no un dato verificado: POR COMPLETAR — requiere validación. Para Chile, asume que ese argumento es débil y compite por costo y cobertura funcional."),
   ("Los componentes chinos son inferiores", "El propio material reconoce que los componentes individuales pueden no ser tan buenos como los de los competidores internacionales. No lo niegues: vende la integración y el costo total, y compara funcionalidad por componente solo donde SUPCON tenga ventaja."),
   ("¿Por qué no comprar solo el DCS y el software por separado?", "El argumento del material es que OMC evita el OPC tradicional entre DCS y software, con bus suave cifrado. Ese es el caso técnico: se cobra en menos integraciones y menos riesgo."),
   ("¿Cuánto cuesta OMC?", "El material revisado no publica lista de precios ni esquema de licenciamiento de OMC. Sí indica que la versión Standard es de costo comparable al ECS-700. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Es una planta nueva o ya tiene DCS instalado?",
   "Si ya tiene DCS: ¿es ECS-700 o de otra marca?",
   "¿Qué software industrial se quiere integrar (APC, IDM, AAS, Pilot, otros)?",
   "¿Cuántas estaciones de operación y cuántos clientes de software hay que reemplazar?",
   "¿El cliente busca automatización básica, operación autónoma, u optimización en tiempo real?",
   "¿Se requiere el hub de aplicaciones inteligentes con administración de servicios?",
   "¿Cuántos usuarios de operación tiene la planta?",
 ],
 "fuente":"OMC One Page Introduction-Sales 20240630.pptx + OMC Poster Foldout 20240630.pdf + OMC Poster Foldout (Standard) 20240630.pdf + Presentacion_ENAP_IA_v4.pptx",
}

# ======================= Ciberseguridad OT ================================
F["Sistema de ciberseguridad industrial (ICS Security Management Platform + VxDefenderPro)"] = {
 "familia":"Ciberseguridad OT",
 "descripcion":"Sistema de ciberseguridad industrial compuesto por la Plataforma de Gestión de Seguridad ICS y el software de protección de host industrial InPlant Defender Pro (VxDefenderPro). La plataforma gestiona de forma unificada los productos de seguridad industrial de SUPCON (VxDefenderPro, Firewall Industrial, Diodo de Datos Industrial, Plataforma de Diagnóstico de Red y Sistema de Monitoreo y Auditoría de Red Industrial), con gestión de activos, configuración unificada, inmunidad de grupo, gestión de parches, análisis de eventos y auditoría de registros. VxDefenderPro protege el host industrial con lista blanca de programas, lista blanca de red (puerto más programa), escaneo y eliminación de virus, control de acceso obligatorio (MAC, modelos BLP y BIBA), línea base de seguridad, USB seguro, gestión de parches, inmunidad de grupo y medición dinámica de integridad.",
 "beneficios":[
   "Gestión centralizada de todos los productos de seguridad industrial del fabricante desde una sola plataforma",
   "Monitoreo del estado de riesgo con evaluación de valor de activo, vulnerabilidad y amenaza, y ranking de riesgo por activo",
   "Inmunidad de grupo: cuando un cliente detecta un virus, la política de seguridad se despliega en todos los clientes",
   "Gestión de parches con actualización de un clic, sin servidor de parches independiente",
   "Diodo de datos industrial para separar redes; firewall industrial y sistema de monitoreo y auditoría de red incluidos en el portafolio gestionado",
   "Análisis dinámico de comportamiento en sandbox virtual durante el escaneo (desempaquetado y análisis de comportamiento)",
   "USB seguro para acceso de emergencia al host industrial, bloqueando el uso de memorias no confiables",
   "Despliegue distribuido con gestión centralizada por la plataforma supervisora, para escenarios discretos y redes industriales jerárquicas grandes",
   "VxDefenderPro se vende con pago único; las actualizaciones de la base antivirus son gratuitas cada seis meses durante la garantía",
 ],
 "clientes_target":[
   "Petroquímica y química",
   "Energía eléctrica",
   "Protección ambiental, agricultura, transporte marítimo, hierro y acero, y celulosa y papel",
   "Plantas con estaciones de ingeniería, estaciones de operador, servidores SCADA, de base de datos y OPC que deben protegerse",
   "Empresas que necesitan cumplir requisitos de ciberseguridad OT (trazabilidad, auditoría de registros, gestión de vulnerabilidades)",
 ],
 "competencia":"POR COMPLETAR — requiere validación: el material no trae battlecard de ciberseguridad OT (ni precios ni comparación con competidores). En el mercado chileno el segmento de ciberseguridad OT está cubierto por Claroty, Nozomi Networks, Tenable OT, Fortinet y las suites de los propios fabricantes de automatización; además, la normativa local empuja el cumplimiento (Ley 21.663 y las exigencias sectoriales del Coordinador Eléctrico Nacional en el sector eléctrico) (INFERENCIA — conocimiento general, no del material).",
 "argumentos_venta":[
   "La serie de productos tiene certificación IEC 62443: el material incluye certificados IEC 62443-4-1 y 4-2 (SL1) y de capacidad de servicio de integración IEC 62443-2-4 para TCS-900 y ECS-700, con vigencia hasta marzo de 2027",
   "VxDefenderPro se vende con pago único y la actualización de la base antivirus es gratuita cada 6 meses durante la garantía: costo total más bajo que una suscripción anual",
   "Inmunidad de grupo: una detección en un host protege a todos los hosts de la red, sin intervención manual host por host",
   "Gestión de parches con un clic, sin servidor de parches independiente: reduce el esfuerzo de mantención de la red OT",
   "El portafolio es más que antivirus: firewall industrial, diodo de datos y sistema de monitoreo y auditoría de red, con gestión centralizada desde una plataforma",
   "El bloqueo por lista blanca de programas y scripts detiene la ejecución de software desconocido, que es el vector típico de un ataque a una estación de ingeniería",
   "Se puede desplegar en capas (plataforma supervisora para varias plataformas) y crecer con la red",
 ],
 "objeciones":[
   ("Un antivirus en mi estación de ingeniería me va a romper el sistema", "El material responde a eso explícitamente: el antivirus tradicional no es adecuado para un IPC industrial, y VxDefenderPro trabaja con lista blanca de programas y de red más línea base, con gestión de parches que valida compatibilidad antes de instalar. El piloto se hace primero en una estación no crítica."),
   ("¿Cumple la normativa chilena?", "El material entrega certificados IEC 62443 (4-1, 4-2 y 2-4), que son estándar internacional, pero no menciona normativa chilena específica. POR COMPLETAR — requiere validación local: contrastar con Ley 21.663, con los requisitos del Coordinador Eléctrico Nacional y con lo que exija la SEC según el segmento."),
   ("Ya tenemos firewall perimetral corporativo", "El material distingue el firewall industrial y el diodo de datos industrial dentro del portafolio gestionado: la protección del host y del piso OT es distinta de la del perímetro corporativo. Pide el esquema de red del cliente antes de proponer."),
   ("¿Cuánto cuesta?", "El material revisado no publica precios de la plataforma de gestión ni de VxDefenderPro. Sí indica que Defender Pro es pago único con actualizaciones gratuitas cada 6 meses durante la garantía. POR COMPLETAR — requiere cotización del fabricante."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos hosts industriales hay que proteger (estaciones de ingeniería, de operador, servidores SCADA, de base de datos, OPC)?",
   "¿Cuántas redes o segmentos hay que cubrir?",
   "¿Se requiere firewall industrial, diodo de datos, o ambos?",
   "¿Se requiere sistema de monitoreo y auditoría de red?",
   "¿Se requiere gestión centralizada con plataforma supervisora para varias subredes?",
   "¿El cliente requiere trazabilidad y auditoría de registros por normativa?",
   "¿Los sistemas operativos de los hosts son compatibles con la versión ofrecida?",
   "¿Hay un esquema de red vigente y una política de ciberseguridad corporativa que respetar?",
 ],
 "fuente":"Industrial Cybersecurity System.pdf + InPlant Defender Pro V3.0 One Page Introduction 20241014.pptx + DCS-ECS-700 IEC62443-3-3 SL1 + TCS-900 IEC62443-4-1&2 SL1 + TCS-900 IEC62443-2-4 (certificados del material de certificación)",
}

# ===========================================================================
DATA = {
 "titulo":"Fichas de Producto SUPCON — Software y plataforma",
 "generado_desde":"datos/software_extraido.json (163 documentos, deduplicados por MD5)",
 "nota":"Cada dato de cada ficha proviene de un documento real del fabricante, citado en el campo 'fuente'. Los campos sin respaldo en el material quedan marcados 'POR COMPLETAR'. La 'competencia' se marca como inferencia cuando proviene de conocimiento general y no del material.",
 "fichas":F,
}

os.makedirs(DATOS, exist_ok=True)
SAL = os.path.join(DATOS, "fichas_4_datos.json")
with open(SAL, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)

print(f"escrito: {SAL}")
print(f"fichas: {len(F)}")
for n, f in F.items():
    falt = sum(1 for k in ("descripcion","competencia") if "POR COMPLETAR" in str(f.get(k,"")))
    falt += sum(1 for v in list(f["beneficios"])+list(f["argumentos_venta"]) if "POR COMPLETAR" in str(v))
    falt += sum(1 for o in f["objeciones"] for x in o if "POR COMPLETAR" in str(x))
    print(f"  [{f['familia']}] {n}  (beneficios={len(f['beneficios'])}, "
          f"clientes={len(f['clientes_target'])}, argumentos={len(f['argumentos_venta'])}, "
          f"objeciones={len(f['objeciones'])}, preguntas={len(f['preguntas_tecnicas'])}, "
          f"menciones POR COMPLETAR={falt})")
tot_pc = sum(1 for f in F.values() if "POR COMPLETAR" in json.dumps(f, ensure_ascii=False))
print(f"\nTOTAL fichas: {len(F)} | con campos POR COMPLETAR: {tot_pc}")
