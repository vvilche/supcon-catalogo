#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HISTORIA COMERCIAL INECO (2004 -> FY14): las cuentas y productos que se repiten.

QUÉ HACE
------------------------------------------------------------------------------
Cruza los planes de negocio de INECO (la operación chilena como Local Business Partner de
Emerson/Rosemount, 2003-2014) y extrae lo que SE REPITE a lo largo de 11 años:
  - las cuentas que aparecen una y otra vez (y siguen siendo clientes hoy),
  - los productos/líneas que se vendían,
  - los competidores que se nombran,
  - los EPC con los que se trabajaba,
  - los proyectos grandes con su monto.

POR QUÉ SIRVE HOY
------------------------------------------------------------------------------
CONECTA vende hoy instrumentación, analítica y válvulas SUPCON a las MISMAS plantas. La
historia permite: (1) saber qué cuenta lleva 20 años comprando, (2) qué producto reemplaza al
que ya tienen instalado, (3) quién era el competidor entonces y sigue siéndolo.

FUENTES (extraídas a texto, no inventadas)
  /tmp/plan2004.txt                 Plan de Negocios 2004 (Division Instrumentos)
  /tmp/ineco/ineco_slides.txt       FY08 (65 slides) + FY09 (67) + FY14 (47)
"""
import re, json, collections, os

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")

FUENTES = ["/tmp/plan2004.txt", "/tmp/ineco/ineco_slides.txt"]
texto = ""
for f in FUENTES:
    if os.path.exists(f):
        texto += open(f, encoding="utf-8", errors="replace").read() + "\n"
    else:
        print(f"AVISO: falta {f}")
print(f"texto total: {len(texto):,} chars de {len(FUENTES)} fuentes")

# ---------------------------------------------------------------------------
# CUENTAS: las que se nombran en los planes. Se normalizan a la razón social del catálogo.
# ---------------------------------------------------------------------------
CUENTAS = {
    "CODELCO": ["codelco", "division andina", "radomiro tomic", "ministro hales", "chuquicamata",
                "el teniente", "el salvador", "division ventanas", "division gaby"],
    "ARAUCO": ["arauco", "constitución", "constitucion", "licancel", "nueva aldea", "valdivia",
               "viñales", "vi nales", "trupan", "paneles arauco", "aserradero arauco",
               "planta arauco", "bioenergia"],
    "CMPC": ["cmpc", "pacífico cmpc", "pacifico cmpc", "planta laja", "planta maule",
             "inforsa", "santa fe", "santafe", "cmpc madera", "cmpc pulp"],
    "ENAP": ["enap", "aconcagua", "petrox", "rpc", "refinerías bio bio", "refinerias bio bio",
             "quintero enap", "enap magallanes"],
    "ESCONDIDA": ["escondida"],
    "COLLAHUASI": ["collahuasi"],
    "PELAMBRES": ["pelambres", "mlp"],
    "CANDELARIA": ["candelaria"],
    "EL ABRA": ["el abra"],
    "SPENCE": ["spence"],
    "GABY": ["gaby"],
    "QUEBRADA BLANCA": ["quebrada blanca"],
    "ANGLO AMERICAN": ["anglo american", "el soldado", "chagres", "los bronces"],
    "METHANEX": ["methanex"],
    "COLBUN": ["colbún", "colbun"],
    "AES GENER": ["aes gener", "aes rena", "aes andes", "campiche", "ventanas aes"],
    "GUACOLDA": ["guacolda"],
    "SQM": ["sqm"],
    "ENAEX": ["enaex", "panna4", "panna 4"],
    "OXIQUIM": ["oxiquim"],
    "MASISA": ["masisa"],
    "ARAUCO PANELES": ["paneles arauco"],
    "E-CL": ["e-cl", "cta-cth", "ctm", "ctt"],
    "GASATACAMA": ["gas atacama", "gnl mejillones"],
    "GNL QUINTERO": ["gnl quintero", "lng quinteros"],
    "ABASTIBLE": ["abastible"],
    "LIPIGAS": ["lipigas"],
    "COPEC": ["copec"],
    "CAP / HUACHIPATO": ["huachipato", "empresas cap", " cmp / cap"],
    "Ecometales": ["ecometales"],
    "Zaldívar": ["zaldivar", "zaldívar"],
    "Antucoya": ["antucoya"],
    "Pucobre": ["pucobre"],
    "Pampa Camarones": ["pampa camarones"],
    "Cerro Colorado": ["cerro colorado"],
    "Lomas Bayas": ["lomas bayas"],
    "Mantos Blancos": ["mantos blancos"],
    "Franke": ["franke"],
    "El Tesoro": ["el tesoro"],
    "Michilla": ["michilla"],
    "Meridian El Peñón": ["el peñón", "el penon"],
    "Norgener": ["norgener"],
    "Corpesca": ["corpesca"],
    "Cementos Bío Bío": ["cementos bio bio"],
    "Colun": ["colun"],
    "IANSA": ["iansa"],
    "Nestlé": ["nestle", "nestlé"],
    "Norske Skog": ["norske skog"],
    "Georgia Pacific": ["georgia pacific"],
    "Vidrios Lirquén": ["vidrios lirquen", "vidrios lirquén"],
    "Ancali": ["ancali"],
    "Bocamina": ["bocamina"],
    "Catamutún": ["catamutun", "catamutún"],
    "Oleoducto Trasandino": ["oleoducto trasandino"],
    "Indura": ["indura"],
    "AGA / Air Liquide": ["aga", "air liquide"],
    "Metrogas": ["metrogas"],
    "Endesa": ["endesa"],
    "GIST BROCADES": ["gist brocades"],
}

# ---------------------------------------------------------------------------
# COMPETIDORES nombrados
# ---------------------------------------------------------------------------
COMPETIDORES = {
    "ABB": ["abb", "ac800"],
    "Emerson/Rosemount (propio)": ["rosemount", "delta v", "deltav", "fisher", "plantweb",
                                   "micro motion", "micromotion"],
    "Honeywell": ["honeywell", "tdc3000", "infi90", "bailey"],
    "Yokogawa": ["yokogawa", "yew"],
    "Endress+Hauser": ["e+h", "endress"],
    "Siemens": ["siemens", "pcs7"],
    "Invensys / Foxboro / IA": ["invensys", "foxboro", "ia invensys", "mod300", "modicom"],
    "Schneider / Rockwell": ["schneider", "rockwell", "modicom"],
    "Dezurik": ["dezurik"],
    "Samson": ["samson"],
    "Masoneilan": ["masoneilan"],
    "Neles": ["neles"],
    "Mesura": ["mesura"],
    "Maxcontrol": ["maxcontrol"],
}

# ---------------------------------------------------------------------------
# EPC / Ingenierías nombradas
# ---------------------------------------------------------------------------
EPCS = ["fluor", "bechtel", "aker", "amc", "amec", "snc lavalin", "hatch", "worley",
        "santiago", "kvaerner", "foster wheeler", "inacap", "proingesa", "pares y alvarez",
        "millan y seguel", "ingeo", "SIM", "green", "masisa", "wood"]

# ---------------------------------------------------------------------------
# PRODUCTOS / LÍNEAS
# ---------------------------------------------------------------------------
PRODUCTOS = {
    "Presión (RMT)": ["presión", "presion", "pressure", "3051", "2088", "1151", "3095", "333u"],
    "Temperatura (RMT)": ["temperatura", "temperature", "3144", "644h", "848t", "0068", "0078"],
    "DP Flow (RMT)": ["dp flow", "405", "1595", "annubar", "caudal"],
    "Nivel": ["nivel", "level", "radar", "3300", "5600", "5300", "sl903"],
    "Analítica (PAD/RAI)": ["analizador", "analitica", "analítica", "cem", "cems", "gas",
                            "oximeter", "oxímetro", "cromatograf", "ph ", "xstream", "raí"],
    "Válvulas (FCS)": ["válvula", "valvula", "valve", "fisher", "dvc", "control valve"],
    "Sistemas (PSS)": ["delta v", "deltav", "dcs", "sys", "scada", "sistema de control"],
    "AO / AMS (activos)": [" ams", "asset", "ao ", "gestión de activos", "diagnostico",
                           "predictivo", "guardian"],
    "Wireless": ["wireless", "inalámbric", "inalambric"],
    "Reguladores (REGS)": ["regulador", "regs", "95h", "1098", "bryan donkin", "tescom"],
    "MRO / Reposición": ["mro", "reposición", "reposicion", "base instalada"],
}

res = {"fuentes": FUENTES, "que_es": (
 "Historia comercial de INECO (operación chilena como Local Business Partner de Emerson/Rosemount, "
 "2003-2014) extraída de sus planes de negocio, cruzada contra el trabajo actual. Sirve para ver "
 "qué cuenta lleva 20 años comprando y qué competidor sigue siendo el mismo.")}

low = texto.lower()
for nombre, pats in CUENTAS.items():
    n = sum(low.count(p) for p in pats)
    if n:
        res.setdefault("cuentas", {})[nombre] = {"menciones": n}

res["competidores"] = {}
for nombre, pats in COMPETIDORES.items():
    n = sum(low.count(p) for p in pats)
    if n:
        res["competidores"][nombre] = n

res["productos"] = {}
for nombre, pats in PRODUCTOS.items():
    n = sum(low.count(p) for p in pats)
    if n:
        res["productos"][nombre] = n

res["epcs"] = {e: low.count(e) for e in EPCS if low.count(e)}

# ---- CRUCE con el trabajo de hoy ----
def load(p):
    return json.load(open(os.path.join(D, p), encoding="utf-8")) if os.path.exists(os.path.join(D, p)) else None

per = load("personas_todas.json")
da = load("dolor_ambiental_empresas.json")
pc = load("plan_contacto.json")
per_emp = per["por_empresa"] if per else {}
dolor = {e["empresa"].upper(): e for e in (da["empresas"] if da else [])}
plan = {p["empresa"].upper(): p for p in (pc["plan"] if pc else [])}

def buscar_hoy(patrones):
    """¿Existe esta cuenta hoy en mis datos? Personas + dolor + plan, cada uno por separado.

    OJO (bug corregido): la primera versión solo buscaba el dolor si NO había personas, así que
    las cuentas que sí tienen gente salían con la carga tóxica vacía. Son datos independientes:
    se consultan los tres siempre.
    """
    out = None
    # 1) personas por área
    for e in per_emp:
        el = e.lower()
        if any(p in el for p in patrones):
            if out is None:
                out = {"empresa_hoy": e, "areas": 0, "personas": 0, "carga_toxica": None,
                       "respel_t": None, "en_plan": False, "dolor": None, "prio": None}
            out["areas"] = max(out["areas"], len(per_emp[e]))
            out["personas"] += sum(len(v) for v in per_emp[e].values())
    # 2) dolor ambiental (SIEMPRE, no solo si falta gente)
    # OJO: las claves de `dolor` estan en MAYUSCULA, asi que hay que comparar en minuscula
    # (`p in u` daba False siempre: 'arauco' no esta en 'CELULOSA ARAUCO...').
    for u, e in dolor.items():
        if any(p in u.lower() for p in patrones):
            if out is None:
                out = {"empresa_hoy": e["empresa"], "areas": 0, "personas": 0,
                       "carga_toxica": None, "respel_t": None, "en_plan": False,
                       "dolor": None, "prio": None}
            out["carga_toxica"] = e.get("carga_peligrosa_t")
            out["respel_t"] = e.get("respel_t")
            break
    # 3) plan de contacto
    for u, p in plan.items():
        if any(x in u.lower() for x in patrones):
            if out is None:
                out = {"empresa_hoy": p["empresa"], "areas": 0, "personas": 0,
                       "carga_toxica": None, "respel_t": None, "en_plan": False,
                       "dolor": None, "prio": None}
            out["en_plan"] = True
            out["dolor"] = p.get("dolor")
            out["prio"] = p.get("prioridad_contacto")
            break
    return out

print("\n" + "=" * 92)
print("HISTORIA COMERCIAL INECO — CUENTAS QUE SE REPITEN 2003-2014, Y SU ESTADO HOY")
print("=" * 92)
filas = []
for nombre, pats in sorted(CUENTAS.items(), key=lambda x: -sum(low.count(p) for p in x[1])):
    n = sum(low.count(p) for p in pats)
    if not n:
        continue
    hoy = buscar_hoy(pats)
    filas.append((nombre, n, hoy))
    if hoy:
        ct = f"{hoy['carga_toxica']:>9,.1f}" if hoy.get("carga_toxica") is not None else "        —"
        pl = f"plan prio {hoy['prio']:>5.0f}" if hoy.get("en_plan") else "no en plan"
        print(f"  {nombre[:22]:24s} {n:>4} menc | HOY: {hoy['areas']} áreas, {hoy['personas']:>3} pers, "
              f"tóxicas {ct} t | {pl}")
    else:
        print(f"  {nombre[:22]:24s} {n:>4} menc | (sin registro hoy)")

print(f"\n=== productos/líneas que se vendían ===")
for k, v in sorted(res["productos"].items(), key=lambda x: -x[1]):
    print(f"   {k:24s} {v:>5} menciones")
print(f"\n=== competidores nombrados entonces ===")
for k, v in sorted(res["competidores"].items(), key=lambda x: -x[1]):
    print(f"   {k:28s} {v:>5}")
print(f"\n=== EPC / ingenierías ===")
print("   " + ", ".join(sorted(res["epcs"], key=lambda x: -res["epcs"][x])))

res["cruces_hoy"] = {n: h for n, _, h in filas}
json.dump(res, open(os.path.join(D, "historia_comercial_ineco.json"), "w"),
          ensure_ascii=False, indent=1)
print(f"\nguardado: datos/historia_comercial_ineco.json")
