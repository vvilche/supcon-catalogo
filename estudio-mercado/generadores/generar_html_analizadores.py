#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML del estudio focalizado de analizadores de proceso (90.27), Chile 2025."""
import os, json, collections

BASE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(BASE, "datos", "analizadores_2025.json"), encoding="utf-8"))

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# normalizar marcas del mismo fabricante
def norm(m):
    x = m.upper().replace("-F","").strip()
    for b,a in [("ENDRESS","Endress+Hauser"),("MSA","MSA"),("THERMO","Thermo Fisher"),
                ("METSO","Metso"),("CIDRA","CIDRA"),("KT-KINETICS","KT Kinetics"),("HACH","Hach"),
                ("WATERS","Waters"),("SHIMADZU","Shimadzu"),("AGILENT","Agilent"),("TELEDYNE","Teledyne"),
                ("FLIR","FLIR"),("SIEMENS","Siemens"),("ABB","ABB"),("YOKOGAWA","Yokogawa"),
                ("EMERSON","Emerson"),("BRUKER","Bruker"),("PERKIN","PerkinElmer"),("LECO","LECO"),
                ("DANFOSS","Danfoss"),("BUCHI","Buchi"),("PENTAIR","Pentair"),("KNAUER","Knauer"),
                ("ANALYTIK","Analytik Jena"),("HONEYWELL","Honeywell"),("KROHNE","Krohne")]:
        if x.startswith(b) or b in x: return a
    return m[:24]

agg = collections.Counter()
for p, info in d["por_subpartida"].items():
    for m, v in info["marcas"]:
        agg[norm(m)] += v
total = sum(agg.values())
top = agg.most_common(18)

# tabla de subpartidas
filas_sub = ""
for p, info in sorted(d["por_subpartida"].items(), key=lambda x:-x[1]["cif"]):
    g = d["glosas"].get(p, "")
    mk = info["marcas"][:4]
    chips = "".join(f'<span class="mk">{esc(norm(m))} <b>${v/1e6:.1f}M</b></span>' for m,v in mk)
    filas_sub += f"""<tr><td class="cod">{p}</td><td class="num dest">{info['cif']/1e6:,.1f}</td>
      <td class="num">{info['items']:,}</td><td class="gl">{esc(g)}<div class="mks">{chips}</div></td></tr>"""

# ranking
filas_rank = ""
for i,(m,v) in enumerate(top,1):
    pct = v/agg.most_common(1)[0][1]*100
    filas_rank += f"""<tr><td class="num">{i}</td><td class="mkc">{esc(m)}</td>
      <td class="num">{v/1e6:,.2f}</td>
      <td><div class="bar"><i style="width:{pct:.0f}%"></i></div></td></tr>"""

# meses
meses = sorted(d.get("por_mes",{}).items())
maxm = max(v for _,v in meses) if meses else 1
filas_mes = "".join(f'<div class="mes"><span class="ml">{esc(k[:14])}</span>'
  f'<div class="mbar"><i style="width:{v/maxm*100:.0f}%"></i></div>'
  f'<span class="mv">${v/1e6:,.2f}M</span></div>' for k,v in meses)

# competidores directos de SUPCON/Hobre en el nicho
NICHO = [("C-QUAND (XRF en línea)", "Análisis elemental en líquidos por fluorescencia de rayos X", "90273000 / 90275000"),
         ("PRISM (Raman)", "Composición de gas multicomponente", "90271010 / 90275000"),
         ("TISOMIC (PA-TDL)", "H2S, H2O y CO2 en gas y líquidos", "90271010 / 90278999"),
         ("WIM COMPAS", "Wobbe, poder calorifico, CARI", "90271010"),
         ("CEMS 5000", "Monitoreo continuo de emisiones", "90271010 / 90278000")]
