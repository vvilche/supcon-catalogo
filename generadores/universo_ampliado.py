#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UNIVERSO AMPLIADO: el padrón RETC completo, no el subconjunto de 3.157.

POR QUÉ. El catálogo de 3.157 empresas es un subconjunto filtrado, no el padrón. Las fuentes
reales tienen mucho más:
  Ventanilla única (padrón RETC)      11.840 empresas distintas / 26.649 establecimientos
  Residuos peligrosos 2025             5.327 empresas distintas
  RILES 2024                             370 empresas distintas
  catálogo heredado                    3.157  <- lo que se estaba usando

Faltaban ~8.700 empresas del padrón. Este módulo construye el universo desde las FUENTES, no
desde el catálogo heredado.

QUÉ ENTRA Y QUÉ NO. El padrón incluye rubros que no son clientes de automatización de proceso:
comercio (3.258), municipios (283), bancos y "otras actividades" (8.701). Se incluyen solo los
rubros industriales de proceso continuo, y el resto se cuenta y se declara (no se borra en
silencio).

Salida: datos/universo_ampliado.json
"""
import os, json, collections, re, unicodedata
import openpyxl

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
RETC = os.path.join(D, "retc")

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s).strip()

def norm_rut(r):
    """Normaliza RUT quitando el .0 espurio del RETC (viene de float: '61704000.0-K')."""
    s = str(r or "").strip().upper()
    s = re.sub(r"\.0(?=-|$)", "", s)
    s = s.replace(".", "").replace("-", "").replace(" ", "")
    return re.sub(r"[^0-9K]", "", s)

# ---------- rubros que SÍ son clientes de SUPCON (proceso continuo industrial) ----------
RUBRO_PROCESO = {
 "Industria manufacturera", "Industria agropecuaria y silvicultura", "Producción de alimentos",
 "Gestor de residuos", "Combustibles", "Pesca", "Extracción de minerales",
 "Generación de energía", "Producción química", "Industria del papel y celulosa",
 "Producción de metal", "Suministro y tratamiento de aguas",
 "Transmision y distribucion de energía eléctrica",
}
# rubros que NO (se cuentan y se declaran)
RUBRO_EXCLUIDO = {
 "Otras actividades", "0", "Comercio", "Construcción e inmobiliarias", "Transporte",
 "Municipio", "Servicios", "Educación", "Salud", "Turismo", "Telecomunicaciones",
 "Financiero", "Minero no metálico",
}
# organizaciones que NO son clientes de automatizacion de proceso aunque caigan en un rubro
# industrial del padron (una municipalidad con planta de agua sigue siendo un municipio)
EXCLUIR_POR_NOMBRE = ["MUNICIPALIDAD", "I MUNICIPAL", "ILUSTRE MUNICIP", "SERVICIO DE SALUD",
 "HOSPITAL", "CLINICA", "MUTUAL DE SEGURIDAD", "ASOC CHILENA DE SEGURIDAD", "MINISTERIO DE",
 "FUNDACION", "UNIVERSIDAD", "COLEGIO", "JUNTA DE VECINOS", "LATAM AIRLINES", "ENTEL",
 "TELEFONICA", "CENCOSUD", "WALMART", "SALFA", "CASA MATRIZ"]

LINEAS_POR_RUBRO = {
 "Producción química": ["SIS","DCS","Instrumentación","Software y plataforma"],
 "Industria del papel y celulosa": ["DCS","Instrumentación","Válvulas","Software y plataforma"],
 "Extracción de minerales": ["DCS","Instrumentación","SIS","Válvulas"],
 "Producción de metal": ["DCS","Instrumentación","SIS"],
 "Generación de energía": ["DCS","Analítica","Instrumentación","Software y plataforma"],
 "Transmision y distribucion de energía eléctrica": ["DCS","Software y plataforma","Instrumentación"],
 "Suministro y tratamiento de aguas": ["Instrumentación","Analítica","Software y plataforma"],
 "Combustibles": ["SIS","Instrumentación","DCS"],
 "Gestor de residuos": ["Instrumentación","Software y plataforma"],
 "Producción de alimentos": ["Instrumentación","DCS","Válvulas","Software y plataforma"],
 "Industria manufacturera": ["Instrumentación","DCS","Válvulas"],
 "Pesca": ["Instrumentación","DCS"],
 "Industria agropecuaria y silvicultura": ["Instrumentación","Software y plataforma"],
}

ZONA_REGION = {
 "Z1": ["metropolitana","santiago"], "Z2": ["antofagasta","tarapaca"],
 "Z3": ["valparaiso"], "Z4": ["biobio","araucania","nuble"],
 "Z5": ["los lagos","aysen","magallanes"], "Z6": ["coquimbo","atacama"],
 "Z7": ["maule","o'higgins","ohiggins","libertador"],
}
def zona_de(region, comuna):
    t = norm(f"{region} {comuna}")
    for z, regs in ZONA_REGION.items():
        if any(r in t for r in regs): return z
    return None

# ---------- 0. el catalogo heredado como fuente de RUBRO ----------
# 3.157 empresas con rubro ya asignado. Sirve para completar el rubro de las que el padron
# trae vacio, antes de rendirse a "sin clasificar".
import glob
RUBRO_CATALOGO = {}
CATALOGO_DIR = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"
for f in glob.glob(os.path.join(CATALOGO_DIR, "catalogo-*/research/*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    if d.get("empresa") and d.get("rubro"):
        RUBRO_CATALOGO[str(d["empresa"]).upper().strip()] = d["rubro"]
print(f"catálogo heredado (fuente de rubro): {len(RUBRO_CATALOGO):,} empresas\n")

# ---------- 1. cargar el padrón RETC ----------
print("=== 1. padrón RETC (ventanilla única) ===")
wb = openpyxl.load_workbook(os.path.join(RETC,"ventanilla.xlsx"), read_only=True, data_only=True)
ws = wb["Hoja1"]; it = ws.iter_rows(values_only=True); head = list(next(it))
H = {c: i for i, c in enumerate(head)}
padron = {}
for row in it:
    if not row or H["Razón social"] >= len(row): continue
    razon = str(row[H["Razón social"]] or "").strip()
    if not razon: continue
    rubro = str(row[H["Rubro RETC"]] or "").strip()
    reg = str(row[H["Región"]] or "").strip()
    com = str(row[H["Comuna"]] or "").strip()
    # Deduplicar por (RAZON SOCIAL, COMUNA): la misma empresa en la misma comuna no se repite,
    # pero sus plantas en comunas distintas SI son oportunidades distintas (Codelco opera en
    # Calama, Rancagua, Los Andes, Machalí...). Deduplicar solo por razón social colapsaba 4.812
    # empresas a 3.887 y perdía la geografía, que es justamente lo que usa la estrategia.
    clave = (razon.upper(), com.upper())
    prev = padron.get(clave)
    if prev is not None:
        prev_rubro_valido = prev["rubro"] not in ("0", "", "None")
        este_valido = rubro not in ("0", "", "None")
        if prev_rubro_valido or not este_valido:
            continue   # ya tenemos uno mejor (o este no aporta)
    padron[clave] = {
      "empresa": razon, "rubro": rubro, "region": reg, "comuna": com,
      "lat": row[H["Latitude"]] if H["Latitude"] < len(row) else None,
      "lon": row[H["Longitude"]] if H["Longitude"] < len(row) else None,
      "id_vu": row[H["ID Ventanilla única"]] if H["ID Ventanilla única"] < len(row) else None,
      "establecimiento": str(row[H["Nombre de Establecimiento"]] or ""),
      "zona": zona_de(reg, com),
    }
wb.close()
print(f"  empresas distintas en el padrón: {len(padron):,}")

# ---------- 2. cruzar señales ----------
print("\n=== 2. señales del RETC ===")
# residuos peligrosos (kg -> t) e RILES
def leer(f, hoja):
    wb = openpyxl.load_workbook(os.path.join(RETC,f), read_only=True, data_only=True)
    ws = wb[hoja]; it = ws.iter_rows(values_only=True); head = [str(c or "") for c in next(it)]
    filas = [dict(zip(head, r)) for r in it if r and any(c is not None for c in r)]
    wb.close(); return filas

resp = leer("respeligrosos_2025.xlsx","Generador")
riles = leer("riles_2024.xlsx","Datos")
print(f"  residuos peligrosos: {len(resp):,} filas | RILES: {len(riles):,} filas")

res_por_nom, res_tipos = collections.defaultdict(float), collections.defaultdict(set)
# el archivo de residuos trae 'rubro' granular por empresa: es la MEJOR fuente de rubro
RUBRO_RESPEL = {
 "Pesca y acuicultura": "Pesca",
 "Otras industrias manufactureras": "Industria manufacturera",
 "Industria química, de plástico y caucho": "Producción química",
 "Minería": "Extracción de minerales",
 "Industria de la madera y silvicultura": "Industria agropecuaria y silvicultura",
 "Otras centrales de generación eléctrica": "Generación de energía",
 "Termoeléctricas": "Generación de energía",
 "Captación, tratamiento y distribución de agua": "Suministro y tratamiento de aguas",
 "Plantas de tratamiento de aguas servidas": "Suministro y tratamiento de aguas",
 "Gestores de residuos": "Gestor de residuos",
 "Industria del papel y celulosa": "Industria del papel y celulosa",
 "Producción cemento, cal y yeso": "Industria manufacturera",
 "Producción agropecuaria": "Industria agropecuaria y silvicultura",
 "Elaboración de alimentos y bebidas": "Producción de alimentos",
 "Fabricación de metales": "Producción de metal",
 "Coquización y refinación de petróleo": "Combustibles",
}
rubro_por_nom = {}
for r in resp:
    try: v = float(str(r.get("cantidad_transferencia") or 0).replace(",",""))
    except: v = 0.0
    if v <= 0: continue
    u = str(r.get("unidad_abreviacion") or "kg").strip().lower()
    if u.startswith("kg"): v /= 1000.0        # el RETC publica en kg
    k = str(r.get("razon_social") or "").upper().strip()
    if not k: continue
    res_por_nom[k] += v
    if r.get("tipo_respel"): res_tipos[k].add(str(r["tipo_respel"])[:30])
    rr = str(r.get("rubro") or "").strip()
    for clave, destino in RUBRO_RESPEL.items():
        if clave.lower() in rr.lower():
            rubro_por_nom[k] = destino
            break

ril_por_nom, ril_cont = collections.defaultdict(float), collections.defaultdict(set)
for r in riles:
    try: v = float(str(r.get("emision_total") or 0).replace(",",""))
    except: v = 0.0
    if v <= 0: continue
    k = str(r.get("razon_social") or "").upper().strip()
    if not k: continue
    ril_por_nom[k] += v
    if r.get("contaminante"): ril_cont[k].add(str(r["contaminante"]))

# ---------- 3. construir el universo ----------
print("\n=== 3. construir ===")
emps = []
excluidos = collections.Counter()
# Clasificador por nombre, para los establecimientos con el rubro vacio. Medido: 4.910 filas
# del padron no traen rubro, y entre ellas hay plantas industriales reales (Marine Harvest,
# Cermaq, Camanchaca, rellenos sanitarios, plantas de agua). Descartarlas por el campo vacio
# dejaba fuera demanda real.
CLAVES_NOMBRE = {
 "Pesca": ["salmon","pesquer","acuicultur","cermaq","marine harvest","camanchaca","piscicol",
           "cultivo","centro de mar","ventisqueros","austral","pacific star","pesca"],
 "Gestor de residuos": ["relleno","vertedero","reciclaj","reciclad","triciclos","tratamiento de residuo",
           "disposicion final","revaloriz","compostaj"],
 "Suministro y tratamiento de aguas": ["agua","sanitari","elevadora","ptas","alcantarillad","essbio",
           "aguas andinas","esval","nuevosur","aguas del valle","tratamiento de agua"],
 "Combustibles": ["combustible","copec","shell","petrobras","enex","estacion de servicio","gas ",
           "gnl","combustion","petroleo"],
 "Producción de alimentos": ["aliment","frigorific","agroindus","molino","panificad","lacteos",
           "cecinas","conserva"],
 "Extracción de minerales": ["miner","faena","codelco","collahuasi","escondida","los pelambres"],
 "Generación de energía": ["generad","central hidro","eolic","solar","engie","colbun","aes ",
           "enel","hidroelectric","termoelectr"],
 "Industria manufacturera": ["manufactur","plastico","metalmecan","fabric","maderer","aserrader",
           "cement","acero","papel","celulos","textil","quimic","vidrio","ceramic"],
 "Producción química": ["quimic","oxiquim","basf","enaex"],
}
def clasificar_por_nombre(razon, establecimiento):
    t = norm(f"{razon} {establecimiento}")
    for k, cs in CLAVES_NOMBRE.items():
        if any(c in t for c in cs): return k
    return None

for (razon_u, _com), p in padron.items():
    rubro = p["rubro"]
    # descartar organizaciones que no son clientes aunque el rubro sea industrial
    if any(x in razon_u for x in EXCLUIR_POR_NOMBRE):
        excluidos["(no cliente: institución) " + razon_u[:28]] += 1
        continue
    res = res_por_nom.get(razon_u, 0.0)
    ril = ril_por_nom.get(razon_u, 0.0)
    # el rubro vacio o "0" se completa por nombre; si no se puede, se decide por la senal de dolor
    rubro_efectivo = rubro
    origen_rubro = "padron"
    if rubro in ("0", "", "None") or rubro in RUBRO_EXCLUIDO:
        est = str(p.get("establecimiento") or "")
        alt = clasificar_por_nombre(razon_u, est)
        if alt:
            rubro_efectivo = alt; origen_rubro = "inferido_del_nombre"
        elif rubro_por_nom.get(razon_u):
            rubro_efectivo = rubro_por_nom[razon_u]
            origen_rubro = "residuos_peligrosos"
        elif RUBRO_CATALOGO.get(razon_u):
            # el catalogo heredado SI tiene el rubro de estas: usarlo antes de rendirse
            rubro_efectivo = RUBRO_CATALOGO[razon_u]
            origen_rubro = "catalogo_heredado"
        else:
            # NO se puede determinar el rubro -> queda FUERA.
            # Antes entraba cualquier empresa con senal de dolor, y el resultado se lleno de
            # mutuales, hospitales, aerolineas, telecomunicaciones y automotoras: generan
            # residuos peligrosos pero no tienen proceso continuo que automatizar. Aportaban
            # 21.592 de dolor (37% del total) y habrian inflado todas las zonas.
            excluidos[(rubro or "(vacío)") + " [no determinable]"] += 1
            continue
    p["rubro_original"] = rubro
    p["origen_rubro"] = origen_rubro
    rubro = rubro_efectivo
    dolor = 0.0
    señales = []
    if ril > 0:
        dolor += min(ril/50 + 8, 40); señales.append(f"RILES al agua {ril:,.0f}")
    if res > 0:
        dolor += min(res/20 + 5, 40); señales.append(f"residuos peligrosos {res:,.0f} t")
    if len(ril_cont.get(razon_u, ())) > 3:
        dolor += 10; señales.append(f"{len(ril_cont[razon_u])} contaminantes")
    emps.append({
      "empresa": p["empresa"], "rubro": rubro, "rubro_original": p.get("rubro_original"),
      "origen_rubro": p.get("origen_rubro"), "region": p["region"], "comuna": p["comuna"],
      "zona": p["zona"], "lat": p["lat"], "lon": p["lon"], "id_vu": p["id_vu"],
      "residuos_t": round(res,2), "riles": round(ril,2),
      "residuos_tipos": len(res_tipos.get(razon_u, ())),
      "riles_contaminantes": sorted(ril_cont.get(razon_u, ())),
      "dolor": round(min(dolor,100),1), "senales_dolor": señales,
      "lineas_supcon": LINEAS_POR_RUBRO.get(rubro, []),
      "fuente": "RETC MMA — padrón ventanilla única + residuos peligrosos 2025 + RILES 2024",
    })

con = [e for e in emps if e["dolor"] > 0]
print(f"  empresas de proceso continuo:  {len(emps):,}")
print(f"  con dolor verificado:          {len(con):,}")
print(f"  excluidas por rubro (no cliente): {sum(excluidos.values()):,}")
print(f"\n  top rubros excluidos:")
for k,v in excluidos.most_common(6): print(f"    {k[:40]:42s} {v:>6,}")

rz = collections.Counter(e["rubro"] for e in emps)
print(f"\n  === rubros incluidos ({len(rz)}) ===")
for k,v in rz.most_common(): print(f"    {k[:46]:48s} {v:>6,}")

zz = collections.Counter(e["zona"] or "sin zona" for e in emps)
print(f"\n  === por zona ===")
for k in ["Z1","Z2","Z3","Z4","Z5","Z6","Z7","sin zona"]:
    if k in zz: print(f"    {k:9s} {zz[k]:>6,}")

json.dump({
 "metodo": ("Universo construido desde las FUENTES, no desde el catálogo heredado. Padrón RETC "
   "(ventanilla única) filtrado a rubros de proceso continuo industrial, cruzado con residuos "
   "peligrosos 2025 y RILES 2024 por razón social. Los rubros no industriales se cuentan y se "
   "declaran, no se borran en silencio."),
 "fuentes": {
   "padron": "datos/retc/ventanilla.xlsx (RETC/MMA, ventanilla única)",
   "residuos": "datos/retc/respeligrosos_2025.xlsx (kg -> t)",
   "riles": "datos/retc/riles_2024.xlsx (emision_total)",
 },
 "comparacion": {
   "catalogo_heredado": 3157,
   "padron_retc_completo": len(padron),
   "universo_ampliado": len(emps),
   "excluidos_no_industriales": sum(excluidos.values()),
 },
 "resumen": {"empresas": len(emps), "con_dolor": len(con),
   "por_rubro": dict(rz), "por_zona": dict(zz),
   "excluidos_por_rubro": dict(excluidos)},
 "lineas_por_rubro": LINEAS_POR_RUBRO,
 "empresas": sorted(emps, key=lambda e: -e["dolor"]),
}, open(os.path.join(D,"universo_ampliado.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/universo_ampliado.json")
