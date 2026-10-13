#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASO 1 (v3 - DEFINITIVA) del estudio de mercado SUPCON.

PROBLEMA que corrige la v3: filtrar solo por partida arancelaria NO alcanza.
Las partidas de equipo de red (8517), procesamiento (8471) y analisis (9027) mezclan
TI de consumo/cloud (Google, Dell, Apple, Cisco, SpaceX) y equipamiento MEDICO
(Roche, MiniMed, Waters) con la automatizacion industrial. Medido: US$766M "servidores"
de los cuales la mayoria es Google/Dell/Apple.

ESTRATEGIA v3: dos condiciones simultaneas
  (1) la partida arancelaria pertenece al dominio de automatizacion, Y
  (2) la MARCA declarada es de un fabricante de automatizacion/instrumentacion conocido
      (o la descripcion contiene un termino tecnico inequivoco de proceso).
Asi se separa mercado industrial real de TI de consumo.

Fuente de partidas: Registro de Importaciones DIN (Aduanas) 2025, 12 meses, datos.gob.cl
"""
import os, glob, json, collections

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "datos", "aduanas_2025", "extraido")
OUT = os.path.join(BASE, "datos")

COL_ARANC, COL_CIF, COL_NOMBRE, COL_MARCA = 157, 158, 133, 134
COL_CANT, COL_PAIS, COL_FOB, COL_MEDIDA = 142, 21, 64, 144

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

# ---------------------------------------------------------------------------
# PARTIDAS del dominio automatizacion / instrumentacion industrial
# ---------------------------------------------------------------------------
PARTIDAS = {
 "Instrumentacion de campo": [
   "90261010","90261090","90262010","90262019","90262090","90268010","90268090","90269000",
   "90251100","90251900","90258010","90258090","90259000","90248000","90249000",
 ],
 "Analizadores de proceso": [
   "90271010","90271090","90272000","90273000","90275000","90278100","90278900","90278999","90279000","90279090",
 ],
 "Valvulas de control y proceso": [
   "84811000","84812010","84812020","84813000","84814000","84818010","84818090","84819000",
 ],
 "Controladores, PLC y modulos de E/S": [
   "85371010","85371090","85372000","85372010","85372090","85371000","85381000","85389000",
 ],
 "Medida y control electrico": [
   "90301000","90302000","90303100","90303200","90303300","90303900","90304000","90308200","90308400","90308900","90309000",
   "90321000","90322000","90328100","90328900","90329000","90283000","90283010","90283090","90289000",
 ],
 "Redes industriales (OT)": ["85176210","85176220","85176290","85176900","85177000","85177900"],
 "Fuentes de poder y convertidores": ["85043100","85043200","85043300","85044000","85045000","85049000"],
 "Aparatos de conexion y proteccion": ["85361000","85362000","85363000","85364100","85364900","85365000","85366100","85366900","85367000","85369000","85369013"],
 "Detectores de gas y alarma": ["85311000","85312000","85318000","85319000"],
 "Vision industrial": ["85258100","85258200","85258300","85258900"],
}

# Accesorios/partes que NO son instrumentos (se excluyen por descripcion)
EXCLUIR_DESC = [
 "PARTE","PARTES","ACCESORIO","REPUESTO","SOPORTE","CARCASA","CUBIERTA","CABLE","CONDUCTOR",
 "PLACA","ETIQUETA","MANUAL","CATALOGO","ESTUCHE","MALETIN","CORREA","BATERIA","PILA",
 "AUTOMOVIL","VEHICULO","CAMION","TRACTOR","BUS","MOTOCICLETA","MOTOR DIESEL","FRENO",
 "TELEFONO","CELULAR","TABLET","NOTEBOOK","LAPTOP","IMPRESORA","TELEVISOR","AUDIFONO",
 "JUGUETE","ELECTRODOMESTICO","MEDICAMENTO","COSMETICO","PROTESIS",
]

# MARCAS de automatizacion / instrumentacion industrial (lista blanca)
MARCAS_OT = {
 # instrumentacion y analisis
 "ENDRESS","ENDRESS + HAUSER","ENDRESS+HAUSER","E+H","KROHNE","MICRO MOTION","FLEXIM","CIDRA",
 "ROSEMOUNT","YOKOGAWA","HONEYWELL","ABB","SIEMENS","SCHNEIDER","SCHNEIDER ELECTRIC","EMERSON",
 "METSO","VALMET","FUJI","AZBIL","MITSUBISHI","OMRON","PHOENIX CONTACT","PEPPERL","TURCK",
 "IFM","IFM ELECTRONIC","SICK","BALLUFF","BAUMER","LEUZE","KEYENCE","WIKA","ASHCROFT",
 "GE","GE MEASUREMENT","DANFOSS","SAMSON","MASONEILAN","FISHER","SENSIDACQUA","VALVITALIA",
 "BRAY","NELES","VELAN","CONSORT","CIRCOR","KITZ","BROOKS","EMERSON-F","ROTORK","AUMA",
 "MTS","AMETEK","DREXELBROOK","MAGNETROL","HAWK","VEGA","PEPPERL+FUCHS","BD SENSORS",
 "TESTO","DRAGER","MSA","MSA-F","DETCON","GASMET","ELT","SERVOMEX","ROSEMOUNT ANALYTICAL",
 "THERMO","THERMO ELECTRON","THERMO FISHER","AGILENT","SHIMADZU","PERKIN","BRUKER","HACH",
 "WTW","XYLEM","YSI","ENDRESS ANALYTICAL","APPLITEK","APPLITEK-F","BARTEC","STAHL",
 # control y PLC
 "SUPCON","NOVATECH","SEL","SCHWEITZER","GENERAL ELECTRIC","SEPRO","HITACHI ENERGY",
 "BECKHOFF","WAGO","ROCKWELL","ALLEN","ALLEN-BRADLEY","DELTA","FESTO","SMC","PILZ",
 "TURCK-F","LAPP","RITTAL","WEIDMULLER","PHOENIX","LUTZE","MURR","B&R","BECKHOFF-F",
 "GE FANUC","FANUC","YASKAWA","SEW","LENZE","VACON","VACON-F","INNOMOTICS","WEG",
 # redes OT
 "HIRSCHMANN","BELDEN","MOXA","ADVANTECH","SIERRA WIRELESS","DIGI","LANTRONIX","PERLE",
 "SCALANCE","RUGGEDCOM","CISCO IE","GARRETTCOM","KYLAND","H3C",
 # energia / proteccion
 "SEL-F","SEL","GENERAL ELECTRIC-F","GESILENT","HITACHI","HYOSUNG","ALSTOM","ETP",
 "SGB","ARTECHE","PFIFFNER","TELEDYNE","QUALITROL","DOBLE","OMICRON","MEGGER","FLUKE",
 "CHROMALOX","EUROTHERM","WATLOW","HANYOUNG",
}

def marca_es_ot(marca):
    m = (marca or "").upper().strip()
    if not m: return False
    # limpiar sufijos internos de Aduanas (-F = facturado?)
    m_limpio = m.replace("-F","").replace("~","").split("~")[0].strip()
    for cand in MARCAS_OT:
        c = cand.replace("-F","")
        if m_limpio == c or m_limpio.startswith(c + " ") or m_limpio.startswith(c + "-") or c in m_limpio:
            return True
    return False

def desc_es_proceso(nombre):
    n = (nombre or "").upper()
    return not any(x in n for x in EXCLUIR_DESC)

P2FAM = {}
for fam, lista in PARTIDAS.items():
    for p in lista: P2FAM[p] = fam

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}  |  partidas en el dominio: {len(P2FAM)}")

por_familia = collections.defaultdict(lambda: {"cif":0.0,"items":0,"marcas":collections.Counter(),
                                               "marcas_valor":collections.Counter(),"partidas":collections.Counter()})
por_partida = collections.defaultdict(lambda: {"cif":0.0,"items":0,"fam":""})
por_pais = collections.defaultdict(float)
por_mes = collections.defaultdict(float)
tot = rel = excl = sinmarca = 0

for f in archivos:
    et = os.path.basename(f).replace("Importaciones - ","").replace("Importaciones ","").replace(".txt","")
    bajo = 0.0
    with open(f, encoding="latin-1") as fh:
        for line in fh:
            tot += 1
            c = line.rstrip("\n").split(";")
            if len(c) <= COL_CIF: continue
            p8 = (c[COL_ARANC] or "").strip()[:8]
            fam = P2FAM.get(p8)
            if not fam: continue
            nombre = c[COL_NOMBRE]; marca = c[COL_MARCA]
            if not desc_es_proceso(nombre):
                excl += 1; continue
            # condicion 2: marca de automatizacion conocida
            if not marca_es_ot(marca):
                sinmarca += 1; continue
            cif = num(c[COL_CIF])
            if cif <= 0: continue
            rel += 1
            fa = por_familia[fam]; fa["cif"]+=cif; fa["items"]+=1
            ml = marca.strip().upper()[:30]
            fa["marcas"][ml]+=1; fa["marcas_valor"][ml]+=cif; fa["partidas"][p8]+=1
            pp = por_partida[p8]; pp["cif"]+=cif; pp["items"]+=1; pp["fam"]=fam
            por_pais[(c[COL_PAIS] or "").strip()]+=cif
            por_mes[et]+=cif
            bajo += cif
    print(f"  {et:26s} US${bajo/1e6:>8,.1f} M")

print(f"\n=== TOTALES ===")
print(f"lineas leidas      : {tot:,}")
print(f"  fuera de dominio : {tot-rel-excl-sinmarca:,}")
print(f"  excluidas (parte/consumo): {excl:,}")
print(f"  sin marca OT      : {sinmarca:,}")
print(f"  RELEVANTES        : {rel:,}")

print(f"\n=== MERCADO POR FAMILIA (USD CIF 2025, marcas OT) ===")
tt=0
for fam,d in sorted(por_familia.items(), key=lambda x:-x[1]["cif"]):
    tt+=d["cif"]
    print(f"  {fam:42s} US${d['cif']/1e6:>8,.1f} M  items={d['items']:>7,}")
print(f"  {'TOTAL':42s} US${tt/1e6:>8,.1f} M")

json.dump({
 "anio":2025,"lineas_totales":tot,"lineas_relevantes":rel,
 "excluidas":excl,"sin_marca_ot":sinmarca,
 "por_familia":{f:{"cif":round(d["cif"],2),"items":d["items"],
   "marcas":[list(m) for m in d["marcas"].most_common(40)],
   "marcas_valor":[list(m) for m in d["marcas_valor"].most_common(40)],
   "partidas":dict(d["partidas"].most_common(40))} for f,d in por_familia.items()},
 "por_partida":dict(sorted(por_partida.items(), key=lambda x:-x[1]["cif"])),
 "por_pais":dict(sorted(por_pais.items(), key=lambda x:-x[1])[:50]),
 "por_mes":dict(por_mes),
}, open(os.path.join(OUT,"estudio_mercado_2025.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/estudio_mercado_2025.json")
