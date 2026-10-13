#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALISIS FOCALIZADO: mercado de ANALIZADORES de proceso en Chile 2025.

Separa, dentro del capitulo 90.27 (instrumentos de analisis fisico/quimico), lo que es
ANALIZADOR DE PROCESO INDUSTRIAL de lo que es equipamiento MEDICO, de LABORATORIO o de
CONSUMO. El capitulo 9027 es el mas contaminado del arancel: mezcla gas, cromatografia,
espectrometria, pH... con reactivos de diagnostico y consumibles medicos.

Salida: datos/analizadores_2025.json + ranking por subpartida, pais y marca.
"""
import os, glob, json, collections

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "datos", "aduanas_2025", "extraido")
D = os.path.join(BASE, "datos")

COL_ARANC, COL_CIF, COL_NOMBRE, COL_MARCA = 157, 158, 133, 134
COL_CANT, COL_PAIS, COL_MEDIDA, COL_FOB = 142, 21, 144, 64

# Glosa oficial de cada subpartida de 90.27 (segun arancel chileno)
GLOSAS = {
 "90271010": "Analizadores de gases o humos (detectores de gas, analizadores de combustion)",
 "90271090": "Los demas analizadores de gases o humos",
 "90272000": "Cromatografos y aparatos de electroforesis",
 "90273000": "Espectrometros, espectrofotometros y espectrografos (opticos UV, IR, absorcion atomica)",
 "90275000": "Los demas aparatos que utilizan radiaciones opticas (UV, visible, IR)",
 "90278000": "Los demas instrumentos y aparatos (pH, conductividad, oxigeno disuelto)",
 "90278100": "Espectrometros de masa",
 "90278900": "Los demas",
 "90278999": "Los demas",
 "90279000": "Microtomos; partes y accesorios de los anteriores",
 "90279090": "Las demas partes y accesorios",
}

# Palabras que marcan ANALIZADOR DE PROCESO / INSTRUMENTO (no consumible ni medico)
KW_PROCESO = ["ANALIZADOR","ANALYZER","CROMATOGRAFO","CHROMATOGRAPH","ESPECTROMETRO","SPECTROMETER",
 "ESPECTROFOTOMETRO","SPECTROPHOTOMETER","FOTOMETRO","PH METRO","MEDIDOR DE PH","CONDUCTIVIMETRO",
 "OXIGENO DISUELTO","DETECTOR DE GAS","GAS DETECTOR","ANALIZADOR DE GAS","MULTIPARAMETRO",
 "TURBIDIMETRO","COLORIMETRO","REFRACTOMETRO","OPACIMETRO","NEPHELOMETER","TITULADOR","TITRATOR",
 "SONDA DE OXIGENO","ANALYZER","MONITOR DE GAS","ANALIZADOR DE HUMOS","MEDIDOR DE CLORO",
 "ANALIZADOR DE OXIGENO","ANALIZADOR DE AZUFRE","XRF","RAMAN","FLUORESCENCIA","CEMS",
 "MEDIDOR DE HUMEDAD","HUMIDITY","ANALIZADOR DE H2S","CONTADOR DE PARTICULAS",
 # agregados tras inspeccion de la categoria 'revisar' (son instrumentos, no consumibles):
 "SENSOR","SONDA","MEDIDOR","TRANSMISOR","DETECTOR","ELECTRODO","CONDUCTIVIDAD","CELDA",
 "LAMBDA","CM442","TERMOGRAFICA","CROMATOGRAFIA","CROMATOGRAFICA","COLUMNA ANALITICA",
 "COLUMNA CROMATOGRAFICA","MONITOR DE","SISTEMA ANALITICO","EQUIPO DE CROMATOGRAFIA",
 "ESPECTOMETRO","ESPECTROMETRO","VISCOSIMETRO","COLORIMETRO","REGISTRADOR DE FUGAS"]

# Palabras que delatan MEDICO, LABORATORIO CLINICO, DIAGNOSTICO o CONSUMIBLE
KW_EXCLUIR = ["REACTIVO","REAGENT","CALIBRADOR","CALIBRATOR","CONTROL DE CALIDAD","DIAGNOSTICO",
 "DIAGNOSTIC","IN VITRO","VITRO","MEDICO","MEDICAL","CLINICO","CLINICAL","PACIENTE","SANGRE",
 "BLOOD","SUERO","SERUM","PLASMA","ORINA","URINE","HEMOGLOBINA","GLUCOSA","GLUCOSE","PCR",
 "COVID","ANTIGENO","ANTIBODY","ANTICUERPO","VACUNA","BIOMERIEUX","ROCHE","SIEMENS HEALTHINEERS",
 "ABBOTT","BECKMAN","ORTHO","BIO-RAD","MINIMED","MEDTRONIC","ANALITO","TEST KIT","KIT DE",
 "CONSUMIBLE","COLUMNA PARA","CARTUCHO","TIRA REACTIVA","SENSOR DE GLUCOSA","ELECTRODO DE",
 "PARTES","PARTE ","ACCESORIO","REPUESTO","ESTUCHE","MALETIN","CUBIERTA","CARCASA",
 "MASCOTA","VETERINAR","ALIMENTO","AGUA POTABLE DOMESTICA","PISCINA",
 # clinico / diagnostico in vitro (hallado en la inspeccion):
 "WERFEN","STAGO","COBAS","INMUNOENSAYO","HEMATOLOGIA","F LASHDX","FLASHDX","TERMOCICLADOR",
 "SEEGENE","DIRUI","GESOTEC","HEALTHCARE","HEALTHINEERS","SIEMENS HEALTHCARE",
 # servicios y consumibles:
 "MANTENCION","REPARACION","INSUMO","SERVICIO DE","MONTAJE","ENSAMBLE","COLUMNA PARA",
 "TUBOS PARA","PLACA PARA","DIFUSOR MICROBURBUJA"]

def parse_num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

def clasificar(nombre, marca):
    n = (nombre or "").upper(); m = (marca or "").upper()
    txt = n + " " + m
    if any(k in txt for k in KW_EXCLUIR): return "excluido"
    if any(k in txt for k in KW_PROCESO): return "proceso"
    return "revisar"

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
SUB = set(GLOSAS.keys())

proceso = collections.defaultdict(lambda: {"cif":0.0,"items":0,"marcas":collections.Counter(),"marcas_valor":collections.Counter()})
revisar = collections.defaultdict(lambda: {"cif":0.0,"items":0})
excluido = {"cif":0.0,"items":0}
por_pais = collections.defaultdict(float)
por_mes = collections.defaultdict(float)
detalle_proceso = []

for f in archivos:
    et = os.path.basename(f).replace("Importaciones - ","").replace("Importaciones ","").replace(".txt","")
    with open(f, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= COL_CIF: continue
            p8 = (c[COL_ARANC] or "").strip()[:8]
            if p8 not in SUB: continue
            cif = parse_num(c[COL_CIF])
            if cif <= 0: continue
            nombre, marca = c[COL_NOMBRE], c[COL_MARCA]
            cl = clasificar(nombre, marca)
            if cl == "proceso":
                d = proceso[p8]; d["cif"]+=cif; d["items"]+=1
                ml = marca.strip().upper()[:30]
                d["marcas"][ml]+=1; d["marcas_valor"][ml]+=cif
                por_pais[(c[COL_PAIS] or "").strip()]+=cif
                por_mes[et]+=cif
                if len(detalle_proceso) < 400:
                    detalle_proceso.append({"mes":et,"partida":p8,"cif":round(cif,2),
                        "nombre":nombre.strip()[:110],"marca":marca.strip()[:40]})
            elif cl == "revisar":
                d = revisar[p8]; d["cif"]+=cif; d["items"]+=1
            else:
                excluido["cif"]+=cif; excluido["items"]+=1

tp = sum(d["cif"] for d in proceso.values())
tr = sum(d["cif"] for d in revisar.values())
print("=== ANALIZADORES (capitulo 90.27) Chile 2025 ===\n")
print(f"  ANALIZADOR DE PROCESO : US${tp/1e6:>7.2f}M  ({sum(d['items'] for d in proceso.values()):,} items)")
print(f"  POR REVISAR (ambiguo) : US${tr/1e6:>7.2f}M  ({sum(d['items'] for d in revisar.values()):,} items)")
print(f"  EXCLUIDO (medico/lab) : US${excluido['cif']/1e6:>7.2f}M  ({excluido['items']:,} items)")

print(f"\n=== POR SUBPARTIDA (solo analizador de proceso) ===")
for p8,d in sorted(proceso.items(), key=lambda x:-x[1]["cif"]):
    print(f"  {p8}  US${d['cif']/1e6:>6.2f}M  {d['items']:>5,} items  {GLOSAS.get(p8,'')[:58]}")

print(f"\n=== PROVEEDORES DE ANALIZADORES DE PROCESO (top 20) ===")
agg = collections.Counter()
for d in proceso.values():
    for m,v in d["marcas_valor"].items(): agg[m]+=v
for m,v in agg.most_common(20):
    print(f"  {m[:34]:34s} US${v/1e6:>6.2f}M")

json.dump({
 "anio":2025,
 "total_proceso_usd":round(tp,2),"total_revisar_usd":round(tr,2),"total_excluido_usd":round(excluido["cif"],2),
 "glosas":GLOSAS,
 "por_subpartida":{p:{"cif":round(d["cif"],2),"items":d["items"],
    "marcas":[list(m) for m in d["marcas_valor"].most_common(25)]} for p,d in proceso.items()},
 "por_pais":dict(sorted(por_pais.items(), key=lambda x:-x[1])[:30]),
 "por_mes":dict(por_mes),
 "detalle_muestra":detalle_proceso,
}, open(os.path.join(D,"analizadores_2025.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/analizadores_2025.json")
