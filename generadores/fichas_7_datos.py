#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATOS de las fichas de ANALÍTICA COMPLETA HOBRÉ (7a entrega).

CORRECCIÓN DE UN ERROR PROPIO: en la validación de cobertura declaré "sin material" a
HIFISC y NICOSYS-3 basándome SOLO en el árbol de carpetas local, sin buscar en la web del
fabricante. Victor lo detectó. Ambos tienen material público:
  - HIFISC: página propia en hobre.com/products/hifisc (especificaciones de sonda, filtro
    HPFF, gabinete, presión y temperatura máximas).
  - NICOSYS-3: datasheet PDF completo (rango 0-200 ppm, NDIR gas filter correlation,
    límite de detección <0,4 ppm, 3 niveles de alarma, temperatura de proceso máx 450 °C,
    gabinete IP56 de 2045x620x900 mm).
  - HICOSYS AQUA: listado en hobre.com/products (no estaba en el material local).

LECCIÓN: "no hay material" nunca se declara mirando solo el repo local. Antes de cerrar un
caso por ausencia, buscar en la web del fabricante. La ausencia de archivo no es ausencia
de producto.

Genera: datos/fichas_7_datos.json
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

F = {}

F["HIFISC (acondicionamiento de muestra de gas)"] = {
 "familia":"Analítica",
 "descripcion":"Sistema modular de acondicionamiento de muestra para gas y gas licuado (LPG), de Hobré. "
   "Combina dos componentes probados por más de 10 años: la sonda de impacto de flujo (Flow Impact "
   "Probe) y el filtro de membrana multifóbico de lazo rápido HPFF. El sistema usa el flujo del fluido "
   "como fuerza motriz del lazo rápido de preacondicionamiento, sin partes móviles ni bombas. Se instala "
   "antes del analizador para asegurar que reciba una muestra no contaminada.",
 "beneficios":[
   "Tiempo de respuesta superior: baja de horas a minutos en aplicaciones de bajo ppm",
   "Reducción declarada de más del 90% en venteo y quema (flaring) de gas",
   "Intervalo de mantención probado de 1 año en corrientes de gas contaminado",
   "Aislamiento de proceso completo con doble bloqueo y purga (double block and bleed) para "
   "intervención segura del sistema analizador",
   "Tiempo de retardo en la sonda de 0,2 a 2 segundos según la velocidad de la tubería",
   "El lazo rápido de 1/2\" sin restricción opera típicamente al 25% de la velocidad de la tubería",
   "Filtro HPFF que remueve sólidos y líquidos polares y no polares en la entrada",
   "Mantiene agentes reactivos (glicol, amina, óxido de zinc, cáustico, polvo de tamiz molecular) "
   "fuera de las líneas de muestra, evitando absorción y desorción",
   "Cero volumen muerto en el sistema de reducción de presión, líneas y acondicionamiento",
   "Tamaño de poro del filtro unas 500 veces menor que el sistema de reducción: riesgo de "
   "obstrucción casi nulo",
   "Sonda sin mantención, que no requiere retracción salvo cuando se hace pigging de la tubería",
   "Modular: se configura con los elementos necesarios según el analizador y la aplicación",
   "Combinable con la mayoría de los analizadores de gas de proceso",
 ],
 "clientes_target":[
   "Oil and gas: gas natural y gas licuado (LPG)",
   "Refinación y petroquímica: corrientes de gas con contaminantes reactivos",
   "Aplicaciones de medición de H2S y humedad en niveles de bajo ppm",
   "Plantas donde el tiempo de respuesta del analizador es crítico para el control",
   "Instalaciones con requisito de reducción de emisiones por venteo y quema",
   "Cualquier planta que ya tenga un analizador de gas y necesite que mida confiablemente",
 ],
 "competencia":"POR COMPLETAR — no hay battlecard en el material público revisado. El segmento de "
   "sistemas de acondicionamiento de muestra tiene oferta de Parker, Swagelok, Genie (AMETEK) y "
   "fabricantes especializados. INFERENCIA de mercado, no dato del fabricante.",
 "argumentos_venta":[
   "Es un producto VENDIBLE DENTRO de una venta de analizador: quien compra un TISOMIC o un WIM COMPAS "
   "necesita resolver el acondicionamiento, y HIFISC es la pieza de la misma marca",
   "La reducción de más del 90% en venteo y quema es un argumento de cumplimiento ambiental medible",
   "El intervalo de mantención de 1 año en gas contaminado es un argumento de costo operativo directo",
   "Bajo de horas a minutos el tiempo de respuesta en aplicaciones de bajo ppm: eso cambia si el "
   "analizador sirve para control o solo para registro",
   "El doble bloqueo y purga permite intervenir el analizador sin parar el proceso",
   "Se configura modular, así que se adapta a la aplicación sin sobredimensionar",
 ],
 "objeciones":[
   ("Ya tenemos un sistema de muestreo instalado","El argumento es el tiempo de respuesta y el venteo. "
     "Un sistema convencional donde el gas a presión y el líquido en la sonda son la causa principal del "
     "retardo total, típicamente se mide en horas. El HIFISC baja eso a minutos."),
   ("¿Sirve para mi analizador?","El material declara que se puede combinar con la mayoría de los "
     "analizadores de gas de proceso, y que los sistemas se diseñan y producen a medida para cada "
     "analizador. Es un punto de ingeniería, no de catálogo."),
   ("Nuestra corriente tiene glicol o amina","Es el caso de diseño: el filtro HPFF mantiene los agentes "
     "reactivos fuera de las líneas de muestra, evitando absorción y desorción que distorsionan la "
     "medición."),
   ("¿Aguanta la presión de mi línea?","El filtro HPFF opera hasta 340 barG en versión estándar y "
     "285 barG en versión de alta temperatura. La sonda usa brida de 150# a 2500# en RF o RTJ."),
   ("Requerimos análisis en bajo ppm","El material advierte que para análisis en niveles de bajo ppm se "
     "requiere tubería Silcosteel. Es un requisito a considerar en la especificación."),
 ],
 "preguntas_tecnicas":[
   "¿Qué analizador va a alimentar este sistema de muestreo?",
   "¿El fluido es gas natural, gas de proceso o gas licuado (LPG)?",
   "¿Cuál es la presión y temperatura del proceso? (hasta 340 barG y 120 °C en versión estándar)",
   "¿Qué contaminantes tiene la corriente: glicol, amina, cáustico, polvo de tamiz?",
   "¿Cuál es el requisito de tiempo de respuesta del analizador?",
   "¿Qué nivel de medición requiere: porcentaje o bajo ppm? (define si necesita tubería Silcosteel)",
   "¿Qué tipo de conexión de proceso tiene la tubería? (2\" o 3\", brida 150# a 2500#)",
   "¿Requiere calefacción del gabinete?",
   "¿Se hace pigging en la tubería? (define si la sonda debe ser retractable)",
   "¿Dónde se instalará el acondicionamiento secundario: en campo o en la caseta del analizador?",
 ],
 "fuente":"hobre.com/products/hifisc (página oficial del fabricante) + SUPCON_HOBRE ASI & Product "
   "Introduction.pdf. Las especificaciones de sonda, filtro HPFF y gabinete vienen de la ficha web.",
}

