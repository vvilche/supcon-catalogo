#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/objetivos_priorizados.html — el cruce estrategico."""
import os, json, html
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"artefactos","objetivos_priorizados.html")
d=json.load(open(os.path.join(D,"cruce_estrategico_objetivos.json"),encoding="utf-8"))
PROC=[c for c in d["cuentas"] if c["es_proceso_continuo"]]
NOPROC=[c for c in d["cuentas"] if not c["es_proceso_continuo"]]

def usd(v):
    if not v: return "-"
    return "US$" + f"{v/1e6:,.1f}".replace(",","X").replace(".",",").replace("X",".")

ZN={"Z1":"Santiago (RM)","Z2":"Norte minero","Z3":"Valparaíso-Quintero","Z4":"Concepción-Biobío",
    "Z5":"Sur acuícola","Z6":"Coquimbo-Atacama","multi":"Multirregional","-":"sin clasificar",None:"sin clasificar"}

def tarjeta(c,i):
    sen=[]
    if c["estado_participacion"]=="verificado": sen.append('<span class="ch v">capital chino verificado</span>')
    elif c["estado_participacion"]=="parcial": sen.append('<span class="ch p">participación parcial</span>')
    if c["zona"]: sen.append(f'<span class="ch z">{ZN.get(c["zona"],c["zona"])}</span>')
    if c["es_epc"]: sen.append('<span class="ch e">EPC — especifica sin licitación</span>')
    if c["lineas_norma"]: sen.append('<span class="ch n">disparador normativo directo</span>')
    elif c["lineas_por_industria"]: sen.append('<span class="ch n">norma aplicable por industria</span>')
    if c["zona_por"]=="operacion": sen.append('<span class="ch o">planta en la zona</span>')
    normas=""
    if c["normas"]:
        normas=f'<div class="det"><b>Norma que obliga</b> {" · ".join(html.escape(n) for n in c["normas"])}</div>'
    linea_norma=""
    ls=sorted(set(c["lineas_norma"]+c["lineas_por_industria"]))
    if ls:
        linea_norma=f'<div class="det"><b>Línea que entra</b> {html.escape(", ".join(ls))}</div>'
    falt=""
    if c["senales_faltantes"]:
        falt=f'<div class="falta">Sin dato: {html.escape(", ".join(c["senales_faltantes"]))}</div>'
    web=f'<div class="det"><b>Web</b> <a href="{html.escape(c["web"] or "")}">{html.escape(c["web"] or "")}</a></div>' if c.get("web") else ""
    return f'''<article class="cuenta">
  <div class="cab"><span class="rank">{i}</span><h3>{html.escape(c["nombre"] or "")}</h3>
    <span class="score">{c["score"]:.0f}</span></div>
  <div class="chips">{"".join(sen)}</div>
  <div class="det"><b>Dueño chino</b> {html.escape(c["grupo_chino"] or "")}</div>
  <div class="det"><b>Participación</b> {html.escape(str(c["participacion"] or ""))[:170]}</div>
  {linea_norma}{normas}
  <div class="det"><b>Productos SUPCON</b> {html.escape(", ".join(c["productos_supcon"] or []))}</div>
  {web}{falt}
  <div class="razon">{html.escape(c["razon_prioridad_original"] or "")}</div>
</article>'''

