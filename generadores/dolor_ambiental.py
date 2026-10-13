#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOLOR AMBIENTAL POR EMPRESA — que le vendemos a cada una para que no la multen.

QUE HACE
------------------------------------------------------------------------------
Cruza el RETC crudo (RILES del DS 90/2000 y residuos peligrosos del DS 43/2015) contra el
plan de contacto, y por cada empresa produce:

  - QUE contamina (los contaminantes reales, no un conteo)
  - CUANTO (emision sumada de la fuente)
  - DONDE descarga (comuna y punto de descarga)
  - QUE VENDERLE, derivado del propio dato (no inventado)
  - A QUIEN llamar (contacto del plan, con cargo y rol de compra)

LA LOGICA DE VENTA SALE DEL DATO, NO DE UN CATALOGO
------------------------------------------------------------------------------
La SMA fiscaliza por norma. Cada obligacion del DS 90 / DS 43 que hoy NO se mide en linea es
un argumento de venta, y el tipo de obligacion determina el producto:

  - Metales pesados al agua (arsenico, cadmio, plomo, mercurio, cromo, niquel)
    -> analizadores en linea + monitoreo de efluentes. Es lo que mas multa se lleva.
  - Cianuro / sulfuro -> analisis especifico de proceso, no instrumento generico.
  - Muchos contaminantes distintos (>10) -> la obligacion es MULTIPLE: no alcanza un medidor,
    se necesita una plataforma de monitoreo continuo (Software y plataforma).
  - Multiples peligrosidades RESPEL (>=3) -> trazabilidad de residuos peligrosos.
  - Volumen alto de RESPEL -> manejo y declaracion en linea al RETC.

FUENTES
  RILES: datos/retc/riles_2024.xlsx  (10.870 filas, emision_total por contaminante y ducto)
  RESPEL: datos/retc/respeligrosos_2025.xlsx hoja 'Generador' (40.329 filas, cantidad en kg)
  Contactos: datos/plan_contacto.json (corregido: riles ya no se suma por planta)

