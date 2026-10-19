# Prompt para Gamma — Workshop ConectaTalento 2026 (v2: diseño + Ventas Técnicas)

> **El orden importa.**
> 1. Crear primero el **tema personalizado** (Sección A) en Gamma → Theme → Custom Theme.
>    Si no, Gamma aplica un tema de su galería y se pierde la marca CONECTA.
> 2. En "Paste in text": abrir el menú **Visuals** → elegir el tema CONECTA recién creado
>    → Images: **No images** (o "Abstract" si obliga a elegir).
> 3. Pegar la Sección B (el contenido).
> 4. Opcional, para afinar: pegar la Sección A.5 en el **Custom CSS** del tema.

---

# SECCIÓN A — TEMA PERSONALIZADO (crear antes de generar)

## A.1 Colores (hex reales, tomados de conecta.cl)

| Rol en Gamma | Hex | Uso |
|---|---|---|
| Background / card bg | `#0A1628` | Fondo base oscuro |
| Background alterno | `#FFFFFF` | Slides claras |
| Accent / Primary | `#2563EB` | Kickers, cifras, destacados |
| Accent sobre oscuro | `#60A5FA` | Kickers en slides oscuras |
| Texto sobre oscuro | `#F1F5F9` | Títulos en slides oscuras |
| Texto secundario oscuro | `#94A3B8` | Cuerpo en slides oscuras |
| Texto sobre claro | `#0F172A` | Títulos en slides claras |
| Texto secundario claro | `#475569` | Cuerpo en slides claras |
| Acento verde | `#10B981` | Solo línea PROCESOS |
| Acento naranja | `#F26522` | Solo Ventas Técnicas |
| Bordes | `#1E293B` / `#E2E8F0` | Separadores suaves |

## A.2 Tipografía

- **Headings:** `Outfit`, peso 700, interletrado -1.5 px, 44-64 px.
- **Body:** `Inter`, peso 400, 16-19 px, interlineado 1.5.
- **Kicker** (etiqueta chica sobre el título): `Outfit`, 13 px, MAYÚSCULAS,
  interletrado +1.6 px, color `#2563EB`.

## A.3 Estructura de slide

- Márgenes: **64 px arriba/abajo, 76 px izquierda/derecha**. Nada toca el borde.
- **Marca** arriba a la izquierda en TODAS las slides: un **punto azul de 8 px** +
  `CONECTA` (mayúscula, bold, 20 px) + `S.A.` (16 px, gris `#94A3B8`, 55% opacidad).
- Kicker debajo de la marca (18 px de aire). Luego título. Luego contenido.
- Fuente de datos al pie, 12.5 px, gris. Numeración de slide al pie.

## A.4 Reglas visuales

- **Alternar fondo:** impares oscuras (`#0A1628`), pares claras (`#FFFFFF`).
  Excepciones: portada y cierre oscuras; la slide de actitud en gris muy claro `#F8FAFC`.
- **Cifras grandes:** 46-64 px, peso 800, color de acento, cifra y unidad separadas
  (`106` grande + `TWh` chico al lado).
- **Tarjetas:** esquinas 12-16 px, sin sombra fuerte, borde 1 px suave.
- **Cita/destacado:** barra vertical de 4 px del color de acento a la izquierda, fondo
  `#EFF6FF` en claro / `rgba(37,99,235,.14)` en oscuro, tipografía Outfit.
- **Prohibido:** fotos de stock, gente sonriendo en oficinas, íconos decorativos,
  degradados llamativos, sombras dramáticas, emojis.

## A.5 Custom CSS del tema (pegar en Theme → Custom CSS)

```css
:root{
  --cx-navy:#0A1628; --cx-navy2:#0F1F3D; --cx-blue:#2563EB;
  --cx-blue-l:#60A5FA; --cx-green:#10B981; --cx-orange:#F26522;
  --cx-tx:#0F172A; --cx-tx2:#475569; --cx-tx3:#94A3B8; --cx-bd:#E2E8F0;
}
h1,h2,h3{font-family:'Outfit',sans-serif;letter-spacing:-1.5px;line-height:1.1}
body,p,li{font-family:'Inter',sans-serif;line-height:1.55}
.kicker,.eyebrow{font-family:'Outfit',sans-serif;font-size:13px;font-weight:700;
  letter-spacing:1.6px;text-transform:uppercase;color:var(--cx-blue)}
.card{border-radius:14px;border:1px solid var(--cx-bd)}
.stat-number{font-family:'Outfit',sans-serif;font-weight:800;letter-spacing:-2px}
```

