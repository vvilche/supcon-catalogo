#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/personas_por_area.html — LAS PERSONAS A CARGO DE CADA ÁREA.

Qué resuelve: la matriz de productos dice QUÉ necesita la planta; esto dice QUIÉN lo compra.
Sin la persona del área no hay a quién venderle la línea.

Lee datos/personas_por_area_barrido.json y datos/matriz_dolor_linea_perfil.json.
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "personas_por_area.html")

p = json.load(open(os.path.join(D, "personas_por_area_barrido.json"), encoding="utf-8"))
# el archivo tiene metadatos + el mapa por empresa (cambió de forma al fusionar)
EMP = p.get("por_empresa") or {k: v for k, v in p.items()
                               if isinstance(v, dict) and k not in
                               ("fuente", "advertencia", "por_empresa")}

# la matriz, para cruzar: qué área compra cada línea
try:
    mp = json.load(open(os.path.join(D, "matriz_dolor_linea_perfil.json"), encoding="utf-8"))
    LINEA_POR_AREA = {
        "Medio Ambiente": ["Analítica", "Software y plataforma"],
        "Calidad": ["Analítica", "Instrumentación"],
        "Instrumentacion y Control": ["DCS", "SIS", "Software y plataforma", "Instrumentación"],
        "Mantenimiento": ["Válvulas", "Instrumentación", "SIS"],
        "Electrico": ["Instrumentación", "Software y plataforma"],
        "Produccion": ["DCS", "Instrumentación"],
    }
except Exception:
    LINEA_POR_AREA = {}

AREA_COLOR = {
    "Medio Ambiente": "#b91c1c", "Calidad": "#c2410c", "Instrumentacion y Control": "#7c3aed",
    "Mantenimiento": "#1d4ed8", "Electrico": "#0891b2", "Produccion": "#047857",
}
AREA_LABEL = {"Instrumentacion y Control": "Instrumentación y Control"}


def e(s):
    return html.escape(str(s if s is not None else ""))


# ---- agregado por area ----
tot_area = collections.Counter()
emp_area = collections.defaultdict(set)
for emp, areas in EMP.items():
    for a, personas in areas.items():
        tot_area[a] += len(personas)
        emp_area[a].add(emp)

filas_area = ""
for a, n in tot_area.most_common():
    col = AREA_COLOR.get(a, "#475569")
    lineas = ", ".join(LINEA_POR_AREA.get(a, []))
    filas_area += f'''
    <tr>
      <td><span class="dot" style="background:{col}"></span><b>{e(AREA_LABEL.get(a,a))}</b></td>
      <td class="num"><b>{n}</b></td>
      <td class="num">{len(emp_area[a])}</td>
      <td class="ct">{e(lineas) or '—'}</td>
    </tr>'''

# ---- fichas por empresa ----
fichas = ""
for emp, areas in sorted(EMP.items(), key=lambda x: -sum(len(v) for v in x[1].values())):
    bloques = ""
    for a, personas in sorted(areas.items(), key=lambda x: -len(x[1])):
        col = AREA_COLOR.get(a, "#475569")
        ps = ""
        for pr in personas:
            li = pr.get("linkedin") or ""
            nom = e(pr["nombre"]) if not li else f'<a href="{e(li)}" target="_blank" rel="noopener">{e(pr["nombre"])}</a>'
            ps += f'<div class="per"><b>{nom}</b><span class="cg">{e(pr["cargo"])}</span></div>'
        lineas = ", ".join(LINEA_POR_AREA.get(a, []))
        bloques += f'''
        <div class="ar" style="border-left-color:{col}">
          <div class="arh"><span class="dot" style="background:{col}"></span><b>{e(AREA_LABEL.get(a,a))}</b>
            <span class="n">{len(personas)}</span>
            <span class="ln">{e(lineas)}</span>
          </div>
          <div class="pers">{ps}</div>
        </div>'''
    n_p = sum(len(v) for v in areas.values())
    fichas += f'''
    <section class="emp" data-b="{e(' '.join(areas.keys())).lower()}">
      <div class="eh"><h3>{e(emp)}</h3>
        <span class="tot">{len(areas)} áreas · {n_p} personas</span></div>
      <div class="ars">{bloques}</div>
    </section>'''

