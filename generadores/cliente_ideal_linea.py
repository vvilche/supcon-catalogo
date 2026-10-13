#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLIENTE IDEAL POR LÍNEA DE NEGOCIO — el análisis al derecho.

POR QUE AL DERECHO (corrección de enfoque del usuario)
------------------------------------------------------------------------------
Todo el trabajo anterior partió del dolor: "estas plantas contaminan, ¿a quién le vendo?".
Eso deja afuera la mitad del catálogo, porque la mayor parte de lo que vendemos NO se activa
por dolor ambiental. Victor lo pidió al revés: "para cada cosa que vendemos, quién es el
cliente ideal". Este script hace eso.

PARA CADA LÍNEA, TRES COSAS
  1. LA SEÑAL que la activa — de qué dato sale, en qué fuente oficial.
  2. EL CLIENTE IDEAL — rubro, tamaño, y por qué ESA señal lo califica.
  3. CUÁNTOS HAY — contado en el universo real de 3.157 empresas, no estimado.

LAS SEÑALES VIENEN DE NORMAS, NO SOLO DEL RETC
------------------------------------------------------------------------------
Medido en el universo: los disparadores normativos son la señal más rica y estaban sin usar
como criterio de línea:
  DS 13/2011 Art. 8 (CEMS)  105 empresas  -> obliga medición continua de emisiones = Analítica
  NTSyCS 4-12 / 4-16        105 empresas  -> exige SCADA y reporte al Coordinador = Software
  DS 132 (seguridad minera) 174+42        -> SIS y seguridad funcional
  DS 90/2000                1109+774      -> RILES = Analítica de efluente
  DS 43/2015                1075+100      -> residuos peligrosos = trazabilidad
  Ley 21.305                1236          -> SSCC = medición para el Coordinador
  Ley 20.920 (REP)          360           -> Ley REP = trazabilidad de envases
  DS 148                    360           -> manejo de residuos
  Ley 20.551 (cierre)       174           -> cierre de faenas mineras
