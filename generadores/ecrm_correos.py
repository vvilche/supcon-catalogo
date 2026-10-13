#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORREOS DE LOS COMPRADORES DEL eCRM (2023-2025).

EL PROBLEMA
------------------------------------------------------------------------------
El eCRM de INECO trae 211 contactos con NOMBRE y su empresa (la que pidió la cotización).
Ninguno tiene correo. Son los compradores REALES — los que pidieron cotización y muchos los que
dieron la orden de compra.

LA MÁQUINA QUE YA EXISTE (no se reinventa)
------------------------------------------------------------------------------
1. `datos/cen_coordinados_correos.json`  → 1.353 CORREOS REALES de 449 dominios, cosechados de
   las planillas oficiales del Coordinador Eléctrico. Dato duro, auditable.
2. `datos/correos_ct.json` → motor de inferencia por PATRÓN de empresa, medido al 90,9% con
   leave-one-out. Requiere DOMINIO + PATRÓN.

LO QUE FALTABA
------------------------------------------------------------------------------
El eCRM nunca se pasó por esa máquina. Y el cuello de botella no es el patrón: es el DOMINIO
(el patrón se deriva de la empresa, el dominio hay que tenerlo).

ESTRATEGIA (en orden de dureza del dato)
------------------------------------------------------------------------------
A) COSECHAR: si el nombre del eCRM aparece en la cosecha del Coordinador → correo REAL.
B) INFERIR: si la empresa del eCRM tiene dominio + patrón conocido → correo inferido con
   confianza declarada.
C) MARCAR HUECO: si falta dominio o patrón, se dice. No se inventa.

