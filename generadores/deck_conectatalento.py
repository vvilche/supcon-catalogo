#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deck real — Workshop ConectaTalento 2026, Facultad de Ingeniería PUCV.

15 slides, 15 minutos. Marca CONECTA real (extraída de conecta.cl /v2/assets/css/main.min.css):
  navy-deep #0A1628 · navy #0F1F3D · blue-accent #2563eb · outFit + Inter
  logo = punto azul + "CONECTA S.A."

Contenido = el guion aprobado en artefactos/guion_conectatalento_2026.html.
Navegación ← → / espacio. Cada slide mide 16:9 (1280x720 escalable).
"""
import os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "artefactos", "deck_conectatalento_2026.html")


def esc(x):
    return html.escape(str(x))


def logo(on_dark=True):
    """Logo real CONECTA (verde #0A8439), extraido de 'Logo Conecta.pdf'.
    Dos archivos: transparente para fondo oscuro, sobre-blanco para fondo claro."""
    f = "img/conecta_logo.png" if on_dark else "img/conecta_logo_claro.png"
    return f'<img class="logo" src="{f}" alt="CONECTA Ingeniería S.A.">'


# ============================================================ SLIDES
# tipo: cover | light | dark | stats | split | quote
S = []

S.append(dict(tipo="cover", kicker="Workshop ConectaTalento 2026 · 3ª edición",
              h1="Lo que viene en los<br>próximos veinte años",
              sub="Y por qué conviene empezar acá",
              foot="Víctor Vilche · Ingeniero Eléctrico · CEO CONECTA<br>"
                   "Facultad de Ingeniería PUCV · 20 de octubre de 2026"))

S.append(dict(tipo="light", kicker="El punto de partida",
              h1="Están a punto de titularse.<br>La próxima decisión es esta.",
              body=[
                  ("La práctica y el primer trabajo no son trámites",
                   "Son la primera decisión de carrera. Y no la define el primer sueldo."),
                  ("Les quedan cuarenta años de trabajo", 
                   "La pregunta no es qué hay hoy. Es dónde estará el trabajo que siga existiendo en 2046."),
              ]))

S.append(dict(tipo="dark", kicker="Tendencia 1 · Energía",
              h1="La demanda eléctrica<br>se duplica al 2035",
              stats=[("106", "TWh", "escenario medio"), ("117", "TWh", "escenario alto"),
                     ("149", "TWh", "con hidrógeno verde")],
              foot="Fuente: Coordinador Eléctrico Nacional, proyección de demanda del SEN"))

S.append(dict(tipo="light", kicker="Tendencia 2 · Inversión",
              h1="US$ 104.549 millones<br>en minería al 2034",
              body=[("51 proyectos", "Plantas, moliendas, fundiciones, relaves, puertos, líneas eléctricas."),
                    ("Cada uno necesita", "Un DCS, protecciones, instrumentación, una subestación y un equipo que lo ponga en marcha.")],
              foot="Fuente: Cochilco, cartera de proyectos mineros 2025-2034"))

S.append(dict(tipo="dark", kicker="Tendencia 3 · Personas",
              h1="Faltan 37.000 personas.<br>Y el 75% en cuatro perfiles",
              stats=[("~37.000", "", "nuevos trabajadores al 2034"),
                     ("73-75%", "", "en 4 perfiles"),
                     ("88%", "", "son reemplazos, no proyectos nuevos")],
              body_after="Mantenedor mecánico · Mantenedor eléctrico · Operador de equipo móvil · Operador de equipo fijo",
              foot="Fuente: CCM-Eleva / Consejo Minero, estudio de fuerza laboral"))

S.append(dict(tipo="light", kicker="Tendencia 4 · El oficio",
              h1="El ingeniero ya no trabaja solo",
              body=[("Antes", "El dato estaba en un tablero y en un papel. Se decidía con lo que se veía."),
                    ("Hoy", "Hay miles de señales por planta que nadie ocupa. Decide el que sabe qué preguntar.")],
              pull="La diferencia entre un ingeniero bueno y uno muy bueno ya no es calcular. Es saber qué dato importa."))

S.append(dict(tipo="dark", kicker="Tres caminos",
              h1="En CONECTA hay tres formas<br>de ser ingeniero",
              body=[("POWER", "La red, la subestación y la protección. El sistema eléctrico."),
                    ("PROCESOS", "El interior de la planta. El proceso industrial."),
                    ("VENTAS TÉCNICAS", "El ingeniero que entiende al cliente y sabe qué venderle.")],
              foot="No es el mismo trabajo. Conviene saber a cuál apuntar."))

S.append(dict(tipo="split", kicker="Línea POWER", acento="blue",
              h1="La red, la subestación,<br>la protección",
              items=["Subestaciones eléctricas", "Protecciones y ajustes",
                     "RTU y SCADA", "Calidad de energía", "Sincronización por satélite",
                     "Comunicaciones industriales"],
              rep="NovaTech · Vizimax · Belden / Hirschmann",
              perfil="Eléctrica · Electrónica · Control",
              nota="Un ajuste mal puesto apaga media ciudad."))

S.append(dict(tipo="split", kicker="Línea PROCESOS", acento="green",
              h1="El interior de la planta,<br>con SUPCON",
              items=["DCS ECS-700 y SIS TCS-500", "Instrumentación", "Válvulas y posicionadores",
                     "Analizadores y CEMS", "Optimización avanzada", "Predictivo y capa de datos"],
              rep="SUPCON",
              perfil="Mecánica · Química · Electrónica · Eléctrica",
              nota="Se aprende la planta, no el equipo. Por qué se rompe, no solo que se rompió."))

S.append(dict(tipo="split", kicker="Ventas Técnicas", acento="orange",
              h1="El ingeniero que vende<br>no deja de ser ingeniero",
              items=["Visitar plantas y subestaciones", "Levantar el requerimiento real",
                     "Armar la propuesta técnica y económica", "Cotizar y sustentar el precio",
                     "Acompañar la puesta en marcha"],
              rep="Lo que tiene que saber: el equipo, el proceso del cliente, costos y márgenes",
              perfil="Eléctrica · Mecánica · Química · cualquier especialidad con base técnica",
              nota="Se vende lo que se entiende. Sin base técnica, la venta es de intermediario."))


S.append(dict(tipo="light", kicker="Dónde se aprende",
              h1="En terreno, no en un PowerPoint",
              body=[("A la minera", "Con el ruido, el polvo y el turno de noche."),
                    ("A la subestación", "Con el plano en la mano y el equipo energizado."),
                    ("A la planta", "Cuando algo falla y hay que resolverlo ahora.")],
              pull="Eso no lo enseña la universidad. Y no se aprende leyendo."))

S.append(dict(tipo="dark", kicker="Cómo crecemos",
              h1="No se entra a un puesto:<br>se construye uno",
              body=[("En una empresa grande", "Hay un organigrama y un lugar reservado."),
                    ("Acá", "El organigrama se escribe con los que llegan.")],
              pull="Es más difícil. Y es la mejor escuela que hay."))

S.append(dict(tipo="light", kicker="Lo que buscamos", h1="No buscamos el mejor promedio",
              body=[("El promedio", "Dice que alguien sabe memorizar."),
                    ("Lo que miramos", "Que le importe hacer bien las cosas, que pregunte cuando no entiende y que se haga cargo.")],
              pull="En diez años, el que se destacó no fue el que sabía más. Fue el que se hizo cargo."))

S.append(dict(tipo="quote", kicker="Actitud y liderazgo",
              h1="El liderazgo empieza<br>el primer día",
              items=[("Se hace cargo", "Cuando algo sale mal, la primera frase no es 'fue el otro'."),
                     ("Pregunta", "'No lo sé, lo averiguo y te aviso' vale más que una respuesta inventada."),
                     ("Cumple", "Si dijiste a las 8, a las 7:50 estás. El liderazgo es que tu palabra valga."),
                     ("Le importa", "Anotar el dato que te pidieron aunque nadie te esté mirando.")]))

S.append(dict(tipo="dark", kicker="Por qué CONECTA",
              h1="Hacemos la pega completa",
              body=[("Vendemos", "Elegimos la tecnología."),
                    ("Diseñamos", "Calculamos e ingenierizamos."),
                    ("Instalamos", "Ponemos el equipo en terreno."),
                    ("Ponemos en marcha", "Y respondemos por el resultado.")],
              pull="No tercerizamos el problema."))

S.append(dict(tipo="cover", kicker="La invitación",
              h1="Hagan la práctica acá",
              sub="No para quedarse para siempre.<br>Para saber lo que es la ingeniería de verdad.",
              foot="Los espero en el MatchUp con un desafío real.<br><b>Víctor Vilche · CEO · CONECTA</b>"))


def render(s):
    t = s["tipo"]
    kick = f'<div class="kicker">{s["kicker"]}</div>' if s.get("kicker") else ""
    h1 = f'<h1>{s["h1"]}</h1>' if s.get("h1") else ""

    if t == "cover":
        inner = f'''{logo(True)}<div class="coverbox">{kick}{h1}
          <div class="sub">{s.get("sub","")}</div></div>
          <div class="coverfoot">{s.get("foot","")}</div>'''

    elif t in ("light", "dark"):
        cuerpo = ""
        if s.get("body"):
            cuerpo += '<div class="pairs">' + "".join(
                f'<div class="pair"><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a, b in s["body"]) + "</div>"
        if s.get("stats"):
            cuerpo += '<div class="stats">' + "".join(
                f'<div class="st"><span class="sv">{esc(v)}</span><span class="su">{esc(u)}</span>'
                f'<span class="sl2">{esc(l)}</span></div>' for v, u, l in s["stats"]) + "</div>"
        if s.get("body_after"):
            cuerpo += f'<div class="after">{esc(s["body_after"])}</div>'
        if s.get("pull"):
            cuerpo += f'<div class="pull">{s["pull"]}</div>'
        foot = f'<div class="foot">{s.get("foot","")}</div>' if s.get("foot") else ""
        inner = f'{logo(t == "dark")}{kick}{h1}{cuerpo}{foot}'

    elif t == "split":
        items = "".join(f"<li>{esc(x)}</li>" for x in s["items"])
        inner = f'''{logo(False)}{kick}{h1}
          <div class="splitbox">
            <div class="scol"><ul class="icheck">{items}</ul></div>
            <div class="scol meta">
              <div class="mi"><b>Representamos</b><span>{esc(s["rep"])}</span></div>
              <div class="mi"><b>Perfiles que entran</b><span>{esc(s["perfil"])}</span></div>
              <div class="note ac-{s["acento"]}">{esc(s["nota"])}</div>
            </div>
          </div>'''

    elif t == "quote":
        items = "".join(
            f'<div class="qi"><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a, b in s["items"])
        inner = f'{logo(False)}{kick}{h1}<div class="qgrid">{items}</div>'

    else:
        inner = logo(False)

    cls = f"slide s-{t}"
    if t == "split":
        cls += f" ac-{s['acento']}"
    return f'<section class="{cls}">{inner}<div class="num"></div></section>'


slides_html = "\n".join(render(s) for s in S)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CONECTA · Workshop ConectaTalento 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#0A1628;--navy2:#0F1F3D;--royal:#1E3A5F;--blue:#2563eb;--blueh:#1d4ed8;
--green:#10B981;--orange:#F26522;--tx:#0F172A;--tx2:#475569;--tx3:#94A3B8;
--bg:#fff;--bg2:#F1F5F9;--bg3:#F8FAFC;--bd:#E2E8F0}}
html,body{{height:100%;overflow:hidden;background:var(--navy)}}
body{{font-family:'Inter',sans-serif;color:var(--tx)}}
#stage{{position:fixed;inset:0;display:grid;place-items:center}}
.slide{{position:absolute;width:1280px;height:720px;padding:64px 76px;opacity:0;visibility:hidden;
transform:scale(.985);transition:opacity .32s ease,transform .32s ease,visibility .32s;
display:flex;flex-direction:column;overflow:hidden}}
.slide.on{{opacity:1;visibility:visible;transform:scale(1)}}
.s-light{{background:var(--bg);color:var(--tx)}}
.s-dark{{background:var(--navy);color:#F1F5F9}}
.s-cover{{background:var(--navy);color:#F1F5F9}}
.s-split{{background:var(--bg);color:var(--tx)}}
.s-quote{{background:var(--bg3);color:var(--tx)}}

/* logo */
img.logo{{display:block!important;height:62px!important;width:auto!important;
max-width:260px!important;margin-bottom:auto!important;align-self:flex-start!important;
flex:0 0 auto!important;object-fit:contain!important}}
.s-split img.logo,.s-quote img.logo{{height:56px!important}}
/* en slides claras el logo positivo (verde+blanco) ya funciona: no invertir */

.kicker{{font-family:'Outfit',sans-serif;font-size:13px;font-weight:700;letter-spacing:1.6px;
text-transform:uppercase;color:var(--blue);margin-bottom:18px}}
.s-dark .kicker,.s-cover .kicker{{color:#60a5fa}}
.ac-green .kicker{{color:var(--green)}}
.ac-orange .kicker{{color:var(--orange)}}
.ac-orange .icheck li:before{{background:var(--orange)}}
.ac-orange .note{{background:#fff7ed;color:#9a3412}}

h1{{font-family:'Outfit',sans-serif;font-size:52px;font-weight:700;line-height:1.1;
letter-spacing:-1.4px;margin-bottom:34px}}
.s-cover h1{{font-size:64px;letter-spacing:-2px;margin-bottom:22px;max-width:15ch}}
.s-quote h1,.s-split h1{{font-size:44px;margin-bottom:30px}}

.coverbox{{margin-top:auto;margin-bottom:auto}}
.sub{{font-size:22px;color:#94a3b8;line-height:1.55;font-weight:400;max-width:26ch}}
.coverfoot{{font-size:14.5px;color:#64748b;line-height:1.75;border-top:1px solid #1e293b;padding-top:20px}}
.coverfoot b{{color:#e2e8f0}}

/* pares */
.pairs{{display:grid;gap:22px;margin-bottom:26px}}
.pair{{border-left:3px solid var(--blue);padding-left:20px}}
.pair b{{display:block;font-family:'Outfit',sans-serif;font-size:22px;font-weight:600;margin-bottom:5px}}
.pair p{{font-size:16.5px;color:var(--tx2);line-height:1.6}}
.s-dark .pair p{{color:#94a3b8}}
.s-dark .pair{{border-left-color:#3b82f6}}

/* stats */
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:24px}}
.st{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
border-radius:14px;padding:24px 22px}}
.s-light .st{{background:var(--bg3);border-color:var(--bd)}}
.sv{{display:block;font-family:'Outfit',sans-serif;font-size:46px;font-weight:800;
color:#fff;letter-spacing:-1.5px;line-height:1}}
.s-light .sv{{color:var(--blue)}}
.su{{font-size:18px;font-weight:600;color:#60a5fa;margin-left:5px}}
.sl2{{display:block;font-size:13.5px;color:#94a3b8;margin-top:9px;line-height:1.4}}
.s-light .sl2{{color:var(--tx2)}}
.sl2:first-letter{{text-transform:uppercase}}

.after{{font-size:15px;color:#cbd5e1;background:rgba(37,99,235,.15);border-radius:10px;
padding:14px 20px;line-height:1.6;border-left:3px solid var(--blue)}}

.pull{{font-family:'Outfit',sans-serif;font-size:23px;font-weight:500;line-height:1.5;
color:var(--navy);background:#eff6ff;border-left:4px solid var(--blue);border-radius:0 12px 12px 0;
padding:22px 26px;margin-top:20px}}
.s-dark .pull{{background:rgba(37,99,235,.14);color:#e2e8f0}}

.foot{{font-size:12.5px;color:#94a3b8;margin-top:auto;padding-top:16px;border-top:1px solid var(--bd)}}
.s-dark .foot{{border-top-color:#1e293b;color:#64748b}}

/* split */
.splitbox{{display:grid;grid-template-columns:1.15fr .85fr;gap:44px}}
.icheck{{list-style:none}}
.icheck li{{font-size:19px;padding:11px 0 11px 34px;position:relative;border-bottom:1px solid var(--bg2)}}
.icheck li:last-child{{border-bottom:none}}
.icheck li:before{{content:"";position:absolute;left:0;top:20px;width:9px;height:9px;
border-radius:50%;background:var(--blue)}}
.ac-green .icheck li:before{{background:var(--green)}}
.meta{{display:flex;flex-direction:column;gap:8px}}
.mi{{background:var(--bg3);border-radius:11px;padding:15px 19px}}
.mi b{{display:block;font-size:11px;letter-spacing:1.1px;text-transform:uppercase;
color:var(--tx3);font-weight:700;margin-bottom:4px}}
.mi span{{font-size:15.5px;font-weight:600;color:var(--tx);line-height:1.4}}
.note{{font-size:15px;line-height:1.55;border-radius:11px;padding:16px 19px;margin-top:6px;
background:#eff6ff;color:#1e3a8a;font-style:italic}}
.ac-green .note{{background:#ecfdf5;color:#065f46}}

/* quote */
.qgrid{{display:grid;grid-template-columns:1fr 1fr;gap:15px}}
.qi{{background:#fff;border:1px solid var(--bd);border-radius:13px;padding:19px 22px}}
.qi b{{display:block;font-family:'Outfit',sans-serif;font-size:17px;font-weight:700;
color:var(--navy);margin-bottom:6px}}
.qi p{{font-size:14.5px;color:var(--tx2);line-height:1.55}}

/* nav */
.nav{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;
align-items:center;gap:14px;background:rgba(10,22,40,.88);border:1px solid rgba(255,255,255,.13);
backdrop-filter:blur(12px);border-radius:40px;padding:9px 20px;z-index:60}}
.nav button{{background:none;border:none;color:#94a3b8;font-size:17px;cursor:pointer;
padding:3px 8px;border-radius:7px;transition:.15s}}
.nav button:hover{{color:#fff;background:rgba(255,255,255,.08)}}
.ctr{{font-family:'Outfit',sans-serif;font-size:13px;font-weight:600;color:#e2e8f0;
min-width:52px;text-align:center;font-variant-numeric:tabular-nums}}
.prog{{position:fixed;top:0;left:0;height:2.5px;background:var(--blue);transition:width .3s;
z-index:70;box-shadow:0 0 10px var(--blue)}}

/* ===== IMPRESION / PDF: una slide por pagina, apiladas ===== */
@page{{size:1280px 720px;margin:0}}
@media print{{
  html,body{{overflow:visible;background:#fff;height:auto}}
  #stage{{position:static;inset:auto;display:block;transform:none!important}}
  .slide{{position:relative!important;opacity:1!important;visibility:visible!important;
    transform:none!important;width:1280px;height:720px;page-break-after:always;
    break-after:page;display:flex!important}}
  .slide:last-child{{page-break-after:auto;break-after:auto}}
  .nav,.prog{{display:none!important}}
}}
</style></head><body>
<div class="prog" id="prog"></div>
<div id="stage">{slides_html}</div>
<div class="nav">
  <button onclick="mv(-1)" aria-label="anterior">←</button>
  <span class="ctr" id="ctr">1 / {len(S)}</span>
  <button onclick="mv(1)" aria-label="siguiente">→</button>
</div>
<script>
const sl=[...document.querySelectorAll('.slide')];let i=0;
function show(n){{i=Math.max(0,Math.min(sl.length-1,n));
  sl.forEach((s,k)=>s.classList.toggle('on',k===i));
  document.getElementById('ctr').textContent=(i+1)+' / '+sl.length;
  document.getElementById('prog').style.width=((i+1)/sl.length*100)+'%';}}
function mv(d){{show(i+d)}}
document.addEventListener('keydown',e=>{{
  if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){{e.preventDefault();mv(1)}}
  if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){{e.preventDefault();mv(-1)}}
  if(e.key==='Home')show(0); if(e.key==='End')show(sl.length-1);}});
document.addEventListener('click',e=>{{if(!e.target.closest('.nav'))mv(1)}});
// escalar al viewport manteniendo 16:9
function fit(){{const s=Math.min(innerWidth/1280,innerHeight/720)*0.96;
  document.getElementById('stage').style.transform=`scale(${{s}})`;}}
addEventListener('resize',fit);fit();show(0);
</script></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes) · {len(S)} slides")
