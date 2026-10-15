#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/plan_accion_geo.html — la GEO reconstruida con los 533 contactos validados."""
import json, os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "plan_accion_geo.html")

g = json.load(open(os.path.join(D, "plan_geo_limpio.json"), encoding="utf-8"))
sol = json.load(open(os.path.join(D, "personas_validadas.json"), encoding="utf-8"))


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v):
    try:
        return f"{v:,}"
    except Exception:
        return "—"


plan = g["plan"]
tot = g["totales"]

# líneas de producto, para los chips de filtro
import collections as _c
_lineas = _c.Counter(c.get("linea") or "—" for p in plan for c in p["contactos"])
chips_html = "".join(
    f'<button class="chip" data-l="{esc(k)}" onclick="porLinea(this)">{esc(k)}<b>{v}</b></button>'
    for k, v in _lineas.most_common())


def guion(p, c):
    return (f"Hola, llamo de CONECTA. Busco a {c['nombre']}, {c['cargo']}, "
            f"por {p['empresa'].title()}. Trabajamos instrumentación, válvulas y control: "
            f"{c.get('que_ofrecer','')}. ¿Me puede derivar con él o dejarme un correo?")


def bloque_emp(p):
    tel = (f'<span class="tel">{esc(p.get("telefono_central",""))}</span>'
           if p.get("telefono_central") else '<span class="notel">sin teléfono</span>')
    filas = ""
    for c in p["contactos"]:
        li = (f'<a href="{esc(c["linkedin"])}" target="_blank">in</a>' if c.get("linkedin") else "")
        tipo = c.get("tipo", "")
        badge = ('<span class="bg">fuente</span>' if "garant" in tipo
                 else '<span class="bl">LI</span>')
        linea = c.get("linea") or "—"
        ofrecer = c.get("que_ofrecer") or ""
        gt = guion(p, c)
        filas += (f'<div class="ct">'
                  f'<div class="cl1"><span class="nm">{esc(c["nombre"])}</span>'
                  f'<span class="cg">{esc(c["cargo"][:56])}</span>{badge} {li}</div>'
                  f'<div class="cl2"><span class="lin">{esc(linea)}</span>'
                  f'<span class="ofr">{esc(ofrecer)}</span>'
                  f'<button class="cp" data-g="{esc(gt)}" onclick="copiar(this)">guion</button></div>'
                  f'</div>')
    # ALIAS DE BÚSQUEDA: sin esto, buscar "codelco" o "mlp" no encuentra nada porque la razón
    # social es otra ("CORP NACIONAL DEL COBRE DE CHILE", "MINERA LOS PELAMBRES").
    ALIAS = {
        "corp nacional del cobre": "codelco cobre chuquicamata andina teniente salvador",
        "minera los pelambres": "mlp pelambres",
        "minera escondida": "escondida bhp",
        "cia minera del pacifico": "cmp cap acero huachipato cmpc",
        "empresa nacional del petroleo": "enap",
        "empresa nacional de mineria": "enami",
        "soc quimica y minera": "sqm",
        "comp a minera do a in s": "collahuasi",
        "minera spence": "spence",
        "anglo american sur": "anglo",
        "minera cemin": "cemin",
        "minera florida": "yamana gold fields",
    }
    idx = (p["empresa"] + " " + (p.get("region") or "") + " " + (p.get("industria") or "")).lower()
    # el buscador también filtra por CARGO, LÍNEA y "qué ofrecer" de cada contacto
    for c in p["contactos"]:
        idx += " " + (c.get("nombre") or "").lower()
        idx += " " + (c.get("cargo") or "").lower()
        idx += " " + (c.get("linea") or "").lower()
        idx += " " + (c.get("que_ofrecer") or "").lower()
    ne = p["empresa"].lower()
    for k, a in ALIAS.items():
        if k in ne:
            idx += " " + a
    return f'''<div class="emp" data-b="{esc(idx)}">
      <div class="eh"><b>{esc(p["empresa"])}</b>
        <span class="com">{esc(p.get("region") or "—")}</span>
        <span class="ind">{esc(p.get("industria") or "—")}</span>
        <span class="nct">{len(p["contactos"])} contactos</span>{tel}</div>
      <div class="cts">{filas}</div></div>'''


