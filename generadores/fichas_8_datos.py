#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATOS de fichas de los MÓDULOS ASOCIADOS AL DCS ECS-700 (8a entrega).

Salen de la web del fabricante (supinco.com y global.supcon.com), no del material local:
el árbol de carpetas no traía estos productos por separado. Es la lección de la validación
de cobertura: la ausencia de archivo local no es ausencia de producto.

Productos: SAMS (gestión de activos de instrumentos), FF Foundation Fieldbus, JX-300XP
(plataforma PCS de la generación anterior, aún comercializada) y SCSS (ciberseguridad).
SCSS ya está cubierta por la ficha de Ciberseguridad OT de la 4a entrega: no se duplica.

Genera: datos/fichas_8_datos.json
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

F = {}

F["SAMS (gestión de activos de instrumentos)"] = {
 "familia":"DCS",
 "descripcion":"Sistema de gestión de activos de SUPCON (SUPCON Asset Management System). Es el "
   "componente de software de la solución de gestión de instrumentos inteligentes: administra "
   "instrumentos HART y Foundation Fieldbus, con monitoreo de estado del dispositivo, configuración, "
   "diagnóstico de fallas, alarmas de dispositivo y registro de operaciones. Incluye función de "
   "diagnóstico PST (prueba de carrera parcial) para instrumentos y válvulas mediante DTM de equipo.",
 "beneficios":[
   "Gestiona instrumentos HART y Foundation Fieldbus desde un solo sistema",
   "Monitoreo de estado del dispositivo, configuración y diagnóstico de fallas",
   "Función de diagnóstico PST (Partial Stroke Test) para válvulas e instrumentos",
   "El PST permite extender el intervalo entre pruebas de válvulas de seguridad y reducir el costo "
   "de mantención de la planta (beneficio declarado por el fabricante)",
   "Registro de operaciones y alarmas de dispositivo: trazabilidad para auditoría",
   "Se integra con el ECS-700 y con el resto de la plataforma de automatización",
   "Usa DTM de equipo, que es el estándar abierto de descripción de dispositivos (FDT/DTM): "
   "no queda atado a instrumentos de una sola marca",
 ],
 "clientes_target":[
   "Plantas con instrumentación inteligente HART o Foundation Fieldbus instalada",
   "Operaciones que necesitan reducir el intervalo de pruebas de válvulas de seguridad (PST)",
   "Instalaciones con requisito de trazabilidad de mantención de instrumentos",
   "Plantas que quieren pasar de mantenimiento correctivo de instrumentos a predictivo",
   "Clientes que ya tienen ECS-700 o TCS-900 y quieren sumar la capa de gestión",
 ],
 "competencia":"POR COMPLETAR — sin battlecard en el material. El segmento se llama históricamente "
   "AMS (Asset Management System) y su incumbente es Emerson con AMS Device Manager, seguido de "
   "Endress+Hauser (FieldCare/Netilion), Yokogawa (FieldMate) y Honeywell. INFERENCIA de mercado: "
   "Emerson AMS es el estándar de facto y viene incluido en la mayoría de las bases instaladas de "
   "instrumentación inteligente.",
 "argumentos_venta":[
   "El PST es el argumento económico concreto: extender el intervalo entre pruebas de válvulas de "
   "seguridad reduce directamente el costo de mantención y las paradas de planta",
   "Usa DTM estándar (FDT/DTM), así que puede gestionar instrumentos de otras marcas: no obliga a "
   "tener todo SUPCON",
   "Es la puerta de entrada al mantenimiento predictivo de instrumentos, que es un discurso que ya "
   "tiene CONECTA en otras líneas (PRIDE, MP3000)",
   "Se vende como agregado a una venta de DCS o de instrumentación, con lo que sube el ticket de "
   "la misma conversación",
   "Gestiona HART y Fieldbus: cubre tanto la base instalada antigua como los proyectos nuevos",
 ],
 "objeciones":[
   ("Ya usamos Emerson AMS","Es el incumbente del segmento. La entrada honesta es por planta donde no "
     "haya AMS instalado, o evaluando el costo de licencia de un sistema frente al otro."),
   ("Nuestra instrumentación no es inteligente","Entonces el caso es más débil hoy, pero el PST "
     "aplica igual a las válvulas de seguridad, que casi siempre tienen posicionador inteligente. "
     "Es por ahí donde conviene partir."),
   ("¿Puede gestionar instrumentos de otras marcas?","El material declara uso de DTM de equipo, que es "
     "el mecanismo estándar FDT/DTM para describir dispositivos de cualquier fabricante. POR COMPLETAR: "
     "confirmar la lista de DTM certificados disponibles."),
   ("¿Quién implementa y mantiene el sistema?","POR COMPLETAR: la gestión de activos requiere cargar "
     "la base de instrumentos, que es trabajo de terreno. Hay que dimensionar esa ingeniería en la "
     "oferta, porque no es solo licencia."),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos instrumentos inteligentes tiene la planta?",
   "¿Cuántos son HART y cuántos Foundation Fieldbus?",
   "¿Cuántas válvulas de seguridad con posicionador tiene la planta?",
   "¿Cuál es el intervalo actual de prueba de las válvulas de seguridad?",
   "¿Usa un sistema de gestión de activos hoy? ¿De qué marca?",
   "¿Quiere integrar el sistema con el DCS para ver el diagnóstico en el lazo?",
   "¿Necesita trazabilidad de mantención para auditoría?",
   "¿Quién cargará y mantendrá la base de datos de instrumentos?",
   "¿Requiere gestión de instrumentos de otras marcas?",
   "¿El objetivo es reducir costo de mantención, evitar paradas o cumplir normativa?",
 ],
 "fuente":"supinco.com/products/supcon-webfield-ecs-700/ (sección 'SAMS SUPCON Asset Management "
   "System'). Producto del fabricante no presente en el material local.",
}

