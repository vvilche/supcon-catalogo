#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPLETA LAS SEÑALES de dolor sobre el universo de 3.157 empresas.

Señales que se suman, todas de fuente oficial verificada:
  1. RILES (emisión al agua, DS 90/2000) ............ RETC MMA, `datos/retc_empresas.json`
  2. Residuos peligrosos (DS 43/2015) ............... RETC MMA, idem
  3. Completitud CEN < 80% .......................... InfoTécnica Coordinador (1.082 empresas SEN)
  4. Calidad CEN < 60% (datos rechazados) ........... InfoTécnica Coordinador
  5. Multas SEC ..................................... NO DISPONIBLE como dataset (ver nota)

MULTAS SEC: la SEC no publica un dataset de sanciones. Su portal tiene 2.307 archivos, de los
cuales 344 son resoluciones exentas (REX) en PDF individual, mezcladas con otros temas
(administradores provisionales, costo de explotación). Parsear 344 PDFs sería caro y frágil.
Se declara como señal NO INCORPORADA en vez de estimarla o inventarla.

Entrada: datos/universo_prospeccion_supcon.json (3.157 empresas con dolor RETC)
         cen_completitud_empresas.json + cen_calidad_empresas.json (1.082 empresas SEN)
Salida:  datos/universo_senales_completas.json
"""
import os, json, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
WS = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s)

STOP = {"s","a","sa","ltda","limitada","spa","cia","compania","sociedad","empresa","de","del",
        "la","el","los","las","y","chile","generacion","generadora","electrica","energia",
        "transmisora","transmision","servicios","comercial","industrial","inversiones","sp"}

def clave(s):
    """Tokens significativos ordenados, para cruzar nombres de empresa entre fuentes."""
    return " ".join(sorted(t for t in norm(s).split() if t not in STOP and len(t) > 2))

def jaccard(a, b):
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb: return 0.0
    return len(sa & sb) / len(sa | sb)

# ---------- cargar el universo ----------
uni = json.load(open(os.path.join(D, "universo_prospeccion_supcon.json"), encoding="utf-8"))
emps = uni["empresas"]
print(f"universo: {len(emps):,} empresas\n")

# ---------- cargar señales CEN ----------
com = json.load(open(os.path.join(WS, "cen_completitud_empresas.json"), encoding="utf-8"))
cal = json.load(open(os.path.join(WS, "cen_calidad_empresas.json"), encoding="utf-8"))
cal_por_id = {c["id_empresa"]: c for c in cal}

cen = {}
for c in com:
    k = cal_por_id.get(c["id_empresa"], {})
    cen[c["id_empresa"]] = {
      "nombre": c["empresa_nombre"], "clave": clave(c["empresa_nombre"]),
      "completitud": c.get("completitud"), "calidad": k.get("calidad"),
      "rechazados": k.get("datos_rechazados") or 0,
      "no_informados": c.get("datos_no_informados") or 0,
    }
print(f"señal CEN: {len(cen):,} empresas del SEN")

# índice por clave para el cruce
idx_cen = collections.defaultdict(list)
for v in cen.values():
    if v["clave"]: idx_cen[v["clave"]].append(v)

# ---------- cruzar ----------
stats = collections.Counter()
for e in emps:
    k = clave(e.get("empresa"))
    match = None
    if k in idx_cen:
        match = idx_cen[k][0]
        stats["cen_exacto"] += 1
    else:
        # Jaccard >= 0.6 (umbral de la skill: evita que "Empresa Electrica X" matchee a todas)
        mejor, mejor_j = None, 0.0
        for kk, vs in idx_cen.items():
            j = jaccard(k, kk)
            if j > mejor_j: mejor, mejor_j = vs[0], j
        if mejor_j >= 0.6:
            match = mejor
            stats["cen_jaccard"] += 1

    if match:
        d_cen = 0
        det = []
        comp, cali, rej = match["completitud"], match["calidad"], match["rechazados"]
        if comp is not None and comp < 0.8:
            d_cen += min(30, (1-comp)*40)
            det.append(f"completitud CEN {comp:.0%} ({match['no_informados']:,} datos sin informar)")
        if cali is not None and cali < 0.6:
            d_cen += min(30, (1-cali)*40)
            det.append(f"calidad CEN {cali:.0%} ({rej:,} datos rechazados)")
        elif rej > 50:
            d_cen += 20
            det.append(f"{rej:,} datos rechazados por el Coordinador")
        if d_cen > 0:
            stats["con_dolor_cen"] += 1
            e["cen_dolor"] = round(d_cen, 1)
            e["cen_detalle"] = det
            e["cen_nombre"] = match["nombre"]
            e["dolor"] = round(e.get("dolor", 0) + d_cen, 1)
        else:
            e["cen_dolor"] = 0

# recomputar prioridad con el dolor total
import math
# El desempate por magnitud cruda hacia que Codelco (2,2 millones de toneladas) dominara el
# orden y el resto quedara indistinguible entre si. Se usa el log de la magnitud y se escala
# a 0-10 por percentil: ordena DENTRO del empate de dolor sin aplastar la escala.
mags = sorted(((e.get("residuos_t") or 0) + (e.get("riles") or 0) * 100) for e in emps)
def percentil(v):
    if v <= 0: return 0.0
    lo = sum(1 for m in mags if m < v)
    return (lo / max(len(mags), 1)) * 10.0
# La magnitud es DESEMPATE, no componente del puntaje: se usa como fraccion (<1) para que
# jamas supere un punto de dolor. Si sumara 0-10 entero, invertiria el orden y una empresa de
# volumen alto con dolor bajo pasaria por encima de una con dolor alto (medido con ENAEX: dolor
# 129 por incumplimiento CEN, que quedaba 30o frente a pesqueras de dolor 90).
# OJO CON LA ESCALA: antes la prioridad era dolor x capacidad, pero el dolor llega hasta ~130
# mientras la capacidad multiplica por 2 o 3. Resultado medido: ENAEX con el dolor MAS ALTO
# (129, por 39 puntos de incumplimiento CEN) quedaba 30o, por debajo de pesqueras con dolor 90
# y tier GRANDE. La capacidad no puede dominar a la señal de incumplimiento.
# Correccion: la capacidad es un FACTOR ACOTADO (1.0 a 1.4), no un multiplicador 2x/3x.
CAP = {"GRANDE": 1.4, "MEDIANA": 1.2, "PEQUEÑA": 1.0, "PEQUENA": 1.0, "MICRO": 1.0}
for e in emps:
    magnitud = (e.get("residuos_t") or 0) + (e.get("riles") or 0) * 100
    desempate = percentil(magnitud) / 100.0 if magnitud > 0 else 0.0
    e["factor_capacidad"] = CAP.get(e.get("tier", ""), 1.0)
    e["prioridad"] = round(e["dolor"] * e["factor_capacidad"] + desempate, 3)
    e["magnitud"] = round(magnitud, 1)

emps.sort(key=lambda e: -e["prioridad"])
con_dolor = [e for e in emps if e["dolor"] > 0]

print(f"\n=== CRUCE CEN → catálogo industrial ===")
print(f"  match exacto por tokens:    {stats['cen_exacto']:,}")
print(f"  match por Jaccard >= 0.6:   {stats['cen_jaccard']:,}")
print(f"  empresas con dolor CEN:     {stats['con_dolor_cen']:,}")
print(f"\n=== SEÑALES COMPLETAS ===")
print(f"  empresas con dolor > 0:     {len(con_dolor):,} / {len(emps):,} ({len(con_dolor)/len(emps)*100:.0f}%)")
con_riles = sum(1 for e in emps if (e.get("riles") or 0) > 0)
con_res = sum(1 for e in emps if (e.get("residuos_t") or 0) > 0)
con_cen = sum(1 for e in emps if (e.get("cen_dolor") or 0) > 0)
print(f"    por RILES al agua:        {con_riles:,}")
print(f"    por residuos peligrosos:  {con_res:,}")
print(f"    por CEN (completitud/calidad): {con_cen:,}")

print(f"\n=== TOP 30 CON TODAS LAS SEÑALES ===")
print(f"{'#':>3s} {'EMPRESA':40s} {'RUBRO':24s} {'Z':>3s} {'dolor':>6s} {'prio':>6s}  señales")
print("-"*104)
for i, e in enumerate(con_dolor[:30], 1):
    sen = []
    if e.get("riles"): sen.append(f"RILES {e['riles']:,.0f}")
    if e.get("residuos_t"): sen.append(f"res {e['residuos_t']:,.0f}t")
    if e.get("cen_dolor"): sen.append(f"CEN +{e['cen_dolor']:.0f}")
    print(f"{i:>3d} {str(e['empresa'])[:40]:40s} {e['rubro'][:24]:24s} {e.get('zona') or '-':>3s} "
          f"{e['dolor']:>6.0f} {e['prioridad']:>6.0f}  {' · '.join(sen)}")

json.dump({
 "metodo": ("Universo de 3.157 empresas industriales con señales de dolor de fuente oficial: "
   "(1) RILES al agua y (2) residuos peligrosos del RETC del MMA, cruzados por RUT; "
   "(3) completitud y (4) calidad CEN del Coordinador Eléctrico, cruzadas por Jaccard de tokens "
   "(umbral 0.6). Prioridad = dolor × capacidad, con desempate por magnitud real."),
 "fuentes": {
   "retc": "datosretc.mma.gob.cl (Emisiones al agua + Generación de residuos peligrosos)",
   "cen": "api-infotecnica.coordinador.cl (completitud y calidad de información técnica)",
   "catalogo": "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo/catalogo-*/research/",
 },
 "senales_no_incorporadas": {
   "multas_sec": ("NO DISPONIBLE como dataset. La SEC no publica un archivo de sanciones: su "
     "portal tiene 2.307 archivos y 344 resoluciones exentas (REX) en PDF individual, mezcladas "
     "con otros temas (administradores provisionales, costo de explotación). Incorporarlas "
     "requeriría parsear 344 PDFs. Se declara como señal no incorporada en vez de estimarla."),
 },
 "resumen": {
   "empresas": len(emps), "con_dolor": len(con_dolor),
   "con_riles": con_riles, "con_residuos": con_res,
   "con_dolor_cen": con_cen,
   "cen_match_exacto": stats["cen_exacto"], "cen_match_jaccard": stats["cen_jaccard"],
 },
 "empresas": emps,
}, open(os.path.join(D,"universo_senales_completas.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/universo_senales_completas.json")
