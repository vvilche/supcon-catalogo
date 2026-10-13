#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/matriz_dolor_perfil.html — MATRIZ DOLOR x LÍNEA x PERFIL.

Un solo documento. Por empresa: qué necesita (medido en el RETC), qué producto lo resuelve, y
QUIÉN de esa empresa lo compra. Marca la línea de ENTRADA y avisa cuando no hay contacto del
perfil comprador — que es el hueco comercial más importante que se midió.

Lee datos/matriz_dolor_linea_perfil.json.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "matriz_dolor_perfil.html")

d = json.load(open(os.path.join(D, "matriz_dolor_linea_perfil.json"), encoding="utf-8"))
EM = d["empresas"]
PERFIL_FALTA = d["perfil_que_compra"]

COLOR = {"Analítica": "#b91c1c", "SIS": "#c2410c", "Software y plataforma": "#1d4ed8",
         "Instrumentación": "#7c3aed", "Válvulas": "#047857", "DCS": "#0891b2",
         "PLC": "#4b5563"}


def e(s):
    return html.escape(str(s if s is not None else ""))


def n(v, dec=0):
    try:
        return f"{float(v):,.{dec}f}"
    except Exception:
        return "—"


# ---- agregados por linea ----
lin_stats = collections.defaultdict(lambda: {"nec": 0, "con": 0, "empresas_con": []})
for s in EM:
    for l in s["lineas"]:
        lin_stats[l["linea"]]["nec"] += 1
        if l["tiene_contacto"]:
            lin_stats[l["linea"]]["con"] += 1
            lin_stats[l["linea"]]["empresas_con"].append(s["empresa"])

filas_lin = ""
for lin, v in sorted(lin_stats.items(), key=lambda x: -x[1]["nec"]):
    cob = v["con"] / v["nec"] * 100 if v["nec"] else 0
    col = COLOR.get(lin, "#475569")
    estado = ("CRÍTICO" if cob < 10 else "BAJO" if cob < 45 else "OK")
    ecol = {"CRÍTICO": "#b91c1c", "BAJO": "#c2410c", "OK": "#047857"}[estado]
    filas_lin += f'''
    <tr>
      <td><span class="dot" style="background:{col}"></span><b>{e(lin)}</b></td>
      <td class="num">{v['nec']}</td>
      <td class="num">{v['con']}</td>
      <td class="num"><b style="color:{ecol}">{cob:.0f}%</b></td>
      <td><span class="badge" style="background:{ecol}14;color:{ecol};border:1px solid {ecol}3d">{estado}</span></td>
      <td class="perf">{e(PERFIL_FALTA.get(lin,''))}</td>
    </tr>'''

# ---- empresas ----
filas_emp = ""
for s in sorted(EM, key=lambda x: -(x["carga_peligrosa_t"] or 0)):
    lineas_html = ""
    for l in s["lineas"]:
        col = COLOR.get(l["linea"], "#475569")
        est = ""
        if l["tiene_contacto"]:
            c = l["contactos_que_compran"][0]
            est = f'<span class="cto">→ {e(c["nombre"])} <i>{e((c.get("cargo") or "")[:34])}</i></span>'
        else:
            est = f'<span class="falta">✗ falta {e(l["perfil_que_compra"])}</span>'
        marcas = ' <span class="ent">ENTRADA</span>' if l["entrada"] else ""
        prods = " · ".join(l["productos"][:3])
        filas_emp += f'''
        <div class="ln">
          <div class="lnh"><span class="dot" style="background:{col}"></span><b>{e(l['linea'])}</b>{marcas}</div>
          <div class="lnq">{e(l['por_que'][0])}</div>
          <div class="lnp">{e(prods)}</div>
          <div class="lnc">{est}</div>
        </div>'''
    bord = "#b91c1c" if (s["lineas_sin_contacto"] and "Analítica" in s["lineas_sin_contacto"]) else "#e5e7eb"
    filas_emp += f'''
    <section class="emp" data-b="{e(' '.join(x['linea'] for x in s['lineas'])).lower()}" style="border-left-color:{bord}">
      <div class="eh">
        <h3>{e(s['empresa'])}</h3>
        <span class="rub">{e(s['rubro'] or '')}</span>
        <span class="met"><b>{n(s['carga_peligrosa_t'],1)}</b> t tóxicas · <b>{n(s['emision_agua_t'])}</b> t al agua total</span>
      </div>
      <div class="lns">{lineas_html}</div>
    </section>'''

