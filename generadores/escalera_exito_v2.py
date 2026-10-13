#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESCALERA AL ÉXITO — catálogo SUPCON, en DOS escaleras separadas.

POR QUE DOS. El estudio de importaciones (Registro DIN de Aduanas 2025) mide lo que entra
por partida arancelaria: hardware. El SOFTWARE no entra así — se vende dentro del proyecto,
y su valor no aparece en ninguna partida. Medir software con el mercado arancelario produce
un artefacto: 15 productos heredaban el mismo mercado (US$112,5M del DCS) y 5 de los 6
"focos primarios" eran el mismo mercado con distinto nombre. Se separan para no mezclar
un dato medido con una estimación.

  ESCALERA A — HARDWARE (27 productos): M sale del mercado importado real.
  ESCALERA B — SOFTWARE Y PLATAFORMA (17): el mercado NO es medible con este estudio.
      Se evalúa con lo que SÍ es dato del fabricante: P (fuerza de la propuesta) y
      R (capacidad de responder). El tamaño del nicho se marca como no medido.

Metodología: skill `escalera-al-exito` (TTung Agent System / CONECTA).
  Escalón 1 — P x M x R: ¿podemos cumplir? R es semáforo; con R rojo NO se sube.
  Escalón 2 — N x Pv x Map: ¿dónde está el dinero? Matriz Pv x Esfuerzo.

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
for arch in ["fichas_1_datos.json","fichas_2_datos.json","fichas_3_datos.json","fichas_4_datos.json"]:
    for nombre, x in cargar(arch).items():
        if not isinstance(x, dict): continue
        crit = sum(json.dumps(x.get(c), ensure_ascii=False).count(PORC) for c in
                   ("descripcion","beneficios","clientes_target","argumentos_venta",
                    "preguntas_tecnicas","objeciones"))
        CAP[nombre] = {
          "familia": x.get("familia","?"), "criticos": crit,
          "battlecard": PORC not in (x.get("competencia") or ""),
          "argumentos": len(x.get("argumentos_venta") or []),
          "objeciones": len(x.get("objeciones") or []),
          "descripcion": (x.get("descripcion") or ""),
          "fuente_arch": arch,
        }

merc = json.load(open(os.path.join(D,"cruce_catalogo_importaciones.json"), encoding="utf-8"))
MERCADO = {f: {"usd": i["cif"], "items": i["items"], "rivales": [m for m,_ in i["marcas"][:4]]}
           for f, i in merc["mercado_por_familia"].items()}

# ---------------------------------------------------------------- mapeo HARDWARE
# Solo productos cuya venta entra por partida arancelaria y por lo tanto tiene mercado medido.
HARDWARE = {
 "CXT (transmisor de presión)":                        "Presión (CXT, CJT)",
 "W Series (temperatura)":                             "Temperatura (W Series)",
 "SFE910 (caudal electromagnético)":                   "Caudal (SFE910, SFM800, LUGB, YHLW, SF20)",
 "SFM800 (caudal másico)":                             "Caudal (SFE910, SFM800, LUGB, YHLW, SF20)",
 "LUGB (caudal vortex)":                               "Caudal (SFE910, SFM800, LUGB, YHLW, SF20)",
 "YHLW (caudal por turbina)":                          "Caudal (SFE910, SFM800, LUGB, YHLW, SF20)",
 "SF20 (rotámetro metálico)":                          "Caudal (SFE910, SFM800, LUGB, YHLW, SF20)",
 "SL903 (radar de nivel 80 GHz)":                      "Nivel (SL903, SL10/20/80)",
 "SL10 / SL20 / SL80 (nivel magnético y magnetostrictivo)": "Nivel (SL903, SL10/20/80)",
 "CVP2000 (posicionador inteligente)":                 "Válvulas y posicionadores (CVP2000)",
 "X600 (calibrador de procesos)":                      "Calibración (X600)",
 "C-QUAND":                                            "Analizadores de proceso (Hobre)",
 "TISOMIC":                                            "Analizadores de proceso (Hobre)",
 "WIM COMPAS":                                         "Analizadores de proceso (Hobre)",
 "PRISM":                                              "Analizadores de proceso (Hobre)",
 "Analítica (línea completa Hobre)":                   "Analizadores de proceso (Hobre)",
 "CEMS 5000":                                          "Analizadores de proceso (Hobre)",
 "Flare CEMS":                                         "Analizadores de proceso (Hobre)",
 "TCS-900 (SIS)":                                      "SIS (TCS-900, TCS-500)",
 "TCS-500 (SIS)":                                      "SIS (TCS-900, TCS-500)",
 "G5Pro (PLC)":                                        "PLC (G5Pro, G3Smart)",
 "G3Smart (PLC)":                                      "PLC (G5Pro, G3Smart)",
 "T9100 (CCS)":                                        "DCS / Controladores (ECS-700, OMC)",
 "T5100 (CCS)":                                        "DCS / Controladores (ECS-700, OMC)",
 "UCS Nyx (sistema de control universal)":             "DCS / Controladores (ECS-700, OMC)",
 "OMC (Intelligent Operation Management & Control System)": "DCS / Controladores (ECS-700, OMC)",
 "ESP-iSYS (base de datos en tiempo real)":            "DCS / Controladores (ECS-700, OMC)",
}

