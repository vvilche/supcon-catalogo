#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera estudio-mercado/valvulas_2025.html — análisis de mercado de válvulas en Chile 2025.

Lee datos/mercado_valvulas_2025.json (lo produce analizar_valvulas.py, sobre el registro
crudo de Aduanas).

INCLUYE UNA CORRECCIÓN IMPORTANTE: el cruce general había medido válvulas en US$53,8M. Ese
número era el valor de las importaciones QUE DECLARAN MARCA de fabricante del rubro, no el
mercado. En válvulas, el 88% del valor no declara marca reconocible (se importa como
"válvula" sin marca o con marcas genéricas). El capítulo 84.81 completo es US$454,9M.
El documento presenta las dos cifras y explica cuál sirve para qué.
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "estudio-mercado", "valvulas_2025.html")

d = json.load(open(os.path.join(D, "mercado_valvulas_2025.json"), encoding="utf-8"))

PAIS = {"225":"Francia","336":"Alemania","512":"Italia","504":"EE.UU.","563":"China",
 "317":"Corea del Sur","517":"Singapur","507":"Japón","331":"Brasil","528":"Países Bajos",
 "511":"Canadá","510":"Taiwán","220":"España","226":"Reino Unido","549":"India","216":"Noruega",
 "505":"EE.UU.","528":"Países Bajos"}

def usd(v):
    return f"US${v/1e6:,.1f}M" if v >= 1e6 else f"US${v/1e3:,.0f}K"

# tipos: solo los del dominio de control de proceso
ORDEN = ["Válvulas de bola","Los demás artículos de grifería","Partes de válvulas",
 "Válvulas para transmisión oleohidráulica","Válvulas reductoras de presión",
 "Válvulas de seguridad o alivio","Válvulas de retención (check)",
 "Válvulas para transmisión neumática"]
tot = d["total_usd"]
maxv = max(v["usd"] for v in d["por_tipo"].values())

filas_tipo = ""
for t in ORDEN:
    if t not in d["por_tipo"]: continue
    v = d["por_tipo"][t]
    pct = v["usd"]/tot*100
    ancho = v["usd"]/maxv*100
    top = ", ".join(f"{m} ({usd(x)})" for m, x in v["marcas"][:3]) or "sin marca declarada"
    filas_tipo += f'''
    <div class="tipo">
      <div class="th"><span class="tn">{t}</span><span class="tv">{usd(v["usd"])}</span></div>
      <div class="bar"><div class="fill" style="width:{ancho:.0f}%"></div></div>
      <div class="tm">{v["items"]:,} ítems · {pct:.1f}% del capítulo · marcas principales: {top}</div>
    </div>'''

filas_marca = ""
for m, v in d["por_marca"][:20]:
    filas_marca += (f'<tr><td><b>{m}</b></td><td class="num">{usd(v)}</td>'
                    f'<td class="num">{v/55797086*100:.1f}%</td></tr>')

filas_pais = ""
for p, v in d["por_pais"][:8]:
    filas_pais += (f'<tr><td>{PAIS.get(p, "cód. "+p)}</td><td class="num">{usd(v)}</td>'
                   f'<td class="num">{v/tot*100:.1f}%</td></tr>')

con_marca = d["total_usd"] - d["sin_marca_usd"]

HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mercado de válvulas — Chile 2025</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706;--ams:#fffbeb}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:1000px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:850px}}
h2{{font-size:20px;font-weight:660;margin:36px 0 11px;letter-spacing:-.2px}}
p{{margin-bottom:11px}}
ul{{list-style:none;margin:9px 0 12px}}
ul li{{position:relative;padding-left:17px;margin-bottom:6px}}
ul li:before{{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}}
table{{width:100%;border-collapse:collapse;margin:13px 0;font-size:14px}}
th{{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 10px;border-bottom:1px solid #f1f5f9}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:15px 18px;margin:16px 0;font-size:14px}}
.aviso b{{color:#92400e}}
.correccion{{background:#f1f5f9;border:1px solid #cbd5e1;border-left:4px solid #475569;border-radius:9px;padding:15px 18px;margin:16px 0;font-size:14px}}
.correccion b{{color:#334155}}
.tipo{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:13px 16px;margin-bottom:9px}}
.th{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:7px}}
.tn{{font-weight:640;font-size:14.5px}}
.tv{{font-weight:700;font-size:16px;letter-spacing:-.3px}}
.bar{{height:6px;background:#f1f5f9;border-radius:3px;overflow:hidden;margin-bottom:6px}}
.fill{{height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:3px}}
.tm{{font-size:12px;color:var(--mu)}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Mercado de válvulas en Chile</h1>
<p class="sub">Capítulo arancelario 84.81 completo, año 2025, desde el registro de importaciones de Aduanas.
Con el desglose por tipo de válvula, que es como se habla de válvulas en una planta.</p>

<div class="kpi">
  <div><b>{usd(d["total_usd"])}</b>capítulo 84.81 completo</div>
  <div><b>{d["total_items"]:,}</b>ítems importados</div>
  <div><b>{d["n_importadores"]:,}</b>importadores activos</div>
  <div><b>88%</b>sin marca declarada</div>
</div>

<div class="correccion">
  <b>Corrección de una cifra anterior.</b> El cruce general del catálogo había medido válvulas en
  <b>US${con_marca/1e6:,.1f}M</b>. Ese número es real pero es <b>otra cosa</b>: es el valor de las
  importaciones que declaran una marca de fabricante del rubro. En válvulas, el <b>88% del valor no
  declara marca reconocible</b> — entra como "válvula" a secas o con marcas genéricas sin fabricante
  identificable. El capítulo completo mueve <b>{usd(d["total_usd"])}</b>.
  <br><br>
  <b>Cuál usar para qué.</b> Para dimensionar el mercado: <b>{usd(d["total_usd"])}</b>.
  Para saber contra quién se compite: <b>{usd(con_marca)}</b>, que es donde hay marca con nombre.
  El filtro por marca sirve para medir competencia, no tamaño.
</div>

<h2>El mercado por tipo de válvula</h2>
<p>Esto es lo que el registro permitre separar. Es la vista útil: un cliente no compra "válvulas",
compra una válvula de bola para pulpa o una de seguridad para un estanque.</p>
{filas_tipo}

<div class="aviso">
  <b>Aclaración sobre "los demás artículos de grifería" (US$229,7M).</b> Es la partida residual del
  sistema arancelario: todo lo que no cae en una categoría específica. Ahí conviven válvulas de
  control, de globo, de diafragma y de mariposa con artículos de grifería doméstica. <b>No se puede
  separar con el registro de Aduanas.</b> Es el límite de la fuente, y es importante saberlo antes
  de usar esa cifra.
</div>

<h2>Quién domina el segmento con marca declarada</h2>
<p>Sobre los {usd(con_marca)} que sí declaran fabricante:</p>
<table>
  <tr><th>Marca</th><th class="num">Importado 2025</th><th class="num">% del segmento con marca</th></tr>
  {filas_marca}
</table>
<p><b>Lectura:</b> Valmet, Emerson, Bray y Danfoss concentran la mitad del segmento con marca. Valmet
aparece primero casi enteramente por la partida de válvulas para transmisión neumática (US$4,3M), que
es su negocio de válvulas de control de proceso: es el competidor más directo de lo que ofrece SUPCON FLUID.
Emerson está en segundo lugar por la línea Fisher y por válvulas de cuchilla (hay un ítem explícito de
"cuchillo, series KGD").</p>

<h2>De dónde vienen</h2>
<table>
  <tr><th>Origen</th><th class="num">Valor</th><th class="num">% del capítulo</th></tr>
  {filas_pais}
</table>
<p>Alemania y Francia explican más de la mitad del valor del capítulo. El origen europeo domina
el segmento de válvulas industriales en Chile, que es el mismo patrón que se vio en el canal técnico:
el estándar es europeo, no asiático. <b>China aparece tercero con US$27,9M</b>, y ahí está el espacio
natural para una marca china como SUPCON: el mercado ya acepta producto chino en válvulas, pero
todavía no en instrumentación de proceso crítica.</p>

<h2>La línea de SUPCON frente a este mercado</h2>
<p>SUPCON Fluid Technology fabrica 13 series que cubren cuatro de los tipos medidos:</p>
<table>
  <tr><th>Tipo del mercado</th><th class="num">Mercado 2025</th><th>Serie SUPCON que compite</th></tr>
  <tr><td>Válvulas de bola</td><td class="num">US$56,7M</td>
      <td>SN O-type (bola flotante y trunnion) y VN V-type (bola V con corte de fibras)</td></tr>
  <tr><td>"Los demás artículos de grifería"</td><td class="num">US$229,7M</td>
      <td>LN y LM de vástago deslizante, mariposa BN y excéntrica CN</td></tr>
  <tr><td>Válvulas de seguridad o alivio</td><td class="num">US$20,4M</td>
      <td>No cubierto directamente: SUPCON no fabrica válvulas de alivio</td></tr>
  <tr><td>Válvulas reductoras de presión</td><td class="num">US$21,3M</td>
      <td>Parcial: los posicionadores CVP2000 sí participan del control de presión</td></tr>
</table>
<p><b>Lo que la línea cubre y lo que no:</b> SUPCON Fluid fabrica válvulas de CONTROL (vástago
deslizante, bola, mariposa, excéntrica) y especiales (alimentación, cuchilla, compuerta). <b>No
fabrica válvulas de alivio ni de seguridad</b>, que son US$20,4M del mercado y suelen venderse con
marca especializada (Consolidated, Anderson Greenwood, Farris). Si un cliente pide una válvula de
alivio, no hay oferta SUPCON: hay que decirlo, no improvisar.</p>

<h2>Qué significa para la estrategia</h2>
<ul>
  <li><b>El mercado es grande (US$454,9M) pero está fragmentado.</b> El 88% sin marca indica un
      mercado donde el importador compra por especificación técnica, no por marca. Eso es una
      oportunidad para una marca nueva: el cliente no está casado con un nombre.</li>
  <li><b>Pero la especificación la escribe el proyectista, y ahí manda Valmet y Emerson.</b> Entrar
      requiere estar en las bases técnicas del proyecto, no en la compra.</li>
  <li><b>El nicho donde SUPCON tiene algo que otros no tienen es la serie VN.</b> Rangeability 300:1
      con acción de corte de fibras: pulpa, papel, relaves y lodos. Es un argumento técnico
      específico, no una competencia por precio.</li>
  <li><b>Y el mercado acepta origen chino en válvulas.</b> China ya importa US$27,9M en este
      capítulo: la barrera de origen que existe en instrumentación crítica no está en válvulas.</li>
</ul>

<div class="aviso">
  <b>Lo que falta para poder vender válvulas.</b> El brief de válvulas de SUPCON no incluye
  battlecard ni red de servicio local. Es la objeción que hay que resolver con el fabricante
  antes de ofrecer, igual que en el resto de las líneas de hardware.
</div>

<footer>
  Fuente: Registro DIN de importaciones, Servicio Nacional de Aduanas de Chile, año 2025
  (capítulo 84.81, {d["total_items"]:,} ítems filtrados por descripción).
  <br>Ver <a href="analizadores_2025.html">analizadores de proceso</a> ·
  <a href="estudio_mercado_2025.html">estudio general</a> ·
  <a href="../artefactos/metodologia_mercado.html">cómo se calcularon los números</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"tipos: {len(ORDEN)} | marcas: {len(d['por_marca'][:20])} | origenes: {len(filas_pais)}")
