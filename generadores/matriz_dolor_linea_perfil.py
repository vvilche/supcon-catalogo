#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MATRIZ DOLOR x LÍNEA x PERFIL — no todos compran lo mismo.

POR QUE ESTE CAMBIO (corrección del usuario, medida)
------------------------------------------------------------------------------
Observación de Victor: "ojo que no todos compran lo mismo, un técnico de automatización no
comprará analítica por ejemplo". Tiene razón y es un error de diseño de la versión anterior:
la matriz decía "esta planta necesita analítica + SIS + válvulas" sin decir QUIÉN compra cada
una. Al jefe de I&C no se le vende analítica de proceso: eso lo compra calidad / medio ambiente
/ laboratorio. Si el vendedor llega con el argumento que su interlocutor no puede decidir,
quema la reunión.

Y el dato que lo agrava, medido en el catálogo (1.629 tomadores):
  perfiles que compran instrumentación/I&C/automatización:  336  (20,6%)
  perfiles que compran calidad/medio ambiente/laboratorio:    53  ( 3,3%)
  y de esos 53, casi ninguno es un cargo de medio ambiente real (son gerentes generales de
  empresas que se LLAMAN "Laboratorio X").
=> Hay contactos para las líneas técnicas y casi ninguno para la línea analítica, que es la
   que resuelve el dolor ambiental. Eso hay que decirlo, no taparlo.

TRES DIMENSIONES
------------------------------------------------------------------------------
  1. DOLOR MEDIDO (RETC): contaminante con masa > 0, peligrosidad, volumen.
  2. LÍNEA DE NEGOCIO (las 7 de CONECTA/SUPCON): qué producto lo resuelve.
  3. PERFIL QUE COMPRA: quién decide cada línea, y qué contactos tengo de ese perfil.

LA REGLA DE ASIGNACIÓN
  Una línea llega al contacto SOLO si el perfil del contacto es comprador de esa línea. Si no,
  queda como línea SIN CONTACTO ASIGNADO, con el nombre del perfil que falta. Eso es accionable:
  dice a quién hay que buscar para venderla.
