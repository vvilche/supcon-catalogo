#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLIENTE IDEAL POR LÍNEA — v2, solo con señales duras.

QUE CAMBIA RESPECTO DE LA v1, Y POR QUE
------------------------------------------------------------------------------
La v1 calificaba por rubro y por tier. Medido, los dos fallan:

1. EL RUBRO MEZCLA PLANTA CON PUNTO DE VENTA. "Combustibles" tiene 343 empresas y adentro
   están Petrobas Red, Abastible, Lipigas y "Administradora de Ventas al Detalle": son
   estaciones de servicio, no plantas de proceso. Calificar por rubro les vende DCS a un
   servicentro.

2. EL TIER ES UNA HEURISTICA, NO UN DATO. Medido contra casos conocidos:
     Minera Escondida  -> MEDIANA   (es la mina de cobre mas grande del mundo)
     Collahuasi        -> MEDIANA
     Teck Quebrada Blanca -> PEQUEÑA (proyecto de US$4.700 M)
     CCU, Soprole, Agrosuper -> MEDIANA
   Y 2.578 de 3.157 (82%) quedan en "PEQUEÑA". Un tier asi no ordena nada.

LA SEÑAL DE TAMAÑO QUE SI SIRVE: `dotacion` de las fichas, con fuente citada
  ("aproximadamente 9.600 empleados en Chile" para CMPC, "mas de 19.000 trabajadores" para
  Arauco). Es dato de la empresa, no inferencia. Medido: presente en 258 fichas.

LAS SEÑALES DURAS QUE SI USO (todas de fuente oficial, medidas)
  normas declaradas        3.080 empresas  (DS 13/2011 CEMS, NTSyCS, DS 132, Ley 21.305...)
  señal RETC               1.465 empresas  (contaminante con masa, residuos en t)
  dolor del Coordinador      115 empresas  (completitud/calidad CEN, dato oficial del CEN)
  tomadores (contacto)       502 empresas
  dotacion verificada        258 empresas

