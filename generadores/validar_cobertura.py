#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDACIÓN DE COBERTURA — ¿tenemos fichado todo lo que vende SUPCON?

Metodo: inventariar el material del fabricante por carpeta de producto y por 1-Pager, y
cruzarlo contra los productos que YA tienen ficha en datos/fichas_*_datos.json.
Reporta: cubierto, faltante, y material que no es producto (propuestas, casos, org).

Salida: datos/cobertura_catalogo.json + impresion por stdout.
"""
import os, json, re, glob, collections

RAIZ = os.path.expanduser("~/Documents/ConocimientoSupcon")
BASE = os.path.join(RAIZ, "supcon-catalogo")
D = os.path.join(BASE, "datos")

# ------------------------------------------------ 1) lo que YA esta fichado
FICHADO = {}
for f in glob.glob(os.path.join(D, "fichas_*_datos.json")):
    d = json.load(open(f, encoding="utf-8"))
    F = d.get("fichas", d)
    for n in F:
        FICHADO[n] = os.path.basename(f)

# ------------------------------------------------ 2) INVENTARIO del material
# Cada entrada: nombre comercial -> patron con el que se reconoce en el material.
# Se marca si esta fichado (clave presente en FICHADO o detectado por patron).
INVENTARIO = [
 # --- Instrumentación
 ("CXT (transmisor de presión)",        ["CXT"],                      "Instrumentación"),
 ("CJT (transmisor de presión)",        ["CJT"],                      "Instrumentación"),
 ("W Series (temperatura)",             ["W Series","WMT","Temperature Meter"], "Instrumentación"),
 ("SFE910 (caudal electromagnético)",   ["SFE910","EMF89"],           "Instrumentación"),
 ("SFM800 (caudal másico)",             ["SFM800"],                   "Instrumentación"),
 ("LUGB (caudal vortex)",               ["LUGB"],                     "Instrumentación"),
 ("YHLW (caudal por turbina)",          ["YHLW"],                     "Instrumentación"),
 ("SF20 (rotámetro)",                   ["SF20"],                     "Instrumentación"),
 ("SL903 (radar 80 GHz)",               ["SL903","SL900"],            "Instrumentación"),
 ("SL10/20/30/80 (nivel)",              ["SL10","SL20","SL30","SL80"],"Instrumentación"),
 ("X600 (calibrador)",                  ["X600"],                     "Instrumentación"),
 # --- Analítica
 ("C-QUAND",                            ["C-Quand","C-QUAND"],        "Analítica"),
 ("TISOMIC",                            ["TISOMIC","TISOMIC"],        "Analítica"),
 ("WIM COMPAS",                         ["WIM COMPAS"],               "Analítica"),
 ("PRISM (Raman)",                      ["PRISM"],                    "Analítica"),
 ("CEMS 5000",                          ["CEMS"],                     "Analítica"),
 ("Flare CEMS",                         ["Flare"],                    "Analítica"),
 ("HICOSYS / BICOSYS",                  ["Hicosys","Bicosys"],        "Analítica"),
 ("HIFISC (acondicionamiento)",         ["HIFISC"],                   "Analítica"),
 ("NICOSYS-3",                          ["NICOSYS"],                  "Analítica"),
 # --- Válvulas
 ("Válvulas SUPCON FLUID (13 series)",  ["control valve product"],    "Válvulas"),
 ("CVP2000 (posicionador)",             ["CVP2000"],                  "Válvulas"),
 ("Barrera IS (seguridad intrínseca)",  ["Intrinsic Safety","IS Barrier"], "Válvulas"),
 # --- DCS / control
 ("ECS-700 (DCS)",                      ["ECS-700","ECS700"],         "DCS"),
 ("OMC (control inteligente)",          ["OMC"],                      "DCS"),
 ("UCS Nyx",                            ["UCS Nyx","Nyx"],            "DCS"),
 ("ESP-iSYS (historiador)",             ["ESP","i-SYS","iSYS"],       "DCS"),
 ("SmartEIO (IO remoto)",               ["SmartEIO"],                 "DCS"),
 ("APL (Ethernet al campo)",            ["APL"],                      "DCS"),
 ("GW Series (gateway)",                ["GW Series","GW002","gateway"], "DCS"),
 ("CCS T9100 (compresores)",            ["T9100"],                    "DCS"),
 ("CCS T5100 (compresores)",            ["T5100"],                    "DCS"),
 # --- PLC
 ("G5Pro (PLC)",                        ["G5Pro"],                    "PLC"),
 ("G3Smart (PLC)",                      ["G3Smart","G3S"],            "PLC"),
 ("G5Pro Safety",                       ["G5Pro Safety"],             "PLC"),
 # --- SIS
 ("TCS-900 (SIS)",                      ["TCS-900","TCS900"],         "SIS"),
 ("TCS-500 (SIS)",                      ["TCS-500","TCS500"],         "SIS"),
 ("HIPPS",                              ["HIPPS"],                    "SIS"),
 # --- Software
 ("InPlant APC",                        ["APC"],                      "Software"),
 ("InPlant RTO",                        ["RTO"],                      "Software"),
 ("APEX",                               ["APEX"],                     "Software"),
 ("InPlant OMS",                        ["OMS"],                      "Software"),
 ("InPlant OTS",                        ["OTS"],                      "Software"),
 ("InPlant PID",                        ["PID"],                      "Software"),
 ("InPlant Blend",                      ["Blend"],                    "Software"),
 ("InPlant SCO",                        ["SCO"],                      "Software"),
 ("InPlant TAS",                        ["TAS"],                      "Software"),
 ("InPlant EAM",                        ["EAM"],                      "Software"),
 ("InPlant LIMS",                       ["LIMS"],                     "Software"),
 ("InPlant IFEM ProcessSuite",          ["IFEM ProcessSuite"],        "Software"),
 ("InPlant IFEM BatchSuite",            ["BatchSuite"],               "Software"),
 ("InPlant PLS",                        ["PLS"],                      "Software"),
 ("InPlant MP3000",                     ["MP3000"],                   "Software"),
 ("MPS5000",                            ["MPS5000"],                  "Software"),
 ("PRIDE",                              ["PRIDE"],                    "Software"),
 ("Q-Lab (SPC)",                        ["Q-Lab","Q-lab"],            "Software"),
 ("TPT (IA industrial)",                ["TPT"],                      "Software"),
 ("supOS",                              ["supOS","SupOS"],            "Software"),
 ("SoliSCADA",                          ["SOLISCADA","SoliSCADA"],    "Software"),
 ("Smart Site Solution",                ["Smart Site"],               "Software"),
 ("PLANTBOT (robot)",                   ["PLANTBOT","PLANTBOT"],      "Software"),
 ("Defender Pro",                       ["Defender Pro"],             "Software"),
 ("NG USB Guard",                       ["USB Guard"],                "Software"),
 ("Ciberseguridad OT (ICS)",            ["Cybersecurity","Firewall","Data Diode"], "Software"),
 # --- Otras áreas
 ("Switchgear KYN28-12 (MT)",           ["KYN28"],                    "Eléctrico"),
 ("Switchgear MNS (BT)",                ["MNS"],                      "Eléctrico"),
 ("Medición fiscal / Metering",         ["Metering"],                 "Eléctrico"),
 ("CCTV / videovigilancia",             ["CCTV"],                     "Eléctrico"),
 ("TELECOM",                            ["TELECOM","Telecom"],        "Eléctrico"),
 ("Sistemas de incendio",               ["Fire","FIRE"],              "Eléctrico"),
 ("Fermentation Industry solution",     ["Fermentation"],             "Eléctrico"),
 ("Mining & Metallurgical",             ["Mining"],                   "Eléctrico"),
 ("Pulp and Paper",                     ["Pulp and Paper"],           "Eléctrico"),
]

def en_material(patrones):
    """Busca los patrones en los NOMBRES DE ARCHIVO del material (no en el contenido:
    buscar en contenido daria falsos positivos por menciones de contexto)."""
    for pat in patrones:
        for f in glob.glob(os.path.join(RAIZ, "**", "*"), recursive=True):
            b = os.path.basename(f)
            if re.search(re.escape(pat), b, re.I):
                return True
    return False

print("VALIDACIÓN DE COBERTURA — material SUPCON vs catálogo fichado\n")
res = []
for nombre, patrones, area in INVENTARIO:
    # fichado si alguna ficha menciona el patron en su nombre
    fich = any(any(re.search(re.escape(p), n, re.I) for p in patrones) for n in FICHADO)
    mat  = en_material(patrones)
    # CORRECCION DE UN ERROR PROPIO: antes se declaraba "SIN MATERIAL" mirando SOLO el arbol
    # local, y asi se descartaron HIFISC y NICOSYS-3 — que tienen pagina y datasheet publico.
    # Ahora, cuando no aparece en el material local, el estado es "VERIFICAR EN WEB" y no una
    # conclusion: la ausencia de archivo NO es ausencia de producto.
    if fich:
        estado = "FICHADO"
    elif mat:
        estado = "SIN FICHA"
    else:
        estado = "VERIFICAR EN WEB"
    res.append({"producto":nombre,"area":area,"material":mat,"fichado":fich,"estado":estado})

por_area = collections.defaultdict(lambda: {"total":0,"fichado":0,"sin_ficha":0,"a_verificar_web":0})
for r in res:
    a = por_area[r["area"]]
    a["total"] += 1
    if r["estado"]=="FICHADO": a["fichado"] += 1
    elif r["estado"]=="SIN FICHA": a["sin_ficha"] += 1
    else: a["a_verificar_web"] += 1

for area, a in por_area.items():
    print(f"[{area}] {a['fichado']}/{a['total']} fichado | {a['sin_ficha']} con material sin ficha | {a['a_verificar_web']} a verificar en web")
    for r in res:
        if r["area"]==area and r["estado"]!="FICHADO":
            marca = "CON MATERIAL, SIN FICHA" if r["material"] else "VERIFICAR EN LA WEB DEL FABRICANTE"
            print(f"      - {r['producto'][:52]:54s} {marca}")
    print()

faltan = [r for r in res if r["estado"]=="SIN FICHA"]
web = [r for r in res if r["estado"]=="VERIFICAR EN WEB"]
print(f"TOTAL: {len(res)} productos/áreas | fichado {sum(1 for r in res if r['estado']=='FICHADO')} | "
      f"con material sin ficha {len(faltan)} | A VERIFICAR EN WEB {len(web)}")
if web:
    print("\nOJO: los siguientes NO se declaran ausentes. La ausencia de archivo local no es "
          "ausencia de producto: hay que buscar en la web del fabricante antes de concluir.")
    for r in web: print(f"    - {r['producto']}")

json.dump({"resumen":{k:dict(v) for k,v in por_area.items()},
  "detalle":res,"total":len(res),
  "fichado":sum(1 for r in res if r["estado"]=="FICHADO"),
  "sin_ficha":len(faltan)}, open(os.path.join(D,"cobertura_catalogo.json"),"w"),
  ensure_ascii=False, indent=1)
print(f"\nguardado: datos/cobertura_catalogo.json")
