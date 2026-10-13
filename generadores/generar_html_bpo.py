#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/bpo_abastecimiento.html — cuántas empresas como SupplyNet hay en Chile.
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "bpo_abastecimiento.html")

d = json.load(open(os.path.join(D, "bpo_abastecimiento.json"), encoding="utf-8"))
E, N = d["empresas"], d["no_es_bpo"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


filas = ""
for k, v in sorted(E.items(), key=lambda x: -len(x[1]["evidencia"])):
    web = v["web"]
    filas += f'''
    <tr>
      <td><b>{esc(k)}</b><span class="sub">{esc(v['origen'])}</span></td>
      <td><a href="https://{esc(web)}" target="_blank">{esc(web)}</a></td>
      <td>{esc(v['industrias'])[:64]}</td>
      <td class="sub">{esc(v['evidencia'])[:110]}</td>
    </tr>'''

filas_no = ""
for k, v in N.items():
    filas_no += f'<tr><td><b>{esc(k)}</b></td><td class="sub">{esc(v)}</td></tr>'

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BPO de abastecimiento en Chile</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--am:#b45309}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:26px 18px 70px}}
.wrap{{max-width:1160px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:20px;max-width:960px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:20px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid var(--ac);border-radius:9px;padding:13px 16px;margin:15px 0;font-size:13.5px}}
.aviso b{{color:#1e40af}}
.aviso.am{{background:#fffbeb;border-color:#fde68a;border-left-color:var(--am)}}
.aviso.am b{{color:#92400e}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:18px;font-weight:660;margin:24px 0 10px;letter-spacing:-.2px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 9px;border-bottom:2px solid var(--bd)}}
td{{padding:9px 9px;border-bottom:1px solid #f3f4f6;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.sub{{display:block;font-size:11.5px;color:var(--mu);margin-top:1px}}
a{{color:var(--ac);text-decoration:none}} a:hover{{text-decoration:underline}}
blockquote{{border-left:3px solid var(--bd);padding:6px 0 6px 14px;margin:10px 0;color:#374151;font-size:13.5px}}
ul{{margin:8px 0 8px 20px}} li{{margin-bottom:6px}}
footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12.5px}}
</style></head><body><div class="wrap">

<h1>Cuántas empresas como SupplyNet hay en Chile</h1>
<p class="sub0">SupplyNet no vende insumos: <b>le opera el proceso de compras a la minera</b>. Es
<strong>BPO de abastecimiento</strong> — la empresa entrega su función de compras a un tercero, que
la corre con su propio equipo, procesos y tecnología. Acá está cuántas hacen lo mismo.</p>

<div class="kpis">
  <div><b>{len(E)}</b>empresas del mismo modelo</div>
  <div><b>{len(N)}</b>del rubro pero NO BPO (excluidas)</div>
  <div><b>1</b>con origen declarado en Quadrem/Ariba</div>
  <div><b>0</b>aparecen en el eCRM de INECO</div>
</div>

<div class="aviso">
  <b>De dónde sale SupplyNet (textual de su historia):</b>
  <blockquote>"Supplynet Nace como un spin-off del negocio de Procurement Outsourcing (BPO)
  desarrollado por <b>Quadrem</b> y posteriormente <b>SAP Ariba</b>. Hereda alrededor de 7 años de
  experiencia del área de Servicios de Abastecimiento y gran parte del equipo de Profesionales."</blockquote>
  Quadrem fue el marketplace de abastecimiento de la gran minería (Chile fue mercado piloto) y Ariba
  es la plataforma que hoy opera. De esa estirpe salieron varios jugadores locales.
</div>

<div class="aviso am">
  <b>Por qué esto importa para CONECTA.</b> Estas empresas son <b>intermediarios en la compra</b>:
  corren la licitación, las bases técnicas y la administración del contrato de la minera. Son dos
  cosas a la vez:
  <ul>
    <li><b>CANAL:</b> lo que entre en sus bases técnicas se compra. Incluir instrumentación,
    válvulas o analítica SUPCON en su estándar es venderle a todas sus faenas de una vez.</li>
    <li><b>COMPETIDOR:</b> compiten por el presupuesto de "gestión" del área de abastecimiento.</li>
  </ul>
  Y <b>ninguna aparece en el eCRM de INECO</b>: son un canal que nunca se trabajó.
</div>

<h2>Las empresas del modelo</h2>
<div class="card">
  <table><thead><tr>
    <th>Empresa</th><th>Sitio</th><th>Industrias</th><th>Evidencia de que es BPO de abastecimiento</th>
  </tr></thead><tbody>{filas}</tbody></table>
  <p class="sub" style="margin-top:10px">"Evidencia" = el rasgo textual que se leyó en su sitio
  (BPO, abastecimiento, licitaciones, contratos). <b>SGAI</b> sirve su contenido con JS y no se pudo
  leer: se declara como tal en vez de inventarle rasgos.</p>
</div>

<h2>Del rubro, pero NO son del modelo (excluidas a propósito)</h2>
<div class="card">
  <table><thead><tr><th>Quién</th><th>Por qué no entra</th></tr></thead><tbody>{filas_no}</tbody></table>
</div>

<h2>Lo que el servicio incluye (caso de éxito de SupplyNet, textual)</h2>
<div class="card">
  <p class="sub">Sobre un cliente minero no nombrado, con la Gerencia Corporativa y cada faena:</p>
  <p>Compras · Licitaciones · Backoffice · Administración de contratos · Sustentabilidad ·
  Proveedores Regionales · Soporte plataforma Ariba · Reportabilidad · Control de gestión y
  excelencia operacional.</p>
  <p class="sub" style="margin-top:8px">Es la <b>función completa</b> de abastecimiento. Un dato
  operativo a considerar: quien quiera venderle a esa minera por la vía de SupplyNet está
  negociando con este equipo, no con la minera.</p>
</div>

<h2>Qué no dice esta lista</h2>
<div class="card">
  <ul>
    <li><b>No es un censo cerrado.</b> Es lo que aparece buscando el modelo en fuentes públicas.
    Puede haber más, sobre todo equipos chicos que operan dentro de una sola faena y no tienen
    sitio web.</li>
    <li><b>No dice el tamaño de cada una.</b> Solo SupplyNet tiene dato público (entre 51 y 500
    trabajadores según los perfiles que la listan). Las demás no publican dotación.</li>
    <li><b>No dice a qué minera sirve cada una</b>, salvo los casos con evidencia: SupplyNet (grupo
    minero no nombrado + una minera global) y Metaproject (renovó por 5 años con Codelco).</li>
    <li><b>El cruce con el eCRM dio cero</b> usando el nombre completo. La primera medición dio
    "52 menciones" de CAS Group y "19" de IDE: eran <b>coincidencias de substring</b>
    ("cas" dentro de "caso", "ide" dentro de "consideraciones"). Corregido.</li>
  </ul>
</div>

<footer>
  Fuente: sitios oficiales de cada empresa + <code>supplynet.cl/about/#historia</code> ·
  <a href="ecrm_supcon.html">eCRM × SUPCON</a> ·
  <a href="compradores_linkedin.html">compradores en LinkedIn</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(E)} empresas BPO | {len(N)} excluidas")