# vistas
def vista(dic, titulo):
    items = sorted(dic.items(), key=lambda x: -x[1]["contactos"])
    tabs, panes = "", ""
    for i, (k, v) in enumerate(items):
        on = " active" if i == 0 else ""
        # OJO: el id lleva el PREFIJO de la vista. Sin él, las dos vistas generan g0..g15 y los ids
        # se REPITEN en el documento: al hacer clic, querySelector('#g0') devuelve siempre el de la
        # primera vista, así que el panel que cambia es el de la vista que no se está mirando
        # (síntoma: "hago clic en la pestaña y no pasa nada").
        pid = f'{titulo}-{i}'
        tabs += (f'<button class="tab{on}" onclick="ver(this,\'{pid}\')">'
                 f'{esc(k)}<span class="tb">{v["contactos"]}</span></button>')
        emps = [p for p in plan if (p.get("region") if titulo == "reg" else p.get("industria")) == k]
        emps.sort(key=lambda p: -len(p["contactos"]))
        panes += (f'<div class="pane{on}" id="{pid}">'
                  + "".join(bloque_emp(p) for p in emps) + '</div>')
    return f'<div class="grupo" data-v="{titulo}">{tabs}</div><div class="panes">{panes}</div>'


HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Plan de acción por región e industria — {n(tot["contactos"])} contactos</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;line-height:1.55;padding:22px 16px 70px}}
.wrap{{max-width:1260px;margin:0 auto}}
h1{{font-size:25px;font-weight:680;letter-spacing:-.4px;margin-bottom:4px}}
.sub0{{color:var(--mu);font-size:13.5px;margin-bottom:16px;max-width:980px}}
.kpis{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:9px 14px;font-size:11.5px;color:var(--mu)}}
.kpis b{{display:block;font-size:19px;font-weight:700;color:var(--tx)}}
.buscar{{width:100%;padding:10px 14px;border:1px solid var(--bd);border-radius:9px;font-size:14px;margin-bottom:12px;background:var(--cd)}}
.vistas{{display:flex;gap:8px;margin-bottom:14px}}
.vista{{background:var(--cd);border:1px solid var(--bd);border-radius:8px;padding:7px 15px;font-size:13px;cursor:pointer;font-weight:600}}
.vista.on{{background:var(--ac);color:#fff;border-color:var(--ac)}}
.grupo{{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:12px}}
.tab{{background:var(--cd);border:1px solid var(--bd);border-radius:7px;padding:5px 11px;font-size:12.5px;cursor:pointer;font-weight:500}}
.tab.on{{background:#111827;color:#fff;border-color:#111827}}
.tb{{display:inline-block;margin-left:6px;font-size:10.5px;opacity:.7}}
/* el JS controla el display de cada pane (filtro + pestaña activa); el CSS solo da la base */
.pane{{display:none}}
.emp{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:12px 15px;margin-bottom:8px}}
.eh{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;padding-bottom:7px;margin-bottom:7px;border-bottom:1px solid #f3f4f6}}
.eh b{{font-size:14px}}
.com{{font-size:11.5px;color:var(--mu)}}
.ind{{font-size:11px;background:#f3f4f6;border-radius:4px;padding:1px 6px;color:#374151}}
.nct{{font-size:11.5px;font-weight:700;color:var(--vd)}}
.tel{{margin-left:auto;font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--vd)}}
.notel{{margin-left:auto;font-size:11px;color:var(--am);font-style:italic}}
.ct{{padding:6px 0;border-bottom:1px solid #f9fafb}}
.ct:last-child{{border-bottom:none}}
.cl1{{display:flex;gap:9px;align-items:baseline;flex-wrap:wrap}}
.cl2{{display:flex;gap:9px;align-items:baseline;margin-top:2px;padding-left:2px}}
.nm{{font-weight:600;font-size:13px;min-width:165px}}
.cg{{color:var(--mu);font-size:12.5px;flex:1}}
.lin{{font-size:10.5px;font-weight:700;background:#eef2ff;color:#3730a3;border:1px solid #c7d2fe;border-radius:4px;padding:1px 7px;white-space:nowrap}}
.ofr{{font-size:12px;color:#065f46;flex:1}}
.chips{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}}
.chip{{background:var(--cd);border:1px solid var(--bd);border-radius:14px;padding:4px 12px;font-size:12px;cursor:pointer}}
.chip.on{{background:#3730a3;color:#fff;border-color:#3730a3}}
.chip b{{margin-left:5px;opacity:.75;font-size:11px}}
.bg{{font-size:9.5px;background:#f0fdf4;color:#065f46;border:1px solid #bbf7d0;border-radius:4px;padding:0 4px}}
.bl{{font-size:9.5px;background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;border-radius:4px;padding:0 4px}}
.cp{{font-size:10.5px;background:#f9fafb;border:1px solid var(--bd);border-radius:5px;padding:1px 7px;cursor:pointer}}
.cp:hover{{background:#111827;color:#fff}}
a{{color:var(--ac);font-size:11.5px;text-decoration:none}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:11px 15px;margin:13px 0;font-size:13px}}
.aviso b{{color:#92400e}}
footer{{margin-top:24px;padding-top:14px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
#msg{{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#111827;color:#fff;padding:8px 18px;border-radius:8px;font-size:13px;display:none}}
</style></head><body><div class="wrap">

<h1>Plan de acción por región e industria</h1>
<p class="sub0"><b>{n(tot["contactos"])} contactos validados</b> en {tot["empresas"]} empresas —
<b>cada uno con la línea que le corresponde y qué ofrecerle</b>. Cada persona fue verificada: o viene
de una fuente que garantiza la pertenencia (Direcmin, Transparencia), o su headline de LinkedIn
menciona la empresa. Se descartaron <b>339 contactos ajenos</b> y 21 de cargos que no compran.</p>

<div class="kpis">
  <div><b>{n(tot["empresas"])}</b>empresas</div>
  <div><b>{n(tot["contactos"])}</b>contactos</div>
  <div><b>{n(tot["con_telefono"])}</b>con teléfono</div>
  <div><b>{tot["regiones"]}</b>regiones</div>
  <div><b>{tot["industrias"]}</b>industrias</div>
</div>

<p class="sub0" style="margin-bottom:6px"><b>Filtrar por línea de producto:</b></p>
<div class="chips">{chips_html}</div>

<div class="vistas">
  <button class="vista on" onclick="cambiar('reg',this)">Por región</button>
  <button class="vista" onclick="cambiar('ind',this)">Por industria</button>
</div>

<input class="buscar" id="q" placeholder="Buscar empresa, cargo, persona o línea (busca en todas las pestañas)..." oninput="filtrar()">

<div id="vreg">{vista(g["por_region"], "reg")}</div>
<div id="vind" style="display:none">{vista(g["por_industria"], "ind")}</div>

<div class="aviso">
  <b>Cómo leer cada contacto:</b> el nombre y el cargo arriba; <b>abajo la etiqueta azul es la línea
  de producto</b> y el texto verde es <b>qué ofrecerle concretamente</b>.
  <span class="bg">fuente</span> = de Direcmin o Transparencia (pertenencia garantizada) ·
  <span class="bl">LI</span> = de LinkedIn con headline validado.
  El botón <b>guion</b> copia la primera frase con el dato real de la empresa.
</div>

<footer>
  Región del RETC (hoja Generador, declaración por faena, región dominante).
  Contactos validados en <code>personas_validadas.json</code>.
  <a href="inventario_final.html">inventario final</a> ·
  <a href="campana_process.html">campaña Process</a> · <a href="../index.html">catálogo</a>.
</footer>
</div>
<div id="msg">guion copiado</div>
<script>
function cambiar(v, el){{
  document.querySelectorAll('.vista').forEach(x=>x.classList.remove('on'));
  el.classList.add('on');
  document.getElementById('vreg').style.display = v==='reg'?'':'none';
  document.getElementById('vind').style.display = v==='ind'?'':'none';
  filtrar();
}}
function ver(el, id){{
  // el grupo de tabs y el contenedor de panes son HERMANOS dentro de la vista
  const grupo = el.closest('.grupo');
  const panes = grupo.nextElementSibling;
  grupo.querySelectorAll('.tab').forEach(t=>t.classList.remove('on'));
  el.classList.add('on');
  // OJO: hay que poner display='block' EXPLÍCITO. Con display='' el pane vuelve al valor del CSS
  // (.pane{{display:none}}) y no se ve nada: la pestaña se marca pero el contenido no aparece
  // (síntoma reportado: "hago clic y no sale nada").
  panes.querySelectorAll('.pane').forEach(p=>{{
    p.classList.remove('active');
    p.style.display = 'none';
  }});
  const p = panes.querySelector('#'+CSS.escape(id));
  if(p){{ p.classList.add('active'); p.style.display = 'block'; }}
  filtrar();
}}
function filtrar(){{
  const raw = (document.getElementById('q').value||'').trim();
  // NORMALIZAR ACENTOS: "analitica" debe encontrar "Analítica".
  const sinTilde = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const palabras = sinTilde(raw).split(/\s+/).filter(Boolean);
  const hay = (s) => {{
    if(!palabras.length) return true;
    const t = sinTilde(s);
    return palabras.every(w => t.includes(w));
  }};

  document.querySelectorAll('.panes').forEach(cont=>{{
    cont.querySelectorAll('.pane').forEach(p=>{{
      let visibles = 0;
      p.querySelectorAll('.emp').forEach(e=>{{
        // 1) la empresa pasa el filtro? (data-b trae empresa, ALIAS, región, industria, cargos...)
        if(!hay(e.dataset.b||'')) {{ e.style.display='none'; return; }}
        // 2) dentro, mostrar los contactos que matchean por nombre/cargo/línea.
        //    Si NINGUNO matchea (búsqueda por empresa o región), mostrar todos.
        const cts = [...e.querySelectorAll('.ct')];
        const marcas = cts.map(ct => hay(
          (ct.querySelector('.nm')?.textContent||'') + ' ' +
          (ct.querySelector('.cg')?.textContent||'') + ' ' +
          (ct.querySelector('.lin')?.textContent||'') + ' ' +
          (ct.querySelector('.ofr')?.textContent||'')));
        const alguno = marcas.some(Boolean);
        cts.forEach((ct, i) => {{
          const mostrar = !palabras.length || !alguno || marcas[i];
          ct.style.display = mostrar ? '' : 'none';
          if(mostrar) visibles++;
        }});
        e.style.display = visibles > 0 ? '' : 'none';
      }});
      // sin búsqueda: solo el panel activo. con búsqueda: los paneles con resultados.
      p.style.display = (palabras.length ? visibles > 0 : p.classList.contains('active')) ? 'block' : 'none';
    }});
  }});
}}
// al cargar, mostrar el panel activo de cada vista (sin esto la pagina aparece VACIA hasta
// que el usuario hace clic en una pestana). Va en IIFE sin esperar DOMContentLoaded: el script
// esta al final del body, asi que el DOM ya existe y el evento ya paso.
(function init(){{
  document.querySelectorAll('.panes .pane.active').forEach(p => p.style.display = 'block');
  filtrar();
}})();
// FILTRO POR LÍNEA: marca el chip y escribe la línea en el buscador (que ya indexa la línea de
// cada contacto). Se usa el mismo camino que el texto libre para no duplicar la lógica.
function porLinea(el){{
  const on = el.classList.contains('on');
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('on'));
  if(on){{ document.getElementById('q').value=''; filtrar(); return; }}
  el.classList.add('on');
  document.getElementById('q').value = el.dataset.l;
  filtrar();
}}
function copiar(b){{
  navigator.clipboard.writeText(b.dataset.g);
  const m = document.getElementById('msg');
  m.style.display='block'; setTimeout(()=>m.style.display='none', 1400);
}}
</script></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {tot['empresas']} empresas | {tot['contactos']} contactos | {tot['regiones']} regiones | {tot['industrias']} industrias")
