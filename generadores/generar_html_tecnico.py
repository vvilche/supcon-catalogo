#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera artefactos/plan_contacto_tecnico.html — jefes de planta y mantenimiento."""
import os, json, html
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(BASE,"datos")
OUT=os.path.join(BASE,"artefactos","plan_contacto_tecnico.html")
d=json.load(open(os.path.join(D,"plan_contacto_tecnico.json"),encoding="utf-8"))
C=d["cuentas"]; R=d["resumen"]

ZCOL={"Z1":"#2563eb","Z2":"#d97706","Z3":"#0891b2","Z4":"#7c3aed","Z5":"#059669","Z6":"#64748b","Z7":"#b45309"}
PERFIL_COL={"Jefe de Mantenimiento":"#7c3aed","Jefe de Planta":"#2563eb","Jefe de Producción":"#0891b2",
 "Jefe de Ingeniería":"#059669","Jefe de Instrumentación y Control":"#d97706","Superintendente":"#b45309",
 "Jefe Eléctrico":"#64748b","Ingeniero de Automatización":"#1d4ed8","Ingeniero de Procesos":"#047857",
 "Jefe de Calidad":"#7e22ce","Jefe de Medio Ambiente":"#059669"}

def miles(v,d_=0):
    if v is None: return "—"
    return f"{v:,.{d_}f}".replace(",","X").replace(".",",").replace("X",".")

# PERFIL AGRUPADO: el mismo perfil aparece con nombres ligeramente distintos
def perfil(t):
    tp=(t.get("tipo") or "")
    cg=(t.get("cargo") or "").lower()
    if tp=="jefe_mantenimiento" or "manten" in cg: return "Jefe de Mantenimiento"
    if tp=="jefe_planta" or "jefe de planta" in cg: return "Jefe de Planta"
    if tp=="jefe_produccion": return "Jefe de Producción"
    if tp=="jefe_ingenieria": return "Jefe de Ingeniería"
    if tp=="jefe_ic" or "instrumentac" in cg: return "Jefe de Instrumentación y Control"
    if tp=="jefe_electrico" or "electric" in cg: return "Jefe Eléctrico"
    if tp=="ingeniero_automatizacion" or "automatiz" in cg: return "Ingeniero de Automatización"
    if tp=="ingeniero_procesos": return "Ingeniero de Procesos"
    if tp=="superintendente": return "Superintendente"
    if tp=="jefe_calidad": return "Jefe de Calidad"
    return d["perfiles_incluidos"].get(tp, "Técnico")

filas=""
for i,p in enumerate(C[:80],1):
    ts=""
    for t in p["tomadores"][:3]:
        pf=perfil(t)
        li=f'<a class="li" href="{html.escape(t["linkedin"])}" target="_blank">LinkedIn</a>' if t.get("linkedin") else ''
        ts+=f'''<div class="tom"><b>{html.escape(str(t.get("nombre") or ""))}</b>
          <span class="cg">{html.escape(str(t.get("cargo") or "")[:52])}</span>
          <span class="pf" style="background:{PERFIL_COL.get(pf,'#64748b')}1a;color:{PERFIL_COL.get(pf,'#64748b')}">{html.escape(pf)}</span>{li}</div>'''
    zonas=", ".join(p.get("zonas") or [])
    filas+=f'''<article class="ct">
  <div class="ch">
    <span class="rk">{i}</span>
    <div class="nz"><b>{html.escape(str(p["empresa"])[:50])}</b>
      <span class="sub">{html.escape(str(p.get("comuna") or ""))} · {html.escape(str(p["rubro"])[:28])}</span></div>
    <span class="zn" style="background:{ZCOL.get(p.get("zona"),'#94a3b8')}1a;color:{ZCOL.get(p.get("zona"),'#64748b')}">{zonas or "multi"}</span>
    <div class="dl"><b>{p["dolor"]:.0f}</b><span>dolor/planta</span></div>
  </div>
  <div class="toms">{ts}</div>
  <div class="ang"><b>El problema que él ve</b> {html.escape(p["angulo"] or "sin señal específica")}</div>
  <div class="ln"><b>Lo que necesita</b> {html.escape(", ".join(p["lineas"][:4]) or "—")}</div>
</article>'''

perfiles="".join(f'''<div class="part"><div class="ph"><span>{html.escape(k)}</span><span class="pv">{v:,}</span></div>
  <div class="bar"><div class="fill" style="width:{max(v/max(R["por_perfil"].values())*100,3):.0f}%;background:{PERFIL_COL.get(k,'#64748b')}"></div></div></div>'''
  for k,v in sorted(R["por_perfil"].items(), key=lambda x:-x[1]))
zonas="".join(f'''<div class="part"><div class="ph"><span>{k}</span><span class="pv">{v:,}</span></div>
  <div class="bar"><div class="fill" style="width:{max(v/max(R["por_zona"].values())*100,3):.0f}%;background:{ZCOL.get(k,'#94a3b8')}"></div></div></div>'''
  for k,v in sorted(R["por_zona"].items(), key=lambda x:-x[1]) if k!="sin zona")

