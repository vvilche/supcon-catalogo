#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REPOBLA riles y residuos_t del catálogo de 3.157 empresas cruzando con el RETC (MMA).

PROBLEMA QUE RESUELVE. En el catálogo, `residuos_t` tiene valor en 52 de 3.157 empresas (1,6%)
y `riles` en 2 (0,06%): los dos campos solo están poblados en el rubro química. Con eso, el
motor de leads no puede calcular dolor de agua/residuos en 12 de los 13 rubros.

FUENTE. Portal de datos abiertos del RETC (CKAN, sin credenciales):
  - Emisiones al agua → "AAAA Estimación de Residuos Industriales Líquidos"  (esto ES el RILES)
  - Generación de residuos peligrosos (por generador, con RUT y rubro)
  - Establecimientos registrados en ventanilla única (padrón completo con RUT)

MÉTODO. El cruce es por RUT normalizado; si el RUT no está, por razón social normalizada.
NUNCA inventa: lo que no cruza queda fuera y se cuenta.

Salida: datos/retc_empresas.json  (slug -> {riles, residuos_t, fuente, metodo})
"""
import os, json, glob, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
RETC = os.path.join(D, "retc")
CATALOGO = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s).strip()

def norm_rut(r):
    """Normaliza RUT a digitos + DV, sin puntos ni guion.

    OJO: el RETC trae el RUT como '61704000.0-K' (viene de un float, con .0 espurio).
    Un re.sub de no-digitos convierte eso en '617040000K' — un digito de mas que hace fallar
    TODO el cruce por RUT en silencio (cruzaba 0 por RUT y caia a nombre sin avisar).
    """
    s = str(r or "").strip().upper()
    s = re.sub(r"\.0(?=-|$)", "", s)      # quitar el .0 espurio antes del DV
    s = s.replace(".", "").replace("-", "").replace(" ", "")
    return re.sub(r"[^0-9K]", "", s)

def clave_nombre(s):
    """Clave de razón social: tokens significativos ordenados (el RUT no siempre está)."""
    stop = {"s","a","sa","ltda","limitada","spa","cia","compania","sociedad","empresa","e","i","r","l",
            "de","del","la","el","los","las","y","chile","industrial","servicios","comercial"}
    toks = [t for t in norm(s).split() if t not in stop and len(t) > 2]
    return " ".join(sorted(toks))

# ---------- 1. cargar el catálogo ----------
cat = {}
for f in sorted(glob.glob(os.path.join(CATALOGO, "catalogo-*/research/*.json"))):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    q = d.get("quien_es") or {}
    rut = q.get("rut") if isinstance(q, dict) else ""
    cat[d.get("slug")] = {
      "empresa": d.get("empresa"), "rubro": d.get("rubro"),
      "rut": rut, "region": d.get("region"), "comuna": d.get("comuna"),
    }
print(f"catálogo: {len(cat):,} empresas")

# ---------- 2. leer el RETC ----------
import openpyxl

def leer(f, hoja):
    wb = openpyxl.load_workbook(os.path.join(RETC, f), read_only=True, data_only=True)
    ws = wb[hoja]
    it = ws.iter_rows(values_only=True)
    head = [str(c or "").strip() for c in next(it)]
    filas = []
    for row in it:
        if row and any(c is not None for c in row):
            filas.append(dict(zip(head, row)))
    wb.close()
    return filas

print("\n=== leyendo RETC ===")
riles = leer("riles_2024.xlsx", "Datos")
print(f"  riles 2024:        {len(riles):>8,} filas")
respel = leer("respeligrosos_2025.xlsx", "Generador")
print(f"  residuos peligrosos: {len(respel):>8,} filas")
vent = leer("ventanilla.xlsx", "Hoja1")
print(f"  ventanilla única:  {len(vent):>8,} filas")

# ---------- 3. índices del RETC ----------
# RILES: agregar por RUT y por nombre
idx_riles_rut, idx_riles_nom = collections.defaultdict(float), collections.defaultdict(float)
# la columna de cantidad puede llamarse distinto segun el año: buscarla
def cols(d, *claves):
    for k in d:
        for c in claves:
            if c.lower() in k.lower(): return k
    return None
c_riles = cols(riles[0], "emision_total", "carga", "cantidad", "m3", "toneladas", "riles")
print(f"\n  columna de cantidad en RILES: {c_riles}")
# el RILES del RETC es por CONTAMINANTE y por punto de descarga: se agrega por empresa y se
# guarda cuantos contaminantes distintos emite (mas contaminantes = mas obligaciones de monitoreo)
riles_cont, riles_puntos = collections.defaultdict(set), collections.defaultdict(set)
for r in riles:
    try: v = float(str(r.get(c_riles) or 0).replace(",", ""))
    except: v = 0.0
    if v <= 0: continue
    rut = norm_rut(r.get("rut_razon_social"))
    nom = clave_nombre(r.get("razon_social"))
    k = rut or nom
    if rut: idx_riles_rut[rut] += v
    if nom: idx_riles_nom[nom] += v
    if k:
        if r.get("contaminante"): riles_cont[k].add(str(r["contaminante"]))
        if r.get("ducto_nombre"): riles_puntos[k].add(str(r["ducto_nombre"]))

# residuos peligrosos
idx_res_rut, idx_res_nom = collections.defaultdict(float), collections.defaultdict(float)
c_res = cols(respel[0], "cantidad", "toneladas", "generacion", "peso", "total")
print(f"  columna de cantidad en residuos peligrosos: {c_res}")
for r in respel:
    try: v = float(str(r.get(c_res) or 0).replace(",", ""))
    except: v = 0.0
    if v <= 0: continue
    rut = norm_rut(r.get("rut_razon_social"))
    nom = clave_nombre(r.get("razon_social"))
    if rut: idx_res_rut[rut] += v
    if nom: idx_res_nom[nom] += v

# ---------- 4. cruzar con el catálogo ----------
salida, stats = {}, collections.Counter()
for slug, e in cat.items():
    rut = norm_rut(e["rut"])
    nom = clave_nombre(e["empresa"])
    fila = {}
    # RILES
    v = idx_riles_rut.get(rut, 0) if rut else 0
    met = "rut" if v > 0 else None
    if not v and nom:
        v = idx_riles_nom.get(nom, 0)
        met = "nombre" if v > 0 else None
    if v > 0:
        fila["riles"] = round(v, 2); fila["riles_metodo"] = met
        kk = rut or nom
        if kk in riles_cont: fila["riles_contaminantes"] = sorted(riles_cont[kk])
        if kk in riles_puntos: fila["riles_puntos_descarga"] = len(riles_puntos[kk])
    # residuos peligrosos
    v2 = idx_res_rut.get(rut, 0) if rut else 0
    met2 = "rut" if v2 > 0 else None
    if not v2 and nom:
        v2 = idx_res_nom.get(nom, 0)
        met2 = "nombre" if v2 > 0 else None
    if v2 > 0: fila["residuos_t"] = round(v2, 2); fila["residuos_metodo"] = met2
    fila["fuente"] = "RETC MMA 2024/2025 (datosretc.mma.gob.cl)"
    if rut: fila["rut_catalogo"] = rut
    if "riles" in fila: stats["con_riles"] += 1
    if "residuos_t" in fila: stats["con_residuos"] += 1
    if fila.get("riles_metodo") == "rut": stats["riles_por_rut"] += 1
    if fila.get("residuos_metodo") == "rut": stats["residuos_por_rut"] += 1
    salida[slug] = fila

print(f"\n=== RESULTADO DEL CRUCE ===")
print(f"  empresas con RILES encontrado:      {stats['con_riles']:>5,} / {len(cat):,} "
      f"({stats['con_riles']/len(cat)*100:.1f}%)  [por RUT: {stats['riles_por_rut']:,}]")
print(f"  empresas con residuos peligrosos:   {stats['con_residuos']:>5,} / {len(cat):,} "
      f"({stats['con_residuos']/len(cat)*100:.1f}%)  [por RUT: {stats['residuos_por_rut']:,}]")
sin_rut = sum(1 for e in cat.values() if not norm_rut(e["rut"]))
print(f"  empresas sin RUT en el catálogo:    {sin_rut:>5,} (el cruce cae a nombre)")

json.dump({
 "metodo": ("Cruce del catálogo de 3.157 empresas con el RETC del MMA por RUT normalizado; "
   "si el RUT no cruza, por razón social normalizada (tokens significativos ordenados). "
   "RILES = 'Estimación de Residuos Industriales Líquidos' (emisiones al agua). "
   "Nunca inventa: lo que no cruza queda fuera."),
 "fuente": "datosretc.mma.gob.cl — datasets de Emisiones al agua y Generación de residuos peligrosos",
 "archivos_retc": ["datos/retc/riles_2024.xlsx","datos/retc/respel_2025.xlsx","datos/retc/ventanilla.xlsx"],
 "estadisticas": dict(stats),
 "cobertura": {"empresas_catalogo": len(cat), "con_riles": stats["con_riles"],
   "con_residuos_peligrosos": stats["con_residuos"], "sin_rut": sin_rut},
 "empresas": salida,
}, open(os.path.join(D,"retc_empresas.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/retc_empresas.json ({len(salida):,} entradas)")
