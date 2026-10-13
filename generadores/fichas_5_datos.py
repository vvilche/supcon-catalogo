#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATOS de las fichas de VÁLVULAS DE CONTROL SUPCON (5a entrega).

FUENTE: "5. Brief of SUPCON control valve product.pdf" (12 páginas) de
ZHEJIANG SUPCON FLUID TECHNOLOGY CO., LTD. — la filial de válvulas del grupo SUPCON.
Ese PDF NO tiene capa de texto (11 caracteres extraídos): se leyó por OCR con Tesseract
sobre las páginas convertidas a imagen a 200 dpi. El texto OCR queda en
datos/valvulas_extraido.json para que cada dato sea auditable.

POR QUE ESTA ENTREGA EXISTE: el catálogo solo tenía el posicionador CVP2000 como
"válvulas", y la escalera le asignaba el mercado completo de válvulas (US$53,8M) a un
posicionador. Lo correcto es fichar la línea de válvulas real, que son 13 series.

Genera: datos/fichas_5_datos.json
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")

FUENTE_PDF = ("5. Brief of SUPCON control valve product.pdf "
              "(Zhejiang SUPCON Fluid Technology Co., Ltd., 12 pp, leído por OCR)")

F = {}

F["Válvulas de control — línea completa SUPCON FLUID"] = {
 "familia":"Válvulas",
 "descripcion":"Línea completa de válvulas de control de proceso de Zhejiang SUPCON Fluid Technology, "
   "la filial de válvulas del grupo SUPCON. Trece series: vástago deslizante (LN y LM), bola "
   "O-type y V-type (SN y VN), excéntrica rotativa (CN), mariposa triple excéntrica (BN2302/BN1302), "
   "mariposa con revestimiento plástico (SN2401F, BN2101F/BN1101F), mariposa con caucho "
   "(BN2101J/BN1101J), válvula de alimentación de fondo de estanque, válvula de cuchilla y "
   "válvula de compuerta.",
 "beneficios":[
   "Cobertura de DN15 a DN1200: la línea cubre desde líneas de instrumento hasta ductos de gran diámetro",
   "Rango de temperatura de proceso de -196 °C a +593 °C según serie",
   "Rango de presión hasta ANSI 2500 (PN420) en la serie de alta presión LM",
   "Rango de regulación (rangeability) de 50:1 en las series de vástago deslizante",
   "Serie VN de bola V con rangeability 300:1, la más alta de la línea, con acción de corte de fibras",
   "Características de flujo seleccionables: porcentaje igual, lineal y on/off",
   "Series de baja emisión acústica (LN8220, LN8320, LN8520, LN8720) para condiciones de alta caída de presión",
   "Conexiones RF, RJ, FM, SW, BW, TG, MFM y clip según serie",
   "Cumple normas de brida HG20592-2009 y clasificación ANSI",
   "Fabrica todo el portafolio: vástago deslizante, bola, mariposa y excéntrica con un solo proveedor",
 ],
 "clientes_target":[
   "Petroquímica y refinación (la industria que el material declara como principal)",
   "Química: incluidas las corrientes corrosivas con revestimiento plástico",
   "Metalurgia y siderurgia",
   "Energía eléctrica: vapor y agua de proceso",
   "Tratamiento de agua y aguas residuales",
   "Minería y pulpa: la serie VN de bola V está diseñada para pulpas y fluidos con fibras",
   "Alimentos y farmacéutica: válvula de cuchilla para pasta y material en polvo",
 ],
 "competencia":"POR COMPLETAR — el brief de válvulas NO trae sección de competidores ni battlecard. "
   "En Chile el segmento está ocupado y medido en el registro de importaciones 2025 (US$53,8M en "
   "partidas de válvulas): BRAY US$5,6M, VALMET US$5,4M, VALVITALIA US$4,6M. Además están Metso, "
   "Emerson (Fisher), Samson y Neles. Es INFERENCIA DE MERCADO a partir del estudio de importaciones, "
   "no un dato del material del fabricante.",
 "argumentos_venta":[
   "Es una línea completa, no un producto: vástago deslizante, bola, mariposa y excéntrica del mismo "
   "proveedor, con lo que se puede cotizar el paquete entero de una planta en vez de piezas sueltas",
   "El rango de proceso es el del segmento: de -196 °C a +593 °C y hasta ANSI 2500 (PN420) en la serie LM",
   "La serie VN de bola V tiene rangeability 300:1 y acción de corte: sirve en pulpa, fibra y sólidos "
   "en suspensión, que es donde las válvulas convencionales se tapan",
   "Las series de baja emisión acústica cubren los casos de alta caída de presión, donde el ruido es "
   "el criterio de selección",
   "Hay revestimiento plástico (PTFE, FEP, PFA) para corrientes ácidas, alcalinas y tóxicas",
   "DN hasta 1200 en mariposa: cubre ductos grandes que otros proveedores cotizan como caso especial",
   "Se integra naturalmente con el posicionador CVP2000 de la misma marca (la única pieza de "
   "instrumentación de válvula que ya estaba en el catálogo)",
   "El material entrega las tablas de parámetros por serie: permite dimensionar sin adivinar",
 ],
 "objeciones":[
   ("Nunca había oído de válvulas SUPCON","Es exacto y es el estado real: la filial de válvulas no tiene "
     "presencia registrada en Chile. En el registro de importaciones 2025 no aparece ni una importación "
     "de SUPCON. Es una línea nueva en el mercado local, con el activo y el riesgo que eso implica: "
     "sin base instalada que consultar."),
   ("¿Quién da soporte y repuestos en Chile?","POR COMPLETAR: el material no documenta estructura de "
     "servicio ni bodega local. El brief es de la fábrica, no incluye red de distribución. Es el punto "
     "a resolver con el fabricante antes de ofrecer válvulas."),
   ("Ya trabajamos con Fisher / Metso / Samson","Son los incumbentes del segmento en Chile. La entrada "
     "honesta es por proyecto nuevo o por una aplicación donde la línea tenga algo específico "
     "(por ejemplo pulpa con la serie VN, o DN grande con mariposa). Sin battlecard del fabricante, "
     "la conversación es técnica y por aplicación, no por marca."),
   ("¿Las válvulas cumplen la normativa chilena?","El material cita normas de brida HG20592-2009 y "
     "clasificación ANSI, que son estándar internacional. POR COMPLETAR: no hay referencia a "
     "normativa chilena (NCh) ni a requisitos de la SEC. Verificar antes de ofrecer en una instalación "
     "regulada."),
   ("¿Tienen el mismo respaldo que una marca europea?","El brief no entrega datos de base instalada, "
     "años en el mercado ni casos de referencia. POR COMPLETAR: pedirlos al fabricante antes de "
     "una oferta grande, porque es la pregunta que va a hacer el cliente."),
 ],
 "preguntas_tecnicas":[
   "¿Cuál es el fluido y su temperatura y presión de operación?",
   "¿Qué diámetro nominal tiene la línea? (la línea cubre DN15 a DN1200)",
   "¿Qué función cumple: control modulante o corte (on/off)?",
   "¿Cuál es la caída de presión del proceso? (define si necesita serie de presión balanceada)",
   "¿El fluido tiene sólidos, fibras o es abrasivo? (define bola V, excéntrica o cuchilla)",
   "¿El fluido es corrosivo? (define revestimiento plástico PTFE/FEP/PFA)",
   "¿El ruido es un criterio de selección? (define las series de baja emisión acústica)",
   "¿Requiere característica de flujo porcentaje igual, lineal o on/off?",
   "¿Qué tipo de conexión requiere: brida RF, RJ, FM, SW, BW o clip?",
   "¿Qué accionamiento usa: neumático, eléctrico o manual?",
   "¿Requiere posicionador inteligente? (se integra el CVP2000)",
   "¿La instalación es en zona peligrosa?",
 ],
 "fuente": FUENTE_PDF,
}