---

# SECCIÓN B — CONTENIDO (pegar en "Paste in text")

Crea una presentación de **17 slides** en **español de Chile** (tuteo, no voseo) para una
exposición de **15 minutos** en la **Facultad de Ingeniería de la Pontificia Universidad Católica
de Valparaíso**, en el **Workshop ConectaTalento 2026** (feria de práctica profesional y primer
empleo).

**Audiencia:** estudiantes de ingeniería **a punto de titularse**, que buscan práctica profesional
o primer empleo. No son clientes. No van a comprar nada.

**Objetivo:** atraer talento a CONECTA, una empresa chilena de ingeniería eléctrica, automatización
y digitalización industrial que está en crecimiento acelerado y necesita contratar mucha gente.

**Tono:** directo, sin marketing inflado, sin adjetivos vacíos. Habla de cifras reales y de trabajo
concreto. Nada de "somos líderes", "sinergia", "revolucionario" ni signos de admiración.
El presentador es Víctor Vilche, ingeniero eléctrico, CEO de CONECTA.

**Estructura narrativa obligatoria:**
1. Primero el MUNDO (qué va a pasar en Chile en los próximos 20 años).
2. Después la EMPRESA, con **TRES caminos**: dos técnicos (POWER y PROCESOS) y uno comercial
   (**VENTAS TÉCNICAS**).
3. Al final, lo más importante: **la ACTITUD y el LIDERAZGO** con que se hacen las cosas.
4. Cierre con invitación concreta: hacer la práctica en CONECTA.

---

## Slide 1 — Portada
Kicker: WORKSHOP CONECTATALENTO 2026 · 3ª EDICIÓN
Título: **Lo que viene en los próximos veinte años**
Subtítulo: Y por qué conviene empezar acá
Pie: Víctor Vilche · Ingeniero Eléctrico · CEO CONECTA · Facultad de Ingeniería PUCV · 20 de octubre de 2026

## Slide 2 — El punto de partida
Kicker: EL PUNTO DE PARTIDA
Título: **Están a punto de titularse. La próxima decisión es esta.**
Dos bloques:
- **La práctica y el primer trabajo no son trámites** — Son la primera decisión de carrera. Y no la define el primer sueldo.
- **Les quedan cuarenta años de trabajo** — La pregunta no es qué hay hoy. Es dónde estará el trabajo que siga existiendo en 2046.

## Slide 3 — Tendencia 1
Kicker: TENDENCIA 1 · ENERGÍA
Título: **La demanda eléctrica se duplica al 2035**
Tres cifras grandes: **106 TWh** (escenario medio) · **117 TWh** (escenario alto) · **149 TWh** (con hidrógeno verde)
Pie: Fuente: Coordinador Eléctrico Nacional, proyección de demanda del SEN

## Slide 4 — Tendencia 2
Kicker: TENDENCIA 2 · INVERSIÓN
Título: **US$ 104.549 millones en minería al 2034**
Dos bloques:
- **51 proyectos** — Plantas, moliendas, fundiciones, relaves, puertos, líneas eléctricas.
- **Cada uno necesita** — Un sistema de control, protecciones, instrumentación, una subestación y un equipo que lo ponga en marcha.
Pie: Fuente: Cochilco, cartera de proyectos mineros 2025-2034

## Slide 5 — Tendencia 3
Kicker: TENDENCIA 3 · PERSONAS
Título: **Faltan 37.000 personas. Y el 75% en cuatro perfiles**
Tres cifras: **~37.000** nuevos trabajadores al 2034 · **73-75%** en 4 perfiles · **88%** son reemplazos, no proyectos nuevos
Franja destacada: Mantenedor mecánico · Mantenedor eléctrico · Operador de equipo móvil · Operador de equipo fijo
Pie: Fuente: CCM-Eleva / Consejo Minero, estudio de fuerza laboral

## Slide 6 — Tendencia 4
Kicker: TENDENCIA 4 · EL OFICIO
Título: **El ingeniero ya no trabaja solo**
Dos bloques:
- **Antes** — El dato estaba en un tablero y en un papel. Se decidía con lo que se veía.
- **Hoy** — Hay miles de señales por planta que nadie ocupa. Decide el que sabe qué preguntar.
Cita destacada: *La diferencia entre un ingeniero bueno y uno muy bueno ya no es calcular. Es saber qué dato importa.*

