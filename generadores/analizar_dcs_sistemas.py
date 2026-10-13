#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCS Y SISTEMAS DE CONTROL — detalle del mercado por tipo de sistema.

Las partidas 8537 agrupan tres cosas distintas que conviene separar porque se venden distinto:
  1. CONTROL DE PROCESO: tableros con PLC/DCS, paneles de operador, sistemas de control.
     Es donde compite SUPCON (ECS-700, OMC, G5Pro, TCS-900, UCS Nyx).
  2. DISTRIBUCIÓN ELÉCTRICA: tableros de media y alta tensión, celdas, centros de carga.
     Es el negocio eléctrico clásico (lo que CONECTA ya vende con otras marcas).
  3. PARTES Y COMPONENTES: partes de tableros y de aparatos de conexión.

Además, el registro de Aduanas NO tiene partida de DCS: un DCS entra como "tablero con aparato
eléctrico de control" (85371000), igual que un tablero de distribución. La separación se hace
por GLOSA del ítem y por MARCA, con el mismo criterio curado del análisis de hardware.

Cubre tambien los sistemas asociados que no tienen partida propia: SCADA, historizador,
seguridad funcional (SIS), instrumentación de sistema y red de control.

Salida: datos/mercado_dcs_sistemas.json
"""
import glob, os, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

PARTIDAS = {
 "85371000":"Tableros y paneles de control (hasta 1000 V)",
 "85371010":"Tableros de control numérico",
 "85371090":"Soportes con aparatos eléctricos de control",
 "85372000":"Tableros de control (más de 1000 V)",
 "85372010":"Tableros de distribución de alta tensión",
 "85372090":"Tableros eléctricos (otros)",
 "85381000":"Partes de tableros y paneles",
 "85389000":"Partes de aparatos eléctricos de conexión",
}

# ---- clasificación por GLOSA: qué tipo de sistema es ----
GLOSA = {
 "Control de proceso (DCS/PLC/SCADA)": ["CONTROL","PLC","DCS","SCADA","LOGIC","LOGICO","AUTOMATIZ",
   "PROCESO","MONITOREO","TELEMETR","ADQUISICION DE DATOS","OPERADOR","HMI","PROGRAMABLE",
   "SOFTWARE","SISTEMA DE CONTROL","PANEL DE CONTROL","TABLERO DE CONTROL","CONTROLADOR"],
 "Distribución eléctrica (celdas, CCM)": ["DISTRIBUCION","CELDA","MEDIA TENSION","ALTA TENSION",
   "CENTRO DE CARGA","CCM","MCC","SWITCHGEAR","INTERRUPTOR","SECCIONADOR","BARRA","TRANSFORMADOR",
   "COMPENSACION","CORRECTOR","BANCO DE CONDENSAD","SUBESTACION","PROTECCION ELECTRIC","RELE"],
 "Instrumentación de sistema": ["TRANSMISOR","SENSOR","MEDIDOR","ANALIZADOR","ACTUADOR","VALVULA",
   "ROTAMETRO","CAUDALIMETRO","TERMOCUPLA","PRESOSTATO","TERMOSTATO"],
 "Red de control / comunicación": ["SWITCH","ROUTER","FIREWALL","FIBRA","ETHERNET","COMUNICAC",
   "GATEWAY","MODEM","ANTENA","RED ","PROTOCOLO"],
 "Seguridad funcional (SIS/ESD/F&G)": ["SEGURIDAD","ESD","SHUTDOWN","PARADA","SIL","FIRE","GAS",
   "DETECCION","ALARMA","INCENDIO","EXTINCION"],
}
MARCAS_CONTROL = ["SIEMENS","ABB","SCHNEIDER","ROCKWELL","ALLEN","EMERSON","HONEYWELL","YOKOGAWA",
 "MITSUBISHI","OMRON","FANUC","YASKAWA","BECKHOFF","WAGO","PHOENIX","TURCK","IFM","AZBIL","FUJI",
 "LS ELECTRIC","DELTA","SEW","LENZE","VACON","INNOMOTICS","SUPCON","GE","HITACHI","TOSHIBA"]
MARCAS_ELECTRICO = ["SCHNEIDER","ABB","SIEMENS","ETP","HYOSUNG","ALSTOM","HYUNDAI","LS ELECTRIC",
 "EATON","LEGRAND","HAGER","SOCOMEC","CHINT","DELIXI","DAVENHAM","KT-KINETICS","S.E.","S.A.I",
 "I-LINE","POWELL","BARR","RITTAL","WEIDMULLER","CROMPTON","GE GRID","SEL","ARTECHE","PFIFFNER",
 "HITACHI ENERGY","TOSHIBA","MITSUBISHI ELECTRIC","ORMAZABAL","GENERAL ELECTRIC"]
RUIDO = ["CATERPILLAR","KOMATSU","CUMMINS","DOOSAN","DEUTZ","SCANIA","VOLVO","MERCEDES","FORD",
 "TOYOTA","NISSAN","COPRECI","BOSCH","DENSO","DELL","LENOVO","HP","APPLE","SAMSUNG","XIAOMI",
 "LG","WHIRLPOOL","HAIER","MIDEA","CISCO","MOTOROLA","SPACEX","HUAWEI","ZTE","NOKIA","ERICSSON",
 "UBIQUITI","ARISTA","FORTINET","GOOGLE","INETICS","ROCHE","ABBOTT","MINIMED"]

def clasificar(nombre, marca):
    n = (nombre or "").upper()
    m = (marca or "").upper().replace("-F","").split("~")[0].strip()
    if any(x in m for x in RUIDO) or any(x in n for x in RUIDO): return "ruido"
    for cat, claves in GLOSA.items():
        if any(k in n for k in claves): return cat
    # sin glosa util: clasificar por marca
    if any(x in m for x in MARCAS_CONTROL): return "Control de proceso (DCS/PLC/SCADA)"
    if any(x in m for x in MARCAS_ELECTRICO): return "Distribución eléctrica (celdas, CCM)"
    return "sin clasificar"

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}\n")

cat = collections.defaultdict(float)
cat_items = collections.defaultdict(float)
ruido_tot = 0.0
total = 0.0
marcas_ctrl = collections.Counter()
marcas_elec = collections.Counter()
por_partida_cat = collections.defaultdict(lambda: collections.Counter())
paises_ctrl = collections.Counter()
importadores_ctrl = set()
importadores_elec = set()

for txt in archivos:
    with open(txt, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= 158: continue
            p8 = (c[157] or "").strip()[:8]
            if p8 not in PARTIDAS: continue
            cif = num(c[158])
            if cif <= 0: continue
            total += cif
            k = clasificar(c[133], c[134])
            cat[k] += cif
            cat_items[k] += 1
            por_partida_cat[k][PARTIDAS[p8]] += cif
            m = (c[134] or "").upper().replace("-F","").split("~")[0].strip()[:28]
            if k == "Control de proceso (DCS/PLC/SCADA)":
                marcas_ctrl[m] += cif
                paises_ctrl[(c[21] or "").strip()] += cif
                if (c[6] or "").strip(): importadores_ctrl.add((c[6] or "").strip())
            elif k == "Distribución eléctrica (celdas, CCM)":
                marcas_elec[m] += cif
                if (c[6] or "").strip(): importadores_elec.add((c[6] or "").strip())
            elif k == "ruido":
                ruido_tot += cif

PAIS = {"336":"Alemania","563":"China","505":"EE.UU.","504":"EE.UU.","508":"Japón","507":"Japón",
 "512":"Italia","225":"Francia","317":"Corea del Sur","220":"España","528":"Países Bajos",
 "511":"Canadá","510":"Taiwán","331":"Brasil","517":"Singapur","216":"Noruega","549":"India",
 "224":"Finlandia","484":"Suecia"}

print(f"=== PARTIDAS 8537 + 8538: US${total/1e6:,.1f}M en total ===\n")
print(f"{'CATEGORÍA':38s} {'VALOR':>11s} {'%':>6s} {'ítems':>8s}")
print("-"*68)
for k, v in sorted(cat.items(), key=lambda x:-x[1]):
    print(f"{k:38s} US${v/1e6:>8,.1f}M {v/total*100:>5.1f}% {cat_items[k]:>8,}")

ctrl = cat["Control de proceso (DCS/PLC/SCADA)"]
elec = cat["Distribución eléctrica (celdas, CCM)"]
sis  = cat["Seguridad funcional (SIS/ESD/F&G)"]
print(f"\n=== RESULTADO ===")
print(f"  CONTROL DE PROCESO (donde compite SUPCON): US${ctrl/1e6:,.1f}M — {len(importadores_ctrl):,} importadores")
print(f"  Distribución eléctrica (no es nuestro rubro): US${elec/1e6:,.1f}M — {len(importadores_elec):,} importadores")
print(f"  Seguridad funcional (SIS/ESD/F&G): US${sis/1e6:,.1f}M")
print(f"  Ruido restado: US${ruido_tot/1e6:,.1f}M")

print(f"\n=== marcas de CONTROL más grandes ===")
for m,v in marcas_ctrl.most_common(15):
    if m: print(f"  {m[:30]:32s} US${v/1e6:>6,.2f}M")
print(f"\n=== marcas de DISTRIBUCIÓN ELÉCTRICA más grandes ===")
for m,v in marcas_elec.most_common(12):
    if m: print(f"  {m[:30]:32s} US${v/1e6:>6,.2f}M")
print(f"\n=== origen del control de proceso ===")
for p,v in paises_ctrl.most_common(8):
    print(f"  {PAIS.get(p,'cód. '+p):18s} US${v/1e6:>6,.2f}M")

json.dump({
 "partidas":"85371000, 85371010, 85371090, 85372000, 85372010, 85372090, 85381000, 85389000",
 "total_partidas_usd":round(total,2),
 "control_proceso_usd":round(ctrl,2),"control_proceso_importadores":len(importadores_ctrl),
 "distribucion_electrica_usd":round(elec,2),"distribucion_electrica_importadores":len(importadores_elec),
 "seguridad_funcional_usd":round(sis,2),"ruido_restado_usd":round(ruido_tot,2),
 "por_categoria":{k:{"usd":round(v,2),"items":cat_items[k],
   "por_partida":[[a,round(b,2)] for a,b in por_partida_cat[k].most_common()]} for k,v in cat.items()},
 "marcas_control":[[m,round(v,2)] for m,v in marcas_ctrl.most_common(25) if m],
 "marcas_electrico":[[m,round(v,2)] for m,v in marcas_elec.most_common(20) if m],
 "origen_control":[[PAIS.get(p,"cód. "+p),round(v,2)] for p,v in paises_ctrl.most_common(10)],
 "nota":("No existe partida arancelaria de DCS: un DCS entra como 'tablero con aparato eléctrico "
   "de control' (85371000), igual que un tablero de distribución. La separación se hace por glosa "
   "y marca. Las partidas 8537-8538 mezclan control de proceso con distribución eléctrica: la "
   "distribución NO es el rubro de SUPCON y se reporta aparte para no inflar su mercado."),
}, open(os.path.join(D,"mercado_dcs_sistemas.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/mercado_dcs_sistemas.json")