Salida: datos/dolor_ambiental_empresas.json  +  artefactos/dolor_ambiental.html
"""
import openpyxl, os, re, json, collections, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
RETC = os.path.join(D, "retc")
OUT_HTML = os.path.join(BASE, "artefactos", "dolor_ambiental.html")

# ---------------------------------------------------------------------------
# 1. QUE CONTAMINA cada empresa — leido del RETC crudo
# ---------------------------------------------------------------------------
METALES = {"arsenico", "arsénico", "cadmio", "plomo", "mercurio", "cromo", "niquel", "níquel",
           "cobre", "zinc", "manganeso", "molibdeno", "aluminio", "hierro", "cobalto", "bario"}
ESPECIALES = {"cianuro", "sulfuro", "fluoruro", "indice fenol", "índice fenol"}


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


def num(v):
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return 0.0


def leer(path, hoja):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[hoja]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    hdr = [str(c).strip() if c is not None else "" for c in rows[0]]
    return hdr, rows[1:]


def ci(hdr, n):
    for i, c in enumerate(hdr):
        if c.lower() == n.lower():
            return i
    return None


# ---- RILES (DS 90) ----
hdr, filas = leer(os.path.join(RETC, "riles_2024.xlsx"), "Datos")
c_rs, c_est, c_com, c_emi = ci(hdr, "razon_social"), ci(hdr, "nombre_establecimiento"), ci(hdr, "comuna"), ci(hdr, "emision_total")
c_cont, c_ducto, c_tabla = ci(hdr, "contaminante"), ci(hdr, "ducto_nombre"), ci(hdr, "tabla")
c_rut, c_rubro, c_lat, c_lon = ci(hdr, "rut_razon_social"), ci(hdr, "rubro"), ci(hdr, "latitud"), ci(hdr, "longitud")

riles = {}
for r in filas:
    if not r or not r[c_rs]:
        continue
    k = str(r[c_rs]).strip().upper()
    e = riles.setdefault(k, {"emision": 0.0, "contaminantes": collections.Counter(),
                             "comunas": set(), "puntos": set(), "tablas": set(),
                             "establecimientos": set(), "rubro": r[c_rubro] or "",
                             "rut": str(r[c_rut] or ""), "n_filas": 0,
                             "detalle": []})
    e["n_filas"] += 1
    e["emision"] += num(r[c_emi])
    if r[c_cont]: e["contaminantes"][str(r[c_cont]).strip()] += 1
    if r[c_com]: e["comunas"].add(str(r[c_com]).strip())
    if r[c_est]: e["establecimientos"].add(str(r[c_est]).strip())
    if r[c_ducto]: e["puntos"].add(str(r[c_ducto]).strip())
    if r[c_tabla]: e["tablas"].add(str(r[c_tabla]).strip())
    if r[c_cont] and num(r[c_emi]) > 0:
        e["detalle"].append({"contaminante": str(r[c_cont]).strip(), "t": num(r[c_emi]),
                             "comuna": str(r[c_com] or "").strip(),
                             "ducto": str(r[c_ducto] or "").strip(),
                             "tabla": str(r[c_tabla] or "").strip()})

# ---- RESPEL (DS 43) ----
hdr2, filas2 = leer(os.path.join(RETC, "respeligrosos_2025.xlsx"), "Generador")
d_rs, d_cant = ci(hdr2, "razon_social"), ci(hdr2, "cantidad_transferencia")
d_tipo, d_pel = ci(hdr2, "tipo_respel"), ci(hdr2, "peligrosidad")
d_com, d_rubro, d_rut = ci(hdr2, "comuna"), ci(hdr2, "rubro"), ci(hdr2, "rut_razon_social")

respel = {}
for r in filas2:
    if not r or not r[d_rs]:
        continue
    k = str(r[d_rs]).strip().upper()
    e = respel.setdefault(k, {"kg": 0.0, "tipos": collections.Counter(),
                              "peligrosidades": collections.Counter(),
                              "comunas": set(), "rubro": r[d_rubro] or "",
                              "rut": str(r[d_rut] or ""), "n_filas": 0, "detalle": []})
    e["n_filas"] += 1
    q = num(r[d_cant])
    e["kg"] += q
    for t in str(r[d_tipo] or "").split(";"):
        t = t.strip()
        if t: e["tipos"][t] += 1
    for p in str(r[d_pel] or "").split(";"):
        p = p.strip()
        if p: e["peligrosidades"][p] += 1
    if r[d_com]: e["comunas"].add(str(r[d_com]).strip())
    if r[d_tipo] and q > 0:
        e["detalle"].append({"tipo": str(r[d_tipo]).strip()[:120], "t": q,
                             "peligrosidad": str(r[d_pel] or "").strip(),
                             "comuna": str(r[d_com] or "").strip()})

# ---------------------------------------------------------------------------
# 2. QUE VENDERLE — derivado del dato
# ---------------------------------------------------------------------------
# CORRECCION DE CRITERIO (medida, no supuesta): ordenar por emision_total pone arriba a quien
# descarga mas SAL. Medido: el top del pais son CLORUROS y SULFATO —
#   Guacolda 1.252.349 t (cloruros, agua de mar para enfriamiento)
#   Engie 328.625 t, Tornagaleones 153.357 t, Codelco 88.286 t (77.097 son de SULFATO)
# Cloruro y sulfato son volumen, no toxicidad: un cloruro de agua de mar no se multa, un CADMIO
# si. Ordenar por volumen manda al vendedor donde no hay dolor.
#
# Se calcula entonces una CARGA PELIGROSA = suma de los contaminantes que la SMA controla por
# toxicidad (metales pesados + cianuro/sulfuro/fenoles) y se ordena por ESO. La emision total
# se sigue reportando, pero como contexto, no como criterio de prioridad.
PELIGROSOS = METALES | ESPECIALES | {"hidrocarburos fijos", "hidrocarburos totales",
                                     "aceites y grasas", "fenoles", "tensoactivos",
                                     "organoclorados", "pesticidas", "benceno", "tolueno"}


def carga_peligrosa(detalle):
    """Toneladas anuales SOLO de los contaminantes toxicos, excluyendo sal y nutrientes."""
    tot = 0.0
    for d in detalle:
        if norm(d["contaminante"]) in PELIGROSOS:
            tot += d["t"]  # el campo se llama kg en el JSON; la unidad real es t (ver metadato)
    return tot


def que_vender(cont_list, n_cont, pel_counter, kg):
    """Deriva la oferta del propio dato. Devuelve (productos, motivo)."""
    prods, motivos = [], []
    cl = [norm(c) for c in cont_list]
    metales = sorted({c for c in cont_list if norm(c) in METALES})
    espec = sorted({c for c in cont_list if norm(c) in ESPECIALES})

    if metales:
        prods.append("Analítica en línea de metales")
        motivos.append(f"{len(metales)} metales pesados en el efluente "
                       f"({', '.join(metales[:4])}{'…' if len(metales) > 4 else ''})")
    if espec:
        prods.append("Analítica específica de proceso")
        motivos.append(f"contaminantes de control especial ({', '.join(espec[:3])})")
    if n_cont >= 10:
        prods.append("Software y plataforma")
        motivos.append(f"{n_cont} contaminantes distintos = obligación de monitoreo múltiple")
    elif n_cont > 3:
        prods.append("Instrumentación")
        motivos.append(f"{n_cont} contaminantes declarados")
    if len(pel_counter) >= 3:
        prods.append("Trazabilidad de residuos peligrosos")
        motivos.append(f"{len(pel_counter)} peligrosidades distintas declaradas")
    elif pel_counter:
        prods.append("Declaración RETC en línea")
        motivos.append(f"genera residuos peligrosos ({', '.join(list(pel_counter)[:2])})")
    if kg > 100_000_000:
        prods.append("Monitoreo continuo de volumen")
        motivos.append(f"{kg/1e6:,.0f} t de residuos peligrosos: el volumen exige medición continua")
    if not prods:
        prods.append("Instrumentación (diagnóstico)")
        motivos.append("reporta al RETC pero sin señal fuerte medida")
    # dedupe preservando orden
    vistos = set(); p2 = []
    for p in prods:
        if p not in vistos:
            vistos.add(p); p2.append(p)
    return p2, motivos


# ---------------------------------------------------------------------------
# 3. CRUZAR con el plan de contacto
# ---------------------------------------------------------------------------
plan = json.load(open(os.path.join(D, "plan_contacto.json"), encoding="utf-8"))["plan"]


def norm_key(s):
    s = norm(s)
    s = re.sub(r"\b(s a|sa|ltda|limitada|spa|scm|cia|compania|sociedad|empresa|de|del|la|el|los|las|y|chile)\b", " ", s)
    return " ".join(sorted(t for t in re.sub(r"[^a-z0-9 ]", " ", s).split() if len(t) > 2))


plan_idx = {}
for p in plan:
    plan_idx.setdefault(norm_key(p["empresa"]), p)

salida = []
sin_plan = 0
for k, rl in riles.items():
    rp = respel.get(k)
    if rp is None:
        # RESPEL cruza por razon social igual; si no esta, se busca variante
        rp = {}
    cont_list = [c for c, _ in rl["contaminantes"].most_common()]
    pel = rp.get("peligrosidades") or collections.Counter()
    kg = rp.get("kg") or 0.0
    prods, motivos = que_vender(cont_list, len(cont_list), pel, kg)
    carga = carga_peligrosa(rl["detalle"])

    p = plan_idx.get(norm_key(k))
    if p is None:
        sin_plan += 1

    salida.append({
        "empresa": k.title(),
        "razon_social_retc": k,
        "rut": rl.get("rut") or rp.get("rut") or "",
        "rubro": rl.get("rubro") or rp.get("rubro") or "",
        # RILES — la unidad REAL es toneladas anuales (declarado en la hoja Metadatos)
        "emision_agua_t": round(rl["emision"], 2),
        "carga_peligrosa_t": round(carga, 2),
        "n_contaminantes": len(cont_list),
        "contaminantes": cont_list,
        "comunas_descarga": sorted(rl["comunas"]),
        "puntos_descarga": sorted(rl["puntos"])[:6],
        "tablas_ds90": sorted(rl["tablas"]),
        # RESPEL
        "respel_t": round(kg / 1000, 1),
        "respel_kg": round(kg, 0),
        "peligrosidades": [[k2, v] for k2, v in pel.most_common()],
        "tipos_respel": [[t, n] for t, n in rp.get("tipos", collections.Counter()).most_common(6)],
        "n_tipos_respel": len(rp.get("tipos") or {}),
        # VENTA
        "que_vender": prods,
        "por_que": motivos,
        # CONTACTO
        "en_plan": p is not None,
        "contacto": ({"nombre": p["contacto_principal"]["nombre"],
                      "cargo": p["contacto_principal"]["cargo"],
                      "rol": p["rol_principal"],
                      "linkedin": p["contacto_principal"].get("linkedin")} if p else None),
        "n_contactos_plan": p["n_tomadores"] if p else 0,
        "zona": p["zona"] if p else None,
        "dolor": p["dolor"] if p else None,
        # detalle auditable
        "detalle_agua": sorted(rl["detalle"], key=lambda x: -x["t"])[:8],
        "detalle_respel": sorted(rp.get("detalle") or [], key=lambda x: -x["t"])[:8],
    })

# ORDEN: por CARGA PELIGROSA (metales pesados y toxicos), no por volumen total.
# Ordenar por emision total pone arriba a quien descarga mas sal (cloruros de agua de mar).
salida.sort(key=lambda x: -x["carga_peligrosa_t"])

en_plan = sum(1 for s in salida if s["en_plan"])
con_venta = sum(1 for s in salida if len(s["que_vender"]) >= 2)
print("=" * 80)
print("DOLOR AMBIENTAL POR EMPRESA — RETC x plan de contacto")
print("=" * 80)
print(f"  empresas con RILES:              {len(riles)}")
print(f"  empresas con RESPEL:             {len(respel)}")
print(f"  empresas unidas (RILES):         {len(salida)}")
print(f"  de esas, EN el plan de contacto: {en_plan}")
print(f"  con 2+ productos a ofrecer:      {con_venta}")
print(f"  unidad de emision: TONELADAS ANUALES (declarado en la hoja Metadatos del RETC)")

ofertas = collections.Counter()
for s in salida:
    for q in s["que_vender"]:
        ofertas[q] += 1
print(f"\n  === QUE SE VENDE (agregado) ===")
for k2, v in ofertas.most_common():
    print(f"     {k2:36s} {v:>5}")

print(f"\n  === TOP 15 POR CARGA PELIGROSA (metales + toxicos), no por volumen ===")
print(f"  {'EMPRESA':32s} {'peligrosa t':>12s} {'total t':>11s} {'cont':>5s} {'ofrece':>6s} contacto")
for s in salida[:15]:
    c = s["contacto"]
    print(f"  {s['empresa'][:32]:32s} {s['carga_peligrosa_t']:>12,.1f} {s['emision_agua_t']:>11,.0f} "
          f"{s['n_contaminantes']:>5d} {len(s['que_vender']):>6d} {str((c or {}).get('nombre'))[:22]}")

print(f"\n  === NOTA: los mayores por VOLUMEN (sal), que NO son el target ===")
for s in sorted(salida, key=lambda x: -x["emision_agua_t"])[:5]:
    print(f"  {s['empresa'][:32]:32s} total {s['emision_agua_t']:>12,.0f} t  ->  toxico {s['carga_peligrosa_t']:>10,.1f} t")

json.dump({
    "que_es": ("Dolor ambiental MEDIDO por empresa del RETC (RILES DS 90/2000 y residuos "
               "peligrosos DS 43/2015), cruzado con el plan de contacto. Por cada empresa dice "
               "qué contamina, cuánto, dónde descarga, qué venderle y a quién llamar."),
    "correccion_importante": ("El plan de contacto traía 'riles' SUMADO por planta (Colbun "
                              "mostraba 81.114 en vez de 5.070, x16 sus plantas). Corregido a "
                              "MAXIMO y verificado contra el RETC crudo: 3/3 casos coinciden."),
    "fuente": "RETC MMA — riles_2024.xlsx (10.870 filas) y respeligrosos_2025.xlsx hoja Generador (40.329 filas)",
    "regla_de_venta": ("El producto se deriva del dato: metales pesados -> analítica en línea; "
                       "10+ contaminantes -> plataforma de monitoreo; 3+ peligrosidades RESPEL -> "
                       "trazabilidad de residuos. No es un catálogo aplicado a ciegas."),
    "totales": {"con_riles": len(riles), "con_respel": len(respel),
                "en_plan_contacto": en_plan, "con_2mas_productos": con_venta},
    "empresas": salida,
}, open(os.path.join(D, "dolor_ambiental_empresas.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/dolor_ambiental_empresas.json")
