#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renderiza la ESCALERA AL ÉXITO del catálogo SUPCON.

Lee datos/escalera_exito.json (lo produce escalera_exito_v2.py).

Dos escaleras separadas, porque el software no entra por partida arancelaria y por lo
tanto no tiene mercado medible con el Registro DIN de Aduanas:
  A · Hardware        (27) — el mercado sale de las importaciones reales 2025
  B · Software        (17) — el mercado NO es medible; se evalua P y R, y el nicho se
                            declara sin tamaño

Salida: artefactos/escalera_exito.html
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "escalera_exito.html")

d = json.load(open(os.path.join(D, "escalera_exito.json"), encoding="utf-8"))
A = d["escalera_a_hardware"]
B = d["escalera_b_software"]

COL = {"VERDE":"#047857", "AMARILLO":"#d97706", "ROJO":"#64748b"}
BG  = {"VERDE":"#ecfdf5", "AMARILLO":"#fffbeb", "ROJO":"#f1f5f9"}

def usd(v):
    if v is None: return "no medido"
    return f"US${v/1e6:,.1f}M"

def barra(score, maximo):
    pct = max(2.0, (score/maximo)*100) if maximo else 2.0
    return (f'<div class="bar"><div class="fill" style="width:{pct:.0f}%"></div></div>')

def fila(t, i, maxscore, esc):
    r = t["R"]
    rivales = ", ".join(t.get("rivales") or [t.get("rivales_declarados","")])
    rivales = " · ".join(x for x in [t.get("rivales") and ", ".join(t["rivales"]) or t.get("rivales_declarados","")] if x)
    mercado = (f'<b>{usd(t["mercado_usd"])}</b><span class="sub">{t["mercado_items"]:,} ítems importados</span>'
               if t["mercado_usd"] is not None else
               f'<b class="nomedido">no medido</b><span class="sub">el software no entra por partida arancelaria</span>')
    nicho = f'<div class="nic"><span class="k">Nicho</span> {html.escape(t.get("nicho",""))}' \
            f'<span class="k" style="margin-left:12px">Rivales declarados</span> {html.escape(t.get("rivales_declarados",""))}</div>' \
            if "nicho" in t else ""
    return f'''
  <article class="fila">
    <div class="pr">
      <span class="rank">{i}</span>
      <div class="nm">
        <b>{html.escape(t["producto"])}</b>
        <span class="fam">{html.escape(t["familia"])}</span>
      </div>
      <div class="sc">{t["score"]}<span>/ {maxscore}</span></div>
    </div>
    <div class="ejes">
      <div class="eje"><span class="k">P · Producto</span><b>{t["P"]}</b>
        <span class="sub">{t["argumentos"]} argumentos · {t["objeciones"]} objeciones</span></div>
      <div class="eje"><span class="k">M · Mercado</span>{mercado}</div>
      <div class="eje"><span class="k">R · Respuesta</span>
        <b style="color:{COL[r]};background:{BG[r]};border-radius:6px;padding:2px 8px;font-size:13px">{r}</b>
        <span class="sub">{html.escape(t["R_nota"])}</span></div>
    </div>
    {barra(t["score"], maxscore)}
    {nicho}
    <div class="fuentes">
      {'<span class="chip-si">con battlecard</span>' if t["battlecard"] else '<span class="chip-no">sin battlecard del fabricante</span>'}
      <span class="sub">{t["criticos"]} campo(s) por completar</span>
      {f'<span class="sub">rivales en Chile: {html.escape(rivales)}</span>' if rivales else ''}
    </div>
  </article>'''

maxA = max(t["score"] for t in A) or 1
maxB = max(t["score"] for t in B) or 1

filasA = "".join(fila(t, i, maxA, "A") for i, t in enumerate(A, 1))
filasB = "".join(fila(t, i, maxB, "B") for i, t in enumerate(B, 1))

con_bat = sum(1 for t in A+B if t["battlecard"])
verde   = sum(1 for t in A+B if t["R"]=="VERDE")
rojo    = [t for t in A+B if t["R"]=="ROJO"]
no_suben = "".join(f'<li><b>{html.escape(t["producto"])}</b> — {html.escape(t["R_nota"])}</li>' for t in rojo)

HTML = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Escalera al Éxito — Catálogo SUPCON</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:14.5px;line-height:1.55;padding:26px 20px 70px}}
.wrap{{max-width:1060px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.5px}}
.sub-top{{color:var(--mu);margin:5px 0 20px;font-size:14.5px;max-width:880px}}
h2{{font-size:19px;font-weight:660;margin:34px 0 6px;letter-spacing:-.2px}}
h2 .tag{{font-size:12px;background:var(--acs);color:var(--ac);border-radius:6px;padding:3px 10px;font-weight:600;margin-left:8px;vertical-align:middle}}
.explica{{color:var(--mu);font-size:13.5px;margin-bottom:14px;max-width:880px}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid #d97706;border-radius:10px;
  padding:14px 17px;margin-bottom:20px;font-size:14px}}
