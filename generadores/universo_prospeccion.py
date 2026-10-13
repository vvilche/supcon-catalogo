#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUCE AMPLIADO: el catálogo normativo de 3.157 empresas industriales × líneas SUPCON.

POR QUÉ. El cruce anterior usaba solo 34 empresas (las de capital chino). Pero existe un
catálogo ya construido de 3.157 empresas industriales chilenas con dolor normativo verificado,
que trae por empresa: rubro, región, comuna, tier, score de tamaño, toneladas de residuos
peligrosos, si emite RILES, coordenadas y tomadores de decisión.

Fuente: /Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo/
        catalogo-<rubro>/research/*.json  (3.157 archivos, 13 rubros)

Este módulo los cruza con las líneas SUPCON y las zonas geográficas priorizadas, para producir
el universo completo de prospección —no solo las 34 con capital chino.

Salida: datos/universo_prospeccion_supcon.json
"""
import os, json, glob, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
CATALOGO = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.replace("aisen", "aysen")   # pitfall de la skill: AISEN <-> AYSEN

# ---- RETC cruzado: los campos riles/residuos_t del catalogo estan poblados solo en 1 rubro
# de 13 (52 de 3157 con residuos, 2 con RILES). Se reemplazan por el dato real del RETC,
# cruzado por RUT y nombre en generadores/cruzar_retc.py.
RETC = json.load(open(os.path.join(D, "retc_empresas.json"), encoding="utf-8"))["empresas"]

# ---------- rubro del catálogo -> líneas SUPCON que aplican ----------
# Basado en el mapeo rubro->producto de la estrategia normativa (cruce_normativo_estrategia.json),
# no inventado: cada rubro tiene su norma y su producto.
RUBRO_LINEAS = {
 "Producción química":            ["SIS","DCS","Instrumentación","Software y plataforma"],
 "Fabricación de celulosa":       ["DCS","Instrumentación","Válvulas","Software y plataforma"],
 "Extracción de minerales":       ["DCS","Instrumentación","SIS","Válvulas"],
 "Producción de metal":           ["DCS","Instrumentación","SIS"],
 "Generación de energía":         ["DCS","Analítica","Instrumentación","Software y plataforma"],
 "Transmisión y distribución de energía eléctrica":
                                  ["DCS","Software y plataforma","Instrumentación"],
 "Suministro y tratamiento de aguas":
                                  ["Instrumentación","Analítica","Software y plataforma"],
 "Combustibles":                  ["SIS","Instrumentación","DCS"],
 "Gestor de residuos":            ["Instrumentación","Software y plataforma"],
 "Producción de alimentos":       ["Instrumentación","DCS","Válvulas","Software y plataforma"],
 "Industria manufacturera":       ["Instrumentación","DCS","Válvulas"],
 "Pesca":                         ["Instrumentación","DCS"],
 "Industria agropecuaria y silvicultura":
                                  ["Instrumentación","Software y plataforma"],
}

# ---------- zonas geográficas por región ----------
ZONA_REGION = {
 "Z1": ["metropolitana","santiago"],
 "Z2": ["antofagasta","tarapaca"],
 "Z3": ["valparaiso"],
 "Z4": ["biobio","araucania","nuble"],
 "Z5": ["los lagos","aysen","magallanes"],
 "Z6": ["coquimbo","atacama"],
 "Z7": ["maule","o'higgins","ohiggins","libertador"],
}

# ---------- normas por rubro (del cruce normativo, con su disparador) ----------
NORMAS_RUBRO = {
 "Producción química": ["DS 43/2015 (sust. peligrosas)","DS 90/2000 (RILES)","RETC DS 1/2013","DS 594"],
 "Fabricación de celulosa": ["DS 90/2000 (RILES)","RETC DS 1/2013","DS 594","Ley 21.455"],
 "Extracción de minerales": ["DS 132 (seguridad minera)","Ley 20.551 (cierre)","RETC","DS 90/2000"],
 "Producción de metal": ["DS 132","Ley 20.551","DS 43/2015","RETC"],
 "Generación de energía": ["DS 13/2011 Art. 8 (CEMS)","NTSyCS 4-12/4-16","Ley 21.305","DS 594"],
 "Transmisión y distribución de energía eléctrica": ["Ley 21.663 (OIV)","NTSyCS","Ley 21.305"],
 "Suministro y tratamiento de aguas": ["DS 90/2000 (RILES)","Ley 18.902","NCh 409","DS 609/1998"],
 "Combustibles": ["DS 43/2015","DS 160","DS 90/2000"],
 "Gestor de residuos": ["DS 148","Ley 20.920 (REP)","RETC"],
 "Producción de alimentos": ["DS 594","DS 90/2000 (RILES)","RETC","Ley 21.305"],
 "Industria manufacturera": ["RETC","DS 594","Ley 21.305","DS 43/2015"],
 "Pesca": ["DS 594","DS 90/2000 (RILES)","RETC"],
 "Industria agropecuaria y silvicultura": ["DS 594","Ley 18.450","Ley 21.455","DS 90/2000"],
}

def zona_de(region, comuna):
    txt = norm(f"{region} {comuna}")
    for z, regs in ZONA_REGION.items():
        if any(r in txt for r in regs):
            return z
    return None

TIER_P = {"GRANDE": 3, "MEDIANA": 2, "PEQUEÑA": 1, "PEQUENA": 1, "MICRO": 1}

archivos = sorted(glob.glob(os.path.join(CATALOGO, "catalogo-*/research/*.json")))
print(f"catálogo: {len(archivos)} empresas en {len(set(os.path.dirname(a) for a in archivos))} rubros\n")

empresas = []
errores = 0
for f in archivos:
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        errores += 1; continue
    rubro = d.get("rubro") or ""
    lineas = RUBRO_LINEAS.get(rubro)
    if not lineas:
        # rubro no mapeado: no se inventa, se marca
        lineas = []
    def fl(x):
        try: return float(str(x).replace(",", ""))
        except: return 0.0
    # el dato del catalogo esta vacio en 12 de 13 rubros: se usa el del RETC cruzado
    retc = RETC.get(d.get("slug")) or {}
    residuos = fl(retc.get("residuos_t")) or fl(d.get("residuos_t"))
    riles = fl(retc.get("riles")) or fl(d.get("riles"))
    contaminantes = retc.get("riles_contaminantes") or []
    tier = (d.get("tier") or "").upper()
    score = fl(d.get("score"))
    region = d.get("region") or ""
    comuna = d.get("comuna") or ""
    z = zona_de(region, comuna)

    # dolor: señales verificadas, no estimadas
    dolor = 0
    if riles > 0: dolor += min(int(riles/50)+8, 40)     # emite RILES: DS 90/2000
    if residuos > 0: dolor += min(int(residuos/20)+5, 40)  # residuos peligrosos: DS 43/148
    if len(contaminantes) > 3: dolor += 10              # varios contaminantes = mas monitoreo
    señales = []
    if riles > 0: señales.append(f"RILES {riles:,.0f}")
    if residuos > 0: señales.append(f"residuos peligrosos {residuos:,.0f} t")
    if contaminantes: señales.append(f"{len(contaminantes)} contaminantes en RILES")

    cap = TIER_P.get(tier, 1)

    # desempate por magnitud: dos empresas con el mismo dolor no valen lo mismo si una emite
    # 10 t y la otra 50.000 t. Se usa el logaritmo para que el orden no lo domine un solo caso.
    import math
    magnitud = (residuos or 0) + (riles or 0) * 100   # el RILES se pondera (es efluente directo)
    desempate = math.log10(magnitud + 1) if magnitud > 0 else 0.0
    prioridad = dolor * cap + desempate

    empresas.append({
      "empresa": d.get("empresa"), "rubro": rubro, "clasificacion": d.get("clasificacion"),
      "region": region, "comuna": comuna, "zona": z, "tier": tier, "score": score,
      "residuos_t": residuos, "riles": riles, "riles_contaminantes": contaminantes,
      "senales_dolor": señales,
      "dolor": dolor, "capacidad": cap, "prioridad": round(prioridad,2),
      "magnitud_residuos": round(magnitud,1),
      "lineas_supcon": lineas, "normas": NORMAS_RUBRO.get(rubro, []),
      "tomadores": [t.get("nombre") for t in (d.get("tomadores") or []) if t.get("nombre")][:3],
      "lat": d.get("lat"), "lon": d.get("lon"), "slug": d.get("slug"),
    })

print(f"empresas cargadas: {len(empresas)} (errores: {errores})\n")

with_riles = [e for e in empresas if e["riles"] > 0]
with_res = [e for e in empresas if e["residuos_t"] > 0]
con_dolor = [e for e in empresas if e["dolor"] > 0]
por_zona = collections.Counter(e["zona"] or "sin zona" for e in empresas)
por_rubro = collections.Counter(e["rubro"] for e in empresas)

print("=== SEÑALES DE DOLOR NORMATIVO ===")
print(f"  con RILES declarado (DS 90/2000):           {len(with_riles):>5,}")
print(f"  con residuos peligrosos (DS 43/148):        {len(with_res):>5,}")
print(f"  con alguna señal de dolor verificada:       {len(con_dolor):>5,}")
print()
print("=== POR ZONA GEOGRÁFICA ===")
for z in ["Z1","Z2","Z3","Z4","Z5","Z6","Z7","sin zona"]:
    if z in por_zona: print(f"  {z:9s} {por_zona[z]:>5,}")
print()
print("=== POR RUBRO (top 8) ===")
for r, n in por_rubro.most_common(8):
    print(f"  {r[:46]:48s} {n:>5,}")

# top por prioridad
top = sorted(con_dolor, key=lambda e: -e["prioridad"])[:25]
print()
print("=== TOP 25 POR DOLOR × CAPACIDAD ===")
print(f"{'#':>3s} {'EMPRESA':40s} {'RUBRO':26s} {'Z':>3s} {'tier':>7s} {'dolor':>6s} {'prio':>6s}")
print("-"*100)
for i, e in enumerate(top, 1):
    print(f"{i:>3d} {str(e['empresa'])[:40]:40s} {e['rubro'][:26]:26s} {e['zona'] or '-':>3s} "
          f"{e['tier']:>7s} {e['dolor']:>6.0f} {e['prioridad']:>6.0f}")

json.dump({
 "metodo": ("Universo completo de prospección SUPCON: 3.157 empresas industriales chilenas del "
   "catálogo normativo (RETC/RILES) cruzadas con las 7 líneas de producto y las zonas "
   "geográficas. El dolor sale de señales VERIFICADAS del registro (toneladas de residuos "
   "peligrosos y emisión de RILES), no de una estimación. Prioridad = dolor × capacidad."),
 "fuente": ("/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo/"
   "catalogo-<rubro>/research/*.json — 3.157 empresas, 13 rubros, con datos de RETC y RILES"),
 "resumen": {
   "empresas": len(empresas),
   "con_riles": len(with_riles),
   "con_residuos_peligrosos": len(with_res),
   "con_dolor_verificado": len(con_dolor),
   "por_zona": dict(por_zona),
   "por_rubro": dict(por_rubro),
 },
 "mapeo_rubro_lineas": RUBRO_LINEAS,
 "empresas": sorted(empresas, key=lambda e: -e["prioridad"]),
}, open(os.path.join(D,"universo_prospeccion_supcon.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/universo_prospeccion_supcon.json")
