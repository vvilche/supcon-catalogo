#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSOLIDA las 4 entregas de fichas comerciales en un indice unico navegable,
pensado para VENDEDORES (no para el area tecnica).

Entradas:
  datos/fichas_1_datos.json   (analizadores, extraido de generar_fichas_producto.py)
  datos/fichas_2_datos.json   (SIS, PLC, CCS)
  datos/fichas_3_datos.json   (instrumentacion de campo y analitica)
  datos/fichas_4_datos.json   (software, plataforma, ciberseguridad)

Salida: artefactos/fichas_vendedores.html

CRITERIO DE DISENO (encargo de Victor: "hazlo intuitivo, es material para mis vendedores")
- Una sola vista. Buscar arriba, filtrar por familia, tarjetas que abren y cierran.
- Cada ficha arranca con lo que el vendedor necesita EN LA REUNION:
  que es, para quien, y los 3 argumentos que cierran. Lo tecnico queda plegado abajo.
- Se marca el estado de cada ficha (completa / con datos por completar) porque
  el vendedor necesita saber si puede usarla con cliente sin validar antes.
"""
import os, json, html, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "fichas_vendedores.html")

# ---------------------------------------------------------------- cargar 4 fuentes
def cargar(n):
    p = os.path.join(D, n)
    if not os.path.exists(p): return {}
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, dict) and "fichas" in d: return d["fichas"]
    return d if isinstance(d, dict) else {}

F1 = cargar("fichas_1_datos.json")
F2 = cargar("fichas_2_datos.json")
F3 = cargar("fichas_3_datos.json")
F4 = cargar("fichas_4_datos.json")

def norm(x, grp):
    """Normaliza los dos formatos de clave que usan las entregas."""
    return {
      "grupo": grp,
      "familia": x.get("familia") or x.get("grupo") or grp,
      "descripcion": x.get("descripcion") or x.get("descripción") or "",
      "beneficios": x.get("beneficios") or [],
      "clientes": x.get("clientes_target") or x.get("clientes") or [],
      "competencia": x.get("competencia") or "",
      "argumentos": x.get("argumentos_venta") or [],
      "objeciones": x.get("objeciones") or [],
      "preguntas": x.get("preguntas_tecnicas") or x.get("preguntas") or [],
      "fuente": x.get("fuente") or "",
    }

# mapeo de grupo comercial (el vendedor piensa en soluciones, no en carpetas)
GRUPO = {
  "fichas_1_datos.json": ("Analítica de proceso", "Hobré"),
  "fichas_2_datos.json": ("Control y seguridad", "SIS · PLC · CCS"),
  "fichas_3_datos.json": ("Instrumentación de campo", "Presión · temperatura · caudal · nivel"),
  "fichas_4_datos.json": ("Software y plataforma", "APC · MES · IA industrial · ciberseguridad"),
}
TODAS = []
for src, F in [("fichas_1_datos.json",F1), ("fichas_2_datos.json",F2),
               ("fichas_3_datos.json",F3), ("fichas_4_datos.json",F4)]:
    g, sub = GRUPO[src]
    for nombre, x in F.items():
        if not isinstance(x, dict): continue
        f = norm(x, g)
        f["nombre"] = nombre
        f["sub"] = sub
        f["origen"] = src
        TODAS.append(f)

print(f"fichas consolidadas: {len(TODAS)}")
from collections import Counter
print(Counter(f["grupo"] for f in TODAS))

# ---------------------------------------------------------------- render
def sin_tilde(t):
    """Normaliza para buscar: minusculas, sin tildes, sin puntuacion.

    Un vendedor escribe 'valvula', 'presion', 'analitica' sin tildes. Si el indice
    guarda la forma con tilde, la busqueda devuelve cero y parece que el producto
    no existe en el catalogo.
    """
    t = str(t).lower()
    for a, b in (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")):
        t = t.replace(a, b)
    return " ".join(t.split())

def lista(xs, limite=None):
    xs = [x for x in xs if str(x).strip()]
    if limite: xs = xs[:limite]
    return "".join(f'<li>{html.escape(str(x))}</li>' for x in xs)

def obj_html(objs):
    out = []
    for o in objs:
        if isinstance(o, (list, tuple)) and len(o) >= 2:
            q, r = o[0], o[1]
        elif isinstance(o, dict):
            q, r = o.get("pregunta",""), o.get("respuesta","")
        else:
            continue
        if not str(q).strip() or str(q).upper().startswith("POR COMPLETAR"): continue
        out.append(f'<div class="obj"><div class="q">{html.escape(str(q))}</div>'
                   f'<div class="r">{html.escape(str(r)) if str(r).strip() else "<i>Sin respuesta documentada — validar con fábrica</i>"}</div></div>')
    return "".join(out)

PORC = "POR COMPLETAR"

def porc_count(f):
    """Cuenta campos POR COMPLETAR EXCLUYENDO competencia.

    Por que: en la mayoria de las fichas el campo 'competencia' queda POR COMPLETAR
    porque el material del fabricante no trae battlecard para ese segmento. Eso NO
    hace inutil la ficha para vender: el vendedor igual tiene beneficios, clientes y
    argumentos. Mezclarlo con los faltantes reales marcaba 56% del catalogo como
    'revisar' y le quitaba senal a la alerta.
    """
    crit = 0
    for campo in ("descripcion", "beneficios", "clientes", "argumentos", "preguntas"):
        crit += json.dumps(f.get(campo), ensure_ascii=False).count(PORC)
    crit += json.dumps(f.get("objeciones"), ensure_ascii=False).count(PORC)
    return crit

def comp_pendiente(f):
    return PORC in (f.get("competencia") or "")

def estado(f):
    n = porc_count(f)
    if n == 0:
        return ("OK", "ok", "Completa: se puede usar con cliente sin validar")
    if n <= 4:
        return ("casi", "casi", f"Usable: {n} dato{'s' if n>1 else ''} a confirmar con fabrica")
    return ("revisar", "rev", f"Validar antes de ofrecer: {n} datos sin respaldo en el material")

def tarjeta(f, i):
    etq, cls, titulo_etq = estado(f)
    marca_comp = ('<span class="pend-chip">sin battlecard</span>' if comp_pendiente(f) else '')
    # los 3 primeros argumentos = el pitch de reunion
    pitch = lista(f["argumentos"], 3)
    resto_arg = f["argumentos"][3:]
    return f'''
  <article class="ficha" data-grupo="{html.escape(f["grupo"])}" data-fam="{html.escape(f["familia"])}"
     data-busca="{html.escape(sin_tilde(f["nombre"]+" "+f["familia"]+" "+f["grupo"]+" "+f["sub"]+" "+" ".join(f["argumentos"][:5])+" "+" ".join(f["clientes"][:4])+" "+" ".join(f["preguntas"][:4])))}">
    <header class="fh">
      <div class="fn">
        <span class="num">{i}</span>
        <h3>{html.escape(f["nombre"])}</h3>
        <span class="fam">{html.escape(f["familia"])}</span>
      </div>
      <span class="estado {cls}" title="{html.escape(titulo_etq)}">{'Lista' if etq=='OK' else ('Usable' if etq=='casi' else 'Validar')}</span>
    </header>

    <p class="que">{html.escape(f["descripcion"][:340])}{'…' if len(f["descripcion"])>340 else ''}</p>

    <div class="dos">
      <section>
        <h4>Por qué gana</h4>
        <ul class="arg">{pitch}</ul>
        {f'<details class="mas"><summary>{len(resto_arg)} argumento(s) más</summary><ul class="arg">{lista(resto_arg)}</ul></details>' if resto_arg else ''}
      </section>
      <section>
        <h4>Quién lo compra</h4>
        <ul class="cli">{lista(f["clientes"], 5)}</ul>
      </section>
    </div>

    <details class="prof">
      <summary>Todo el detalle técnico y comercial</summary>
      <div class="grid">
        <div><h4>Descripción completa</h4><p>{html.escape(f["descripcion"])}</p></div>
        <div><h4>Todos los beneficios</h4><ul>{lista(f["beneficios"])}</ul></div>
        <div><h4>Competencia {marca_comp}</h4><p>{html.escape(f["competencia"])}</p></div>
        <div><h4>Argumentos de venta</h4><ul>{lista(f["argumentos"])}</ul></div>
        <div><h4>Preguntas para el cliente</h4><ul>{lista(f["preguntas"])}</ul></div>
        <div><h4>Manejo de objeciones</h4>{obj_html(f["objeciones"]) or "<p>Sin objeciones documentadas.</p>"}</div>
      </div>
      <p class="fuente">Fuente: {html.escape(f["fuente"]) or "material del fabricante"}</p>
    </details>
  </article>'''

tarjetas = "".join(tarjeta(f, i) for i, f in enumerate(TODAS, 1))

grupos = []
for g in ["Analítica de proceso","Control y seguridad","Instrumentación de campo","Software y plataforma"]:
    n = sum(1 for f in TODAS if f["grupo"]==g)
    if n:
        grupos.append(f'<label class="fb"><input type="radio" name="g" value="{html.escape(g)}">'
                      f'<span>{html.escape(g)} <b>{n}</b></span></label>')

familias = sorted(set(f["familia"] for f in TODAS))
fams = "".join(f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in familias)

lista_ok    = sum(1 for f in TODAS if estado(f)[0] == "OK")
lista_casi  = sum(1 for f in TODAS if estado(f)[0] == "casi")
lista_pend  = sum(1 for f in TODAS if estado(f)[0] == "revisar")

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo SUPCON — fichas de venta</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  :root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;
    --am:#d97706;--ams:#fffbeb;--ok:#047857;--oks:#ecfdf5}}
  body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    font-size:15px;line-height:1.6;padding:26px 20px 70px}}
  .wrap{{max-width:1080px;margin:0 auto}}
  .hero{{margin-bottom:20px}}
  .hero h1{{font-size:26px;font-weight:680;letter-spacing:-.5px}}
  .hero p{{color:var(--mu);font-size:14.5px;margin-top:5px;max-width:820px}}
  .leyenda{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:9px;font-size:13px;color:var(--mu)}}
  .kpi{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 22px}}
  .kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:13px}}
  .kpi b{{display:block;font-size:20px;font-weight:700;letter-spacing:-.3px}}
  .barra{{position:sticky;top:0;z-index:20;background:rgba(248,250,252,.96);backdrop-filter:blur(8px);
    border-bottom:1px solid var(--bd);padding:12px 0;margin-bottom:18px;display:flex;gap:9px;flex-wrap:wrap;align-items:center}}
  .barra input[type=search]{{flex:1;min-width:230px;padding:9px 13px;border:1px solid #cbd5e1;border-radius:9px;font-size:14.5px;
    font-family:inherit}}
  .barra select{{padding:9px 11px;border:1px solid #cbd5e1;border-radius:9px;font-size:14px;background:var(--cd);font-family:inherit}}
  .fb{{cursor:pointer}} .fb input{{display:none}}
  .fb span{{display:inline-block;border:1px solid #cbd5e1;background:var(--cd);color:#334155;border-radius:9px;
    padding:8px 12px;font-size:13px}}
  .fb input:checked+span{{background:var(--ac);border-color:var(--ac);color:#fff}}
  .fb b{{opacity:.7}}
  .ficha{{background:var(--cd);border:1px solid var(--bd);border-radius:16px;padding:19px 21px;margin-bottom:13px}}
  .fh{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:9px}}
  .fn{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}}
  .num{{font-size:12px;color:#94a3b8;font-weight:600}}
  .fn h3{{font-size:19px;font-weight:660;letter-spacing:-.3px}}
  .fam{{background:var(--acs);color:var(--ac);border-radius:6px;padding:2px 10px;font-size:12px;font-weight:600}}
  .estado{{font-size:11.5px;border-radius:6px;padding:3px 10px;font-weight:700;text-transform:uppercase;letter-spacing:.3px;
    white-space:nowrap}}
  .estado.ok{{background:var(--oks);color:var(--ok)}}
  .estado.casi{{background:var(--ams);color:var(--am)}}
  .estado.rev{{background:#f1f5f9;color:#475569}}
  .pend-chip{{font-size:10.5px;font-weight:600;color:#94a3b8;background:#f1f5f9;
    border-radius:5px;padding:1px 7px;text-transform:none;letter-spacing:0;margin-left:5px}}
  .que{{font-size:14.5px;color:#334155;margin-bottom:13px}}
  .dos{{display:grid;grid-template-columns:1.35fr 1fr;gap:20px}}
  @media(max-width:760px){{.dos{{grid-template-columns:1fr}}}}
  h4{{font-size:11.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin-bottom:6px}}
  ul{{list-style:none}}
  ul li{{position:relative;padding-left:15px;margin-bottom:4px;font-size:13.8px}}
  ul li:before{{content:"";position:absolute;left:3px;top:8px;width:5px;height:5px;border-radius:50%;background:var(--ac)}}
  .clin li:before{{background:var(--am)}}
  .mas{{margin-top:7px}}
  .mas summary{{font-size:12.5px;color:var(--ac);cursor:pointer;font-weight:600}}
  .prof{{margin-top:14px;border-top:1px solid #f1f5f9;padding-top:11px}}
  .prof summary{{font-size:13px;color:var(--ac);cursor:pointer;font-weight:650}}
  .grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:15px}}
  @media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}
  .grid>div{{background:#fbfdff;border:1px solid var(--bd);border-radius:10px;padding:12px 14px}}
  .grid p{{font-size:13.5px;color:#334155}}
  .obj{{margin-bottom:9px;padding-left:10px;border-left:2px solid var(--bd)}}
  .obj .q{{font-weight:640;font-size:13.3px;color:#334155}}
  .obj .r{{font-size:13.2px;color:var(--mu)}}
  .fuente{{margin-top:12px;font-size:11px;color:#94a3b8;font-family:ui-monospace,monospace}}
  .vacio{{text-align:center;color:var(--mu);padding:40px;font-size:15px}}
  footer{{margin-top:34px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <h1>Catálogo SUPCON — fichas de venta</h1>
    <p>Todo el portafolio en una sola vista. Busca por producto, filtra por línea, abre la ficha y tienes
    qué es, por qué gana y quién lo compra. El detalle técnico está adentro, plegado.</p>
    <p class="leyenda"><span class="estado ok">Lista</span> se puede usar tal cual ·
    <span class="estado casi">Usable</span> sirve para vender, con algún dato a confirmar en fábrica ·
    <span class="estado rev">Validar</span> el material es escaso, confirmar antes de ofrecer</p>
  </div>

  <div class="kpi">
    <div><b>{len(TODAS)}</b>productos</div>
    <div><b>{len(familias)}</b>familias</div>
    <div><b>{lista_ok}</b>completas sin observación</div>
    <div><b>{lista_casi + lista_pend}</b>usables con algún dato a confirmar</div>
  </div>

  <div class="barra">
    <input id="q" type="search" placeholder="Buscar producto, aplicación o cliente… (ej. mineria, valvula, APC) — no importan las tildes">
    <select id="fam"><option value="">Todas las familias</option>{fams}</select>
    <label class="fb"><input type="radio" name="g" value="" checked><span>Todos <b>{len(TODAS)}</b></span></label>
    {''.join(grupos)}
  </div>

  <div id="lista">{tarjetas}</div>
  <div class="vacio" id="vacio" style="display:none">Ninguna ficha coincide con la búsqueda.</div>

  <footer>
    {len(TODAS)} fichas · Fuente: material del fabricante SUPCON y su filial Hobré.
    Las fichas marcadas <b>Revisar</b> tienen datos sin respaldo en el material del fabricante:
    verifícalos antes de usarlas con un cliente.
  </footer>
</div>
<script>
  var lista = document.getElementById('lista');
  var fichas = Array.prototype.slice.call(lista.querySelectorAll('.ficha'));
  var q = document.getElementById('q'), fam = document.getElementById('fam');
  var v = document.getElementById('vacio');
  var radios = Array.prototype.slice.call(document.querySelectorAll('input[name=g]'));

  // la misma normalizacion que el indice: sin tildes, sin signos
  function norm(x) {{
    return (x || '').toLowerCase()
      .replace(/[\u00e1\u00e0\u00e4\u00e2]/g,'a').replace(/[\u00e9\u00e8\u00eb\u00ea]/g,'e')
      .replace(/[\u00ed\u00ec\u00ef\u00ee]/g,'i').replace(/[\u00f3\u00f2\u00f6\u00f4]/g,'o')
      .replace(/[\u00fa\u00f9\u00fc\u00fb]/g,'u').replace(/\u00f1/g,'n')
      .replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim();
  }}

  function aplicar() {{
    var tipo = (radios.filter(function(r){{return r.checked;}})[0] || {{}}).value || '';
    var t = norm(q.value || '');
    var f = fam.value || '';
    var n = 0;
    fichas.forEach(function(c) {{
      var okG = !tipo || c.getAttribute('data-grupo') === tipo;
      var okF = !f || c.getAttribute('data-fam') === f;
      var okQ = !t || c.getAttribute('data-busca').indexOf(t) !== -1;
      var ver = okG && okF && okQ;
      c.style.display = ver ? '' : 'none';
      if (ver) {{ n++; var e = c.querySelector('.num'); if (e) e.textContent = n; }}
    }});
    v.style.display = n ? 'none' : '';
  }}
  radios.forEach(function(r){{ r.addEventListener('change', aplicar); }});
  q.addEventListener('input', aplicar);
  fam.addEventListener('change', aplicar);
  aplicar();
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"\nescrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"listas={lista_ok} | casi={lista_casi} | revisar={lista_pend}")
