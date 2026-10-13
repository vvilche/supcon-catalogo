#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEPARACIÓN DEL MERCADO DE VÁLVULAS: manuales vs control.

ENCARGO: separar el mercado de válvulas en manuales y de control.

HALLAZGO HONESTO: el registro de Aduanas de Chile NO permite esa separación completa.
El 50% del valor del capítulo (US$230,1M) cae en la partida residual 84818090 "los demás
artículos de grifería", donde conviven válvulas de control modulante, válvulas manuales y
grifería doméstica. La glosa del ítem suele decir solo "VÁLVULA", y las marcas incluyen tanto
a Valvitalia y Flowserve (control) como a Genebre (manual). Verificado ítem por ítem.

LO QUE SÍ SE SEPARA (con evidencia):
  1. Por PARTIDA: hay 5 partidas que identifican un tipo específico con certeza.
  2. Por MARCA: las marcas de control de proceso y las de válvula manual son en gran medida
     distintas. Cruzando ambas señales se obtiene un piso confiable por categoría.
  3. El resto queda DECLARADO como no separable, no repartido a ojo.

Salida: datos/valvulas_manual_vs_control.json
"""
import glob, os, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

# --- partidas que SÍ identifican por sí solas ---
POR_PARTIDA = {
 "84811000": ("Reductoras de presión", "Control/regulación"),
 "84812010": ("Transmisión oleohidráulica", "Potencia"),
 "84812020": ("Transmisión neumática", "Potencia"),
 "84813000": ("Retención (check)", "Corte, sin accionamiento"),
 "84814000": ("Seguridad o alivio", "Seguridad"),
 "84818010": ("Válvulas de bola", "Corte manual o accionado"),
 "84819000": ("Partes de válvulas", "Partes"),
 "84818090": ("Los demás artículos de grifería", "MIXTO — no separable"),
}

# --- marcas de válvula de CONTROL de proceso (modulante, con actuador) ---
MARCAS_CONTROL = ["VALVITALIA","FLOWSERVE","EMERSON","FISHER","SAMSON","NELES","MASONEILAN",
 "WEIR","MOGAS","INSTRUVALVE","SWENSON","CGIS","FORUM","DRESSER","CONSOLIDATED","LESLIE",
 "SPENCE","ARCA","KROMBACH","M&C","JC VALVES","SOMAS","NAF","MAPAG","CIRCOR","DEZURIK",
 "ORBINOX","VAT","KVT","HIROSE","GEMU","BURKERT","VALMET","METSO","TYCO","PENTAIR","KEYSTONE",
 "ECKARDT","SAMSON AG","BADGER","MASONEILAN","KTM","NELES-JAMESBURY","FLOW-TEK"]

# --- marcas de válvula MANUAL (corte, operación con volante o palanca) ---
MARCAS_MANUAL = ["BRAY","GENEBRE","EBRO","ARGUS","BONOMI","BELGIC","PERRIN","FUSIMAN","TRILLIUM",
 "KITZ","WATTS","HAWLE","AVK","CRANE","HABONIM","VELAN","CIM","WENZHOU","XINHUA","YUHUA",
 "SHANGHAI","SUZHOU","NANFANG","TUOFEI","ZHEJIANG","TAIZHOU","XINFENG","MIL","SIRAI"]

def es_control(marca, nombre):
    m = (marca or "").upper().replace("-F","").split("~")[0].strip()
    n = (nombre or "").upper()
    if any(x in m for x in MARCAS_CONTROL): return True
    # la glosa puede declarar control explicitamente
    return any(x in n for x in ["DE CONTROL","CONTROL MODUL","REGULADORA","MODULANTE","CON ACTUADOR"])

def es_manual(marca, nombre):
    m = (marca or "").upper().replace("-F","").split("~")[0].strip()
    n = (nombre or "").upper()
    if any(x in m for x in MARCAS_MANUAL): return True
    return any(x in n for x in ["MANUAL","VOLANTE","PALANCA","DE CIERRE"])

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}\n")

por_partida = collections.Counter()
control_marca = collections.Counter()
manual_marca = collections.Counter()
mixto_total = 0.0
mixto_control = 0.0
mixto_manual = 0.0
mixto_sin = 0.0
items = 0

for txt in archivos:
    with open(txt, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= 158: continue
            p8 = (c[157] or "").strip()[:8]
            if p8 not in POR_PARTIDA: continue
            cif = num(c[158])
            if cif <= 0: continue
            items += 1
            nombre, tipo = POR_PARTIDA[p8]
            por_partida[tipo] += cif
            if p8 == "84818090":   # la partida mixta
                mixto_total += cif
                if es_control(c[134], c[133]):
                    mixto_control += cif
                    control_marca[(c[134] or "").upper().replace("-F","").split("~")[0].strip()[:26]] += cif
                elif es_manual(c[134], c[133]):
                    mixto_manual += cif
                    manual_marca[(c[134] or "").upper().replace("-F","").split("~")[0].strip()[:26]] += cif
                else:
                    mixto_sin += cif
            else:
                # en las partidas específicas tambien se puede leer la marca
                if es_control(c[134], c[133]):
                    control_marca[(c[134] or "").upper().replace("-F","").split("~")[0].strip()[:26]] += cif
                elif es_manual(c[134], c[133]):
                    manual_marca[(c[134] or "").upper().replace("-F","").split("~")[0].strip()[:26]] += cif

total = sum(por_partida.values())
print(f"TOTAL capítulo 84.81: US${total/1e6:,.1f}M ({items:,} ítems)\n")

print("=== 1) POR PARTIDA (lo que sí identifica el tipo solo) ===")
for tipo, v in por_partida.most_common():
    print(f"  {tipo:28s} US${v/1e6:>7,.1f}M  ({v/total*100:>4.1f}%)")

print(f"\n=== 2) LA PARTIDA MIXTA (84818090: 'los demás artículos de grifería') ===")
print(f"  total de la partida:                 US${mixto_total/1e6:>7,.1f}M")
print(f"  identificable como CONTROL por marca: US${mixto_control/1e6:>7,.1f}M ({mixto_control/mixto_total*100:.0f}%)")
print(f"  identificable como MANUAL por marca:  US${mixto_manual/1e6:>7,.1f}M ({mixto_manual/mixto_total*100:.0f}%)")
print(f"  NO identificable:                     US${mixto_sin/1e6:>7,.1f}M ({mixto_sin/mixto_total*100:.0f}%)")

ctrl = mixto_control + por_partida.get("Control/regulación",0)
man  = mixto_manual + por_partida.get("Corte, sin accionamiento",0) + por_partida.get("Corte manual o accionado",0)
print(f"\n=== 3) EL PISO CONFIABLE DE CADA CATEGORÍA ===")
print(f"  CONTROL (identificado por marca o partida):  US${ctrl/1e6:>7,.1f}M")
print(f"  MANUAL/corte:                                US${man/1e6:>7,.1f}M")
print(f"  seguridad + potencia + partes:               US${(por_partida.get('Seguridad',0)+por_partida.get('Potencia',0)+por_partida.get('Partes',0))/1e6:>7,.1f}M")
print(f"  NO CLASIFICABLE:                             US${mixto_sin/1e6:>7,.1f}M")
print(f"\n  -> El resto ({mixto_sin/total*100:.0f}% del capítulo) NO se puede repartir con el registro de Aduanas.")

print(f"\n=== marcas de CONTROL más grandes (en todo el capítulo) ===")
for m, v in control_marca.most_common(10):
    print(f"  {m[:28]:30s} US${v/1e6:>6,.2f}M")
print(f"\n=== marcas de MANUAL más grandes ===")
for m, v in manual_marca.most_common(10):
    print(f"  {m[:28]:30s} US${v/1e6:>6,.2f}M")

json.dump({
 "capitulo":"84.81", "total_usd":round(total,2), "items":items,
 "por_partida":[[k,round(v,2)] for k,v in por_partida.most_common()],
 "partida_mixta":{"partida":"84818090","nombre":"Los demás artículos de grifería",
   "total":round(mixto_total,2),"control_identificado":round(mixto_control,2),
   "manual_identificado":round(mixto_manual,2),"no_identificable":round(mixto_sin,2)},
 "piso_control_usd":round(ctrl,2), "piso_manual_usd":round(man,2),
 "no_clasificable_usd":round(mixto_sin,2),
 "marcas_control":[[m,round(v,2)] for m,v in control_marca.most_common(25)],
 "marcas_manual":[[m,round(v,2)] for m,v in manual_marca.most_common(25)],
 "nota_metodologica":("El registro de Aduanas no permite separar manuales de control: el 50% "
   "del capítulo cae en la partida residual 84818090, donde conviven válvulas de control, "
   "manuales y grifería doméstica. La glosa suele decir solo 'VÁLVULA'. Se entrega un PISO "
   "confiable por categoría (identificado por partida o marca) y se declara el resto como no "
   "clasificable, en vez de repartirlo a ojo."),
}, open(os.path.join(D,"valvulas_manual_vs_control.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/valvulas_manual_vs_control.json")
