#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/dolor_ambiental.html — DOLOR AMBIENTAL POR EMPRESA.

Un solo documento, dos pestanas (RILES al agua / residuos peligrosos) mas una tercera de
cruces, como pide Victor: UNA sola vista por herramienta, no varios archivos sueltos.

Lee datos/dolor_ambiental_empresas.json.
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "dolor_ambiental.html")

d = json.load(open(os.path.join(D, "dolor_ambiental_empresas.json"), encoding="utf-8"))
EM = d["empresas"]
T = d["totales"]


def e(s):
    return html.escape(str(s if s is not None else ""))


def n(v, dec=0):
    try:
        return f"{float(v):,.{dec}f}"
    except Exception:
        return "—"


def li_contaminantes(lista, tope=12):
    out = []
    for c in lista[:tope]:
        out.append(f'<span class="chip">{e(c)}</span>')
    if len(lista) > tope:
        out.append(f'<span class="chip mas">+{len(lista)-tope}</span>')
    return "".join(out)


def badge_producto(p):
    col = {"Analítica en línea de metales": "#b91c1c",
           "Analítica específica de proceso": "#c2410c",
           "Software y plataforma": "#1d4ed8",
           "Trazabilidad de residuos peligrosos": "#047857",
           "Instrumentación": "#7c3aed",
           "Declaración RETC en línea": "#0891b2",
           "Monitoreo continuo de volumen": "#4b5563",
           "Instrumentación (diagnóstico)": "#6b7280"}.get(p, "#475569")
    return f'<span class="prod" style="background:{col}14;color:{col};border:1px solid {col}3d">{e(p)}</span>'


# ---------------- filas de la tabla ----------------
filas_agua = ""
for i, s in enumerate(EM, 1):
    c = s.get("contacto") or {}
    cont = c.get("nombre") or "—"
    filas_agua += f'''
    <tr data-b="{e(' '.join(s['que_vender'])).lower()}" data-t="{e(' '.join(s['contaminantes'])).lower()}">
      <td class="n">{i}</td>
      <td class="emp"><b>{e(s['empresa'])}</b><span class="sub">{e(s['rubro'])}</span></td>
      <td class="num"><b>{n(s['carga_peligrosa_t'],1)}</b><span class="sub">{n(s['emision_agua_t'])} t total</span></td>
      <td class="num">{s['n_contaminantes']}</td>
      <td class="cg">{li_contaminantes(s['contaminantes'], 8)}</td>
      <td class="pv">{"".join(badge_producto(p) for p in s['que_vender'])}</td>
      <td class="ct">{('<b>'+e(cont)+'</b><span class="sub">'+e(c.get('cargo') or '')+'</span>') if c.get('nombre') else '<span class="nada">sin contacto en el plan</span>'}</td>
    </tr>'''

# ---------------- RESPEL ----------------
con_respel = [s for s in EM if s.get("respel_t")]
con_respel.sort(key=lambda x: -x["respel_t"])
filas_respel = ""
for i, s in enumerate(con_respel, 1):
    pels = "".join(f'<span class="chip p">{e(k)} <b>{v}</b></span>' for k, v in (s.get("peligrosidades") or [])[:6])
    tipos = "".join(f'<span class="chip">{e(t[:46])}</span>' for t, _ in (s.get("tipos_respel") or [])[:4])
    c = s.get("contacto") or {}
    filas_respel += f'''
    <tr data-b="{e(' '.join(s['que_vender'])).lower()}">
      <td class="n">{i}</td>
      <td class="emp"><b>{e(s['empresa'])}</b><span class="sub">{e(s['rubro'])}</span></td>
      <td class="num"><b>{n(s['respel_t'])}</b><span class="sub">toneladas</span></td>
      <td class="num">{s['n_tipos_respel']}</td>
      <td class="cg">{pels}</td>
      <td class="cg">{tipos}</td>
      <td class="ct">{('<b>'+e(c.get('nombre'))+'</b>') if c.get('nombre') else '<span class="nada">sin contacto</span>'}</td>
    </tr>'''

# ---------------- ofertas ----------------
from collections import Counter
of = Counter()
for s in EM:
    for p in s["que_vender"]:
        of[p] += 1
