#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renderiza la ESCALERA AL ÉXITO agrupada POR LÍNEA DE PRODUCTO.

Lee datos/escalera_exito.json (lo produce escalera_por_linea.py), cuya estructura es
{"lineas": {nombre: {desc, medible, productos: [...]}}}.

7 líneas: Instrumentación · Analítica · Válvulas · DCS · PLC · SIS · Software y plataforma.
Cada línea declara si su mercado es medible (hardware, partida arancelaria) o no (software,
que se vende dentro del proyecto).

NO se comparan puntajes entre líneas: una línea con mercado medido y otra sin mercado no
son comparables. El puntaje ordena DENTRO de cada línea.

Salida: artefactos/escalera_exito.html
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "escalera_exito.html")

# usar la v3 si existe: trae los mercados corregidos por partida arancelaria
_ruta = os.path.join(D, "escalera_exito_v3.json")
if not os.path.exists(_ruta):
    _ruta = os.path.join(D, "escalera_exito.json")
d = json.load(open(_ruta, encoding="utf-8"))
L = d["lineas"]

COL = {"VERDE":"#047857", "AMARILLO":"#d97706", "ROJO":"#64748b"}
BG  = {"VERDE":"#ecfdf5", "AMARILLO":"#fffbeb", "ROJO":"#f1f5f9"}

def ancla(n): return "l-" + n.lower().replace(" ","-").replace("ó","o").replace("á","a").replace("í","i").replace("é","e")

def usd(v):
    if not v: return "no medido"
    return "US$" + f"{v/1e6:,.1f}".replace(",","X").replace(".",",").replace("X",".") + "M"

def barra(score, mx):
    pct = max(2.0, (score/mx)*100) if mx else 2.0
    return f'<div class="bar"><div class="fill" style="width:{pct:.0f}%"></div></div>'

def fila(t, i, mx):
    r = t["R"]
    if t["mercado_usd"]:
        mer = (f'<b>{usd(t["mercado_usd"])}</b>'
               f'<span class="sub">{t["mercado_items"]:,} ítems importados</span>')
        extra = (f'<div class="nic"><span class="k">Rivales en Chile</span> '
                 f'{html.escape(", ".join(t["rivales_chile"] or []) or "sin dato")}</div>')
    else:
        mer = ('<b class="nomedido">mercado de línea</b>'
               '<span class="sub">vive del mercado de su línea, no tiene cuota propia medida</span>')
        extra = (f'<div class="nic"><span class="k">Nicho</span> {html.escape(t["nicho"] or "")}'
                 f'<span class="k" style="margin-left:14px">Rivales declarados</span> '
                 f'{html.escape(t["rivales_declarados"] or "")}</div>')
    return f'''
  <article class="fila">
    <div class="pr">
      <span class="rank">{i}</span>
      <div class="nm"><b>{html.escape(t["producto"])}</b></div>
      <div class="sc">{t["score"]}<span>/ {mx}</span></div>
    </div>
    <div class="ejes">
      <div class="eje"><span class="k">P · Producto</span><b>{t["P"]}</b>
        <span class="sub">{t["argumentos"]} argumentos · {t["objeciones"]} objeciones</span></div>
      <div class="eje"><span class="k">M · Mercado</span>{mer}</div>
      <div class="eje"><span class="k">R · Respuesta</span>
        <b style="color:{COL[r]};background:{BG[r]};border-radius:6px;padding:2px 8px;font-size:13px">{r}</b>
        <span class="sub">{html.escape(t["R_nota"])}</span></div>
    </div>
    {barra(t["score"], mx)}
    {extra}
    <div class="fuentes">
      {'<span class="chip-si">con battlecard</span>' if t["battlecard"] else '<span class="chip-no">sin battlecard del fabricante</span>'}
      <span class="sub">{t["criticos"]} campo(s) por completar</span>
    </div>
  </article>'''