# ---- las series, agrupadas por familia de válvula, para el detalle ----
F["Válvulas de vástago deslizante (series LN y LM)"] = {
 "familia":"Válvulas",
 "descripcion":"Válvulas de control de vástago deslizante en cuatro grupos: guiada por el asiento "
   "(LN81/82), guiada por jaula con cuatro tipos de sello (LN83/84/85/87), y de alta presión (LM81/85/87). "
   "La LN81/82 usa obturador de tipo émbolo con desequilibrio de presión y guía en la parte superior de "
   "la tapa. Las LN83/84/85/87 usan obturador balanceado por jaula, con sello O-ring, resorte o émbolo. "
   "La LM usa jaula separable con anillo metálico de alta performance para alta presión.",
 "beneficios":[
   "LN81/82: cuerpo DN15 a DN400, temperatura de -196 °C a +593 °C (el rango más amplio de la línea)",
   "LN83/84/85/87: cuerpo DN40 a DN400, temperatura de -80 °C a +260 °C (grupo 83/84/85) y -17 °C a +593 °C (grupo 87)",
   "LM de alta presión: DN40 a DN200, hasta ANSI 2500 (PN420) y PN250, temperatura -17 °C a +593 °C",
   "Rangeability 50:1 en todas las series del grupo",
   "Presiones PN16, PN25, PN40, PN63 según HG20592-2009 y ANSI 150/300/600",
   "Características de flujo porcentaje igual y lineal",
   "Cuatro opciones de sello balanceado: O-ring, resorte energizado, émbolo y doble jaula",
   "Versiones de baja emisión acústica en cada grupo (LN8220, LN8320, LN8520, LN8720)",
   "LN81/82 con estructura simple, buen sellado y bajo costo de mantención: para baja caída de presión",
 ],
 "clientes_target":[
   "Refinación y petroquímica: lazos de control de proceso con caída de presión alta",
   "Vapor y agua de caldera en generación",
   "Alta presión: inyección, amoníaco, urea y procesos de presión severa (serie LM)",
   "Servicios criogénicos (hasta -196 °C en LN81/82)",
   "Procesos con ruido crítico (series de baja emisión acústica)",
 ],
 "competencia":"POR COMPLETAR — el brief no incluye battlecard. El segmento de válvulas de vástago "
   "deslizante en Chile está cubierto por Fisher (Emerson), Samson, Metso y Neles. INFERENCIA de mercado.",
 "argumentos_venta":[
   "Es el grupo con el rango de temperatura más amplio de la línea: -196 °C a +593 °C",
   "La LN81/82 es la opción de menor costo de mantención para baja caída de presión: entrada económica",
   "La LM llega a ANSI 2500 / PN420, que es el segmento de alta presión donde no todos compiten",
   "Cuatro tipos de sello balanceado permiten ajustar el diseño al fluido en vez de sobredimensionar",
   "Las versiones de baja emisión acústica resuelven el ruido como criterio de selección, no como "
   "consecuencia",
 ],
 "objeciones":[
   ("La válvula estándar nos sirve","Depende del criterio: si la caída de presión es alta o el fluido "
     "es sucio, la válvula estándar se erosiona o se atasca. Por eso existe el grupo balanceado y las "
     "series de baja emisión acústica."),
   ("Necesitamos servicio local","POR COMPLETAR: sin red de servicio documentada en Chile, este punto "
     "hay que resolverlo con el fabricante antes de ofrecer la línea."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿Cuál es la caída de presión del lazo? (define si basta la serie no balanceada)",
   "¿Qué temperatura tiene el fluido? (LN81/82 cubre hasta -196 °C y +593 °C)",
   "¿La presión de operación supera ANSI 600? (entonces es serie LM)",
   "¿El fluido es limpio o puede depositar sólidos?",
   "¿El ruido es un problema en el punto de instalación?",
   "¿Qué diámetro nominal requiere?",
   "¿Requiere característica porcentaje igual o lineal?",
   "¿Con qué accionamiento y qué posicionador?",
 ],
 "fuente": FUENTE_PDF,
}

F["Válvulas de bola (series SN O-type y VN V-type)"] = {
 "familia":"Válvulas",
 "descripcion":"Dos familias de válvula de bola. SN O-type: bola de paso total que gira 90° para "
   "abrir o cerrar, en versión de asiento flotante (blando o metal-metal) y de montura fija (trunnion). "
   "VN V-type: bola con abertura en V, con acción de cizalla entre la V y el asiento al cerrar, lo que "
   "permite cortar materiales fibrosos.",
 "beneficios":[
   "SN O-type: DN15 a DN200 en la versión flotante, DN50 a DN300 en la trunnion",
   "SN con funciones de vástago antiexpulsión (fly) y antiestático",
   "SN sello duro de -29 °C a +538 °C; sello blando de -29 °C a +200 °C",
   "VN V-type: DN20 a DN350, temperatura de -29 °C a +425 °C",
   "VN con rangeability 300:1, la más alta de toda la línea de válvulas",
   "VN con pasaje de flujo suave y alto coeficiente de caudal",
   "VN apta para pulpa, aguas residuales, fluidos con fibras y sólidos en suspensión",
   "SN trunnion con sello blando PTFE de doble asiento elástico: cierre sin fuga declarado",
 ],
 "clientes_target":[
   "Minería y pulpa: la serie VN para pulpas y fluidos con fibras",
   "Tratamiento de aguas y aguas residuales: VN para lodos y sólidos en suspensión",
   "Papel y celulosa: VN por su acción de corte de fibras",
   "Petroquímica: SN O-type para corte de líquidos y gases",
   "Alimentos y bebidas: donde se requiere cierre hermético y limpieza",
   "Fluidos con partículas sólidas: SN trunnion de sello duro",
 ],
 "competencia":"POR COMPLETAR — sin battlecard en el brief. En Chile el segmento de válvulas de bola "
   "está cubierto por BRAY (US$5,6M importados en 2025, el mayor del segmento) y por Metso, Neles y "
   "Velan. INFERENCIA de mercado desde el registro de importaciones.",
 "argumentos_venta":[
   "La series VN tiene rangeability 300:1, muy por encima del 50:1 de las series de vástago deslizante: "
   "es la mejor de la línea para control modulante",
   "La acción de cizalla de la VN corta fibras, así que no se tapa con pulpa ni con material fibroso",
   "El corte de la VN sirve tanto para control modulante como para corte, con la misma válvula",
   "La SN trunnion de sello duro llega a +538 °C, útil en líneas de vapor y proceso térmico",
   "Funciones antiestático y vástago antiexpulsión en la SN: son requisitos de seguridad en "
   "hidrocarburos",
 ],
 "objeciones":[
   ("Necesitamos control muy preciso","Para eso está la VN con rangeability 300:1. La de bola O-type "
     "es de corte (on/off), no modulante."),
   ("Nuestro fluido tiene fibras y las válvulas se tapan","Es el caso de diseño de la serie VN: la "
     "abertura en V corta el material contra el asiento al cerrar. Es su diferencia específica."),
   ("Ya usamos válvulas de bola de otra marca","BRAY domina el segmento en Chile. La entrada es por "
     "aplicación donde la VN aporte el corte de fibras, no por costo."),
 ],
 "preguntas_tecnicas":[
   "¿La válvula es para control modulante o para corte? (define O-type o V-type)",
   "¿El fluido tiene fibras, sólidos o es pulpa? (define VN)",
   "¿Qué temperatura de operación tiene? (sello duro hasta +538 °C)",
   "¿El fluido es limpio o abrasivo? (define sello blando o duro, flotante o trunnion)",
   "¿Qué diámetro nominal requiere? (SN hasta DN300, VN hasta DN350)",
   "¿Requiere función antiestático y vástago antiexpulsión? (aplica en hidrocarburos)",
   "¿Requiere actuación automática o es de operación manual?",
 ],
 "fuente": FUENTE_PDF,
}

F["Válvulas mariposa y excéntricas (series BN y CN)"] = {
 "familia":"Válvulas",
 "descripcion":"Tres grupos: mariposa triple excéntrica BN2302/BN1302 con plato de estructura "
   "excéntrica tridimensional y sello de placas de acero inoxidable y grafito; mariposa con "
   "revestimiento plástico SN2401F (bola) y BN2101F/BN1101F, con liner de FEP o PFA inyectado a "
   "presión; mariposa con caucho BN2101J/BN1101J con efecto autolimpiante; y la válvula excéntrica "
   "rotativa CN de carátula esférica con estructura de doble excentricidad, apta para flujo con lodo.",
 "beneficios":[
   "BN triple excéntrica: DN80 a DN1200, el mayor diámetro de toda la línea de válvulas",
   "BN triple excéntrica: prácticamente sin fricción entre asiento y disco durante el accionamiento",
   "BN2101F/BN1101F con liner cerámico FEP o PFA: resistencia fuerte a corrosión, para ácidos, "
   "álcalis y gases tóxicos o volátiles",
   "SN2401F revestida en PTFE o FEP: todas las partes en contacto con el fluido aisladas, para "
   "sellado estricto con medio corrosivo",
   "BN2101J/BN1101J con liner de caucho: efecto autolimpiante, para fluido con partículas en "
   "suspensión, pulpa y corrientes turbias",
   "BN2101J/BN1101J: ciclos de apertura y cierre de hasta cientos de miles de veces, con fuga cero "
   "en prueba con gas",
   "CN excéntrica: estructura de doble excentricidad con desgaste mínimo en el accionamiento",
   "CN excéntrica: apta para flujo con lodo, con resistencia al desgaste y a la corrosión, y buen "
   "coeficiente de caudal",
   "Temperaturas de -45 °C a +425 °C según serie",
 ],
 "clientes_target":[
   "Ductos de gran diámetro: agua, aire y gases de proceso (BN hasta DN1200)",
   "Industria química con corrientes ácidas, alcalinas o tóxicas (liner FEP/PFA)",
   "Tratamiento de aguas y aguas residuales con sólidos en suspensión (liner de caucho)",
   "Minería y pulpa con flujo de lodo (CN excéntrica y BN de caucho)",
   "Papel y celulosa",
   "Procesos que exigen cierre hermético con gas (fuga cero declarada)",
 ],
 "competencia":"POR COMPLETAR — sin battlecard en el brief. El segmento de mariposa y excéntricas en "
   "Chile está cubierto por Metso, Bray, Valmet y Neles. INFERENCIA de mercado.",
 "argumentos_venta":[
   "DN hasta 1200 en mariposa triple excéntrica: cubre ductos grandes sin ir a un diseño especial",
   "El liner de FEP o PFA es la respuesta al fluido corrosivo, que es donde las válvulas metálicas "
   "se degradan rápido",
   "El liner de caucho con efecto autolimpiante evita el taponamiento en corrientes con sólidos, "
   "que es el principal costo de mantención en agua y pulpa",
   "Ciclos de cientos de miles de accionamientos con fuga cero en gas: sirve en servicio de corte "
   "frecuente",
   "La triple excentricidad reduce el desgaste del asiento porque casi no hay fricción al accionar",
   "La CN excéntrica está diseñada específicamente para lodo, no adaptada",
 ],
 "objeciones":[
   ("El fluido es muy corrosivo para una válvula metálica","Para eso están SN2401F y BN2101F/BN1101F: "
     "todas las partes en contacto quedan aisladas por revestimiento de PTFE, FEP o PFA."),
   ("Nuestro fluido tiene sólidos y se tapan las válvulas","El liner de caucho de la BN2101J/BN1101J "
     "tiene efecto autolimpiante y está pensada para partículas en suspensión y pulpa."),
   ("Necesito un ducto grande y las válvulas son caras","La BN triple excéntrica llega a DN1200 con "
     "bajo torque de operación y baja resistencia al flujo: es el diseño correcto para diámetro grande."),
   ("¿Aguanta el ciclo de abrir y cerrar muchas veces?","El material declara hasta cientos de miles "
     "de ciclos con fuga cero en prueba con gas, en la serie de liner de caucho."),
 ],
 "preguntas_tecnicas":[
   "¿Cuál es el diámetro del ducto? (BN cubre DN80 a DN1200)",
   "¿El fluido es corrosivo? (define revestimiento FEP, PFA o PTFE)",
   "¿El fluido tiene sólidos en suspensión o es pulpa? (define liner de caucho o excéntrica)",
   "¿Qué temperatura de operación tiene? (-45 °C a +425 °C según serie)",
   "¿Requiere cierre hermético verificado con gas?",
   "¿Cuántos ciclos de operación por día tendrá la válvula?",
   "¿Se acciona automáticamente con actuador o es manual?",
   "¿La instalación es en zona peligrosa?",
 ],
 "fuente": FUENTE_PDF,
}

F["Válvulas especiales (alimentación, cuchilla y compuerta)"] = {
 "familia":"Válvulas",
 "descripcion":"Válvulas para servicios específicos. Válvula de alimentación: se suelda por brida en "
   "el fondo de estanques y reactores para eliminar el volumen residual de proceso, con opción de "
   "carrera ascendente o descendente. Válvula de cuchilla (knife gate): con disco de función cortante "
   "que arrastra los residuos adheridos y limpia automáticamente. Válvula de compuerta: de baja "
   "resistencia al fluido, para servicio de abrir o cerrar sin regulación.",
 "beneficios":[
   "Válvula de alimentación: DN25 a DN200, PN6/PN10/PN16, elimina el volumen residual del fondo del estanque",
   "Válvula de alimentación: disponible en dos configuraciones de carrera, ascendente y descendente",
   "Válvula de cuchilla: DN50 a DN600, hasta PN40 y ANSI 150, temperatura hasta +100 °C",
   "Válvula de cuchilla: disco con función de cizalla que retira residuos y evita la fuga por "
   "acumulación en el sello",
   "Válvula de cuchilla: disco de acero inoxidable para evitar la corrosión del sello",
   "Válvula de compuerta: DN40 a DN600, PN16/PN40/PN63, para servicio de corte sin regulación",
   "Válvula de compuerta: baja resistencia al flujo y rango amplio de presión y temperatura",
 ],
 "clientes_target":[
   "Estanques y reactores que requieren vaciado completo (alimentación)",
   "Química, petróleo, metalurgia, farmacéutica, pesticidas, tinturas y alimentos "
   "(alcance declarado de la válvula de alimentación)",
   "Papel y celulosa: válvula de cuchilla para pasta y fibra",
   "Minería y drenaje de agua: válvula de cuchilla para material en polvo y lodo",
   "Petroquímica: cuchilla para fibra y pasta",
   "Líneas de corte que no requieren regulación (compuerta)",
 ],
 "competencia":"POR COMPLETAR — sin battlecard. En válvulas de cuchilla y compuerta el segmento chileno "
   "tiene oferta de fabricantes especializados (DeZURIK, Orbinox, VAT y fabricantes nacionales). "
   "INFERENCIA de mercado, no dato del material.",
 "argumentos_venta":[
   "La válvula de alimentación resuelve el problema del volumen residual del fondo: es una necesidad "
   "de proceso, no una mejora",
   "El disco cortante de la válvula de cuchilla limpia los residuos adheridos solos, así que no hay "
   "que desarmar para destapar",
   "La cuchilla en acero inoxidable se especifica justamente para que la corrosión del disco no "
   "provoque fuga",
   "Rango amplio: cuchilla hasta DN600 y compuerta hasta DN600 en PN63",
   "Son las únicas del portafolio que ya tienen una marca fuerte en Chile (VAT y Orbinox en cuchilla)"
   " — competir acá exige argumento de precio o de plazo, no de tecnología",
 ],
 "objeciones":[
   ("La válvula de cuchilla la compramos a un especialista","Es cierto que el segmento tiene "
     "fabricantes especializados con marca consolidada. La ventaja de incluirla es que permite cerrar "
     "el paquete completo de la planta con un solo proveedor."),
   ("¿La de alimentación es necesaria si ya tenemos válvula de fondo?","El material la presenta como "
     "alternativa al volumen residual típico de la salida del estanque. Hay que evaluar la instalación "
     "concreta: es una decisión de diseño, no un reemplazo automático."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿Qué servicio cumple: vaciado de fondo, corte de pasta o corte de línea?",
   "¿El fluido tiene sólidos, pasta o material en polvo?",
   "¿Qué diámetro requiere la línea?",
   "¿Qué presión y temperatura de operación tiene?",
   "¿La instalación del estanque permite brida de fondo? (válvula de alimentación)",
   "¿Cuánta frecuencia de accionamiento tendrá?",
   "¿Requiere actuador automático o es de operación manual?",
 ],
 "fuente": FUENTE_PDF,
}

json.dump(F, open(os.path.join(DATOS, "fichas_5_datos.json"), "w"), ensure_ascii=False, indent=1)
print(f"fichas de valvulas: {len(F)}")
for n, f in F.items():
    print(f"  {n[:58]:60s} fam={f['familia']:12s} benef={len(f['beneficios']):>2} "
          f"cli={len(f['clientes_target']):>2} arg={len(f['argumentos_venta']):>2} obj={len(f['objeciones']):>2}")
print(f"\nguardado: datos/fichas_5_datos.json")