bloques_of = ""
for p, v in of.most_common():
    emp = [s for s in EM if p in s["que_vender"]]
    top = ", ".join(x["empresa"] for x in emp[:6])
    bloques_of += f'''
    <div class="ofrec">
      <div class="ofh">{badge_producto(p)}<b>{v}</b> empresas</div>
      <div class="ofl">{e(top)}{'…' if len(emp) > 6 else ''}</div>
    </div>'''

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dolor ambiental medido — RETC x plan de contacto</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309;--ro:#b91c1c;--ve:#047857}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1360px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:900px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx);letter-spacing:-.3px}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
.tabs{{display:flex;gap:5px;margin:22px 0 0;border-bottom:2px solid var(--bd);flex-wrap:wrap}}
.tab{{padding:9px 17px;font-size:14px;font-weight:600;color:var(--mu);cursor:pointer;border:none;background:none;border-bottom:2.5px solid transparent;margin-bottom:-2px;font-family:inherit}}
.tab.on{{color:var(--ac);border-bottom-color:var(--ac)}}
.pan{{display:none;padding-top:16px}} .pan.on{{display:block}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
.barra{{display:flex;gap:9px;align-items:center;margin-bottom:12px;flex-wrap:wrap}}
input[type=search]{{flex:1;min-width:220px;padding:9px 13px;border:1px solid var(--bd);border-radius:8px;font-size:14px;font-family:inherit}}
input[type=search]:focus{{outline:none;border-color:var(--ac);box-shadow:0 0 0 3px #1d4ed814}}
.cuenta{{font-size:12.5px;color:var(--mu);white-space:nowrap}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd);position:sticky;top:0;background:var(--cd);z-index:2}}
td{{padding:10px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
tbody tr:hover{{background:#fafbfc}}
.num,.n{{text-align:right;font-variant-numeric:tabular-nums}}
.n{{color:var(--mu);font-size:12px;width:34px}}
.num b{{font-size:15px;letter-spacing:-.2px}}
.sub{{display:block;font-size:11px;color:var(--mu);font-weight:400;margin-top:1px}}
.emp b{{font-size:13.5px}}
.cg{{max-width:290px}}
.chip{{display:inline-block;font-size:11px;background:#f3f4f6;color:#374151;border-radius:5px;padding:2px 7px;margin:0 3px 3px 0}}
.chip.mas{{background:#1d4ed814;color:var(--ac)}}
.chip.p{{background:#b91c1c10;color:#991b1b}}
.chip.p b{{font-weight:700}}
.prod{{display:inline-block;font-size:11px;border-radius:5px;padding:2px 7px;margin:0 3px 3px 0;font-weight:600}}
.ct{{max-width:200px}} .ct b{{font-size:12.5px}}
.nada{{font-size:11.5px;color:#9ca3af;font-style:italic}}
.ofrec{{border:1px solid var(--bd);border-radius:9px;padding:11px 14px;margin-bottom:8px;background:var(--cd)}}
.ofh{{display:flex;align-items:center;gap:10px;margin-bottom:5px;font-size:13px}}
.ofh b{{font-size:17px;margin-left:auto}}
.ofl{{font-size:12px;color:var(--mu);line-height:1.5}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:15px 18px;font-size:13.5px;margin-bottom:14px}}
.metodo b{{font-weight:660}} .metodo code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12px}}
h2{{font-size:18px;font-weight:660;margin:22px 0 10px;letter-spacing:-.2px}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:5px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Dolor ambiental medido — qué le vendemos a cada empresa</h1>
<p class="sub0">RETC del Ministerio del Medio Ambiente cruzado con el plan de contacto. Por cada
empresa: qué contamina, cuánto, dónde descarga, qué producto lo resuelve y a quién llamar.
Dos vistas — <b>agua (DS 90/2000)</b> y <b>residuos peligrosos (DS 43/2015)</b>.</p>

<div class="kpis">
  <div><b>{T['con_riles']}</b>empresas con RILES</div>
  <div><b>{T['con_respel']:,}</b>generadoras de residuos peligrosos</div>
  <div><b>{T['en_plan_contacto']}</b>ya en el plan de contacto</div>
  <div><b>{T['con_2mas_productos']}</b>con 2+ productos a ofrecer</div>
</div>

<div class="aviso">
  <b>Se ordena por carga tóxica, no por volumen.</b> Al ordenar por emisión total aparecen
  arriba Guacolda (1.252.349 t), Engie (328.625 t) y Tornagaleones (153.357 t) — pero eso son
  <b>cloruros y sulfato</b>: agua de mar para enfriamiento y yeso. Volumen no es toxicidad: un
  cloruro no se multa, un cadmio sí. Tornagaleones pasa de 153.357 t de volumen a
  <b>23,8 t de carga tóxica</b>. El ranking prioriza los metales pesados y el cianuro.
</div>

<div class="tabs">
  <button class="tab on" data-p="agua">Agua — metales y tóxicos ({len(EM)})</button>
  <button class="tab" data-p="resp">Residuos peligrosos ({len(con_respel)})</button>
  <button class="tab" data-p="ofre">Qué se vende ({len(of)})</button>
  <button class="tab" data-p="met">Método y límites</button>
</div>

<div class="pan on" id="agua">
  <div class="card">
    <div class="barra">
      <input type="search" placeholder="Filtrar por empresa, contaminante o producto…" data-t="agua">
      <span class="cuenta" id="c-agua"></span>
    </div>
    <table><thead><tr>
      <th>#</th><th>Empresa</th><th>Carga tóxica</th><th>Cont.</th>
      <th>Qué contamina</th><th>Qué venderle</th><th>Contacto</th>
    </tr></thead><tbody id="t-agua">{filas_agua}</tbody></table>
  </div>
</div>

<div class="pan" id="resp">
  <div class="card">
    <div class="barra">
      <input type="search" placeholder="Filtrar por empresa o producto…" data-t="resp">
      <span class="cuenta" id="c-resp"></span>
    </div>
    <table><thead><tr>
      <th>#</th><th>Empresa</th><th>Respel</th><th>Tipos</th>
      <th>Peligrosidades declaradas</th><th>Residuos principales</th><th>Contacto</th>
    </tr></thead><tbody id="t-resp">{filas_respel}</tbody></table>
  </div>
</div>

<div class="pan" id="ofre">
  <h2>Qué se vende, y a cuántas empresas</h2>
  <p class="sub0">El producto no sale de un catálogo: se deriva del dato. Metales pesados al agua
  → analítica en línea. Diez o más contaminantes → plataforma de monitoreo continuo. Tres o más
  peligrosidades → trazabilidad de residuos.</p>
  {bloques_of}
</div>

<div class="pan" id="met">
  <div class="metodo">
    <b>El principio.</b> La SMA fiscaliza por norma. Cada obligación del DS 90 y del DS 43 que
    hoy no se mide en línea es un argumento de venta, y el tipo de obligación determina el
    producto. No se aplicó un catálogo a ciegas: el producto se deduce del contaminante real
    que la empresa declara.
  </div>
  <div class="metodo">
    <b>De dónde sale el dato, y por qué se puede auditar.</b><br>
    · <b>RILES</b> (DS 90/2000): <code>riles_2024.xlsx</code> del RETC, 10.870 filas, una por
    contaminante y punto de descarga. La unidad es <b>toneladas anuales</b>, declarada en la
    hoja <code>Metadatos</code> oficial.<br>
    · <b>Residuos peligrosos</b> (DS 43/2015): <code>respeligrosos_2025.xlsx</code> hoja
    <code>Generador</code>, 40.329 filas, con tipo de residuo y peligrosidad.<br>
    · <b>Contactos</b>: <code>plan_contacto.json</code>. Ambos archivos son públicos en
    datosretc.mma.gob.cl, sin credenciales.
  </div>
  <div class="metodo">
    <b>Dos errores que se midieron y se corrigieron en este trabajo.</b>
    <ul>
      <li><b>Emisión sumada por planta.</b> El plan de contacto sumaba la emisión una vez por
      establecimiento: Colbún mostraba <b>81.114</b> cuando la fuente dice <b>5.069,6</b>
      (×16, sus 16 plantas). Corregido a máximo y verificado contra el RETC crudo: los 3 casos
      de control coinciden. Ese número inflado estaba en la frase comercial.</li>
      <li><b>Señales duplicadas.</b> 219 de 468 empresas tenían la señal de RILES repetida,
      porque el universo repite la fila por comuna. Corregido con deduplicación: ahora 0.</li>
    </ul>
  </div>
  <div class="aviso">
    <b>Lo que este documento NO dice.</b><br>
    · Que estas empresas estén incumpliendo. Están <b>declarando</b> al RETC, que es una
    obligación distinta. El documento mide el <b>dolor</b> (lo que hay que medir y hoy no se mide
    en línea), no una infracción.<br>
    · Que la emisión sea constante. Es la <b>estimación anual</b> que la empresa reporta.<br>
    · Que el contacto sea el comprador técnico. Solo <b>{T['en_plan_contacto']}</b> de estas 370
    empresas están en el plan de contacto; el resto trae el dato ambiental sin contacto asignado.
  </div>
</div>

<footer>
  Fuente: Registro de Emisiones y Transferencias de Contaminantes (RETC), Ministerio del Medio
  Ambiente de Chile · <code>datosretc.mma.gob.cl</code>. Archivos: RILES 2024 y generación de
  residuos peligrosos 2025.
  <br>Ver también <a href="plan_contacto.html">plan de contacto</a> ·
  <a href="plan_contacto_tecnico.html">contacto técnico</a> ·
  <a href="estrategia_normativa.html">estrategia normativa</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div>
<script>
function activar(p) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('on', t.dataset.p === p));
  document.querySelectorAll('.pan').forEach(x => x.classList.toggle('on', x.id === p));
}}
document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => activar(t.dataset.p)));
function contar(k) {{
  const tb = document.getElementById('t-' + k);
  if (!tb) return;
  const vis = tb.querySelectorAll('tr:not([hidden])').length;
  const c = document.getElementById('c-' + k);
  if (c) c.textContent = vis + ' de ' + tb.querySelectorAll('tr').length + ' empresas';
}}
document.querySelectorAll('input[type=search]').forEach(inp => {{
  inp.addEventListener('input', () => {{
    const q = inp.value.toLowerCase().trim();
    const tb = document.getElementById('t-' + inp.dataset.t);
    tb.querySelectorAll('tr').forEach(tr => {{
      const hay = (tr.dataset.t || '') + ' ' + (tr.dataset.b || '') + ' ' +
                  tr.textContent.toLowerCase();
      tr.hidden = q && !hay.includes(q);
    }});
    contar(inp.dataset.t);
  }});
}});
contar('agua'); contar('resp');
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  filas agua:   {EM.__len__()}")
print(f"  filas respel: {len(con_respel)}")
print(f"  productos:    {len(of)}")
