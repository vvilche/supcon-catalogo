#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruye artefactos/plan_accion.html (la LISTA PLANA) con los contactos VALIDADOS.

POR QUÉ SE REHACE
------------------------------------------------------------------------------
El plan_accion.html original era del 14-oct con los 899 contactos SIN validar: al buscar los primeros
salían personas sin LinkedIn y contactos que después se supo que eran de OTRAS empresas (339 ajenos).
Ahora usa `plan_accion_limpio.json` (518 contactos validados), cada uno con su línea y qué ofrecerle.

Es la versión LISTA (plana, con buscador) del mismo dato que `plan_accion_geo.html` da por región e
industria: una sola vista por herramienta.
"""
import json, os, re, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "plan_accion.html")


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v):
    try:
        return f"{v:,}"
    except Exception:
        return "—"


plan = json.load(open(os.path.join(D, "plan_accion_limpio.json"), encoding="utf-8"))["plan"]

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
}


def bloque_emp(p):
    tel = (f'<span class="tel">{esc(p.get("telefono_central",""))}</span>'
           if p.get("telefono_central") else '<span class="notel">sin teléfono</span>')
    filas = ""
    for c in p["contactos"]:
        est = c.get("linkedin_estado", "")
        if est == "se fue":
            li = (f'<a href="{esc(c["linkedin"])}" target="_blank" class="li-sefue">in</a>'
                  f'<span class="aviso-fue">ya no está en la empresa</span>')
        elif est == "sin confirmar":
            li = (f'<a href="{esc(c["linkedin"])}" target="_blank" class="li-dud">in</a>'
                  f'<span class="dud">sin confirmar</span>')
        elif c.get("linkedin"):
            li = f'<a href="{esc(c["linkedin"])}" target="_blank">in</a>'
        else:
            li = '<span class="noli">sin LinkedIn</span>'
        badge = ('<span class="bg">fuente</span>' if "garant" in c.get("tipo", "")
                 else '<span class="bl">LI</span>')
        gt = (f"Hola, llamo de CONECTA. Busco a {c['nombre']}, {c['cargo']}, por "
              f"{p['empresa'].title()}. Trabajamos instrumentación, válvulas y control: "
              f"{c.get('que_ofrecer','')}. ¿Me puede derivar con él o dejarme un correo?")
        filas += (f'<div class="ct">'
                  f'<div class="l1"><span class="nm">{esc(c["nombre"])}</span>'
                  f'<span class="cg">{esc(c["cargo"][:60])}</span>{badge} {li}</div>'
                  f'<div class="l2"><span class="lin">{esc(c.get("linea") or "—")}</span>'
                  f'<span class="ofr">{esc(c.get("que_ofrecer") or "")}</span>'
                  f'<button class="cp" data-g="{esc(gt)}" onclick="copiar(this)">guion</button></div>'
                  f'</div>')
    idx = (p["empresa"] + " " + (p.get("region") or "") + " " + (p.get("industria") or "")).lower()
    for c in p["contactos"]:
        idx += " " + (c.get("nombre") or "").lower() + " " + (c.get("cargo") or "").lower()
        idx += " " + (c.get("linea") or "").lower() + " " + (c.get("que_ofrecer") or "").lower()
    for k, a in ALIAS.items():
        if k in p["empresa"].lower():
            idx += " " + a
    return f'''<div class="emp" data-b="{esc(idx)}">
      <div class="eh"><b>{esc(p["empresa"])}</b>
        <span class="com">{esc(p.get("region") or "—")}</span>
        <span class="ind">{esc(p.get("industria") or "—")}</span>
        <span class="nct">{len(p["contactos"])} contactos</span>{tel}</div>
      <div class="cts">{filas}</div></div>'''


plan_ord = sorted(plan, key=lambda p: -(p.get("dolor_t") or 0))
emps_html = "".join(bloque_emp(p) for p in plan_ord)

_lineas = collections.Counter(c.get("linea") or "—" for p in plan for c in p["contactos"])
chips = "".join(f'<button class="chip" data-l="{esc(k)}" onclick="porLinea(this)">{esc(k)}<b>{v}</b></button>'
                for k, v in _lineas.most_common())
n_ct = sum(len(p["contactos"]) for p in plan)
con_li = sum(1 for p in plan for c in p["contactos"] if c.get("linkedin"))

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Plan de acción: a quién llamar — {n(n_ct)} contactos validados</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;line-height:1.55;padding:22px 16px 70px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:25px;font-weight:680;letter-spacing:-.4px;margin-bottom:4px}}
.sub0{{color:var(--mu);font-size:13.5px;margin-bottom:16px;max-width:980px}}
.kpis{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:9px 14px;font-size:11.5px;color:var(--mu)}}
.kpis b{{display:block;font-size:19px;font-weight:700;color:var(--tx)}}
.buscar{{width:100%;padding:10px 14px;border:1px solid var(--bd);border-radius:9px;font-size:14px;margin-bottom:10px;background:var(--cd)}}
.chips{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}}
.chip{{background:var(--cd);border:1px solid var(--bd);border-radius:14px;padding:4px 12px;font-size:12px;cursor:pointer}}
.chip.on{{background:#3730a3;color:#fff;border-color:#3730a3}}
.chip b{{margin-left:5px;opacity:.75;font-size:11px}}
.emp{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:12px 15px;margin-bottom:8px}}
.eh{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;padding-bottom:7px;margin-bottom:6px;border-bottom:1px solid #f3f4f6}}
.eh b{{font-size:14px}}
.com{{font-size:11.5px;color:var(--mu)}}
.ind{{font-size:11px;background:#f3f4f6;border-radius:4px;padding:1px 6px;color:#374151}}
.nct{{font-size:11.5px;font-weight:700;color:var(--vd)}}
.tel{{margin-left:auto;font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--vd)}}
.notel{{margin-left:auto;font-size:11px;color:var(--am);font-style:italic}}
.ct{{padding:6px 0;border-bottom:1px solid #f9fafb}}
.ct:last-child{{border-bottom:none}}
.l1{{display:flex;gap:9px;align-items:baseline;flex-wrap:wrap}}
.l2{{display:flex;gap:9px;align-items:baseline;margin-top:2px;padding-left:2px}}
.nm{{font-weight:600;font-size:13px;min-width:165px}}
.cg{{color:var(--mu);font-size:12.5px;flex:1}}
.lin{{font-size:10.5px;font-weight:700;background:#eef2ff;color:#3730a3;border:1px solid #c7d2fe;border-radius:4px;padding:1px 7px;white-space:nowrap}}
.ofr{{font-size:12px;color:#065f46;flex:1}}
.bg{{font-size:9.5px;background:#f0fdf4;color:#065f46;border:1px solid #bbf7d0;border-radius:4px;padding:0 4px}}
.bl{{font-size:9.5px;background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;border-radius:4px;padding:0 4px}}
.noli{{font-size:10px;color:var(--am);font-style:italic}}
.li-sefue{{color:#b91c1c;text-decoration:line-through}}
.aviso-fue{{font-size:9.5px;background:#fef2f2;color:#b91c1c;border:1px solid #fecaca;border-radius:4px;padding:0 4px}}
.li-dud{{color:#6b7280}}
.dud{{font-size:9.5px;background:#f9fafb;color:#6b7280;border:1px solid #e5e7eb;border-radius:4px;padding:0 4px}}
.cp{{font-size:10.5px;background:#f9fafb;border:1px solid var(--bd);border-radius:5px;padding:1px 7px;cursor:pointer}}
.cp:hover{{background:#111827;color:#fff}}
a{{color:var(--ac);font-size:11.5px;text-decoration:none}}
.aviso{{background:#f0fdf4;border:1px solid #bbf7d0;border-left:4px solid var(--vd);border-radius:9px;padding:12px 16px;margin:14px 0;font-size:13.5px}}
.aviso b{{color:#065f46}}
footer{{margin-top:24px;padding-top:14px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
#msg{{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#111827;color:#fff;padding:8px 18px;border-radius:8px;font-size:13px;display:none}}
</style></head><body><div class="wrap">

<h1>Plan de acción: a quién llamar</h1>
<p class="sub0"><b>{n(n_ct)} contactos validados</b> en {len(plan)} empresas. Cada persona fue
verificada: o viene de una fuente que garantiza la pertenencia (Direcmin, Transparencia), o su
headline de LinkedIn menciona la empresa. <b>Se descartaron 366 contactos del listado anterior</b>:
339 eran de otra empresa, 21 de cargos que no compran y 6 con problemas de registro.</p>

<div class="kpis">
  <div><b>{n(len(plan))}</b>empresas</div>
  <div><b>{n(n_ct)}</b>contactos</div>
  <div><b>{n(con_li)}</b>con LinkedIn</div>
  <div><b>{n(sum(1 for p in plan if p.get("telefono_central")))}</b>con teléfono</div>
</div>

<p class="sub0" style="margin-bottom:6px"><b>Filtrar por línea de producto:</b></p>
<div class="chips">{chips}</div>

<input class="buscar" id="q" placeholder="Buscar empresa, cargo, persona o línea..." oninput="filtrar()">

<div id="lista">{emps_html}</div>

<div class="aviso">
  <b>Cómo leer cada contacto:</b> arriba el nombre y el cargo; <b>abajo la etiqueta azul es la línea
  de producto</b> y el texto verde es <b>qué ofrecerle</b>.
  <span class="bg">fuente</span> = de Direcmin o Transparencia (pertenencia garantizada) ·
  <span class="bl">LI</span> = de LinkedIn validado por headline.
  El botón <b>guion</b> copia la primera frase.
  <br><br>
  <b>Sobre el LinkedIn:</b> de los {n(n_ct)} contactos, <b>{n(n_ct - con_li)} no tienen perfil
  propio</b> (Direcmin publica nombre y cargo, no el link). Se buscaron por nombre: <b>se
  recuperaron 171</b>, y de ésos <b>43 resultaron de personas que YA NO están en la empresa</b>
  (aparecen marcadas en rojo, su headline dice otra compañía). Los que quedan sin link, la vía es el
  <b>teléfono de la central</b> pidiendo a la persona por nombre y cargo.
</div>

<footer>
  Contactos validados en <code>personas_validadas.json</code>.
  <a href="plan_accion_geo.html">la misma lista por región e industria</a> ·
  <a href="inventario_final.html">inventario</a> ·
  <a href="campana_process.html">campaña Process</a> · <a href="../index.html">catálogo</a>.
</footer>
</div>
<div id="msg">guion copiado</div>
<script>
function filtrar(){{
  const raw = (document.getElementById('q').value||'').trim();
  const sinTilde = s => s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
  const palabras = sinTilde(raw).split(/\\s+/).filter(Boolean);
  const hay = (s) => {{
    if(!palabras.length) return true;
    const t = sinTilde(s);
    return palabras.every(w => t.includes(w));
  }};
  document.querySelectorAll('.emp').forEach(e=>{{
    const okEmp = hay(e.dataset.b||'');
    const cts = [...e.querySelectorAll('.ct')];
    const marcas = cts.map(ct => hay(
      (ct.querySelector('.nm')?.textContent||'') + ' ' +
      (ct.querySelector('.cg')?.textContent||'') + ' ' +
      (ct.querySelector('.lin')?.textContent||'') + ' ' +
      (ct.querySelector('.ofr')?.textContent||'')));
    const alguno = marcas.some(Boolean);
    let visibles = 0;
    cts.forEach((ct,i)=>{{
      const mostrar = !palabras.length || !alguno || marcas[i];
      ct.style.display = mostrar ? '' : 'none';
      if(mostrar) visibles++;
    }});
    e.style.display = (okEmp && visibles>0) ? '' : 'none';
  }});
}}
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
print(f"  {len(plan)} empresas | {n_ct} contactos | {con_li} con LinkedIn")
