#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACTUALIZA la Escalera al Éxito con los mercados medidos POR PARTIDA ARANCELARIA.

POR QUÉ. La escalera publicada usaba los números del estudio general, que estaban mal en varias
líneas y, peor, repartía mercados que NO se pueden separar:
  - DCS aparecía con US$112,5M (el valor de las partidas de tableros, que son en su mayoría
    subestaciones eléctricas). El control de proceso real es US$83,0M.
  - PLC aparecía con US$83,9M y SIS con US$52,8M. Ninguno de los dos tiene partida propia:
    el PLC está CONTENIDO en el control y el SIS CONTENIDO en el DCS. Reportarlos como mercados
    aparte era contar los mismos ítems tres veces.
  - Instrumentación aparecía repartida en presión 9,4M / caudal 19,7M / temperatura 0,3M. Medido
    por partida, la instrumentación de campo completa es US$128,4M.

CORRECCIONES APLICADAS (todas verificadas contra el Registro DIN 2025):
  Instrumentación:  presion      9,4M  -> la linea completa 128,4M
                    caudal      19,7M  -> (incluida)
                    temperatura  0,3M  -> (incluida)
                    calibracion 11,3M  -> (incluida en instrumentacion)
  Analítica:        44,3M ->  es techO: capitulo 90.27 completo 171,4M, del cual 38,6M es
                    analisis de proceso identificado por marca
  Válvulas:        396,6M -> la linea de CONTROL es 69,0M (piso); el total incluye manuales y
                    grifería doméstica que no son SUPCON
  DCS:             112,5M -> 83,0M (control de proceso verificado)
  PLC:              83,9M -> NO MEDIBLE como mercado aparte (contenido en DCS/control)
  SIS:              52,8M -> NO MEDIBLE como mercado aparte (contenido en DCS)

