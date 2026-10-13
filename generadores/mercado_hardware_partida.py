#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MERCADO DE HARDWARE POR PARTIDA ARANCELARIA — el método correcto.

CORRECCIÓN DE MÉTODO (la tercera y definitiva):
  v1 filtraba por palabras clave        -> contaminación grave
  v2 filtraba por partida sola          -> ruido de otros rubros
  v3 filtraba por partida + marca       -> SUBESTIMA el mercado (el campo DMARCA viene con
                                            siglas y truncamientos el 38% de las veces, así que
                                            exigir marca conocida deja fuera valor real)

EL MÉTODO CORRECTO: medir el mercado con LA PARTIDA (dato duro, siempre correcto) y aplicar
solo DOS ajustes verificables:
  1. Excluir ítems cuya GLOSA declare otro rubro (parte de vehículo, accesorio, etc.)
  2. Restar el valor de marcas de OTRO rubro verificable (Caterpillar, Cummins, Komatsu en
     válvulas son repuestos de automoción, no válvulas de proceso).
NO se exige marca del rubro: esa exigencia es la que producía la subestimación.

La marca se reporta APARTE, solo como indicador de competencia identificable.

Salida: datos/mercado_hardware_partida.json
"""
import glob, os, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

# ============================================================================
# LÍNEAS DE HARDWARE: PARTIDAS (dato duro) + ruido verificable a restar
# ============================================================================
LINEAS = {
 "Instrumentación": {
   "partidas": {
     "90262010":"Transmisores de presión (manométricos)","90262019":"Transmisores de presión (otros)",
     "90262090":"Instrumentos de presión (otros)","90269000":"Partes de instrumentos de presión",
     "90251100":"Termómetros de líquido (lectura directa)","90251900":"Termómetros y pirómetros (otros)",
     "90258010":"Termómetros y higrómetros electrónicos","90258090":"Los demás instrumentos de temperatura",
     "90259000":"Partes de instrumentos de temperatura",
     "90261010":"Medidores de caudal (caudalímetros)","90261090":"Instrumentos de caudal (otros)",
     "90268010":"Instrumentos de nivel","90268090":"Instrumentos de medida de fluidos (otros)",
     "90303100":"Multímetros","90303200":"Multímetros con registro","90303300":"Instrumentos de tensión/corriente",
     "90303900":"Instrumentos de medida eléctrica (otros)","90304000":"Instrumentos de radiofrecuencia",
     "90308900":"Instrumentos de medida eléctrica sin registro",
   },
   "ruido_marcas": ["CATERPILLAR","KOMATSU","CUMMINS","DOOSAN","DEUTZ","SCANIA","VOLVO","MERCEDES",
     "FORD","TOYOTA","NISSAN","JOHN DEERE","PERKINS","YANMAR","CNH","COPRECI","BOSCH","DENSO",
     "MAHLE","ROCHE","ABBOTT","MINIMED","BECKMAN","SYSMEX"],
   "ruido_glosa": ["VEHICULO","AUTOMOVIL","MOTOR","CAMION","TRACTOR","REFRIGERADOR","LAVADORA"],
 },
 "Analítica": {
   "partidas": {
     "90271010":"Analizadores de gases (electrónicos)","90271090":"Analizadores de gases (otros)",
     "90272000":"Cromatógrafos y aparatos de electroforesis","90273000":"Espectrómetros y espectrofotómetros",
     "90275000":"Instrumentos con radiación óptica","90278100":"Espectrómetros de masas",
     "90278999":"Los demás instrumentos de análisis físico/químico","90279090":"Micrótomos y partes",
   },
   "ruido_marcas": ["ROCHE","ABBOTT","MEDTRONIC","MINIMED","BECKMAN","SYSMEX","BIOMERIEUX",
     "VITROS","MINDRAY","STAGO","BIOFIRE","SIEMENS HEALTHINEERS","CATERPILLAR","KOMATSU","DELL",
     "LENOVO","HP","APPLE","SAMSUNG"],
   "ruido_glosa": ["DIAGNOSTICO","IN VITRO","REACTIVO","MEDICAMENTO","LABORATORIO CLINICO"],
 },
 "Válvulas": {
   "partidas": {
     "84811000":"Válvulas reductoras de presión","84812010":"Válvulas para transmisión oleohidráulica",
     "84812020":"Válvulas para transmisión neumática","84813000":"Válvulas de retención (check)",
     "84814000":"Válvulas de seguridad o alivio","84818010":"Válvulas de bola",
     "84818090":"Los demás artículos de grifería","84819000":"Partes de válvulas",
   },
   "ruido_marcas": ["CATERPILLAR","CUMMINS","DOOSAN","KOMATSU","DEUTZ","SCANIA","COPRECI","SENSI",
     "WASSER","M.-F","M-F","EPCM","BOSCH","DENSO","VOLVO","TOYOTA","NISSAN","FORD","JOHN DEERE"],
   "ruido_glosa": ["VEHICULO","AUTOMOVIL","MOTOR","CAMION","TRACTOR","LAVADORA","REFRIGERADOR",
     "GRIFERIA DOMESTICA","SANITARIO"],
 },
 "DCS y control": {
   "partidas": {
     "85371000":"Tableros y paneles de control (hasta 1000 V)","85371010":"Tableros de control numérico",
     "85371090":"Soportes con aparatos eléctricos de control","85372000":"Tableros de control (más de 1000 V)",
     "85372010":"Tableros de distribución de alta tensión","85372090":"Tableros eléctricos (otros)",
     "85381000":"Partes de tableros y paneles","85389000":"Partes de aparatos eléctricos de conexión",
   },
   "ruido_marcas": ["CATERPILLAR","KOMATSU","CUMMINS","DOOSAN","DEUTZ","SCANIA","VOLVO","MERCEDES",
     "FORD","TOYOTA","NISSAN","COPRECI","BOSCH","DENSO","DELL","LENOVO","HP","APPLE","SAMSUNG",
     "XIAOMI","LG","WHIRLPOOL","HAIER","MIDEA","CISCO","MOTOROLA","SPACEX","HUAWEI","ZTE","NOKIA",
     "ERICSSON","UBIQUITI","ARISTA","FORTINET","GOOGLE","INETICS"],
   "ruido_glosa": ["VEHICULO","AUTOMOVIL","MOTOR","CAMION","TRACTOR","TELEFONO","CELULAR"],
 },
 "SIS (seguridad)": {
   "partidas": {
     "85371000":"Tableros y paneles de control","85371010":"Tableros de control numérico",
     "85371090":"Soportes con aparatos de control","85389000":"Partes de aparatos eléctricos",
   },
   "ruido_marcas": ["CATERPILLAR","KOMATSU","CUMMINS","DOOSAN","DELL","LENOVO","HP","APPLE",
     "SAMSUNG","CISCO","MOTOROLA","HUAWEI","GOOGLE","COPRECI","BOSCH","INETICS","SANDVIK"],
   "ruido_glosa": ["VEHICULO","AUTOMOVIL","MOTOR","CAMION","TELEFONO"],
 },
}

def marca_ruido(marca, lista):
    m = (marca or "").upper().replace("-F","").split("~")[0].strip()
    return any(x in m for x in lista)

def glosa_ruido(nombre, lista):
    n = (nombre or "").upper()
    return any(x in n for x in lista)

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}\n")

P2L = collections.defaultdict(list)
for lin, cfg in LINEAS.items():
    for p in cfg["partidas"]: P2L[p].append(lin)

bruto = collections.defaultdict(float)      # valor de la partida, sin ajustes
ruido = collections.defaultdict(float)      # lo que se resta
limpio = collections.defaultdict(float)     # mercado estimado
items = collections.defaultdict(int)
por_partida = collections.defaultdict(lambda: collections.Counter())
marcas = collections.defaultdict(collections.Counter)
paises = collections.defaultdict(collections.Counter)
importadores = collections.defaultdict(set)

for txt in archivos:
    with open(txt, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= 158: continue
            p8 = (c[157] or "").strip()[:8]
            lins = P2L.get(p8)
            if not lins: continue
            cif = num(c[158])
            if cif <= 0: continue
            for lin in lins:
                cfg = LINEAS[lin]
                bruto[lin] += cif
                items[lin] += 1
                por_partida[lin][cfg["partidas"][p8]] += cif
                if marca_ruido(c[134], cfg["ruido_marcas"]) or glosa_ruido(c[133], cfg["ruido_glosa"]):
                    ruido[lin] += cif
                else:
                    limpio[lin] += cif
                    marcas[lin][(c[134] or "").upper().replace("-F","").split("~")[0].strip()[:30]] += cif
                    paises[lin][(c[21] or "").strip()] += cif
                    k = (c[6] or "").strip()
                    if k: importadores[lin].add(k)

PAIS = {"336":"Alemania","563":"China","505":"EE.UU.","549":"India","508":"Japón","512":"Italia",
 "225":"Francia","317":"Corea del Sur","220":"España","226":"Reino Unido","528":"Países Bajos",
 "511":"Canadá","510":"Taiwán","331":"Brasil","504":"EE.UU.","517":"Singapur","507":"Japón",
 "216":"Noruega","412":"México","204":"Argentina","484":"Suecia","223":"Finlandia"}

print(f"{'LÍNEA':18s} {'PARTIDA (bruto)':>16s} {'ruido restado':>14s} {'MERCADO':>12s} {'% ruido':>8s} {'importadores':>13s}")
print("-"*90)
sal = {}
for lin in LINEAS:
    b, r, l = bruto[lin], ruido[lin], limpio[lin]
    pct = r/b*100 if b else 0
    print(f"{lin:18s} US${b/1e6:>13,.1f}M US${r/1e6:>11,.1f}M US${l/1e6:>9,.1f}M {pct:>7.0f}% {len(importadores[lin]):>13,}")
    sal[lin] = {"partida_bruto_usd":round(b,2),"ruido_restado_usd":round(r,2),
      "mercado_usd":round(l,2),"pct_ruido":round(pct,1),
      "items":items[lin],"n_importadores":len(importadores[lin]),
      "por_partida":[[k,round(v,2)] for k,v in por_partida[lin].most_common()],
      "top_marcas":[[k,round(v,2)] for k,v in marcas[lin].most_common(20)],
      "top_paises":[[PAIS.get(k,"cód. "+k),round(v,2)] for k,v in paises[lin].most_common(8)]}

total = sum(v["mercado_usd"] for v in sal.values())
print(f"\nTOTAL hardware: US${total/1e6:,.1f}M")

json.dump({"metodo":"Partida arancelaria como medida del mercado (dato duro) menos el ruido de otros rubros verificable por marca y glosa. NO se exige marca del rubro: esa exigencia era la que subestimaba.",
  "fuente":"Registro DIN Aduanas Chile 2025 (4.847.036 líneas)",
  "por_que_este_metodo":("El campo DMARCA trae siglas y truncamientos el 38% de las veces "
    "(N.S.I.C., E.R.D., S + HAUSER), así que filtrar por marca conocida deja fuera valor real. "
    "La partida arancelaria, en cambio, siempre está y siempre es correcta."),
  "lineas":sal,"total_hardware_usd":round(total,2)},
  open(os.path.join(D,"mercado_hardware_partida.json"),"w"), ensure_ascii=False, indent=1)
print(f"guardado: datos/mercado_hardware_partida.json")