secciones = ""
nav = ""
for nombre, cfg in L.items():
    ps = cfg["productos"]
    if not ps: continue
    mx = max(p["score"] for p in ps) or 1
    verdes = sum(1 for p in ps if p["R"]=="VERDE")
    rojos  = sum(1 for p in ps if p["R"]=="ROJO")
    medible = cfg["medible"]
    # el mercado medido es el de la LINEA (varias fichas de la misma linea viven del mismo
    # mercado). Se muestra a nivel de linea, con la nota de correccion si la hay.
    mlinea = cfg.get("mercado_corregido_usd")
    nota_c = cfg.get("nota_correccion")
    nav += (f'<a class="nb" href="#{ancla(nombre)}">{html.escape(nombre)} <b>{len(ps)}</b></a>')
    extra_tags = (f'<span class="tag tv">{verdes} con R verde</span>' if verdes else '') + \
                 (f'<span class="tag tr">{rojos} no sube{"n" if rojos>1 else ""}</span>' if rojos else '')
    if mlinea:
        bloque_mercado = (f'<div class="mlinea"><span class="ml-k">Mercado medido de la línea</span>'
                          f'<b>{usd(mlinea)}</b>'
                          f'<span class="ml-n">Registro DIN de Aduanas Chile 2025, por partida '
                          f'arancelaria. Es el mercado de la línea: las fichas de abajo viven de '
                          f'este mismo mercado.</span></div>')
    elif nota_c:
        bloque_mercado = (f'<div class="mlinea sin"><span class="ml-k">Mercado</span>'
                          f'<b>no medible aparte</b><span class="ml-n">{html.escape(nota_c)}</span></div>')
    else:
        bloque_mercado = (f'<div class="mlinea sin"><span class="ml-k">Mercado</span>'
                          f'<b>no medible con Aduanas</b><span class="ml-n">Esta línea no entra '
                          f'por partida arancelaria: se vende dentro del proyecto.</span></div>')
    if nota_c and mlinea:
        antes = cfg.get("mercado_antes_usd")
        if isinstance(antes, list):
            antes = sum(antes)
        txt_antes = f" Antes se reportaba {usd(antes)}." if antes else ""
        bloque_mercado += (f'<div class="corr-l"><b>Corrección.</b> {html.escape(nota_c)}'
                           f'{txt_antes}</div>')
    secciones += f'''
<h2 id="{ancla(nombre)}">{html.escape(nombre)}
  <span class="tag">{len(ps)} producto{'s' if len(ps)!=1 else ''}</span>
  <span class="tag {'tm' if medible else 'tn'}">{'mercado medido' if medible else 'mercado no medido'}</span>
  {extra_tags}
</h2>
<p class="explica">{html.escape(cfg["desc"])}</p>
{bloque_mercado}
{"".join(fila(p, i, mx) for i, p in enumerate(ps, 1))}'''

total = sum(len(c["productos"]) for c in L.values())
todos = [p for c in L.values() for p in c["productos"]]
verde_tot = sum(1 for p in todos if p["R"]=="VERDE")
rojo = [p for p in todos if p["R"]=="ROJO"]
bat = sum(1 for p in todos if p["battlecard"])
medibles = sum(1 for p in todos if p["mercado_usd"])
n_lineas = len([c for c in L.values() if c["productos"]])
def linea_de(t):
    """Devuelve la linea a la que pertenece un producto (para etiquetarlo en el resumen)."""
    for k, c in L.items():
        if t in c["productos"]:
            return k
    return ""

no_suben = ""
for t in rojo:
    ln = html.escape(linea_de(t))
    no_suben += f'<li><b>{html.escape(t["producto"])}</b> <span class="ln">{ln}</span> — {html.escape(t["R_nota"])}</li>'

HTML = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Escalera al Éxito por línea — Catálogo SUPCON</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:14.5px;line-height:1.55;padding:26px 20px 70px}}
.wrap{{max-width:1060px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.5px}}
.sub-top{{color:var(--mu);margin:5px 0 18px;font-size:14.5px;max-width:880px}}
.nav{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px;position:sticky;top:0;z-index:20;
  background:rgba(248,250,252,.97);backdrop-filter:blur(8px);padding:11px 0;border-bottom:1px solid var(--bd)}}
.nb{{font-size:13px;text-decoration:none;color:#334155;background:var(--cd);border:1px solid #cbd5e1;
  border-radius:9px;padding:7px 12px;font-weight:550}}
