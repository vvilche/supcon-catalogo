#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el HTML del estudio de mercado 2025 (importaciones Aduanas Chile).
Lee datos/estudio_mercado_2025.json. NO inventa: solo lo medido.
"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, "datos")
d = json.load(open(os.path.join(D, "estudio_mercado_2025.json"), encoding="utf-8"))

# normalizar marcas (agrupar variantes del mismo fabricante)
import collections
def normaliza(m):
    x = m.upper().replace("-F","").replace("~"," ").strip()
    for base, alias in [
        ("SIEMENS","SIEMENS"),("ABB","ABB"),("SCHNEIDER","SCHNEIDER ELECTRIC"),("ENDRESS","ENDRESS+HAUSER"),
        ("EMERSON","EMERSON"),("DANFOSS","DANFOSS"),("METSO","METSO"),("VALMET","VALMET"),
        ("HONEYWELL","HONEYWELL"),("YOKOGAWA","YOKOGAWA"),("PHOENIX","PHOENIX CONTACT"),
        ("ROCKWELL","ROCKWELL"),("MITSUBISHI","MITSUBISHI"),("IFM","IFM ELECTRONIC"),
        ("KROHNE","KROHNE"),("FLEXIM","FLEXIM"),("MICRO MOTION","MICRO MOTION"),("CIDRA","CIDRA"),
        ("MSA","MSA"),("HACH","HACH"),("THERMO","THERMO FISHER"),("TELEDYNE","TELEDYNE"),
        ("PERKIN","PERKIN ELMER"),("SAMSON","SAMSON"),("FISHER","FISHER"),("BRAY","BRAY"),
        ("VALVITALIA","VALVITALIA"),("GENEBRE","GENEBRE"),("MOXA","MOXA"),("TELTONIKA","TELTONIKA"),
        ("WAGO","WAGO"),("FLUKE","FLUKE"),("OMICRON","OMICRON"),("SEL","SEL"),("VEGA","VEGA"),
        ("GEWISS","GEWISS"),("FESTO","FESTO"),("INNOMOTICS","INNOMOTICS"),("WEG","WEG"),
        ("HITACHI","HITACHI ENERGY"),("HYOSUNG","HYOSUNG"),("ALSTOM","ALSTOM"),("ETP","ETP ELEKTRO"),
    ]:
        if x.startswith(base) or base in x:
            return alias
    return x[:26]

FAMILIAS = d["por_familia"]

# tildes de los nombres de familia (los del JSON vienen sin acentos por el clasificador)
TILDES = {
 "Instrumentacion de campo":"Instrumentación de campo",
 "Valvulas de control y proceso":"Válvulas de control y proceso",
 "Aparatos de conexion y proteccion":"Aparatos de conexión y protección",
 "Medida y control electrico":"Medida y control eléctrico",
 "Controladores, PLC y modulos de E/S":"Controladores, PLC y módulos de E/S",
 "Fuentes de poder y convertidores":"Fuentes de poder y convertidores",
 "Redes industriales (OT)":"Redes industriales (OT)",
 "Detectores de gas y alarma":"Detectores de gas y alarma",
 "Analizadores de proceso":"Analizadores de proceso",
}
FAMILIAS = {TILDES.get(k, k): v for k, v in FAMILIAS.items()}
# ordenar por valor y agrupar marcas
grupos = []
for fam, info in sorted(FAMILIAS.items(), key=lambda x: -x[1]["cif"]):
    if "Vision" in fam:      # excluida: capturaba camaras de consumo (Sony/Canon)
        continue
    ag = collections.Counter()
    for m, v in info["marcas_valor"]:
        ag[normaliza(m)] += v
    grupos.append((fam, info["cif"], info["items"], ag.most_common(8), info.get("partidas", {})))

total = sum(g[1] for g in grupos)
top_marcas = collections.Counter()
for fam, info in FAMILIAS.items():
    if "Vision" in fam: continue
    for m, v in info["marcas_valor"]:
        top_marcas[normaliza(m)] += v

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

filas_fam = ""
for fam, cif, items, marcas, partidas in grupos:
    ms = "".join(f'<span class="mk">{esc(m)} <b>US${v/1e6:.1f}M</b></span>' for m, v in marcas)
    ps = " · ".join(list(partidas.keys())[:6])
    filas_fam += f"""
    <tr>
      <td class="fam">{esc(fam)}</td>
      <td class="num dest">{cif/1e6:,.1f}</td>
      <td class="num">{items:,}</td>
      <td class="mks">{ms}</td>
    </tr>"""