n_emp = len(EMP)
n_per = sum(tot_area.values())

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Personas a cargo de cada área</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1200px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:900px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6}}
tr:last-child td{{border-bottom:none}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.ct{{font-size:12.5px;color:var(--mu)}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:7px;vertical-align:middle}}
.barra{{display:flex;gap:9px;align-items:center;margin-bottom:12px;flex-wrap:wrap}}
input[type=search]{{flex:1;min-width:230px;padding:9px 13px;border:1px solid var(--bd);border-radius:8px;font-size:14px;font-family:inherit}}
input[type=search]:focus{{outline:none;border-color:var(--ac);box-shadow:0 0 0 3px #1d4ed814}}
.cuenta{{font-size:12.5px;color:var(--mu);white-space:nowrap}}
.emp{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:15px 18px;margin-bottom:12px}}
.eh{{display:flex;align-items:baseline;gap:12px;margin-bottom:11px;flex-wrap:wrap}}
.eh h3{{font-size:15.5px;font-weight:660}}
.tot{{font-size:11.5px;color:var(--mu);margin-left:auto}}
.ars{{display:grid;gap:8px}}
.ar{{background:#fbfcfd;border:1px solid #eef1f4;border-left:3px solid var(--bd);border-radius:8px;padding:9px 12px}}
.arh{{display:flex;align-items:center;gap:8px;font-size:13px;margin-bottom:6px;flex-wrap:wrap}}
.arh b{{font-weight:640}}
.arh .n{{font-size:11px;background:#f1f5f9;border-radius:9px;padding:1px 7px;color:#475569;font-weight:700}}
.arh .ln{{font-size:11px;color:var(--mu);margin-left:auto}}
.pers{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:4px}}
.per{{font-size:12.5px;line-height:1.4}}
.per b{{font-weight:600;display:block}}
.per a{{color:var(--ac);text-decoration:none}} .per a:hover{{text-decoration:underline}}
.cg{{color:var(--mu);font-size:11.5px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:5px}}
</style></head><body><div class="wrap">

<h1>Las personas a cargo de cada área</h1>
<p class="sub0">Para cada empresa, quién responde por cada área: mantenimiento, instrumentación y
control, calidad, medio ambiente, eléctrico y producción. Es lo que faltaba: la matriz de
productos dice <b>qué</b> necesita la planta, esto dice <b>quién lo compra</b>. Al jefe de I&amp;C
no se le vende analítica; al de medio ambiente no se le vende un DCS.</p>

<div class="kpis">
  <div><b>{n_emp}</b>empresas con personas por área</div>
  <div><b>{n_per}</b>personas identificadas</div>
  <div><b>{len(tot_area)}</b>áreas cubiertas</div>
  <div><b>{sum(1 for a in EMP.values() if len(a)>=4)}</b>empresas con 4+ áreas</div>
</div>

<h2>Cobertura por área</h2>
<div class="card">
  <table><thead><tr>
    <th>Área</th><th class="num">Personas</th><th class="num">Empresas</th>
    <th>Líneas que compra esa área</th>
  </tr></thead><tbody>{filas_area}</tbody></table>
</div>

<h2>Las empresas, con su gente por área</h2>
<div class="card">
  <div class="barra">
    <input type="search" id="q" placeholder="Filtrar por empresa o área…">
    <span class="cuenta" id="c"></span>
  </div>
</div>
{fichas}

<h2>Cómo se obtuvo, y qué no dice</h2>
<div class="card">
  <ul>
    <li><b>El método:</b> búsqueda por empresa × área, y la persona se clasifica <b>por su cargo
    real</b>, no por la consulta que la encontró. Medido por qué importa: "Subgerente de
    Contabilidad" entraba como Instrumentación porque lo encontró esa búsqueda; por cargo no
    clasifica y se descarta.</li>
    <li><b>Se descartó el ruido:</b> el buscador devuelve en el snippet nombres que en realidad son
    la razón social (GNL Quintero S.A., Exportadora Los Fiordos Limitada). Esos se filtran.</li>
    <li><b>El cargo es al momento del dato, no está verificado hoy.</b> Las personas se mueven:
    Víctor Balbontín aparece en el registro del CEN como Encargado Titular de Enel, y hoy es
    Director de Operaciones de CGE (confirmado en prensa 2026).</li>
    <li><b>Solo nombre y cargo.</b> El LinkedIn se guarda cuando el buscador lo devuelve en el
    mismo resultado, pero no se buscó correo ni teléfono: eso es un paso aparte.</li>
    <li><b>Cobertura concentrada.</b> 258 personas en 55 empresas: el barrido rinde mucho en las
    grandes y casi nada en las chicas (medido: 3-4 personas/empresa en las primeras, 0,1 en las
    siguientes). Por eso no se recorrió el universo completo: se priorizó donde hay mercado.</li>
  </ul>
</div>

<footer>
  Fuente: barrido de perfiles públicos por empresa × área (nombre y cargo del snippet indexado).
  <br>Ver también <a href="matriz_dolor_perfil.html">matriz dolor·línea·perfil</a> ·
  <a href="cliente_ideal_linea.html">cliente ideal por línea</a> ·
  <a href="dolor_ambiental.html">dolor ambiental</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div>
<script>
const q = document.getElementById('q'), c = document.getElementById('c');
function filtrar() {{
  const v = q.value.toLowerCase().trim();
  let vis = 0;
  document.querySelectorAll('.emp').forEach(s => {{
    const hay = (s.dataset.b || '') + ' ' + s.textContent.toLowerCase();
    const ok = !v || hay.includes(v);
    s.hidden = !ok;
    if (ok) vis++;
  }});
  c.textContent = vis + ' de ' + document.querySelectorAll('.emp').length + ' empresas';
}}
q.addEventListener('input', filtrar);
filtrar();
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {n_emp} empresas | {n_per} personas | {len(tot_area)} areas")
