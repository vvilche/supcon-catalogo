#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/perfiles_importador_2025.html — perfiles de importador de
instrumentacion y automatizacion en Chile 2025, a partir del registro DIN de Aduanas.

El registro no trae nombre ni RUT (Ley 20.285), pero si un ID estable por empresa.
Los perfiles describen CONDUCTA (que importa, cuanto, de quien, con que regularidad),
no identidad. Eso es lo que sirve para decidir canal.

Entrada:  datos/perfiles_importador_2025.json
Salida:   artefactos/perfiles_importador_2025.html
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "perfiles_importador_2025.html")

d = json.load(open(os.path.join(D, "perfiles_importador_2025.json"), encoding="utf-8"))
P = d["perfiles"]
por_tipo = d["por_tipo"]

# codigos de pais (ISO numerico) mas frecuentes, para leer los origenes
PAIS = {"336":"Alemania","563":"China","505":"EE.UU.","549":"India","508":"Japón","512":"Italia",
 "225":"Francia","317":"Corea del Sur","220":"España","226":"Reino Unido","528":"Países Bajos",
 "511":"Canadá","510":"Taiwán","513":"Bélgica","559":"Malasia","412":"México","301":"Brasil",
 "204":"Argentina","484":"Suecia","223":"Finlandia","206":"Dinamarca","222":"Suiza"}

# comunas de Santiago (codigo -> nombre), las mas frecuentes en el rubro
COMUNA = {"13114":"Las Condes","13123":"Santiago Centro","13101":"Santiago","13119":"Providencia",
 "13122":"Vitacura","13115":"Lo Barnechea","13110":"Ñuñoa","13124":"Quinta Normal",
 "13126":"Pudahuel","13120":"Macul","13104":"Conchalí","13111":"Quilicura","13109":"Renca",
 "13125":"Cerro Navia","13108":"Estación Central","13116":"Maipú","13105":"La Cisterna",
 "05101":"Valparaíso","05109":"Viña del Mar","08101":"Concepción","02101":"Antofagasta",
 "03301":"Copiapó","04101":"La Serena","06301":"Rancagua","07101":"Talca","09101":"Temuco",
 "10101":"Puerto Montt","01101":"Iquique","12201":"Punta Arenas"}
def comuna(c):
    c = (c or "").strip()
    if not c: return "sin dato"
    return COMUNA.get(c, "cód. "+c)

def usd(v):
    if v >= 1e6: return f"US${v/1e6:,.2f}M"
    if v >= 1e3: return f"US${v/1e3:,.0f}K"
    return f"US${v:,.0f}"

COLOR = {"ESPECIALISTA en instrumentación":"#047857",
 "INTEGRADOR / distribuidor técnico":"#2563eb",
 "IMPORTADOR GRANDE multirrubro":"#d97706",
 "COMPRA MENOR":"#64748b"}

def barra(pct, color="#2563eb"):
    pct = max(0.0, min(100.0, float(pct)))
    return (f'<div class="bar"><div class="fill" style="width:{pct:.1f}%;background:{color}"></div></div>')

def filas_perfil(p, i):
    col = COLOR.get(p["tipo"], "#64748b")
    marcas = ", ".join(p["marcas"][:6]) or "sin marca identificada"
    origenes = ", ".join(PAIS.get(x, "cód. "+x) or "" for x in p["paises"][:4])
    fams = "".join(
      f'<li><span>{html.escape(f)}</span><b>{usd(v)}</b></li>' for f, v in p["familias"][:5])
    return f'''
    <div class="perf" data-tipo="{html.escape(p["tipo"])}" data-txt="{html.escape((p["id"]+" "+p["tipo"]+" "+" ".join(p["marcas"])+" "+p["fam_principal"]).lower())}">
      <div class="ph">
        <span class="rank">#{i}</span>
        <span class="pid">Importador ID {html.escape(p["id"])}</span>
        <span class="tag" style="border-color:{col};color:{col}">{html.escape(p["tipo"])}</span>
        <span class="vol">{usd(p["instru_usd"])}</span>
      </div>
      <div class="prow">
        <div class="cell"><span class="k">Volumen del rubro</span><b>{usd(p["instru_usd"])}</b>
          <span class="sub">{p["instru_items"]:,} ítems</span></div>
        <div class="cell"><span class="k">Importación total</span><b>{usd(p["total_usd"])}</b>
          <span class="sub">{p["items_totales"]:,} ítems en total</span></div>
        <div class="cell"><span class="k">Peso del rubro</span><b>{p["share_pct"]}%</b>
          {barra(p["share_pct"], col)}</div>
        <div class="cell"><span class="k">Regularidad</span><b>{p["meses_activos"]}/12</b>
          <span class="sub">meses con importación</span></div>
        <div class="cell"><span class="k">Marcas distintas</span><b>{p["n_marcas"]}</b>
          <span class="sub">en el rubro</span></div>
        <div class="cell"><span class="k">Comuna</span><b>{html.escape(comuna(p["comuna"]))}</b>
          <span class="sub">{html.escape(", ".join(p["rubros"][:2]))}</span></div>
      </div>
      <div class="pfoot">
        <div class="fam"><span class="k">Familia principal</span>
          <span class="chip">{html.escape(p["fam_principal"])}</span></div>
        <div class="fam"><span class="k">Origen</span> {html.escape(origenes or "sin dato")}</div>
        <div class="marcas"><span class="k">Marcas</span> {html.escape(marcas)}</div>
      </div>
      <details>
        <summary>Ver desglose por familia de producto</summary>
        <ul class="flist">{fams}</ul>
      </details>
    </div>'''

