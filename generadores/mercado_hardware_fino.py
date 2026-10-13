#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MERCADO DE HARDWARE, MEDIDO FINO — línea por línea, con lista de marcas curada a mano.

Por qué existe: el estudio general filtró por marca para limpiar ruido, y eso sirve para medir
COMPETENCIA pero destruye la medición de TAMAÑO. El factor de subestimación va de 2,7x a 36x
según la línea. No se puede arreglar con listas automáticas: en el dominio hay 27.718 marcas
distintas y las mayores no son del rubro (Cisco US$57,3M, Google US$54,7M en partidas de redes
y computación).

MÉTODO (el que funcionó en válvulas): para las partidas de cada línea, clasificar cada ítem en
cuatro categorías con LISTA CURADA A MANO:
  (a) marca del rubro      -> competencia identificable
  (b) sin marca declarada  -> mercado real, fabricante no declarado
  (c) ruido de otro rubro  -> se RESTA (automoción, consumo, telecom, médico)
  (d) dudoso               -> se reporta aparte, no se suma

Mercado de la línea = (a) + (b).  El (d) se publica como rango superior.

Cubre las 5 líneas de HARDWARE (excluye software y plataforma, que no entra por partida).
Salida: datos/mercado_hardware_fino.json
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
# LÍNEAS DE HARDWARE, con las marcas curadas a mano
# ============================================================================
LINEAS = {
 "Instrumentación": {
   "partidas": ["90262010","90262019","90262090","90269000",   # presión
                "90251100","90251900","90258010","90258090","90259000",  # temperatura
                "90261010","90261090","90268010","90268090",   # caudal y nivel
                "90303100","90303200","90303300","90303900","90304000","90308900"],  # calibración
   "rubro": ["ENDRESS","KROHNE","MICRO MOTION","FLEXIM","ROSEMOUNT","YOKOGAWA","WIKA","ASHCROFT",
     "MAGNETROL","VEGA","SIEMENS","ABB","EMERSON","DANFOSS","SAMSON","METSO","VALMET","AZBIL",
     "FUJI","MITSUBISHI","OMRON","KEYENCE","SICK","BALLUFF","BAUMER","IFM","TURCK","PEPPERL",
     "MTS","AMETEK","WIKA","TESTO","DRAGER","FLUKE","OMICRON","MEGGER","ADDITEL","BEAMEX",
     "AMPROBE","EXTEK","PCE","DWYER","ASHCROFT","ENDRESS & HAUSER","BARKSDALE"],
   "ruido": ["CATERPILLAR","KOMATSU","CUMMINS","DOOSAN","DEUTZ","SCANIA","VOLVO","MERCEDES","FORD",
     "TOYOTA","NISSAN","JOHN DEERE","PERKINS","YANMAR","CNH","COPRECI","BOSCH","DENSO","MAHLE",
     "SENSI","SAMSUNG","LG","WHIRLPOOL","ELECTROLUX","HAIER","MIDEA","ROCHE","ABBOTT","MINIMED"],
 },
 "Analítica": {
   "partidas": ["90271010","90271090","90272000","90273000","90275000","90278100","90278999","90279090"],
   "rubro": ["ENDRESS","THERMO","AGILENT","SHIMADZU","BRUKER","HACH","WTW","SERVOMEX","MSA",
     "SIEMENS","ABB","YOKOGAWA","EMERSON","METSO","CIDRA","MALVERN","PERKIN","LECO","WATERS",
     "ANALYTIK","BUCHI","KNAUER","TELEDYNE","XIONGFA","FOCUSED","PHOTON","AMETEK","BARTEC",
     "NOVATECH","COSA XENTAUR","ENERAC","TESTO","MIRIS","ANTON PAAR"],
   "ruido": ["ROCHE","ABBOTT","MEDTRONIC","MINIMED","BECKMAN","SYSMEX","BIOMERIEUX","SIEMENS HEALTHINEERS",
     "CATERPILLAR","KOMATSU","CUMMINS","DELL","LENOVO","HP","APPLE","SAMSUNG"],
 },
 "Válvulas": {
   "partidas": ["84811000","84812010","84812020","84813000","84814000","84818010","84818090","84819000"],
   "rubro": ["BRAY","VALMET","VALVITALIA","DANFOSS","METSO","EMERSON","FISHER","SAMSON","NELES",
     "VELAN","CIRCOR","KITZ","CAMERON","BERMAD","PETROL","HABONIM","TYCO","PENTAIR","KEYSTONE",
     "CRANE","KSB","INTERAPP","GEMU","BURKERT","ASCO","AVK","HAWLE","CLA-VAL","FLOWSERVE",
     "GENEBRE","ROTORK","AUMA","LIMITORQUE","SMC","FESTO","PARKER","DEZURIK","PERRIN","BONOMI",
     "ARGUS","EBRO","SIRAI","MAGNETROL","SPENCE","LESLIE","WATTS","BELGIC","XOMOX","JC VALVES",
     "FUSIMAN","TRILLIUM","ARCA","KROMBACH","SAMSON AG","M&C"],
   "ruido": ["CATERPILLAR","CUMMINS","DOOSAN","KOMATSU","DEUTZ","SCANIA","COPRECI","SENSI","WASSER",
     "M.-F","M-F","EPCM","SAMSUNG","LG","WHIRLPOOL","ELECTROLUX","HAIER","MIDEA","BOSCH","DENSO"],
 },
 "DCS y PLC": {
   "partidas": ["85371000","85371010","85371090","85372000","85372010","85372090","85381000","85389000"],
   "rubro": ["SIEMENS","ABB","SCHNEIDER","ROCKWELL","ALLEN","EMERSON","HONEYWELL","YOKOGAWA",
     "MITSUBISHI","OMRON","FANUC","YASKAWA","BECKHOFF","WAGO","PHOENIX","TURCK","IFM","PEPPERL",
     "RITTAL","WEIDMULLER","LUTZE","HYOSUNG","HITACHI ENERGY","ALSTOM","ETP","GE GRID","HYUNDAI",
     "LS ELECTRIC","EATON","CROMPTON","LAPP","KLAY","NEXANS","SOCOMEC","LEGRAND","HAGER",
     "CHINT","DELIXI","SEW","LENZE","VACON","INNOMOTICS","WEG","DANFOSS","SCHWEITZER","SEL",
     "ARTECHE","PFIFFNER","DAVENHAM","KT-KINETICS","S.A.I.","ETP ELEKTRO","I-LINE","POWELL",
     "FLEXIM","AZBIL","FUJI","SUPCON"],
   "ruido": ["CATERPILLAR","KOMATSU","CUMMINS","DOOSAN","DEUTZ","SCANIA","VOLVO","MERCEDES","FORD",
     "TOYOTA","NISSAN","JOHN DEERE","CNH","COPRECI","BOSCH","DENSO","DELL","LENOVO","HP","APPLE",
     "SAMSUNG","XIAOMI","LG","WHIRLPOOL","HAIER","MIDEA","CISCO","MOTOROLA","SPACEX","HUAWEI",
     "ZTE","NOKIA","ERICSSON","UBIQUITI","ARISTA","FORTINET","TRILIANT","MITRASTAR","GOOGLE"],
 },
 "SIS": {
   "partidas": ["85371000","85371010","85371090","85389000"],
   "rubro": ["HIMA","PILZ","TRICONEX","INVENSYS","SCHNEIDER","SIEMENS","ROCKWELL","ALLEN",
     "YOKOGAWA","HONEYWELL","EMERSON","ABB","SUPCON","ETP","DAVENHAM","NOVA TECH","NOVATECH",
     "MTL","PEPPERL","STAHL","BARTEC","RITTAL","TURCK","IFM","PHOENIX"],
   "ruido": ["CATERPILLAR","KOMATSU","CUMMINS","DOOSAN","DEUTZ","SCANIA","DELL","LENOVO","HP",
     "APPLE","SAMSUNG","CISCO","MOTOROLA","HUAWEI","ZTE","GOOGLE","COPRECI","BOSCH"],
 },
}

