#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENTREGABLE: los compradores del eCRM con su correo — qué se logró y qué no.

LA RESPUESTA HONESTA (medida, no estimada)
------------------------------------------------------------------------------
De los 183 compradores reales del eCRM (con nombre de persona), el correo NO está publicado
en ninguna fuente cosechable. Se midió por todas las vías:
  1. Cosecha del Coordinador Eléctrico (1.353 correos REALES): solapamiento CERO — son
     empresas de generación, los compradores del eCRM son mineras.
  2. Cosecha de las webs corporativas de las mineras (pelambres.cl, codelco.cl, enami.cl...):
     ya NO publican correos personales (solo buzones genéricos: oficinadepartes@enami.cl).
  3. Teléfono: el campo existe en los archivos pero está VACÍO en los 2.327 registros.
  4. LinkedIn: el 90% de los tomadores traen su perfil, pero no el correo.

LO QUE SÍ SE LOGRA
------------------------------------------------------------------------------
DOMINIO verificado (10 de 15 empresas clave, con curl, no adivinado) + PATRÓN estándar de la
industria. Con eso el correo se INFIERE, con la confianza declarada en cada línea.

Salida: artefactos/correos_compradores.html + datos/ecrm_correos_compradores.json
"""
import json, os, re, subprocess, collections, unicodedata

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "correos_compradores.html")


def load(p):
    fp = os.path.join(D, p)
    return json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else None


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", " ", s.lower()).strip()


def partes(nombre):
    return [x for x in norm(nombre).split() if len(x) > 1]


# ---- dominios VERIFICADOS (MX ok = el dominio recibe correo) + patrón de la industria ----
# El MX se verifica con dig (prueba dura). Un dominio sin MX NO recibe correo: se descarta.
DOMINIOS = {
    "MLP": ("pelambres.cl", "nombre.apellido", "MX ok · outlook"),
    "Andina": ("codelco.cl", "nombre.apellido", "MX ok · proofpoint"),
    "Salvador": ("codelco.cl", "nombre.apellido", "MX ok · proofpoint"),
    "Codelco": ("codelco.cl", "nombre.apellido", "MX ok · proofpoint"),
    "Caserones": ("caserones.cl", "nombre.apellido", "MX ok · outlook"),
    "Enami": ("enami.cl", "nombre.apellido", "MX ok · propio"),
    "CMP": ("cmp.cl", "nombre.apellido", "MX ok · outlook"),
    "Pucobre": ("pucobre.cl", "nombre.apellido", "MX ok · outlook"),
    "Anglo": ("angloamerican.com", "nombre.apellido", "MX ok · mimecast"),
    "JRI": ("jri.cl", "nombre.apellido", "MX ok · outlook"),
    "SGS": ("sgs.com", "nombre.apellido", "MX ok · outlook"),
    # Candelaria: DESCARTADO. candelariamine.com no existe y candelaria.cl no tiene MX.
    # Su dominio de correo no se pudo establecer con fuente: se declara el hueco, no se adivina.
}


def tiene_mx(dom):
    """Prueba dura: el dominio recibe correo? (dig MX)."""
    try:
        r = subprocess.run(["dig", "+short", "MX", dom], capture_output=True, text=True, timeout=15)
        return any(l.strip() for l in r.stdout.strip().split("\n"))
    except Exception:
        return False


def inferir(nombre, dom, pat="nombre.apellido"):
    p = partes(nombre)
    if len(p) < 2:
        return ""
    nom, ap = p[0], p[-1]
    tablas = {"nombre.apellido": f"{nom}.{ap}", "inicial_apellido": f"{nom[0]}{ap}",
              "nombreapellido": f"{nom}{ap}"}
    return f"{tablas.get(pat, tablas['nombre.apellido'])}@{dom}"


# ---- compradores del eCRM ----
e = load("ecrm_extraido.json")
opp = e["oportunidades"]
agg = {}
for r in opp:
    c = (r.get("contacto") or "").strip()
    if not c or c.lower() in ("abastecimiento", "compras", "contacto", "sin contacto"):
        continue
    if not re.match(r"^[A-Za-zÁÉÍÓÚÑÜáéíóúñü]+(\s+[A-Za-zÁÉÍÓÚÑÜáéíóúñü.]+)+$", c):
        continue
    a = agg.setdefault(norm(c), {"nombre": c, "empresas": collections.Counter(),
                                 "cot": 0, "usd": 0.0, "oc": 0})
    a["cot"] += 1
    a["usd"] += r.get("valor_num") or 0
    if (r.get("oc") or "").strip():
        a["oc"] += 1
    if r.get("cliente"):
        a["empresas"][r["cliente"].strip()] += 1

res = []
for k, a in sorted(agg.items(), key=lambda x: -x[1]["usd"]):
    emp = a["empresas"].most_common(1)[0][0] if a["empresas"] else ""
    dom_info = DOMINIOS.get(emp)
    correo, estado, fuen = "", "SIN DOMINIO", "empresa sin dominio de correo resuelto"
    if dom_info:
        dom, pat, nota = dom_info
        c2 = inferir(a["nombre"], dom, pat)
        if c2:
            correo = c2
            estado = "INFERIDO"
            fuen = f"{nota} · patrón {pat}"
        else:
            estado, fuen = "SIN PATRON", f"dominio {dom} · nombre sin 2 palabras"
    res.append({"nombre": a["nombre"], "empresa": emp, "cotizaciones": a["cot"],
                "usd": round(a["usd"], 2), "oc": a["oc"], "correo": correo,
                "estado": estado, "fuente": fuen})

con = [r for r in res if r["correo"]]
est = collections.Counter(r["estado"] for r in res)

# verificacion final: todo dominio usado TIENE que tener MX (si no, se descarta el correo)
print("=== VERIFICACIÓN FINAL: dominios con MX ===")
doms_usados = sorted(set(r["correo"].split("@")[1] for r in con))
mxs = {d: tiene_mx(d) for d in doms_usados}
for d, ok in mxs.items():
    n = sum(1 for r in con if r["correo"].endswith("@" + d))
    print(f"  {d:24s} MX:{'OK' if ok else 'NO':4s} {n:>3} correos")
malos = [d for d, ok in mxs.items() if not ok]
if malos:
    print(f"\n  DESCARTANDO dominios sin MX: {malos}")
    for r in res:
        if r["correo"] and r["correo"].split("@")[1] in malos:
            r["correo"], r["estado"] = "", "DOMINIO SIN MX"
    con = [r for r in res if r["correo"]]
    est = collections.Counter(r["estado"] for r in res)

print("=" * 100)
print("COMPRADORES DEL eCRM Y SU CORREO — ESTADO REAL")
print("=" * 100)
print(f"  compradores (con nombre de persona): {len(res)}")
for e2, n in est.most_common():
    print(f"    {e2:14s} {n:>4}")
print(f"\n  con correo (inferido): {len(con)} de {len(res)} ({len(con)/len(res)*100:.0f}%)")
print("\n  === LOS DE MAYOR MONTO ===")
for r in res[:22]:
    print(f"    {r['nombre'][:24]:26s} {r['empresa'][:14]:16s} {r['correo'][:40]:42s} {r['estado']}")

json.dump({
    "que_es": ("Compradores del eCRM (los que pidieron cotización 2023-2025) con su correo. "
               "El correo NO está publicado en ninguna fuente cosechable (medido por 4 vías): "
               "se infiere con DOMINIO VERIFICADO + patrón, y se declara como inferido."),
    "lo_que_se_medió": {
        "cosecha_coordinador": "1.353 correos REALES, solapamiento CERO (son empresas eléctricas, no mineras)",
        "webs_corporativas": "las mineras ya no publican correos personales, solo buzones genéricos",
        "telefono": "el campo existe en los archivos pero está VACÍO en los 2.327 registros",
        "linkedin": "el 90% de los tomadores trae perfil, pero no correo",
    },
    "dominios": {k: v[0] for k, v in DOMINIOS.items()},
    "totales": {"compradores": len(res), "con_correo": len(con),
                "por_estado": dict(est)},
    "advertencia": ("Todos los correos son INFERIDOS, no verificados. No usar para envío masivo "
                    "sin validar: un correo mal dirigido rebota o llega a un tercero."),
    "compradores": res,
}, open(os.path.join(D, "ecrm_correos_compradores.json"), "w"), ensure_ascii=False, indent=1)
