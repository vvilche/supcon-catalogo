#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/buscador_decisores.html — el resultado del buscador multi-fuente.

Muestra las 3 capas de búsqueda, su alcance MEDIDO, y los decisores hallados por empresa con
su cargo, fuente auditable y, donde existe, el LinkedIn.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "buscador_decisores.html")

d = json.load(open(os.path.join(D, "buscador_decisores.json"), encoding="utf-8"))
R = d["resultados"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


con = [x for x in R if x["n_decisores"]]
sin = [x for x in R if not x["n_decisores"]]
tot = sum(x["n_decisores"] for x in R)
tot_rel = sum(x["n_relevantes"] for x in R)
con_li = sum(1 for x in R for h in x["hallazgos"] if h.get("linkedin"))
# fuentes usadas: contar
fuentes = collections.Counter()
for x in R:
    for f in x["fuentes_usadas"]:
        fuentes[f.split(":")[0].split("(")[0].strip()] += 1

orden = sorted(con, key=lambda x: -x["n_decisores"])
filas = ""
for x in orden:
    hs = ""
    for h in x["hallazgos"][:14]:
        mark = "★" if h.get("relevante") else "·"
        li = (f'<a href="{esc(h["linkedin"])}" target="_blank">in</a>'
              if h.get("linkedin") else "")
        col = "#047857" if h.get("relevante") else "#9ca3af"
        hs += (f'<div class="p"><span class="mk" style="color:{col}">{mark}</span>'
               f'<b>{esc(h["nombre"])}</b> <span class="cg">{esc(h["cargo"])[:62]}</span> {li}</div>')
    if len(x["hallazgos"]) > 14:
        hs += f'<div class="p mas">+{len(x["hallazgos"])-14} más</div>'
    filas += f'''
    <tr>
      <td><b>{esc(x["empresa"])}</b><span class="sub">{esc(", ".join(x["fuentes_usadas"]))[:80]}</span></td>
      <td class="num">{x["n_decisores"]}</td>
      <td class="num">{x["n_relevantes"]}</td>
      <td>{hs}</td>
    </tr>'''

sin_html = "".join(f'<span class="chip">{esc(x["empresa"])}</span>' for x in sin) or \
    "<span class='sub'>ninguna</span>"

fuentes_html = ""
for f, n in fuentes.most_common():
    fuentes_html += (f'<div class="bar"><span class="lb">{esc(f)}</span>'
                     f'<div class="tr"><div class="fl" style="width:{n/max(fuentes.values())*100:.0f}%"></div></div>'
                     f'<span class="vl">{n}</span></div>')

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buscador de decisores · resultado</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:960px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#f0fdf4;border:1px solid #bbf7d0;border-left:4px solid #047857;border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#065f46}}
.aviso.am{{background:#fffbeb;border-color:#fde68a;border-left-color:var(--am)}}
.aviso.am b{{color:#92400e}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.p{{font-size:12.5px;padding:2px 0;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}}
.p .mk{{font-weight:700;flex-shrink:0}}
.p .cg{{color:#4b5563;font-size:12px}}
.mas{{color:var(--mu);font-style:italic}}
.sub{{display:block;font-size:11px;color:var(--mu);margin-top:1px}}
.chip{{display:inline-block;font-size:12px;background:#f3f4f6;color:#374151;border-radius:5px;padding:3px 9px;margin:0 4px 4px 0}}
.bar{{display:flex;align-items:center;gap:10px;margin-bottom:7px;font-size:13px}}
.lb{{width:230px;flex-shrink:0;color:#374151}}
.tr{{flex:1;height:9px;background:#f1f5f9;border-radius:5px;overflow:hidden}}
.fl{{height:100%;background:linear-gradient(90deg,#1d4ed8,#60a5fa);border-radius:5px}}
.vl{{width:46px;text-align:right;font-variant-numeric:tabular-nums;color:var(--mu);font-size:12px}}
a{{color:var(--ac);text-decoration:none}} a:hover{{text-decoration:underline}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Buscador de decisores: resultado y cobertura</h1>
<p class="sub0">Un buscador que, dado el nombre de una empresa, encuentra a sus decisores en
<b>todas las fuentes que rinden</b>. Cada fuente candidata se probó contra un caso conocido antes
de entrar. <b>★</b> = cargo relevante para la compra (mantenimiento, I&C, medio ambiente,
operaciones, supply chain, gerencias).</p>

<div class="kpis">
  <div><b>{len(con)}</b>de {len(R)} empresas con decisores</div>
  <div><b>{tot}</b>decisores hallados</div>
  <div><b>{tot_rel}</b>relevantes para compra</div>
  <div><b>{con_li}</b>con LinkedIn</div>
</div>

<div class="aviso">
  <b>Arquitectura: 3 capas, cada una con su alcance medido.</b>
  <ul>
    <li><b>Direcmin</b> (<code>direcmin.com/&lt;empresa&gt;/ejecutivos</code>): <b>93 mineras</b> de
    Chile, con Cargo + Nombre, una página por empresa y por división. Es la fuente más rica donde
    aplica (MLP 21, Escondida 11, Candelaria 11, Codelco 9 por división).</li>
    <li><b>Transparencia (Ley 20.285)</b>: las empresas del <b>Estado</b> publican por obligación
    sus responsables de la administración con nombre, cargo, profesión y RUT. ENAP 12 y Codelco 12.</li>
    <li><b>LinkedIn vía búsqueda</b>: universal — es la que cubre los rubros <b>sin directorio</b>
    (acuicultura, celulosa, química, termoeléctricas). Trae el <b>headline real</b> escrito por la
    propia persona ("Jefe de mantenimiento en Salmones Camanchaca"), que sirve de validación.</li>
  </ul>
</div>

<div class="aviso am">
  <b>Fuentes que se probaron y NO rindieron (para no repetir):</b>
  <ul>
    <li><b>Webs corporativas "nuestro equipo"</b>: <b>7 de 8 fallaron</b> — urls que no existen o
    que solo publican el <b>directorio</b> (los directores, no los gerentes). No sirven para vender.</li>
    <li><b>Gremios</b> (SalmonChile, Generadoras de Chile): listan el directorio <b>del gremio</b>,
    no los gerentes de cada empresa socia.</li>
    <li><b>CMF</b>: el registro de "Presidentes, Directores, Gerentes, Ejecutivos Principales"
    existe, pero el sitio bloquea el acceso automatizado.</li>
  </ul>
  <b>La lección:</b> no inventar URLs de equipo. Lo que rinde son los <b>directorios sectoriales</b>,
  la <b>transparencia por ley</b> y la <b>búsqueda con validación</b>.
</div>

<h2>Fuentes que aportaron</h2>
<div class="card">{fuentes_html}</div>

<h2>Decisores por empresa</h2>
<div class="card">
  <table><thead><tr>
    <th>Empresa</th><th class="num">Total</th><th class="num">Relevantes</th><th>Personas</th>
  </tr></thead><tbody>{filas}</tbody></table>
</div>

<h2>Empresas sin decisores ({len(sin)})</h2>
<div class="card">
  {sin_html}
  <p class="sub" style="margin-top:10px">Estas son las que ninguna capa cubre: sin directorio
  sectorial, sin obligación de transparencia y sin perfil localizable. Se declaran: no se inventa.</p>
</div>

<h2>Qué no dice este resultado</h2>
<div class="card">
  <ul>
    <li><b>El cargo viene de la fuente, no está verificado hoy.</b> En las tres capas el cargo es
    al momento del registro (Direcmin, tabla de transparencia) o al del perfil de LinkedIn.</li>
    <li><b>La capa LinkedIn exige que el headline nombre la empresa</b> para aceptar el hallazgo:
    eso descarta homónimos, pero también deja fuera a quien no puso su empleador en el perfil.</li>
    <li><b>Direcmin da el nivel gerencial, no la jefatura de planta.</b> El que firma la compra
    técnica suele estar una capa más abajo y no aparece en ninguna fuente pública.</li>
    <li><b>No todos los decisores son compradores.</b> Por eso se marca "relevante" por cargo:
    Recursos Humanos o Asuntos Públicos aparecen listados pero no compran instrumentación.</li>
  </ul>
</div>

<footer>
  Motor: <code>generadores/buscador_decisores.py</code> ·
  <a href="bpo_decisores.html">decisores de las BPO</a> ·
  <a href="compradores_linkedin.html">compradores del eCRM</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(con)}/{len(R)} empresas | {tot} decisores | {tot_rel} relevantes | {con_li} con LinkedIn")
