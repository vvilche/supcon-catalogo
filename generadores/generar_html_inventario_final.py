#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/inventario_final.html con las 617 empresas por industria y sus decisores."""
import json, os, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "inventario_final.html")

inv = json.load(open(os.path.join(D, "inventario_final.json"), encoding="utf-8"))
camp = json.load(open(os.path.join(D, "campana_process.json"), encoding="utf-8"))


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v):
    try:
        return f"{v:,}"
    except Exception:
        return "—"


tot = inv["totales"]
pr = inv["por_rubro"]
emp = inv["empresas"]
max_d = max(x["decisores"] for x in pr)

# tabla por rubro
filas = "".join(f'''
  <tr>
    <td><b>{esc(x['rubro'])}</b></td>
    <td class="num">{n(x['empresas'])}</td>
    <td class="num">{n(x['decisores'])}</td>
    <td class="bar"><span style="width:{x['decisores']/max_d*100:.0f}%"></span></td>
  </tr>''' for x in pr)

# top empresas con sus decisores (los que más tienen)
top = sorted([e for e in emp if e["n_decisores"] > 0], key=lambda x: -x["n_decisores"])[:60]
filas_top = ""
for e in top:
    personas = e["personas"][:3]
    pp = "".join(f'<div class="p"><b>{esc(p["nombre"][:30])}</b> <span>{esc(p["cargo"][:52])}</span></div>'
                 for p in personas)
    mas = f'<div class="mas">+{e["n_decisores"]-3} más</div>' if e["n_decisores"] > 3 else ""
    filas_top += f'''
    <div class="emp">
      <div class="eh"><b>{esc(e["nombres"][0])}</b>
        <span class="rb">{esc(e["rubro"])}</span>
        <span class="nd">{e["n_decisores"]} decisores</span></div>
      {pp}{mas}
    </div>'''

# embudo de cobertura
embudo = [
    ("Universo RETC (padrón)", 3157, "todas las empresas industriales con declaración ambiental"),
    ("GRANDES + MEDIANAS", 579, "las vendibles: 286 grandes y 293 medianas"),
    ("Con decisores mapeados", tot["empresas_unicas"], "el resultado de este trabajo"),
]

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Inventario final: {n(tot["empresas_unicas"])} empresas por industria</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1200px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:960px}}
h2{{font-size:19px;font-weight:660;margin:28px 0 11px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:18px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 16px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:22px;font-weight:700;color:var(--tx)}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 19px;margin-bottom:13px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px;border-bottom:2px solid var(--bd)}}
td{{padding:7px 8px;border-bottom:1px solid #f3f4f6}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}}
.bar{{width:150px;padding:0 10px}}
.bar span{{display:block;height:8px;border-radius:4px;background:#3b82f6}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:10px}}
.emp{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 14px}}
.eh{{margin-bottom:6px;padding-bottom:5px;border-bottom:1px solid #f3f4f6}}
.eh b{{font-size:13.5px;display:block}}
.rb{{font-size:11px;color:var(--mu);display:block}}
.nd{{font-size:11.5px;font-weight:700;color:var(--vd)}}
.p{{font-size:12px;margin-bottom:2px}}
.p b{{font-weight:600}}
.p span{{color:var(--mu);font-size:11.5px}}
.mas{{font-size:11px;color:var(--mu);font-style:italic;margin-top:3px}}
.embudo{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}}
.eb{{background:var(--cd);border:1px solid var(--bd);border-left:4px solid var(--ac);border-radius:10px;padding:11px 16px;flex:1;min-width:200px}}
.eb b{{display:block;font-size:11.5px;color:var(--mu)}} .eb .v{{font-size:22px;font-weight:700}}
.eb .d{{font-size:11.5px;color:var(--mu)}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:12px 16px;margin:14px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
.aviso.vd{{background:#f0fdf4;border-color:#bbf7d0;border-left-color:#047857}}
.aviso.vd b{{color:#065f46}}
footer{{margin-top:28px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Inventario final: {n(tot["empresas_unicas"])} empresas con decisores, por industria</h1>
<p class="sub0">El universo de prospección clasificado por rubro, con los decisores <b>auditados</b>
(sólo los que pertenecen de verdad a la empresa y tienen cargo de decisión).</p>

<div class="kpis">
  <div><b>{n(tot["empresas_unicas"])}</b>empresas con decisores</div>
  <div><b>{n(tot["decisores"])}</b>decisores</div>
  <div><b>{n(len(pr))}</b>industrias</div>
  <div><b>{n(sum(1 for e in emp if e["tier"]=="GRANDE"))}</b>grandes</div>
</div>

<h2>El embudo de cobertura</h2>
<div class="embudo">
  <div class="eb"><b>Universo RETC</b><span class="v">{n(3157)}</span>
    <span class="d">el padrón completo</span></div>
  <div class="eb"><b>Vendibles (grandes+medianas)</b><span class="v">579</span>
    <span class="d">el target con tamaño</span></div>
  <div class="eb"><b>Con decisores</b><span class="v">{n(tot["empresas_unicas"])}</span>
    <span class="d">nombre y cargo mapeados</span></div>
</div>

<div class="aviso">
  <b>De dónde salen los {n(tot["decisores"])} decisores:</b> se barrieron las 356 empresas que
  faltaban en 3 fuentes y se auditó uno por uno. <b>De 1.226 hallazgos brutos, 445 (36%) eran de
  otras empresas</b> y se descartaron. Casos medidos:
  <ul style="margin:7px 0 0 19px">
    <li><b>Direcmin contaminado:</b> "CMPC Tissue", "CMPC Celulosa" e "Inversiones del Pacífico"
    recibieron los MISMOS ejecutivos de <i>Compañía Minera del Pacífico</i> (otra empresa).</li>
    <li><b>LinkedIn con homónimos:</b> razones sociales que son un apellido ("CONTRERAS",
    "GOMEZ", "FERNANDEZ") devolvieron el headline de cualquier persona con ese apellido.</li>
  </ul>
</div>

<h2>Por tipo de industria</h2>
<div class="card">
  <table><thead><tr><th>Industria</th><th class="num">Empresas</th><th class="num">Decisores</th><th></th></tr></thead>
  <tbody>{filas}
  <tr style="border-top:2px solid var(--bd)"><td><b>TOTAL</b></td>
  <td class="num"><b>{n(tot["empresas_unicas"])}</b></td>
  <td class="num"><b>{n(tot["decisores"])}</b></td><td></td></tr></tbody></table>
</div>

<h2>Las {len(top)} empresas con más decisores</h2>
<div class="grid">{filas_top}</div>

<footer>
  Fuentes: <code>universo_prospeccion_supcon.json</code> (3.157 del RETC) ·
  <code>buscador_decisores.json</code> · <code>barrido_universo_auditado.json</code>.
  Auditoría: <code>generadores/auditar_universo.py</code>.
  <a href="inventario_universo.html">inventario por industria y formato del Excel</a> ·
  <a href="campana_process.html">la campaña Process</a> · <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {tot['empresas_unicas']} empresas | {tot['decisores']} decisores | {len(pr)} rubros | grid top {len(top)}")
