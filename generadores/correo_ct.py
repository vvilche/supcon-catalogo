#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORREO DE LOS COMPRADORES TÉCNICOS (CT), deducido del patrón REAL de cada empresa.

EL PROBLEMA
------------------------------------------------------------------------------
Los 577 contactos CT del plan técnico traen nombre, cargo y LinkedIn, pero 0 correos. Y los CT
son los que importan: para instrumentación y control, el que especifica abre la puerta y el
gerente firma después.

EL MÉTODO (no se inventa el correo, se deduce el PATRÓN)
------------------------------------------------------------------------------
La cosecha del Coordinador dio 1.353 correos REALES de 449 dominios (nombre + correo, de
planillas oficiales). De ahí se saca, POR EMPRESA, cuál es el patrón que esa empresa usa:
    inicial_apellido        jcancino@transelec.cl
    nombre.apellido         juan.munoz@engie.com
    inicial.apellido        j.perez@...
    nombre_apellido         juanperez@...
etc. Ese patrón se mide sobre correos reales, no se supone.

Después se aplica el patrón al nombre del CT. El resultado se marca SIEMPRE como INFERIDO,
nunca como verificado: el patrón es real, el correo resultante es una deducción.

VERIFICACIÓN OBLIGATORIA
------------------------------------------------------------------------------
Antes de usar el método se prueba contra casos conocidos de punta a punta: para cada persona
de la cosecha, se deduce su correo con el patrón de su empresa (excluyéndola del cálculo) y se
compara con el correo real. Eso mide la TASA DE ACIERTO del patrón, que es el dato que dice si
esto sirve o no.
"""
import json, os, re, collections, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


def partes(nombre):
    """(primer_nombre, apellido_paterno) de un nombre chileno. Limpia titulos e iniciales."""
    SUF = {"pmp", "mba", "msc", "ing", "sr", "sra", "don", "dra", "dr", "mg", "mag", "pe",
           "pmi", "cisa", "cia", "cpa", "phd", "esp", "tec", "ex", "jr", "ii", "iii", "iv",
           "snr", "leed", "mf"}
    s = norm(nombre or "")
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[.,;/]", " ", s)
    toks = []
    for t in s.split():
        if t in SUF or len(t) < 2 or re.fullmatch(r"[ivx]+", t):
            continue
        toks.append(t)
    if len(toks) < 2:
        return "", ""
    return toks[0], toks[-1]


# ===========================================================================
# 1. PATRONES: como se construye un local-part a partir de (nombre, apellido)
# ===========================================================================
PATRONES = {
    "inicial_apellido":     lambda f, l: f[0] + l,
    "nombre.apellido":      lambda f, l: f + "." + l,
    "inicial.apellido":     lambda f, l: f[0] + "." + l,
    "nombre_apellido":      lambda f, l: f + l,
    "nombre-apellido":      lambda f, l: f + "-" + l,
    "apellido":             lambda f, l: l,
    "nombre":               lambda f, l: f,
    "apellido.nombre":      lambda f, l: l + "." + f,
    "apellido_inicial":     lambda f, l: l + f[0],
    "inicial_apellido_inicial": lambda f, l: f[0] + l[0],
    # --- agregados DESPUES de medir los patrones reales que faltaban ---
    # Medido en Codelco y Colbun, que daban "sin patron":
    #   jpgutierrez@colbun.cl  (Javiera Gutierrez) -> inicial+inicial+apellido
    #   jescobart@colbun.cl    (Jose Escobar)      -> truncamiento, no se modela
    #   cvald027@codelco.cl    (Carolina Valderrama) -> inicial + 3 letras + 3 digitos
    #   Mauricio.Alvarez@codelco.cl -> nombre.apellido con mayusculas
    "inicial_inicial_apellido": lambda f, l: f[0] + (f[1] if len(f) > 1 else "") + l,
    "inicial_apellido3_dig": lambda f, l: f[0] + l[:3],
    "nombre_apellido_dig":  lambda f, l: f[0] + l[:4],
}


def detectar_patron(local, nombre):
    """Dado un local-part real y el nombre, devuelve que patron es (o None)."""
    f, l = partes(nombre)
    if not f or not l:
        return None
    loc = norm(local)
    for k, fn in PATRONES.items():
        if fn(f, l) == loc:
            return k
    return None


# ===========================================================================
# 2. VALIDACION: predecir el correo de gente que YA conocemos
# ===========================================================================
def validar(cen, min_ejemplos=1, holdout=True):
    """Por cada empresa con correos reales, deduce el patron y se prueba a si misma.

    holdout=True: el patron se calcula excluyendo a la persona que se evalua (leave-one-out).
    Ese es el test honesto: mide si el patron de la empresa predice a un individuo NUEVO.
    """
    por_dom = {}
    for dom, lista in cen["por_dominio"].items():
        items = []
        for x in lista:
            loc = (x.get("correo") or "").split("@")[0]
            if not loc or not x.get("nombre"):
                continue
            p = detectar_patron(loc, x["nombre"])
            if p:
                items.append({"nombre": x["nombre"], "local": norm(loc), "patron": p})
        if len(items) >= min_ejemplos:
            por_dom[dom] = items

    aciertos = fallos = sin_patron = 0
    ejemplos_mal = []
    por_patron_ok = collections.Counter()
    for dom, items in por_dom.items():
        for i, it in enumerate(items):
            resto = [x for j, x in enumerate(items) if j != i] if holdout else items
            if not resto:
                sin_patron += 1
                continue
            # patron mayoritario de la empresa (sin la persona evaluada)
            c = collections.Counter(x["patron"] for x in resto)
            pat = c.most_common(1)[0][0]
            f, l = partes(it["nombre"])
            pred = PATRONES[pat](f, l)
            if pred == it["local"]:
                aciertos += 1
                por_patron_ok[pat] += 1
            else:
                fallos += 1
                if len(ejemplos_mal) < 12:
                    ejemplos_mal.append((dom, it["nombre"], it["local"], pat, pred))
    return aciertos, fallos, sin_patron, por_dom, por_patron_ok, ejemplos_mal


cen = json.load(open(os.path.join(D, "cen_coordinados_correos.json"), encoding="utf-8"))
print("=" * 84)
print("VALIDACIÓN DEL MÉTODO (leave-one-out sobre correos REALES)")
print("=" * 84)
ac, fa, sp, por_dom, por_pat_ok, malos = validar(cen)
tot = ac + fa
print(f"  empresas con patrón detectable: {len(por_dom)}")
print(f"  predicciones evaluadas:         {tot}")
print(f"  ACIERTOS:                       {ac}  ({ac/tot*100:.1f}%)" if tot else "  sin datos")
print(f"  fallos:                         {fa}")
print(f"\n  === TASA DE ACIERTO POR PATRÓN ===")
for p, v in por_pat_ok.most_common():
    print(f"     {p:28s} {v:>4} aciertos")
print(f"\n  === EJEMPLOS DE FALLO (para ver por qué) ===")
for dom, nom, real, pat, pred in malos:
    print(f"     {nom[:26]:28s} real={real:26s} pred={pred:26s} patrón={pat}  [{dom}]")
