#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MINERAS DEL RETC — recupera las que el cruce había perdido, con los índices CORREGIDOS.

EL ERROR DE UNIVERSO (lo que este script repara)
------------------------------------------------------------------------------
`dolor_ambiental.py` cruzó el RETC CON el plan de contacto y conservó solo la intersección
(370 empresas). Las mineras grandes no estaban en el plan (es un catálogo de otro origen), así que
se cayeron TODAS — Codelco, Los Pelambres, Collahuasi, Spence, El Abra, Antucoya — aunque SÍ están
en el RETC. Se descubrió al cruzar la cuenta #1 del eCRM (Minera Los Pelambres, US$7,8M) y ver que
no aparecía en ningún lado.

REGLA: el universo se toma de la FUENTE, no de la intersección con otro catálogo.

ÍNDICES CORREGIDOS de respeligrosos_2025.xlsx hoja 'Generador' (33 columnas):
  [5] rut_razon_social  [6] razon_social  [8] ciiu6  [12] rubro
  [19] cantidad_transferencia  [20] unidad_abreviacion  [22] tipo_respel  [24] peligrosidad
  (el primer intento leyó el RUT como razón social y una columna sin unidad: salían 2.200M de
   toneladas, absurdo. Verificar la columna contra su nombre, no por posición.)