F["FF Foundation Fieldbus (sobre ECS-700)"] = {
 "familia":"DCS",
 "descripcion":"Sistema Foundation Fieldbus de SUPCON, montado sobre la plataforma ECS-700. Conforma "
   "los estándares 61b de sistema host FF y cubre los requisitos de aplicación de un proyecto Fieldbus. "
   "El sistema usa FCS simplificado, con alta distribución y autocontrol con los dispositivos de campo.",
 "beneficios":[
   "Conforma el estándar 61b de sistema host Foundation Fieldbus",
   "Más de 350 fabricantes ofrecen dispositivos Fieldbus certificados por Fieldbus Foundation que "
   "pueden conectarse",
   "La infraestructura FCS simplificada reduce el costo de inversión",
   "Alta distribución y autocontrol con los dispositivos de campo: mejora el desempeño del control",
   "Basado en el modelo de interconexión de sistemas abiertos ISO/OSI, con H1 y capa de usuario "
   "conforme a IEC 61158-2",
   "Control y diagnóstico en el propio instrumento: menos cableado al sistema de control",
   "Beneficios declarados en diseño, instalación, comisionamiento, arranque, operación y mantención",
 ],
 "clientes_target":[
   "Proyectos nuevos que especifican Foundation Fieldbus como red de campo",
   "Plantas con base instalada FF que necesitan un host compatible",
   "Aplicaciones donde el control distribuido en el instrumento reduce cableado y costo de instalación",
   "Instalaciones que requieren interoperabilidad con instrumentos de múltiples fabricantes",
   "Clientes que ya tienen ECS-700 y quieren extenderlo con red de campo digital",
 ],
 "competencia":"POR COMPLETAR — sin battlecard. El segmento de host Foundation Fieldbus lo dominan "
   "Emerson (DeltaV), Yokogawa (CENTUM) y Honeywell, que tienen FF integrado en sus DCS desde hace "
   "más de dos décadas. INFERENCIA de mercado. La ventaja de SUPCON es el costo, no la madurez: "
   "conviene no entrar por un proyecto FF crítico sin referencias propias.",
 "argumentos_venta":[
   "Interoperabilidad declarada con más de 350 fabricantes: no encierra al cliente en una marca de "
   "instrumentos",
   "Reduce cableado y costo de instalación, que es el argumento clásico del bus de campo",
   "El control vive en el instrumento, así que la planta sigue operando si falla la comunicación "
   "con la sala de control",
   "Se ofrece sobre la misma plataforma ECS-700, así que no exige un sistema de control adicional",
   "Los beneficios están declarados en todo el ciclo del proyecto, lo que permite usarlo como "
   "argumento en cada etapa",
 ],
 "objeciones":[
   ("Fieldbus es más complejo de ingeniería y mantener","Es una objeción real y reconocida en el "
     "segmento: exige disciplina de segmento, terminadores y herramientas de diagnóstico. Hay que "
     "calificar si el cliente tiene el equipo para operarlo."),
   ("Ya usamos 4-20 mA HART y funciona","El argumento del bus de campo es el ahorro de cableado y el "
     "diagnóstico del instrumento, no que 4-20 mA no funcione. En una planta existente, migrar tiene "
     "costo alto: aplica mejor en proyecto nuevo o ampliación."),
   ("¿Hay ingenieros FF certificados disponibles?","POR COMPLETAR: es el punto crítico del segmento. "
     "Sin certificación FF en el equipo que implementa, el proyecto se complica. Verificar antes de "
     "comprometer."),
   ("¿Es maduro comparado con el FF de Emerson o Yokogawa?","La pregunta es legítima: ellos llevan más "
     "de veinte años con FF integrado. POR COMPLETAR: pedir al fabricante referencias de proyectos FF "
     "en operación antes de ofrecer en un caso crítico."),
 ],
 "preguntas_tecnicas":[
   "¿El proyecto especifica Foundation Fieldbus o 4-20 mA HART?",
   "¿Cuántos segmentos FF requiere la instalación?",
   "¿Cuántos dispositivos por segmento?",
   "¿Qué instrumentos se conectarán y de qué marcas?",
   "¿El cliente tiene experiencia previa en Fieldbus?",
   "¿Hay personal certificado FF en el equipo de ingeniería y mantención?",
   "¿Requiere herramientas de diagnóstico de segmento?",
   "¿El proyecto es nuevo o una ampliación de planta existente?",
   "¿Requiere integración con el sistema de gestión de activos?",
   "¿Qué requisitos de disponibilidad tiene la red de campo?",
 ],
 "fuente":"supinco.com/products/supcon-webfield-ecs-700/ (sección 'FF FOUNDATION Fieldbus System'). "
   "Producto del fabricante no presente en el material local.",
}