## Slide 7 — Bisagra
Kicker: CUATRO CAMINOS
Título: **En CONECTA hay cuatro formas de ser ingeniero**
- **POWER** — La red, la subestación y la protección. El sistema eléctrico.
- **PROCESOS** — El interior de la planta. El proceso industrial.
- **CUMPLIMIENTO NORMATIVO** — El ingeniero que sabe demostrarle al Coordinador que la planta cumple.
- **VENTAS TÉCNICAS** — El ingeniero que entiende al cliente y sabe qué venderle.
Pie: No es el mismo trabajo. Conviene saber a cuál apuntar.

## Slide 8 — Línea POWER
Kicker: LÍNEA POWER (en azul #2563EB)
Título: **La red, la subestación, la protección**
Lista (7 ítems): Subestaciones eléctricas · Protecciones y ajustes · **SISTEMAS SCADA: sala de control, HMI, histórico, alarmas** · RTU y gateways (OrionLX+) · Calidad de energía y medición · Sincronización por satélite · Red OT y ciberseguridad IEC 62443
Tarjetas laterales:
- **Representamos:** NovaTech (Orion SCADA, RTU, Kronos) · Vizimax · Belden / Hirschmann
- **Perfiles que entran:** Eléctrica · Electrónica · Control · Informática
- Destacado en cursiva: *El SCADA es el que ve TODO. Si no está bien hecho, el operador trabaja a ciegas — y ahí nace el apagón.*

## Slide 9 — Arquitectura: dónde vendemos
Kicker: LÍNEA POWER · DÓNDE VENDEMOS (azul)
Título: **La cadena completa: de la central al cliente**
Diseño: cadena horizontal de CINCO bloques numerados, cada uno con nombre y subtítulo:
1. **Generación** — Hidro · solar · eólica · térmica
2. **Transmisión** — Alta tensión y SE primarias
3. **Subestación** — El nodo donde todo se conecta
4. **Distribución** — Media tensión y clientes libres
5. **Consumo** — Minas · plantas · puertos
Debajo, una BANDA OSCURA (#0A1628) de ancho completo titulada "TRANSVERSAL A TODOS LOS ESLABONES" con cuatro cajas (borde verde #10B981):
- **Sala de control / SCADA** — HMI, histórico, alarmas, reportes
- **Comunicaciones OT** — Switches IEC 61850-3, ciber IEC 62443
- **Protección y medición** — Relés, ajustes, TC/TP, calidad de energía
- **Sincronización** — Reloj GPS: sin esto los fasores no sirven
Leyenda al pie: cuadro azul "CONECTA vende e integra" · cuadro verde "Transversal: aplica en todos lados".
IMPORTANTE: la banda transversal NO es una etapa más de la cadena, es una capa que aplica a todas. Debe verse visualmente distinta (oscura, ancho completo, sin flechas que la conecten).

## Slide 10 — Cumplimiento normativo
Kicker: CUMPLIMIENTO NORMATIVO (en morado #7C3AED)
Título: **La planta que no lo demuestra, no cobra**
Lista (6 ítems, viñetas moradas):
1. **SSCC: los 4 servicios complementarios (CPF, CSF, CTF, CT)**
2. **EDAC / EDAG y ROCOF: respuesta ante perturbaciones**
3. **Informes de conexión y puesta en servicio**
4. **Reportes periódicos al Coordinador Eléctrico**
5. **Verificación IBR Grid-Forming (nuevo 2026)**
6. **Ciberseguridad: Ley 21.663**
Tarjetas laterales:
- **Normativa:** NTSyCS · protocolo CPF · guía IBR GFM v0 (mayo 2026)
- **Perfiles que entran:** Eléctrica · Electrónica · Control — y saber leer una norma
- Destacado en cursiva sobre fondo lila: *Si el dato no llega en el formato que el Coordinador exige, la planta genera energía y NO cobra ese servicio. La plata está en demostrar, no solo en operar.*

## Slide 11 — Línea PROCESOS
Kicker: LÍNEA PROCESOS (en verde #10B981)
Título: **El interior de la planta, con SUPCON**
Lista: DCS ECS-700 y SIS TCS-500 · Instrumentación · Válvulas y posicionadores · Analizadores y CEMS · Optimización avanzada · Predictivo y capa de datos
Tarjetas laterales:
- **Representamos:** SUPCON
- **Perfiles que entran:** Mecánica · Química · Electrónica · Eléctrica
- Destacado en cursiva: *Se aprende la planta, no el equipo. Por qué se rompe, no solo que se rompió.*

## Slide 12 — Ventas Técnicas
Kicker: VENTAS TÉCNICAS (en naranja #F26522)
Título: **El ingeniero que vende no deja de ser ingeniero**
Párrafo de entrada: Acá un vendedor no es alguien que repite un discurso. Es un ingeniero que entiende el problema del cliente, aterriza la solución y responde por ella cuando se pone en marcha.
Dos columnas:
- **Lo que hace** — Visitar plantas y subestaciones · Levantar el requerimiento real · Armar la propuesta técnica y económica · Cotizar y sustentar el precio · Acompañar la puesta en marcha
- **Lo que tiene que saber** — El equipo que vende · El proceso del cliente · Costos y márgenes · Leer un plano y una hoja de datos · Hablar con un jefe de planta y con un comprador
Destacado: *Se vende lo que se entiende. Sin base técnica, la venta es de intermediario.*

## Slide 13 — Dónde se aprende
Kicker: DÓNDE SE APRENDE
Título: **En terreno, no en un PowerPoint**
- **A la minera** — Con el ruido, el polvo y el turno de noche.
- **A la subestación** — Con el plano en la mano y el equipo energizado.
- **A la planta** — Cuando algo falla y hay que resolverlo ahora.
Cita: *Eso no lo enseña la universidad. Y no se aprende leyendo.*

## Slide 14 — Cómo crecemos
Kicker: CÓMO CRECEMOS
Título: **No se entra a un puesto: se construye uno**
- **En una empresa grande** — Hay un organigrama y un lugar reservado.
- **Acá** — El organigrama se escribe con los que llegan.
Cita: *Es más difícil. Y es la mejor escuela que hay.*

## Slide 15 — Lo que buscamos
Kicker: LO QUE BUSCAMOS
Título: **No buscamos el mejor promedio**
- **El promedio** — Dice que alguien sabe memorizar.
- **Lo que miramos** — Que le importe hacer bien las cosas, que pregunte cuando no entiende y que se haga cargo.
Cita grande y destacada: **En diez años, el que se destacó no fue el que sabía más. Fue el que se hizo cargo.**

## Slide 16 — Actitud y liderazgo
Kicker: ACTITUD Y LIDERAZGO
Título: **El liderazgo empieza el primer día**
Cuatro tarjetas:
- **Se hace cargo** — Cuando algo sale mal, la primera frase no es "fue el otro".
- **Pregunta** — "No lo sé, lo averiguo y te aviso" vale más que una respuesta inventada.
- **Cumple** — Si dijiste a las 8, a las 7:50 estás. El liderazgo es que tu palabra valga.
- **Le importa** — Anotar el dato que te pidieron aunque nadie te esté mirando.

## Slide 17 — Cierre
Kicker: LA INVITACIÓN
Título: **Hagan la práctica acá**
Subtítulo: No para quedarse para siempre. Para saber lo que es la ingeniería de verdad.
Pie: Los espero en el MatchUp con un desafío real. · Víctor Vilche · CEO · CONECTA
Incluir la línea: Vendemos · Diseñamos · Instalamos · Ponemos en marcha. No tercerizamos el problema.

---

# SECCIÓN C — REGLAS DURAS (pegar al final del contenido)

- **No agregar estadísticas, cifras ni datos** que no estén arriba. Todas las cifras tienen fuente
  y horizonte; no extrapolar ni completar.
- **No mencionar clientes por nombre** (Codelco, BHP, etc.) salvo en la lista de empresas que
  participan del evento, que no va en el deck.
- **No poner precios, sueldos, ni cantidad de vacantes** — no están definidos. Se habla de
  **perfiles**, nunca de cupos.
- **No agregar "misión", "visión", "valores"** ni sección de historia de la empresa.
- **Nada en inglés** salvo siglas técnicas del rubro (DCS, SIS, SCADA, RTU, CEMS, HMI).
- **No usar fotos de personas sonriendo en oficinas.** Si Gamma requiere imágenes, preferir
  abstractas geométricas o ninguna.
- Mantener **exactamente 17 slides**.
- **VENTAS TÉCNICAS no es un área menor**: va como slide propia (la 12), con el mismo peso
  visual que POWER y PROCESOS.
