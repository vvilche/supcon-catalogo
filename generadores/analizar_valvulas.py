#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISIS DE MERCADO DE VÁLVULAS — Chile 2025, desde el registro crudo de Aduanas.

Por qué este análisis por separado: el cruce general agrupó las 8 partidas de válvulas en
un solo bloque de US$53,8M, y eso no dice nada útil para vender. Lo que sirve es el desglose
por TIPO de válvula, que es como el cliente y el fabricante hablan: bola, compuerta,
mariposa, globo, diafragma, seguridad, alivio, y sus partes.

Las partidas del capítulo 84.81 se distinguen por tipo de válvula en los subgrupos:
  848110 — válvulas reductoras de presión
  848120 — válvulas para transmisión oleohidráulica o neumática
  848130 — válvulas de retención (check)
  848140 — válvulas de seguridad o de alivio
  848180 — los demás artículos de grifería (bola, compuerta, mariposa, globo, diafragma)
  848190 — PARTES de válvulas
A su vez 848180 se abre en 10 (los demás), 20 (de bola), 30 (mariposa), 40 (compuerta...),
etc. Se usa el código de 8 dígitos completo para separarlas.

Salida: datos/mercado_valvulas_2025.json + estudio-mercado/valvulas_2025.html
"""
import os, glob, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

COL_ARANC, COL_CIF, COL_NOMBRE, COL_MARCA = 157, 158, 133, 134
COL_PAIS, COL_FOB, COL_IMP, COL_COMUNA = 21, 64, 6, 5

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

# ---------------------------------------------------------------------------
# TIPOS DE VÁLVULA por código de 8 dígitos del SA chileno
# ---------------------------------------------------------------------------
TIPOS = {
 "84811000": ("Válvulas reductoras de presión", "Regulación"),
 "84812010": ("Válvulas para transmisión oleohidráulica", "Potencia"),
 "84812020": ("Válvulas para transmisión neumática", "Potencia"),
 "84813000": ("Válvulas de retención (check)", "Corte"),
 "84814000": ("Válvulas de seguridad o alivio", "Seguridad"),
 "84818010": ("Válvulas de bola", "Control/Corte"),
 "84818020": ("Válvulas de mariposa", "Control/Corte"),
 "84818030": ("Válvulas de compuerta, globo y similares (acero)", "Control/Corte"),
 "84818040": ("Válvulas de compuerta, globo y similares (otros materiales)", "Control/Corte"),
 "84818050": ("Válvulas de diafragma", "Control/Corte"),
 "84818060": ("Válvulas de macho o tapón", "Control/Corte"),
 "84818090": ("Los demás artículos de grifería", "Otros"),
 "84819000": ("Partes de válvulas", "Partes"),
}

# Marcas del rubro de válvulas y control de fluidos, para no contar ruido de otro rubro
MARCAS = ["BRAY","VALMET","VALVITALIA","DANFOSS","METSO","EMERSON","FISHER","SAMSON","NELES",
 "GENEBRE","SIEMENS","FESTO","SMC","SAUER","FLOWSERVE","VELAN","CIRCOR","KITZ","CRANE",
 "CAMERON","PETROL","VELAN","HABONIM","JC VALVES","TYCO","PENTAIR","XOMOX","ARGUS","PERRIN",
 "BELGIC","BONOMI","CIRCOR","DELTA","DUPLOMATIC","PARKER","BOSCH REXROTH","HYDAC","ARGO",
 "WATTS","SPENCE","LESLIE","CLA-VAL","BERMAD","OCV","DOROT","SOCIEDAD","TALIS","EBRO",
 "INTERAPP","GEMU","BURKERT","ASCO","SIRAI","SIRGA","KEYSTONE","VANESSA","BRAY","TYCO",
 "DRESSER","CONSOLIDATED","ANDERSON","GREENWOOD","FARRIS","BROADY","AVK","HAWLE","M&H",
 "STAFSJO","AMRI","KSB","PFEIFFER","ZIKESCH","GEFA","ZVA","ROTORK","AUMA","BETTIS","LIMITORQUE"]

EXCLUIR = ["PARTE DE MOTOR","AUTOMOVIL","VEHICULO","CAMION","TRACTOR","NEUMATICO","LLANTA",
 "REPUESTO PARA","ELECTRODOMESTICO","LAVADORA","REFRIGERADOR","BOMBA DE AGUA PARA MOTOR"]

def desc_ok(n):
    n=(n or "").upper()
    return not any(x in n for x in EXCLUIR)

def marca_ok(m):
    x = (m or "").upper().replace("-F","").split("~")[0].strip()
    if not x: return None
    for c in MARCAS:
        if x == c or x.startswith(c+" ") or x.startswith(c+"-") or c in x:
            return c
    return None

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}")
print("Analizando el capítulo 84.81 (válvulas) completo...\n")

por_tipo = collections.defaultdict(lambda: {"cif":0.0,"items":0,"marcas":collections.Counter(),
                                            "paises":collections.Counter()})
por_marca = collections.Counter()
por_pais = collections.Counter()
por_tipo_marca = collections.defaultdict(collections.Counter)
total = 0.0; total_items = 0
sin_marca = 0.0
importadores_valv = collections.Counter()

for f in archivos:
    with open(f, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= COL_CIF: continue
            p8 = (c[COL_ARANC] or "").strip()[:8]
            if not p8.startswith("8481"): continue
            nombre = c[COL_NOMBRE] or ""
            if not desc_ok(nombre): continue
            cif = num(c[COL_CIF])
            if cif <= 0: continue
            total += cif; total_items += 1
            tipo = TIPOS.get(p8, (f"Partida {p8} (otros)", "Otros"))[0]
            m = marca_ok(c[COL_MARCA])
            d = por_tipo[tipo]
            d["cif"] += cif; d["items"] += 1
            if m:
                d["marcas"][m] += cif
                por_marca[m] += cif
                por_tipo_marca[tipo][m] += cif
            else:
                sin_marca += cif
            pais = (c[COL_PAIS] or "").strip()
            d["paises"][pais] += cif
            por_pais[pais] += cif
            k = (c[COL_IMP] or "").strip()
            if k and m: importadores_valv[k] += cif

print(f"TOTAL capítulo 84.81: US${total:,.0f} en {total_items:,} ítems")
print(f"Sin marca identificable: US${sin_marca:,.0f} ({sin_marca/total*100:.0f}%)\n")

print("=== MERCADO POR TIPO DE VÁLVULA ===")
for tipo, d in sorted(por_tipo.items(), key=lambda x:-x[1]["cif"]):
    print(f"\n{tipo:52s} US${d['cif']/1e6:>7,.1f}M  ({d['items']:>6,} ítems)")
    for m,v in d["marcas"].most_common(6):
        print(f"      {m[:28]:30s} US${v/1e6:>6.2f}M")

print("\n=== TOP 15 MARCAS DEL RUBRO ===")
for m,v in por_marca.most_common(15):
    print(f"  {m[:30]:32s} US${v/1e6:>7,.2f}M")

PAIS = {"225":"Francia","336":"Alemania","512":"Italia","504":"EE.UU.","563":"China",
 "317":"Corea del Sur","517":"Singapur","507":"Japón","331":"Brasil","528":"Países Bajos",
 "511":"Canadá","510":"Taiwán","220":"España","226":"Reino Unido","549":"India"}
print("\n=== TOP 10 ORÍGENES ===")
for p,v in por_pais.most_common(10):
    print(f"  {PAIS.get(p,'cód. '+p):18s} US${v/1e6:>7,.2f}M")

print(f"\nimportadores distintos con marca del rubro: {len(importadores_valv):,}")

json.dump({
 "anio":2025,
 "capitulo":"84.81 válvulas y artículos similares",
 "total_usd":round(total,2), "total_items":total_items,
 "sin_marca_usd":round(sin_marca,2),
 "por_tipo":{k:{"usd":round(v["cif"],2),"items":v["items"],
   "marcas":[[m,round(x,2)] for m,x in v["marcas"].most_common(15)],
   "paises":[[p,round(x,2)] for p,x in v["paises"].most_common(5)]} for k,v in por_tipo.items()},
 "por_marca":[[m,round(v,2)] for m,v in por_marca.most_common(40)],
 "por_pais":[[p,round(v,2)] for p,v in por_pais.most_common(20)],
 "n_importadores":len(importadores_valv),
}, open(os.path.join(D,"mercado_valvulas_2025.json"),"w"), ensure_ascii=False, indent=1)
print("\nguardado: datos/mercado_valvulas_2025.json")
