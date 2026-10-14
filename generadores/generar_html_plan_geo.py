#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/plan_accion_geo.html — el plan de acción por REGIÓN y por INDUSTRIA.

Dos vistas conmutables (región / industria), pestañas por grupo, buscador, y por empresa: a quién
llamar, el número, qué ofrecerle y el guion listo para copiar.
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "plan_accion_geo.html")

g = json.load(open(os.path.join(D, "plan_accion_geo.json"), encoding="utf-8"))
REG, IND, T = g["por_region"], g["por_industria"], g["totales"]
TIPOS = g.get("por_tipo", {})


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


def guion(p, c):
    partes = []
    if p["usd_cotizado"]:
        partes.append(f"ya les cotizamos US${n(p['usd_cotizado'])}")
    if p["dolor_t"]:
        partes.append(f"declaran {n(p['dolor_t'],0)} t de residuos peligrosos al RETC")
    dato = ("; ".join(partes)) if partes else "están en nuestro mapa de cuentas"
    return (f"Hola, llamo de CONECTA por {p['empresa']}. Sé que {dato}. "
            f"Busco a {c['nombre']}, {c['cargo']}, para ver si les sirve {c['que_ofrecer']}.")


def bloque_emp(p):
    tel = (f'<span class="tel">{esc(p["telefono_central"])}</span>'
           if p["telefono_central"] else '<span class="notel">sin teléfono → LinkedIn</span>')
    monto = (f'US${n(p["usd_cotizado"])} cotizado' if p["usd_cotizado"] else "nunca cotizado")
    dolor = f'{n(p["dolor_t"],0)} t resp. peligrosos' if p["dolor_t"] else "sin dolor declarado"
    comunas = ", ".join(p.get("comunas") or [])[:52] or "—"
    ind = p.get("industria", "")
    filas = ""
    for c in p["contactos"]:
        li = (f'<a href="{esc(c["linkedin"])}" target="_blank">in</a>' if c["linkedin"] else "")
        gt = guion(p, c)
        filas += (f'<div class="ct"><span class="nm">{esc(c["nombre"])}</span>'
                  f'<span class="cg">{esc(c["cargo"])[:56]}</span>'
                  f'<span class="ofr">{esc(c["linea"])}</span> {li}'
                  f'<button class="cp" data-g="{esc(gt)}" onclick="copiar(this)">guion</button></div>')
    # OJO: el índice de búsqueda tiene que incluir los ALIAS, o buscar "codelco" (cuando la razón
    # social dice "CORP NACIONAL DEL COBRE DE CHILE") o "MLP" no encuentra nada.
    ALIAS_BUSQUEDA = {
        "corp nacional del cobre": "codelco cobre chuquicamata andina el teniente salvador",
        "minera los pelambres": "mlp pelambres",
        "cia minera del pacifico": "cmp cap acero huachipato pacifico cmpc",
        "comp a minera del pacifico": "cmp cap acero huachipato pacifico cmpc",
        "cartulinas cmpc": "cmpc cartulinas",
        "celulosa arauco": "arauco celulosa",
        "cmpc": "cmpc cartulinas",
        "cia contractual minera candelaria": "candelaria",
        "minera escondida": "escondida bhp",
        "scm minera lumina copper": "caserones lumina",
        "soc quimica y minera": "sqm quimica",
        "empresa nacional del petroleo": "enap",
        "compa a minera do a in s de collahuasi": "collahuasi",
        "minera centinela": "centinela",
        "minera spence": "spence",
        "minera teck": "teck",
        "anglo american sur": "anglo",
        "minera meridian": "meridian",
        "comp a minera mantos": "mantos",
    }
    idx = (p["empresa"] + " " + comunas + " " + ind + " " +
           " ".join(p.get("lineas_empresa", [])) + " " + p.get("sigla", "")).lower()
    n_emp = p["empresa"].lower()
    for k, alias in ALIAS_BUSQUEDA.items():
        if k in n_emp:
            idx += " " + alias
    return f'''
    <div class="emp" data-b="{esc(idx)}">
      <div class="eh">
        <b>{esc(p["empresa"])}</b>
        <span class="com">{esc(p.get("comuna") or "—")}</span>
        <span class="ind">{esc(ind)}</span>
        <span class="met">{esc(monto)} · {esc(dolor)}</span>
        <span class="num">{tel}</span>
      </div>
      <div class="cm">{esc(comunas)}</div>
      <div class="cts">{filas}</div>
    </div>'''


