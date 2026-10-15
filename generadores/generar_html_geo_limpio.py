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
        gt = guion(p, c)
        filas += (f'<div class="ct"><span class="nm">{esc(c["nombre"])}</span>'
                  f'<span class="cg">{esc(c["cargo"][:50])}</span>{badge} {li}'
                  f'<button class="cp" data-g="{esc(gt)}" onclick="copiar(this)">guion</button></div>')
    return f'''<div class="emp">
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
        tabs += (f'<button class="tab{on}" onclick="ver(this,\'g{i}\')">'
                 f'{esc(k)}<span class="tb">{v["contactos"]}</span></button>')
        emps = [p for p in plan if (p.get("region") if titulo == "reg" else p.get("industria")) == k]
        emps.sort(key=lambda p: -len(p["contactos"]))
        panes += (f'<div class="pane{on}" id="g{i}">'
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
.pane{{display:none}} .pane.active{{display:block}}
.emp{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:12px 15px;margin-bottom:8px}}
.eh{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;padding-bottom:7px;margin-bottom:7px;border-bottom:1px solid #f3f4f6}}
.eh b{{font-size:14px}}
.com{{font-size:11.5px;color:var(--mu)}}
.ind{{font-size:11px;background:#f3f4f6;border-radius:4px;padding:1px 6px;color:#374151}}
.nct{{font-size:11.5px;font-weight:700;color:var(--vd)}}
.tel{{margin-left:auto;font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--vd)}}
.notel{{margin-left:auto;font-size:11px;color:var(--am);font-style:italic}}
.ct{{display:flex;gap:9px;align-items:baseline;padding:3px 0;font-size:13px;flex-wrap:wrap}}
.nm{{font-weight:600;min-width:170px}}
.cg{{color:var(--mu);flex:1;font-size:12.5px}}
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
<p class="sub0"><b>{n(tot["contactos"])} contactos validados</b> en {tot["empresas"]} empresas.
Cada persona fue verificada: o viene de una fuente que garantiza la pertenencia (Direcmin,
Transparencia), o su headline de LinkedIn menciona la empresa. Se descartaron <b>339 contactos
ajenos</b> y 21 de cargos que no compran.</p>

<div class="kpis">
  <div><b>{n(tot["empresas"])}</b>empresas</div>
  <div><b>{n(tot["contactos"])}</b>contactos</div>
  <div><b>{n(tot["con_telefono"])}</b>con teléfono</div>
  <div><b>{tot["regiones"]}</b>regiones</div>
  <div><b>{tot["industrias"]}</b>industrias</div>
</div>

<div class="vistas">
  <button class="vista on" onclick="cambiar('reg',this)">Por región</button>
  <button class="vista" onclick="cambiar('ind',this)">Por industria</button>
</div>

<input class="buscar" id="q" placeholder="Buscar empresa, cargo o persona (busca en todas las pestañas)..." oninput="filtrar()">

<div id="vreg">{vista(g["por_region"], "reg")}</div>
<div id="vind" style="display:none">{vista(g["por_industria"], "ind")}</div>

<div class="aviso">
  <b>Las etiquetas de cada contacto:</b> <span class="bg">fuente</span> = viene de Direcmin o
  Transparencia (pertenencia garantizada por la fuente) · <span class="bl">LI</span> = de LinkedIn,
  con el headline validado. El botón <b>guion</b> copia la primera frase con el dato real de la empresa.
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
  const grupo = el.parentElement;
  grupo.querySelectorAll('.tab').forEach(t=>t.classList.remove('on'));
  el.classList.add('on');
  const panes = grupo.nextElementSibling;
  panes.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
  const p = panes.querySelector('#'+id);
  if(p) p.classList.add('active');
  filtrar();
}}
function filtrar(){{
  const q = (document.getElementById('q').value||'').toLowerCase().trim();
  document.querySelectorAll('.panes').forEach(cont=>{{
    cont.querySelectorAll('.pane').forEach(p=>{{
      let hits = 0;
      p.querySelectorAll('.emp').forEach(e=>{{
        const ok = !q || e.textContent.toLowerCase().includes(q);
        e.style.display = ok ? '' : 'none';
        if(ok) hits++;
      }});
      if(q){{
        p.style.display = hits ? '' : 'none';
      }} else {{
        p.style.display = p.classList.contains('active') ? '' : 'none';
      }}
    }});
  }});
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
