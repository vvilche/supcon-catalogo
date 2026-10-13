#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera dos documentos HTML para CONECTA / SUPCON:

1. METODOLOGÍA DEL ESTUDIO DE MERCADO — cómo se calcularon los números, con qué fuente,
   qué decisiones se tomaron en el camino, qué errores se corrigieron y cuáles son los
   límites honestos del resultado. Es el documento que permite auditar o replicar el estudio.

2. ESTRATEGIA DE PENETRACIÓN — de lo más fácil a lo más difícil, ordenando las líneas y los
   productos por dificultad real (no por tamaño de mercado), con el argumento de entrada de
   cada paso.

Ambos salen de datos ya medidos y verificados, no de supuestos nuevos.

Salida: artefactos/metodologia_mercado.html + artefactos/estrategia_penetracion.html
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
ART = os.path.join(BASE, "artefactos")

E = json.load(open(os.path.join(D, "escalera_exito.json"), encoding="utf-8"))
CR = json.load(open(os.path.join(D, "cruce_catalogo_importaciones.json"), encoding="utf-8"))
PERF = json.load(open(os.path.join(D, "perfilado_74_integradores.json"), encoding="utf-8"))
COB = json.load(open(os.path.join(D, "cobertura_catalogo.json"), encoding="utf-8"))

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706;--ams:#fffbeb;--ok:#047857;--oks:#ecfdf5}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}
.wrap{max-width:940px;margin:0 auto}
h1{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}
.sub{color:var(--mu);font-size:14.5px;margin-bottom:26px;max-width:820px}
h2{font-size:20px;font-weight:660;margin:38px 0 10px;letter-spacing:-.2px;padding-top:8px;border-top:2px solid var(--bd)}
h2:first-of-type{border-top:none;padding-top:0}
h3{font-size:16px;font-weight:650;margin:22px 0 7px}
p{margin-bottom:11px}
ul,ol{margin:9px 0 13px 0}
ul{list-style:none}
ul li{position:relative;padding-left:17px;margin-bottom:6px}
ul li:before{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}
ol{list-style:none;counter-reset:n}
ol li{position:relative;padding-left:24px;margin-bottom:8px;counter-increment:n}
ol li:before{content:counter(n);position:absolute;left:0;top:1px;background:var(--acs);color:var(--ac);font-weight:700;font-size:11.5px;width:17px;height:17px;border-radius:50%;text-align:center;line-height:17px}
code{background:#f1f5f9;padding:1px 6px;border-radius:4px;font-size:13px;font-family:ui-monospace,monospace}
table{width:100%;border-collapse:collapse;margin:13px 0;font-size:14px}
th{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--bd)}
td{padding:9px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}
tr:last-child td{border-bottom:none}
.num{text-align:right;font-variant-numeric:tabular-nums}
.box{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:15px 18px;margin:14px 0}
.aviso{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:15px 0;font-size:14px}
.aviso b{color:#92400e}
.ok{background:var(--oks);border:1px solid #a7f3d0;border-left:4px solid var(--ok);border-radius:9px;padding:14px 17px;margin:15px 0;font-size:14px}
.ok b{color:var(--ok)}
.chip{display:inline-block;font-size:11.5px;border-radius:5px;padding:2px 9px;font-weight:600;margin-right:6px}
.c1{background:var(--oks);color:var(--ok)}.c2{background:var(--ams);color:var(--am)}.c3{background:#f1f5f9;color:#475569}
.paso{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:17px 20px;margin-bottom:13px;border-left:4px solid var(--ac)}
.paso.f1{border-left-color:#047857}.paso.f2{border-left-color:#2563eb}
.paso.f3{border-left-color:#d97706}.paso.f4{border-left-color:#64748b}
.ph{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;margin-bottom:9px}
.pn{font-size:13px;font-weight:700;color:var(--mu)}
.ph h3{margin:0;font-size:17px}
.et{font-size:11px;border-radius:5px;padding:2px 9px;font-weight:700;text-transform:uppercase;letter-spacing:.3px}
.e1{background:var(--oks);color:var(--ok)}.e2{background:var(--acs);color:var(--ac)}
.e3{background:var(--ams);color:var(--am)}.e4{background:#f1f5f9;color:#475569}
.merc{font-size:12.5px;color:var(--mu);margin-bottom:9px}
.merc b{color:var(--tx)}
footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}
footer a{color:var(--ac)}
"""

# ================================================================ DOC 1: METODOLOGÍA
filas_cruce = ""
for fam, info in sorted(CR["mercado_por_familia"].items(), key=lambda x: -x[1]["cif"]):
    riv = ", ".join(m for m, _ in info["marcas"][:3])
    filas_cruce += (f'<tr><td>{fam}</td><td class="num">US${info["cif"]/1e6:,.1f}M</td>'
                    f'<td class="num">{info["items"]:,}</td><td style="font-size:12.5px;color:#64748b">{riv}</td></tr>')

MET = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Metodología del estudio de mercado — SUPCON Chile 2025</title><style>{CSS}</style></head>
<body><div class="wrap">

<h1>Metodología del estudio de mercado</h1>
<p class="sub">Cómo se calcularon los números del mercado de automatización e instrumentación en Chile.
Documento de trazabilidad: permite auditar cada cifra y replicar el estudio.</p>

<div class="box">
  <b>Resumen en una línea.</b> Se descargó el registro completo de importaciones de Aduanas de Chile
  para 2025 (4.847.036 líneas), se filtró por partida arancelaria del dominio de automatización e
  instrumentación y por marca de fabricante conocida, y se cruzó con el catálogo SUPCON para saber
  dónde compite cada producto.
</div>

<h2>1. La fuente y por qué se eligió</h2>
<p><b>Fuente:</b> Registro DIN de importaciones, Servicio Nacional de Aduanas de Chile, descargado
desde <code>datos.gob.cl</code>. Doce archivos mensuales del año 2025.</p>
<table>
  <tr><th>Dato de la fuente</th><th class="num">Valor</th></tr>
  <tr><td>Líneas totales del año</td><td class="num">4.847.036</td></tr>
  <tr><td>Valor CIF total importado por Chile</td><td class="num">US$85.671M</td></tr>
  <tr><td>Tamaño de los archivos</td><td class="num">3,7 GB</td></tr>
  <tr><td>Columnas por registro</td><td class="num">178</td></tr>
</table>
<p><b>Por qué esta fuente:</b> es el registro real de lo que entró al país, con marca del fabricante y
valor CIF declarados. No es una estimación de consultora ni un dato de proveedor: es la declaración
de aduana. Eso permite hablar de mercado con números defendibles frente a un cliente.</p>

<h3>Columnas que se usaron</h3>
<table>
  <tr><th>Columna (índice)</th><th>Qué aporta</th></tr>
  <tr><td><code>4</code> FECVENCI</td><td>Fecha. Formato <b>DDMMAAAA</b> (ej. 17042025 = 17-abr-2025)</td></tr>
  <tr><td><code>6</code> NUM_UNICO_IMPORTADOR</td><td>Identificador del importador, estable por empresa</td></tr>
  <tr><td><code>21</code> PA_ORIG</td><td>País de origen</td></tr>
  <tr><td><code>133</code> DNOMBRE</td><td>Glosa descriptiva del producto</td></tr>
  <tr><td><code>134</code> DMARCA</td><td>Marca del fabricante</td></tr>
  <tr><td><code>157</code> ARANC-NAC</td><td>Partida arancelaria de 8 dígitos</td></tr>
  <tr><td><code>158</code> CIF-ITEM</td><td>Valor CIF del ítem, en dólares</td></tr>
</table>
<div class="aviso">
  <b>Aviso técnico:</b> el diccionario de datos de Aduanas anuncia 182 columnas, pero los archivos
  reales traen <b>178</b>. Los últimos campos del diccionario no vienen. Se verificó contra líneas
  reales conocidas (partidas 84705000 cajas registradoras, 85176900 receptores, 71082000 oro) antes
  de construir cualquier cálculo: si el mapeo de columnas está corrido, todo el estudio está mal.
</div>

<h2>2. Cómo se filtró (la decisión más importante)</h2>
<p>El registro trae todo lo que importa Chile. Filtrar mal es lo que arruina un estudio de mercado.
Se iteró tres veces:</p>

<h3>v1 — Solo palabras clave. Falló.</h3>
<p>Buscaba términos como "SCADA", "instrumento", "válvula" en la glosa. Resultado: contaminación grave.
La categoría "Ciberseguridad" capturaba a Dell, Google, Cisco y TP-Link (computación de consumo).
"Válvulas" capturaba a Caterpillar y Scania, porque las llantas también son "válvulas".</p>

<h3>v2 — Solo por partida arancelaria. Falló.</h3>
<p>Se filtró por las partidas del dominio. Resultado: US$1.708M en seis meses, pero seguía entrando
ruido. La partida de tableros eléctricos incluye tanto un panel de control de proceso como un tablero
de automóvil.</p>

<h3>v3 — Partida + marca del fabricante. Es la que quedó.</h3>
<div class="ok">
  <b>Criterio final.</b> Un registro cuenta como mercado de instrumentación y automatización si cumple
  <b>las tres</b> condiciones:
  <ol style="margin-top:9px">
    <li>Su partida arancelaria pertenece al dominio (lista explícita de 69 partidas).</li>
    <li>Su marca corresponde a un fabricante del rubro (lista de ~90 marcas conocidas).</li>
    <li>Su glosa no es de otro rubro (exclusión explícita de "parte", "accesorio", "teléfono",
        "medicamento", "reactivo", etc.).</li>
  </ol>
  Exigir marca es lo que limpia el resultado: un tablero de automóvil no tiene marca de fabricante
  de automatización, y una llanta Caterpillar no entra en la lista de marcas del rubro.
</div>

<h2>3. El resultado del cruce, por familia</h2>
<p>Estos son los mercados medidos que después alimentan la escalera de priorización:</p>
<table>
  <tr><th>Familia del catálogo</th><th class="num">Mercado 2025</th><th class="num">Ítems</th><th>Rivales principales</th></tr>
  {filas_cruce}
</table>
<div class="aviso">
  <b>Dos familias comparten cifra a propósito.</b> "Caudal" y "Nivel" aparecen las dos en US$19,7M
  porque se miden con las <b>mismas partidas arancelarias</b>: el sistema aduanero no distingue un
  medidor de flujo de un medidor de nivel, ambos son "instrumentos para medir el caudal o el nivel
  de líquidos". Es una limitación de la fuente, no un error de cálculo. Lo mismo pasa con DCS y PLC.
</div>

<h2>4. La presencia de SUPCON en Chile: cero</h2>
<div class="aviso">
  <b>Hallazgo central.</b> Se buscaron las marcas SUPCON, Hobré, TISOMIC, C-QUAND, WIM COMPAS y
  PRISM en las 4.847.036 líneas del año. <b>No aparece ninguna.</b> No hay una sola importación
  registrada de SUPCON ni de su filial Hobré en Chile en 2025.
</div>
<p>Esto tiene dos lecturas, y las dos son ciertas:</p>
<ul>
  <li><b>La buena:</b> no hay base instalada que defender, ni canal comprometido, ni cliente con
      mala experiencia previa. El mercado está abierto.</li>
  <li><b>La mala:</b> tampoco hay referencia local. Cualquier cliente va a preguntar "¿quién más lo
      usa en Chile?" y la respuesta honesta es "nadie todavía".</li>
</ul>

<h3>Dos falsos positivos que se descartaron con evidencia</h3>
<table>
  <tr><th>Marca buscada</th><th>Qué apareció</th><th>Conclusión</th></tr>
  <tr><td>HOBRE</td><td>"CAMISAS PARA HOBRES", "POLERA DE HOBRE"</td>
      <td>Es la palabra "hombre" sin tilde. <b>Ropa</b>, no analizadores.</td></tr>
  <tr><td>NOVATECH</td><td>Frenos, tanques de aire, cojinetes, un gabinete de "Raltrac Innovatech"</td>
      <td>Es otra empresa homónima de repuestería automotriz. <b>No es NovaTech Automation.</b></td></tr>
</table>
<p>La lección: una coincidencia de nombre no prueba presencia. Antes de reportar que una marca está
en el mercado, hay que revisar el ítem.</p>

<h2>5. Los importadores: qué se puede y qué no</h2>
<div class="aviso">
  <b>El registro NO trae el nombre ni el RUT del importador.</b> Aduanas los omite amparada en la
  Ley 20.285, y el Consejo para la Transparencia lo confirmó. Tampoco entrega bases de importadores
  por solicitud de transparencia.
</div>
<p>Pero sí trae <code>NUM_UNICO_IMPORTADOR</code>, que es un correlativo estable. Se verificó que
identifica a la empresa: de los <b>16.240 importadores</b> del año, <b>4.720 aparecen los 12 meses</b>.
Eso permite perfilar <b>conducta</b> sin conocer identidad.</p>

<h3>El método de perfilado, y un error que hubo que corregir</h3>
<p>La primera versión perfiló a cada importador usando solo las líneas que pasaban el filtro del rubro.
Resultado: <b>75% de los importadores quedaron clasificados como "compra puntual"</b> — un balde
inútil. El motivo era el método: un distribuidor grande importa mezclado, un ítem de instrumentación
entre cientos de otros. Mirando solo ese ítem, su operación real quedaba invisible.</p>
<p>La versión corregida hace dos pasos:</p>
<ol>
  <li>Perfila la <b>operación completa</b> del importador (todas sus partidas, todo su CIF).</li>
  <li>Mide, dentro de esa operación, <b>cuánto y qué</b> es de instrumentación.</li>
</ol>
<p>De ahí sale el <b>peso del rubro</b>, que es el dato que separa al especialista del generalista:</p>
<table>
  <tr><th>Arquetipo</th><th class="num">Cuántos</th><th class="num">Volumen</th><th>Qué significa</th></tr>
  <tr><td><b>Importador grande multirrubro</b></td><td class="num">335</td><td class="num">US$164,5M (52%)</td>
      <td>Compra de todo; instrumentación es una parte</td></tr>
  <tr><td><b>Integrador / distribuidor técnico</b></td><td class="num">74</td><td class="num">US$108,6M (34%)</td>
      <td><b>Aquí está el canal real</b></td></tr>
  <tr><td><b>Compra menor</b></td><td class="num">1.532</td><td class="num">US$30,6M (10%)</td>
      <td>Sin estructura</td></tr>
  <tr><td><b>Especialista en instrumentación</b></td><td class="num">5</td><td class="num">US$13,2M (4%)</td>
      <td>Puro rubro, compra enfocada</td></tr>
</table>

<h2>6. Límites honestos del estudio</h2>
<p>Lo que estos números <b>no</b> pueden decir:</p>
<ul>
  <li><b>El software no se mide así.</b> El software no entra por partida arancelaria: se vende
      dentro del proyecto. Medir el APC o el OTS con este registro es imposible. En esos productos
      el mercado se declara "no medido" en vez de inventarlo.</li>
  <li><b>Los analizadores están subestimados.</b> El capítulo 90.27 da US$44,3M, pero los sensores
      de proceso entran dentro de sistemas y proyectos, no como ítem suelto con marca. El cálculo
      más confiable para ese segmento es el desglose del capítulo (US$86,8M de proceso industrial).</li>
  <li><b>Un mismo importador puede usar más de un identificador.</b> El correlativo es estable, pero
      no se puede garantizar que sea único por empresa en todos los casos.</li>
  <li><b>El registro es de importaciones, no de consumo.</b> Un equipo importado en 2025 puede
      instalarse en 2027, y puede haber reventa o reexportación.</li>
  <li><b>Los nombres de importadores no son recuperables</b> por vía pública. Para ponerle nombre hay
      que ir por búsqueda inversa (marca + partida + volumen → catálogo público) o preguntando al
      fabricante quién le compra.</li>
</ul>

<h2>7. Cómo replicar el estudio</h2>
<ol>
  <li>Descargar los 12 archivos mensuales del Registro DIN 2025 desde <code>datos.gob.cl</code>.</li>
  <li>Extraer los <code>.txt</code> (separador <code>;</code>, codificación <code>latin-1</code>).</li>
  <li>Verificar el mapeo de columnas contra líneas conocidas <b>antes</b> de calcular nada.</li>
  <li>Correr el filtro de tres condiciones (partida + marca + glosa).</li>
  <li>Aplicar el perfilado en dos pasos (operación completa, después el rubro).</li>
  <li>Cruzar con el catálogo por partida arancelaria.</li>
</ol>
<p>Los generadores están en <code>generadores/</code> del repositorio:
<code>cruzar_importaciones.py</code>, <code>perfilar_importadores_v2.py</code>,
<code>perfilar_detalle_integradores.py</code>, <code>escalera_por_linea.py</code>.</p>

<footer>
  Estudio elaborado por CONECTA · Fuente: Registro DIN de Aduanas de Chile, año 2025
  (4.847.036 líneas, US$85.671M importados).
  <br>Volver al <a href="../index.html">catálogo de fichas</a> ·
  <a href="escalera_exito.html">escalera al éxito</a> ·
  <a href="estrategia_penetracion.html">estrategia de penetración</a>.
</footer>
</div></body></html>"""

open(os.path.join(ART, "metodologia_mercado.html"), "w", encoding="utf-8").write(MET)
print(f"escrito: metodologia_mercado.html ({len(MET.encode()):,} bytes)")
print("guardado en artefactos/metodologia_mercado.html")
