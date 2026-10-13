#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOLOR → LÍNEA DE NEGOCIO — motor de reglas (v3, calibrado contra el dato).

QUE RESUELVE
------------------------------------------------------------------------------
El problema no era "a quién llamo" sino "qué le vendo a ESTA planta". Cada señal MEDIDA en el
RETC activa líneas de negocio de las 7 de CONECTA/SUPCON, con el producto y el argumento que se
defiende frente al cliente.

LA REGLA: la señal activa la línea, no el rubro
------------------------------------------------------------------------------
El vendedor no dice "le vendo DCS". Dice "declaró cadmio y cianuro en tu descarga y hoy no los
mides en línea". Eso se audita abriendo el RETC; un mapeo por rubro no se puede defender.

DOS CORRECCIONES MEDIDAS (v1 -> v2 -> v3)
------------------------------------------------------------------------------
v1 activaba 5-6 líneas en 193 de 370 empresas: a todos le vendía todo, o sea ninguna
priorización. Los infladores: DCS en 283/370 por un any() de rubro que matcheaba casi todo,
Válvulas en 234/370 por "corrosivo" (el 60% de los residuos), SIS en 222/370 por "inflamable".

v2 bajó DCS a 91 pero seguía inflada: Analítica en 86%, Instrumentación 62%, SIS 63%.
**La causa era un bug de fondo**: se analizaba el NOMBRE del contaminante sin verificar que
tuviera masa declarada. El DS 90 obliga a reportar TODOS los parámetros de su tabla, así que
"declara cadmio" no significa nada — puede estar en cero. Medido: la mediana de contaminantes
por empresa es 25 y el p75 es 29, es decir casi todos reportan casi todo. **El conteo de
contaminantes no distingue: es una obligación legal, no una señal de dolor.**

v3 (esta): una señal cuenta SOLO si tiene masa > 0 declarada. Y los umbrales se fijaron sobre
la distribución real medida, no a ojo:
  carga peligrosa (t): p25=0  mediana=0,6  p75=13,7  p90=92,3  max=8.692,9
  respel (t):          mediana=34,5  p75=268,8  p90=1.669,7