.nb:hover{{border-color:var(--ac);color:var(--ac)}}
.nb b{{opacity:.65;margin-left:3px}}
h2{{font-size:19px;font-weight:660;margin:36px 0 6px;letter-spacing:-.2px;scroll-margin-top:70px}}
.tag{{font-size:11.5px;background:var(--acs);color:var(--ac);border-radius:6px;padding:3px 10px;font-weight:600;margin-left:7px;vertical-align:middle}}
.tag.tm{{background:#ecfdf5;color:#047857}}
.tag.tn{{background:#f1f5f9;color:#64748b}}
.tag.tv{{background:#ecfdf5;color:#047857}}
.tag.tr{{background:#f1f5f9;color:#475569}}
.explica{{color:var(--mu);font-size:13.5px;margin-bottom:13px;max-width:880px}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:15px 18px;margin-bottom:20px;font-size:13.5px;color:#334155}}
.metodo code{{background:#f1f5f9;padding:1px 6px;border-radius:4px;font-size:12.5px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:19px;font-weight:700;color:var(--tx);letter-spacing:-.3px}}
.fila{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:15px 18px;margin-bottom:10px}}
.pr{{display:flex;align-items:center;gap:11px;margin-bottom:11px}}
.rank{{font-size:12.5px;color:#94a3b8;font-weight:700;min-width:24px}}
.nm{{flex:1}} .nm b{{font-size:15.5px;font-weight:650;letter-spacing:-.2px}}
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
.mlinea{{background:#fff;border:1px solid #e2e8f0;border-left:4px solid #2563eb;border-radius:10px;
  padding:13px 18px;margin:12px 0 18px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}}
.mlinea.sin{{border-left-color:#94a3b8}}
.mlinea b{{font-size:23px;font-weight:700;letter-spacing:-.5px;font-variant-numeric:tabular-nums}}
.ml-k{{font-size:11.5px;text-transform:uppercase;letter-spacing:.5px;color:#64748b;font-weight:700}}
.ml-n{{font-size:12.5px;color:#64748b;flex:1;min-width:200px;line-height:1.5}}
.corr-l{{background:#eff6ff;border:1px solid #bfdbfe;border-radius:9px;padding:12px 16px;margin:-8px 0 18px;
  font-size:13px;color:#1e40af;line-height:1.58}}
.nic{{font-size:12.5px;color:#475569;background:#fbfdff;border:1px solid var(--bd);border-radius:8px;padding:8px 11px;margin-bottom:7px}}
.nic .k{{font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:.4px;font-weight:700;margin-right:4px}}
.fuentes{{display:flex;gap:14px;align-items:center;flex-wrap:wrap;padding-top:7px;border-top:1px solid #f1f5f9}}
.chip-si{{font-size:11px;background:#ecfdf5;color:#047857;border-radius:5px;padding:2px 8px;font-weight:700}}
.chip-no{{font-size:11px;background:#f1f5f9;color:#64748b;border-radius:5px;padding:2px 8px;font-weight:700}}
h3{{font-size:15px;margin:24px 0 9px}}
ul{{list-style:none}}
ul li{{position:relative;padding-left:15px;margin-bottom:6px;font-size:14px}}
ul li:before{{content:"";position:absolute;left:3px;top:8px;width:5px;height:5px;border-radius:50%;background:#d97706}}
.ln{{font-size:11.5px;background:#f1f5f9;color:#64748b;border-radius:5px;padding:1px 7px;margin:0 4px}}
footer{{margin-top:34px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Escalera al Éxito por línea</h1>
<p class="sub-top">Los {total} productos del portafolio SUPCON calificados con la metodología de CONECTA,
agrupados en {n_lineas} líneas de producto, para decidir dónde poner el esfuerzo comercial.</p>

<div class="metodo">
  <b>Cómo se lee.</b> <code>P</code> (producto) = fuerza de la propuesta según el material del fabricante:
  argumentos documentados, objeciones ya trabajadas y si trae battlecard. <code>M</code> (mercado) = tamaño
  importado real en Chile 2025, solo en las líneas de hardware. <code>R</code> (respuesta) = si podemos cumplir:
  <b style="color:#047857">VERDE</b> respondemos hoy ·
  <b style="color:#d97706">AMARILLO</b> respondemos con condiciones ·
  <b style="color:#64748b">ROJO</b> no podemos responder todavía.
  <br><br>
  <b>Regla de hierro:</b> con R en rojo <u>no se sube de escalón</u>.
  <b>El puntaje ordena dentro de cada línea, nunca entre líneas</b>: una línea con mercado medido y otra
  sin mercado no son comparables. El puntaje no es una probabilidad de venta.
</div>

<div class="kpi">
  <div><b>{total}</b>productos evaluados</div>
  <div><b>{n_lineas}</b>líneas de producto</div>
  <div><b>{medibles}</b>con mercado medido en Aduanas</div>
  <div><b>{verde_tot}</b>con R verde</div>
  <div><b>{bat}</b>con battlecard del fabricante</div>
</div>

<div class="nav">{nav}</div>
{secciones}

<h3>Los que no suben de escalón</h3>
<ul>{no_suben}</ul>

<footer>
  Metodología: Escalera al Éxito (Escalón 1 <i>P×M×R</i> y matriz de priorización), CONECTA.
  Mercado de hardware: Registro DIN de Aduanas, Chile 2025 · Capacidad: material del fabricante SUPCON y Hobré.
  Las líneas de software y plataforma no tienen mercado medible con ese registro y se declaran sin tamaño.
  <br>Volver al <a href="../index.html">catálogo de fichas de producto</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"lineas={n_lineas} | productos={total} | mercado medido={medibles} | R verde={verde_tot} | battlecard={bat}")
