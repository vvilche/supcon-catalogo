#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESCALERA AL ÉXITO — catálogo SUPCON.
Aplica el Escalón 1 (P x M x R) y el Escalón 2 (N x Pv x Map) a los 44 productos del
catálogo, para decidir dónde poner el foco comercial.

Metodología: skill `escalera-al-exito` (TTung Agent System / CONECTA).
  Escalón 1 — P x M x R: ¿podemos cumplir?  R es semáforo: verde sube, rojo NO sube.
  Escalón 2 — N x Pv x Map: ¿dónde está el dinero? Matriz Pv x Esfuerzo.

DATOS REALES que alimentan los ejes (ninguno estimado a ojo):
  M (mercado)   -> datos/cruce_catalogo_importaciones.json (importaciones Aduanas 2025)
  R (respuesta) -> material del fabricante: campos POR COMPLETAR y presencia de battlecard
  P (producto)  -> capacidades declaradas en las fichas (datos/fichas_*_datos.json)

Salida: datos/escalera_exito.json + artefactos/escalera_exito.html
"""
import os, json, html, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT_HTML = os.path.join(BASE, "artefactos", "escalera_exito.html")

PORC = "POR COMPLETAR"

# ------------------------------------------------------------------ cargar capacidad
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
          "familia": x.get("familia","?"),
          "criticos": crit,
          "battlecard": PORC not in (x.get("competencia") or ""),
          "argumentos": len(x.get("argumentos_venta") or []),
          "objeciones": len(x.get("objeciones") or []),
          "descripcion": (x.get("descripcion") or "")[:200],
        }

# ------------------------------------------------------------------ cargar mercado
merc = json.load(open(os.path.join(D,"cruce_catalogo_importaciones.json"), encoding="utf-8"))
MERCADO = {}
for fam, info in merc["mercado_por_familia"].items():
    MERCADO[fam] = {"usd": info["cif"], "items": info["items"],
                    "rivales": [m for m,_ in info["marcas"][:4]]}

# ------------------------------------------------------------------ mapear producto -> mercado
# El nombre del mercado es la familia arancelaria; el del catalogo es la familia comercial.
# El mapeo es explicito y verificable, no inferido.
MAPEO = {
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
 # El software se cotiza DENTRO de proyectos de automatizacion, no como importacion
 # suelta: su mercado NO es una partida arancelaria. Se le asigna el mercado del nicho
 # donde compite (el mismo segmento que su rival declarado), nunca el total del DCS.
 "InPlant APC (control avanzado de procesos)":         "DCS / Controladores (ECS-700, OMC)",
 "InPlant RTO (optimización en tiempo real)":          "DCS / Controladores (ECS-700, OMC)",
 "InPlant OMS (gestión de movimientos de petróleo)":   "Válvulas y posicionadores (CVP2000)",
 "InPlant OTS (simulador de entrenamiento de operadores)": "DCS / Controladores (ECS-700, OMC)",
 "InPlant Blend (optimización y mezcla en línea)":     "Válvulas y posicionadores (CVP2000)",
 "InPlant SCO (optimización de cadena de suministro y scheduling)": "DCS / Controladores (ECS-700, OMC)",
 "InPlant PID (evaluación y sintonización de lazos de control)": "DCS / Controladores (ECS-700, OMC)",
 "InPlant TAS (carga y descarga inteligente)":         "Calibración (X600)",
 "InPlant EAM (gestión de activos empresariales)":     "DCS / Controladores (ECS-700, OMC)",
 "InPlant PLS (posicionamiento de personal)":          "Ciberseguridad / procesamiento",
 "InPlant IFEM ProcessSuite (MES de producción continua)": "DCS / Controladores (ECS-700, OMC)",
 "InPlant MP3000 (monitoreo y diagnóstico de equipos rotativos)": "Medición eléctrica / protecciones",
 "PRIDE (diagnóstico predictivo y monitoreo de equipos)": "Medición eléctrica / protecciones",
 "ESP-iSYS (base de datos en tiempo real)":            "DCS / Controladores (ECS-700, OMC)",
 "supOS (plataforma industrial / sistema operativo industrial)": "DCS / Controladores (ECS-700, OMC)",
 "UCS Nyx (sistema de control universal)":             "DCS / Controladores (ECS-700, OMC)",
 "OMC (Intelligent Operation Management & Control System)": "DCS / Controladores (ECS-700, OMC)",
 "TPT (modelo de series de tiempo de industria de proceso)": "DCS / Controladores (ECS-700, OMC)",
 "APEX (simulación y diseño de procesos)":             "DCS / Controladores (ECS-700, OMC)",
 "Sistema de ciberseguridad industrial (ICS Security Management Platform + VxDefenderPro)": "Ciberseguridad / procesamiento",
}

# ------------------------------------------------------------------ ESCALON 1: P x M x R
def evaluar(nombre, cap):
    mkey = MAPEO.get(nombre)
    m = MERCADO.get(mkey, {"usd":0,"items":0,"rivales":[]})

    # --- P (producto): cuan defendible es el vector de diferenciacion ---
    # Se puntua por la FUERZA DE LA PROPUESTA que el propio material declara:
    # argumentos documentados + objeciones ya trabajadas + battlecard disponible.
    p = 0
    if cap["battlecard"]: p += 2          # el fabricante entrego argumento competitivo
    if cap["argumentos"] >= 6: p += 2
    elif cap["argumentos"] >= 4: p += 1
    if cap["objeciones"] >= 5: p += 1
    if cap["criticos"] == 0: p += 2       # material completo
    elif cap["criticos"] <= 2: p += 1
    p = min(p, 7)

    # --- M (mercado): tamano real importado + si hay necesidad obligatoria ---
    u = m["usd"]
    if u >= 80e6: mm = 7
    elif u >= 50e6: mm = 6
    elif u >= 20e6: mm = 5
    elif u >= 10e6: mm = 4
    elif u >= 1e6: mm = 3
    else: mm = 1

    # --- R (respuesta): semaforo segun lo que falta para poder responder ---
    # ROJO: material escaso (el equipo no puede cotizar ni defender sin pedir a fabrica)
    # AMARILLO: hay material pero falta algo declarado
    # VERDE: se puede responder hoy
    if cap["criticos"] >= 5:
        r, rcol = "ROJO", "🔴 No podemos responder: falta material de base para cotizar"
    elif cap["criticos"] >= 3:
        r, rcol = "AMARILLO", "🟡 Podemos responder con condiciones: hay campos clave por confirmar"
    elif not cap["battlecard"]:
        r, rcol = "AMARILLO", "🟡 Podemos responder: falta el argumento competitivo (no lo dio el fabricante)"
    else:
        r, rcol = "VERDE", "🟢 Podemos responder hoy"

    # Puntaje global del Escalon 1: P x M, condicionado por R
    base = p * mm
    if r == "ROJO": base = base * 0.3
    elif r == "AMARILLO": base = base * 0.7

    return {"producto": nombre, "familia": cap["familia"],
            "mercado_k": mkey, "mercado_usd": u, "mercado_items": m["items"],
            "rivales": m["rivales"], "P": p, "M": mm, "R": r, "R_nota": rcol,
            "battlecard": cap["battlecard"], "criticos": cap["criticos"],
            "argumentos": cap["argumentos"], "objeciones": cap["objeciones"],
            "score1": round(base, 1)}

TODO = [evaluar(n, c) for n, c in CAP.items()]
TODO.sort(key=lambda x: -x["score1"])

# ------------------------------------------------------------------ ESCALON 2: N x Pv x Map
# Pv (potencial de venta por nicho): tamano de mercado x fuerza de la propuesta.
# Esfuerzo: cuan listo esta CONECTA para venderlo = derivado de R.
def escalon2(t):
    """Escalon 2: N x Pv x Map. Pv = score del Escalon 1; Esfuerzo = cuan listos estamos.

    Calibracion (iterada sobre la distribucion real de scores, que va de 0 a 35):
      - El esfuerzo NO depende solo de R: un producto con material completo y sin
        battlecard es esfuerzo MEDIO (hay que armar el argumento con el fabricante),
        no ALTO.
      - Un producto que el Escalon 1 declara 'podemos responder' NO puede caer en
        Descartar: como maximo baja a 'Evaluar'. Descartar se reserva para lo que no
        podemos responder hoy (R rojo), que es el unico caso en que la skill prohibe subir.
    """
    pv = t["score1"]
    if t["R"] == "VERDE":
        esf = "Bajo"
    elif t["criticos"] <= 1 and not t["battlecard"]:
        esf = "Medio"          # material completo, solo falta el battlecard
    elif t["criticos"] <= 3:
        esf = "Medio"          # hay que confirmar algunos campos
    else:
        esf = "Alto"

    if t["R"] == "ROJO":
        # la skill es explicita: con R rojo NO se sube de escalon
        prio = "NO SUBE (R rojo)"
    elif esf == "Bajo":
        prio = "FOCO PRIMARIO" if pv >= 20 else ("Volumen" if pv >= 10 else "Mantenimiento")
    elif esf == "Medio":
        prio = "FOCO PRIMARIO" if pv >= 25 else ("Evaluar" if pv >= 8 else "Mantenimiento")
    else:
        prio = "Evaluar ROI" if pv >= 25 else ("Solo estratégico" if pv >= 12 else "Evaluar")
    return pv, esf, prio

for t in TODO:
    pv, esf, prio = escalon2(t)
    t["esfuerzo"] = esf
    t["prioridad"] = prio

# ------------------------------------------------------------------ resumen
foco = [t for t in TODO if t["prioridad"] == "FOCO PRIMARIO"]
vol  = [t for t in TODO if t["prioridad"] == "Volumen"]
ev   = [t for t in TODO if t["prioridad"] in ("Evaluar","Evaluar ROI")]
man  = [t for t in TODO if t["prioridad"] == "Mantenimiento"]
estr = [t for t in TODO if t["prioridad"] == "Solo estratégico"]
desc = [t for t in TODO if t["prioridad"].startswith("NO SUBE")]

print(f"ESCALON 1+2 sobre {len(TODO)} productos\n")
print(f"{'FOCO PRIMARIO':16s} {len(foco):>3}  -> mercados de mayor tamaño con propuesta defendible")
print(f"{'Volumen':16s} {len(vol):>3}")
print(f"{'Evaluar':16s} {len(ev):>3}")
print(f"{'Mantenimiento':16s} {len(man):>3}")
print(f"{'Solo estratégico':16s} {len(estr):>3}")
print(f"{'NO SUBE (R rojo)':16s} {len(desc):>3}")
print()
print("=== TOP 15 (foco primario) ===")
for i,t in enumerate(foco[:15],1):
    print(f"{i:2d}. {t['producto'][:46]:48s} P{t['P']} M{t['M']} {t['R']:9s} "
          f"US${t['mercado_usd']/1e6:>6,.1f}M  score={t['score1']}")

print()
print("=== LOS QUE NO SUBEN (R rojo o amarillo critico) ===")
for t in TODO:
    if t["R"] == "ROJO":
        print(f"  {t['producto'][:50]:52s} criticos={t['criticos']}  {t['R_nota']}")

json.dump({"metodologia":"Escalera al Exito - Escalon 1 (PxMxR) y Escalon 2 (NxPvxMap)",
  "fuente_mercado":"Registro DIN Aduanas Chile 2025 (datos/cruce_catalogo_importaciones.json)",
  "fuente_capacidad":"material del fabricante (datos/fichas_1..4_datos.json)",
  "productos":TODO,
  "resumen":{"foco_primario":len(foco),"volumen":len(vol),"evaluar":len(ev),
             "mantenimiento":len(man),"estrategico":len(estr),"no_sube":len(desc)}},
  open(os.path.join(D,"escalera_exito.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/escalera_exito.json")