HTML=f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Contacto técnico — jefes de planta y mantenimiento</title><style>
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
.aviso{{background:#ecfdf5;border:1px solid #a7f3d0;border-left:4px solid #047857;border-radius:9px;padding:15px 18px;margin:15px 0;font-size:14px}}
.aviso b{{color:#047857}}
.warn{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:14px 0;font-size:14px}}
.warn b{{color:#92400e}}
.dos{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:22px}}
@media(max-width:760px){{.dos{{grid-template-columns:1fr}}}}
.card{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:17px 20px}}
.part{{margin-bottom:9px}}
.ph{{display:flex;justify-content:space-between;gap:10px;margin-bottom:4px;font-size:12.5px}}
.pv{{font-weight:700;font-variant-numeric:tabular-nums}}
.bar{{height:5px;background:#f1f5f9;border-radius:3px;overflow:hidden}}
.fill{{height:100%;border-radius:3px}}
.ct{{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:15px 19px;margin-bottom:11px}}
.ch{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:9px}}
.rk{{background:#eff6ff;color:#2563eb;font-weight:700;font-size:12px;border-radius:6px;padding:2px 9px;min-width:26px;text-align:center}}
.nz{{flex:1;min-width:200px}}
.nz b{{font-size:15.5px;font-weight:650;letter-spacing:-.2px}}
.sub{{display:block;font-size:11.5px;color:#94a3b8;font-weight:400}}
.zn{{font-size:11px;font-weight:700;border-radius:5px;padding:2px 8px}}
.dl{{text-align:right}}
.dl b{{display:block;font-size:19px;font-weight:700;color:#2563eb;font-variant-numeric:tabular-nums}}
.dl span{{font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:.3px}}
.toms{{display:flex;flex-direction:column;gap:5px;margin-bottom:9px}}
.tom{{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;font-size:13.5px}}
.tom b{{font-weight:600}}
.cg{{color:#64748b;font-size:12.5px}}
.pf{{font-size:10.5px;font-weight:700;border-radius:5px;padding:1px 7px}}
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

<h1>Contacto técnico: jefes de planta y mantenimiento</h1>
<p class="sub">El plan anterior priorizaba gerentes generales por peso del rol. Pero quien sufre el
problema y arma la especificación es el técnico. Acá están los {R["contactos_tecnicos"]:,} contactos
técnicos operativos, ordenados por el dolor de su planta.</p>

<div class="kpi">
  <div><b>{R["empresas"]:,}</b>empresas</div>
  <div><b>{R["contactos_tecnicos"]:,}</b>contactos técnicos</div>
  <div><b>{R["por_perfil"].get("Jefe de Mantenimiento",0):,}</b>jefes de mantenimiento</div>
  <div><b>{R["por_perfil"].get("Jefe de Planta",0):,}</b>jefes de planta</div>
  <div><b>{R["con_linkedin"]:,}</b>con LinkedIn</div>
</div>

<div class="aviso">
  <b>Por qué este orden y no el de gerencias.</b> El gerente general firma, pero no especifica.
  El jefe de mantenimiento es el que persigue el dato que no llega; el jefe de planta el que tiene
  el efluente sin medir; el jefe de I&C el que define el instrumento. <b>Para vender
  instrumentación y control, el técnico abre la puerta y el gerente firma después.</b>
  <br><br>
  Se excluyeron los perfiles de firma y comerciales: gerente general, gerente comercial,
  directorio, dueño, abastecimiento y gerente de proyectos.
</div>

<h2>Los perfiles que hay en la base</h2>
<div class="dos">
  <div class="card">
    <h3>Por perfil técnico</h3>
    {perfiles}
  </div>
  <div class="card">
    <h3>Por zona</h3>
    {zonas}
    <p style="font-size:12.5px;color:#64748b;margin-top:10px">Z4 (Biobío) y Z5 (sur acuícola)
    concentran más de la mitad: son las zonas donde el técnico de planta decide y el argumento
    es el mismo en cada cuenta.</p>
  </div>
</div>

<h2>Las 80 cuentas técnicas a llamar primero</h2>
{filas}

<h2>Cómo trabajarlos</h2>
<ul>
  <li><b>Al jefe de mantenimiento, por la confiabilidad y el dato que falta.</b> Es el perfil más
  numeroso ({R["por_perfil"].get("Jefe de Mantenimiento",0):,}) y el que primero nota que un
  instrumento no mide. El mensaje es sobre la mantención que hoy es a ciegas.</li>
  <li><b>Al jefe de I&C, con la especificación en la mano.</b> Es el perfil más chico
  ({R["por_perfil"].get("Jefe de Instrumentación y Control",0):,}) pero el más calificado: con él
  se habla de protocolo, rango y certificación, no de beneficios.</li>
  <li><b>Al jefe de planta, con el dolor operativo y su número.</b> Cermaq, Orizon, Corpesca,
  Carozzi y Blumar tienen jefe de planta identificado. El argumento es el efluente sin medir, con
  la cifra que sale del RETC.</li>
  <li><b>Y el caso ideal ya apareció:</b> en Linde Gas hay un <b>Ingeniero DCS &
  Instrumentación</b> identificado. Ese es el interlocutor exacto para el ECS-700.</li>
</ul>

<footer>
  Fuentes: dolor de <b>RETC del MMA</b> y <b>Coordinador Eléctrico</b>; contactos del catálogo de
  prospección CONECTA. Perfiles técnicos operativos filtrados de {R["contactos_tecnicos"]:,} personas
  con nombre y cargo. Correos y teléfonos no están en la fuente (el contacto es por LinkedIn).
  <br>Ver <a href="plan_contacto.html">plan general</a> ·
  <a href="estrategia_territorial.html">estrategia territorial</a> ·
  <a href="universo_prospeccion.html">universo</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div></body></html>"""
open(OUT,"w",encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print("cuentas:", len(C[:80]))