tarjetas = "".join(filas_perfil(p, i) for i, p in enumerate(P[:60], 1))

tipos_html = "".join(
  f'<label class="fbtn"><input type="radio" name="tipo" value="{html.escape(t)}">'
  f'<span>{html.escape(t)} <b>{v["n"]}</b></span></label>'
  for t, v in sorted(por_tipo.items(), key=lambda x: -x[1]["cif"]))

tot_instru = d["total_instrumentacion_usd"]
tot_merc = d["total_importado_usd"]

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Perfiles de importador — instrumentación y automatización Chile 2025</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#f8fafc; color:#0f172a;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    font-size:15px; line-height:1.55; }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:34px 20px 70px; }}
  h1 {{ font-size:27px; margin:0 0 6px; letter-spacing:-.02em; }}
  .sub {{ color:#64748b; margin:0 0 26px; font-size:14.5px; }}
  .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; margin-bottom:28px; }}
  .stat {{ background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:15px 17px; }}
  .stat .n {{ font-size:23px; font-weight:700; letter-spacing:-.02em; display:block; }}
  .stat .l {{ font-size:12.5px; color:#64748b; text-transform:uppercase; letter-spacing:.04em; }}
  .aviso {{ background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #d97706;
    border-radius:8px; padding:14px 17px; margin-bottom:26px; font-size:14px; }}
  .aviso b {{ color:#92400e; }}
  h2 {{ font-size:18px; margin:34px 0 12px; letter-spacing:-.01em; }}
  .fbar {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; }}
  .fbtn {{ cursor:pointer; }}
  .fbtn input {{ display:none; }}
  .fbtn span {{ display:inline-block; border:1px solid #cbd5e1; background:#fff; color:#334155;
    border-radius:6px; padding:6px 11px; font-size:13px; }}
  .fbtn input:checked + span {{ background:#2563eb; border-color:#2563eb; color:#fff; }}
  .fbtn b {{ font-weight:600; opacity:.75; }}
  .perf {{ background:#fff; border:1px solid #e2e8f0; border-radius:11px;
    padding:16px 18px; margin-bottom:12px; }}
  .ph {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding-bottom:11px;
    border-bottom:1px solid #f1f5f9; }}
  .rank {{ font-size:12.5px; color:#94a3b8; font-weight:600; min-width:30px; }}
  .pid {{ font-weight:700; font-size:15px; letter-spacing:-.01em; }}
  .tag {{ font-size:11.5px; border:1px solid; border-radius:5px; padding:2px 8px;
    font-weight:600; text-transform:uppercase; letter-spacing:.03em; }}
  .vol {{ margin-left:auto; font-weight:700; font-size:16px; letter-spacing:-.02em; }}
  .prow {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
    gap:12px; padding:13px 0 4px; }}
  .cell {{ display:flex; flex-direction:column; gap:2px; }}
  .k {{ font-size:11.5px; color:#94a3b8; text-transform:uppercase; letter-spacing:.04em; }}
  .cell b {{ font-size:16px; font-weight:700; letter-spacing:-.02em; }}
  .sub2, .cell .sub {{ font-size:12px; color:#64748b; }}
  .bar {{ height:5px; background:#f1f5f9; border-radius:3px; overflow:hidden; margin-top:5px; }}
  .fill {{ height:100%; border-radius:3px; }}
  .pfoot {{ display:flex; flex-wrap:wrap; gap:16px; padding-top:11px; margin-top:9px;
    border-top:1px solid #f1f5f9; font-size:13.5px; }}
  .fam, .marcas {{ display:flex; align-items:center; gap:7px; }}
  .marcas {{ flex:1 1 100%; color:#475569; }}
  .chip {{ background:#f1f5f9; border-radius:5px; padding:2px 9px; font-size:12.5px;
    font-weight:600; color:#334155; }}
  details {{ margin-top:11px; }}
  summary {{ cursor:pointer; font-size:13px; color:#2563eb; font-weight:600; }}
  .flist {{ list-style:none; margin:9px 0 0; padding:0; }}
  .flist li {{ display:flex; justify-content:space-between; padding:5px 0;
    border-bottom:1px solid #f8fafc; font-size:13.5px; }}
  .flist b {{ font-variant-numeric:tabular-nums; }}
  footer {{ margin-top:42px; padding-top:20px; border-top:1px solid #e2e8f0;
    font-size:13px; color:#64748b; }}
  footer code {{ background:#f1f5f9; padding:1px 6px; border-radius:4px; font-size:12.5px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Perfiles de importador — instrumentación y automatización</h1>
  <p class="sub">Chile 2025 · Registro DIN de Aduanas · {len(P):,} importadores con actividad en el rubro</p>

  <div class="stats">
    <div class="stat"><span class="l">Importación total Chile 2025</span><span class="n">{usd(tot_merc)}</span></div>
    <div class="stat"><span class="l">Del rubro instrumentación</span><span class="n">{usd(tot_instru)}</span></div>
    <div class="stat"><span class="l">Importadores en el rubro</span><span class="n">{len(P):,}</span></div>
    <div class="stat"><span class="l">Importadores totales del país</span><span class="n">{d["n_importadores"]:,}</span></div>
  </div>

  <div class="aviso">
    <b>El registro no trae nombre ni RUT del importador.</b> Aduanas los omite amparada en la
    Ley 20.285, y el Consejo para la Transparencia lo confirmó. Sí trae un
    <code>NUM_UNICO_IMPORTADOR</code> estable por empresa (verificado: 4.720 de los 16.240
    importadores aparecen los 12 meses del año). Por eso estos perfiles describen
    <b>conducta</b> —qué importa, cuánto, de qué origen, con qué regularidad— y no identidad.
    Es lo que sirve para decidir canal: distingue al especialista del importador grande que
    compra de todo.
  </div>

  <h2>Cómo se reparte el rubro</h2>
  <div class="prow">
    {barra(52, "#d97706")}<p class="sub">{usd(164.5e6)} (52%) en 335 importadores grandes multirrubro</p>
    {barra(34, "#2563eb")}<p class="sub">{usd(108.6e6)} (34%) en 74 integradores y distribuidores técnicos</p>
    {barra(10, "#64748b")}<p class="sub">{usd(30.6e6)} (10%) en 1.532 compras menores</p>
    {barra(4, "#047857")}<p class="sub">{usd(13.2e6)} (4%) en 5 especialistas puros de instrumentación</p>
  </div>

  <h2>Los {min(60,len(P))} principales por volumen del rubro</h2>
  <div class="fbar">
    <label class="fbtn"><input type="radio" name="tipo" value="" checked><span>Todos <b>{min(60,len(P))}</b></span></label>
    {tipos_html}
  </div>
  <div class="fbar"><input id="q" type="search" placeholder="Buscar por marca, familia o ID…"
    style="flex:1;min-width:240px;padding:8px 12px;border:1px solid #cbd5e1;border-radius:7px;font-size:14px"></div>

  <div id="lista">{tarjetas}</div>

  <footer>
    Fuente: Registro DIN de importaciones, Servicio Nacional de Aduanas, descargado desde
    <code>datos.gob.cl</code> (12 archivos mensuales, 4.847.036 líneas, 3,7 GB). Elaborado por CONECTA.
    Filtro: partidas arancelarias del dominio de instrumentación y automatización, con marca de
    fabricante identificable del rubro. Los capítulos contaminados (vestuario, automoción,
    médicos de laboratorio) se excluyeron por descripción.
  </footer>
</div>
<script>
  var lista = document.getElementById('lista');
  var perfiles = Array.prototype.slice.call(lista.querySelectorAll('.perf'));
  var q = document.getElementById('q');
  var radios = Array.prototype.slice.call(document.querySelectorAll('input[name=tipo]'));

  function aplicar() {{
    var tipo = (radios.filter(function(r){{return r.checked;}})[0] || {{}}).value || '';
    var t = (q.value || '').toLowerCase().trim();
    var n = 0;
    perfiles.forEach(function(p) {{
      var okT = !tipo || p.getAttribute('data-tipo') === tipo;
      var okQ = !t || p.getAttribute('data-txt').indexOf(t) !== -1;
      var visible = okT && okQ;
      p.style.display = visible ? '' : 'none';
      if (visible) {{
        n++;
        var r = p.querySelector('.rank');
        if (r) r.textContent = '#' + n;
      }}
    }});
  }}
  radios.forEach(function(r) {{ r.addEventListener('change', aplicar); }});
  q.addEventListener('input', aplicar);
  aplicar();
</script>
</body>
</html>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(HTML)
print(f"generado: {OUT}")
print(f"  perfiles en el HTML: {len(P[:60])} de {len(P):,}")
print(f"  bytes: {len(HTML):,}")
