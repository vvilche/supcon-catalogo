#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construye el catalogo SUPCON: indice de fichas por familia + las fichas Hobre con specs.
Lee: fichas_extraidas.json (texto extraido de las fichas), inventario_familias.json
Escribe: catalogo_supcon.html  (single-file, datos inyectados desde el JSON)
NO inventa nada: solo lo que esta en los archivos.
"""
# -*- coding: utf-8 -*-
"""Resuelve las rutas desde la ubicacion del propio archivo (autocontenido).
BASE = raiz del repo; DATOS = datos/; SALIDA = artefactos/.
El material fuente del fabricante NO vive en el repo: se lee de FUENTE_MATERIAL."""
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")
SALIDA = os.path.join(BASE, "artefactos")
# ruta del material del fabricante (PDF/PPTX), fuera del repo
FUENTE_MATERIAL = os.path.expanduser("~/Documents/ConocimientoSupcon")
import os, json, re, html as H

CACHE = DATOS
fichas = json.load(open(os.path.join(CACHE, "fichas_extraidas.json"), encoding="utf-8"))

def txt(nombre):
    return fichas.get(nombre, {}).get("texto", "")

# ---------------------------------------------
# CLASIFICACION POR FAMILIA (reglas sobre el nombre)
# ---------------------------------------------
def familia(n):
    s = n.lower()
    if "hobre" in s or "tisomic" in s or "quand" in s or "prism" in s or "compas" in s: return "Analizadores"
    if "tcs-" in s or "sis product" in s:                    return "Seguridad (SIS)"
    if "g5pro" in s or "g3smart" in s or "plc" in s:         return "PLC"
    if "omc" in s:                                           return "DCS / OMC (software de operación)"
    if "ccs" in s:                                           return "CCS (control de compresores)"
    if "apc" in s or "apex" in s or s.startswith("inplant"):  return "Software de proceso (InPlant/APC)"
    if "supos" in s or "tpt" in s or "ucs" in s or "apl" in s: return "Plataforma (supOS/TPT/UCS/APL)"
    if "cybersecurity" in s or "defender" in s or "usb guard" in s or "mps5000" in s: return "Ciberseguridad OT"
    if "pride" in s:                                         return "PRIDE (monitoreo de activos)"
    if "smart site" in s:                                    return "Smart Site"
    if "esp i-sys" in s:                                     return "ESP i-SYS"
    return "Otros"

def prioridad(n):
    """Las Hobre primero (son las de mayor valor), luego el orden por familia."""
    orden = ["Analizadores","Seguridad (SIS)","PLC","DCS / OMC (software de operación)",
             "Software de proceso (InPlant/APC)","Plataforma (supOS/TPT/UCS/APL)",
             "Ciberseguridad OT","CCS (control de compresores)","PRIDE (monitoreo de activos)",
             "Smart Site","ESP i-SYS","Otros"]
    return orden.index(familia(n)) if familia(n) in orden else 99

# Solo fichas con contenido real
validas = {n: v for n, v in fichas.items() if v["chars"] >= 50}
grupos = {}
for n in sorted(validas, key=lambda x: (prioridad(x), x)):
    grupos.setdefault(familia(n), []).append(n)

# ---------------------------------------------
# SPECS CURADAS DE ANALIZADORES (del JSON verificado, no inventadas)
# ---------------------------------------------
SPECS = {
 "Hobre C-Quand brochure.pdf": {
   "rol":"Análisis elemental multi-elemento en líquidos (XRF)",
   "badges":["ED-XRF","mineria"],
   "specs":[("Rango de elementos","Si (Z=14) a U (Z=92)"),
            ("Rango de medición","<1 ppmWt a >10 %Wt"),
            ("Elementos simultáneos","hasta 15"),
            ("Fuente de rayos X","15 W / 50 kV, anodo Ag"),
            ("Detector","SDD alta resolución"),
            ("Tiempo de medición","típico 5 min"),
            ("Vida útil SDD/tubo","larga (sin dato exacto)"),
            ("Dimensiones","1000 x 400 x 360 mm"),
            ("Peso","85 kg"),
            ("Protección","IP65 / NEMA4X"),
            ("Comunicación","Modbus TCP/IP, RS485 RTU"),
            ("Zona peligrosa","ATEX II 2G Ex pxb IIC T4 / Cl1 Div2")],
   "aplicaciones":["Fe, Ni, Co, Cu, Mo, V, W, As, Zn, Sn y PGM en minería / refinería / reciclaje",
                   "Azufre en crudos, ULSD, ULSG, kerosene",
                   "Cloro en crudo y condensado de CDU (corrosión)",
                   "Metales en crudo (V, Fe, Ni)","Sal en crudo",
                   "Metales que envenenan catalizador HDS/FCC",
                   "Aguas residuales","PTA, PIA, FDCA en fase liquida",
                   "Uranio en minería y plantas nucleares"],
   "nota":"Disponibilidad declarada &gt;99,5%. Medición directa sin preparación de muestra ni reactivos. Versión PLUS con flush de celda y validación automática cero/span."},
 "Hobre TISOMIC Analyzer Brochure.pdf": {
   "rol":"Análisis H2S, H2O y CO2 en gas y líquidos",
   "badges":["PA-TDL","sin partes moviles"],
   "specs":[("Mide","H2S, H2O, CO2 (+CH4 segun SUPCON)"),
            ("Excitación","Láser de diodo sintonizable (TDL)"),
            ("Detección","Foto-acústica (PA)"),
            ("Láseres","hasta 4"),
            ("Corrientes de proceso","hasta 2"),
            ("Alta precisión","0 - 100 ppm (programable)"),
            ("Baja precisión","0 - niveles de % (programable)"),
            ("Repetibilidad alta","0,3 ppm"),
            ("Repetibilidad baja","1% escala completa"),
            ("Celda PA","~100 mm, 50 C (80 C opcional)"),
            ("Flujo celda","< 200 cm3/min"),
            ("Calibración","cada 3 a 6 meses"),
            ("MTBF","más de 5 años"),
            ("Drift","típico &lt;3% por año (con HIFISC)"),
            ("Analógicas","4 x 4-20 mA"),
            ("Comunicación","Modbus RTU RS485 + Modbus RTU TCP/IP"),
            ("Dimensiones","1200 x 600 x 500 mm"),
            ("Peso","~150 kg"),
            ("Protección","IP66 (electrónica aluminio marino, celda SS316)"),
            ("Zona peligrosa","ATEX II 2G Ex db IIB+H2 T3 / CSA Cl1 Div1")],
   "aplicaciones":["H2S en crudo multifásico y fluidos de pozo",
                   "Presión parcial de H2S en separadores y strippers",
                   "H2S / H2O en crudo de exportación y condensado",
                   "H2S / H2O / CO2 en tratamiento de gas natural",
                   "H2S / H2O / CO2 en gas de venta y ducto",
                   "H2S antes y despues de dosificación de scavenger",
                   "H2S y CO2 en absorbedores de amina",
                   "H2S en gas combustible de refinería y flare",
                   "Control de turbina de gas","Calidad de gas combustible",
                   "H2S en combustibles liquidos"],
   "nota":"Se vende siempre en paquete con HIFISC (acondicionamiento de muestra). Para H2S a nivel ppm bajo usa DOS celdas en serie con scrubber de referencia. Para H2S en líquidos no existen estándares de calibración: Hobre desarrolló extrusión de H2S."},
 "Hobre WIM COMPAS Brochure.pdf": {
   "rol":"Índice de Wobbe / poder calorífico / combustión",
   "badges":["4 modelos","+1000 instaladas"],
   "specs":[("Principio","Oxígeno residual (celda de zirconia)"),
            ("Normas","ASTM D4891-13, ISO 15971"),
            ("Mide","Wobbe, BTU, CARI, Air Demand, densidad, peso molecular"),
            ("Wobbe continuo","0-100 MJ/Nm3 (0-2500 BTU/scf)"),
            ("Exactitud continuo","< +/- 0,4% FS en gas natural"),
            ("Repetibilidad continuo","< +/- 0,05% FS"),
            ("Respuesta continuo","T90 < 5 s"),
            ("Poder calorífico inyección","0-120 MJ/Nm3 (0-3000 BTU/scf)"),
            ("Respuesta inyección","update 30 s"),
            ("CARI","rango 0-25"),
            ("Aire instrumento","15 Nl/min (continuo) / 0,2 Nl/min (inyección)"),
            ("Materiales húmedos","SS316, Inconel, Platino"),
            ("Dimensiones","1000x950x450 mm (no-Ex) / 1200x900x450 (HT)"),
            ("Peso","80 kg (no-Ex) / 120 kg (HT)"),
            ("Comunicación","Modbus TCP/IP Ethernet o fibra; Modbus RTU RS485"),
            ("Zona peligrosa","ATEX Zone 1/2 IIC T3/T4, CSA Cl1 Div2, IECEx, KCS, TRCU")],
   "aplicaciones":["Mezcla de gas natural y LNG","Control de quemadores y hornos",
                   "Control de turbinas de gas","Gas combustible de refinería",
                   "Reporte de emisiones CO2 y SO2","Análisis de biogás y syngas",
                   "Power to gas","Gas de alto horno (BFG) y coque (COG)",
                   "Flare gas y gas amargo","Sistema de estabilización de gas (acero y vidrio)"],
   "nota":"Cuatro modelos: Xpress (continuo, LNG, 1 punto), Flex (continuo, más opciones, 2 puntos), Pulse (inyección, gas amargo/flare), Pulse HT (rocío hasta 150&nbsp;C, opción H2 FEH2)."},
 "Hobre PRISM Raman Brochure.pdf": {
   "rol":"Composición de gas multicomponente (Raman)",
   "badges":["Raman","hidrogeno"],
   "specs":[("Principio","Espectroscopía Raman (con TNO, patentada)"),
            ("Mide","C1..C5+, H2, N2, CO2 (+CO, H2O segun SUPCON)"),
            ("Rango","0,1 a 100%"),
            ("H2","0-100% de fabrica"),
            ("Respuesta","T90 tipico 10 s"),
            ("Repetibilidad","mejor que +/- 0,5% FS"),
            ("Exactitud","mejor que +/- 1% FS"),
            ("Presión muestra","10-75 barG, SIN reduccion de presion"),
            ("Temperatura muestra","hasta 80 C"),
            ("Partes húmedas","SS316"),
            ("Fibra óptica","5, 10, 20, 30, 50 m"),
            ("Espectrómetro","800x500x400 mm"),
            ("Sonda","600x600x300 mm"),
            ("Comunicación","Modbus RTU RS485, Modbus TCP/IP Ethernet o fibra"),
            ("Zona peligrosa","ATEX/IECEx II 2G IIC T3; CSA Cl1 Div2 (pendiente)")],
   "aplicaciones":["Gas natural y syngas (metanol, amoníaco, hidrógeno)",
                   "Mezcla de hidrógeno (hydrogen blending)",
                   "Monitoreo de syngas","Control feed-forward de procesos",
                   "Reducción de emisiones y eficiencia energética",
                   "Producción de hidrógeno"],
   "nota":"Cero emisión: la muestra vuelve al proceso. Presión alta MEJORA la señal Raman (no requiere reducción). Ganó el Annual Product Award en ATC 2024."},
}

# ---------------------------------------------
# RENDER
# ---------------------------------------------
def esc(s): return H.escape(str(s))

def quitar_ext(n):
    """Quita la extension sin usar regex dentro de f-string."""
    return n.rsplit(".", 1)[0] if "." in n else n

def limpiar_nombre(n):
    b = quitar_ext(n)
    for frag in (" brochure", " Analyzer Brochure", " Raman Brochure", "Hobre ", " (For Sales)",
                 " One-Page Introduction", " One Page Introduction", " One-page Introduction"):
        b = b.replace(frag, "")
    return b

# chips de familia (armados FUERA del f-string grande: los f-string anidados con backslash fallan en py<3.12)
chips_html = "".join('<span class="chip" data-f="%s">%s</span>' % (esc(f), esc(f))
                     for f in sorted(grupos, key=lambda x: prioridad(x)))

payload = {"grupos": grupos, "specs": SPECS,
           "fuente": {n: validas[n]["ruta"] for n in validas}}

cards_html = []
for fam, items in sorted(grupos.items(), key=lambda x: prioridad(x[1][0])):
    cards_html.append(f'<div class="fam"><div class="fam-h"><h2>{esc(fam)}</h2>'
                      f'<span class="org">{len(items)} ficha{"s" if len(items)!=1 else ""}</span></div>')
    for n in items:
        sp = SPECS.get(n)
        if sp:
            specs = "".join(f'<div class="kv"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div></div>'
                            for k, v in sp["specs"])
            apps  = "".join(f'<span class="tag">{esc(a)}</span>' for a in sp["aplicaciones"])
            badges= "".join(f'<span class="p-badge">{esc(b)}</span>' for b in sp["badges"])
            body = f"""
      <div class="p-body">
        <h4>Especificaciones</h4><div class="grid">{specs}</div>
        <h4>Aplicaciones</h4><div class="tags">{apps}</div>
        <div class="aviso"><b>Nota de ingenieria:</b> {esc(sp["nota"])}</div>
        <div class="fuente">fuente: {esc(validas[n]["ruta"])}</div>
      </div>"""
            cards_html.append(f"""<details class="prod"><summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">{esc(n.replace('.pdf','').replace(' brochure','').replace(' Analyzer Brochure','').replace(' Raman Brochure','').replace('Hobre ',''))}</span>
        <span class="p-rol">{esc(sp["rol"])}</span>{badges}
      </summary>{body}</details>""")
        else:
            nombre_limpio = limpiar_nombre(n)[:70]
            cards_html.append(f"""<details class="prod"><summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">{esc(nombre_limpio)}</span>
        <span class="p-rol">Ficha 1-Pager &middot; {validas[n]["chars"]:,} caracteres extraídos</span>
      </summary><div class="p-body">
        <div class="aviso">Sin specs curadas todavía. El texto completo está extraído en <code>fichas_extraidas.json</code>.</div>
        <div class="fuente">fuente: {esc(validas[n]["ruta"])}</div>
      </div></details>""")
    cards_html.append('</div>')

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo SUPCON</title><style>
:root{{--bg:#f8fafc;--card:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--tx);font-family:Inter,-apple-system,sans-serif;font-size:15px;line-height:1.55;padding:30px 26px 80px}}
.wrap{{max-width:1280px;margin:0 auto}}
.hero{{background:var(--card);border:1px solid var(--bd);border-radius:20px;padding:26px 30px;margin-bottom:18px}}
.hero h1{{font-size:25px;font-weight:650;letter-spacing:-.4px;margin-bottom:6px}}
.hero p{{color:var(--mu);font-size:14.5px;max-width:840px}}
.stats{{display:flex;gap:34px;margin-top:20px;padding-top:18px;border-top:1px solid var(--bd);flex-wrap:wrap}}
.stat b{{display:block;font-size:26px;font-weight:650;font-family:"IBM Plex Mono",monospace}}
.stat span{{font-size:11.5px;color:var(--mu);text-transform:uppercase;letter-spacing:.5px}}
.filt{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:18px;align-items:center}}
.chip{{border:1px solid var(--bd);background:var(--card);border-radius:100px;padding:7px 15px;font-size:13px;cursor:pointer;color:var(--mu);user-select:none}}
.chip.on{{background:var(--ac);border-color:var(--ac);color:#fff}}
.search{{border:1px solid var(--bd);border-radius:100px;padding:8px 15px;font-size:13.5px;font-family:inherit;min-width:260px}}
.fam{{margin-bottom:28px}}
.fam-h{{display:flex;align-items:baseline;gap:11px;margin-bottom:12px}}
.fam-h h2{{font-size:17.5px;font-weight:620}}
.fam-h .org{{font-size:11.5px;background:var(--acs);color:var(--ac);border-radius:100px;padding:3px 11px;font-weight:550}}
details.prod{{background:var(--card);border:1px solid var(--bd);border-left:3px solid var(--ac);border-radius:18px;margin-bottom:10px;overflow:hidden}}
details.prod[open]{{border-color:#94a3b8;box-shadow:0 1px 3px rgba(15,23,42,.06)}}
summary.p-sum{{padding:16px 20px;cursor:pointer;display:flex;align-items:center;gap:13px;list-style:none;transition:background .12s}}
summary.p-sum:hover{{background:#f8fafc}}
summary.p-sum::-webkit-details-marker{{display:none}}
.p-name{{font-size:15.5px;font-weight:620;min-width:190px;color:var(--ac)}}
.p-rol{{color:var(--mu);font-size:13px;flex:1}}
.p-badge{{font-size:11px;border:1px solid var(--bd);border-radius:100px;padding:3px 10px;color:var(--mu);white-space:nowrap}}
.caret{{color:#fff;background:var(--ac);font-size:11px;transition:transform .15s;font-weight:700;
         width:22px;height:22px;min-width:22px;border-radius:50%;display:flex;align-items:center;
         justify-content:center;line-height:1}}
details[open] .caret{{transform:rotate(90deg)}}
.p-body{{padding:2px 20px 20px;border-top:1px solid var(--bd);background:#fcfdff}}
.p-body h4{{font-size:11.5px;text-transform:uppercase;letter-spacing:.6px;color:var(--mu);margin:17px 0 8px;font-weight:600}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1px;background:var(--bd);border:1px solid var(--bd);border-radius:12px;overflow:hidden}}
.kv{{background:var(--card);padding:9px 12px}}
.kv .k{{font-size:11.5px;color:var(--mu);margin-bottom:2px}}
.kv .v{{font-size:13px;font-family:"IBM Plex Mono",monospace}}
.tags{{display:flex;flex-wrap:wrap;gap:6px}}
.tag{{background:var(--acs);color:#1e40af;border-radius:100px;padding:4px 12px;font-size:12.5px}}
.aviso{{background:#fffbeb;border-left:3px solid var(--am);border-radius:8px;padding:10px 13px;font-size:13px;color:#78350f;margin-top:13px}}
.fuente{{margin-top:14px;font-size:11.5px;color:var(--mu);font-family:"IBM Plex Mono",monospace;word-break:break-all}}
.foot{{margin-top:30px;text-align:center;font-size:12px;color:var(--mu)}}
</style></head><body><div class="wrap">
<div class="hero"><h1>Catálogo SUPCON</h1>
<p>Todo el material de producto del árbol <code>ConocimientoSupcon</code>, agrupado por familia.
Solo fichas con contenido real: {len(validas)} de {len(fichas)} archivos. Las 4 que no se leían
(1 PDF escaneado + 3 comprimidos) fueron recuperadas por OCR y descompresión.</p>
<div class="stats">
<div class="stat"><b>{len(validas)}</b><span>Fichas</span></div>
<div class="stat"><b>{len(grupos)}</b><span>Familias</span></div>
<div class="stat"><b id="c-vis">0</b><span>Visibles</span></div>
<div class="stat"><b>{sum(v["chars"] for v in validas.values()):,}</b><span>Caracteres</span></div>
</div></div>
<div class="filt"><span class="chip on" data-f="*">Todas</span>
{chips_html}
<input class="search" id="q" placeholder="Buscar ficha por nombre..."></div>
{"".join(cards_html)}
<div class="foot">Los datos de analizadores vienen de las fichas técnicas Hobre; el resto de las fichas 1-Pager de SUPCON.</div>
</div><script>
const chips=document.querySelectorAll('.chip'), q=document.getElementById('q'),
      fams=document.querySelectorAll('.fam'), vis=document.getElementById('c-vis');
function upd(){{
  const f=document.querySelector('.chip.on').dataset.f, t=q.value.toLowerCase().trim();
  let n=0;
  fams.forEach(fam=>{{
    const name=fam.querySelector('h2').innerText;
    let mostrarFam = (f==='*'||f===name), c=0;
    fam.querySelectorAll('details.prod').forEach(d=>{{
      const nom=d.querySelector('.p-name').innerText.toLowerCase(),
            ok = (!t||nom.includes(t));
      d.style.display = ok?'':'none';
      if(ok) c++;
    }});
    fam.style.display = (mostrarFam && c>0)?'':'none';
    n += (mostrarFam? c:0);
  }});
  vis.innerText=n;
}}
chips.forEach(c=>c.onclick=()=>{{chips.forEach(x=>x.classList.remove('on'));c.classList.add('on');upd();}});
q.oninput=upd; upd();
document.querySelectorAll('details.prod').forEach((d,i)=>{{if(i===0)d.open=true;}});
</script></body></html>"""

OUT = os.path.join(SALIDA, "catalogo_supcon.html")
open(OUT, "w", encoding="utf-8").write(HTML)

# VERIFICACION
ab = len(re.findall(r'<details\b', HTML)); ce = len(re.findall(r'</details>', HTML))
dv = len(re.findall(r'<div\b', HTML));      dc = len(re.findall(r'</div>', HTML))
print("escrito:", OUT, "|", len(HTML.encode()), "bytes")
print(f"details: {ab} abiertos / {ce} cerrados ->", "OK" if ab==ce else "DESCUADRE")
print(f"div:     {dv} abiertos / {dc} cerrados ->", "OK" if dv==dc else f"DESCUADRE ({dv-dc})")
print("fichas renderizadas:", ab)
print("familias:", len(grupos))
for f, it in sorted(grupos.items(), key=lambda x: prioridad(x[1][0])):
    marca = " [SPECS]" if any(n in SPECS for n in it) else ""
    print(f"   {len(it):3d}  {f}{marca}")
# control: ninguna ficha perdida
print("\ncontrol de perdidas: fichas con texto =", len(validas), "| sin texto =", len(fichas)-len(validas))
