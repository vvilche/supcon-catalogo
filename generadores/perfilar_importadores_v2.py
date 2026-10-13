#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PERFILES DE IMPORTADOR v2 — enfoque corregido.

CORRECCION v1 -> v2: la v1 perfilaba al importador usando SOLO las lineas que matcheaban
el filtro (partida del dominio + marca del rubro). Pero un distribuidor grande importa
mezclado: un item de instrumentacion entre cientos de otros. Con ese filtro su volumen
real quedaba invisible y TODOS parecian "compra puntual" (75% en un solo balde).

v2 hace dos pasos en una pasada:
  PASO 1: perfila la OPERACION COMPLETA de cada importador (todas sus partidas, todo su CIF).
  PASO 2: mide, dentro de esa operacion, cuanto y que es de instrumentacion/automatizacion.
Asi se distingue el ESPECIALISTA (casi todo su volumen es del rubro) del IMPORTADOR GRANDE
multirrubro, que es la distincion comercialmente util.

Dato verificado: el NUM_UNICO_IMPORTADOR es estable por empresa (16.240 IDs en el anio;
4.720 aparecen los 12 meses). Aduanas omite nombre y RUT por Ley 20.285.

Salida: datos/perfiles_importador_2025.json
"""
import os, glob, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

COL_IMP, COL_COMUNA = 6, 5
COL_ARANC, COL_CIF, COL_NOMBRE, COL_MARCA = 157, 158, 133, 134
COL_PAIS, COL_FECHA = 21, 4

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

FAMILIAS = {
 "Instrumentación (presión/temp/caudal/nivel)": ["90262010","90262019","90262090","90269000",
    "90251100","90251900","90258010","90258090","90259000","90261010","90261090","90268010","90268090"],
 "Analizadores de proceso": ["90271010","90271090","90272000","90273000","90275000","90278100","90278999","90279090"],
 "Válvulas de control": ["84811000","84812010","84812020","84813000","84814000","84818010","84818090","84819000"],
 "Control / DCS / PLC / SIS": ["85371000","85371010","85371090","85372000","85372010","85372090","85381000","85389000"],
 "Medición eléctrica y protecciones": ["90301000","90302000","90303100","90303200","90303300","90303900",
    "90304000","90308200","90308400","90308900","90283000","90283010","90283090"],
 "Redes OT": ["85176210","85176220","85176290","85176900","85177000"],
 "Fuentes y convertidores": ["85043100","85043200","85043300","85044000","85045000","85049000"],
}
P2FAM = {}
for fam, l in FAMILIAS.items():
    for p in l: P2FAM[p] = fam

RUBRO_CAP = {
 "84":"Maquinaria mecánica","85":"Eléctrico / electrónico","90":"Instrumentos de medida",
 "87":"Vehículos y automoción","39":"Plásticos","73":"Manufacturas de acero","76":"Aluminio",
 "28":"Química inorgánica","29":"Química orgánica","38":"Productos químicos","72":"Acero",
 "26":"Minerales","27":"Combustibles","62":"Vestuario","61":"Vestuario","64":"Calzado",
 "94":"Muebles","48":"Papel","40":"Caucho","74":"Cobre","30":"Farmacéutico","33":"Cosméticos",
 "22":"Bebidas","32":"Pinturas","25":"Minerales no metálicos","19":"Cereales","20":"Frutas y hortalizas",
}

MARCAS_RUBRO = ["ENDRESS","KROHNE","MICRO MOTION","FLEXIM","CIDRA","ROSEMOUNT","YOKOGAWA","HONEYWELL",
 "ABB","SIEMENS","SCHNEIDER","EMERSON","METSO","VALMET","FUJI","AZBIL","MITSUBISHI","OMRON",
 "PHOENIX","TURCK","IFM","SICK","BALLUFF","BAUMER","LEUZE","KEYENCE","WIKA","ASHCROFT","DANFOSS",
 "SAMSON","MASONEILAN","FISHER","VALVITALIA","BRAY","NELES","VELAN","CIRCOR","KITZ","ROTORK","AUMA",
 "MTS","AMETEK","MAGNETROL","VEGA","PEPPERL","TESTO","DRAGER","MSA","SERVOMEX","THERMO","AGILENT",
 "SHIMADZU","BRUKER","HACH","WTW","XYLEM","YSI","BARTEC","STAHL","SEL","HITACHI","HYOSUNG","ALSTOM",
 "ETP","ARTECHE","PFIFFNER","TELEDYNE","QUALITROL","DOBLE","OMICRON","MEGGER","FLUKE","WATERS",
 "PERKIN","LECO","BUCHI","KNAUER","ANALYTIK","BECKHOFF","WAGO","ROCKWELL","ALLEN","FESTO","SMC",
 "PILZ","RITTAL","WEIDMULLER","LUTZE","FANUC","YASKAWA","SEW","LENZE","VACON","INNOMOTICS","WEG",
 "HIRSCHMANN","BELDEN","MOXA","ADVANTECH","DIGI","LANTRONIX","PERLE","KYLAND","GENERAL ELECTRIC"]

def norm_marca(m):
    x = (m or "").upper().replace("-F","").split("~")[0].strip()
    for c in MARCAS_RUBRO:
        if x == c or x.startswith(c+" ") or x.startswith(c+"-") or c in x: return c
    return None

EXCLUIR = ["PARTE","ACCESORIO","REPUESTO","ESTUCHE","AUTOMOVIL","VEHICULO","CAMION","TRACTOR",
 "TELEFONO","CELULAR","TABLET","NOTEBOOK","LAPTOP","IMPRESORA","TELEVISOR","AUDIFONO","JUGUETE",
 "ELECTRODOMESTICO","MEDICAMENTO","REACTIVO","DIAGNOSTICO","IN VITRO"]
def desc_ok(n):
    n=(n or "").upper(); return not any(x in n for x in EXCLUIR)

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}")

imp = collections.defaultdict(lambda: {
    "total":0.0,"items":0,"rubro":collections.Counter(),"meses":set(),
    "instru":0.0,"instru_items":0,"familias":collections.Counter(),
    "marcas":collections.Counter(),"paises":collections.Counter(),"comunas":collections.Counter()})

for f in archivos:
    with open(f, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= COL_CIF: continue
            k = (c[COL_IMP] or "").strip()
            if not k: continue
            cif = num(c[COL_CIF])
            if cif <= 0: continue
            p8 = (c[COL_ARANC] or "").strip()[:8]
            nombre = c[COL_NOMBRE] or ""
            d = imp[k]
            d["total"] += cif; d["items"] += 1
            cap = p8[:2] if len(p8) >= 2 else "?"
            d["rubro"][RUBRO_CAP.get(cap,"Otros")] += cif
            d["comunas"][(c[COL_COMUNA] or "").strip()] += cif
            # FECVENCI viene como DDMMAAAA (ej. 17042025 = 17-abr-2025). Verificado
            # contra el registro: el prefijo varia 01..30 (dia) y el sufijo siempre 2025.
            fe = (c[COL_FECHA] or "").strip()
            if len(fe) == 8 and fe.isdigit() and fe[4:8] == "2025":
                dd, mm = int(fe[0:2]), int(fe[2:4])
                if 1 <= dd <= 31 and 1 <= mm <= 12:
                    d["meses"].add(f"2025-{mm:02d}")
            fam = P2FAM.get(p8)
            if not fam or not desc_ok(nombre): continue
            marca = norm_marca(c[COL_MARCA])
            if not marca: continue
            d["instru"] += cif; d["instru_items"] += 1
            d["familias"][fam] += cif
            d["marcas"][marca] += cif
            d["paises"][(c[COL_PAIS] or "").strip()] += cif

tot_mercado = sum(d["total"] for d in imp.values())
tot_instru = sum(d["instru"] for d in imp.values())
print(f"importadores: {len(imp):,}")
print(f"total importado (todos los rubros): US${tot_mercado/1e6:,.0f}M")
print(f"de instrumentación/automatización  : US${tot_instru/1e6:,.1f}M\n")

perfiles = []
for k, d in imp.items():
    if d["instru"] <= 0: continue
    share = d["instru"]/d["total"]*100
    fams = d["familias"].most_common()
    if share >= 70 and d["instru"] > 100000:
        tipo = "ESPECIALISTA en instrumentación"
    elif share >= 25:
        tipo = "INTEGRADOR / distribuidor técnico"
    elif d["instru"] > 100000:
        tipo = "IMPORTADOR GRANDE multirrubro"
    else:
        tipo = "COMPRA MENOR"
    perfiles.append({
      "id":k, "instru_usd":round(d["instru"],2), "total_usd":round(d["total"],2),
      "share_pct":round(share,1), "instru_items":d["instru_items"], "items_totales":d["items"],
      "tipo":tipo, "meses_activos":len(d["meses"]), "n_marcas":len(d["marcas"]),
      "fam_principal":fams[0][0] if fams else "", "familias":[(a,round(b,2)) for a,b in fams[:5]],
      "marcas":[m for m,_ in d["marcas"].most_common(8)],
      "paises":[p for p,_ in d["paises"].most_common(4)],
      "comuna":d["comunas"].most_common(1)[0][0] if d["comunas"] else "",
      "rubros":[r for r,_ in d["rubro"].most_common(3)],
    })
perfiles.sort(key=lambda x:-x["instru_usd"])

print("=== ARQUETIPO DEL IMPORTADOR (por valor de instrumentación) ===")
pt = collections.defaultdict(lambda: {"cif":0.0,"n":0})
for p in perfiles:
    pt[p["tipo"]]["cif"] += p["instru_usd"]; pt[p["tipo"]]["n"] += 1
for t,v in sorted(pt.items(), key=lambda x:-x[1]["cif"]):
    print(f"  {t:36s} {v['n']:>4} imp.  US${v['cif']/1e6:>7,.1f}M  ({v['cif']/tot_instru*100:.0f}%)")

print(f"\n=== TOP 15 POR VOLUMEN DE INSTRUMENTACIÓN ===")
for i,p in enumerate(perfiles[:15],1):
    print(f"\n{i:2d}. ID {p['id']:>7s}  US${p['instru_usd']/1e6:>6,.2f}M en instrumentación "
          f"({p['share_pct']}% de sus US${p['total_usd']/1e6:,.1f}M totales)")
    print(f"    {p['tipo']} | {p['meses_activos']}/12 meses | {p['instru_items']:,} items del rubro")
    print(f"    familia: {p['fam_principal']}  marcas: {', '.join(p['marcas'][:5])}")
    print(f"    otros rubros: {', '.join(p['rubros'][:3])}")

json.dump({"anio":2025,"n_importadores":len(imp),"total_importado_usd":round(tot_mercado,2),
  "total_instrumentacion_usd":round(tot_instru,2),
  "por_tipo":{k:{"n":v["n"],"cif":round(v["cif"],2)} for k,v in pt.items()},
  "perfiles":perfiles}, open(os.path.join(D,"perfiles_importador_2025.json"),"w"),
  ensure_ascii=False, indent=1)
print(f"\nguardado: datos/perfiles_importador_2025.json ({len(perfiles)} perfiles)")