Salida: datos/mineras_retc.json
"""
import openpyxl, os, re, json, collections

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
RETC = os.path.join(D, "retc")

# CIUU de minería: B = minas y canteras (CIIU4 rev.4)
RX_MIN = re.compile(r"^(B0|B1|B2|B3|B4|B5|B6|B7|B8|B9)", re.I)
RX_MIN_TXT = re.compile(r"extracci[oó]n (de|y)|minas y canteras|procesamiento de cobre|"
                        r"miner[ií]a", re.I)

# nombres de las mineras grandes y operadores (por si el CIIU no las marca)
OPERADORES = ["codelco", "collahuasi", "pelambres", "escondida", "centinela", "candelaria",
              "spence", "el abra", "antucoya", "mantos", "lomas bayas", "zald", "franke",
              "teck", "glencore", "anglo", "quebrada blanca", "sierra gorda", "minera",
              "caseron", "lumina", "maricunga", "salar", "sQM", "albemarle", "kinross"]


def es_minera(rs, ciiu6, ciiu4, rubro):
    if RX_MIN.match(str(ciiu4 or "")) or RX_MIN.match(str(ciiu6 or "")):
        return True
    if RX_MIN_TXT.search(str(ciiu6 or "")) or RX_MIN_TXT.search(str(rubro or "")):
        return True
    n = str(rs or "").lower()
    return any(k in n for k in [o.lower() for o in OPERADORES])


# ---------------------------------------------------------------------------
# 1. RESPELIGROSOS (hoja Generador)
# ---------------------------------------------------------------------------
C = {"rut": 5, "rs": 6, "ciiu6": 8, "ciiu4": 10, "rubro": 12,
     "cant": 19, "unidad": 20, "tipo": 22, "pelig": 24}

por_emp = collections.defaultdict(lambda: {"respel_t": 0.0, "n_decl": 0, "rut": "", "rubro": "",
                                           "ciiu6": "", "residuos": collections.Counter(),
                                           "peligrosidades": collections.Counter()})
p = os.path.join(RETC, "respeligrosos_2025.xlsx")
wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
ws = wb["Generador"]
n_min = 0
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        continue
    rs = row[C["rs"]]
    if not rs:
        continue
    if not es_minera(rs, row[C["ciiu6"]], row[C["ciiu4"]], row[C["rubro"]]):
        continue
    n_min += 1
    rs = str(rs).strip()
    e = por_emp[rs]
    e["rut"] = e["rut"] or str(row[C["rut"]] or "")
    e["rubro"] = e["rubro"] or str(row[C["rubro"]] or "")
    e["ciiu6"] = e["ciiu6"] or str(row[C["ciiu6"]] or "")
    # cantidad: convertir a toneladas según la unidad declarada
    try:
        cant = float(str(row[C["cant"]]).replace(",", ".")) if row[C["cant"]] is not None else 0.0
    except Exception:
        cant = 0.0
    u = str(row[C["unidad"]] or "").lower()
    if u.startswith("kg") or u == "k":
        cant /= 1000.0
    elif u.startswith("g") and not u.startswith("g/") and u != "g":
        cant /= 1e6
    e["respel_t"] += cant
    e["n_decl"] += 1
    if row[C["tipo"]]:
        e["residuos"][str(row[C["tipo"]])[:50]] += 1
    if row[C["pelig"]]:
        e["peligrosidades"][str(row[C["pelig"]])[:30]] += 1
wb.close()
print(f"respeligrosos: {n_min:,} filas de minería -> {len(por_emp)} empresas")

# ---------------------------------------------------------------------------
# 2. RILES (hoja Datos) — cuáles también descargan a agua
# ---------------------------------------------------------------------------
p2 = os.path.join(RETC, "riles_2024.xlsx")
wb2 = openpyxl.load_workbook(p2, read_only=True, data_only=True)
ws2 = wb2["Datos"]
h2 = None
for i, row in enumerate(ws2.iter_rows(values_only=True)):
    if i == 0:
        h2 = {str(c).strip(): j for j, c in enumerate(row) if c is not None}
        break
print(f"riles columnas: {list(h2)[:12]}")
j_rs = h2.get("razon_social", 2)
j_rsv = h2.get("rut_razon_social", 3)
en_riles = set()
n_riles = 0
for row in ws2.iter_rows(values_only=True):
    rs = row[j_rs] if j_rs < len(row) else None
    if not rs:
        continue
    if es_minera(rs, "", "", ""):
        en_riles.add(str(rs).strip())
        n_riles += 1
wb2.close()
print(f"riles: {n_riles:,} filas de minería -> {len(en_riles)} empresas")

# ---------------------------------------------------------------------------
# 3. RESULTADO
# ---------------------------------------------------------------------------
res = []
for rs, e in por_emp.items():
    res.append({"empresa": rs, "rut": e["rut"], "rubro": e["rubro"], "ciiu6": e["ciiu6"],
                "respel_t": round(e["respel_t"], 2), "n_declaraciones": e["n_decl"],
                "en_riles": rs in en_riles,
                "residuos_top": [r for r, _ in e["residuos"].most_common(4)],
                "peligrosidades": [p2 for p2, _ in e["peligrosidades"].most_common(3)]})
res.sort(key=lambda x: -x["respel_t"])

print(f"\n=== MINERAS: {len(res)} ===")
for x in res[:30]:
    print(f"  {x['empresa'][:42]:44s} respel {x['respel_t']:>12,.1f} t | {x['n_declaraciones']:>4} decl | "
          f"{'RILES' if x['en_riles'] else '     '} | {x['rubro'][:18]}")

json.dump({
    "que_es": ("Mineras del RETC con su dolor medido (residuos peligrosos declarados en la hoja "
               "'Generador' de respeligrosos_2025). Recupera las que el cruce anterior perdió."),
    "el_error_que_repara": ("dolor_ambiental.py conservó solo la INTERSECCIÓN del RETC con el plan "
                            "de contacto (370 empresas). Las mineras grandes no estaban en el plan "
                            "y se cayeron todas, aunque SÍ están en el RETC. Se descubrió al cruzar "
                            "la cuenta #1 del eCRM (MLP US$7,8M) y ver que no aparecía."),
    "regla": ("El universo se toma de la FUENTE, no de la intersección con otro catálogo. "
              "Filtrar por intersección pierde justo las empresas que no están del otro lado."),
    "indices_verificados": ("respeligrosos/Generador: [5] rut [6] razon_social [8] ciiu6 "
                            "[12] rubro [19] cantidad [20] unidad [22] tipo [24] peligrosidad. "
                            "Verificar la columna contra su NOMBRE, no por posición: el primer "
                            "intento leyó el RUT como razón social y sumó una columna sin unidad "
                            "(salían 2.200 millones de toneladas, absurdo)."),
    "fuente": "datos/retc/respeligrosos_2025.xlsx (hoja Generador) + riles_2024.xlsx (hoja Datos)",
    "totales": {"mineras": len(res), "con_riles": len(en_riles),
                "respel_total_t": round(sum(x["respel_t"] for x in res), 2)},
    "mineras": res,
}, open(os.path.join(D, "mineras_retc.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/mineras_retc.json — {len(res)} mineras")
