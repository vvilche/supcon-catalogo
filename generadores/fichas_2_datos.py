#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FICHAS COMERCIALES - SEGUNDA ENTREGA (familias SIS, PLC, CCS, Software, Plataforma, Ciber).

Complementa generar_fichas_producto.py (que tiene los 6 analizadores).
Mismo formato de 8 campos. Cada dato viene del material del fabricante extraido en
datos/fichas_extraidas.json. Lo que no tiene respaldo va marcado POR COMPLETAR.

Uso:  python3 generar_fichas_2.py
Salida: artefactos/fichas_producto_2.html
"""
import os, json, html as H

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")
SALIDA = os.path.join(BASE, "artefactos")

def esc(s): return H.escape(str(s))

# ===========================================================================
# FICHAS (8 campos). Datos tomados del material del fabricante.
# ===========================================================================
F = {}

# ------------------------------- SIS ---------------------------------------
F["TCS-900 (SIS)"] = {
 "familia":"Seguridad (SIS)",
 "descripcion":"Sistema Instrumentado de Seguridad (SIS) de gran escala que combina seguridad funcional y ciberseguridad. Arquitectura TMR (triple redundante modular) con redundancia dual de trabajo, que garantiza operación continua. Diseñado para parada de emergencia (ESD/SIS), control de compresores (CCS/ITCC/TMC), detección de fuego y gas (F&GS/GDS), gestión de quemadores (BMS) y protección de alta integridad por sobrepresión (HIPPS).",
 "beneficios":[
   "Disponibilidad de 99,999% con baja probabilidad de disparo espurio",
   "Arquitectura TMR con redundancia dual de trabajo: operación continua",
   "Cumple IEC 61508 e IEC 61511; certificado SIL3",
   "Integración sin fricción con el DCS (configuración y monitoreo)",
   "Descarga y ampliación de configuración en línea, sin detener el proceso",
   "Prueba de carrera completa y prueba de carrera parcial (PST)",
   "Alta adaptabilidad ambiental, bus de E/S de alta velocidad y expansión flexible",
   "Registro de aplicación de 6.700 unidades",
 ],
 "clientes_target":[
   "Refinería e integración petroquímica (grandes aplicaciones)",
   "Producción química continua",
   "Plantas de proceso con riesgo de sobrepresión, fuego o gas",
   "Unidades con compresores accionados por turbina de vapor, turbina de gas o motor",
   "Plantas con obligación de SIL3 por análisis de riesgo (HAZOP/LOPA)",
 ],
 "competencia":"POR COMPLETAR — requiere validación. Referencia interna: PRIDE y el material de software declaran haber enfrentado a Honeywell en proyectos de optimización de lazos (mencionado literalmente en la ficha de InPlant PID como competidor con 'evaluación completa de índices, buena presentación, pero baja localización').",
 "argumentos_venta":[
   "6.700 unidades de aplicación acumuladas: es el argumento de track record más duro del catálogo",
   "Certificación SIL3 por TÜV Rheinland sobre arquitectura TMR",
   "Disponibilidad 99,999% con baja tasa de disparo espurio: responde directo a la objeción de que un SIS 'para la planta sin necesidad'",
   "Integración nativa con el DCS de la misma marca: menos puntos de falla y una sola ingeniería",
   "Permite descarga en línea: el cliente no tiene que detener la planta para cambiar la lógica",
   "Cubre 5 aplicaciones distintas (ESD, CCS, F&GS, BMS, HIPPS) con una misma plataforma: un solo estándar de ingeniería y repuestos para toda la planta",
   "SILSight: monitoreo en línea del riesgo de seguridad",
 ],
 "objeciones":[
   ("Un SIS nos va a parar la planta sin necesidad","La arquitectura TMR con redundancia dual de trabajo está diseñada exactamente para eso: 99,999% de disponibilidad con baja probabilidad de disparo espurio. Un canal puede fallar y el sistema sigue operando, con el canal aislado y diagnosticado."),
   ("Ya tenemos el DCS, no queremos otro sistema","La integración con el DCS es nativa. Comparte configuración y monitoreo, y se puede hacer la ingeniería de ambos en un solo entorno."),
   ("Cambiar la lógica exige parar la planta","Soporta descarga y expansión en línea: se modifica la configuración sin detener el proceso."),
   ("¿Cómo verificamos que el SIS realmente funciona?","Tiene prueba de carrera completa y prueba de carrera parcial (PST) sobre las válvulas de parada, más el software SILSight para monitoreo del riesgo en línea."),
   ("Es caro comparado con una solución simple de relés","POR COMPLETAR — no hay precio en el material. El argumento correcto se construye con el costo del evento que el SIS evita (análisis de riesgo de la planta), no con el precio de los equipos."),
 ],
 "preguntas_tecnicas":[
   "¿Cuál es el nivel SIL que exige el análisis de riesgo (HAZOP/LOPA) para cada lazo?",
   "¿Qué aplicaciones debe cubrir: ESD, CCS, F&GS, BMS, HIPPS? (la plataforma cubre las cinco)",
   "¿Cuántos lazos de seguridad y cuántas E/S (AI, AO, DI, DO) requiere?",
   "¿Cuál es la arquitectura requerida: TMR o es suficiente redundancia dual?",
   "¿Se requiere certificación SIL3 para toda la planta o por lazo?",
   "¿Debe integrarse con un DCS existente? ¿De qué marca y versión?",
   "¿Requiere prueba de carrera parcial (PST) en válvulas ESD?",
   "¿Necesita monitoreo de riesgo de seguridad en línea (SILSight)?",
   "¿Qué condiciones ambientales y de zona peligrosa aplican?",
   "¿Se requiere capacitación del personal de operación y mantenimiento?",
 ],
 "fuente":"TCS-900 One Page Introduction-Sales 20240630.pptx + SUPCON SIS Product_20250602v3.pdf",
}

F["TCS-500 (SIS)"] = {
 "familia":"Seguridad (SIS)",
 "descripcion":"Sistema instrumentado de seguridad flexible y de alta densidad, basado en tecnología QMR (cuádruple redundante modular). Certificado SIL3 conforme a IEC 61508. Diseñado para aplicaciones de seguridad con espacio limitado, restricciones de instalación y límites de volumen y peso.",
 "beneficios":[
   "Arquitectura QMR/DMR, certificado SIL3 (IEC 61508)",
   "Totalmente redundante, con disponibilidad 99,999% y baja probabilidad de disparo espurio",
   "Configuraciones flexibles: redundante y no redundante",
   "Diversas arquitecturas de E/S y formas de entrada de cable",
   "Diseño compacto y de alta densidad: 480 x 298 x 145 mm",
   "Multiestación sin fricción",
 ],
 "clientes_target":[
   "Oil and gas, almacenamiento y transporte",
   "Química fina",
   "Metalurgia",
   "Farmacéutica",
   "Plantas con restricción de espacio para el sistema de seguridad",
   "Aplicaciones de parada de emergencia (SIS/ESD) y detección de fuego y gas (FGS/GDS)",
 ],
 "competencia":"POR COMPLETAR — requiere validación. No hay battlecard en el material.",
 "argumentos_venta":[
   "Certificación SIL3 con arquitectura QMR: el grado más alto de redundancia de la línea",
   "Es la opción cuando el espacio manda: 480 x 298 x 145 mm permite instalar seguridad SIL3 donde un TMR de rack no cabe",
   "Flexibilidad de configuración: el cliente puede empezar no redundante y escalar a redundante",
   "Misma familia que el TCS-900: si el cliente ya usa TCS-900, la ingeniería y la capacitación se reutilizan",
   "Cubre SIS/ESD y FGS/GDS con la misma plataforma",
 ],
 "objeciones":[
   ("Es un sistema chico, ¿aguanta una aplicación grande?","Es de alta densidad, no de baja capacidad: el formato es compacto justamente para concentrar muchos puntos. Si la aplicación es de gran escala con miles de E/S, la plataforma correcta es el TCS-900."),
   ("¿Por qué QMR y no TMR?","QMR significa cuádruple redundante modular: tolera más fallas que una arquitectura triple. Es el grado más alto de la línea y está certificado SIL3."),
   ("Restricción de espacio y de peso en la instalación","Es exactamente el caso de diseño: las dimensiones y el peso están pensados para instalaciones con restricciones de volumen."),
   ("POR COMPLETAR — el material no documenta más objeciones",""),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos puntos de E/S requiere el sistema? (define si aplica TCS-500 o TCS-900)",
   "¿Cuál es el espacio disponible en el gabinete o sala?",
   "¿Hay restricción de peso en la instalación?",
   "¿Requiere configuración redundante o no redundante?",
   "¿Qué tipo de entrada de cable requiere la instalación?",
   "¿Cuál es el nivel SIL exigido por el análisis de riesgo?",
   "¿Debe cubrir parada de emergencia, fuego y gas, o ambos?",
   "¿Se integra con un DCS existente? ¿De qué marca?",
   "¿Qué condiciones ambientales y zona peligrosa aplican?",
   "¿Requiere multiestación (varias salas de operación)?",
 ],
 "fuente":"TCS-500 One-Page Introduction 20240816.pdf + TCS-500 Selection Guide 20240816.pdf",
}

# ------------------------------- PLC ---------------------------------------
F["G5Pro (PLC)"] = {
 "familia":"PLC",
 "descripcion":"Sistema PLC de gran escala, alta confiabilidad y alto desempeño, perteneciente a la plataforma de control GCS con arquitectura de comunicación basada en el protocolo UCP. Diseñado para controlar uno o varios objetos: múltiples equipos, una línea de producción o una planta completa. Envía los resultados de medición al sistema de control y al sistema de parada de emergencia, permitiendo monitorear y analizar el estado de equipos críticos.",
 "beneficios":[
   "Hardware totalmente redundante y cobertura de diagnóstico de fallas superior al 90%",
   "Componentes y redes soportan modo redundante",
   "Diseño de doble núcleo 'control + red': seguridad de la información de red en tiempo real con control seguro y confiable",
   "Grado industrial de temperatura amplia, resistencia a corrosión G3 y nivel EMC 3: apto para ambientes severos",
   "Basado en protocolo UCP, permite construir topologías de red flexibles: anillo simple, doble anillo, estrella",
   "Red industrial Ethernet segura y de comunicación en tiempo real",
   "Capacidad de red múltiple: soporta aplicaciones distribuidas sobre red inalámbrica y red pública",
   "Topología de red redundante: estrella, bus, anillo y cadena tipo margarita",
   "Sistema operativo multitarea con operación por ciclo periódico, cíclico y por evento; integra control de proceso, por lotes, discreta, de accionamiento y de movimiento",
 ],
 "clientes_target":[
   "Oil and gas y ductos",
   "Transporte ferroviario",
   "Red de calefacción y suministro inteligente de agua",
   "Tratamiento de aguas residuales",
   "Túneles de tráfico y túneles de servicios (utility tunnel)",
   "Energía nuclear",
   "Paquetes de equipo (equipment package)",
 ],
 "competencia":"POR COMPLETAR — requiere validación. No hay battlecard en el material.",
 "argumentos_venta":[
   "Cobertura de diagnóstico de fallas sobre 90% con hardware totalmente redundante: la disponibilidad es el argumento",
   "Doble núcleo control+red: resuelve a la vez el control confiable y la ciberseguridad de red, que suelen venderse por separado",
   "Calificación ambiental para ambientes severos: temperatura amplia, corrosión G3 y EMC nivel 3",
   "Flexibilidad de topología de red (anillo, doble anillo, estrella, cadena): se adapta a la traza existente sin rediseñar la red",
   "Multitarea integrada: proceso, lotes, discreta, accionamiento y movimiento en un mismo controlador",
   "Variante G5Pro Safety certificada SIL3 para la misma instalación",
 ],
 "objeciones":[
   ("¿Es un PLC o un DCS? No queremos confundir arquitecturas","Es un PLC de gran escala: controla desde un equipo hasta una planta completa. Si la aplicación exige control distribuido con unidades de proceso separadas, la plataforma correcta es el DCS ECS-700."),
   ("El ambiente de la planta es muy severo","Está calificado para eso: grado industrial de temperatura amplia, resistencia a corrosión G3 y EMC nivel 3."),
   ("Necesitamos seguridad funcional en la misma instalación","Existe la variante G5Pro Safety, certificada SIL3, sobre la misma plataforma y con la misma ingeniería."),
   ("La red que tenemos es vieja y no es en anillo","Soporta estrella, bus, anillo y cadena tipo margarita. Se adapta a la topología existente."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿Qué debe controlar: un equipo, una línea o la planta completa?",
   "¿Cuántos puntos de E/S requiere y de qué tipo (AI, AO, DI, DO)?",
   "¿Requiere redundancia de CPU, de red y de fuentes?",
   "¿Cuál es la topología de red disponible en la planta?",
   "¿Cuál es la temperatura ambiente y el grado de corrosión del sitio?",
   "¿Requiere seguridad funcional (SIL) además del control? (evaluar G5Pro Safety)",
   "¿Debe comunicarse con otros sistemas? ¿Qué protocolos?",
   "¿Cuántas estaciones de operación y de ingeniería se requieren?",
   "¿Requiere aplicación distribuidas sobre red inalámbrica o pública?",
   "¿Es un equipo nuevo o un reemplazo de un sistema existente?",
 ],
 "fuente":"G5Pro One-Page Introduction-Sales 20240530.pptx + G5Pro PLC System Catalog.pdf (OCR) + G5Pro Selection Guide 20240418.pdf",
}

F["G3Smart (PLC)"] = {
 "familia":"PLC",
 "descripcion":"Controlador diseñado para manejar puntos de E/S de alta densidad, adecuado para escenarios de aplicación compactos y distribuidos. Permite la conexión sin fricción de datos de software y hardware de los sistemas GCS-G3 y GCS-G5. Sus E/S también pueden funcionar como E/S remotas del sistema G5Pro para lograr expansión remota.",
 "beneficios":[
   "Alta densidad de E/S: formato compacto para aplicaciones distribuidas",
   "Conexión sin fricción con los sistemas GCS-G3 y GCS-G5: protege la inversión existente",
   "Las E/S funcionan como remotas del G5Pro: expansión remota sin cambiar el controlador principal",
   "Opción costo-efectiva frente a un controlador de mayor porte",
   "Multitarea con tipos de tarea diversos: de arranque, periódica, cíclica y por evento",
   "Programación estándar IEC 61131-3: LD, FBD, SFC, ST",
   "Configuración de comunicación simple para mejorar la eficiencia de ingeniería",
   "Temperatura de operación extendida y resistencia a corrosión G3",
 ],
 "clientes_target":[
   "Petroquímica y química fina",
   "Química del carbón",
   "Oil and gas",
   "Ingeniería municipal",
   "Metalurgia",
   "Farmacéutica",
   "Plantas que requieren expansión remota de E/S sin cambiar el controlador principal",
 ],
 "competencia":"POR COMPLETAR — requiere validación. No hay battlecard en el material.",
 "argumentos_venta":[
   "Conecta sin fricción con GCS-G3 y GCS-G5: el cliente que ya tiene esa plataforma no rehace la ingeniería",
   "Sus E/S sirven como remotas del G5Pro: permite expandir una instalación existente sin tocar el controlador principal",
   "Opción costo-efectiva: no sobra capacidad donde no se necesita",
   "Programación estándar IEC 61131-3, que el personal de mantenimiento ya conoce",
   "Calificación ambiental extendida con resistencia a corrosión G3",
 ],
 "objeciones":[
   ("Necesitamos expandir una instalación existente sin parar","Sus E/S funcionan como remotas del G5Pro: se expande la instalación agregando módulos, sin reemplazar el controlador principal."),
   ("Nuestro personal solo conoce programación estándar","Usa los lenguajes estándar IEC 61131-3: LD, FBD, SFC y ST. No requiere capacitación en un lenguaje propietario."),
   ("Es una plataforma chica para nuestra aplicación","Es de alta densidad y formato compacto, pensado para aplicaciones distribuidas. Si la aplicación es centralizada y de gran porte, la plataforma correcta es el G5Pro."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos puntos de E/S requiere?",
   "¿La aplicación es compacta y localizada, o distribuida en varios puntos de la planta?",
   "¿Ya tiene un sistema GCS-G3 o GCS-G5 instalado?",
   "¿Es una expansión remota de un G5Pro existente?",
   "¿Cuál es la temperatura ambiente y el grado de corrosión del sitio?",
   "¿Qué lenguajes de programación usa su equipo de mantenimiento?",
   "¿Qué protocolos de comunicación requiere?",
   "¿Requiere módulos de E/S remotas y a qué distancia?",
   "¿Cuál es la fuente de alimentación disponible?",
   "¿Requiere montaje en riel DIN o en gabinete?",
 ],
 "fuente":"G3Smart One-Page Introduction-Sales 20240530.pptx + G5Pro & G3Smart Poster Foldout 20240530.pdf",
}

# ------------------------------- CCS ---------------------------------------
F["T9100 (CCS)"] = {
 "familia":"CCS (compresores)",
 "descripcion":"Sistema de control de compresores (CCS) desarrollado por SUPCON como parte del sistema instrumentado de seguridad TCS-900. Es un sistema de control mejorado para compresores centrífugos y axiales en las industrias petroquímica y química, donde se usan accionamientos como turbinas de vapor, turbinas de gas y motores eléctricos. Es especialmente adecuado para el control y protección de compresores en áreas peligrosas.",
 "beneficios":[
   "Comparte la plataforma TCS-900: arquitectura TMR tolerante a fallas, certificada SIL3 por TÜV Rheinland",
   "Control mejorado para compresores centrífugos y axiales",
   "Adecuado para servicio en áreas peligrosas",
   "Integra control y protección del compresor en un mismo sistema",
   "Modelamiento con sistema de coordenadas independiente (supCCS)",
   "Solución de optimización de control de compresores supCCS",
   "Prueba de surgimiento (surge test) incluida en la solución",
 ],
 "clientes_target":[
   "Refinerías y petroquímica con compresores centrífugos o axiales",
   "Industria química con compresores accionados por turbina de vapor, turbina de gas o motor eléctrico",
   "Plantas con compresores en áreas peligrosas (zona clasificada)",
   "Unidades donde una falla del compresor detiene la producción completa",
 ],
 "competencia":"POR COMPLETAR — requiere validación. No hay battlecard en el material. El mercado de control de compresores tiene incumbentes fuertes y consolidados (los módulos ITCC de los grandes fabricantes).",
 "argumentos_venta":[
   "Es parte del TCS-900: no es un controlador de compresor aislado, es el mismo sistema SIL3 que ya protege la planta",
   "Control y protección del compresor en un solo sistema: elimina la frontera entre el CCS y el SIS, que es donde se pierden las señales",
   "Apto para áreas peligrosas",
   "Modelamiento de coordenadas independiente: aplica a distintos tipos de compresor sin rehacer el proyecto",
   "Solución de optimización supCCS incluida: además de controlar, busca el punto de mejor eficiencia",
 ],
 "objeciones":[
   ("Ya tenemos un CCS dedicado del fabricante del compresor","Si ese CCS no está certificado SIL3 ni integrado con el SIS de la planta, quedan dos sistemas con una frontera entre ellos. El T9100 unifica control y protección bajo la misma plataforma certificada."),
   ("¿Conocemos la tecnología de este proveedor para compresores?","El T9100 se apoya en el TCS-900, del que hay 6.700 unidades instaladas. Lo nuevo es el módulo de control de compresores, no la plataforma de seguridad."),
   ("El compresor está en zona peligrosa","Está diseñado justamente para el control y protección de compresores en áreas peligrosas."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿El compresor es centrífugo, axial o de otro tipo?",
   "¿Cuál es el accionamiento: turbina de vapor, turbina de gas o motor eléctrico?",
   "¿Qué capacidad y presión de descarga tiene el compresor?",
   "¿El compresor está en zona peligrosa clasificada?",
   "¿Qué tipo de control requiere: anti-surgimiento, capacidad, arranque/parada?",
   "¿El CCS debe integrarse con el SIS de la planta?",
   "¿Requiere protección SIL3 independiente del control?",
   "¿Necesita el sistema de optimización supCCS o solo el control básico?",
   "¿Cuáles son las condiciones de proceso (gas, presión, temperatura)?",
   "¿Cuántas E/S requiere el sistema y de qué tipo?",
 ],
 "fuente":"CCS T9100 Product Catalog 20241210.pdf",
}

F["T5100 (CCS)"] = {
 "familia":"CCS (compresores)",
 "descripcion":"Sistema de control de compresores de la línea CCS de SUPCON, con la solución de optimización de control supCCS. Comparte el catálogo y la arquitectura con el T9100, orientado al control de compresores en la industria de proceso.",
 "beneficios":[
   "Solución de optimización de control supCCS",
   "Modelamiento con sistema de coordenadas independiente",
   "Prueba de surgimiento (surge test) incluida",
   "Integración de control y protección del compresor",
   "Filosofía de catálogo común con el T9100: misma ingeniería y repuestos",
 ],
 "clientes_target":[
   "Refinerías y petroquímica",
   "Industria química con compresores de proceso",
   "Plantas que requieren optimización energética del compresor",
 ],
 "competencia":"POR COMPLETAR — requiere validación. No hay battlecard en el material.",
 "argumentos_venta":[
   "Misma arquitectura y catálogo que el T9100: permite ofrecer una u otra versión según el tamaño del compresor, sin cambiar de proveedor",
   "Solución de optimización supCCS: apunta al consumo energético del compresor, que suele ser uno de los mayores de la planta",
   "Modelamiento de coordenadas independiente: aplica a distintas configuraciones sin rehacer el proyecto",
   "Prueba de surgimiento integrada en la solución",
 ],
 "objeciones":[
   ("¿En qué se diferencia del T9100?","POR COMPLETAR: el material no explicita la diferencia entre ambos modelos más allá de compartir catálogo. Requiere confirmar con el fabricante antes de ofrecer uno u otro."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿Qué tipo y tamaño de compresor se va a controlar? (define T5100 vs T9100)",
   "¿Cuál es el accionamiento del compresor?",
   "¿Requiere el sistema de optimización supCCS?",
   "¿El compresor está en zona peligrosa?",
   "¿El CCS debe integrarse con el SIS de la planta?",
   "¿Qué protocolos de comunicación requiere?",
   "¿Cuántas E/S requiere?",
   "¿Debe integrarse con el DCS o SCADA existente?",
   "¿Cuáles son las condiciones de proceso?",
   "¿POR COMPLETAR?: diferencia con el T9100 — confirmar con el fabricante",
 ],
 "fuente":"CCS T5100 Product Catalog 20241210.pdf",
}

print("fichas cargadas:", len(F))
json.dump(F, open(os.path.join(DATOS, "fichas_2_datos.json"), "w"), ensure_ascii=False, indent=1)
print("datos guardados en datos/fichas_2_datos.json")