total_nec = sum(v["nec"] for v in lin_stats.values())
total_con = sum(v["con"] for v in lin_stats.values())
vend_hoy = sum(1 for s in EM if s["lineas_vendibles_hoy"])

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Matriz dolor · línea · perfil — qué le vendemos y a quién</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:920px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#fef2f2;border:1px solid #fecaca;border-left:4px solid #b91c1c;border-radius:9px;padding:14px 17px;margin:16px 0;font-size:13.5px}}
.aviso b{{color:#991b1b}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:10px 9px;border-bottom:1px solid #f3f4f6}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:7px;vertical-align:middle}}
.badge{{font-size:10.5px;border-radius:5px;padding:2px 8px;font-weight:700;letter-spacing:.3px}}
.perf{{font-size:12.5px;color:var(--mu)}}
.barra{{display:flex;gap:9px;align-items:center;margin-bottom:14px;flex-wrap:wrap}}
input[type=search]{{flex:1;min-width:230px;padding:9px 13px;border:1px solid var(--bd);border-radius:8px;font-size:14px;font-family:inherit}}
input[type=search]:focus{{outline:none;border-color:var(--ac);box-shadow:0 0 0 3px #1d4ed814}}
.cuenta{{font-size:12.5px;color:var(--mu);white-space:nowrap}}
.emp{{background:var(--cd);border:1px solid var(--bd);border-left:3px solid var(--bd);border-radius:11px;padding:14px 17px;margin-bottom:11px}}
.eh{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:10px}}
.eh h3{{font-size:15.5px;font-weight:660}}
.rub{{font-size:11.5px;color:var(--mu);background:#f3f4f6;padding:1px 8px;border-radius:5px}}
.met{{font-size:12px;color:var(--mu);margin-left:auto;font-variant-numeric:tabular-nums}}
.met b{{color:var(--tx)}}
.lns{{display:grid;gap:7px}}
.ln{{background:#fbfcfd;border:1px solid #eef1f4;border-radius:8px;padding:9px 12px}}
.lnh{{display:flex;align-items:center;gap:7px;font-size:13px;margin-bottom:3px}}
.lnh b{{font-weight:640}}
.ent{{font-size:9.5px;background:#1d4ed814;color:var(--ac);border:1px solid #1d4ed83d;border-radius:4px;padding:1px 5px;font-weight:700;letter-spacing:.3px}}
.lnq{{font-size:12.5px;color:#374151;margin-bottom:3px}}
.lnp{{font-size:11.5px;color:var(--mu);margin-bottom:3px}}
.lnc{{font-size:12px}}
.cto{{color:#047857}} .cto i{{color:var(--mu);font-style:normal}}
.falta{{color:#b91c1c;font-weight:600}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:5px}}
</style></head><body><div class="wrap">

<h1>Qué le vendemos a cada planta, y a quién</h1>
<p class="sub0">Tres cosas juntas, por empresa: el <b>dolor medido</b> en el RETC, la <b>línea de
negocio</b> que lo resuelve, y el <b>perfil que lo compra</b>. La línea de entrada abre la
conversación; las demás se venden después. Cuando no hay contacto del perfil comprador, se dice.</p>

<div class="kpis">
  <div><b>{len(EM)}</b>plantas con dolor medido</div>
  <div><b>{total_nec}</b>asignaciones línea-planta</div>
  <div><b>{total_con}</b>con comprador identificado</div>
  <div><b>{vend_hoy}</b>empresas vendibles hoy</div>
</div>

<div class="aviso">
  <b>El hueco comercial más grande está medido: Analítica.</b> 253 plantas la necesitan —es la
  línea que resuelve metales pesados y cianuro, y la que la SMA fiscaliza— y solo <b>6</b> tienen
  el contacto que la compra: <b>2% de cobertura</b>. En 247 empresas Analítica es la línea de
  entrada y no hay a quién venderle. El motivo es de origen: el catálogo se armó buscando
  compradores de instrumentación y control (336 perfiles), y de calidad/medio ambiente/laboratorio
  hay 53, casi ninguno con ese cargo real.
</div>

<h2>La matriz, por línea de negocio</h2>
<div class="card">
  <table><thead><tr>
    <th>Línea</th><th class="num">Plantas que la necesitan</th><th class="num">Con comprador</th>
    <th class="num">Cobertura</th><th>Estado</th><th>Perfil que hay que buscar</th>
  </tr></thead><tbody>{filas_lin}</tbody></table>
</div>

<h2>Por empresa: qué necesita, qué le vendo, quién lo compra</h2>
<div class="card">
  <div class="barra">
    <input type="search" id="q" placeholder="Filtrar por empresa o línea de negocio…">
    <span class="cuenta" id="c"></span>
  </div>
  <div id="lista">{filas_emp}</div>
</div>

<h2>Cómo se lee, y qué no dice</h2>
<div class="card">
  <ul>
    <li><b>Una línea se asigna a un contacto solo si su perfil es comprador de esa línea.</b>
    Al jefe de I&amp;C no se le vende analítica de proceso: eso lo compra calidad o medio ambiente.
    Si el vendedor llega con el argumento que su interlocutor no puede decidir, quema la reunión.</li>
    <li><b>Solo cuenta el contaminante con masa declarada mayor que cero.</b> El DS 90 obliga a
    reportar todos los parámetros de su tabla, así que "declara cadmio" no significa nada si está
    en cero: la mediana de contaminantes por empresa es 25. El conteo es una obligación legal,
    no una señal de dolor.</li>
    <li><b>Se ordena por carga tóxica, no por volumen.</b> Los mayores volúmenes del país son
    cloruros y sulfato (agua de mar para enfriamiento, yeso), que no se multan.</li>
    <li><b>No dice que haya incumplimiento.</b> Mide el dolor: lo que hay que medir y hoy no se
    mide en línea. Declarar al RETC es una obligación distinta.</li>
    <li><b>Los cargos pueden estar vencidos.</b> Caso medido: Víctor Balbontín aparece en el
    registro del CEN como Encargado Titular de Enel, pero hoy es Director de Operaciones de CGE
    (confirmado en prensa, 2026). Los contactos del catálogo tienen cargo al momento del dato,
    no cargo verificado hoy.</li>
  </ul>
</div>

<footer>
  Fuentes: RETC del Ministerio del Medio Ambiente (RILES 2024 y residuos peligrosos 2025) ·
  catálogo de prospección de 3.157 empresas y 1.629 tomadores · líneas de negocio de
  <code>escalera_exito_v3</code> (7 líneas, 63 productos).
  <br>Ver también <a href="dolor_ambiental.html">dolor ambiental</a> ·
  <a href="plan_contacto_tecnico.html">contacto técnico</a> ·
  <a href="plan_contacto.html">plan de contacto</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div>
<script>
const q = document.getElementById('q');
const lista = document.getElementById('lista');
const cuenta = document.getElementById('c');
function filtrar() {{
  const v = q.value.toLowerCase().trim();
  let vis = 0;
  lista.querySelectorAll('.emp').forEach(s => {{
    const hay = (s.dataset.b || '') + ' ' + s.textContent.toLowerCase();
    const ok = !v || hay.includes(v);
    s.hidden = !ok;
    if (ok) vis++;
  }});
  cuenta.textContent = vis + ' de ' + lista.querySelectorAll('.emp').length + ' plantas';
}}
q.addEventListener('input', filtrar);
filtrar();
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  empresas: {len(EM)} | asignaciones: {total_nec} | con comprador: {total_con}")
