#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAN 2009 DE VÁLVULAS (INECO/Fisher) — cruzado con el mercado de válvulas de hoy.

QUÉ ES EL DOCUMENTO
------------------------------------------------------------------------------
`Plan 2009 vvs.ppt`: el plan anual de la línea de VÁLVULAS DE CONTROL (Fisher) de INECO,
noviembre 2008. 73 slides. Es el documento MÁS ACCIONABLE de la serie INECO para un producto
puntual, porque trae:
  - metas por SEGMENTO con clientes principales y sus plantas exactas,
  - la lista de proyectos 2009 con monto y probabilidad de adjudicación,
  - el análisis de COMPETENCIA de válvulas por segmento (no genérico),
  - la tabla de RESULTADOS POR PLANTA (venta total, válvulas, margen, repuestos),
  - la proyección de mercado: "US$10M a US$12M, con 52% en 3 años".

POR QUÉ SIRVE HOY
------------------------------------------------------------------------------
CONECTA vende válvulas de control SUPCON. Este documento da, para el producto exacto:
  1. los CLIENTES PRINCIPALES con sus plantas (Arauco: Arauco y Nueva Aldea; CMPC: Pacífico y
     Laja; ENAP: Aconcagua, Bio Bio, Magallanes),
  2. el TAMAÑO del mercado de válvulas en Chile y la participación que se tenía,
  3. el COMPETIDOR por segmento y su debilidad concreta,
  4. el ARGUMENTO DE SERVICIO: "el crecimiento adicional debe producirse en el área de
     servicios, que reportará márgenes distintos" — el mismo argumento de hoy.

