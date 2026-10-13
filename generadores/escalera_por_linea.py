#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESCALERA AL ÉXITO — catálogo SUPCON, POR LÍNEA DE PRODUCTO.

Lineas (definidas por Victor; la analitica es linea propia, no va dentro de instrumentacion):
  Instrumentación     presión, temperatura, caudal, nivel, calibración
  Analítica           los analizadores (Hobré + CEMS SUPCON)
  Válvulas            posición y accesorios de válvula
  DCS                 sistemas de control, incluidos CCS de compresores y UCS Nyx
  PLC                 controladores lógicos
  SIS                 seguridad instrumentada
  Software y plataforma   APC, MES, IA industrial, ciberseguridad

CRITERIO DE MERCADO POR LÍNEA: el hardware se mide con el Registro DIN de Aduanas (entra por
partida arancelaria). El software y la plataforma NO: se venden dentro del proyecto y no
aparecen como importación. En esas líneas el mercado se declara "no medido", nunca se inventa.
Esta distinción existe porque medir software con el mercado del DCS produjo un artefacto
(15 productos heredando los mismos US$112,5M y 5 de 6 focos primarios con el mismo mercado).

Metodología: skill `escalera-al-exito` — Escalón 1 (P x M x R) y matriz Pv x Esfuerzo.
Regla de hierro: con R en rojo NO se sube.