F["JX-300XP (plataforma PCS)"] = {
 "familia":"DCS",
 "descripcion":"Plataforma de sistema de control de proceso Webfield JX-300XP, de una generación "
   "anterior al ECS-700 y aún comercializada por SUPCON. Se ofrece como alternativa para plantas de "
   "menor tamaño o para proyectos con presupuesto más ajustado.",
 "beneficios":[
   "Sigue comercializada: hay soporte y repuestos vigentes del fabricante",
   "Plataforma de menor costo de entrada que el ECS-700",
   "Adecuada para plantas de menor complejidad o para proyectos con presupuesto acotado",
   "La instalación base de JX-300XP en China es extensa, lo que da respaldo de aplicaciones",
   "POR COMPLETAR: el material local no tiene documentación de esta plataforma; la ficha se arma "
   "con la referencia del catálogo web del fabricante. Pedir el brochure antes de ofrecer.",
 ],
 "clientes_target":[
   "Plantas pequeñas o medianas que requieren un DCS con presupuesto acotado",
   "Proyectos donde el ECS-700 está sobredimensionado para la cantidad de puntos",
   "Ampliaciones de instalaciones que ya usan JX-300XP",
   "Clientes con presupuesto limitado que necesitan control distribuido confiable",
 ],
 "competencia":"POR COMPLETAR — sin battlecard. En el segmento de DCS de entrada compiten las "
   "plataformas de gama baja de Siemens, Schneider y los fabricantes locales. INFERENCIA de mercado.",
 "argumentos_venta":[
   "Costo de entrada menor que el ECS-700: permite entrar en proyectos que no alcanzan para la "
   "plataforma alta",
   "El fabricante lo mantiene vigente, así que no es un producto descatalogado",
   "Sigue siendo un DCS, no un PLC: mantiene el discurso de control distribuido y no baja la "
   "conversación a automatización discreta",
   "POR COMPLETAR: pedir la comparación técnica con el ECS-700 para no ofrecer la plataforma "
   "equivocada. Sin ese dato, hay riesgo de recomendar una plataforma que no soporte los requisitos.",
 ],
 "objeciones":[
   ("Es una plataforma antigua, prefiero el ECS-700","Puede tener razón y hay que evaluarlo caso a "
     "caso: si el ECS-700 cabe en el presupuesto, es la opción correcta porque es la plataforma "
     "vigente del fabricante. El JX-300XP es una alternativa de costo, no una recomendación por defecto."),
   ("¿Tiene el mismo respaldo y repuestos?","El fabricante lo mantiene en catálogo. POR COMPLETAR: "
     "confirmar el compromiso de soporte y la disponibilidad de repuestos para Chile, que es el "
     "riesgo real de una plataforma de generación anterior."),
   ("¿Puedo migrar después al ECS-700?","POR COMPLETAR: hay un documento de ciclo de vida del ECS-700 "
     "mencionado en el catálogo del fabricante. Pedir la ruta de migración antes de ofrecer, porque "
     "el cliente va a preguntar si queda atrapado en una plataforma antigua."),
   ("POR COMPLETAR",""),
 ],
 "preguntas_tecnicas":[
   "¿Cuántos puntos de IO controla la planta? (define si el ECS-700 está sobredimensionado)",
   "¿Cuál es el presupuesto disponible para el sistema de control?",
   "¿El proyecto es nuevo o una ampliación de una instalación JX-300XP existente?",
   "¿Qué requisitos de redundancia tiene?",
   "¿Necesita integración con Fieldbus o HART?",
   "¿Cuántos años de soporte requiere para la plataforma?",
   "¿Existe una ruta de migración al ECS-700 si la planta crece?",
   "POR COMPLETAR: capacidades y límites técnicos del JX-300XP — pedir brochure al fabricante",
 ],
 "fuente":"supinco.com/products/ (catálogo del fabricante: 'Webfield JX-300XP'). Producto del "
   "fabricante no presente en el material local. Sin brochure: la mayoría de los campos técnicos "
   "quedan POR COMPLETAR.",
}

json.dump(F, open(os.path.join(D, "fichas_8_datos.json"), "w"), ensure_ascii=False, indent=1)
print(f"fichas de modulos del DCS: {len(F)}")
for n, f in F.items():
    print(f"  {n[:50]:52s} fam={f['familia']:6s} b={len(f['beneficios']):>2} c={len(f['clientes_target']):>2} "
          f"a={len(f['argumentos_venta']):>2} o={len(f['objeciones']):>2} p={len(f['preguntas_tecnicas']):>2}")
print(f"\nguardado: datos/fichas_8_datos.json")