def bloque_vista(datos, pref):
    """Pestañas + paneles para un agrupamiento."""
    orden = sorted(datos.items(), key=lambda kv: -kv[1]["contactos"])
    tabs, panes = "", ""
    for i, (nom, v) in enumerate(orden):
        rid = f"{pref}{i}"
        activo = "active" if i == 0 else ""
        tabs += (f'<button class="tab {activo}" data-t="{rid}" onclick="ver(this)">'
                 f'{esc(nom)} <b>{v["contactos"]}</b></button>')
        emps = "".join(bloque_emp(p) for p in
                       sorted(v["empresas"], key=lambda x: -(x["usd_cotizado"] or 0)))
        panes += f'<div class="pane {activo}" id="{rid}">{emps}</div>'
    return tabs, panes


tabs_r, pane_r = bloque_vista(REG, "r")
tabs_i, pane_i = bloque_vista(IND, "i")

tipos_html = " · ".join(
    f'{esc(t)}: <b>{v["n_empresas"]}</b> empresas / {v["contactos"]} contactos'
    for t, v in TIPOS.items())

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Plan de acción por región e industria</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:16px;max-width:970px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:16px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.vistas{{display:flex;gap:7px;margin-bottom:14px}}
.vista{{background:#fff;border:1px solid var(--bd);border-radius:9px;padding:8px 16px;font-size:13.5px;font-weight:600;cursor:pointer;font-family:inherit;color:#374151}}
.vista.on{{background:#111827;color:#fff;border-color:#111827}}
.barra input{{width:100%;padding:9px 13px;border:1px solid var(--bd);border-radius:9px;font-size:14px;font-family:inherit;margin-bottom:12px}}
.barra input:focus{{outline:none;border-color:var(--ac)}}
.tabs{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}}
.tab{{background:var(--cd);border:1px solid var(--bd);border-radius:8px;padding:7px 13px;font-size:13px;cursor:pointer;font-family:inherit;color:#374151}}
.tab:hover{{border-color:var(--ac)}}
.tab.active{{background:var(--ac);color:#fff;border-color:var(--ac)}}
.tab b{{font-size:11px;opacity:.75;margin-left:4px}}
.pane{{display:none}} .pane.active{{display:block}}
.grupo{{display:none}} .grupo.on{{display:block}}
.emp{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:12px 15px;margin-bottom:9px}}
.eh{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}}
.eh b{{font-size:15px}}
.com{{font-size:12px;background:#eef2ff;color:#3730a3;border-radius:5px;padding:1px 8px;font-weight:600}}
.ind{{font-size:11px;background:#f3f4f6;color:#4b5563;border-radius:5px;padding:1px 7px}}
.met{{font-size:12px;color:var(--mu);margin-left:auto}}
.tel{{font-family:ui-monospace,Menlo,monospace;font-size:13px;font-weight:700;color:var(--vd);background:#f0fdf4;border-radius:6px;padding:2px 9px}}
.notel{{font-size:11.5px;color:#b45309;background:#fffbeb;border-radius:6px;padding:2px 8px}}
.cm{{font-size:11.5px;color:var(--mu);margin:3px 0 6px}}
.cts{{border-top:1px solid #f3f4f6;padding-top:6px}}
.ct{{font-size:12.5px;padding:3px 0;display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}}
.nm{{font-weight:600;min-width:170px}}
.cg{{color:#4b5563;flex:1;min-width:150px}}
.ofr{{font-size:11px;background:#eff6ff;color:#1e40af;border-radius:4px;padding:1px 7px;font-weight:600;white-space:nowrap}}
.cp{{font-size:10.5px;background:#1d4ed8;color:#fff;border:none;border-radius:5px;padding:2px 8px;cursor:pointer;font-weight:600}}
.cp:hover{{background:#1e40af}}
a{{color:var(--ac);text-decoration:none;font-size:12px}} a:hover{{text-decoration:underline}}
footer{{margin-top:26px;padding-top:14px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Plan de acción por región e industria</h1>
<p class="sub0">Las <b>{T['empresas']} empresas</b> con decisores identificados, agrupadas de las
dos formas que sirven para salir a vender: <b>por región y ciudad</b> (para armar la gira) y
<b>por industria</b> (para hablar el idioma del rubro). Dentro de cada grupo: a quién llamar, el
número de la central, qué ofrecerle y el guion listo.</p>

<div class="kpis">
  <div><b>{T['regiones']}</b>regiones</div>
  <div><b>{T['industrias']}</b>industrias</div>
  <div><b>{T['empresas']}</b>empresas</div>
  <div><b>{T['contactos']}</b>contactos</div>
</div>

<div class="vistas">
  <button class="vista on" data-v="reg" onclick="cambiarVista(this)">Por región y ciudad</button>
  <button class="vista" data-v="ind" onclick="cambiarVista(this)">Por industria</button>
</div>

<div class="barra">
  <input id="q" placeholder="Filtrar por empresa, ciudad o línea…" oninput="filtrar()">
</div>

<div class="grupo on" id="g-reg">
  <div class="tabs">{tabs_r}</div>
  {pane_r}
</div>
<div class="grupo" id="g-ind">
  <div class="tabs">{tabs_i}</div>
  {pane_i}
</div>

<footer>
  Tipo de empresa: {tipos_html} ·
  Fuentes: RETC MMA (región/comuna/rubro) · Direcmin · Transparencia Ley 20.285 · LinkedIn ·
  <a href="plan_accion.html">plan completo</a> ·
  <a href="cliente_producto_persona.html">vista empresa→producto→persona</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div>
<script>
function cambiarVista(b){{
  document.querySelectorAll('.vista').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  document.querySelectorAll('.grupo').forEach(g=>g.classList.remove('on'));
  document.getElementById('g-'+b.dataset.v).classList.add('on');
  filtrar();
}}
function ver(b){{
  const grupo=b.closest('.grupo');
  grupo.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  grupo.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
  b.classList.add('active');
  grupo.querySelector('#'+b.dataset.t).classList.add('active');
  filtrar();
}}
function filtrar(){{
  const q=(document.getElementById('q').value||'').toLowerCase().trim();
  const grupos=document.querySelectorAll('.grupo.on');
  grupos.forEach(grupo=>{{
    if(!q){{
      // sin filtro: se respeta la pestaña elegida
      grupo.querySelectorAll('.pane').forEach(p=>{{
        const on=p.classList.contains('active');
        p.style.display='';
        p.querySelectorAll('.emp').forEach(e=>e.style.display='');
      }});
      grupo.querySelectorAll('.tab').forEach(t=>t.style.outline='');
      return;
    }}
    // CON filtro: busca en TODAS las pestañas y marca dónde hay resultados
    let total=0;
    grupo.querySelectorAll('.pane').forEach(p=>{{
      let n=0;
      p.querySelectorAll('.emp').forEach(e=>{{
        const hit=(e.dataset.b||'').includes(q);
        e.style.display=hit?'':'none';
        if(hit) n++;
      }});
      p.dataset.hits=n;
      total+=n;
      // mostrar el panel si tiene resultados
      p.style.display=n?'':'none';
    }});
    grupo.querySelectorAll('.tab').forEach(t=>{{
      const p=grupo.querySelector('#'+t.dataset.t);
      const n=p?(parseInt(p.dataset.hits)||0):0;
      t.style.outline = n ? '2px solid #047857' : '';
      t.style.opacity = n ? '1' : '.45';
    }});
    grupo.dataset.total=total;
  }});
}}
function copiar(b){{
  navigator.clipboard.writeText(b.getAttribute('data-g')).then(()=>{{
    const t=b.textContent; b.textContent='ok'; b.style.background='#047857';
    setTimeout(()=>{{b.textContent=t; b.style.background='#1d4ed8';}},1000);
  }});
}}
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {T['regiones']} regiones | {T['industrias']} industrias | {T['empresas']} empresas")
print("  vista REGIÓN:")
for r, v in sorted(REG.items(), key=lambda kv: -kv[1]["contactos"])[:6]:
    print(f"    {r[:44]:46s} {len(v['empresas']):>3} emp · {v['contactos']:>3} cont")
print("  vista INDUSTRIA:")
for ind, v in sorted(IND.items(), key=lambda kv: -kv[1]["contactos"]):
    print(f"    {ind[:40]:42s} {len(v['empresas']):>3} emp · {v['contactos']:>3} cont")
