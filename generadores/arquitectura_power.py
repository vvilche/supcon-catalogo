#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la slide de ARQUITECTURA del sistema de potencia para el deck de ConectaTalento.

Objetivo: mostrar de un vistazo DONDE VENDE CONECTA dentro de la cadena eléctrica.
Un estudiante que ve esto entiende en 5 segundos qué se hace en la linea POWER.

Flujo (izq -> der), 5 bloques en la cadena:
  GENERACION -> TRANSMISION -> SUBESTACION -> DISTRIBUCION -> CONSUMO
  + una banda transversal "SALA DE CONTROL / SCADA" que atraviesa todo
  + una banda inferior "PROTECCION, MEDICION Y SINCRONIZACION"

Cada caja lleva un punto verde si CONECTA vende ahi, gris si no es su negocio.
"""
import os, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "artefactos", "arquitectura_power.html")


def esc(x):
    return html.escape(str(x))


# (id, titulo, subtitulo, vendemos, productos)
CADENA = [
    ("gen", "Generación", "Centrales hidro, solar, eólica, térmica", True,
     "SCADA de planta · PMU · telemetría al Coordinador · sincronización"),
    ("tx", "Transmisión", "Líneas de alta tensión y subestaciones primarias", True,
     "Protecciones · RTU OrionLX+ · PMU · reloj Kronos · red OT"),
    ("se", "Subestación", "El nodo donde todo se conecta", True,
     "IEDs IEC 61850 · protecciones · medición · control de interruptores"),
    ("dist", "Distribución", "Redes de media tensión y clientes libres", True,
     "Automatización de feeder · medición · SCADA de distribución"),
    ("cons", "Consumo", "Minas, plantas, puertos, edificios", True,
     "Medición de calidad de energía · eficiencia · monitoreo"),
]

# (nombre, funcion, vendemos)
BANDA_SCADA = [
    ("Sala de control / SCADA", "HMI, histórico, alarmas, reportes al Coordinador", True),
    ("Comunicaciones OT", "Switches IEC 61850-3, red segmentada, ciberseguridad IEC 62443", True),
    ("Protección y medición", "Relés de protección, ajustes, TC/TP, calidad de energía", True),
    ("Sincronización", "Reloj GPS (Kronos) — sin esto, los fasores no sirven", True),
]


def caja(c, i):
    cid, tit, sub, vend, prod = c
    cls = "node yes" if vend else "node no"
    marca = '<span class="tag-si">CONECTA VENDE</span>' if vend else ''
    return f'''
      <div class="{cls}">
        <div class="nh"><span class="nn">{i+1}</span>{esc(tit)}</div>
        <div class="nsub">{esc(sub)}</div>
        <div class="nprod">{esc(prod)}</div>
        {marca}
      </div>'''


def caja_banda(b):
    nom, fun, vend = b
    tag = '<span class="bd-tag">CONECTA VENDE</span>' if vend else ""
    return f'''
      <div class="bd">
        <div class="bdh">{esc(nom)}</div>
        <div class="bdf">{esc(fun)}</div>
        {tag}
      </div>'''



flechas = '<div class="arrow">→</div>'
cadenas = flechas.join(caja(c, i) for i, c in enumerate(CADENA))
bandas = "".join(caja_banda(b) for b in BANDA_SCADA)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>Arquitectura del sistema de potencia — dónde vende CONECTA</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#0A1628;--blue:#2563EB;--green:#0A8439;--gr:#10B981;
--tx:#0F172A;--tx2:#475569;--tx3:#94A3B8;--bd:#E2E8F0}}
body{{background:#F8FAFC;font-family:'Inter',sans-serif;color:var(--tx);
padding:44px 40px 60px}}
.wrap{{max-width:1280px;margin:0 auto}}
h1{{font-family:'Outfit',sans-serif;font-size:34px;font-weight:700;letter-spacing:-1px;
margin-bottom:6px}}
.sub{{color:var(--tx2);font-size:15.5px;margin-bottom:26px;max-width:900px}}

/* ==== CADENA PRINCIPAL ==== */
.cadena{{display:flex;align-items:stretch;gap:0;margin-bottom:16px}}
.node{{flex:1;background:#fff;border:1px solid var(--bd);border-top:4px solid var(--blue);
border-radius:12px;padding:15px 15px 13px;position:relative;display:flex;flex-direction:column}}
.node.no{{border-top-color:#CBD5E1;opacity:.62}}
.nh{{font-family:'Outfit',sans-serif;font-size:16.5px;font-weight:700;margin-bottom:5px;
display:flex;align-items:center;gap:8px}}
.nn{{background:var(--blue);color:#fff;font-size:11px;width:19px;height:19px;border-radius:50%;
display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex:0 0 auto}}
.node.no .nn{{background:#94A3B8}}
.nsub{{font-size:12px;color:var(--tx3);margin-bottom:9px;line-height:1.4;min-height:34px}}
.nprod{{font-size:12.5px;color:#065f46;background:#ECFDF5;border-radius:7px;padding:8px 10px;
line-height:1.45;flex:1}}
.node.no .nprod{{background:#F1F5F9;color:#64748B}}
.tag-si{{display:inline-block;margin-top:9px;font-family:'Outfit',sans-serif;font-size:9.5px;
font-weight:700;letter-spacing:.9px;color:#065f46;background:#D1FAE5;border-radius:4px;
padding:3px 7px;align-self:flex-start}}
.arrow{{display:flex;align-items:center;padding:0 7px;color:var(--blue);font-size:17px;font-weight:700}}

/* ==== BANDAS ==== */
.bandas{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0;
background:var(--navy);border-radius:14px;padding:16px 18px}}
.bandas .ttl{{grid-column:1/-1;font-family:'Outfit',sans-serif;font-size:11px;font-weight:700;
letter-spacing:1.6px;text-transform:uppercase;color:#60A5FA;margin-bottom:2px}}
.bd{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
border-left:3px solid var(--gr);border-radius:9px;padding:10px 12px}}
.bdh{{font-family:'Outfit',sans-serif;font-size:13.5px;font-weight:700;color:#F1F5F9;
margin-bottom:3px}}
.bdf{{font-size:11.5px;color:#94A3B8;line-height:1.4}}
.bd-tag{{display:inline-block;margin-top:7px;font-family:'Outfit',sans-serif;font-size:9px;
font-weight:700;letter-spacing:.8px;color:#6EE7B7;border:1px solid rgba(110,231,183,.4);
border-radius:4px;padding:2px 6px}}

/* ==== LEYENDA ==== */
.ley{{display:flex;gap:26px;flex-wrap:wrap;font-size:13px;color:var(--tx2);
border-top:1px solid var(--bd);padding-top:15px;margin-top:6px}}
.ley span{{display:flex;align-items:center;gap:8px}}
.lk{{width:13px;height:13px;border-radius:4px;display:inline-block}}
.lk.si{{background:var(--blue)}}
.lk.no{{background:#CBD5E1}}
.lk.g{{background:var(--gr)}}
</style></head><body><div class="wrap">

<h1>Dónde vendemos dentro del sistema de potencia</h1>
<p class="sub">La cadena completa, de la central al cliente. En cada eslabón, lo que CONECTA
integra, instala o pone en marcha. Las bandas oscuras son transversales: se repiten en todos
los eslabones, no son una etapa.</p>

<div class="cadena">
  {cadenas}
</div>

<div class="bandas">
  <div class="ttl">Transversal a todos los eslabones</div>
  {bandas}
</div>

<div class="ley">
  <span><i class="lk si"></i> CONECTA vende e integra</span>
  <span><i class="lk g"></i> Transversal (aplica en todos lados)</span>
</div>

</div></body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
