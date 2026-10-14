#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/cliente_producto_persona.html — LA VISTA ÚNICA.

Una sola vista por herramienta (preferencia de Victor): por empresa, todo junto —
cuánto compró, cuánto dolor declaró, qué línea le sirve y quiénes deciden.
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "cliente_producto_persona.html")

d = json.load(open(os.path.join(D, "vista_cliente_producto_persona.json"), encoding="utf-8"))
E, T = d["empresas"], d["totales"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


con_dec = [x for x in E if x["n_decisores"]]
con_compra = [x for x in E if x["usd_cotizado"]]

bloques = ""
for x in E:
    # ordenar decisores: primero los relevantes para compra
    decs = sorted(x["decisores"], key=lambda h: (not h.get("relevante"), h["nombre"]))
    dec_html = ""
    for h in decs[:12]:
        estrella = '<span class="st">★</span>' if h.get("relevante") else '<span class="dt">·</span>'
        li = (f'<a href="{esc(h["linkedin"])}" target="_blank">in</a>'
              if h.get("linkedin") else "")
        dec_html += (f'<div class="p">{estrella}<b>{esc(h["nombre"])}</b> '
                     f'<span class="cg">{esc(h["cargo"])[:64]}</span> {li}</div>')
    if len(decs) > 12:
        dec_html += f'<div class="p mas">+{len(decs)-12} más</div>'

    comp_html = ""
    for c in x["compradores_reales"]:
        li = (f'<a href="{esc(c["linkedin"])}" target="_blank">in</a>'
              if c.get("linkedin") else "")
        comp_html += f'<span class="chip">{esc(c["nombre"])} {li}</span>'

    prod = " · ".join(x["productos"][:5]) if x["productos"] else ""
    lin = " · ".join(x["lineas"]) if x["lineas"] else ""

    monto = (f'<span class="monto">US${n(x["usd_cotizado"])}</span>'
             f'<span class="sub">ganado US${n(x["usd_ganado"])} · {x["n_oc"]} OC</span>'
             if x["usd_cotizado"] else '<span class="gris">nunca cotizado</span>')
    dolor = (f'<span class="dolor">{n(x["respel_t"],1)} t</span>'
             if x["respel_t"] else '<span class="gris">—</span>')

    bloques += f'''
    <div class="card">
      <div class="head">
        <div class="nom"><b>{esc(x["empresa"])}</b>
          {f'<span class="sig">{esc(x["sigla_ecrm"])}</span>' if x["sigla_ecrm"] else ''}</div>
        <div class="met">{monto}</div>
        <div class="met">{dolor}<span class="sub">residuos peligrosos</span></div>
        <div class="met"><span class="num">{x["n_decisores"]}</span><span class="sub">decisores</span></div>
      </div>
      {f'<div class="lin"><span class="lb">Línea</span> {esc(lin)}<span class="prod">{esc(prod)}</span></div>' if lin else ''}
      {f'<div class="dec">{dec_html}</div>' if dec_html else ''}
      {f'<div class="creales"><span class="lb">Ya compraron</span> {comp_html}</div>' if comp_html else ''}
    </div>'''

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cliente · qué comprar · a quién</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1120px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:18px;max-width:940px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:18px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid var(--ac);border-radius:9px;padding:12px 16px;margin:14px 0;font-size:13.5px}}
.aviso b{{color:#1e40af}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:14px 17px;margin-bottom:11px}}
.head{{display:flex;gap:16px;align-items:baseline;flex-wrap:wrap;margin-bottom:7px}}
.nom b{{font-size:15.5px}}
.sig{{font-size:10.5px;background:#eef2ff;color:#3730a3;border-radius:4px;padding:1px 7px;margin-left:6px;font-weight:700}}
.met{{font-size:13px;color:var(--mu);text-align:right}}
.met:first-of-type{{margin-left:auto}}
.monto{{font-weight:700;color:var(--tx)}} .dolor{{font-weight:700;color:#991b1b}}
.num{{font-weight:700;color:var(--tx);font-size:15px}}
.sub{{display:block;font-size:11px;color:var(--mu)}}
.lin{{font-size:13px;margin:6px 0;padding:7px 10px;background:#f0fdf4;border-radius:7px}}
.lb{{font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;margin-right:8px}}
.prod{{color:var(--mu);font-size:12px;margin-left:10px}}
.dec{{margin-top:8px;border-top:1px solid #f3f4f6;padding-top:7px}}
.p{{font-size:12.5px;padding:2px 0;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}}
.p .st{{color:var(--vd);font-weight:700}} .p .dt{{color:#d1d5db}}
.cg{{color:#4b5563;font-size:12px}} .mas{{color:var(--mu);font-style:italic}}
.creales{{margin-top:7px;font-size:12.5px}}
.chip{{display:inline-block;background:#fffbeb;color:#92400e;border:1px solid #fde68a;border-radius:5px;padding:2px 8px;margin:0 4px 3px 0;font-size:12px}}
.gris{{color:var(--mu);font-style:italic}}
a{{color:var(--ac);text-decoration:none}} a:hover{{text-decoration:underline}}
footer{{margin-top:30px;padding-top:15px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Cliente · qué comprar · a quién</h1>
<p class="sub0">Una sola vista por empresa, con los cuatro datos juntos: <b>cuánto compró</b>
(eCRM 2023-2025), <b>cuánto dolor declaró</b> (RETC), <b>qué línea SUPCON le sirve</b> (matriz
dolor × producto) y <b>quiénes deciden</b> (buscador multi-fuente). <b>★</b> = cargo que compra
esa línea.</p>

<div class="kpis">
  <div><b>{T['empresas']}</b>empresas</div>
  <div><b>{T['con_decisores']}</b>con decisores</div>
  <div><b>{T['con_compras_reales']}</b>con compras reales</div>
  <div><b>{sum(x['n_decisores'] for x in E)}</b>decisores</div>
</div>

<div class="aviso">
  <b>Por qué esto no existía antes:</b> las cuatro bases se construyeron por separado y <b>no
  cruzaban por nombre</b> — el eCRM usa siglas internas ("MLP", "Andina") y las otras usan razón
  social ("MINERA LOS PELAMBRES"). El cruce daba <b>cero justo en las cuentas más grandes</b>, y
  eso fue lo que reveló que faltaba la gran minería. Ahora hay alias verificados sigla → razón
  social.
</div>

{bloques}

<footer>
  Fuentes: eCRM INECO 2023-2025 · RETC MMA (residuos peligrosos) ·
  Direcmin + Transparencia Ley 20.285 + LinkedIn ·
  <a href="buscador_decisores.html">buscador de decisores</a> ·
  <a href="compradores_linkedin.html">compradores del eCRM</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(E)} empresas | {len(con_dec)} con decisores | {len(con_compra)} con compras")