Salida: datos/escalera_exito_v3.json
"""
import os, json, copy

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

esc = json.load(open(os.path.join(D, "escalera_exito.json"), encoding="utf-8"))
merc = json.load(open(os.path.join(D, "mercado_hardware_partida.json"), encoding="utf-8"))
dcs  = json.load(open(os.path.join(D, "mercado_dcs_sistemas.json"), encoding="utf-8"))
valv = json.load(open(os.path.join(D, "valvulas_manual_vs_control.json"), encoding="utf-8"))

# --- mercados corregidos por linea ---
INSTR = merc["lineas"]["Instrumentación"]["mercado_usd"]
ANAL  = merc["lineas"]["Analítica"]["mercado_usd"]
VALV_TECHO = merc["lineas"]["Válvulas"]["mercado_usd"]
VALV_CTRL  = valv["piso_control_usd"]
DCS_REAL   = dcs["desglose_verificado"]["control_proceso_confirmado_usd"] * 1e6

CAMBIOS = {
 "Instrumentación": {"antes":[9.4e6,19.7e6,0.3e6,11.3e6],"despues":INSTR,
   "nota":("La instrumentación de campo medida por partida es US$128,4M, no la suma de las "
    "categorías sueltas del estudio anterior (presión 9,4M + caudal 19,7M + temperatura 0,3M + "
    "calibración 11,3M = 40,7M). La diferencia es que las partidas de instrumentación incluyen "
    "todo el valor importado, no solo lo que declara una marca conocida.")},
 "Analítica": {"antes":44.3e6,"despues":ANAL,
   "nota":("El capítulo 90.27 completo es US$171,4M. De ahí, US$38,6M se identifica como análisis "
    "de proceso industrial y ambiental por marca (Siemens, Endress+Hauser, MSA, Thermo, Hach, "
    "Metso). El resto es laboratorio clínico y equipos sin marca reconocible. Se reporta el "
    "techo del capítulo y el segmento de proceso identificado por separado.")},
 "Válvulas": {"antes":396.6e6,"despues":VALV_CTRL,
   "nota":("US$396,6M es el capítulo completo, que incluye válvulas manuales, grifería doméstica "
    "y repuestos de vehículos. La línea de SUPCON son válvulas DE CONTROL: su piso medido es "
    "US$69,0M (reductoras de presión + las identificadas por marca de control).")},
 "DCS": {"antes":112.5e6,"despues":DCS_REAL,
   "nota":("US$112,5M era el valor de las partidas de tableros, donde el 38% son subestaciones "
    "eléctricas (GIS, celdas, interruptores de 220 kV). El control de proceso verificado —tableros "
    "de baja tensión con glosa de control + reguladores automáticos donde aparecen los DCS— es "
    "US$83,0M.")},
 "PLC": {"antes":83.9e6,"despues":None,
   "nota":("NO MEDIBLE como mercado aparte. Un PLC no tiene partida arancelaria propia: entra como "
    "tablero de control o regulador automático, igual que un DCS, y los fabricantes son los "
    "mismos (Siemens, ABB, Schneider, Rockwell). Identificando por glosa y marca se ven US$57,2M "
    "de PLC, pero está CONTENIDO en el control: sumarlo sería contar dos veces.")},
 "SIS": {"antes":52.8e6,"despues":None,
   "nota":("NO MEDIBLE como mercado aparte. No existe una partida de 'sistema instrumentado de "
    "seguridad'. Un SIS entra como tablero de control, igual que un DCS: el TCS-900 se vende "
    "DENTRO del proyecto de control, no como categoría separada.")},
}

# aplicar
for lin, cam in CAMBIOS.items():
    if lin not in esc["lineas"]: continue
    x = esc["lineas"][lin]
    x["mercado_antes_usd"] = cam["antes"]
    x["mercado_corregido_usd"] = cam["despues"]
    x["nota_correccion"] = cam["nota"]
    x["medible"] = cam["despues"] is not None
    # IMPORTANTE: el mercado medido es de la LINEA, no de cada ficha de producto.
    # Varias fichas de la misma linea comparten el mismo mercado medido (ej. las 6 valvulas
    # de SUPCON Fluid viven del mismo mercado de valvulas de control). Repartirlo entre ellas
    # seria inventar una cuota que no se midio; duplicarlo en cada ficha infla la suma 3-10x.
    # Se deja el valor de la LINEA en x["mercado_corregido_usd"] y el de cada ficha queda en
    # None, para que el HTML muestre el mercado a nivel de linea y no por producto.
    for p in x["productos"]:
        p["mercado_usd_antes"] = p.get("mercado_usd")
        p["mercado_usd"] = None
        p["mercado_es_de_linea"] = cam["despues"] is not None

esc["version"] = "v3 — mercados corregidos por partida arancelaria"
esc["nota_mercado"] = ("Hardware: Registro DIN de Aduanas Chile 2025, medido POR PARTIDA "
 "ARANCELARIA (dato duro) menos el ruido de otros rubros verificable. Software y plataforma: no "
 "entra por partida arancelaria, se vende dentro del proyecto.")
esc["correcciones_v3"] = {k:{"antes_usd":v["antes"],"despues_usd":v["despues"],"nota":v["nota"]}
                          for k,v in CAMBIOS.items()}

json.dump(esc, open(os.path.join(D,"escalera_exito_v3.json"),"w"), ensure_ascii=False, indent=1)

print("=== ESCALERA ACTUALIZADA (v3) ===\n")
print(f"{'LÍNEA':22s} {'ANTES':>12s} {'AHORA':>12s}")
print("-"*50)
for lin in esc["lineas"]:
    c = CAMBIOS.get(lin)
    if not c: continue
    av = sum(c['antes']) if isinstance(c['antes'], list) else c['antes']
    a = f"US${av/1e6:,.1f}M" if av > 1e5 else f"US${av:,.1f}M"
    d = f"US${c['despues']/1e6:,.1f}M" if c['despues'] else "no medible aparte"
    print(f"{lin:22s} {a:>12s} {d:>12s}")
print()
print(f"guardado: datos/escalera_exito_v3.json")