F["NICOSYS-3 (detección de CO en secadores)"] = {
 "familia":"Analítica",
 "descripcion":"Sistema de acondicionamiento de muestra y detección de monóxido de carbono (CO) en "
   "corrientes gaseosas, para secadores por atomización. Desarrollado junto a NIZO (Instituto Nacional "
   "Holandés de Investigación Láctea) hace 25 años. Usa principio NDIR de correlación con filtro de gas, "
   "con enfriadores de condensado y sondas de muestreo para distintas aplicaciones. Detecta "
   "combustión latente (smoldering) y reacciones de Maillard.",
 "beneficios":[
   "Rango de medición de CO de 0 a 200 ppm",
   "Límite de detección inferior a 0,4 ppm, o 0,2% de la lectura si es mayor: sensibilidad para "
   "detectar la combustión latente en su etapa inicial",
   "Detecta el aumento de CO más de 30 minutos antes de que aparezca la llama (dato del material)",
   "Tres niveles de alarma configurables desde 0,5 ppm, utilizables para aviso temprano, parada del "
   "sistema o activación de supresión de incendio",
   "Monitorea el CO entrante Y saliente, para evitar falsas alarmas por picos de CO del ambiente o "
   "por CO de fondo de camiones y escapes",
   "Mide en cámara de secado, lecho fluidizado, filtro de mangas y aire de entrada: cobertura de todo "
   "el proceso de secado",
   "Acondicionamiento profesional de muestra en condiciones higiénicas: evita obstrucción y condensación",
   "Temperatura de proceso máxima de 450 °C",
   "Hasta 4 canales de muestra, con líneas de hasta 80 m sin calefacción",
   "Sondas de filtro de acero inoxidable, compatibles con Varinline, DN25",
   "Gabinete IP56 en acero con recubrimiento en polvo (RAL7035), dimensiones 2045 x 620 x 900 mm",
   "Salidas y alarmas automatizadas integradas para la seguridad de la planta de secado",
   "Reduce el costo de seguro de la instalación (beneficio declarado por el fabricante)",
   "Tecnología de bajo costo de detección de CO según el material",
 ],
 "clientes_target":[
   "Secadores por atomización en alimentos: leche en polvo, fórmula infantil, café en polvo, suero",
   "Alimentos y bebidas: cremas no lácteas, sabores y aditivos alimentarios",
   "Industria farmacéutica: secadores por atomización de enzimas, hormonas, aminoácidos, antibióticos, "
   "levaduras, vitaminas y proteínas",
   "Química: detergentes, jabones, pesticidas, fertilizantes, pigmentos, pinturas, tinturas, cosméticos "
   "y materiales cerámicos",
   "Toda planta de secado por atomización sujeta a requisito de protección contra incendio y explosión",
   "Operaciones que necesitan cumplir recomendaciones VDI 2263 sobre riesgo de combustión latente",
 ],
 "competencia":"PARTNER CONOCIDO Y DECLARADO: Fike Corporation y Hobré tienen una alianza anunciada "
   "públicamente; el sistema BICOSYS de Hobré se ofrece a través de Fike como parte de su solución de "
   "protección de explosión para secado industrial. En protección de secadores industriales compiten "
   "Fike, Kidde, Fenwal y otros especialistas en supresión. En el tipo de analizador, el material no "
   "identifica un competidor directo para NICOSYS-3. OJO: el competidor es el sistema de protección "
   "completo (supresión de explosión), no el analizador.",
 "argumentos_venta":[
   "El argumento económico es de SEGURO y de continuidad: el material declara reducción de costo de "
   "seguro y prevención de paradas por incidente",
   "Detectar 30 minutos antes de la llama es el argumento que decide la inversión: en una planta de "
   "leche en polvo, un incendio en el secador es pérdida total de producción, no un incidente menor",
   "Tres niveles de alarma que pueden accionar aviso, parada o supresión: el sistema se integra al plan "
   "de protección, no queda como indicador pasivo",
   "Compara CO entrante y saliente: resuelve el problema real de las falsas alarmas, que es la razón "
   "número uno por la que estos sistemas se terminan desconectando en planta",
   "Desarrollado con NIZO hace 25 años y en su tercera versión: hay historia de producto, no es nuevo",
   "Tecnología de bajo costo declarada: el argumento es que cualquier planta de secado puede pagarlo",
 ],
 "objeciones":[
   ("Ya tenemos protección contra explosión por supresión","No son alternativas: el CO detecta la "
     "combustión latente ANTES de que haya llama, y la supresión actúa cuando ya hubo deflagración. "
     "La combinación es lo que el material describe, y es la alianza comercial que Hobré tiene con Fike."),
   ("Nuestro secador tiene protección de temperatura","El material lo responde con un dato duro: la "
     "temperatura del aire de escape NO se afecta por la combustión latente de un grumo, mientras el CO "
     "sube sostenidamente por más de 30 minutos. La temperatura no detecta lo que el CO sí."),
   ("La planta es de alimentos y el sistema debe ser higiénico","El material declara acondicionamiento "
     "de muestra en condiciones higiénicas, previniendo obstrucción y condensación, y sondas de acero "
     "inoxidable compatibles con Varinline."),
   ("Tenemos falsas alarmas con el sistema actual","Es exactamente el problema que NICOSYS-3 ataca: "
     "monitorea CO entrante y saliente para descartar el CO de fondo del ambiente. Es un argumento "
     "directo contra el sistema incumbente que el cliente tenga instalado."),
   ("¿Diferencia con HICOSYS o BICOSYS?","Los tres son de Hobré para secadores por atomización. POR "
     "COMPLETAR Y ACLARAR CON EL FABRICANTE: el material local no explicita la frontera entre los tres. "
     "NICOSYS-3 es el sistema de detección de CO con acondicionamiento de muestra, desarrollado con "
     "NIZO; HICOSYS ADVANCED mide CO y H2O; HICOSYS AQUA solo H2O. No ofrecer uno u otro sin confirmar "
     "el criterio de selección."),
 ],
 "preguntas_tecnicas":[
   "¿Cuál es el tipo de secador y su capacidad de producción?",
   "¿Cuántos puntos de muestreo requiere? (el sistema admite hasta 4 canales)",
   "¿Dónde se instalan los puntos: cámara de secado, lecho fluidizado, filtro de mangas, aire de entrada?",
   "¿Cuál es la temperatura y la humedad del aire en cada punto? (máx 450 °C)",
   "¿Qué distancia hay desde los puntos de muestreo hasta el gabinete? (máx 80 m sin calefacción)",
   "¿El producto es alimento, fármaco o químico? (define requisitos higiénicos)",
   "¿Cuántos niveles de alarma requiere y qué debe accionar cada uno?",
   "¿El secador tiene sistema de supresión de explosión instalado?",
   "¿Ha tenido eventos de combustión latente o falsas alarmas de CO?",
   "¿Requiere integración con el sistema de control o con el sistema de supresión?",
 ],
 "fuente":"Datasheet NICOSYS-3 'Carbon Monoxide Detection Analyzer' (Hobré Instruments B.V., PDF oficial) "
   "+ hobre.com/industries/food-pharma + nota de prensa de la alianza Fike-Hobré. Las especificaciones "
   "técnicas vienen del datasheet, no del material local.",
}