Salida: datos/ecrm_correos_compradores.json
"""
import json, os, re, collections, unicodedata

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")


def load(p):
    fp = os.path.join(D, p)
    return json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else None


def norm(s):
    """Normaliza para comparar nombres: sin tildes, minúscula, solo letras."""
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", " ", s.lower()).strip()


def partes(nombre):
    """Nombre -> (pila, apellidos) descartando iniciales y partículas."""
    t = [x for x in norm(nombre).split() if len(x) > 1]
    return t


# ---------------------------------------------------------------------------
# 1. LA COSECHA (correos REALES)
# ---------------------------------------------------------------------------
cen = load("cen_coordinados_correos.json")
por_dom = cen.get("por_dominio", {}) if cen else {}

# indice: nombre normalizado -> (correo, dominio, empresa)  [solo correos REALES]
# ESTRUCTURA REAL: por_dominio = {dominio: [ {nombre, correo, rol, empresa}, ... ]}
reales_por_nombre = {}
for dom, lista in por_dom.items():
    if not isinstance(lista, list):
        continue
    for reg in lista:
        if not isinstance(reg, dict):
            continue
        nom = reg.get("nombre") or ""
        mail = reg.get("correo") or ""
        if nom and mail and "@" in mail:
            reales_por_nombre.setdefault(norm(nom), (mail, dom, reg.get("empresa", "")))

print(f"cosecha: {len(reales_por_nombre):,} nombres con correo REAL ({len(por_dom)} dominios)")

# ---------------------------------------------------------------------------
# 2. PATRONES POR EMPRESA (para inferir)
# ---------------------------------------------------------------------------
ct = load("correos_ct.json") or {}
patrones = {}
for dom, info in (ct.get("patrones_por_dominio") or {}).items():
    patrones[dom] = (info.get("patron"), info.get("n", 0),
                     info.get("ejemplos", [])[:2])

# dominios de fuente dura
dd = load("dominios_duros.json") or {}
dominios_emp = {}
for emp, info in (dd.get("empresas") or {}).items():
    if info.get("dominio"):
        dominios_emp[norm(emp)] = info["dominio"]

# también dominios de la propia cosecha (la empresa aparece con su dominio)
for dom, lista in por_dom.items():
    if isinstance(lista, list) and lista:
        emp = norm((lista[0] or {}).get("empresa") or "")
        if emp:
            dominios_emp.setdefault(emp, dom)


def dominio_de(empresa):
    n = norm(empresa)
    if n in dominios_emp:
        return dominios_emp[n]
    toks = [t for t in n.split() if len(t) > 2]
    # match por 2+ tokens distintivos
    for e2, d2 in dominios_emp.items():
        if sum(1 for t in toks if t in e2) >= 2:
            return d2
    return None


def inferir(nombre, dominio):
    """Aplica el patrón del dominio. Devuelve (correo, confianza, patron)."""
    if not dominio or dominio not in patrones:
        return "", "SIN PATRON", None
    pat, nn, ej = patrones[dominio]
    p = partes(nombre)
    if len(p) < 2:
        return "", "SIN PATRON", pat
    nom, ap = p[0], p[-1]
    tablas = {
        "nombre.apellido": f"{nom}.{ap}",
        "inicial_apellido": f"{nom[0]}{ap}",
        "nombreapellido": f"{nom}{ap}",
        "nombre_apellido": f"{nom}_{ap}",
        "apellido.nombre": f"{ap}.{nom}",
        "inicial.apellido": f"{nom[0]}.{ap}",
    }
    local = tablas.get(pat)
    if not local:
        return "", "SIN PATRON", pat
    conf = "ALTA" if nn >= 3 else ("MEDIA" if nn >= 1 else "BAJA")
    return f"{local}@{dominio}", conf, pat


# ---------------------------------------------------------------------------
# 3. LOS COMPRADORES DEL eCRM
# ---------------------------------------------------------------------------
e = load("ecrm_extraido.json")
opp = e["oportunidades"]

# por contacto: sus empresas, cuantas cotizaciones, monto, y si tiene OC
agg = {}
for r in opp:
    c = (r.get("contacto") or "").strip()
    if not c or c.lower() in ("abastecimiento", "compras", "contacto", "sin contacto"):
        continue
    if not re.match(r"^[A-Za-zÁÉÍÓÚÑÜáéíóúñü]+(\s+[A-Za-zÁÉÍÓÚÑÜáéíóúñü.]+)+$", c):
        continue
    k = norm(c)
    a = agg.setdefault(k, {"nombre": c, "empresas": collections.Counter(), "cot": 0,
                           "usd": 0.0, "oc": 0})
    a["cot"] += 1
    a["usd"] += r.get("valor_num") or 0
    if (r.get("oc") or "").strip():
        a["oc"] += 1
    if r.get("cliente"):
        a["empresas"][r["cliente"].strip()] += 1

print(f"\neCRM: {len(agg)} compradores distintos (con nombre de persona)")

res = []
for k, a in sorted(agg.items(), key=lambda x: -x[1]["usd"]):
    emp = a["empresas"].most_common(1)[0][0] if a["empresas"] else ""
    # A) cosecha
    correo, estado, fuente = "", "SIN DOMINIO", ""
    if k in reales_por_nombre:
        correo, _, _ = reales_por_nombre[k]
        estado, fuente = "REAL (cosechado)", "Coordinador Eléctrico"
    else:
        dom = dominio_de(emp)
        if dom:
            c2, conf, pat = inferir(a["nombre"], dom)
            if c2:
                correo, estado = c2, f"INFERIDO ({conf})"
                fuente = f"patron {pat} de {dom}"
            else:
                estado, fuente = "SIN PATRON", f"dominio {dom} sin patron medido"
        else:
            estado, fuente = "SIN DOMINIO", "empresa sin dominio de fuente"
    res.append({"nombre": a["nombre"], "empresa_eCRM": emp, "cotizaciones": a["cot"],
                "usd": round(a["usd"], 2), "oc": a["oc"], "correo": correo,
                "estado": estado, "fuente": fuente})

print("\n" + "=" * 100)
print("COMPRADORES DEL eCRM Y SU CORREO")
print("=" * 100)
c_est = collections.Counter(r["estado"].split(" (")[0] for r in res)
for e2, n in c_est.most_common():
    print(f"  {e2:18s} {n:>4}")
print()
for r in res[:30]:
    est = r["estado"].replace("INFERIDO (", "").replace(")", "").replace("REAL (cosechado", "REAL")
    print(f"  {r['nombre'][:26]:28s} {r['empresa_eCRM'][:16]:18s} {r['correo'][:38]:40s} {est}")

con = [r for r in res if r["correo"]]
print(f"\n  CON correo: {len(con)} de {len(res)} ({len(con)/len(res)*100:.0f}%)")
reales = [r for r in res if "REAL" in r["estado"]]
print(f"  de esos, REALES cosechados: {len(reales)} | inferidos: {len(con)-len(reales)}")

json.dump({
    "que_es": ("Correo de los compradores del eCRM de INECO (los que pidieron cotización "
               "2023-2025). Se cosecha de fuente real cuando el nombre aparece en el "
               "Coordinador Eléctrico; si no, se infiere con el patrón medido de su empresa."),
    "metodo": {"A_cosecha": "nombre en la cosecha del Coordinador -> correo REAL",
               "B_inferencia": "dominio conocido + patrón de la empresa (90,9% medido)",
               "C_hueco": "sin dominio o sin patrón: se declara, no se inventa"},
    "totales": {"compradores": len(res), "con_correo": len(con),
                "reales": len(reales), "inferidos": len(con) - len(reales),
                "por_estado": dict(c_est)},
    "advertencia": ("Un correo INFERIDO no está verificado. No usar para envío masivo: un correo "
                    "mal dirigido rebota o llega a un tercero."),
    "compradores": res,
}, open(os.path.join(D, "ecrm_correos_compradores.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/ecrm_correos_compradores.json")
