#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/plan_contacto.html — a quién llamar, con nombre y cargo."""
import os, json, html
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"artefactos","plan_contacto.html")
d=json.load(open(os.path.join(D,"plan_contacto.json"),encoding="utf-8"))
P=d["plan"]; R=d["resumen"]

def miles(v,d_=0):
    if v is None: return "—"
    return f"{v:,.{d_}f}".replace(",","X").replace(".",",").replace("X",".")

COLR={"Aprobador":"#7c3aed","Decisor":"#2563eb","Comprador técnico":"#0891b2","Recomendador":"#64748b"}
ZCOL={"Z1":"#2563eb","Z2":"#d97706","Z3":"#0891b2","Z4":"#7c3aed","Z5":"#059669","Z6":"#64748b","Z7":"#b45309"}

filas=""
for i,p in enumerate(P[:100],1):
    cp=p["contacto_principal"]
    ts="".join(f'''<div class="tom"><b>{html.escape(str(t.get("nombre") or ""))}</b>
      <span class="cg">{html.escape(str(t.get("cargo") or "")[:44])}</span>
      <span class="rl" style="background:{COLR.get(d["rol_compra"].get(t.get("rol_compra"),"?"),"#64748b")}1a;color:{COLR.get(d["rol_compra"].get(t.get("rol_compra"),"?"),"#64748b")}">{html.escape(d["rol_compra"].get(t.get("rol_compra"),"?"))}</span>
      {f'<a class="li" href="{html.escape(t["linkedin"])}" target="_blank">LinkedIn</a>' if t.get("linkedin") else ''}</div>'''
      for t in p["tomadores"][:3])
    zonas=", ".join(p.get("zonas") or [])
    filas+=f'''<article class="ct">
  <div class="ch">
    <span class="rk">{i}</span>
    <div class="nz"><b>{html.escape(str(p["empresa"])[:52])}</b>
      <span class="sub">{html.escape(str(p.get("comuna") or ""))} · {html.escape(str(p["rubro"])[:30])} · {p["n_plantas"]} planta{"s" if p["n_plantas"]!=1 else ""}</span></div>
    <span class="zn" style="background:{ZCOL.get(p.get("zona"),'#94a3b8')}1a;color:{ZCOL.get(p.get("zona"),'#64748b')}">{zonas or "multi"}</span>
    <div class="dl"><b>{p["dolor"]:.0f}</b><span>dolor/planta</span></div>
  </div>
  <div class="tomadores">{ts}</div>
  <div class="ang"><b>Qué decirle</b> {html.escape(p["angulo"] or "sin señal específica")}</div>
  <div class="ln"><b>Producto</b> {html.escape(", ".join(p["lineas"][:4]) or "—")}</div>
</article>'''

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Plan de contacto — a quién llamar</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--am:#d97706}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}}
.wrap{{max-width:1080px;margin:0 auto}}
h1{{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}}
.sub{{color:var(--mu);font-size:14.5px;margin-bottom:24px;max-width:880px}}
h2{{font-size:20px;font-weight:660;margin:34px 0 12px;letter-spacing:-.2px}}
h3{{font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--mu);font-weight:700;margin:16px 0 8px}}
p{{margin-bottom:10px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
.kpi div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:11px 16px;font-size:12.5px;color:var(--mu)}}
.kpi b{{display:block;font-size:21px;font-weight:700;color:var(--tx);letter-spacing:-.4px}}
.metodo{{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:16px 19px;margin:16px 0;font-size:14px}}
.warn{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:14px 0;font-size:14px}}
.warn b{{color:#92400e}}
.ct{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:15px 19px;margin-bottom:11px}}
.ch{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:9px}}
.rk{{background:#eff6ff;color:#2563eb;font-weight:700;font-size:12px;border-radius:6px;padding:2px 9px;min-width:26px;text-align:center}}
.nz{{flex:1;min-width:220px}}
.nz b{{font-size:15.5px;font-weight:650;letter-spacing:-.2px}}
.sub{{display:block;font-size:11.5px;color:#94a3b8;font-weight:400}}
.zn{{font-size:11px;font-weight:700;border-radius:5px;padding:2px 8px}}
.dl{{text-align:right}}
.dl b{{display:block;font-size:19px;font-weight:700;color:#2563eb;font-variant-numeric:tabular-nums}}
.dl span{{font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:.3px}}
.tomadores{{display:flex;flex-direction:column;gap:5px;margin-bottom:9px}}
.tom{{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;font-size:13.5px}}
.tom b{{font-weight:600}}
.cg{{color:#64748b;font-size:12.5px}}
.rl{{font-size:10.5px;font-weight:700;border-radius:5px;padding:1px 7px}}
.li{{font-size:11.5px;color:#2563eb;text-decoration:none;border:1px solid #bfdbfe;border-radius:5px;padding:1px 7px}}
.ang{{font-size:12.5px;color:#475569;background:#fbfdff;border-left:3px solid #d97706;padding:6px 11px;border-radius:5px;margin-bottom:5px}}
.ang b,.ln b{{color:#0f172a;font-size:11px;text-transform:uppercase;letter-spacing:.4px;margin-right:6px}}
.ln{{font-size:12.5px;color:#64748b}}
ul{{list-style:none}}
ul li{{position:relative;padding-left:17px;margin-bottom:7px}}
ul li:before{{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}}
footer{{margin-top:38px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Plan de contacto: a quién llamar</h1>
<p class="sub">Las cuentas con dolor medido cruzadas con los tomadores de decisión identificados.
Cada llamada trae el nombre, el cargo, el rol que juega en la compra y qué decirle.</p>

<div class="kpi">
  <div><b>{R["empresas_con_tomador"]:,}</b>empresas con contacto</div>
  <div><b>{R["total_tomadores"]:,}</b>tomadores en total</div>
  <div><b>{R["con_linkedin"]:,}</b>con LinkedIn</div>
  <div><b>{R["por_rol"].get("Decisor",0):,}</b>decisores</div>
  <div><b>{R["por_rol"].get("Aprobador",0):,}</b>aprobadores</div>
</div>

<div class="metodo">
  <b>Cómo se arma el orden.</b> La prioridad es <b>dolor por planta × peso del rol</b>: llegar al
  que decide vale más que al que recomienda. El dolor se mide por <b>promedio de planta</b>, no
  por suma — si sumara, una cadena con 105 estaciones de servicio pequeñas superaría a Codelco
  con 11 plantas industriales. Una empresa con muchas plantas sube un poco (más volumen de
  proyecto), con peso acotado.
  <br><br>
  <b>Los roles de compra</b>, tal como vienen clasificados:
  <b>Aprobador</b> (firma el gasto) · <b>Decisor</b> (elige la solución) ·
  <b>Comprador técnico</b> (evalúa y especifica) · <b>Recomendador</b> (influye).
</div>

<div class="warn">
  <b>Lo que este plan NO trae, y hay que conseguir.</b> Los {R["total_tomadores"]:,} tomadores
  vienen con <b>nombre, cargo y LinkedIn (91%), pero con correo y teléfono vacíos</b> — verificado
  en las {R["total_tomadores"]:,} fichas. El enriquecimiento de correo es un paso aparte.
  <br><br>
  Y de las 6.945 empresas del universo, <b>{R["empresas_sin_tomador"]:,} no tienen ningún contacto
  identificado</b>: son las que quedan para la segunda ola, cuando se pase a buscar el nombre.
</div>

<h2>Las 100 cuentas a llamar primero</h2>
{filas}

<h2>Cómo usar esto</h2>
<ul>
  <li><b>Empiece por el Aprobador cuando el dolor es alto.</b> Colbún, ENAP, Codelco y Ventisqueros
  tienen Gerente General o Gerente Corporativo identificado y dolor 90: en esos casos el mensaje
  es de nivel dirección, no técnico.</li>
  <li><b>Cuando el Decisor es de planta, vaya por el dolor operativo.</b> Cermaq tiene Gerente de
  Planta; ahí el argumento es el efluente que no se mide, no el presupuesto de capital.</li>
  <li><b>El clúster salmonero de Z5 es el más trabajable.</b> Nueve de las primeras veinticinco son
  pesqueras con el mismo problema de RILES: un caso de referencia sirve para todo el gremio.</li>
  <li><b>Y el contacto principal es el de más peso, pero están los demás.</b> Cada cuenta muestra
  hasta tres tomadores: el vendedor puede escalar si el primero no responde.</li>
</ul>

<footer>
  Fuentes: dolor de <b>RETC del MMA</b> (emisiones al agua y residuos peligrosos) y
  <b>Coordinador Eléctrico</b>; tomadores del <b>catálogo de prospección CONECTA</b> ({R["total_tomadores"]:,}
  personas con nombre y cargo). El cruce es por razón social normalizada. Los correos y teléfonos
  no están en la fuente y se declaran como faltantes.
  <br>Ver <a href="estrategia_territorial.html">estrategia territorial</a> ·
  <a href="universo_prospeccion.html">universo de prospección</a> ·
  <a href="objetivos_priorizados.html">objetivos priorizados</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print("cuentas:", len(P[:100]), "| con tomador en pagina:", filas.count('class="ct"'))
