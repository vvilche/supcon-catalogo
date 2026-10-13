#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PERFILES DE IMPORTADOR de instrumentacion y automatizacion en Chile 2025.

El registro DIN de Aduanas NO trae nombre ni RUT del importador (lo omite por Ley 20.285),
pero SI trae NUM_UNICO_IMPORTADOR: un correlativo estable. Eso permite perfilar a cada
importador sin identificarlo: cuanto mueve, en que familias, que marcas trae, de que paises,
si es recurrente o compro una vez.

Salida: datos/perfiles_importador_2025.json
"""
import os, glob, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

COL_IMP = 6      # NUM_UNICO_IMPORTADOR
COL_COMUNA = 5   # CODCOMUN (comuna de la direccion del importador)
COL_ARANC, COL_CIF, COL_NOMBRE, COL_MARCA = 157, 158, 133, 134
COL_PAIS, COL_PAIS_ADQ, COL_FOB = 21, 22, 64
COL_FECHA = 4

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

# familias del catalogo SUPCON -> partidas
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

MARCAS_RUBRO = ["ENDRESS","KROHNE","MICRO MOTION","FLEXIM","CIDRA","ROSEMOUNT","YOKOGAWA","HONEYWELL",
 "ABB","SIEMENS","SCHNEIDER","EMERSON","METSO","VALMET","FUJI","AZBIL","MITSUBISHI","OMRON",
 "PHOENIX","TURCK","IFM","SICK","BALLUFF","BAUMER","LEUZE","KEYENCE","WIKA","ASHCROFT","DANFOSS",
 "SAMSON","MASONEILAN","FISHER","VALVITALIA","BRAY","NELES","VELAN","CIRCOR","KITZ","ROTORK","AUMA",
 "MTS","AMETEK","MAGNETROL","VEGA","PEPPERL","TESTO","DRAGER","MSA","SERVOMEX","THERMO","AGILENT",
 "SHIMADZU","BRUKER","HACH","WTW","XYLEM","YSI","BARTEC","STAHL","SEL","HITACHI","HYOSUNG","ALSTOM",
 "ETP","ARTECHE","PFIFFNER","TELEDYNE","QUALITROL","DOBLE","OMICRON","MEGGER","FLUKE","WATERS",
 "PERKIN","LECO","BUCHI","KNAUER","ANALYTIK","BECKHOFF","WAGO","ROCKWELL","ALLEN","FESTO","SMC",
 "PILZ","RITTAL","WEIDMULLER","LUTZE","FANUC","YASKAWA","SEW","LENZE","VACON","INNOMOTICS","WEG",
 "HIRSCHMANN","BELDEN","MOXA","ADVANTECH","DIGI","LANTRONIX","PERLE","KYLAND","GE ","GENERAL ELECTRIC",
 "SCHWEITZER","WINTERS","DEUTZ","CUMMINS","KOMATSU"]

def norm_marca(m):
    x = (m or "").upper().replace("-F","").split("~")[0].strip()
    for c in MARCAS_RUBRO:
        if x == c.strip() or x.startswith(c.strip()+" ") or x.startswith(c.strip()+"-") or c.strip() in x:
            return c.strip()
    return None

EXCLUIR = ["PARTE","ACCESORIO","REPUESTO","ESTUCHE","AUTOMOVIL","VEHICULO","CAMION","TRACTOR",
 "TELEFONO","CELULAR","TABLET","NOTEBOOK","LAPTOP","IMPRESORA","TELEVISOR","AUDIFONO","JUGUETE",
 "ELECTRODOMESTICO","MEDICAMENTO","REACTIVO","DIAGNOSTICO","IN VITRO","ROPA","POLERA","CAMISA"]

def desc_ok(n):
    n = (n or "").upper()
    return not any(x in n for x in EXCLUIR)

archivos = sorted(glob.glob(os.path.join(RAW, "*.txt")))
print(f"archivos: {len(archivos)}")

# perfil por importador
imp = collections.defaultdict(lambda: {
    "cif":0.0, "items":0, "meses":set(), "familias":collections.Counter(),
    "marcas":collections.Counter(), "paises":collections.Counter(), "comunas":collections.Counter(),
    "primera":None, "ultima":None})

for f in archivos:
    with open(f, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= COL_CIF: continue
            p8 = (c[COL_ARANC] or "").strip()[:8]
            fam = P2FAM.get(p8)
            if not fam: continue
            nombre = c[COL_NOMBRE] or ""
            if not desc_ok(nombre): continue
            marca = norm_marca(c[COL_MARCA])
            if not marca: continue
            cif = num(c[COL_CIF])
            if cif <= 0: continue
            k = (c[COL_IMP] or "").strip()
            if not k: continue
            d = imp[k]
            d["cif"] += cif; d["items"] += 1
            d["familias"][fam] += cif
            d["marcas"][marca] += cif
            d["paises"][(c[COL_PAIS] or "").strip()] += cif
            d["comunas"][(c[COL_COMUNA] or "").strip()] += cif
            fe = (c[COL_FECHA] or "").strip()
            if len(fe) == 8 and fe[:2].isdigit() and fe[2:4].isdigit() and fe[4:8].isdigit():
                mm, dd = int(fe[2:4]), int(fe[:2])
                if not (1 <= mm <= 12 and 1 <= dd <= 31): continue
                mes = fe[4:8] + "-" + fe[2:4]
                d["meses"].add(mes)
                if d["primera"] is None or mes < d["primera"]: d["primera"] = mes
                if d["ultima"] is None or mes > d["ultima"]: d["ultima"] = mes

total = sum(d["cif"] for d in imp.values())
print(f"importadores identificados: {len(imp):,}")
print(f"mercado cubierto: US${total/1e6:,.1f}M\n")

# clasificar el perfil de cada importador
perfiles = []
for k, d in imp.items():
    fams = d["familias"].most_common()
    fam_principal = fams[0][0] if fams else ""
    diversidad = len(d["familias"])
    marcas = [m for m,_ in d["marcas"].most_common(8)]
    n_meses = len(d["meses"])
    concentracion = fams[0][1]/d["cif"]*100 if fams else 0
    # tipo de actor: primero por ACTIVIDAD (meses con importacion), luego por escala.
    # Un importador que aparece 1-2 meses puede ser un proyecto puntual; uno que aparece
    # 6+ meses es operacion estable (distribuidor, integrador o usuario con demanda continua).
    marcas_distintas = len(d["marcas"])
    if n_meses >= 6 and marcas_distintas >= 4:
        tipo = "DISTRIBUIDOR / INTEGRADOR"
    elif n_meses >= 6:
        tipo = "USUARIO RECURRENTE"
    elif n_meses >= 3:
        tipo = "COMPRA POR PROYECTO"
    else:
        tipo = "COMPRA PUNTUAL"
    perfiles.append({
        "id": k, "cif": round(d["cif"],2), "items": d["items"], "tipo": tipo,
        "meses_activos": n_meses, "primera": d["primera"], "ultima": d["ultima"],
        "familias": [(f, round(v,2)) for f,v in fams[:5]],
        "fam_principal": fam_principal, "concentracion_pct": round(concentracion,1),
        "marcas": marcas, "n_marcas": marcas_distintas,
        "paises": [p for p,_ in d["paises"].most_common(4)],
        "comuna": d["comunas"].most_common(1)[0][0] if d["comunas"] else "",
    })

perfiles.sort(key=lambda x:-x["cif"])

print("=== TIPO DE ACTOR (por valor) ===")
por_tipo = collections.defaultdict(lambda: {"cif":0.0,"n":0})
for p in perfiles:
    por_tipo[p["tipo"]]["cif"] += p["cif"]; por_tipo[p["tipo"]]["n"] += 1
for t, v in sorted(por_tipo.items(), key=lambda x:-x[1]["cif"]):
    print(f"  {t:26s} {v['n']:>4} importadores   US${v['cif']/1e6:>7,.1f}M  ({v['cif']/total*100:.0f}%)")

print(f"\n=== TOP 20 IMPORTADORES (anonimos, id de Aduanas) ===")
for i, p in enumerate(perfiles[:20], 1):
    print(f"\n{i:2d}. ID {p['id']:>8s}  US${p['cif']/1e6:>6,.2f}M  {p['items']:>5,} items  [{p['tipo']}]")
    print(f"    activo {p['meses_activos']}/12 meses ({p['primera']} a {p['ultima']})  comuna {p['comuna']}")
    print(f"    familia principal: {p['fam_principal']} ({p['concentracion_pct']}%)")
    print(f"    marcas: {', '.join(p['marcas'][:6])}")
    print(f"    paises origen: {', '.join(p['paises'])}")

json.dump({"anio":2025,"total_usd":round(total,2),"n_importadores":len(imp),
  "por_tipo":{k:{"n":v["n"],"cif":round(v["cif"],2)} for k,v in por_tipo.items()},
  "perfiles":perfiles[:300]}, open(os.path.join(D,"perfiles_importador_2025.json"),"w"),
  ensure_ascii=False, indent=1)
print(f"\nguardado: datos/perfiles_importador_2025.json ({len(perfiles)} perfiles)")