F["HICOSYS AQUA (medición de H2O en secado)"] = {
 "familia":"Analítica",
 "descripcion":"Analizador de humedad (H2O) para secadores por atomización, de la línea HICOSYS de "
   "Hobré. Es la versión dedicada exclusivamente a la medición de agua en el proceso de secado, dentro "
   "de la familia de productos para seguridad y eficiencia de secadores.",
 "beneficios":[
   "Dedicado a una sola variable: mide H2O en el secado sin las funciones adicionales de las otras "
   "versiones de la línea",
   "Del mismo fabricante y la misma línea que HICOSYS ADVANCED, que mide CO y H2O",
   "Se integra a los sistemas de seguridad de secadores por atomización de Hobré",
   "POR COMPLETAR: el material público lista el producto pero no entrega datasheet propio. "
   "Las especificaciones de rango, principio de medición y precisión no están disponibles.",
 ],
 "clientes_target":[
   "Secadores por atomización en alimentos: leche en polvo, café, suero, fórmulas infantiles",
   "Industria farmacéutica con secado por atomización",
   "Plantas de secado que requieren control de humedad del producto para calidad y para evitar "
   "depósitos pegajosos y combustión latente",
   "Operaciones que ya tienen detección de CO y quieren cerrar el ciclo con el control de humedad",
 ],
 "competencia":"POR COMPLETAR — sin battlecard. Por la aplicación (medición de humedad en secado), los "
   "competidores son los medidores de humedad de proceso de Endress+Hauser, Vaisala y Michell. "
   "INFERENCIA de mercado, no dato del fabricante.",
 "argumentos_venta":[
   "El material de Hobré lo asocia a un beneficio concreto: el monitoreo de humedad mejora el control "
   "del secador y reduce la probabilidad de depósitos pegajosos y de combustión latente. O sea, no es "
   "solo calidad: es seguridad",
   "Se vende junto con la detección de CO: es el complemento natural del sistema de protección del "
   "secador, y las dos mediciones juntas dan el cuadro completo",
   "Existe la versión combinada (HICOSYS ADVANCED) para quien quiera CO y H2O en un solo equipo: "
   "permite ofrecer dos alcances distintos",
   "POR COMPLETAR: pedir al fabricante el datasheet de HICOSYS AQUA para poder cotizar",
 ],
 "objeciones":[
   ("Podemos medir la humedad con instrumentación general","La diferencia es la aplicación: este "
     "producto es para el ambiente del secador por atomización, con las condiciones de temperatura, "
     "polvo y producto que eso implica. Un medidor general no está pensado para ese ambiente."),
   ("¿Por qué no comprar directamente el que mide CO y H2O?","Es una decisión de alcance: HICOSYS "
     "ADVANCED mide ambos en un equipo. Si solo se necesita humedad, HICOSYS AQUA es la versión "
     "dedicada. POR COMPLETAR: comparar el costo de las dos opciones con el fabricante."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿Necesita medir solo humedad o también CO? (define AQUA o ADVANCED)",
   "¿En qué punto del secador se mide la humedad?",
   "¿Cuál es la temperatura y la concentración de polvo en ese punto?",
   "¿En qué rango de humedad debe medir?",
   "¿Qué nivel de precisión requiere para el control del secador?",
   "¿Se integra con el sistema de control existente?",
   "¿El producto es alimento o fármaco? (define requisitos higiénicos)",
   "POR COMPLETAR: rango, precisión y principio de medición — solicitar datasheet al fabricante",
 ],
 "fuente":"hobre.com/products (listado oficial del fabricante: 'HICOSYS AQUA - H2O Analysis in spray "
   "drying') + hobre.com/industries/food-pharma. No hay datasheet propio disponible: los campos de "
   "especificación quedan POR COMPLETAR.",
}

json.dump(F, open(os.path.join(D, "fichas_7_datos.json"), "w"), ensure_ascii=False, indent=1)
print(f"fichas de analitica completa: {len(F)}")
for n, f in F.items():
    print(f"  {n[:52]:54s} fam={f['familia']:10s} b={len(f['beneficios']):>2} c={len(f['clientes_target']):>2} "
          f"a={len(f['argumentos_venta']):>2} o={len(f['objeciones']):>2} p={len(f['preguntas_tecnicas']):>2}")
print(f"\nguardado: datos/fichas_7_datos.json")
