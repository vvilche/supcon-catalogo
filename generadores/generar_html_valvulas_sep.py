#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera estudio-mercado/valvulas_manual_control_2025.html"""
import os, json
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"estudio-mercado","valvulas_manual_control_2025.html")

d=json.load(open(os.path.join(D,"valvulas_manual_vs_control.json"),encoding="utf-8"))
def usd(v): return f"US${v/1e6:,.1f}M"

tot=d["total_usd"]; mx=d["partida_mixta"]
P=d["por_partida"]

filas_part=""
for t,v in P:
    pct=v/tot*100
    filas_part+=f'''<div class="part"><div class="ph2"><span>{t}</span><span class="pv">{usd(v)}</span></div>
      <div class="bar"><div class="fill" style="width:{max(pct,1.5):.1f}%"></div></div>
      <div class="pp">{pct:.1f}% del capítulo</div></div>'''

filas_ctrl="".join(f'<tr><td>{m}</td><td class="num">{usd(v)}</td></tr>' for m,v in d["marcas_control"][:12] if m)
filas_man="".join(f'<tr><td>{m}</td><td class="num">{usd(v)}</td></tr>' for m,v in d["marcas_manual"][:12] if m)

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Válvulas: manuales vs control — Chile 2025</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:980px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:850px}}
h2{{font-size:20px;font-weight:660;margin:34px 0 10px;letter-spacing:-.2px}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:18px 0 9px}}
p{{margin-bottom:11px}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px}}
th{{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--bd)}}
td{{padding:8px 10px;border-bottom:1px solid #f1f5f9}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:15px 18px;margin:15px 0;font-size:14px}}
.aviso b{{color:#92400e}}
.ok{{background:#ecfdf5;border:1px solid #a7f3d0;border-left:4px solid #047857;border-radius:9px;padding:15px 18px;margin:15px 0;font-size:14px}}
.ok b{{color:#047857}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:17px 20px;margin-bottom:14px}}
.part{{margin-bottom:11px}}
.ph2{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:5px;font-size:14px}}
.pv{{font-weight:700;font-size:15px;font-variant-numeric:tabular-nums}}
.bar{{height:6px;background:#f1f5f9;border-radius:3px;overflow:hidden}}
.fill{{height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:3px}}
.pp{{font-size:11.5px;color:var(--mu);margin-top:3px}}
.dos{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:700px){{.dos{{grid-template-columns:1fr}}}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Válvulas: manuales vs de control</h1>
<p class="sub">Capítulo arancelario 84.81, Chile 2025. La separación que se puede hacer con el
registro de Aduanas, y la que no — declarada en vez de repartida a ojo.</p>

<div class="kpi">
  <div><b>{usd(tot)}</b>capítulo completo</div>
  <div><b>{usd(d["piso_control_usd"])}</b>control (piso)</div>
  <div><b>{usd(d["piso_manual_usd"])}</b>manual / corte (piso)</div>
  <div><b>{d["no_clasificable_usd"]/tot*100:.0f}%</b>no clasificable</div>
</div>

<div class="aviso">
  <b>Lo primero es la advertencia.</b> El registro de Aduanas <b>no permite separar válvulas
  manuales de válvulas de control</b>, y conviene saberlo antes de usar cualquier número.
  El <b>50,5%</b> del capítulo (US$230,1M) cae en la partida residual "los demás artículos de
  grifería", donde conviven las tres cosas: válvulas de control modulante, válvulas manuales y
  grifería doméstica. La glosa del ítem suele decir solo <code>VÁLVULA</code>, sin más.
</div>

<h2>Lo que sí se separa: por partida</h2>
<p>Cinco partidas identifican el tipo de válvula por sí solas, sin ambigüedad:</p>
<div class="card">{filas_part}</div>

<h2>La partida mixta: qué se pudo rescatar</h2>
<p>Dentro de los US$230,1M de la partida residual 84818090, se identificó el tipo cruzando la
<b>marca</b> del fabricante con palabras de la glosa:</p>
<table>
  <tr><th>Segmento de la partida mixta</th><th class="num">Valor</th><th class="num">%</th></tr>
  <tr><td>Identificable como <b>válvula de control</b></td><td class="num">{usd(mx["control_identificado"])}</td><td class="num">{mx["control_identificado"]/mx["total"]*100:.0f}%</td></tr>
  <tr><td>Identificable como <b>válvula manual</b></td><td class="num">{usd(mx["manual_identificado"])}</td><td class="num">{mx["manual_identificado"]/mx["total"]*100:.0f}%</td></tr>
  <tr><td><b>No identificable</b></td><td class="num">{usd(mx["no_identificable"])}</td><td class="num">{mx["no_identificable"]/mx["total"]*100:.0f}%</td></tr>
</table>

<h2>El resultado: un piso confiable por categoría</h2>
<div class="ok">
  <b>Regla.</b> Se reporta el <b>piso</b> de cada categoría: solo lo que se puede atribuir con
  evidencia (por partida específica o por marca conocida del tipo). El resto se declara como
  no clasificable. <b>No se reparte el 37% que no se puede identificar</b>: hacerlo sería
  inventar precisión.
</div>
<table>
  <tr><th>Categoría</th><th class="num">Piso medido</th><th>Qué incluye</th></tr>
  <tr><td><b>Válvulas de control</b></td><td class="num">{usd(d["piso_control_usd"])}</td>
      <td>Reductoras de presión (US$21,3M) + las identificadas por marca de control dentro de la partida mixta (US$47,7M)</td></tr>
  <tr><td><b>Válvulas manuales / corte</b></td><td class="num">{usd(d["piso_manual_usd"])}</td>
      <td>Válvulas de bola (US$56,8M) + retención (US$18,2M) + manuales identificadas por marca (US$12,8M)</td></tr>
  <tr><td><b>Seguridad, potencia y partes</b></td><td class="num">US$129,3M</td>
      <td>Alivio y seguridad (US$20,4M) + transmisión hidráulica y neumática (US$35,9M) + partes (US$73,0M)</td></tr>
  <tr><td><b>No clasificable</b></td><td class="num">{usd(d["no_clasificable_usd"])}</td>
      <td>Partida mixta sin marca que identifique el tipo. Requiere otra fuente para separarse.</td></tr>
</table>

<h2>Quién juega en cada cancha</h2>
<div class="dos">
  <div class="card">
    <h3>Marcas de control de proceso</h3>
    <table>{filas_ctrl}</table>
    <p style="font-size:12.5px;color:#64748b;margin-top:8px">Son las que compiten directamente con
    la línea de SUPCON Fluid. Nota: Caterpillar aparece aquí por ítems de la partida mixta con
    glosa de control que en realidad son repuestos de maquinaria de movimiento de tierras —
    es ruido que el método por marca todavía no separa.</p>
  </div>
  <div class="card">
    <h3>Marcas de válvula manual</h3>
    <table>{filas_man}</table>
    <p style="font-size:12.5px;color:#64748b;margin-top:8px">Bray domina con US$6,4M. Aparecen
    varios fabricantes chinos (Taizhou, Yuhuan, Zhejiang, Zhejiang Gute Ke) con volúmenes
    relevantes: <b>el mercado de válvulas manuales ya acepta origen chino</b>, a diferencia
    del de instrumentación de proceso.</p>
  </div>
</div>

<h2>Qué significa para vender válvulas SUPCON</h2>
<ul style="list-style:none">
  <li style="position:relative;padding-left:17px;margin-bottom:7px">
    <b style="color:#2563eb">·</b> <b>El control es el nicho donde SUPCON tiene argumento.</b>
    La línea SUPCON Fluid es de válvulas de control: vástago deslizante, bola V con corte de
    fibras, mariposa y excéntrica. Compite ahí, no en la válvula manual de grifería.</li>
  <li style="position:relative;padding-left:17px;margin-bottom:7px">
    <b style="color:#2563eb">·</b> <b>El piso de control es US$69,0M</b> y está en manos de
    Valmet, Emerson, Metso, Valvitalia, Weir, Dezurik y Flowserve. Es un mercado mediano con
    incumbentes fuertes y sin marca china dominante: hay espacio.</li>
  <li style="position:relative;padding-left:17px;margin-bottom:7px">
    <b style="color:#2563eb">·</b> <b>En cambio la válvula manual ya está tomada por China.</b>
    Taizhou, Yuhuan y Zhejiang suman US$6,4M y Bray US$6,4M. Competir ahí es precio contra
    precio, sin el argumento técnico que da la serie VN.</li>
  <li style="position:relative;padding-left:17px;margin-bottom:7px">
    <b style="color:#2563eb">·</b> <b>Y SUPCON no fabrica válvulas de alivio ni de seguridad</b>
    (US$20,4M del capítulo). Si el cliente las pide, hay que decirlo.</li>
</ul>

<footer>
  Fuente: Registro DIN de importaciones, Servicio Nacional de Aduanas de Chile, año 2025
  (capítulo 84.81, {d["items"]:,} ítems). El piso de cada categoría se obtuvo cruzando la
  partida específica con la marca del fabricante. El valor no clasificable se declara como tal.
  <br>Ver <a href="valvulas_2025.html">el mercado de válvulas completo</a> ·
  <a href="hardware_partidas_2025.html">hardware por partida</a> ·
  <a href="../artefactos/metodologia_mercado.html">metodología</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