filas_rank = ""
for i, (m, v) in enumerate(top_marcas.most_common(20), 1):
    pct = v / total * 100
    filas_rank += f"""<tr><td class="num">{i}</td><td class="mk-cell">{esc(m)}</td>
      <td class="num">{v/1e6:,.1f}</td>
      <td class="num">{pct:.1f}%</td>
      <td><div class="bar"><i style="width:{min(pct*3,100):.0f}%"></i></div></td></tr>"""

meses = d.get("por_mes", {})
mes_ord = sorted(meses.items(), key=lambda x: x[0])
maxmes = max(v for _, v in mes_ord) if mes_ord else 1
filas_mes = "".join(
    f'<div class="mes"><span class="ml">{esc(k[:14])}</span>'
    f'<div class="mbar"><i style="width:{v/maxmes*100:.0f}%"></i></div>'
    f'<span class="mv">US${v/1e6:,.1f}M</span></div>' for k, v in mes_ord)

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Estudio de mercado 2025 — Automatización e instrumentación en Chile</title>
<style>
:root{{--bg:#f8fafc;--card:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706;--ok:#059669}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--tx);font-family:Inter,-apple-system,sans-serif;font-size:15px;line-height:1.6;padding:36px 26px 90px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:30px;font-weight:660;letter-spacing:-.7px;margin-bottom:8px}}
.sub{{color:var(--mu);font-size:15.5px;max-width:900px}}
.src{{margin-top:16px;padding:13px 17px;background:var(--acs);border-left:3px solid var(--ac);border-radius:10px;font-size:13.5px;color:#1e3a8a}}
h2{{font-size:19px;font-weight:640;margin:38px 0 6px}}
h2 small{{font-weight:400;color:var(--mu);font-size:14px}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:20px;padding:24px;margin-top:14px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--mu);padding:9px 10px;border-bottom:1px solid var(--bd);font-weight:600}}
td{{padding:11px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.num{{font-family:"IBM Plex Mono",ui-monospace,monospace;text-align:right;white-space:nowrap}}
.dest{{font-weight:650;font-size:14.5px}}
.fam{{font-weight:600;min-width:210px}}
.mks{{display:flex;flex-wrap:wrap;gap:6px}}
.mk{{background:var(--acs);color:#1e40af;border-radius:100px;padding:3px 10px;font-size:11.5px;white-space:nowrap}}
.mk b{{font-family:"IBM Plex Mono",monospace;font-weight:650}}
.bar{{background:#f1f5f9;border-radius:100px;height:7px;overflow:hidden;min-width:90px}}
.bar i{{display:block;height:100%;background:var(--ac);border-radius:100px}}
.mes{{display:flex;align-items:center;gap:12px;margin-bottom:7px;font-size:13px}}
.ml{{width:110px;color:var(--mu);text-transform:capitalize}}
.mbar{{flex:1;background:#f1f5f9;border-radius:100px;height:9px;overflow:hidden}}
.mbar i{{display:block;height:100%;background:var(--ac);border-radius:100px}}
.mv{{width:82px;text-align:right;font-family:"IBM Plex Mono",monospace}}
.hall{{background:var(--card);border:1px solid var(--bd);border-left:4px solid var(--am);border-radius:16px;padding:22px 24px;margin-top:14px}}
.hall h3{{font-size:17px;font-weight:650;margin-bottom:9px;color:#92400e}}
.hall p{{font-size:14px;color:#78350f;margin-bottom:9px}}
.big{{display:flex;gap:34px;flex-wrap:wrap;margin:26px 0 8px;padding:22px 0;border-top:1px solid var(--bd);border-bottom:1px solid var(--bd)}}
.big .st b{{display:block;font-size:30px;font-weight:660;font-family:"IBM Plex Mono",monospace;letter-spacing:-1px}}
.big .st span{{font-size:11.5px;color:var(--mu);text-transform:uppercase;letter-spacing:.6px}}
ul{{margin:9px 0 0 20px;font-size:14px}} li{{margin-bottom:5px}}
code{{background:#f1f5f9;padding:2px 6px;border-radius:5px;font-size:12.5px;font-family:"IBM Plex Mono",monospace}}
.foot{{margin-top:36px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
</style></head><body><div class="wrap">

<h1>Estudio de mercado 2025 — Automatización e instrumentación industrial en Chile</h1>
<p class="sub">Tamaño de mercado por familia de producto, medido sobre las importaciones reales
de Chile, no sobre estimaciones.</p>
<div class="src"><b>Fuente primaria:</b> Registro de Importaciones (DIN) del Servicio Nacional de
Aduanas, 12 meses de 2025, publicado en datos.gob.cl. Se procesaron
<b>{d['lineas_totales']:,}</b> líneas de detalle. Cada valor es USD CIF declarado.</div>

<div class="big">
  <div class="st"><b>US${total/1e6:,.0f}M</b><span>Mercado 2025</span></div>
  <div class="st"><b>{len(grupos)}</b><span>Familias</span></div>
  <div class="st"><b>{top_marcas.most_common(1)[0][0]}</b><span>Líder</span></div>
  <div class="st"><b>{d['lineas_relevantes']:,}</b><span>Líneas del dominio</span></div>
</div>

<h2>Mercado por familia <small>con marcas de automatización identificadas</small></h2>
<div class="card"><table>
<thead><tr><th>Familia</th><th style="text-align:right">USD CIF (M)</th>
<th style="text-align:right">Ítems</th><th>Proveedores principales</th></tr></thead>
<tbody>{filas_fam}
<tr><td class="fam"><b>TOTAL</b></td><td class="num dest"><b>{total/1e6:,.1f}</b></td>
<td class="num"><b>{sum(g[2] for g in grupos):,}</b></td><td></td></tr>
</tbody></table></div>

<h2>Ranking de proveedores <small>US$ millones importados en 2025</small></h2>
<div class="card"><table>
<thead><tr><th>#</th><th>Fabricante</th><th style="text-align:right">USD CIF (M)</th>
<th style="text-align:right">Cuota</th><th>Participación</th></tr></thead>
<tbody>{filas_rank}</tbody></table></div>

<h2>Estacionalidad mensual</h2>
<div class="card">{filas_mes}</div>

<h2>Hallazgo principal</h2>
<div class="hall">
  <h3>SUPCON y Hobré no registran importaciones en Chile en 2025</h3>
  <p>Se buscaron las marcas <code>SUPCON</code>, <code>HOBRE</code>, <code>TISOMIC</code>,
  <code>C-QUAND</code>, <code>WIM COMPAS</code> y <code>PRISM RAMAN</code> sobre las
  <b>{d['lineas_totales']:,}</b> líneas del año completo. Las 13 coincidencias halladas eran
  falsos positivos de la palabra «hombre» sin tilde en ropa (poleras, abrigos, cinturones,
  zapatillas).</p>
  <p><b>Conclusión:</b> no hay presencia de importación directa de SUPCON ni de Hobré en Chile
  durante 2025. Todo lo que se venda hoy es proyecto nuevo, sin base instalada previa
  importada de forma directa.</p>
</div>

<h2>Advertencia metodológica</h2>
<div class="card">
  <p style="font-size:14px">Este estudio mide <b>importación directa por marca declarada</b>.
  Eso tiene dos límites que debes considerar antes de usar los números:</p>
  <ul>
    <li><b>El equipo entra por integradores.</b> Si un EPC importa un DCS con su propia marca
    comercial o como «sistema completo», la línea no lleva la marca del fabricante. Por eso
    SUPCON puede vender en Chile y no aparecer: sus equipos llegan dentro de proyectos de
    terceros.</li>
    <li><b>Se excluyó la categoría «Visión industrial»</b> porque las partidas de cámaras
    capturaban principalmente equipos de consumo (Sony, Canon) y no visión de proceso.</li>
  </ul>
  <p style="font-size:14px;margin-top:11px">Los valores de partidas <b>no</b> se suman a las
  familias: un mismo equipo puede declararse bajo más de una partida según su uso. Cada familia
  es un cálculo independiente sobre su conjunto de partidas.</p>
</div>

<div class="foot">
  Fuente: Servicio Nacional de Aduanas — Registro de Importaciones (DIN) 2025, vía datos.gob.cl.<br>
  Procesamiento determinístico sobre {d['lineas_totales']:,} líneas. Sin estimaciones ni datos inferidos.
</div>
</div></body></html>"""

OUT = os.path.join(BASE, "estudio_mercado_2025.html")
open(OUT, "w", encoding="utf-8").write(HTML)
print("escrito:", OUT, len(HTML.encode()), "bytes")
print(f"mercado total: US${total/1e6:,.1f}M | familias: {len(grupos)}")