CRUCE CON HOY
------------------------------------------------------------------------------
Se compara la lista de clientes/plantas de válvulas 2009 contra el mercado de válvulas medido
por partida arancelaria (datos/mercado_valvulas_2025.json) y contra las empresas con dolor
ambiental y personas mapeadas.
"""
import re, json, os, collections

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
TXT = "/tmp/ineco/plan2009.txt"

if not os.path.exists(TXT):
    raise SystemExit(f"falta {TXT}: convertir el .ppt primero")

texto = open(TXT, encoding="utf-8", errors="replace").read()
low = texto.lower()
print(f"texto: {len(texto):,} chars")

# ===========================================================================
# 1. CLIENTES PRINCIPALES POR SEGMENTO (textual del documento)
# ===========================================================================
SEGMENTOS = {
    "M&M (minería)": {
        "clientes": ["CODELCO: NORTE Y TENIENTE", "MINERA ESCONDIDA", "ANGLOAMERICAN: CHAGRES Y LOS BRONCES",
                     "COLLAHUASI", "CSH"],
        "meta_2009": "MRO US$481K + PROJ US$203K = US$684K",
        "crecimiento": "30% sobre 2008 (US$370K)",
    },
    "P&P (celulosa y papel)": {
        "clientes": ["ARAUCO: ARAUCO Y NUEVA ALDEA", "CMPC: PACIFICO Y LAJA", "NORSKE-SKOG"],
        "meta_2009": "US$575K",
        "crecimiento": "25% sobre 2008 (US$460K)",
    },
    "Refinery": {
        "clientes": ["ENAP: REFINERIA ACONCAGUA", "REFINERIA BIO BIO", "MAGALLANES"],
        "meta_2009": "US$275K",
        "crecimiento": "25% (vía zona sur, ERA por servicios)",
    },
    "Power": {
        "clientes": ["GE Sigen (Nueva Renca)", "Electrogas", "Gas Atacama", "ENDESA"],
        "meta_2009": "US$75K",
        "crecimiento": "promedio de 2 años",
    },
    "Chemical": {
        "clientes": ["Methanex"],
        "meta_2009": "US$30K",
        "crecimiento": "segmento perdido por falta de gas en Magallanes",
    },
    "Others (F&B + EPC)": {
        "clientes": ["Actuadores, DVC, Reguladores y accesorios"],
        "meta_2009": "US$100K",
        "crecimiento": "promedio 3 años",
    },
}

# ===========================================================================
# 2. COMPETENCIA DE VÁLVULAS POR SEGMENTO (con su debilidad, textual)
# ===========================================================================
COMPETENCIA = {
    "Metso": ("M&M y P&P. Mantiene mercado apoyado desde Santiago; acuerdo con maestranza en "
              "Antofagasta para servicios; estrategia de precios. En P&P su departamento de "
              "servicios está decayendo (despidieron a César Montecinos)."),
    "Dezurik": ("Ataca base instalada de Metso y Fisher con precios y servicio local en "
                "Antofagasta. El producto 'no ha dejado buena impresión' y están terminando "
                "contrato con Escondida."),
    "Samson": ("Entró en CMPC Santa Fe, Valdivia, Laja y Maule. Arma: precios bajos MÁS entregas "
               "muy cortas (4 a 6 semanas en plaza)."),
    "Masoneilan": ("Cada vez menos presencia: solo 2 vendedores y sin servicios. Se mantiene por "
                   "precios bajos en proyectos internacionales; base instalada en Refinería "
                   "Bio Bio apoyada por un sponsor en ingeniería de la planta."),
    "Tyco / Bray / Least / Breay": ("No tradicionales en minería: compiten en oportunidades "
                                    "puntuales por precio y entrega."),
}

# ===========================================================================
# 3. PROYECTOS 2009 CON MONTO Y PROBABILIDAD
# ===========================================================================
PROYECTOS_VALV = [
    ("Pascua Lama", 1500, 40), ("Esperanza", 1000, 40), ("Expansión Andina", 400, 30),
    ("Expansión Los Bronces", 700, 30), ("El Morro", 1300, 30), ("LNG Mejillones", 800, 10),
]
PROYECTOS_POWER = [
    ("Termoeléctrica Angamos", "Norgener", 1000), ("Central Los Robles", "AES Gener", 1300),
    ("Termoeléctrica Quintero", "Endesa", 200), ("Central Farellones", "Codelco", 1500),
    ("Termoeléctrica Kelar", "BHP Billiton", 800), ("Central Cochrane", "Norgener", 1100),
    ("Central San Pedro (Riñihue)", "Colbún", 233), ("Termoeléctrico Energía Minera", "Codelco", 1700),
    ("Termoeléctrica Salar", "Codelco Norte", 65), ("Central Barracones", "Suez Andino", 1100),
]
PROYECTOS_REF = [
    ("HDT de ERA", 400, "Técnicas Reunidas"), ("Alkilación de ERA", 600, "Técnicas Reunidas"),
    ("Topping III de ERA", 1000, "Tecnip/Tipiel/P&A"),
]

# ===========================================================================
# 4. RESULTADOS POR PLANTA (la tabla del slide 68 — el dato más concreto)
# ===========================================================================
POR_PLANTA = [
    ("Planta Arauco", "Arauco", 469, 141, 28.6, 186, 45.6),
    ("Arauco Nueva Aldea", "Arauco", 394, 188, 56.9, 206, 43.0),
    ("CMPC Pacífico", "CMPC", 355, 57.7, 15.0, 287.3, 98.8),
    ("CMPC Laja", "CMPC", 128, 47, 13.6, 81, 16.9),
    ("CMPC Maule", "CMPC", 11.8, 11.8, 2.4, 0, 0),
    ("CSH (Huachipato)", "CAP", 25, 25, 4.7, 0, 0),
    ("Enap", "ENAP", 33, 33, 3.8, 33, 8.6),
    ("Norske Skog", "Norske Skog", 57, 17, 5.8, 40, 12.2),
    ("Constitución", "Arauco", 5.6, 0, 0, 5.7, 0),
    ("Licancel", "Arauco", 25, 0, 0, 25, 0),
]

# ===========================================================================
# MAPEO A LAS LÍNEAS DE HOY: los clientes de válvulas 2009 vs el catálogo/hoy
# ===========================================================================
def load(p):
    fp = os.path.join(D, p)
    return json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else None

per = load("personas_todas.json")
da = load("dolor_ambiental_empresas.json")
per_emp = per["por_empresa"] if per else {}
dolor = {e["empresa"].upper(): e for e in (da["empresas"] if da else [])}

MAPEO = {
    "CODELCO": ["codelco", "corp nacional del cobre"], "ESCONDIDA": ["escondida"],
    "ANGLO AMERICAN": ["anglo american"], "COLLAHUASI": ["collahuasi"],
    "CSH": ["huachipato", "acero"], "ARAUCO": ["arauco"],
    "CMPC": ["cmpc"], "NORSKE SKOG": ["norske"],
    "ENAP": ["enap"], "METHANEX": ["methanex"], "AES GENER": ["aes"],
    "ENDESA": ["endesa"], "COLBUN": ["colbun"], "NORGENER": ["norgener"],
    "GAS ATACAMA": ["gas atacama", "gnl mejillones"], "ELECTROGAS": ["electrogas"],
}

print("\n" + "=" * 96)
print("PLAN 2009 VÁLVULAS (Fisher) — CLIENTES PRINCIPALES Y SU ESTADO HOY")
print("=" * 96)
cruces = {}
for nombre, pats in MAPEO.items():
    personas = areas = 0; tox = None; emp_hoy = ""
    for e in per_emp:
        if any(p in e.lower() for p in pats):
            emp_hoy = emp_hoy or e
            areas = max(areas, len(per_emp[e]))
            personas += sum(len(v) for v in per_emp[e].values())
    for u, e in dolor.items():
        if any(p in u.lower() for p in pats):
            tox = e.get("carga_peligrosa_t"); break
    cruces[nombre] = {"empresa_hoy": emp_hoy, "areas": areas, "personas": personas,
                      "carga_toxica": tox}
    tx = f"{tox:>9,.1f} t" if tox is not None else "         —"
    print(f"  {nombre[:16]:18s} HOY: {areas} áreas, {personas:>3} personas, tóxicas {tx}  {emp_hoy[:34]}")

print(f"\n=== MERCADO DE VÁLVULAS: lo que decía el plan vs lo medido hoy ===")
mv = load("mercado_valvulas_2025.json")
if mv:
    # estructura: ver qué trae
    print(f"  documento mercado_valvulas_2025.json: {list(mv.keys())[:6]}")
    for k in ("mercado_usd", "total_usd", "mercado_total_usd"):
        if k in mv:
            print(f"  mercado medido hoy: US${mv[k]/1e6:,.1f}M")
    if "mercado_valvulas_control_usd" in mv:
        print(f"  válvulas de control: US${mv['mercado_valvulas_control_usd']/1e6:,.1f}M")
print('  DOCUMENTO 2008 decía: "mercado de válvulas US$10M a US$12M, con 52% en 3 años"')
print('  y "el crecimiento adicional debe producirse en el ÁREA DE SERVICIOS, que reportará')
print('  márgenes distintos" — el mismo argumento que hoy.')

json.dump({
    "que_es": ("Plan 2009 de VÁLVULAS DE CONTROL (Fisher) de INECO, nov-2008, 73 slides. El "
               "documento más accionable de la serie para un producto puntual: clientes por "
               "segmento con sus plantas, proyectos con monto y probabilidad, competencia "
               "específica de válvulas, y resultados por planta."),
    "por_que_sirve_hoy": ("CONECTA vende válvulas de control SUPCON: este documento da los "
                          "clientes con sus plantas exactas, el tamaño del mercado de válvulas "
                          "en Chile y la participación que se tenía, y el argumento de servicios."),
    "segmentos": SEGMENTOS,
    "competencia_valvulas": COMPETENCIA,
    "proyectos_valvulas_2009": [{"proyecto": p, "monto_k": m, "prob": pr} for p, m, pr in PROYECTOS_VALV],
    "proyectos_power_2009": [{"proyecto": p, "empresa": e, "inversion_us_m": m} for p, e, m in PROYECTOS_POWER],
    "proyectos_refineria_2009": [{"proyecto": p, "inversion_vv_k": m, "epc": e} for p, m, e in PROYECTOS_REF],
    "resultados_por_planta_2008": [
        {"planta": p, "grupo": g, "venta_total_k": vt, "valvulas_k": v, "margen_vv_k": m,
         "repuestos_k": r, "margen_rep_k": mr} for p, g, vt, v, m, r, mr in POR_PLANTA],
    "analisis_del_documento": {
        "operaciones_en_plaza": "74% del MRG+Utild corresponde a operaciones en plaza (2006: 71%, 2007: 80%)",
        "proyeccion_mercado": "mercado de válvulas US$10M-US$12M, proyectaba 15% de crecimiento anual y llegar a 52% en 3 años, 55% máximo",
        "el_argumento": "el crecimiento adicional debe producirse en el ÁREA DE SERVICIOS, que reporta márgenes distintos",
    },
    "cruces_hoy": cruces,
}, open(os.path.join(D, "plan2009_valvulas.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/plan2009_valvulas.json")