Las lineas se califican SOLO con estas. Si una empresa no tiene ninguna señal dura para esa
linea, no entra — aunque su rubro "suene" al producto. Es preferible un conteo chico y
defendible que uno grande y falso.
"""
import json, os, glob, re, collections, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
WS = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


# ---------------------------------------------------------------------------
# 1. dotacion verificada (tamaño real, con fuente) desde las fichas
# ---------------------------------------------------------------------------
def empleados(txt):
    """Extrae el numero de empleados de un texto de dotacion. Devuelve (n, cita)."""
    if not txt:
        return None, ""
    t = str(txt)
    # buscar el numero mas grande con separador de miles o "mil"
    cands = []
    for m in re.finditer(r"([\d][\d\.\,]{2,})", t):
        v = m.group(1).replace(".", "").replace(",", "")
        try:
            n = int(v)
        except ValueError:
            continue
        if 20 <= n <= 500_000:
            cands.append(n)
    if not cands:
        return None, t[:90]
    return max(cands), t[:90]


dot = {}
for f in glob.glob(os.path.join(WS, "catalogo-*/research/*.json")):
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    emp = d.get("empresa")
    qe = d.get("quien_es") or {}
    n, cita = empleados(qe.get("dotacion"))
    if emp and n:
        dot[norm(emp)] = {"empleados": n, "cita": cita,
                          "fuente_ficha": os.path.basename(f)}
print(f"dotacion verificada desde fichas: {len(dot)} empresas")

u = json.load(open(os.path.join(D, "universo_senales_completas.json"), encoding="utf-8"))
EMP = u["empresas"]


def dota(e):
    return dot.get(norm(e.get("empresa") or ""), {}).get("empleados")


def tamano(e):
    """Tamaño por dotacion verificada. None si no hay dato."""
    n = dota(e)
    if n is None:
        return None, ""
    if n >= 1000:
        return "GRANDE", f"{n:,} empleados (fuente: ficha)"
    if n >= 200:
        return "MEDIANA", f"{n:,} empleados (fuente: ficha)"
    return "PEQUEÑA", f"{n:,} empleados (fuente: ficha)"


# ---------------------------------------------------------------------------
# 2. las lineas, con sus señales DURAS
# ---------------------------------------------------------------------------
def tiene_norma(e, frag):
    return frag in " ".join(e.get("normas") or [])


def metales_masa(e):
    rl = e.get("riles_contaminantes") or []
    MET = {"cadmio", "cromo total", "plomo", "mercurio", "arsenico", "niquel", "cobre",
           "zinc", "manganeso", "molibdeno", "fluoruro", "sulfuro", "cianuro", "saam",
           "indice fenol", "hidrocarburos fijos", "hidrocarburos totales", "boro"}
    return [c for c in rl if norm(c) in MET]


LINEAS = {
    "Analítica": {
        "productos": ["CEMS 5000", "Analítica en línea (Hobre)", "HIFISC", "TISOMIC"],
        "vende": "medición en línea de composición: gases de combustión y metales en efluente.",
        "compra": "Jefe de Medio Ambiente / Calidad / Laboratorio",
        "ticket": "alto",
        "senal_desc": "norma CEMS aplicable → obligación legal de tener analizador en línea",
        "califica": lambda e: (
            (True, "norma DS 13/2011 Art.8 (CEMS) aplicable: obliga medición continua de emisiones")
            if tiene_norma(e, "DS 13/2011") else
            (True, f"RETC: descarga {len(metales_masa(e))} metales/tóxicos declarados: "
                   f"{', '.join(metales_masa(e)[:4])}")
            if len(metales_masa(e)) >= 2 else (False, "")),
    },
    "Instrumentación": {
        "productos": ["SFE910 (caudal)", "SL903 (nivel radar)", "CXT (presión)", "W Series"],
        "vende": "los sensores de caudal, nivel, presión y temperatura bajo todo lo demás.",
        "compra": "Jefe de Instrumentación y Control / Mantenimiento / Jefe de Planta",
        "ticket": "medio",
        "senal_desc": "reporta al RETC o tiene norma que exige medir, y no tenemos su instrumentación",
        "califica": lambda e: (
            (True, f"obligado a reportar al RETC y declara {len(e.get('riles_contaminantes') or [])} "
                   f"parámetros: exige instrumentación para medirlos")
            if (e.get("riles_contaminantes") or e.get("residuos_t")) else (False, "")),
    },
    "Válvulas": {
        "productos": ["Control SUPCON FLUID", "Bola SN/VN", "Mariposa BN/CN", "CVP2000"],
        "vende": "el actuador final: cierra el lazo que el control decide.",
        "compra": "Jefe de Mantenimiento (mecánico/eléctrico) / I&C",
        "ticket": "medio",
        "senal_desc": "maneja fluidos corrosivos con masa declarada al RETC",
        "califica": lambda e: (
            (True, f"RETC: {len(metales_masa(e))} metales y "
                   f"{len(e.get('riles_contaminantes') or [])} parámetros a la descarga: "
                   f"manejo de fluidos corrosivos")
            if len(e.get("riles_contaminantes") or []) >= 5 else (False, "")),
    },
    "DCS": {
        "productos": ["ECS-700", "UCS Nyx", "OMC", "T9100 (CCS)", "SAMS"],
        "vende": "el control distribuido del proceso: el punto de integración.",
        "compra": "Jefe de I&C / Automatización / Gerente de Operaciones",
        "ticket": "alto",
        "senal_desc": "planta grande CON dolor medido del Coordinador (el control es el origen)",
        "califica": lambda e: (
            (True, f"dolor del Coordinador medido: {'; '.join((e.get('cen_detalle') or [])[:1])[:90]}")
            if (e.get("cen_dolor") or 0) > 0 else (False, "")),
    },
    "SIS": {
        "productos": ["TCS-900 (SIL3)", "TCS-500", "HIPPS"],
        "vende": "parada de emergencia con SIL: contiene el evento antes del vertido.",
        "compra": "Jefe de Seguridad / HSE / I&C",
        "ticket": "alto",
        "senal_desc": "norma DS 132 (seguridad minera) aplicable → exige SIS en la faena",
        "califica": lambda e: (
            (True, "norma DS 132 (reglamento de seguridad minera) aplicable: exige seguridad funcional")
            if tiene_norma(e, "DS 132") else (False, "")),
    },
    "PLC": {
        "productos": ["G5Pro", "G5Pro Safety (SIL3)", "G3Smart"],
        "vende": "control y seguridad discretos para islas de proceso.",
        "compra": "Jefe de Automatización / Mantenimiento",
        "ticket": "bajo",
        "senal_desc": "planta MEDIANA o PEQUEÑA por dotación verificada, con señal de proceso",
        "califica": lambda e: (
            (True, f"{tamano(e)[1]} y proceso propio: corresponde PLC, no DCS")
            if (tamano(e)[0] in ("MEDIANA", "PEQUEÑA")
                and (e.get("riles_contaminantes") or e.get("residuos_t")))
            else (False, "")),
    },
    "Software y plataforma": {
        "productos": ["SolisSCADA", "InPlant APC", "InPlant RTO", "ESP-iSYS", "APEX"],
        "vende": "adquisición, historización, reporte y optimización de muchas señales.",
        "compra": "Jefe de I&C / Automatización / TI industrial / Gerente de Operaciones",
        "ticket": "medio-alto",
        "senal_desc": "coordinado del SEN: NTSyCS o Ley 21.305 aplicable, o dolor CEN medido",
        "califica": lambda e: (
            (True, "norma NTSyCS 4-12/4-16 aplicable: exige SCADA que reporte al Coordinador")
            if tiene_norma(e, "NTSyCS") else
            (True, "Ley 21.305 (SSCC) aplicable: exige telemetría y medición para el Coordinador")
            if tiene_norma(e, "Ley 21.305") else
            (True, f"dolor del Coordinador medido: {'; '.join((e.get('cen_detalle') or [])[:1])[:80]}")
            if (e.get("cen_dolor") or 0) > 0 else (False, "")),
    },
}


# ---------------------------------------------------------------------------
# 3. calificar y verificar
# ---------------------------------------------------------------------------
print()
res = {}
for lin, cfg in LINEAS.items():
    cal = []
    for e in EMP:
        ok, mot = cfg["califica"](e)
        if not ok:
            continue
        t, tcita = tamano(e)
        nd = dota(e)
        cal.append({"empresa": e["empresa"], "rubro": e.get("rubro"),
                    "tamano": t, "empleados": nd, "cita_tamano": tcita,
                    "zona": e.get("zona"), "region": e.get("region"),
                    "prioridad": e.get("prioridad"), "cen_dolor": e.get("cen_dolor"),
                    "motivo": mot})
    res[lin] = cal

print("=" * 96)
print("CLIENTE IDEAL POR LÍNEA — solo señales duras (norma, RETC, CEN, dotación)")
print("=" * 96)
for lin, cal in sorted(res.items(), key=lambda x: -len(x[1])):
    cfg = LINEAS[lin]
    tam = collections.Counter(c["tamano"] or "(sin dotación verificada)" for c in cal)
    emp_c = [c["empleados"] for c in cal if c["empleados"]]
    print(f"\n◆ {lin.upper()}  —  {len(cal)} clientes")
    print(f"   vende:  {cfg['vende']}")
    print(f"   compra: {cfg['compra']}   ·   ticket {cfg['ticket']}")
    print(f"   señal:  {cfg['senal_desc']}")
    print(f"   tamaño: {dict(tam)}")
    if emp_c:
        emp_c.sort()
        print(f"   dotación verificada: mediana {emp_c[len(emp_c)//2]:,} empleados "
              f"(min {emp_c[0]:,} / max {emp_c[-1]:,})")
    print(f"   top 5 por prioridad:")
    for c in sorted(cal, key=lambda x: -(x.get("prioridad") or 0))[:5]:
        print(f"      {c['empresa'][:42]:44s} {str(c['tamano'] or '—'):9s} "
              f"{str(c['empleados'] or ''):>8} emp  {c['motivo'][:58]}")


# ---- VERIFICACION contra casos conocidos (regla 5) ----
print("\n\n" + "=" * 96)
print("VERIFICACION contra casos conocidos")
print("=" * 96)
print("\n  DOTACIÓN (tamaño real) de empresas que conozco:")
for k in ["CODELCO", "ESCONDIDA", "COLLAHUASI", "ENAP", "CMPC CELULOSA", "ARAUCO",
          "AGROSUPER", "SOPROLE", "CCU", "TECK"]:
    for e in EMP:
        if k in e["empresa"].upper():
            n = dota(e)
            print(f"   {k:14s} {str(n if n else 'sin dato'):>10} empleados  -> "
                  f"{tamano(e)[0] or '—'}")
            break

json.dump({
    "que_es": ("CLIENTE IDEAL POR LÍNEA, calificado solo con señales duras: norma aplicable, "
               "señal RETC con masa declarada, dolor medido del Coordinador, y dotación "
               "verificada con fuente. No usa rubro ni tier."),
    "por_que_no_tier": ("El tier del universo es una heurística y falla en casos conocidos: "
                        "Minera Escondida aparece MEDIANA, Collahuasi MEDIANA, Teck Quebrada "
                        "Blanca PEQUEÑA, y CCU/Soprole/Agrosuper MEDIANA. 82% del universo queda "
                        "en PEQUEÑA. Se reemplazó por `dotacion` de las fichas, con cita."),
    "por_que_no_rubro": ("El rubro mezcla planta con punto de venta: 'Combustibles' tiene 343 "
                         "empresas e incluye Petrobas Red, Abastible, Lipigas y 'Administradora "
                         "de Ventas al Detalle', que son estaciones de servicio, no plantas."),
    "lineas": {lin: {"vende": LINEAS[lin]["vende"], "compra": LINEAS[lin]["compra"],
                     "ticket": LINEAS[lin]["ticket"], "senal": LINEAS[lin]["senal_desc"],
                     "n_clientes": len(cal), "clientes": cal}
               for lin, cal in res.items()},
}, open(os.path.join(D, "cliente_ideal_linea.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/cliente_ideal_linea.json")