# ---------------------------------------------------------------- SOFTWARE (sin mercado medible)
# Se agrupa por el NICHO donde el fabricante declara que compite (rivales y sectores del
# 1-Pager). El nicho es un dato del material; su TAMAÑO en Chile no es medible con Aduanas.
SOFTWARE = {
 "InPlant APC (control avanzado de procesos)":   ("Control avanzado (APC)",      "AspenTech, Honeywell, AVEVA"),
 "InPlant RTO (optimización en tiempo real)":    ("Optimización en tiempo real", "Aspen Plus+Online, AVEVA ROMeo"),
 "InPlant PID (evaluación y sintonización de lazos de control)": ("Sintonización de lazos", "Honeywell, SinoControl, Hollysys"),
 "InPlant OTS (simulador de entrenamiento de operadores)": ("Simulación y entrenamiento", "AspenTech, Honeywell UniSim, AVEVA"),
 "APEX (simulación y diseño de procesos)":       ("Simulación de procesos",      "Aspen, AVEVA SimCentral"),
 "InPlant OMS (gestión de movimientos de petróleo)": ("Movimiento de petróleo",  "Honeywell, Yokogawa"),
 "InPlant Blend (optimización y mezcla en línea)": ("Mezcla en línea",           "Yokogawa, Honeywell"),
 "InPlant SCO (optimización de cadena de suministro y scheduling)": ("Scheduling y cadena de suministro", "Blue Yonder, SAP"),
 "InPlant TAS (carga y descarga inteligente)":   ("Carga y descarga",            "por completar"),
 "InPlant EAM (gestión de activos empresariales)": ("Gestión de activos (EAM)",  "SAP PM, IBM Maximo, Fracttal"),
 "InPlant MP3000 (monitoreo y diagnóstico de equipos rotativos)": ("Monitoreo de rotativos", "Bently Nevada, Emerson"),
 "PRIDE (diagnóstico predictivo y monitoreo de equipos)": ("Diagnóstico predictivo", "Bently Nevada, SKF, Emerson"),
 "InPlant IFEM ProcessSuite (MES de producción continua)": ("MES de producción",  "Siemens, Rockwell, AVEVA"),
 "InPlant PLS (posicionamiento de personal)":    ("Posicionamiento de personal", "por completar"),
 "supOS (plataforma industrial / sistema operativo industrial)": ("Plataforma industrial", "AVEVA PI, Siemens, Honeywell Forge"),
 "TPT (modelo de series de tiempo de industria de proceso)": ("IA industrial sobre series de tiempo", "AVEVA, Honeywell, Siemens"),
 "Sistema de ciberseguridad industrial (ICS Security Management Platform + VxDefenderPro)": ("Ciberseguridad OT", "Claroty, Nozomi, Dragos, Tenable OT"),
}

def puntuar_P(cap):
    """P (producto): fuerza del vector de diferenciacion segun el material del fabricante.

    Se puntua sobre 7. ESCALA CORREGIDA: la version anterior daba P=0 a productos que SI
    tienen material (3 argumentos y 3 objeciones documentados) porque todos los tramos
    arrancaban mas arriba. Un P=0 hacia parecer invendible algo que se puede ofrecer, y
    ademas anulaba el score entero aunque el mercado fuera de US$19,7M.
    Piso real: si la ficha tiene descripcion, beneficios y algo de argumentos, tiene base
    para venderse. Los puntos se suman sobre ese piso.
    """
    p = 1  # piso: existe ficha con descripcion y contenido utilizable
    if cap["argumentos"] >= 6: p += 2
    elif cap["argumentos"] >= 4: p += 1
    if cap["objeciones"] >= 5: p += 1
    elif cap["objeciones"] >= 3: p += 0.5
    if cap["criticos"] == 0: p += 2
    elif cap["criticos"] <= 2: p += 1
    elif cap["criticos"] <= 4: p += 0.5
    if cap["battlecard"]: p += 2
    return min(round(p, 1), 7)