"""
import json, os, collections, unicodedata, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


# ===========================================================================
# PERFIL QUE COMPRA CADA LÍNEA  (el hallazgo de esta corrección)
# ===========================================================================
PERFIL_COMPRADOR = {
    "Analítica": ["calidad", "medio ambiente", "medioambient", "ambiental", "laboratorio",
                  "procesos", "sustentab", "prevencion"],
    "Instrumentación": ["instrument", "control", "automataz", "automatiz", "electric",
                        "mantenim", "mantenc", "planta", "operaciones", "produccion", "iec"],
    "Software y plataforma": ["instrument", "control", "automatiz", "electric", "mantenim",
                              "mantenc", "ti", "informatic", "operaciones", "planta"],
    "DCS": ["instrument", "control", "automatiz", "electric", "mantenim", "mantenc",
            "operaciones", "planta", "produccion"],
    "SIS": ["seguridad", "hse", "ehs", "prevencion", "instrument", "control", "mantenim",
            "mantenc", "operaciones"],
    "Válvulas": ["mantenim", "mantenc", "instrument", "control", "electric", "planta",
                 "operaciones", "mecanic", "produccion"],
    "PLC": ["instrument", "control", "automatiz", "electric", "mantenim", "mantenc", "planta"],
}

# El nombre del perfil que hay que buscar cuando no lo tengo.
PERFIL_FALTA = {
    "Analítica": "Jefe de Medio Ambiente / Calidad / Laboratorio",
    "Instrumentación": "Jefe de Instrumentación y Control (I&C) / Mantenimiento",
    "Software y plataforma": "Jefe de I&C / Automatización / TI industrial",
    "DCS": "Jefe de I&C / Automatización",
    "SIS": "Jefe de Seguridad / HSE / I&C",
    "Válvulas": "Jefe de Mantenimiento (mecánico / eléctrico)",
    "PLC": "Jefe de Automatización / Mantenimiento",
}


# "procesos" es AMBIGUA: en mineria "Control de Procesos" si ve la calidad del efluente, pero
# "Sistemas de Procesos" es control industrial. Medido: el cargo de Codelco "Director de
# Proyectos de Tecnologia & Automatizacion y Sistemas de Procesos Mina" entraba en Analitica por
# esa palabra, y es un falso positivo. Si el cargo menciona automatizacion o sistemas, es el area
# de control, no la de calidad: se excluye.
EXCLUYE_ANALITICA = ["automatiz", "sistema de proceso", "sistemas de proceso", "instrument",
                     "control de proceso", "electrocontrol", "mantenc", "mantenim"]


def perfil_compra(linea, cargo, tipo):
    """El contacto compra esta linea? Se mira cargo Y tipo."""
    txt = norm(f"{cargo or ''} {tipo or ''}")
    kws = PERFIL_COMPRADOR.get(linea, [])
    if not any(k in txt for k in kws):
        return False
    # Desambiguar 'procesos' para Analítica: si entro SOLO por esa palabra y el cargo delata
    # area de control, no es comprador de analítica.
    if linea == "Analítica":
        fuerte = any(k in txt for k in ("calidad", "ambiente", "ambiental", "laborator",
                                        "sustentab", "prevencion"))
        if not fuerte and any(x in txt for x in EXCLUYE_ANALITICA):
            return False
    return True


# ===========================================================================
# REGLAS DE DOLOR (v3: solo señales con masa declarada > 0)
# ===========================================================================
ALTA_ESPECIFICIDAD = {"cianuro", "sulfuro", "indice fenol", "fenoles", "organoclorados",
                      "pesticidas", "benceno", "tolueno", "hidrocarburos fijos",
                      "hidrocarburos totales", "hidrocarburos volatiles", "mercurio", "cadmio",
                      "arsenico", "cromo total", "cromo hexavalente", "plomo", "niquel",
                      "tetracloroeteno", "triclorometano", "saam", "fluoruro", "boro"}
METALES = {"arsenico", "cadmio", "plomo", "mercurio", "cromo total", "cromo", "niquel",
           "cobre", "zinc", "manganeso", "molibdeno", "aluminio", "hierro disuelto",
           "hierro", "cobalto", "bario", "plata", "estano"}
SIN_TOXICIDAD = {"cloruros", "sulfato", "solidos suspendidos totales", "conductividad",
                 "dbo5", "dqo", "fosforo", "nitrogeno total", "nitrogeno total kjeldahl",
                 "oxigeno disuelto", "ph", "temperatura", "coliformes", "turbiedad", "color",
                 "olor", "detergentes", "aluminio", "hierro disuelto"}
PEL_SIL = {"toxico agudo", "inflamable", "reactivo", "explosivo", "comburente"}
PEL_ALTA = {"toxico agudo", "toxico cronico", "infeccioso", "cancerigeno", "mutageno",
            "teratogeno", "toxico por lixiviacion"}

LINEAS = {
    "Analítica": {"productos": ["CEMS 5000", "Analítica en línea (línea Hobre)", "HIFISC",
                                "TISOMIC", "C-QUAND", "NISOSYS-3"],
                  "que_resuelve": ("medición en línea de la composición: metales, tóxicos y "
                                   "parámetros de efluente. Es lo que la SMA exige para demostrar "
                                   "cumplimiento del DS 90 y del DS 43.")},
    "Instrumentación": {"productos": ["SFE910 (caudal electromagnético)",
                                      "SL903 (radar de nivel 80 GHz)", "CXT (presión)",
                                      "W Series (temperatura)", "LUGB (caudal vortex)"],
                        "que_resuelve": ("sensores de caudal, nivel, presión y temperatura. Sin "
                                         "instrumentación no hay dato que reportar.")},
    "Software y plataforma": {"productos": ["SolisSCADA", "InPlant APC", "InPlant RTO",
                                            "InPlant MP3000", "ESP-iSYS", "APEX"],
                              "que_resuelve": ("adquisición, historización y reporte de muchas "
                                               "señales en varios puntos a la vez.")},
    "DCS": {"productos": ["ECS-700", "UCS Nyx", "OMC", "T9100 (CCS)", "SmartEIO y APL"],
            "que_resuelve": ("control distribuido del proceso; punto de integración donde se "
                             "cuelgan analítica e instrumentación.")},
    "SIS": {"productos": ["TCS-900", "TCS-500", "HIPPS"],
            "que_resuelve": "parada de emergencia con SIL para contener el evento."},
    "Válvulas": {"productos": ["Válvulas de control SUPCON FLUID", "Válvulas de bola",
                               "Válvulas mariposa y excéntricas", "CVP2000 (posicionador)"],
                 "que_resuelve": "el actuador final: cierra el lazo que el control decide."},
    "PLC": {"productos": ["G5Pro", "G5Pro Safety (SIL3)", "G3Smart"],
            "que_resuelve": "control y seguridad discretos para islas de proceso."},
}


def reglas(det_agua, n_puntos, peligrosidades, kg_t, rubro):
    out = []
    con_masa = {norm(d["contaminante"]): d["t"] for d in det_agua if (d.get("t") or 0) > 0}
    presentes = set(con_masa)
    metales = sorted(c for c in presentes if c in METALES and c not in SIN_TOXICIDAD)
    especif = sorted(c for c in presentes if c in ALTA_ESPECIFICIDAD)
    masa_toxica = sum(v for k, v in con_masa.items() if k in (METALES | ALTA_ESPECIFICIDAD))
    masa_total = sum(con_masa.values())
    pels = {norm(p) for p in peligrosidades}

    if especif:
        out.append(("Analítica",
                    f"descarga {len(especif)} parámetros de analítica específica con masa "
                    f"declarada ({', '.join(especif[:4])}): no se miden con instrumento genérico",
                    True))
    elif len(metales) >= 3:
        out.append(("Analítica",
                    f"descarga {len(metales)} metales pesados ({', '.join(metales[:4])}): "
                    f"obligación de medir en línea", True))
    if n_puntos >= 4:
        out.append(("Software y plataforma",
                    f"descarga en {n_puntos} puntos y declara {len(con_masa)} parámetros: la "
                    f"obligación es múltiple y dispersa", True))
    if masa_toxica > 50:
        out.append(("Instrumentación",
                    f"{masa_toxica:,.1f} t/año de carga tóxica declarada: el volumen y la "
                    f"variabilidad exigen medir caudal y nivel en continuo", False))
    if (pels & PEL_SIL) and len(pels & PEL_ALTA) >= 3:
        out.append(("SIS",
                    f"maneja {', '.join(sorted(pels & PEL_SIL))} junto a {len(pels & PEL_ALTA)} "
                    f"peligrosidades de alta criticidad: exige contención con SIL", False))
    if ("corrosivo" in pels or "reactivo" in pels) and masa_toxica > 20 and len(presentes - SIN_TOXICIDAD) >= 3:
        out.append(("Válvulas",
                    f"maneja corrosivos/reactivos y descarga {masa_toxica:,.1f} t tóxicas: el "
                    f"actuador final contiene el material", False))
    r = norm(rubro)
    proceso_real = any(x in r for x in ["quimica", "celulosa", "papel", "produccion de metal",
                                        "mineria", "cemento", "generacion de energia",
                                        "refinacion", "petroleo", "siderurg", "vidrio"])
    if proceso_real and (masa_total > 1000 or kg_t > 10_000):
        out.append(("DCS",
                    f"{rubro}: proceso continuo con {masa_total:,.0f} t/año en descarga. El DCS "
                    f"es el punto de integración", False))
    if proceso_real and 0 < masa_total <= 1000 and kg_t <= 10_000:
        out.append(("PLC",
                    f"{rubro}: señales acotadas ({masa_total:,.1f} t/año). Control y seguridad "
                    f"discretos", False))
    return out


# ===========================================================================
# CRUZAR CON TODOS LOS CONTACTOS (técnicos + gerentes, como pidió Victor)
# ===========================================================================
da = json.load(open(os.path.join(D, "dolor_ambiental_empresas.json"), encoding="utf-8"))
plan = json.load(open(os.path.join(D, "plan_contacto.json"), encoding="utf-8"))["plan"]


def nkey(s):
    s = norm(s)
    s = re.sub(r"\b(s a|sa|ltda|limitada|spa|scm|cia|compania|sociedad|empresa|de|del|la|el|los|las|y|chile)\b", " ", s)
    return " ".join(sorted(t for t in re.sub(r"[^a-z0-9 ]", " ", s).split() if len(t) > 2))


plan_idx = {}
for p in plan:
    plan_idx.setdefault(nkey(p["empresa"]), p)

salida = []
sin_contacto_amb = 0
for e in da["empresas"]:
    pels = [k for k, _ in (e.get("peligrosidades") or [])]
    regs = reglas(e.get("detalle_agua") or [], len(e.get("puntos_descarga") or []) or 1,
                  pels, e.get("respel_t") or 0, e.get("rubro") or "")
    por_linea = collections.defaultdict(list)
    ent = {}
    for lin, mot, is_e in regs:
        por_linea[lin].append(mot)
        ent[lin] = ent.get(lin, False) or is_e

    pl = plan_idx.get(nkey(e["empresa"]))
    contactos = pl["tomadores"] if pl else []

    lineas = []
    for l in LINEAS:
        if l not in por_linea:
            continue
        # quien compra esta linea, dentro de los contactos que tengo
        compradores = [c for c in contactos
                       if perfil_compra(l, c.get("cargo"), c.get("tipo"))]
        lineas.append({
            "linea": l, "productos": LINEAS[l]["productos"][:4],
            "que_resuelve": LINEAS[l]["que_resuelve"], "por_que": por_linea[l],
            "entrada": ent.get(l, False),
            "perfil_que_compra": PERFIL_FALTA[l],
            "contactos_que_compran": [
                {"nombre": c["nombre"], "cargo": c.get("cargo"), "rol": c.get("rol_compra"),
                 "linkedin": c.get("linkedin"), "correo": c.get("correo") or ""}
                for c in compradores],
            "n_compradores": len(compradores),
            "tiene_contacto": bool(compradores),
        })
    lineas.sort(key=lambda x: (not x["entrada"], not x["tiene_contacto"],
                               -x["n_compradores"]))

    sin_cto = [l["linea"] for l in lineas if not l["tiene_contacto"]]
    if "Analítica" in [l["linea"] for l in lineas] and not any(
            l["tiene_contacto"] for l in lineas if l["linea"] == "Analítica"):
        sin_contacto_amb += 1

    salida.append({
        "empresa": e["empresa"], "rubro": e.get("rubro"), "rut": e.get("rut"),
        "carga_peligrosa_t": e.get("carga_peligrosa_t"),
        "emision_agua_t": e.get("emision_agua_t"), "respel_t": e.get("respel_t"),
        "n_contaminantes": e.get("n_contaminantes"), "n_puntos_descarga": e.get("n_puntos_descarga"),
        "contaminantes_con_masa": e.get("contaminantes_con_masa"),
        "peligrosidades": e.get("peligrosidades"),
        "lineas": lineas, "n_lineas": len(lineas),
        "lineas_vendibles_hoy": [l["linea"] for l in lineas if l["tiene_contacto"]],
        "lineas_sin_contacto": sin_cto,
        "contactos": [{"nombre": c["nombre"], "cargo": c.get("cargo"),
                       "rol": c.get("rol_compra"), "linkedin": c.get("linkedin"),
                       "correo": c.get("correo") or "", "tipo": c.get("tipo")}
                      for c in contactos],
        "n_contactos": len(contactos), "en_plan": pl is not None,
    })

# ---------------------------------------------------------------------------
print("=" * 86)
print("MATRIZ DOLOR x LÍNEA x PERFIL")
print("=" * 86)
print(f"  empresas: {len(salida)}")

pl_c = collections.defaultdict(lambda: {"empresas": 0, "con_contacto": 0})
for s in salida:
    for l in s["lineas"]:
        pl_c[l["linea"]]["empresas"] += 1
        if l["tiene_contacto"]:
            pl_c[l["linea"]]["con_contacto"] += 1
print(f"\n  === CADA LÍNEA: empresas que la necesitan vs cuántas tienen comprador identificado ===")
print(f"  {'LÍNEA':24s} {'necesitan':>10s} {'con comprador':>14s} {'cobertura':>10s}  PERFIL QUE FALTA")
for lin in sorted(pl_c, key=lambda x: -pl_c[x]["empresas"]):
    v = pl_c[lin]
    cob = v["con_contacto"] / v["empresas"] * 100 if v["empresas"] else 0
    print(f"  {lin:24s} {v['empresas']:>10} {v['con_contacto']:>14} {cob:>9.0f}%  {PERFIL_FALTA[lin][:34]}")

print(f"\n  === LÍNEAS POR EMPRESA ===")
c = collections.Counter(s["n_lineas"] for s in salida)
for k in sorted(c):
    print(f"     {k} líneas: {c[k]:>4}")

vend = sum(1 for s in salida if s["lineas_vendibles_hoy"])
print(f"\n  empresas con AL MENOS UNA línea vendible hoy: {vend}/{len(salida)}")
print(f"  empresas cuya línea de ENTRADA es Analítica y NO tienen contacto que la compre: {sin_contacto_amb}")

print(f"\n  === TOP 15: qué venderle y a quién ===")
for s in sorted(salida, key=lambda x: -(x["carga_peligrosa_t"] or 0))[:15]:
    print(f"\n  {s['empresa'][:50]}  ({s['carga_peligrosa_t'] or 0:,.0f} t tóxicas)")
    for l in s["lineas"]:
        est = f"→ {l['contactos_que_compran'][0]['nombre']} ({str(l['contactos_que_compran'][0]['cargo'])[:26]})" \
              if l["tiene_contacto"] else f"✗ falta {l['perfil_que_compra'][:30]}"
        print(f"     {'★' if l['entrada'] else ' '} {l['linea']:22s} {est}")

json.dump({
    "que_es": ("Matriz DOLOR x LÍNEA x PERFIL. Por cada empresa: qué necesita (medido en el RETC), "
               "qué producto lo resuelve, y QUIÉN de esa empresa lo compra. Marca la línea de "
               "entrada y avisa cuando no hay contacto del perfil comprador."),
    "la_regla": ("Una línea se le asigna a un contacto SOLO si su perfil es comprador de esa "
                 "línea. Al jefe de I&C no se le vende analítica de proceso: eso lo compra "
                 "calidad/medio ambiente. Si el vendedor llega con el argumento que el "
                 "interlocutor no puede decidir, quema la reunión."),
    "hallazgo_de_contactos": ("Medido en el catálogo (1.629 tomadores): 336 perfiles compran "
                              "instrumentación/I&C/automatización (20,6%) pero solo 53 compran "
                              "calidad/medio ambiente/laboratorio (3,3%), y de esos casi ninguno "
                              "es un cargo de medio ambiente real. Hay contactos para las líneas "
                              "técnicas y casi ninguno para la línea analítica, que es la que "
                              "resuelve el dolor ambiental."),
    "perfil_que_compra": PERFIL_FALTA,
    "empresas": salida,
}, open(os.path.join(D, "matriz_dolor_linea_perfil.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/matriz_dolor_linea_perfil.json")