tproc="".join(tarjeta(c,i) for i,c in enumerate(PROC,1))
tnop="".join(f'<li>{html.escape(c["nombre"] or "")} — {html.escape((c["grupo_chino"] or "")[:60])}</li>' for c in NOPROC)
res=d["resumen"]

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Objetivos priorizados — SUPCON Chile</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:1000px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:870px}}
h2{{font-size:20px;font-weight:660;margin:34px 0 12px;letter-spacing:-.2px}}
p{{margin-bottom:11px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:16px 19px;margin:16px 0;font-size:14px}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:14px 0;font-size:14px}}
.aviso b{{color:#92400e}}
.cuenta{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:17px 20px;margin-bottom:13px}}
.cab{{display:flex;align-items:baseline;gap:12px;margin-bottom:9px;flex-wrap:wrap}}
.rank{{background:#eff6ff;color:#2563eb;font-weight:700;font-size:13px;border-radius:7px;padding:3px 10px;min-width:28px;text-align:center}}
.cab h3{{font-size:16.5px;font-weight:650;flex:1;letter-spacing:-.2px}}
.score{{font-size:19px;font-weight:700;color:#2563eb;font-variant-numeric:tabular-nums}}
.chips{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:11px}}
.ch{{font-size:11px;border-radius:6px;padding:3px 10px;font-weight:600;border:1px solid}}
.ch.v{{background:#ecfdf5;color:#047857;border-color:#a7f3d0}}
.ch.p{{background:#fffbeb;color:#b45309;border-color:#fde68a}}
.ch.z{{background:#eff6ff;color:#1d4ed8;border-color:#bfdbfe}}
.ch.e{{background:#faf5ff;color:#7e22ce;border-color:#e9d5ff}}
.ch.n{{background:#f0fdf4;color:#15803d;border-color:#bbf7d0}}
.ch.o{{background:#f8fafc;color:#475569;border-color:#e2e8f0}}
.det{{font-size:13.5px;color:#475569;margin-bottom:5px;line-height:1.55}}
.det b{{color:#0f172a;font-weight:600}}
.falta{{font-size:12.5px;color:#b45309;background:#fffbeb;border-radius:6px;padding:5px 10px;margin-top:7px;display:inline-block}}
.razon{{font-size:13px;color:#64748b;border-top:1px solid #f1f5f9;padding-top:9px;margin-top:9px;line-height:1.6}}
ul{{list-style:none;margin:9px 0}}
ul li{{position:relative;padding-left:17px;margin-bottom:5px;font-size:13.5px;color:#475569}}
ul li:before{{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:#94a3b8}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Objetivos priorizados</h1>
<p class="sub">El cruce de las cuatro señales: disparador normativo, zona geográfica, capital chino
y encaje de catálogo. Es el paso que faltaba: la estrategia de penetración existía por un lado y
los cruces por otro. Acá están unidos en una lista de cuentas concreta.</p>

<div class="kpi">
  <div><b>{res["cuentas"]}</b>empresas con capital chino</div>
  <div><b>{len(PROC)}</b>de proceso continuo</div>
  <div><b>{res["con_disparador_normativo"]}</b>con disparador normativo</div>
  <div><b>{res["epcs"]}</b>EPC chinos</div>
  <div><b>{res["en_zona_prioritaria"]}</b>en zona Z1-Z4</div>
</div>

<div class="metodo">
  <b>Cómo se prioriza.</b> Cada cuenta recibe puntaje por cuatro señales medidas:
  <b>capital chino</b> (hasta 25, según participación verificada), <b>encaje de catálogo</b>
  (hasta 24, cuántas líneas SUPCON aplican), <b>geografía</b> (hasta 18, y pesa más si la
  <i>planta</i> está en la zona y no solo la casa matriz) y <b>normativa</b> (hasta 42 si hay una
  norma que obliga a comprar lo que SUPCON vende, no solo una norma del rubro).
  <br><br>
  <b>Por qué el capital chino es la señal más fuerte.</b> Un EPC chino especifica la
  instrumentación, el PLC y los tableros sin licitación abierta, y da acceso a varios activos a
  la vez. Es la puerta más rápida que existe.
</div>

<div class="aviso">
  <b>Lo que se descartó, y por qué.</b> De las 34 empresas con capital chino, <b>17 no son de
  proceso continuo</b>: viñas, automotrices, telecomunicaciones y retail. SUPCON vende a proceso
  industrial, así que se conservan en el listado por completitud pero <b>no se priorizan</b>.
  También se corrigió la geografía: una empresa con la matriz en Las Condes y la faena en
  Antofagasta se visita en Antofagasta. Y <b>7 cuentas son multirregionales</b> (CGE, Transelec,
  Codelco): no se les asigna una zona porque forzarla sería inventar.
</div>

<h2>Las {len(PROC)} cuentas de proceso continuo, priorizadas</h2>
{tproc}

<h2>Con capital chino pero fuera de rubro</h2>
<p>Se listan para que no se pierdan, pero no son cuentas de automatización de proceso:</p>
<ul>{tnop}</ul>

<h2>Las cuatro señales, y de dónde sale cada una</h2>
<div class="metodo">
  <b>1. Normativa</b> — de <code>cruce_normativo_estrategia.json</code>. 26 empresas tienen un
  disparador normativo identificado. El CEMS obligatorio (DS 13/2011) para generación sobre
  50 MWt es el más directo.<br>
  <b>2. Geografía</b> — de <code>mapa_oportunidades_chile.json</code>. Z1 a Z6, con la operación
  pesando más que la sede.<br>
  <b>3. Capital chino</b> — de <code>empresas_capital_chino_chile.json</code>. 28 de 34 con
  participación verificada por fuente.<br>
  <b>4. Catálogo</b> — de <code>cobertura_catalogo.json</code>. Cuántas de las 7 líneas SUPCON
  aplican a la operación declarada.
</div>

<footer>
  Cada señal sale de uno de los tres JSON con su fuente. Donde no hay dato, la cuenta lo declara
  en vez de recibir un puntaje estimado.
  <br>Ver <a href="estrategia_normativa.html">dónde hay dolor normativo</a> ·
  <a href="mapa_oportunidades.html">mapa geográfico</a> ·
  <a href="empresas_chinas_chile.html">empresas con capital chino</a> ·
  <a href="estrategia_penetracion.html">estrategia de penetración</a> ·
  <a href="escalera_exito.html">escalera al éxito</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