def clasificar(marca, nombre, rubro, ruido):
    m = (marca or "").upper().replace("-F","").split("~")[0].strip()
    n = (nombre or "").upper()
    if any(x in m for x in ruido) or any(x in n for x in ruido):
        return "ruido"
    if any(x in m for x in rubro):
        return "rubro"
    if not m or m in ("-","SIN-CODIGO") or len(m) < 3:
        return "sin_marca"
    return "dudoso"

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}\n")

P2L = {}
for lin, cfg in LINEAS.items():
    for p in cfg["partidas"]: P2L.setdefault(p, []).append(lin)

res = collections.defaultdict(lambda: collections.Counter())
items = collections.defaultdict(int)
marcas_lin = collections.defaultdict(collections.Counter)
dudosas = collections.defaultdict(collections.Counter)

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
                k = clasificar(c[134], c[133], cfg["rubro"], cfg["ruido"])
                res[lin][k] += cif
                items[(lin,k)] += 1
                if k == "rubro":
                    marcas_lin[lin][(c[134] or "").upper().replace("-F","").split("~")[0].strip()[:30]] += cif
                elif k == "dudoso":
                    dudosas[lin][(c[134] or "").upper().replace("-F","").split("~")[0].strip()[:30]] += cif

print(f"{'LÍNEA':18s} {'(a) rubro':>12s} {'(b) s/marca':>12s} {'(c) ruido':>11s} {'(d) dudoso':>11s} {'MERCADO a+b':>13s} {'+dudoso':>11s}")
print("-"*100)
sal = {}
for lin in LINEAS:
    d = res[lin]
    a,b,rn,du = d["rubro"], d["sin_marca"], d["ruido"], d["dudoso"]
    mercado = a+b
    con_dud = a+b+du
    print(f"{lin:18s} US${a/1e6:>9,.1f}M US${b/1e6:>9,.1f}M US${rn/1e6:>8,.1f}M US${du/1e6:>8,.1f}M "
          f"US${mercado/1e6:>10,.1f}M US${con_dud/1e6:>8,.1f}M")
    sal[lin] = {"marca_rubro":round(a,2),"sin_marca":round(b,2),"ruido_restado":round(rn,2),
      "dudoso_no_suma":round(du,2),"mercado_usd":round(mercado,2),
      "mercado_con_dudosos_usd":round(con_dud,2),
      "items_rubro":items[(lin,"rubro")],"items_sin_marca":items[(lin,"sin_marca")],
      "top_marcas":[[m,round(v,2)] for m,v in marcas_lin[lin].most_common(15)],
      "top_dudosas":[[m,round(v,2)] for m,v in dudosas[lin].most_common(12)]}

total = sum(v["mercado_usd"] for v in sal.values())
print(f"\nTOTAL hardware (a+b): US${total/1e6:,.1f}M")

json.dump({"metodo":"Clasificación curada a mano por partida: (a) marca del rubro + (b) sin marca = mercado. (c) ruido se resta, (d) dudoso no se suma.",
  "fuente":"Registro DIN Aduanas Chile 2025",
  "lineas":sal,"total_hardware_usd":round(total,2)},
  open(os.path.join(D,"mercado_hardware_fino.json"),"w"), ensure_ascii=False, indent=1)
print(f"guardado: datos/mercado_hardware_fino.json")
