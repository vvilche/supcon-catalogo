# Catálogo SUPCON — Analizadores, Instrumentación y Automatización

Catálogo técnico y comercial del portafolio **SUPCON** (incluida su filial **Hobré Instruments**),
construido a partir del material de producto del fabricante: extracción determinística del texto de
fichas técnicas (PDF) y presentaciones (PPTX), sin intervención de modelos de lenguaje.

## Origen del material

SUPCON Technology (688777.SH) adquirió el **100% de Hobré International BV** en abril de 2023
(filial bajo SUPCON International Holding Pte. Ltd., Singapur). Hobré conserva sede en Purmerend
(Países Bajos), planta en Szeged (Hungría) y oficina en Houston (EE.UU.).

Fuente primaria de la adquisición: informe semestral 2023 de SUPCON Technology, anuncio de
aumento de capital a Hobré (RMB 217,95 millones, sep-2023), y el asesor financiero del vendedor
(EC M&A).

## Contenido

```
generadores/    scripts Python que extraen los datos y generan los artefactos (cero LLM)
artefactos/     salidas HTML autocontenidas
datos/          JSON con el texto extraído y las especificaciones verificadas
docs/           capturas de la verificación en navegador
```

### Artefactos

| Archivo | Contenido |
|---|---|
| `artefactos/catalogo_supcon.html` | 55 fichas de producto agrupadas en 12 familias, con filtro y buscador |
| `artefactos/fichas_producto_supcon.html` | 6 fichas comerciales con los 8 campos (descripción, beneficios, clientes target, competencia, argumentos, objeciones, preguntas técnicas) |
| `artefactos/mockup_diseno.html` | mockup de diseño del layout |
| `artefactos/estrategia_penetracion.html` | escalones de dificultad de penetración comercial |
| `artefactos/estrategia_normativa.html` | cruce de las 7 líneas con el disparador normativo chileno (norma, obligación, industrias y empresas afectadas) |

### Datos

| Archivo | Contenido |
|---|---|
| `datos/fichas_extraidas.json` | texto crudo de las 59 fichas (PDF y PPTX) |
| `datos/analizadores_supcon.json` | especificaciones verificadas de los 4 analizadores Hobré, con fuente por dato |
| `datos/inventario_familias.json` | los 567 archivos de producto clasificados por familia |

## Generadores

```bash
# 1) extraer el texto de las fichas 1-Pager (requiere el material del fabricante en disco)
python3 generadores/extraer_fichas.py

# 2) generar el catálogo por familias
python3 generadores/generar_catalogo.py

# 3) generar las fichas comerciales de 8 campos
python3 generadores/generar_fichas_producto.py
```

El material fuente (PDF y PPTX del fabricante) **no está en este repositorio**: las rutas absolutas
dentro de los generadores apuntan a la carpeta local `Documentos/ConocimientoSupcon`. Para
reproducir, hay que tener ese material en la misma ruta.

Dependencias: `pymupdf` (lectura de PDF), `tesseract` + `pdftoppm` (OCR de PDF escaneado),
`unar` (archivos `.7z`). Todo lo demás es biblioteca estándar de Python.

## Estado y alcance

- **Verificado en navegador real** antes de publicar: conteo de nodos, filtros, buscador y
  apertura de fichas funcionando; sin errores de JavaScript.
- Los analizadores Hobré (C-QUAND, TISOMIC, WIM COMPAS, PRISM) tienen especificaciones completas
  extraídas de las fichas del fabricante.
- El resto del catálogo tiene el nombre y la fuente de cada ficha; las fichas comerciales están
  completas solo para 6 productos.
- Los campos marcados **POR COMPLETAR** requieren validación con el fabricante antes de usarse
  con un cliente. No se inventó ningún dato: lo que no está respaldado por el material queda
  marcado explícitamente.

## Advertencias

- El sistema **CEMS 5000** cita normas chinas (HJ75 / HJ76). La equivalencia con otra normativa
  local debe verificarse antes de ofrecer el equipo.
- El **Flare CEMS** cita normativa federal y estatal de EE.UU. (40 CFR 60.18, 40 CFR 63.670,
  TCEQ Cap. 115, SCAQMD Rule 1118). El proyecto documentado para Corea es una **propuesta**, no
  una instalación confirmada.
- No hay precios en el material del fabricante.

## Licencia

Documentación técnica de referencia. Los nombres de producto y las especificaciones pertenecen a
sus respectivos fabricantes (SUPCON Technology / Hobré Instruments).