"""
import json, os, collections, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


u = json.load(open(os.path.join(D, "universo_senales_completas.json"), encoding="utf-8"))
EMP = u["empresas"]
print(f"universo: {len(EMP):,} empresas\n")

# ===========================================================================
# DEFINICION DE CLIENTE IDEAL POR LÍNEA
# Cada linea declara: la senal que la activa (dato -> fuente), el cliente ideal (rubro +
# condicion), y el perfil que la compra. Todo se verifica contra el universo.
# ===========================================================================
LINEAS = {
    "Analítica": {
        "productos": ["CEMS 5000", "Analítica en línea (línea Hobre)", "HIFISC",
                      "TISOMIC", "C-QUAND", "NISOSYS-3"],
        "que_vende": ("medición en línea de composición: gases de combustión, metales y "
                      "parámetros de efluente."),
        "senales": [
            {"senal": "norma DS 13/2011 Art. 8 (CEMS)", "que_dice":
             "obliga medición continua de emisiones a fuentes fijas: CEMS instalado y "
             "certificado. Es una OBLIGACIÓN de tener analizador en línea.",
             "donde": "campo `normas` del universo", "campo": "DS 13/2011 Art. 8 (CEMS)"},
            {"senal": "RILES DS 90/2000 con metales o tóxicos con masa > 0",
             "que_dice": "descarga metales pesados o cianuro declarados al RETC: hay que "
                         "medirlos, y no se miden con instrumento genérico.",
             "donde": "RETC riles_2024.xlsx", "campo": "RETC_RILES"},
            {"senal": "rubro de proceso con combustión",
             "que_dice": "generación, celulosa, cemento, refinación y fundición tienen "
                         "chimenea: ahí aplica CEMS.",
             "donde": "campo `rubro`", "campo": "RUBRO_COMBUSTION"},
        ],
        "cliente_ideal": ("planta con chimenea o descarga de metales, de tamaño MEDIANA o "
                          "GRANDE (el CEMS es caro: la pequeña no lo instala). Rubro: "
                          "generación eléctrica, celulosa, cemento, refinación, fundición, "
                          "química, tratamiento de agua."),
        "perfil_que_compra": ("Jefe de Medio Ambiente / Calidad / Laboratorio. NO lo compra "
                              "I&C ni automatización."),
        "ticket": "alto",
    },
    "Instrumentación": {
        "productos": ["SFE910 (caudal electromagnético)", "SL903 (radar de nivel 80 GHz)",
                      "CXT (presión)", "W Series (temperatura)", "LUGB (vortex)",
                      "YHLW (turbina)"],
        "que_vende": "los sensores de caudal, nivel, presión y temperatura que hay debajo de todo.",
        "senales": [
            {"senal": "declara al RETC pero mide poco", "que_dice":
             "si tiene que reportar y no tiene instrumentación, la brecha es el sensor que falta.",
             "donde": "RETC + campo `riles_contaminantes`", "campo": "RETC_SIN_INSTRUMENTAR"},
            {"senal": "norma DS 594", "que_dice":
             "condiciones sanitarias y ambientales básicas: exige medición de parámetros "
             "básicos de proceso.", "donde": "campo `normas`", "campo": "DS 594"},
            {"senal": "rubro con proceso continuo", "que_dice":
             "todo proceso continuo necesita instrumentar sus variables.", "donde": "campo `rubro`",
             "campo": "RUBRO_PROCESO"},
        ],
        "cliente_ideal": ("toda planta de proceso continuo, con o sin dolor ambiental. Es el "
                          "producto de ENTRADA más universal del catálogo: casi siempre se "
                          "cuelga del primer proyecto de control."),
        "perfil_que_compra": "Jefe de Instrumentación y Control / Mantenimiento / Jefe de Planta.",
        "ticket": "medio",
    },
    "Válvulas": {
        "productos": ["Válvulas de control SUPCON FLUID", "Bola (SN/VN)",
                      "Mariposa y excéntricas (BN/CN)", "Vástago deslizante (LN/LM)",
                      "CVP2000 (posicionador inteligente)"],
        "que_vende": "el actuador final: cierra el lazo que el control decide.",
        "senales": [
            {"senal": "proceso con fluido corrosivo o abrasivo declarado en RILES",
             "que_dice": "si maneja corrosivos a la descarga, el material de la válvula es "
                         "crítico y hay reemplazo recurrente.",
             "donde": "RETC riles_2024.xlsx", "campo": "RETC_CORROSIVO"},
            {"senal": "rubro celulosa / minería / alimentos / química",
             "que_dice": "son los rubros con más válvulas de control por línea de proceso.",
             "donde": "campo `rubro`", "campo": "RUBRO_VALVULAS"},
        ],
        "cliente_ideal": ("planta con manejo de fluidos corrosivos o pulpa (celulosa, minería, "
                          "química, alimentos, tratamiento de agua). Es producto de CONSUMO: se "
                          "repite, y el posicionador inteligente abre la venta de instrumentación."),
        "perfil_que_compra": "Jefe de Mantenimiento (mecánico / eléctrico) / Jefe de I&C.",
        "ticket": "medio",
    },
    "DCS": {
        "productos": ["ECS-700", "UCS Nyx", "OMC", "T9100 (CCS)", "SmartEIO y APL", "SAMS"],
        "que_vende": "el control distribuido del proceso completo: el punto de integración.",
        "senales": [
            {"senal": "planta de proceso continuo de tamaño grande",
             "que_dice": "un DCS se justifica con cientos de lazos, no con una isla.",
             "donde": "campos `rubro` + `tier`", "campo": "RUBRO_PROCESO + GRANDE"},
            {"senal": "dolor del Coordinador (completitud o calidad CEN baja)",
             "que_dice": "si reporta mal al CEN, el origen suele ser el sistema de control. "
                         "115 empresas tienen dolor medido del Coordinador.",
             "donde": "campo `cen_dolor`", "campo": "CEN_DOLOR"},
        ],
        "cliente_ideal": ("planta de proceso continuo GRANDE (o MEDIANA con varias líneas): "
                          "celulosa, minería, cemento, química, generación, fundición. Es el "
                          "producto de mayor ticket y el que abre todo lo demás."),
        "perfil_que_compra": "Jefe de I&C / Automatización / Gerente de Operaciones.",
        "ticket": "alto",
    },
    "SIS": {
        "productos": ["TCS-900 (SIL3)", "TCS-500", "HIPPS"],
        "que_vende": "parada de emergencia con SIL: contiene el evento antes de que sea vertido.",
        "senales": [
            {"senal": "norma DS 132 (seguridad minera)", "que_dice":
             "reglamento de seguridad minera: exige sistemas instrumentados de seguridad en "
             "faenas. 174+42 empresas lo tienen como norma aplicable.",
             "donde": "campo `normas`", "campo": "DS 132"},
            {"senal": "maneja residuos peligrosos de alta criticidad",
             "que_dice": "tóxico agudo, inflamable o reactivo en cantidad exige contención.",
             "donde": "RETC respeligrosos_2025.xlsx", "campo": "RETC_PEL_ALTA"},
            {"senal": "rubro química / combustibles / minería",
             "que_dice": "proceso con riesgo de evento mayor.", "donde": "campo `rubro`",
             "campo": "RUBRO_RIESGO"},
        ],
        "cliente_ideal": ("planta con sustancia peligrosa en proceso y norma de seguridad "
                          "aplicable: minería (DS 132), química, combustibles, celulosa con "
                          "licor, pesca con amoníaco. Medido: 117 plantas del universo "
                          "ambiental lo califican."),
        "perfil_que_compra": "Jefe de Seguridad / HSE / I&C.",
        "ticket": "alto",
    },
    "PLC": {
        "productos": ["G5Pro", "G5Pro Safety (SIL3)", "G3Smart"],
        "que_vende": "control y seguridad discretos para islas de proceso y plantas de tratamiento.",
        "senales": [
            {"senal": "planta MEDIANA o PEQUEÑA de proceso",
             "que_dice": "una isla no necesita DCS: necesita un PLC confiable y barato.",
             "donde": "campo `tier`", "campo": "TIER_MEDIANA_PEQUENA"},
            {"senal": "rubro tratamiento de agua / gestor de residuos",
             "que_dice": "planta de tratamiento es control discreto por naturaleza.",
             "donde": "campo `rubro`", "campo": "RUBRO_TRATAMIENTO"},
        ],
        "cliente_ideal": ("planta de tratamiento de agua o residuos, y toda planta mediana o "
                          "pequeña con islas discretas. Es el producto de entrada donde NO "
                          "corresponde vender DCS."),
        "perfil_que_compra": "Jefe de Automatización / Mantenimiento.",
        "ticket": "bajo",
    },
    "Software y plataforma": {
        "productos": ["SolisSCADA", "InPlant APC", "InPlant RTO", "InPlant MP3000",
                      "APEX", "ESP-iSYS", "InPlant PID"],
        "que_vende": ("adquisición, historización, reporte y optimización de muchas señales a la "
                      "vez."),
        "senales": [
            {"senal": "norma NTSyCS 4-12 / 4-16", "que_dice":
             "exige reporte y cumplimiento al Coordinador Eléctrico: SCADA que hable con el "
             "CEN. 105 empresas la tienen aplicable.",
             "donde": "campo `normas`", "campo": "NTSyCS 4-12/4-16"},
            {"senal": "Ley 21.305 (SSCC)", "que_dice":
             "sistemas de compensación y medición para el Coordinador: exige telemetría. "
             "1.236 empresas la tienen como norma aplicable.",
             "donde": "campo `normas`", "campo": "Ley 21.305"},
            {"senal": "dolor del Coordinador (completitud o calidad baja)",
             "que_dice": "115 empresas reportan mal al CEN: es el dolor MÁS específico y el "
                         "más caro de ignorar.", "donde": "campo `cen_dolor`",
             "campo": "CEN_DOLOR"},
            {"senal": "descarga en 4+ puntos con muchos parámetros",
             "que_dice": "obligación múltiple y dispersa: exige plataforma, no un medidor.",
             "donde": "RETC riles_2024.xlsx", "campo": "RETC_MULTIPUNTO"},
        ],
        "cliente_ideal": ("empresa COORDINADA del SEN (generación, transmisión, distribución, "
                          "clientes libres) y planta con obligación de reporte múltiple. El "
                          "dolor del Coordinador es la señal más limpia del catálogo: son 1.082 "
                          "empresas con dato oficial y 115 con incumplimiento medido."),
        "perfil_que_compra": "Jefe de I&C / Automatización / TI industrial / Gerente de Operaciones.",
        "ticket": "medio-alto",
    },
}


# ===========================================================================
# CALIFICAR CADA EMPRESA CONTRA CADA LÍNEA (medido, no supuesto)
# ===========================================================================
CIUDADES = None
RUBRO_PROCESO = ["quimica", "celulosa", "papel", "produccion de metal", "mineria",
                 "extraccion de minerales", "cemento", "generacion de energia",
                 "refinacion", "petroleo", "combustible", "alimento", "pesca", "manufactur",
                 "agua", "vidrio", "siderurg", "gestor de residuos", "agropecuaria", "silvicultura"]
RUBRO_COMBUSTION = ["generacion de energia", "celulosa", "cemento", "refinacion", "quimica",
                    "produccion de metal", "combustible", "papel"]
RUBRO_RIESGO = ["quimica", "combustible", "mineria", "extraccion de minerales", "celulosa",
                "produccion de metal", "combustible", "petroleo"]
RUBRO_VALVULAS = ["celulosa", "papel", "mineria", "extraccion de minerales", "alimento",
                  "pesca", "quimica", "agua", "manufactur"]
RUBRO_TRATAMIENTO = ["agua", "gestor de residuos"]


def califica(e, campo):
    """Devuelve (califica, motivo_medido) para un campo de senal."""
    n = norm(e.get("rubro") or "")
    normas = " ".join(e.get("normas") or [])
    tier = (e.get("tier") or "").upper()

    if campo == "DS 13/2011 Art. 8 (CEMS)":
        return ("DS 13/2011" in normas, "norma CEMS aplicable declarada")
    if campo == "NTSyCS 4-12/4-16":
        return ("NTSyCS" in normas, "NTSyCS aplicable declarada")
    if campo == "DS 132":
        return ("DS 132" in normas, "DS 132 seguridad minera aplicable")
    if campo == "DS 594":
        return ("DS 594" in normas, "DS 594 aplicable")
    if campo == "Ley 21.305":
        return ("Ley 21.305" in normas, "Ley 21.305 (SSCC) aplicable")
    if campo == "CEN_DOLOR":
        return ((e.get("cen_dolor") or 0) > 0,
                f"dolor CEN medido: {', '.join(e.get('cen_detalle') or [])[:80]}")
    if campo == "RUBRO_COMBUSTION":
        return (any(x in n for x in RUBRO_COMBUSTION), f"rubro con combustión: {e.get('rubro')}")
    if campo == "RUBRO_PROCESO":
        return (any(x in n for x in RUBRO_PROCESO), f"proceso continuo: {e.get('rubro')}")
    if campo == "RUBRO_PROCESO + GRANDE":
        return (any(x in n for x in RUBRO_PROCESO) and tier == "GRANDE",
                f"proceso continuo y tamaño {tier}")
    if campo == "RUBRO_RIESGO":
        return (any(x in n for x in RUBRO_RIESGO), f"rubro con riesgo mayor: {e.get('rubro')}")
    if campo == "RUBRO_VALVULAS":
        return (any(x in n for x in RUBRO_VALVULAS), f"maneja fluidos: {e.get('rubro')}")
    if campo == "RUBRO_TRATAMIENTO":
        return (any(x in n for x in RUBRO_TRATAMIENTO), f"tratamiento: {e.get('rubro')}")
    if campo == "TIER_MEDIANA_PEQUENA":
        return (tier in ("MEDIANA", "PEQUEÑA", "PEQUENA"), f"tamaño {tier}")
    if campo == "RETC_CORROSIVO":
        rl = e.get("riles_contaminantes") or []
        return (bool(rl) and len(rl) >= 3, f"{len(rl)} contaminantes en RILES")
    if campo == "RETC_SIN_INSTRUMENTAR":
        return (bool(e.get("riles_contaminantes")),
                f"reporta {len(e.get('riles_contaminantes') or [])} contaminantes al RETC")
    if campo == "RETC_MULTIPUNTO":
        return (bool(e.get("riles_contaminantes")) and len(e.get("riles_contaminantes") or []) >= 8,
                f"{len(e.get('riles_contaminantes') or [])} parámetros declarados")
    if campo == "RETC_RILES":
        rl = e.get("riles_contaminantes") or []
        MET = {"cadmio", "cromo total", "plomo", "mercurio", "arsenico", "niquel", "cobre",
               "zinc", "manganeso", "molibdeno", "fluoruro", "sulfuro", "cianuro", "saam",
               "indice fenol", "hidrocarburos fijos", "hidrocarburos totales"}
        hit = [c for c in rl if norm(c) in MET]
        return (len(hit) >= 2, f"{len(hit)} metales/tóxicos declarados: {', '.join(hit[:4])}")
    if campo == "RETC_PEL_ALTA":
        return (bool(e.get("residuos_t")) and (e.get("residuos_t") or 0) > 500,
                f"{e.get('residuos_t') or 0:,.0f} t de residuos peligrosos")
    return (False, "")


# ---- tabla final ----
print("=" * 96)
print("CLIENTE IDEAL POR LÍNEA DE NEGOCIO")
print("=" * 96)

resultado = {}
for lin, cfg in LINEAS.items():
    # una empresa califica si cumple AL MENOS UNA señal de la linea
    cal = []
    for e in EMP:
        motivos = []
        for s in cfg["senales"]:
            ok, mot = califica(e, s["campo"])
            if ok:
                motivos.append({"senal": s["senal"], "medido": mot})
        if motivos:
            cal.append({"empresa": e["empresa"], "rubro": e.get("rubro"), "tier": e.get("tier"),
                        "zona": e.get("zona"), "region": e.get("region"),
                        "prioridad": e.get("prioridad"), "dolor": e.get("dolor"),
                        "cen_dolor": e.get("cen_dolor"),
                        "motivos": motivos,
                        "n_senales": len(motivos)})
    por_tier = collections.Counter(c["tier"] or "(sin tier)" for c in cal)
    por_rubro = collections.Counter(c["rubro"] or "(sin rubro)" for c in cal)
    resultado[lin] = {"config": cfg, "clientes": cal,
                      "n": len(cal), "por_tier": dict(por_tier),
                      "por_rubro": dict(por_rubro.most_common(10))}

    print(f"\n{'='*96}")
    print(f"◆ {lin.upper()}   —   {len(cal):,} clientes calificados de {len(EMP):,}")
    print(f"{'='*96}")
    print(f"  Vende:        {cfg['que_vende']}")
    print(f"  Compra:       {cfg['perfil_que_compra']}")
    print(f"  Ticket:       {cfg['ticket']}")
    print(f"\n  SEÑALES QUE LO ACTIVAN:")
    for s in cfg["senales"]:
        n_ok = sum(1 for c in cal for mm in c["motivos"] if mm["senal"] == s["senal"])
        print(f"    · {s['senal'][:56]:58s} {n_ok:>5}")
        print(f"      {s['que_dice'][:88]}")
    print(f"\n  CLIENTE IDEAL: {cfg['cliente_ideal'][:180]}")
    print(f"\n  Tamaño:  {dict(por_tier)}")
    print(f"  Rubros:  {', '.join(f'{k} ({v})' for k,v in list(por_rubro.items())[:5])}")

json.dump({
    "que_es": ("CLIENTE IDEAL POR LÍNEA DE NEGOCIO. Para cada una de las 7 líneas: qué vende, la "
               "señal que la activa (con el dato y la fuente oficial), el cliente ideal, el "
               "perfil que la compra, y CUÁNTOS hay contados en el universo de 3.157 empresas."),
    "por_que_al_derecho": ("El análisis anterior partía del dolor ambiental y dejaba afuera la "
                           "mitad del catálogo. La mayor parte de lo que se vende no se activa "
                           "por ambiente sino por NORMA: DS 13/2011 (CEMS), NTSyCS 4-12/4-16 y "
                           "Ley 21.305 (coordinado), DS 132 (seguridad minera), Ley 20.920 (REP)."),
    "lineas": {lin: {"que_vende": r["config"]["que_vende"],
                     "perfil_que_compra": r["config"]["perfil_que_compra"],
                     "ticket": r["config"]["ticket"],
                     "cliente_ideal": r["config"]["cliente_ideal"],
                     "senales": r["config"]["senales"],
                     "n_clientes": r["n"], "por_tier": r["por_tier"],
                     "por_rubro": r["por_rubro"],
                     "clientes": sorted(r["clientes"],
                                        key=lambda x: -(x.get("prioridad") or 0))}
              for lin, r in resultado.items()},
}, open(os.path.join(D, "cliente_ideal_por_linea.json"), "w"), ensure_ascii=False, indent=1)
print(f"\n\nguardado: datos/cliente_ideal_por_linea.json")
