#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICACIÓN DEL FILTRO DE MARCA, LÍNEA POR LÍNEA.

Por qué existe: en válvulas, el flujo general (filtrar por marca + partida) midió US$53,8M
cuando el mercado real es US$396,6M — un factor de 7. El filtro por marca sirve para medir
COMPETENCIA, pero destruye la medición de TAMAÑO, porque deja fuera todo lo que entra sin
declarar fabricante. No se puede asumir que ese error sea igual en todas las líneas: hay
que medirlo.

Método: para cada familia, calcular TRES cosas sobre las partidas del dominio:
  a) total de la partida (sin filtro de marca)  -> el techo del mercado
  b) con marca del rubro                          -> competencia identificable
  c) sin marca del rubro                          -> mercado real con fabricante no declarado
  d) ruido de otros rubros                        -> hay que restarlo
Y comparar (a) contra lo que reportó el estudio general.

Salida: datos/verificacion_filtro_marca.json
"""
import glob, os, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

# ---- familias y sus partidas (las mismas del estudio general) ----
FAMILIAS = {
 "Presión": ["90262010","90262019","90262090","90269000"],
 "Temperatura": ["90251100","90251900","90258010","90258090","90259000"],
 "Caudal y Nivel": ["90261010","90261090","90268010","90268090"],
 "Analizadores": ["90271010","90271090","90272000","90273000","90275000","90278100","90278999","90279090"],
 "Válvulas": ["84811000","84812010","84812020","84813000","84814000","84818010","84818090","84819000"],
 "DCS y PLC": ["85371000","85371010","85371090","85372000","85372010","85372090","85381000","85389000"],
 "Calibración": ["90303100","90303200","90303300","90303900","90304000","90308900"],
 "Medición eléctrica": ["90301000","90302000","90308200","90308400","90283000","90283010","90283090"],
 "Redes OT": ["85176210","85176220","85176290","85176900","85177000"],
 "Ciberseguridad": ["84714110","84714190","84714900","84715000","84718000","84733000","85423100","85423900"],
}

# ---- marcas que NO pertenecen a cada rubro (ruido) ----
RUIDO = {
 "AUTOMOCION": ["CATERPILLAR","DOOSAN","CUMMINS","KOMATSU","DEUTZ","SCANIA","VOLVO","JOHN DEERE",
   "PERKINS","YANMAR","MERCEDES","FORD","TOYOTA","NISSAN","CNH","COPRECI","BOSCH","DENSO",
   "MAHLE","WABCO","KNORR","SENSI","M.-F","M-F","EPCM","WASSER","HITACHI","ZF","EATON"],
 "CONSUMO_TI": ["DELL","LENOVO","HP","APPLE","ACER","ASUS","SAMSUNG","XIAOMI","SAMSUNG ELECTRONICS"],
 "ELECTRODOMESTICO": ["LG","WHIRLPOOL","ELECTROLUX","MABE","HAIER","MIDEA"],
}

# ---- marcas del rubro de automatizacion e instrumentacion ----
RUBRO = ["ENDRESS","KROHNE","MICRO MOTION","FLEXIM","CIDRA","ROSEMOUNT","YOKOGAWA","HONEYWELL",
 "ABB","SIEMENS","SCHNEIDER","EMERSON","METSO","VALMET","FUJI","AZBIL","MITSUBISHI","OMRON",
 "PHOENIX","TURCK","IFM","SICK","BALLUFF","BAUMER","LEUZE","KEYENCE","WIKA","ASHCROFT","DANFOSS",
 "SAMSON","MASONEILAN","FISHER","VALVITALIA","BRAY","NELES","VELAN","CIRCOR","KITZ","ROTORK","AUMA",
 "MTS","AMETEK","MAGNETROL","VEGA","PEPPERL","TESTO","DRAGER","MSA","SERVOMEX","THERMO","AGILENT",
 "SHIMADZU","BRUKER","HACH","WTW","XYLEM","YSI","BARTEC","STAHL","SEL","HITACHI ENERGY","HYOSUNG",
 "ALSTOM","ETP","ARTECHE","PFIFFNER","TELEDYNE","QUALITROL","DOBLE","OMICRON","MEGGER","FLUKE",
 "WATERS","PERKIN","LECO","BUCHI","KNAUER","ANALYTIK","BECKHOFF","WAGO","ROCKWELL","ALLEN",
 "FESTO","SMC","PILZ","RITTAL","WEIDMULLER","LUTZE","FANUC","YASKAWA","SEW","LENZE","VACON",
 "INNOMOTICS","WEG","HIRSCHMANN","BELDEN","MOXA","ADVANTAGE","ADVANTECH","DIGI","LANTRONIX",
 "PERLE","KYLAND","GENERAL ELECTRIC","GE GRID","SCHWEITZER","GENEBRE","FLOWSERVE","BERMAD"]

P2FAMS = {}
for fam, lst in FAMILIAS.items():
    for p in lst: P2FAMS.setdefault(p, []).append(fam)

def clasificar(marca, nombre):
    m = (marca or "").upper().replace("-F","").split("~")[0].strip()
    n = (nombre or "").upper()
    for rub, marcas in RUIDO.items():
        if any(x in m for x in marcas) or any(x in n for x in marcas):
            return "ruido"
    if not m or m in ("-","SIN-CODIGO") or len(m) < 3:
        return "sin_marca"
    for c in RUBRO:
        if m == c or m.startswith(c+" ") or m.startswith(c+"-") or c in m:
            return "rubro"
    return "otra_marca"

res = collections.defaultdict(lambda: {"total":0.0,"rubro":0.0,"sin_marca":0.0,"otra":0.0,"ruido":0.0,"items":0})
archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}\n")

for txt in archivos:
    with open(txt, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= 158: continue
            p8 = (c[157] or "").strip()[:8]
            fams = P2FAMS.get(p8)
            if not fams: continue
            cif = num(c[158])
            if cif <= 0: continue
            k = clasificar(c[134], c[133])
            for fam in fams:
                d = res[fam]
                d["total"] += cif; d["items"] += 1
                if k in ("rubro","sin_marca","otra","ruido"):
                    d[k] += cif

print(f"{'FAMILIA':20s} {'PARTIDA':>11s} {'MARCA RUBRO':>12s} {'SIN MARCA':>11s} {'RUIDO':>10s} {'MERCADO est.':>13s} {'vs estudio':>11s}")
print("-"*100)

# lo que reportó el estudio general (datos/cruce_catalogo_importaciones.json)
cruce = json.load(open(os.path.join(D,"cruce_catalogo_importaciones.json"), encoding="utf-8"))
reportado = {k: v["cif"] for k, v in cruce["mercado_por_familia"].items()}

salida = {}
for fam, d in res.items():
    mercado = d["total"] - d["ruido"]
    # buscar el valor reportado que corresponda a esta familia
    rep = 0.0
    for k, v in reportado.items():
        if fam.lower().split()[0] in k.lower(): rep = v; break
    fac = (mercado/rep) if rep > 0 else 0
    print(f"{fam:20s} US${d['total']/1e6:>8,.1f}M US${d['rubro']/1e6:>9,.1f}M US${d['sin_marca']/1e6:>8,.1f}M "
          f"US${d['ruido']/1e6:>7,.1f}M US${mercado/1e6:>10,.1f}M {fac:>10.1f}x")
    salida[fam] = {"total_partida":round(d["total"],2),"marca_rubro":round(d["rubro"],2),
                   "sin_marca_rubro":round(d["sin_marca"],2),"otra_marca":round(d["otra"],2),
                   "ruido":round(d["ruido"],2),"mercado_estimado":round(mercado,2),
                   "reportado_por_estudio_general":round(rep,2),
                   "factor_subestimacion":round(fac,2) if fac else None,"items":d["items"]}

json.dump({"nota":"Verificación del filtro por marca línea por línea. 'mercado_estimado' = partida total - ruido de otros rubros. 'reportado_por_estudio_general' es lo que dijo el cruce general.",
  "familias":salida}, open(os.path.join(D,"verificacion_filtro_marca.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/verificacion_filtro_marca.json")