"""
import json, os, collections, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


LINEAS = {
    "Analítica": {
        "productos": ["CEMS 5000", "Analítica en línea (línea Hobre)", "HIFISC",
                      "NISOSYS-3", "TISOMIC", "C-QUAND"],
        "que_resuelve": ("medición en línea de la composición: metales, tóxicos y parámetros de "
                         "efluente. Es lo que la SMA exige para demostrar cumplimiento del DS 90 "
                         "y del DS 43."),
    },
    "Instrumentación": {
        "productos": ["SFE910 (caudal electromagnético)", "SL903 (radar de nivel 80 GHz)",
                      "CXT (transmisor de presión)", "W Series (temperatura)",
                      "LUGB (caudal vortex)", "YHLW (caudal por turbina)"],
        "que_resuelve": ("sensores de caudal, nivel, presión y temperatura. Sin instrumentación "
                         "no hay dato que reportar."),
    },
    "Software y plataforma": {
        "productos": ["SolisSCADA", "InPlant APC", "InPlant RTO", "InPlant MP3000",
                      "APEX", "ESP-iSYS"],
        "que_resuelve": ("adquisición, historización y reporte de muchas señales a la vez, en "
                         "varios puntos. Con decenas de parámetros no alcanza un medidor."),
    },
    "DCS": {
        "productos": ["ECS-700", "UCS Nyx", "OMC", "T9100 (CCS)", "SmartEIO y APL", "SAMS"],
        "que_resuelve": ("control distribuido del proceso. Es el punto de integración donde se "
                         "cuelgan analítica e instrumentación."),
    },
    "SIS": {
        "productos": ["TCS-900", "TCS-500", "HIPPS"],
        "que_resuelve": ("parada de emergencia con SIL, para contener el evento antes de que sea "
                         "vertido."),
    },
    "Válvulas": {
        "productos": ["Válvulas de control SUPCON FLUID", "Válvulas de bola",
                      "Válvulas mariposa y excéntricas", "CVP2000 (posicionador inteligente)"],
        "que_resuelve": ("el actuador final: cierra el lazo que el control decide."),
    },
    "PLC": {
        "productos": ["G5Pro", "G5Pro Safety (SIL3)", "G3Smart"],
        "que_resuelve": ("control y seguridad discretos para islas de proceso y plantas de "
                         "tratamiento."),
    },
}

# ===========================================================================
# CONTAMINANTES QUE EXIGEN MEDICION DEDICADA (analítica, no sensor de planta).
# Se exige MASA > 0: estar en la tabla del DS 90 no significa estar presente.
# ===========================================================================
ALTA_ESPECIFICIDAD = {"cianuro", "sulfuro", "indice fenol", "fenoles", "organoclorados",
                      "pesticidas", "benceno", "tolueno", "hidrocarburos fijos",
                      "hidrocarburos totales", "hidrocarburos volatiles", "mercurio", "cadmio",
                      "arsenico", "cromo total", "cromo hexavalente", "plomo", "niquel",
                      "tetracloroeteno", "triclorometano", "saam", "fluoruro", "boro"}
METALES = {"arsenico", "cadmio", "plomo", "mercurio", "cromo total", "cromo", "niquel",
           "cobre", "zinc", "manganeso", "molibdeno", "aluminio", "hierro disuelto",
           "hierro", "cobalto", "bario", "plata", "estano"}
# Volumen sin toxicidad: NO activan nada por si solos (medido: los cloruros son 1.845.631 t
# del total del pais y son agua de mar).
SIN_TOXICIDAD = {"cloruros", "sulfato", "solidos suspendidos totales", "conductividad",
                 "dbo5", "dqo", "fosforo", "nitrogeno total", "nitrogeno total kjeldahl",
                 "oxigeno disuelto", "ph", "temperatura", "coliformes", "turbiedad", "color",
                 "olor", "detergentes", "aluminio", "hierro disuelto"}

PEL_SIL = {"toxico agudo", "inflamable", "reactivo", "explosivo", "comburente"}
PEL_ALTA = {"toxico agudo", "toxico cronico", "infeccioso", "cancerigeno", "mutageno",
            "teratogeno", "toxico por lixiviacion"}


def reglas(det_agua, n_puntos, peligrosidades, kg_t, rubro):
    """Devuelve [(linea, motivo, es_entrada)]. det_agua = lista con contaminante y masa."""
    out = []
    # SOLO lo que tiene masa declarada > 0
    con_masa = {norm(d["contaminante"]): d["t"] for d in det_agua if (d.get("t") or 0) > 0}
    presentes = set(con_masa)
    metales = sorted(c for c in presentes if c in METALES and c not in SIN_TOXICIDAD)
    especif = sorted(c for c in presentes if c in ALTA_ESPECIFICIDAD)
    masa_toxica = sum(v for k, v in con_masa.items() if k in (METALES | ALTA_ESPECIFICIDAD))
    masa_total = sum(con_masa.values())
    pels = {norm(p) for p in peligrosidades}

    # ---- ANALITICA: la linea de ENTRADA del dolor ambiental.
    #      Se activa con alta especificidad presente (cianuro, cadmio, plomo, fenoles...) o con
    #      un numero relevante de metales. Exige masa > 0: estar en la tabla del DS 90 no basta.
    if especif:
        out.append(("Analítica",
                    f"descarga {len(especif)} parámetros de analítica específica CON masa "
                    f"declarada ({', '.join(especif[:4])}): no se miden con instrumento genérico",
                    True))
    elif len(metales) >= 3:
        out.append(("Analítica",
                    f"descarga {len(metales)} metales pesados "
                    f"({', '.join(metales[:4])}): obligación de medir en línea", True))

    # ---- SOFTWARE Y PLATAFORMA: cuando se descarga en VARIOS PUNTOS.
    #      Medido: solo 96 de 370 tienen 2+ puntos de descarga. Un punto único se cubre con
    #      analítica; cinco puntos con obligaciones distintas ya piden plataforma.
    if n_puntos >= 4:
        out.append(("Software y plataforma",
                    f"descarga en {n_puntos} puntos y declara {len(con_masa)} parámetros: la "
                    f"obligación es múltiple y dispersa, exige plataforma de monitoreo", True))

    # ---- INSTRUMENTACION: la masa es alta, o hay toxicidad disuelta que hay que medir de base.
    #      Umbral tomado de la distribucion: sobre la mediana (0,6 t) no sirve; sobre p75 si.
    if masa_toxica > 50:
        out.append(("Instrumentación",
                    f"{masa_toxica:,.1f} t/año de carga tóxica declarada: el volumen y la "
                    f"variabilidad exigen medir caudal y nivel en continuo", False))

    # ---- SIS: exige contencion REAL. No "inflamable" a secas.
    if (pels & PEL_SIL) and len(pels & PEL_ALTA) >= 3:
        out.append(("SIS",
                    f"maneja {', '.join(sorted(pels & PEL_SIL))} junto a "
                    f"{len(pels & PEL_ALTA)} peligrosidades de alta criticidad: exige contención "
                    f"con SIL", False))

    # ---- VALVULAS: corrosivo/reactivo CON descarga toxica declarada.
    if ("corrosivo" in pels or "reactivo" in pels) and masa_toxica > 20 and len(presentes - SIN_TOXICIDAD) >= 3:
        out.append(("Válvulas",
                    f"maneja corrosivos/reactivos y descarga {masa_toxica:,.1f} t tóxicas: el "
                    f"actuador final contiene el material en dosificación y trasvase", False))

    # ---- DCS: planta de proceso continuo CON señal de proceso real (masa declarada alta).
    r = norm(rubro)
    proceso_real = any(x in r for x in ["quimica", "celulosa", "papel", "produccion de metal",
                                        "mineria", "cemento", "generacion de energia",
                                        "refinacion", "petroleo", "siderurg", "vidrio"])
    if proceso_real and (masa_total > 1000 or kg_t > 10_000):
        out.append(("DCS",
                    f"{rubro}: proceso continuo con {masa_total:,.0f} t/año declaradas en "
                    f"descarga. El DCS es el punto de integración y el camino al resto", False))

    # ---- PLC: rubro de proceso pero señal acotada (sin DCS).
    if proceso_real and masa_total > 0 and masa_total <= 1000 and kg_t <= 10_000:
        out.append(("PLC",
                    f"{rubro}: señales acotadas ({masa_total:,.1f} t/año). Control y seguridad "
                    f"discretos, sin necesitar un DCS completo", False))

    return out


# ===========================================================================
da = json.load(open(os.path.join(D, "dolor_ambiental_empresas.json"), encoding="utf-8"))
EMP = da["empresas"]
PRIORIDAD = {"Analítica": 0, "Software y plataforma": 1, "SIS": 2, "Instrumentación": 3,
             "Válvulas": 4, "DCS": 5, "PLC": 6}

salida = []
for e in EMP:
    pels = [k for k, _ in (e.get("peligrosidades") or [])]
    regs = reglas(e.get("detalle_agua") or [], len(e.get("puntos_descarga") or []) or 1,
                  pels, e.get("respel_t") or 0, e.get("rubro") or "")
    por_linea = collections.defaultdict(list)
    ent = {}
    for lin, mot, is_e in regs:
        por_linea[lin].append(mot)
        ent[lin] = ent.get(lin, False) or is_e
    lineas = [{"linea": l, "productos": LINEAS[l]["productos"][:4],
               "que_resuelve": LINEAS[l]["que_resuelve"], "por_que": por_linea[l],
               "entrada": ent.get(l, False)} for l in LINEAS if l in por_linea]
    lineas.sort(key=lambda x: (not x["entrada"], PRIORIDAD.get(x["linea"], 9)))
    salida.append({
        "empresa": e["empresa"], "rubro": e.get("rubro"), "rut": e.get("rut"),
        "carga_peligrosa_t": e.get("carga_peligrosa_t"),
        "emision_agua_t": e.get("emision_agua_t"), "respel_t": e.get("respel_t"),
        "n_contaminantes": e.get("n_contaminantes"),
        "n_puntos_descarga": len(e.get("puntos_descarga") or []),
        "contaminantes_con_masa": sorted({d["contaminante"] for d in (e.get("detalle_agua") or [])
                                          if (d.get("t") or 0) > 0}),
        "peligrosidades": e.get("peligrosidades"), "lineas": lineas,
        "lineas_entrada": [l["linea"] for l in lineas if l["entrada"]],
        "n_lineas": len(lineas), "contacto": e.get("contacto"), "en_plan": e.get("en_plan"),
    })

print("=" * 84)
print("MATRIZ DOLOR -> LÍNEA DE NEGOCIO (v3: solo señales con masa declarada)")
print("=" * 84)
print(f"  empresas: {len(salida)}")
pl = collections.defaultdict(list)
for s in salida:
    for l in s["lineas"]:
        pl[l["linea"]].append(s)
print(f"\n  === CADA LÍNEA, a cuántas empresas ===")
for lin in sorted(pl, key=lambda x: -len(pl[x])):
    n = len(pl[lin])
    barra = "█" * int(n / len(salida) * 40)
    print(f"     {lin:24s} {n:>4} ({n/len(salida)*100:>3.0f}%) {barra}")
print(f"\n  === LÍNEAS POR EMPRESA ===")
c = collections.Counter(s["n_lineas"] for s in salida)
for k in sorted(c):
    print(f"     {k} líneas: {c[k]:>4} empresas")
print(f"\n  con línea de ENTRADA: {sum(1 for s in salida if s['lineas_entrada'])}/{len(salida)}")
print(f"  con 0 líneas:        {c[0]} (reportan al agua pero sin masa tóxica relevante)")
print(f"\n  === TOP 20 POR CARGA TÓXICA ===")
print(f"  {'EMPRESA':30s} {'tóx t':>8s} {'ENTRADA':22s} expansión")
for s in sorted(salida, key=lambda x: -(x["carga_peligrosa_t"] or 0))[:20]:
    print(f"  {s['empresa'][:30]:30s} {s['carga_peligrosa_t'] or 0:>8,.0f} "
          f"{(' , '.join(s['lineas_entrada']) or '—')[:22]:22s} "
          f"{', '.join(l['linea'] for l in s['lineas'] if not l['entrada'])[:40]}")

json.dump({
    "que_es": ("Matriz DOLOR -> LÍNEA DE NEGOCIO. Cada señal CON MASA DECLARADA en el RETC activa "
               "líneas de negocio de las 7 de CONECTA/SUPCON, con producto y argumento. Distingue "
               "LÍNEA DE ENTRADA (abre la conversación) de LÍNEAS DE EXPANSIÓN."),
    "la_regla": ("La señal activa la línea, no el rubro. El vendedor no dice 'le vendo DCS': dice "
                 "'descarga cadmio y cianuro con masa declarada y hoy no los mide en línea'."),
    "correccion_v3": ("Una señal cuenta SOLO con masa declarada > 0. El DS 90 obliga a reportar "
                      "todos los parámetros de su tabla, así que 'declara cadmio' no significa "
                      "nada si está en cero: la mediana de contaminantes por empresa es 25 y el "
                      "p75 es 29. El conteo de contaminantes es una obligación legal, no una señal "
                      "de dolor. Los umbrales se fijaron sobre la distribución medida."),
    "lineas_disponibles": {k: {"productos": v["productos"], "que_resuelve": v["que_resuelve"]}
                           for k, v in LINEAS.items()},
    "empresas": salida,
}, open(os.path.join(D, "matriz_dolor_linea.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/matriz_dolor_linea.json")
