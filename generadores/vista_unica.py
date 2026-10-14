#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VISTA ÚNICA: EMPRESA → QUÉ COMPRAR → A QUIÉN  (el cruce de los 4 datos)

QUÉ UNE (y por qué antes no se podía)
------------------------------------------------------------------------------
Cuatro bases que se construyeron por separado y NO cruzaban entre sí por nombre:
  1. DOLOR       mineras_retc.json (220 mineras, residuos peligrosos) +
                 matriz_dolor_linea_perfil.json (370 empresas, RILES + línea + producto)
  2. DECISORES   buscador_decisores.json (personas con cargo y LinkedIn)
  3. COMPRAS     ecrm_supcon.json (las 18 cuentas que pidieron cotización 2023-2025, con monto)
  4. CONTACTO    compradores_linkedin.json (183 personas que compraron de verdad)

EL PROBLEMA DEL CRUCE (y cómo se resuelve)
------------------------------------------------------------------------------
El eCRM usa SIGLAS internas ("MLP", "Andina") y las otras bases usan RAZÓN SOCIAL
("MINERA LOS PELAMBRES", "CORP NACIONAL DEL COBRE DE CHILE"). Sin alias, el cruce da CERO — y
daba cero justo para las cuentas más grandes, que es lo que reveló que faltaba la gran minería.

Se resuelve con ALIAS_ECRM (sigla -> patrón de razón social), verificado caso a caso.

SALIDA: datos/vista_cliente_producto_persona.json + artefactos/cliente_producto_persona.html
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def load(p, default=None):
    fp = os.path.join(D, p)
    if not os.path.exists(fp):
        return default
    return json.load(open(fp, encoding="utf-8"))


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


# sigla del eCRM -> patrón de razón social (verificado)
ALIAS_ECRM = {
    "MLP": "minera los pelambres", "Andina": "cobre", "Salvador": "cobre",
    "Codelco": "cobre", "Chuquicamata": "cobre", "El Teniente": "cobre",
    "Candelaria": "candelaria", "Escondida": "escondida", "Collahuasi": "collahuasi",
    "Caserones": "lumina", "CMP": "pacifico", "Pucobre": "pucobre",
    "Kinross": "kinross", "Enami": "enami", "Anglo": "anglo american sur",
    "Verne SPA": "centinela", "Ventana": "ventana", "SGS": "sgs", "Molymetnos": "molymet",
    "JRI": "jri", "Tecnasic": "tecnasic", "SQM": "quimica y minera",
    "Potrerillos": "potrerillos", "Goldfields": "gold fields",
}

# --- cargar las 4 bases ---
mineras = (load("mineras_retc.json") or {}).get("mineras", [])
matriz = (load("matriz_dolor_linea_perfil.json") or {}).get("empresas", [])
decisores = (load("buscador_decisores.json") or {}).get("resultados", [])
ecrm = (load("ecrm_supcon.json") or {}).get("clientes_hoy", {})
compradores = (load("compradores_linkedin.json") or {}).get("compradores", [])

idx_dec = {norm(x["empresa"]): x for x in decisores}
idx_mat = {norm(x["empresa"]): x for x in matriz}

# compradores del eCRM agrupados por empresa (sigla)
comp_por_sigla = collections.defaultdict(list)
for c in compradores:
    comp_por_sigla[c.get("empresa", "")].append(c)


def buscar_idx(idx, patron):
    for k, v in idx.items():
        if patron in k:
            return v
    return None


def buscar_minera(patron):
    for m in mineras:
        if patron in norm(m["empresa"]):
            return m
    return None


# --- armar la vista ---
filas = []
vistos = set()

# 1) las cuentas que YA COMPRARON (lo más valioso: monto real)
for sigla, x in ecrm.items():
    pat = ALIAS_ECRM.get(sigla)
    if not pat:
        continue
    mn = buscar_minera(pat)
    mt = buscar_idx(idx_mat, pat)
    bd = buscar_idx(idx_dec, pat)
    emp_nombre = (mn or {}).get("empresa") or (bd or {}).get("empresa") or (mt or {}).get("empresa") or sigla
    k = norm(emp_nombre)
    if k in vistos:
        continue
    vistos.add(k)
    filas.append({
        "empresa": emp_nombre, "sigla_ecrm": sigla,
        "usd_cotizado": x["usd_cotizado"], "usd_ganado": x["usd_oc"],
        "n_oc": x["oc"],
        "respel_t": (mn or {}).get("respel_t") or (mt or {}).get("carga_peligrosa_t") or 0,
        "lineas": [L["linea"] for L in (mt or {}).get("lineas", [])],
        "productos": [p for L in (mt or {}).get("lineas", []) for p in L["productos"]][:8],
        "decisores": (bd or {}).get("hallazgos", []),
        "n_decisores": (bd or {}).get("n_decisores", 0),
        "compradores_reales": [{"nombre": c["nombre"], "linkedin": c.get("linkedin", "")}
                               for c in comp_por_sigla.get(sigla, [])][:6],
    })

# 2) las mineras con dolor que NO están en el eCRM (la gran minería recuperada)
for m in mineras:
    k = norm(m["empresa"])
    if k in vistos:
        continue
    mt = buscar_idx(idx_mat, k)
    bd = buscar_idx(idx_dec, k)
    if not (m["respel_t"] > 1000 or bd):
        continue
    vistos.add(k)
    filas.append({
        "empresa": m["empresa"], "sigla_ecrm": "",
        "usd_cotizado": 0, "usd_ganado": 0, "n_oc": 0,
        "respel_t": m["respel_t"],
        "lineas": [L["linea"] for L in (mt or {}).get("lineas", [])],
        "productos": [p for L in (mt or {}).get("lineas", []) for p in L["productos"]][:8],
        "decisores": (bd or {}).get("hallazgos", []),
        "n_decisores": (bd or {}).get("n_decisores", 0),
        "compradores_reales": [],
    })

filas.sort(key=lambda x: -(x["usd_cotizado"] or 0) - (x["respel_t"] or 0) / 1000)

con_dec = [f for f in filas if f["n_decisores"]]
print("=" * 100)
print("VISTA ÚNICA: EMPRESA → QUÉ COMPRAR → A QUIÉN")
print("=" * 100)
print(f"  empresas en la vista: {len(filas)}")
print(f"  con decisores:        {len(con_dec)}")
print(f"  con compras reales:   {sum(1 for f in filas if f['usd_cotizado'])}")
print(f"  con línea asignada:   {sum(1 for f in filas if f['lineas'])}")
print(f"\n  {'empresa':40s} {'US$':>11s} {'dolor t':>11s} {'dec':>4s}  líneas")
for f in filas[:22]:
    print(f"  {f['empresa'][:38]:40s} {f['usd_cotizado']:>11,.0f} {f['respel_t']:>11,.1f} "
          f"{f['n_decisores']:>4}  {', '.join(f['lineas'])[:28]}")

json.dump({
    "que_es": ("Vista única por empresa: cuánto compró (eCRM), cuánto dolor declaró (RETC), "
               "qué línea le sirve (matriz) y quiénes deciden (buscador)."),
    "el_problema_que_resuelve": ("El eCRM usa siglas y las otras bases razón social: sin alias el "
                                 "cruce daba CERO, justo en las cuentas más grandes."),
    "totales": {"empresas": len(filas), "con_decisores": len(con_dec),
                "con_compras_reales": sum(1 for f in filas if f["usd_cotizado"])},
    "empresas": filas,
}, open(os.path.join(D, "vista_cliente_producto_persona.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/vista_cliente_producto_persona.json")
