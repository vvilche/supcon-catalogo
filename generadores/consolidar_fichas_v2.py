#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CATALOGO DE FICHAS DE PRODUCTO SUPCON — las 44 fichas en una sola vista.

Formato: TABLA de los 8 campos de CONECTA, SIEMPRE VISIBLE (igual que las entregas
individuales fichas_producto_2/3/4.html). Arriba, buscador y filtros para llegar rapido.

Los 8 campos (formato de referencia PORTAFOLIO_COMPLETO_CONECTA_360.md):
  Nombre de Producto o Servicio · Descripción del Servicio · Beneficios · Clientes Target
  · Competencia · Argumentos de Venta · Manejo de Objeciones · Preguntas Técnicas

Entradas: datos/fichas_1_datos.json ... fichas_4_datos.json
Salida:   artefactos/fichas_vendedores.html   (es la portada del sitio)

NOTA DE DISENO (leccion de un rechazo real): la v1 (consolidar_fichas_v1.py) envolvia la
ficha en una "tarjeta comercial" con los campos detras de un desplegable. Victor la
rechazo: "no veo las fichas como ficha de producto". El formato correcto es la tabla de
8 campos a la vista, tal como en las entregas 2/3/4. NO volver a esconder los campos.
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "fichas_vendedores.html")

def cargar(n):
    p = os.path.join(D, n)
    if not os.path.exists(p): return {}
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, dict) and "fichas" in d: return d["fichas"]
    return d if isinstance(d, dict) else {}

def norm(x, grupo):
    return {
      "familia": x.get("familia") or grupo,
      "descripcion": x.get("descripcion") or x.get("descripción") or "",
      "beneficios": x.get("beneficios") or [],
      "clientes": x.get("clientes_target") or x.get("clientes") or [],
      "competencia": x.get("competencia") or "",
      "argumentos": x.get("argumentos_venta") or x.get("argumentos") or [],
      "objeciones": x.get("objeciones") or [],
      "preguntas": x.get("preguntas_tecnicas") or x.get("preguntas") or [],
      "fuente": x.get("fuente") or "",
    }

GRUPOS = [
  ("Instrumentación de campo", "fichas_3_datos.json"),
  ("Analítica de proceso",     "fichas_1_datos.json"),
  ("Control y seguridad",      "fichas_2_datos.json"),
  ("Software y plataforma",    "fichas_4_datos.json"),
]

TODAS = []
for grupo, arch in GRUPOS:
    for nombre, x in cargar(arch).items():
        if not isinstance(x, dict): continue
        f = norm(x, grupo)
        f["nombre"] = nombre
        f["grupo"] = grupo
        TODAS.append(f)