filas_nicho = "".join(f'<tr><td class="fam">{esc(a)}</td><td>{esc(b)}</td><td class="cod">{esc(c)}</td></tr>' for a,b,c in NICHO)

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Analizadores de proceso en Chile 2025 — mercado medido</title>
<style>
:root{{--bg:#f8fafc;--card:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--tx);font-family:Inter,-apple-system,sans-serif;font-size:15px;line-height:1.6;padding:36px 26px 90px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:29px;font-weight:660;letter-spacing:-.7px;margin-bottom:8px}}
.sub{{color:var(--mu);font-size:15px;max-width:880px}}
.src{{margin-top:16px;padding:13px 17px;background:var(--acs);border-left:3px solid var(--ac);border-radius:10px;font-size:13.5px;color:#1e3a8a}}
h2{{font-size:19px;font-weight:640;margin:36px 0 6px}}
h2 small{{font-weight:400;color:var(--mu);font-size:14px}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:20px;padding:24px;margin-top:14px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--mu);padding:9px 10px;border-bottom:1px solid var(--bd);font-weight:600}}
td{{padding:11px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.num{{font-family:"IBM Plex Mono",ui-monospace,monospace;text-align:right;white-space:nowrap}}
.dest{{font-weight:650;font-size:14.5px}}
.cod{{font-family:"IBM Plex Mono",monospace;font-size:12.5px;white-space:nowrap}}
.fam{{font-weight:600}}
.gl{{font-size:13px;color:#334155}}
.mkc{{font-weight:600}}
.mks{{display:flex;flex-wrap:wrap;gap:6px;margin-top:7px}}
.mk{{background:var(--acs);color:#1e40af;border-radius:100px;padding:3px 10px;font-size:11.5px;white-space:nowrap}}
.mk b{{font-family:"IBM Plex Mono",monospace}}
.bar{{background:#f1f5f9;border-radius:100px;height:7px;overflow:hidden;min-width:80px}}
.bar i{{display:block;height:100%;background:var(--ac);border-radius:100px}}
.mes{{display:flex;align-items:center;gap:12px;margin-bottom:7px;font-size:13px}}
.ml{{width:110px;color:var(--mu);text-transform:capitalize}}
.mbar{{flex:1;background:#f1f5f9;border-radius:100px;height:9px;overflow:hidden}}
.mbar i{{display:block;height:100%;background:var(--ac);border-radius:100px}}
.mv{{width:82px;text-align:right;font-family:"IBM Plex Mono",monospace}}
.big{{display:flex;gap:32px;flex-wrap:wrap;margin:26px 0 8px;padding:22px 0;border-top:1px solid var(--bd);border-bottom:1px solid var(--bd)}}
.big .st b{{display:block;font-size:29px;font-weight:660;font-family:"IBM Plex Mono",monospace;letter-spacing:-1px}}
.big .st span{{font-size:11.5px;color:var(--mu);text-transform:uppercase;letter-spacing:.6px}}
.nota{{background:#fffbeb;border-left:3px solid var(--am);border-radius:10px;padding:15px 19px;font-size:13.5px;color:#78350f;margin-top:14px}}
ul{{margin:9px 0 0 20px;font-size:14px}} li{{margin-bottom:5px}}
code{{background:#f1f5f9;padding:2px 6px;border-radius:5px;font-size:12.5px;font-family:"IBM Plex Mono",monospace}}
.foot{{margin-top:34px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
</style></head><body><div class="wrap">

<h1>Analizadores de proceso en Chile — mercado 2025</h1>
<p class="sub">Medición del capítulo arancelario 90.27 (instrumentos de análisis físico y químico)
sobre las importaciones reales de Chile, separando analizador industrial de equipamiento
médico y de laboratorio clínico.</p>
<div class="src"><b>Fuente:</b> Registro de Importaciones (DIN) de Aduanas, 12 meses de 2025,
datos.gob.cl. Se procesaron <b>4.847.036</b> líneas y se aislaron las que caen en el capítulo
90.27. Valores en USD CIF declarado.</div>

<div class="big">
  <div class="st"><b>US${d['total_proceso_usd']/1e6:,.1f}M</b><span>Analizador de proceso</span></div>
  <div class="st"><b>US${d['total_excluido_usd']/1e6:,.1f}M</b><span>Médico / laboratorio</span></div>
  <div class="st"><b>9.138</b><span>Ítems de proceso</span></div>
  <div class="st"><b>0</b><span>SUPCON / Hobré</span></div>
</div>

<h2>Mercado por subpartida <small>solo analizador de proceso industrial</small></h2>
<div class="card"><table>
<thead><tr><th>Código</th><th style="text-align:right">USD CIF (M)</th>
<th style="text-align:right">Ítems</th><th>Glosa y proveedores</th></tr></thead>
<tbody>{filas_sub}
<tr><td class="cod"><b>TOTAL</b></td><td class="num dest"><b>{d['total_proceso_usd']/1e6:,.1f}</b></td>
<td class="num"><b>9.138</b></td><td></td></tr>
</tbody></table></div>

<h2>Proveedores <small>USD millones importados en 2025</small></h2>
<div class="card"><table>
<thead><tr><th>#</th><th>Fabricante</th><th style="text-align:right">USD CIF (M)</th><th>Participación</th></tr></thead>
<tbody>{filas_rank}</tbody></table></div>

<h2>Estacionalidad mensual</h2>
<div class="card">{filas_mes}</div>

<h2>Dónde compite cada analizador del catálogo</h2>
<div class="card"><table>
<thead><tr><th>Producto SUPCON / Hobré</th><th>Qué mide</th><th>Subpartidas donde cae</th></tr></thead>
<tbody>{filas_nicho}</tbody></table>
<div class="nota" style="margin-top:16px">
  <b>Sin presencia.</b> Ni SUPCON ni Hobré aparecen como marca declarada en el capítulo 90.27
  durante 2025. El nicho está ocupado por Endress+Hauser, MSA, Thermo Fisher, Metso, CIDRA,
  Hach, Waters, Shimadzu y Agilent.
</div></div>

<h2>Cómo se separó analizador industrial de equipamiento médico</h2>
<div class="card">
  <p style="font-size:14px">El capítulo 90.27 es el más contaminado del arancel: bajo el mismo
  código entran un analizador de gases de proceso y un reactivo de diagnóstico clínico.
  La clasificación se hizo en tres pasos, sobre la descripción y la marca declaradas:</p>
  <ul>
    <li><b>Analizador de proceso</b> (US${d['total_proceso_usd']/1e6:,.1f}M): descripción o marca
    de instrumento — analizador, cromatógrafo, espectrómetro, sensor, sonda, medidor,
    conductividad, detector de gas, XRF, Raman.</li>
    <li><b>Médico / laboratorio</b> (US${d['total_excluido_usd']/1e6:,.1f}M): reactivos,
    calibradores, diagnóstico in vitro, inmunoensayo, hematología, y las marcas Roche, Abbott,
    Beckman, Werfen, Stago, Cobas, Siemens Healthineers.</li>
    <li><b>Ambiguo</b> (US${d['total_revisar_usd']/1e6:,.1f}M): partes, accesorios, consumibles
    y servicios de mantención que no se pueden adscribir a proceso ni a clínico sin revisar
    el ítem caso a caso.</li>
  </ul>
  <p style="font-size:14px;margin-top:11px">El margen de error de esta separación es el
  <b>ambiguo</b>: es un piso y un techo, no un número exacto. El mercado de analizadores de
  proceso está entre US${d['total_proceso_usd']/1e6:,.0f}M y
  US${(d['total_proceso_usd']+d['total_revisar_usd'])/1e6:,.0f}M.</p>
</div>

<div class="foot">
  Fuente: Servicio Nacional de Aduanas — Registro de Importaciones (DIN) 2025, vía datos.gob.cl.<br>
  Procesamiento determinístico. Cada valor es USD CIF declarado por el importador.
</div>
</div></body></html>"""

OUT = os.path.join(BASE, "analizadores_2025.html")
open(OUT, "w", encoding="utf-8").write(HTML)
print("escrito:", OUT, len(HTML.encode()), "bytes")
print(f"proceso US${d['total_proceso_usd']/1e6:.1f}M | excluido US${d['total_excluido_usd']/1e6:.1f}M | ambiguo US${d['total_revisar_usd']/1e6:.1f}M")