def puntuar_M(usd):
    if usd >= 80e6: return 7
    if usd >= 50e6: return 6
    if usd >= 20e6: return 5
    if usd >= 10e6: return 4
    if usd >= 1e6:  return 3
    return 1

def semaforo_R(cap):
    """R (respuesta). La skill es explicita: con R rojo NO se sube al Escalon 2."""
    if cap["criticos"] >= 5:
        return "ROJO", "🔴 No podemos responder: falta el material de base para cotizar"
    if cap["criticos"] >= 3:
        return "AMARILLO", "🟡 Respondemos con condiciones: hay campos clave por confirmar"
    if not cap["battlecard"]:
        return "AMARILLO", "🟡 Respondemos: falta el argumento competitivo (no lo dio el fabricante)"
    return "VERDE", "🟢 Podemos responder hoy"

# ---------------------------------------------------------------- ESCALERA A: hardware
A = []
for nombre, mkey in HARDWARE.items():
    cap = CAP.get(nombre)
    if not cap: continue
    m = MERCADO.get(mkey, {"usd":0,"items":0,"rivales":[]})
    P = puntuar_P(cap); M = puntuar_M(m["usd"])
    R, nota = semaforo_R(cap)
    base = P * M
    if R == "ROJO": base *= 0.3
    elif R == "AMARILLO": base *= 0.7
    A.append({"producto": nombre, "escalera":"A · Hardware", "familia": cap["familia"],
      "mercado": mkey, "mercado_usd": m["usd"], "mercado_items": m["items"],
      "rivales": m["rivales"], "P":P, "M":M, "R":R, "R_nota":nota,
      "battlecard":cap["battlecard"], "criticos":cap["criticos"],
      "argumentos":cap["argumentos"], "objeciones":cap["objeciones"],
      "score":round(base,1), "descripcion":cap["descripcion"][:220]})
A.sort(key=lambda x:-x["score"])

# ---------------------------------------------------------------- ESCALERA B: software
B = []
for nombre, (nicho, rivales) in SOFTWARE.items():
    cap = CAP.get(nombre)
    if not cap: continue
    P = puntuar_P(cap)
    R, nota = semaforo_R(cap)
    # Sin mercado medible: el score usa SOLO P (fuerza de la propuesta), y R lo condiciona.
    # NO se inventa un M. Se deja explicito que el tamano no esta medido.
    base = P
    if R == "ROJO": base = 0
    elif R == "AMARILLO": base *= 0.7
    B.append({"producto": nombre, "escalera":"B · Software y plataforma", "familia": cap["familia"],
      "nicho": nicho, "rivales_declarados": rivales, "mercado_usd": None,
      "P":P, "M":None, "R":R, "R_nota":nota, "battlecard":cap["battlecard"],
      "criticos":cap["criticos"], "argumentos":cap["argumentos"], "objeciones":cap["objeciones"],
      "score":round(base,1), "descripcion":cap["descripcion"][:220]})
B.sort(key=lambda x:-x["score"])

print(f"ESCALERA A — HARDWARE ({len(A)} productos, mercado medido en Aduanas)\n")
print(f"{'#':>2} {'PRODUCTO':44s} {'P':>2} {'M':>2} {'R':10s} {'MERCADO':>10s} {'score':>6}")
print("-"*88)
for i,t in enumerate(A,1):
    print(f"{i:2d} {t['producto'][:42]:44s} {t['P']:>2} {t['M']:>2} {t['R']:10s} "
          f"US${t['mercado_usd']/1e6:>7,.1f}M {t['score']:>6}")

print(f"\nESCALERA B — SOFTWARE ({len(B)} productos, mercado NO medible con Aduanas)\n")
print(f"{'#':>2} {'PRODUCTO':44s} {'P':>2} {'R':10s} {'score':>6}  NICHO")
print("-"*110)
for i,t in enumerate(B,1):
    print(f"{i:2d} {t['producto'][:42]:44s} {t['P']:>2} {t['R']:10s} {t['score']:>6}  {t['nicho'][:40]}")

json.dump({"metodologia":"Escalera al Exito - Escalon 1 (PxMxR) + Escalon 2 (NxPvxMap)",
  "nota_metodologica":"Dos escaleras separadas: el software no entra por partida arancelaria "
    "y por lo tanto no tiene mercado medible con el Registro DIN. Mezclarlo con hardware "
    "producia un artefacto (15 productos heredaban el mercado del DCS).",
  "fuente_mercado_hardware":"Registro DIN Aduanas Chile 2025 (datos/cruce_catalogo_importaciones.json)",
  "fuente_capacidad":"material del fabricante (datos/fichas_1..4_datos.json)",
  "escalera_a_hardware":A, "escalera_b_software":B},
  open(os.path.join(D,"escalera_exito.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/escalera_exito.json")