.aviso b{{color:#92400e}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:15px 18px;margin-bottom:22px;font-size:13.5px;color:#334155}}
.metodo code{{background:#f1f5f9;padding:1px 6px;border-radius:4px;font-size:12.5px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:19px;font-weight:700;color:var(--tx);letter-spacing:-.3px}}
.fila{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:15px 18px;margin-bottom:10px}}
.pr{{display:flex;align-items:center;gap:11px;margin-bottom:11px}}
.rank{{font-size:12.5px;color:#94a3b8;font-weight:700;min-width:24px}}
.nm{{display:flex;align-items:center;gap:9px;flex-wrap:wrap;flex:1}}
.nm b{{font-size:15.5px;font-weight:650;letter-spacing:-.2px}}
.fam{{font-size:11.5px;background:var(--acs);color:var(--ac);border-radius:6px;padding:2px 9px;font-weight:600}}
.sc{{font-size:19px;font-weight:700;letter-spacing:-.5px}}
.sc span{{font-size:11.5px;color:#94a3b8;font-weight:600}}
.ejes{{display:grid;grid-template-columns:1fr 1.15fr 1.5fr;gap:14px;margin-bottom:9px}}
@media(max-width:780px){{.ejes{{grid-template-columns:1fr}}}}
.eje{{display:flex;flex-direction:column;gap:2px}}
.eje .k{{font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:.45px;font-weight:700}}
.eje b{{font-size:15px;font-weight:650}}
.nomedido{{color:#94a3b8 !important;font-weight:600 !important;font-size:13px !important}}
.sub{{font-size:11.5px;color:var(--mu)}}
.bar{{height:5px;background:#f1f5f9;border-radius:3px;overflow:hidden;margin:8px 0}}
.fill{{height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:3px}}
.nic{{font-size:12.5px;color:#475569;background:#fbfdff;border:1px solid var(--bd);border-radius:8px;padding:8px 11px;margin-bottom:7px}}
.nic .k{{font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:.4px;font-weight:700;margin-right:4px}}
.fuentes{{display:flex;gap:14px;align-items:center;flex-wrap:wrap;padding-top:7px;border-top:1px solid #f1f5f9}}
.chip-si{{font-size:11px;background:#ecfdf5;color:#047857;border-radius:5px;padding:2px 8px;font-weight:700}}
.chip-no{{font-size:11px;background:#f1f5f9;color:#64748b;border-radius:5px;padding:2px 8px;font-weight:700}}
h3{{font-size:15px;margin:22px 0 9px}}
ul{{list-style:none}}
ul li{{position:relative;padding-left:15px;margin-bottom:5px;font-size:14px}}
ul li:before{{content:"";position:absolute;left:3px;top:8px;width:5px;height:5px;border-radius:50%;background:#d97706}}
footer{{margin-top:34px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Escalera al Éxito — Catálogo SUPCON</h1>
<p class="sub-top">Los {len(A)+len(B)} productos del portafolio calificados con la metodología de CONECTA,
para decidir dónde poner el esfuerzo comercial. Dos escaleras separadas: el hardware tiene mercado medido
y el software no.</p>

<div class="metodo">
  <b>Cómo se lee.</b> <code>P</code> (producto) = fuerza de la propuesta según el material del fabricante:
  argumentos documentados, objeciones ya trabajadas y si trae battlecard. <code>M</code> (mercado) = tamaño
  importado real en Chile 2025. <code>R</code> (respuesta) = semáforo de si podemos cumplir:
  <b style="color:#047857">VERDE</b> podemos responder hoy ·
  <b style="color:#d97706">AMARILLO</b> respondemos con condiciones ·
  <b style="color:#64748b">ROJO</b> no podemos responder todavía.
  <br><br>
  <b>Regla de hierro de la metodología:</b> con R en rojo <u>no se sube de escalón</u>.
  El puntaje no es una probabilidad de venta: ordena por dónde conviene empezar.
</div>

<div class="kpi">
  <div><b>{len(A)+len(B)}</b>productos evaluados</div>
  <div><b>{verde}</b>con R verde</div>
  <div><b>{len(rojo)}</b>con R rojo (no suben)</div>
  <div><b>{con_bat}</b>con battlecard del fabricante</div>
</div>

<h2>Escalera A · Hardware <span class="tag">{len(A)} productos</span></h2>
<p class="explica">Productos cuya venta entra por partida arancelaria: el mercado sale de las
importaciones reales de Chile 2025 (Registro DIN de Aduanas). El puntaje cruza la fuerza de la
propuesta con el tamaño del mercado y la capacidad de responder.</p>
{filasA}

<h2>Escalera B · Software y plataforma <span class="tag">{len(B)} productos</span></h2>
<p class="explica">El software no entra por partida arancelaria: se vende dentro del proyecto, así que
<b>este estudio no puede medir su mercado</b>. Evaluamos lo que sí es dato del fabricante —la fuerza de
la propuesta (P) y si podemos responder (R)— y declaramos el nicho sin tamaño. No se inventa un mercado.</p>
{filasB}

<h3>Los que no suben de escalón</h3>
<ul>{no_suben}</ul>

<footer>
  Metodología: Escalera al Éxito (Escalón 1 <i>P×M×R</i> y Escalón 2 <i>N×Pv×Map</i>), CONECTA.
  Mercado: Registro DIN de Aduanas, Chile 2025 · Capacidad: material del fabricante SUPCON y Hobré.
  <br>Volver al <a href="../index.html">catálogo de fichas de producto</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"A={len(A)} productos | B={len(B)} productos | R verde={verde} | R rojo={len(rojo)} | battlecard={con_bat}")