Salida: datos/escalera_exito.json + artefactos/escalera_exito.html
"""
import os, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT_HTML = os.path.join(BASE, "artefactos", "escalera_exito.html")
PORC = "POR COMPLETAR"

def cargar(n):
    p = os.path.join(D, n)
    if not os.path.exists(p): return {}
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, dict) and "fichas" in d: return d["fichas"]
    return d if isinstance(d, dict) else {}

CAP = {}
for arch in ["fichas_1_datos.json","fichas_2_datos.json","fichas_3_datos.json","fichas_4_datos.json","fichas_5_datos.json","fichas_6_datos.json","fichas_7_datos.json","fichas_8_datos.json"]:
    for nombre, x in cargar(arch).items():
        if not isinstance(x, dict): continue
        crit = sum(json.dumps(x.get(c), ensure_ascii=False).count(PORC) for c in
                   ("descripcion","beneficios","clientes_target","argumentos_venta",
                    "preguntas_tecnicas","objeciones"))
        CAP[nombre] = {
          "familia": x.get("familia","?"),
          "criticos": crit,
          "battlecard": PORC not in (x.get("competencia") or ""),
          "argumentos": len(x.get("argumentos_venta") or []),
          "objeciones": len(x.get("objeciones") or []),
          "descripcion": (x.get("descripcion") or ""),
        }

merc = json.load(open(os.path.join(D,"cruce_catalogo_importaciones.json"), encoding="utf-8"))
MERCADO = {f: {"usd": i["cif"], "items": i["items"], "rivales": [m for m,_ in i["marcas"][:4]]}
           for f, i in merc["mercado_por_familia"].items()}

# ============================================================================
# LÍNEAS: cada producto con su mercado (partida arancelaria) o None si no es medible
# ============================================================================
P_CAU = "Caudal (SFE910, SFM800, LUGB, YHLW, SF20)"
P_NIV = "Nivel (SL903, SL10/20/80)"
P_ANA = "Analizadores de proceso (Hobre)"

LINEAS = collections.OrderedDict([
 ("Instrumentación", {
   "desc": "Medición de campo: presión, temperatura, caudal, nivel y calibración. Entra por partida arancelaria, así que el mercado es el importado real.",
   "medible": True,
   "productos": {
     "CXT (transmisor de presión)":                        "Presión (CXT, CJT)",
     "W Series (temperatura)":                             "Temperatura (W Series)",
     "SFE910 (caudal electromagnético)":                   P_CAU,
     "SFM800 (caudal másico)":                             P_CAU,
     "LUGB (caudal vortex)":                               P_CAU,
     "YHLW (caudal por turbina)":                          P_CAU,
     "SF20 (rotámetro metálico)":                          P_CAU,
     "SL903 (radar de nivel 80 GHz)":                      P_NIV,
     "SL10 / SL20 / SL80 (nivel magnético y magnetostrictivo)": P_NIV,
     "X600 (calibrador de procesos)":                      "Calibración (X600)",
     "CJT (transmisor de presión)":                        "Presión (CXT, CJT)",
   }}),
 ("Analítica", {
   "desc": "Analizadores de proceso: XRF elemental, fotoacústica láser, Raman, Wobbe y emisiones. Entra por el capítulo 90.27, con mercado medido.",
   "medible": True,
   "productos": {
     "C-QUAND":                                          P_ANA,
     "TISOMIC":                                          P_ANA,
     "WIM COMPAS":                                       P_ANA,
     "PRISM":                                            P_ANA,
     "Analítica (línea completa Hobre)":                 P_ANA,
     "CEMS 5000":                                        P_ANA,
     "Flare CEMS":                                       P_ANA,
     "HIFISC (acondicionamiento de muestra de gas)":      P_ANA,
     "NICOSYS-3 (detección de CO en secadores)":          P_ANA,
     "HICOSYS AQUA (medición de H2O en secado)":          P_ANA,
   }}),
 ("Válvulas", {
   "desc": "Línea completa de válvulas de control de SUPCON Fluid: vástago deslizante, bola, mariposa, excéntrica y especiales, más el posicionador CVP2000. Entra por partida arancelaria, así que el mercado es el importado real.",
   "medible": True,
   "productos": {
     "Válvulas de control — línea completa SUPCON FLUID":  "Válvulas y posicionadores (CVP2000)",
     "Válvulas de vástago deslizante (series LN y LM)":    "Válvulas y posicionadores (CVP2000)",
     "Válvulas de bola (series SN O-type y VN V-type)":    "Válvulas y posicionadores (CVP2000)",
     "Válvulas mariposa y excéntricas (series BN y CN)":   "Válvulas y posicionadores (CVP2000)",
     "Válvulas especiales (alimentación, cuchilla y compuerta)": "Válvulas y posicionadores (CVP2000)",
     "CVP2000 (posicionador inteligente)":                 "Válvulas y posicionadores (CVP2000)",
   }}),
 ("DCS", {
   "desc": "Sistemas de control distribuido, incluido el control de compresores (CCS). El mercado de la partida incluye tableros y paneles de control.",
   "medible": True,
   "productos": {
     "T9100 (CCS)":                                        "DCS / Controladores (ECS-700, OMC)",
     "T5100 (CCS)":                                        "DCS / Controladores (ECS-700, OMC)",
     "UCS Nyx (sistema de control universal)":             "DCS / Controladores (ECS-700, OMC)",
     "OMC (Intelligent Operation Management & Control System)": "DCS / Controladores (ECS-700, OMC)",
     "ESP-iSYS (base de datos en tiempo real)":            "DCS / Controladores (ECS-700, OMC)",
     "ECS-700 (DCS)":                                      "DCS / Controladores (ECS-700, OMC)",
     "SmartEIO y APL (Ethernet al campo)":                 "DCS / Controladores (ECS-700, OMC)",
     "GW Series (gateway de datos)":                       "DCS / Controladores (ECS-700, OMC)",
     "SAMS (gestión de activos de instrumentos)":          "DCS / Controladores (ECS-700, OMC)",
     "FF Foundation Fieldbus (sobre ECS-700)":             "DCS / Controladores (ECS-700, OMC)",
     "JX-300XP (plataforma PCS)":                          "DCS / Controladores (ECS-700, OMC)",
   }}),
 ("PLC", {
   "desc": "Controladores lógicos programables, incluida la variante de seguridad.",
   "medible": True,
   "productos": {
     "G5Pro (PLC)":                                        "PLC (G5Pro, G3Smart)",
     "G3Smart (PLC)":                                      "PLC (G5Pro, G3Smart)",
     "G5Pro Safety (PLC de seguridad SIL3)":               "PLC (G5Pro, G3Smart)",
   }}),
 ("SIS", {
   "desc": "Sistemas instrumentados de seguridad (SIL3).",
   "medible": True,
   "productos": {
     "TCS-900 (SIS)":                                      "SIS (TCS-900, TCS-500)",
     "TCS-500 (SIS)":                                      "SIS (TCS-900, TCS-500)",
     "HIPPS (protección de alta presión)":                 "SIS (TCS-900, TCS-500)",
   }}),
 ("Software y plataforma", {
   "desc": "Software de proceso, plataforma industrial, IA aplicada y ciberseguridad OT. NO entra por partida arancelaria: se vende dentro del proyecto, así que su mercado no es medible con el registro de importaciones.",
   "medible": False,
   "productos": {
     "InPlant APC (control avanzado de procesos)":   ("Control avanzado (APC)",            "AspenTech, Honeywell, AVEVA"),
     "InPlant RTO (optimización en tiempo real)":    ("Optimización en tiempo real",       "Aspen Plus+Online, AVEVA ROMeo"),
     "InPlant PID (evaluación y sintonización de lazos de control)": ("Sintonización de lazos", "Honeywell, SinoControl, Hollysys"),
     "InPlant OTS (simulador de entrenamiento de operadores)": ("Simulación y entrenamiento", "AspenTech, Honeywell UniSim, AVEVA"),
     "APEX (simulación y diseño de procesos)":       ("Simulación de procesos",            "Aspen, AVEVA SimCentral"),
     "InPlant OMS (gestión de movimientos de petróleo)": ("Movimiento de petróleo",        "Honeywell, Yokogawa"),
     "InPlant Blend (optimización y mezcla en línea)": ("Mezcla en línea",                 "Yokogawa, Honeywell"),
     "InPlant SCO (optimización de cadena de suministro y scheduling)": ("Scheduling y cadena de suministro", "Blue Yonder, SAP"),
     "InPlant TAS (carga y descarga inteligente)":   ("Carga y descarga",                  "por completar"),
     "InPlant EAM (gestión de activos empresariales)": ("Gestión de activos (EAM)",        "SAP PM, IBM Maximo, Fracttal"),
     "InPlant MP3000 (monitoreo y diagnóstico de equipos rotativos)": ("Monitoreo de rotativos", "Bently Nevada, Emerson"),
     "PRIDE (diagnóstico predictivo y monitoreo de equipos)": ("Diagnóstico predictivo",  "Bently Nevada, SKF, Emerson"),
     "InPlant IFEM ProcessSuite (MES de producción continua)": ("MES de producción",       "Siemens, Rockwell, AVEVA"),
     "InPlant PLS (posicionamiento de personal)":    ("Posicionamiento de personal",       "por completar"),
     "supOS (plataforma industrial / sistema operativo industrial)": ("Plataforma industrial", "AVEVA PI, Siemens, Honeywell Forge"),
     "TPT (modelo de series de tiempo de industria de proceso)": ("IA industrial sobre series de tiempo", "AVEVA, Honeywell, Siemens"),
     "Sistema de ciberseguridad industrial (ICS Security Management Platform + VxDefenderPro)": ("Ciberseguridad OT", "Claroty, Nozomi, Dragos, Tenable OT"),
     "MPS5000 (protección de maquinaria)":           ("Protección de maquinaria",  "Bently Nevada, Emerson, SKF"),
     "Q-Lab (control estadístico de procesos)":      ("Control estadístico SPC",   "InfinityQS, Minitab, SAP QM"),
     "SolisSCADA (SCADA de proceso)":                ("SCADA de proceso",          "AVEVA InTouch, Siemens WinCC, Ignition"),
   }}),
])

# ============================================================================
# P (producto), M (mercado), R (respuesta)
# ============================================================================
def puntuar_P(cap):
    """P sobre 7. Piso de 1: si la ficha tiene contenido utilizable, tiene base para venderse.
    Los puntos se suman sobre ese piso (una version anterior daba P=0 a productos que SI
    tienen material, y eso anulaba el score aunque el mercado fuera grande)."""
    p = 1
    if cap["argumentos"] >= 6: p += 2
    elif cap["argumentos"] >= 4: p += 1
    if cap["objeciones"] >= 5: p += 1
    elif cap["objeciones"] >= 3: p += 0.5
    if cap["criticos"] == 0: p += 2
    elif cap["criticos"] <= 2: p += 1
    elif cap["criticos"] <= 4: p += 0.5
    if cap["battlecard"]: p += 2
    return min(round(p,1), 7)

def puntuar_M(usd):
    if usd >= 80e6: return 7
    if usd >= 50e6: return 6
    if usd >= 20e6: return 5
    if usd >= 10e6: return 4
    if usd >= 1e6:  return 3
    return 1

def semaforo_R(cap):
    if cap["criticos"] >= 5:
        return "ROJO", "🔴 No podemos responder: falta el material de base para cotizar"
    if cap["criticos"] >= 3:
        return "AMARILLO", "🟡 Respondemos con condiciones: hay campos clave por confirmar"
    if not cap["battlecard"]:
        return "AMARILLO", "🟡 Respondemos: falta el argumento competitivo (no lo dio el fabricante)"
    return "VERDE", "🟢 Podemos responder hoy"

SALIDA = collections.OrderedDict()
for linea, cfg in LINEAS.items():
    filas = []
    for nombre, dato in cfg["productos"].items():
        cap = CAP.get(nombre)
        if not cap: continue
        P = puntuar_P(cap)
        R, nota = semaforo_R(cap)
        if cfg["medible"]:
            m = MERCADO.get(dato, {"usd":0,"items":0,"rivales":[]})
            M = puntuar_M(m["usd"])
            base = P * M
            fila = {"producto": nombre, "familia": cap["familia"], "mercado": dato,
                    "mercado_usd": m["usd"], "mercado_items": m["items"],
                    "rivales_chile": m["rivales"], "nicho": None, "rivales_declarados": None}
        else:
            nicho, rivales = dato
            M = None
            base = P   # sin mercado medible: el score usa solo la fuerza de la propuesta
            fila = {"producto": nombre, "familia": cap["familia"], "mercado": None,
                    "mercado_usd": None, "mercado_items": None, "rivales_chile": None,
                    "nicho": nicho, "rivales_declarados": rivales}
        if R == "ROJO": base = 0 if not cfg["medible"] else base * 0.3
        elif R == "AMARILLO": base *= 0.7
        fila.update({"P":P, "M":M, "R":R, "R_nota":nota, "battlecard":cap["battlecard"],
                     "criticos":cap["criticos"], "argumentos":cap["argumentos"],
                     "objeciones":cap["objeciones"], "score":round(base,1),
                     "descripcion":cap["descripcion"][:220]})
        filas.append(fila)
    filas.sort(key=lambda x:-x["score"])
    SALIDA[linea] = {"desc": cfg["desc"], "medible": cfg["medible"], "productos": filas}

print("ESCALERA AL ÉXITO POR LÍNEA\n")
for linea, cfg in SALIDA.items():
    ps = cfg["productos"]
    verdes = sum(1 for p in ps if p["R"]=="VERDE")
    rojos = sum(1 for p in ps if p["R"]=="ROJO")
    print(f"[{len(ps):>2}] {linea:24s} mercado={'medido' if cfg['medible'] else 'NO medible':12s} "
          f"R: {verdes} verde / {rojos} rojo")
    for i,p in enumerate(ps[:4],1):
        mer = f"US${p['mercado_usd']/1e6:>6,.1f}M" if p["mercado_usd"] else "  no medido"
        print(f"      {i}. {p['producto'][:44]:46s} P{p['P']:>4} {p['R']:9s} {mer}  score={p['score']}")
    if len(ps)>4: print(f"      … y {len(ps)-4} más")

total = sum(len(c["productos"]) for c in SALIDA.values())
print(f"\ntotal productos: {total}")

json.dump({"metodologia":"Escalera al Exito — Escalon 1 (PxMxR) + matriz Pv x Esfuerzo, por linea de producto",
  "nota_mercado":"Hardware: mercado del Registro DIN de Aduanas Chile 2025 (partida arancelaria). "
    "Software y plataforma: mercado NO medible, se declara sin tamano y no se inventa.",
  "fuente_capacidad":"material del fabricante (datos/fichas_1..4_datos.json)",
  "lineas":SALIDA}, open(os.path.join(D,"escalera_exito.json"),"w"), ensure_ascii=False, indent=1)
print(f"guardado: datos/escalera_exito.json")
