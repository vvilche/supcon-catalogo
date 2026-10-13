#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUCE: catalogo SUPCON <-> importaciones reales de Chile 2025.

Para cada familia del catalogo SUPCON, busca en el registro DIN de Aduanas:
  1) si SUPCON aparece declarado como marca (presencia directa del fabricante)
  2) cuantas importaciones caen en las partidas que corresponden a esa familia
  3) que marcas competidoras ocupan esas partidas (con nombre y monto)

Salida: datos/cruce_catalogo_importaciones.json
"""
import os, glob, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

COL_ARANC, COL_CIF, COL_NOMBRE, COL_MARCA = 157, 158, 133, 134
COL_PAIS, COL_FOB, COL_CANT = 21, 64, 142

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

# ---------------------------------------------------------------------------
# PARTIDAS por familia del catalogo (8 digitos del SA chileno)
# ---------------------------------------------------------------------------
FAMILIAS = {
 "Presión (CXT, CJT)": ["90262010","90262019","90262090","90269000"],
 "Temperatura (W Series)": ["90251100","90251900","90258010","90258090","90259000"],
 "Caudal (SFE910, SFM800, LUGB, YHLW, SF20)": [
    "90261010","90261090","90268010","90268090"],
 "Nivel (SL903, SL10/20/80)": ["90261010","90261090","90268010","90268090"],
 "Válvulas y posicionadores (CVP2000)": ["84811000","84812010","84812020","84813000","84814000","84818010","84818090","84819000"],
 "Analizadores de proceso (Hobre)": ["90271010","90271090","90272000","90273000","90275000","90278100","90278999","90279090"],
 "Calibración (X600)": ["90303100","90303200","90303300","90303900","90304000","90308900"],
 "DCS / Controladores (ECS-700, OMC)": ["85371000","85371010","85371090","85372000","85372010","85372090","85381000","85389000"],
 "SIS (TCS-900, TCS-500)": ["85371000","85371010","85371090","85389000"],
 "PLC (G5Pro, G3Smart)": ["85371000","85371010","85371090","85372000","85372090"],
 "Medición eléctrica / protecciones": ["90301000","90302000","90308200","90308400","90283000","90283010","90283090"],
 "Redes OT (switches, gateways)": ["85176210","85176220","85176290","85176900","85177000"],
 "Fuentes y convertidores": ["85043100","85043200","85043300","85044000","85045000","85049000"],
 "Ciberseguridad / procesamiento": ["84714110","84714190","84714900","84715000","84718000","84733000","85423100","85423900"],
}

# Marcas que SON del catalogo SUPCON (para detectar presencia directa)
MARCAS_PROPIAS = ["SUPCON","HOBRE","TISOMIC","C-QUAND","CQUAND","WIM COMPAS","PRISM RAMAN"]

# MARCAS AMBIGUAS: el nombre no es exclusivo del fabricante del catalogo, asi que una
# coincidencia NO prueba presencia. Verificado en el registro 2025:
#  - NOVATECH: aparece en repuestos de automocion (frenos, tanques de aire, cojinetes) y en
#    "RALTRAC INNOVATECH" (gabinete de carga). NO es NovaTech Automation.
#  - HOBRE: aparece en ropa ("CAMISAS PARA HOBRES", "POLERA DE HOBRE") por la palabra
#    "hombre" sin tilde. Se revisa igual, pero se reporta como sospechoso.
MARCAS_AMBIGUAS = ["NOVATECH"]

# Marcas conocidas de instrumentacion/automatizacion (para separar ruido)
MARCAS_RUBRO = [
 "ENDRESS","KROHNE","MICRO MOTION","FLEXIM","CIDRA","ROSEMOUNT","YOKOGAWA","HONEYWELL","ABB",
 "SIEMENS","SCHNEIDER","EMERSON","METSO","VALMET","FUJI","AZBIL","MITSUBISHI","OMRON",
 "PHOENIX CONTACT","TURCK","IFM","SICK","BALLUFF","BAUMER","LEUZE","KEYENCE","WIKA","ASHCROFT",
 "DANFOSS","SAMSON","MASONEILAN","FISHER","VALVITALIA","BRAY","NELES","VELAN","CIRCOR","KITZ",
 "ROTORK","AUMA","MTS","AMETEK","MAGNETROL","VEGA","PEPPERL","TESTO","DRAGER","MSA","SERVOMEX",
 "THERMO","AGILENT","SHIMADZU","BRUKER","HACH","WTW","XYLEM","YSI","BARTEC","STAHL","SEL",
 "HITACHI","HYOSUNG","ALSTOM","ETP","ARTECHE","PFIFFNER","TELEDYNE","QUALITROL","DOBLE","OMICRON",
 "MEGGER","FLUKE","WATERS","PERKIN","LECO","BUCHI","KNAUER","ANALYTIK","BECKHOFF","WAGO",
 "ROCKWELL","ALLEN","FESTO","SMC","PILZ","RITTAL","WEIDMULLER","LUTZE","FANUC","YASKAWA",
 "SEW","LENZE","VACON","INNOMOTICS","WEG","HIRSCHMANN","BELDEN","MOXA","ADVANTECH","DIGI",
 "LANTRONIX","PERLE","KYLAND","GE","GENERAL ELECTRIC","SCHWEITZER",
]

def es_rubro(marca):
    m = (marca or "").upper().replace("-F","").split("~")[0].strip()
    if not m: return False
    return any(m == c or m.startswith(c+" ") or m.startswith(c+"-") or c in m for c in MARCAS_RUBRO)

EXCLUIR = ["PARTE","ACCESORIO","REPUESTO","ESTUCHE","AUTOMOVIL","VEHICULO","CAMION","TRACTOR",
 "TELEFONO","CELULAR","TABLET","NOTEBOOK","LAPTOP","IMPRESORA","TELEVISOR","AUDIFONO",
 "JUGUETE","ELECTRODOMESTICO","MEDICAMENTO","REACTIVO","DIAGNOSTICO","IN VITRO"]

def desc_ok(n):
    n = (n or "").upper()
    return not any(x in n for x in EXCLUIR)

TODAS_PARTIDAS = set()
for l in FAMILIAS.values(): TODAS_PARTIDAS.update(l)

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)} | partidas del cruce: {len(TODAS_PARTIDAS)}")

# por familia: valor, items, marcas rivales
fam_data = collections.defaultdict(lambda: {"cif":0.0,"items":0,"marcas":collections.Counter(),"paises":collections.Counter()})
# presencia propia (cualquier partida)
propia = collections.defaultdict(lambda: {"cif":0.0,"items":0,"detalle":[]})
tot_lineas = 0

for f in archivos:
    mes = os.path.basename(f).replace("Importaciones - ","").replace("Importaciones ","").replace(".txt","")
    with open(f, encoding="latin-1") as fh:
        for line in fh:
            tot_lineas += 1
            c = line.rstrip("\n").split(";")
            if len(c) <= COL_CIF: continue
            p8 = (c[COL_ARANC] or "").strip()[:8]
            marca = c[COL_MARCA] or ""
            nombre = c[COL_NOMBRE] or ""
            up = (nombre + " " + marca).upper()

            # A) PRESENCIA DIRECTA de las marcas del catalogo.
            # GUARDAS: la partida debe pertenecer al dominio (no ropa, no automocion) y la
            # glosa no puede ser de otro rubro. Sin esto entra 'CAMISAS PARA HOBRES' (ropa)
            # y los repuestos de una empresa homonima llamada NOVATECH (automocion).
            PARTIDAS_DOMINIO = set()
            for _l in FAMILIAS.values(): PARTIDAS_DOMINIO.update(_l)
            for mp in MARCAS_PROPIAS:
                if mp in up and p8 in PARTIDAS_DOMINIO and desc_ok(nombre):
                    cif = num(c[COL_CIF])
                    if cif > 0:
                        propia[mp]["cif"] += cif
                        propia[mp]["items"] += 1
                        if len(propia[mp]["detalle"]) < 20:
                            propia[mp]["detalle"].append({
                                "mes":mes,"partida":p8,"cif":round(cif,2),
                                "nombre":nombre.strip()[:100],"marca":marca.strip()[:40]})

            # B) MERCADO por familia (solo partidas del dominio + marca del rubro)
            if p8 not in TODAS_PARTIDAS: continue
            if not desc_ok(nombre): continue
            if not es_rubro(marca): continue
            cif = num(c[COL_CIF])
            if cif <= 0: continue
            for fam, lista in FAMILIAS.items():
                if p8 in lista:
                    d = fam_data[fam]
                    d["cif"] += cif; d["items"] += 1
                    d["marcas"][marca.strip().upper()[:30]] += cif
                    d["paises"][(c[COL_PAIS] or "").strip()] += cif

print(f"\n=== A) PRESENCIA DE MARCAS DEL CATALOGO ===")
for mp in MARCAS_PROPIAS:
    d = propia[mp]
    if d["items"]:
        print(f"  {mp:12s} US${d['cif']:>10,.0f}  ({d['items']} items)")
    else:
        print(f"  {mp:12s} sin presencia")
        propia[mp]["detalle"] = []

print(f"\n=== B) MERCADO QUE MATCHEA CADA FAMILIA ===")
resumen = {}
for fam, d in sorted(fam_data.items(), key=lambda x:-x[1]["cif"]):
    print(f"\n--- {fam} ---")
    print(f"    US${d['cif']/1e6:,.1f}M  ({d['items']:,} items)")
    for m, v in d["marcas"].most_common(8):
        print(f"      {m[:32]:32s} US${v/1e6:>6.2f}M")
    resumen[fam] = {"cif":round(d["cif"],2),"items":d["items"],
                    "marcas":[[m,round(v,2)] for m,v in d["marcas"].most_common(20)],
                    "paises":[[p,round(v,2)] for p,v in d["paises"].most_common(10)]}

json.dump({"anio":2025,"lineas_totales":tot_lineas,
  "presencia_marcas_catalogo":{k:{"cif":round(v["cif"],2),"items":v["items"],"detalle":v["detalle"]} for k,v in propia.items()},
  "mercado_por_familia":resumen,
}, open(os.path.join(D,"cruce_catalogo_importaciones.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/cruce_catalogo_importaciones.json")