def sin_tilde(t):
    t = str(t).lower()
    for a, b in (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")):
        t = t.replace(a, b)
    return " ".join(t.split())

PORC = "POR COMPLETAR"

def criticos(f):
    n = 0
    for c in ("descripcion","beneficios","clientes","argumentos","preguntas","objeciones"):
        n += json.dumps(f.get(c), ensure_ascii=False).count(PORC)
    return n

def estado(f):
    n = criticos(f)
    if n == 0:  return ("Lista", "ok", "Completa: se puede usar con cliente sin validar")
    if n <= 4:  return ("Usable", "casi", f"Usable: {n} dato(s) a confirmar con fábrica")
    return ("Validar", "rev", f"Confirmar antes de ofrecer: {n} datos sin respaldo en el material")

def li(xs):
    xs = [str(x) for x in xs if str(x).strip()]
    return "".join(f'<li>{html.escape(x)}</li>' for x in xs)

def obj(objs):
    out = []
    for o in objs:
        if isinstance(o, (list, tuple)) and len(o) >= 2:
            q, r = o[0], o[1]
        elif isinstance(o, dict):
            q, r = o.get("pregunta",""), o.get("respuesta","")
        else:
            continue
        if not str(q).strip(): continue
        r = str(r).strip()
        rr = html.escape(r) if r else '<i class="falta">Sin respuesta documentada — validar con fábrica</i>'
        out.append(f'<div class="ob"><div class="q">{html.escape(str(q))}</div><div class="r">{rr}</div></div>')
    return "".join(out)

def fila_ficha(f, i):
    etq, cls, tip = estado(f)
    comp = f["competencia"]
    chip = ' <span class="chip-pend">sin battlecard</span>' if PORC in comp else ""
    return f'''
<article class="ficha"
   data-grupo="{html.escape(f["grupo"])}" data-fam="{html.escape(f["familia"])}"
   data-busca="{html.escape(sin_tilde(f["nombre"]+" "+f["familia"]+" "+f["grupo"]+" "+f["descripcion"][:400]+" "+" ".join(f["argumentos"][:6])+" "+" ".join(f["clientes"][:6])+" "+" ".join(f["preguntas"][:8])))}">
  <div class="fh">
    <span class="num">{i}</span>
    <h3>{html.escape(f["nombre"])}</h3>
    <span class="fam">{html.escape(f["familia"])}</span>
    <span class="estado {cls}" title="{html.escape(tip)}">{etq}</span>
  </div>
  <table>
    <tr><td class="k">Nombre de Producto o Servicio</td><td class="v">{html.escape(f["nombre"])}</td></tr>
    <tr><td class="k">Descripción del Servicio</td><td class="v">{html.escape(f["descripcion"])}</td></tr>
    <tr><td class="k">Beneficios</td><td class="v"><ul>{li(f["beneficios"])}</ul></td></tr>
    <tr><td class="k">Clientes Target</td><td class="v"><ul class="cl">{li(f["clientes"])}</ul></td></tr>
    <tr><td class="k">Competencia</td><td class="v">{html.escape(comp)}{chip}</td></tr>
    <tr><td class="k">Argumentos de Venta</td><td class="v"><ul>{li(f["argumentos"])}</ul></td></tr>
    <tr><td class="k">Manejo de Objeciones</td><td class="v">{obj(f["objeciones"]) or "<i>Sin objeciones documentadas en el material.</i>"}</td></tr>
    <tr><td class="k">Preguntas Técnicas</td><td class="v"><ol>{li(f["preguntas"])}</ol></td></tr>
  </table>
  <div class="fuente">Fuente: {html.escape(f["fuente"]) or "material del fabricante SUPCON"}</div>
</article>'''

tarjetas = "".join(fila_ficha(f, i) for i, f in enumerate(TODAS, 1))

fams = sorted(set(f["familia"] for f in TODAS))
opts = "".join(f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in fams)
botones = "".join(
  f'<label class="fb"><input type="radio" name="g" value="{html.escape(g)}">'
  f'<span>{html.escape(g)} <b>{sum(1 for f in TODAS if f["grupo"]==g)}</b></span></label>'
  for g,_ in GRUPOS)

n_ok   = sum(1 for f in TODAS if estado(f)[0]=="Lista")
n_use  = sum(1 for f in TODAS if estado(f)[0]=="Usable")
n_val  = sum(1 for f in TODAS if estado(f)[0]=="Validar")
n_comp = sum(1 for f in TODAS if PORC in f["competencia"])

HTML = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fichas de Producto — Catálogo SUPCON</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;
  --am:#d97706;--ams:#fffbeb;--ok:#047857;--oks:#ecfdf5}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:14.5px;line-height:1.55;padding:26px 20px 70px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.5px}}
.sub{{color:var(--mu);margin:5px 0 18px;font-size:14.5px;max-width:860px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:19px;font-weight:700;color:var(--tx);letter-spacing:-.3px}}
.barra{{position:sticky;top:0;z-index:20;background:rgba(248,250,252,.97);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--bd);padding:12px 0;margin-bottom:18px;display:flex;gap:9px;flex-wrap:wrap;align-items:center}}
.barra input[type=search]{{flex:1;min-width:250px;padding:9px 13px;border:1px solid #cbd5e1;border-radius:9px;font-size:14.5px;font-family:inherit}}
.barra select{{padding:9px 11px;border:1px solid #cbd5e1;border-radius:9px;font-size:14px;background:var(--cd);font-family:inherit}}
.fb{{cursor:pointer}} .fb input{{display:none}}
.fb span{{display:inline-block;border:1px solid #cbd5e1;background:var(--cd);color:#334155;border-radius:9px;padding:8px 12px;font-size:13px}}
.fb input:checked+span{{background:var(--ac);border-color:var(--ac);color:#fff}}
.fb b{{opacity:.7}}
.ficha{{background:var(--cd);border:1px solid var(--bd);border-radius:14px;padding:18px 20px;margin-bottom:14px}}
.fh{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding-bottom:11px;margin-bottom:4px;border-bottom:2px solid var(--ac)}}
.num{{font-size:12px;color:#94a3b8;font-weight:700;min-width:22px}}
.fh h3{{font-size:18px;font-weight:660;letter-spacing:-.3px}}
.fam{{background:var(--acs);color:var(--ac);border-radius:6px;padding:2px 10px;font-size:12px;font-weight:600}}
.estado{{margin-left:auto;font-size:11px;border-radius:6px;padding:3px 10px;font-weight:700;text-transform:uppercase;letter-spacing:.3px}}
.estado.ok{{background:var(--oks);color:var(--ok)}}
.estado.casi{{background:var(--ams);color:var(--am)}}
.estado.rev{{background:#f1f5f9;color:#475569}}
table{{width:100%;border-collapse:collapse;margin-top:8px}}
td{{padding:9px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top;font-size:13.8px}}
tr:last-child td{{border-bottom:none}}
td.k{{width:185px;color:var(--mu);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;padding-top:12px}}
td.v{{color:var(--tx)}}
ul,ol{{list-style:none}}
ul li,ol li{{position:relative;padding-left:15px;margin-bottom:4px}}
ul li:before{{content:"";position:absolute;left:3px;top:7px;width:5px;height:5px;border-radius:50%;background:var(--ac)}}
ul.cl li:before{{background:var(--am)}}
ol{{counter-reset:n}}
ol li{{counter-increment:n}}
ol li:before{{content:counter(n) ".";position:absolute;left:0;color:var(--ac);font-weight:700;font-size:12px;top:1px}}
.ob{{margin-bottom:9px;padding-left:11px;border-left:2px solid var(--bd)}}
.ob .q{{font-weight:640;font-size:13.4px;color:#334155}}
.ob .r{{font-size:13.2px;color:var(--mu)}}
.falta{{color:#94a3b8;font-style:italic}}
.chip-pend{{font-size:10.5px;font-weight:600;color:#94a3b8;background:#f1f5f9;border-radius:5px;padding:1px 7px}}
.fuente{{margin-top:11px;padding-top:9px;border-top:1px solid #f1f5f9;font-size:11px;color:#94a3b8;font-family:ui-monospace,monospace}}
.vacio{{text-align:center;color:var(--mu);padding:40px;display:none}}
.leyenda{{font-size:12.5px;color:var(--mu);margin-bottom:20px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
footer{{margin-top:32px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Fichas de Producto — Catálogo SUPCON</h1>
<p class="sub">Las {len(TODAS)} fichas comerciales del portafolio, en formato de 8 campos.
Busca por producto, aplicación o cliente — no importan las tildes.</p>

<div class="kpi">
  <div><b>{len(TODAS)}</b>productos</div>
  <div><b>{len(fams)}</b>familias</div>
  <div><b>{n_ok}</b>listas sin observación</div>
  <div><b>{n_use}</b>usables con dato a confirmar</div>
  <div><b>{n_val}</b>con material escaso</div>
</div>

<div class="leyenda">
  <span class="estado ok">Lista</span> se puede usar tal cual ·
  <span class="estado casi">Usable</span> sirve para vender, algún dato a confirmar en fábrica ·
  <span class="estado rev">Validar</span> confirmar antes de ofrecer ·
  <span class="chip-pend">sin battlecard</span> el fabricante no entregó argumento de competencia ({n_comp} fichas)
</div>

<div class="barra">
  <input id="q" type="search" placeholder="Buscar producto, aplicación o cliente… (ej. valvula, mineria, analizador, APC)">
  <select id="fam"><option value="">Todas las familias</option>{opts}</select>
  <label class="fb"><input type="radio" name="g" value="" checked><span>Todos <b>{len(TODAS)}</b></span></label>
  {botones}
</div>

<div id="lista">{tarjetas}</div>
<div class="vacio" id="vacio">Ninguna ficha coincide con la búsqueda.</div>

<footer>
  Fuente: material del fabricante SUPCON y su filial Hobré. Formato de ficha: 8 campos de CONECTA.
  {n_val} fichas tienen material escaso del fabricante: confírmalas antes de ofrecer.
  <br>Otros documentos del proyecto:
  <a href="catalogo_supcon.html">catálogo de material por familia</a> ·
  <a href="perfiles_importador_2025.html">perfiles de importador</a> ·
  <a href="../index_otros.html">estudios de mercado</a>
</footer>
</div>
<script>
  var fichas = Array.prototype.slice.call(document.querySelectorAll('.ficha'));
  var q = document.getElementById('q'), fam = document.getElementById('fam');
  var vacio = document.getElementById('vacio');
  var radios = Array.prototype.slice.call(document.querySelectorAll('input[name=g]'));

  function norm(x) {{
    return (x || '').toLowerCase()
      .replace(/[áàäâ]/g,'a').replace(/[éèëê]/g,'e').replace(/[íìïî]/g,'i')
      .replace(/[óòöô]/g,'o').replace(/[úùüû]/g,'u').replace(/ñ/g,'n')
      .replace(/[^a-z0-9 ]/g,' ').replace(/\\s+/g,' ').trim();
  }}

  function aplicar() {{
    var g = (radios.filter(function(r){{return r.checked;}})[0] || {{}}).value || '';
    var t = norm(q.value);
    var f = fam.value || '';
    var n = 0;
    fichas.forEach(function(c) {{
      var ver = (!g || c.getAttribute('data-grupo') === g)
             && (!f || c.getAttribute('data-fam') === f)
             && (!t || c.getAttribute('data-busca').indexOf(t) !== -1);
      c.style.display = ver ? '' : 'none';
      if (ver) {{ n++; var e = c.querySelector('.num'); if (e) e.textContent = n; }}
    }});
    vacio.style.display = n ? 'none' : 'block';
  }}
  radios.forEach(function(r){{ r.addEventListener('change', aplicar); }});
  q.addEventListener('input', aplicar);
  fam.addEventListener('change', aplicar);
  aplicar();
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"fichas={len(TODAS)} | Lista={n_ok} Usable={n_use} Validar={n_val} | sin battlecard={n_comp}")
