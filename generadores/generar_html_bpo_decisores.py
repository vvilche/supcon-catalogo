#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/bpo_decisores.html — toma de decisiones de las empresas BPO de abastecimiento.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "bpo_decisores.html")

d = json.load(open(os.path.join(D, "bpo_decisores.json"), encoding="utf-8"))
DEC, SD, T = d["decisores"], d["sin_decisor_publicado"], d["totales"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


por_emp = collections.OrderedDict()
for x in DEC:
    por_emp.setdefault(x["empresa"], []).append(x)
# ordenar empresas por cantidad de decisores con cargo
orden = sorted(por_emp.items(), key=lambda kv: -sum(1 for x in kv[1] if not x["cargo"].startswith("no declarado")))

bloques = ""
for emp, ds in orden:
    con_cargo = sum(1 for x in ds if not x["cargo"].startswith("no declarado"))
    con_li = sum(1 for x in ds if x["linkedin"])
    filas = ""
    for x in ds:
        sin_cargo = x["cargo"].startswith("no declarado")
        col = "#9ca3af" if sin_cargo else "#047857"
        et = "s/cargo" if sin_cargo else "DECISOR"
        li = (f'<a href="{esc(x["linkedin"])}" target="_blank">perfil</a>'
              if x["linkedin"] else '<span class="gris">no hallado</span>')
        det = f'<span class="sub">{esc(x.get("detalle",""))}</span>' if x.get("detalle") else ""
        filas += f'''
        <tr>
          <td><b>{esc(x['nombre'])}</b>{det}</td>
          <td>{esc(x['cargo'])}</td>
          <td class="sub2">{esc(x['area'])}</td>
          <td>{li}</td>
          <td><span class="badge" style="background:{col}14;color:{col};border:1px solid {col}3d">{et}</span></td>
        </tr>'''
    bloques += f'''
    <div class="card">
      <h2 style="margin-top:0">{esc(emp)} <span class="cnt">{len(ds)} personas · {con_cargo} con cargo · {con_li} con LinkedIn</span></h2>
      <table><thead><tr><th>Persona</th><th>Cargo</th><th>Área</th><th>LinkedIn</th><th>Tipo</th></tr></thead>
      <tbody>{filas}</tbody></table>
    </div>'''

sd_html = ""
for k, v in SD.items():
    sd_html += f'<tr><td><b>{esc(k)}</b></td><td class="sub2">{esc(v)}</td></tr>'

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Toma de decisiones · BPO de abastecimiento</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1180px;margin:0 auto}}
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
h2{{font-size:18px;font-weight:660;margin:0 0 10px;letter-spacing:-.2px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}}
.cnt{{font-size:11.5px;color:var(--mu);font-weight:400}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.sub{{display:block;font-size:11.5px;color:var(--mu);margin-top:2px}}
.sub2{{font-size:12.5px;color:#4b5563}}
.gris{{color:var(--mu);font-style:italic}}
.badge{{font-size:10.5px;border-radius:5px;padding:2px 8px;font-weight:700;white-space:nowrap}}
a{{color:var(--ac);text-decoration:none}} a:hover{{text-decoration:underline}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Toma de decisiones de las empresas BPO de abastecimiento</h1>
<p class="sub0">Las personas que deciden en las <b>10 empresas que operan el proceso de compras
de la minería</b> (el modelo SupplyNet). Cargo tomado de la fuente donde se declara, no inferido.
Sirve para saber con quién hablar si el objetivo es entrar por el canal de abastecimiento.</p>

<div class="kpis">
  <div><b>{T['decisores']}</b>personas identificadas</div>
  <div><b>{T['empresas_con_decisor']}</b>de 10 empresas con equipo publicado</div>
  <div><b>{T['con_linkedin']}</b>con LinkedIn</div>
  <div><b>{T['empresas_sin_decisor_publicado']}</b>empresas sin equipo publicado</div>
</div>

<div class="aviso am">
  <b>Lo primero, porque cambia el uso:</b> estas empresas son <b>chicas y no publican su
  organigrama</b>. Solo 5 de las 10 tienen equipo legible en su sitio. Las otras 5
  ({', '.join(SD.keys())}) no publican quién decide: se declara, no se inventa.
  <br><br>
  <b>Y el cargo es al momento de la fuente.</b> En empresas de este tamaño la gente se mueve rápido
  y las webs quedan viejas: el cargo hay que confirmarlo antes de usarlo en una propuesta.
</div>

<div class="aviso">
  <b>El dato más útil de toda la extracción:</b> <b>Mauricio Herrera (Socio Director de Adelanta)
  lideró abastecimiento en Collahuasi y Yamana Gold</b>, y <b>Cristian Núñez (Director de
  Abastecimiento) estuvo en Kinross y Nueva Unión</b>. SupplyNet tiene una <b>Gerente Cuenta Anglo
  American</b> dedicada. Es decir: estos decisores <b>son ex compradores de las mismas mineras
  donde hay que vender</b>. Conocen el proceso desde adentro.
</div>

{bloques}

<h2 style="margin:28px 0 10px">Empresas sin equipo publicado</h2>
<div class="card">
  <table><thead><tr><th>Empresa</th><th>Por qué no aparece</th></tr></thead><tbody>{sd_html}</tbody></table>
</div>

<h2 style="margin:28px 0 10px">Qué no dice esta lista</h2>
<div class="card">
  <ul>
    <li><b>No es un organigrama.</b> Es lo que cada empresa publica. SupplyNet declara 211
    empleados, pero su org chart público solo muestra 5 cargos de gerencia.</li>
    <li><b>El cargo se marca como "s/cargo" cuando la fuente lista el nombre sin decirlo</b>
    (varios del equipo de Adelanta y CAS aparecen así). No se deduce del parecido del nombre.</li>
    <li><b>Homónimos descartados a propósito:</b> buscando "Ide" en IDE Consulting aparecieron
    perfiles en minería y alimentos que no corresponden; lo mismo con "Sgai". No se listaron.</li>
    <li><b>El rol real de compra en estas empresas es el "Category Manager" y el "BPO de
    abastecimiento"</b> (SupplyNet tiene 108 personas en Procurement and Contracts). Ahí decide
    la compra de insumos: esa capa no está publicada por nadie.</li>
  </ul>
</div>

<footer>
  Fuentes: sitios oficiales de cada empresa (casgroup.cl, adelanta.cl, andeanbpo.com,
  metaprojectgroup.com, mimsprojects.com) + theorg.com/org/supplynet-cl + nuevamineria.com ·
  <a href="bpo_abastecimiento.html">las 10 empresas BPO</a> ·
  <a href="compradores_linkedin.html">compradores del eCRM</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(orden)} empresas | {len(DEC)} personas | {T['con_linkedin']} con LinkedIn")
