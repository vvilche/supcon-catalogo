#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAN DE CONTACTO: a quién llamar y en qué orden.

Une los dos mundos que estan separados:
  - El universo ampliado (6.945 empresas con dolor MEDIDO y zona) — QUE atacar.
  - Los 1.629 tomadores de decision (nombre, cargo, rol de compra, LinkedIn) — A QUIEN llamar.

La union es por razon social normalizada. El resultado es una lista de llamados ordenada por
prioridad, con el angulo de conversacion de cada uno: el dolor medido de su planta + la linea
que lo resuelve + el rol que esa persona juega en la compra.

LO QUE NO HACE: no inventa emails ni telefonos. Los tomadores traen 0 correos y 0 telefonos
(verificado en las 1.629 fichas). El contacto esta en LinkedIn (90% lo tiene). El plan entrega
el nombre, el cargo, el rol y el perfil para llegar; el enriquecimiento de correo es un paso
aparte y se declara.

Salida: datos/plan_contacto.json
"""
import os, json, glob, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
WS = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s).strip()

STOP = {"s","a","sa","ltda","limitada","spa","cia","compania","sociedad","empresa","de","del",
        "la","el","los","las","y","chile","servicios","comercial","industrial","inversiones"}
def clave(s):
    return " ".join(sorted(t for t in norm(s).split() if t not in STOP and len(t) > 2))

# ---------- 1. cargar el universo (qué atacar) ----------
uni = json.load(open(os.path.join(D, "universo_ampliado.json"), encoding="utf-8"))
emps = uni["empresas"]
print(f"universo: {len(emps):,} empresas")

# ---------- 2. cargar los tomadores (a quién llamar) ----------
tomadores = collections.defaultdict(list)
n_tom = 0
for f in glob.glob(os.path.join(WS, "catalogo-*/research/*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    razon = d.get("empresa")
    if not razon: continue
    for t in (d.get("tomadores") or []):
        if not t.get("nombre"): continue
        tomadores[clave(razon)].append({
          "nombre": t.get("nombre"), "cargo": t.get("cargo"), "tipo": t.get("tipo"),
          "rol_compra": t.get("rol_compra"), "linkedin": t.get("linkedin"),
          "correo": t.get("correo") or "", "telefono": t.get("telefono") or "",
          "fuente": t.get("fuente"),
        })
        n_tom += 1
print(f"tomadores: {n_tom:,} en {len(tomadores):,} empresas")

# ---------- 3. cruzar ----------
# rol de compra: A=Aprobador, D=Decisor, R=Recomendador, CT=Comprador tecnico
ROL = {"A": "Aprobador", "D": "Decisor", "R": "Recomendador", "CT": "Comprador técnico"}
PESO_ROL = {"A": 4, "D": 3, "CT": 2, "R": 1}

# Consolidar por EMPRESA (no por planta). El universo tiene una fila por (razon, comuna), asi
# que la misma persona aparecia repetida: medido, Colbun 12 veces y Ventisqueros 9. Para
# contactar la unidad es la empresa: una persona, una llamada.
#
# BUG CORREGIDO (medido contra el RETC crudo): riles y residuos_t venian con +=, es decir se
# SUMABAN una vez por planta. Pero el valor del RETC es de la EMPRESA (la emision se reporta
# por establecimiento y ya viene agregada en el universo), asi que sumar por planta lo
# multiplicaba por el numero de plantas:
#     Colbun     fuente cruda 5.069,6  ->  suma por planta 81.114   (x16)
#     Codelco    fuente cruda 88.286,4 ->  suma por planta ~353.145 (x4)
# La senal de texto ('RILES al agua 5,070') SI traia el valor correcto, por eso los dos
# numeros se contradecian en el mismo registro. Ahora se toma el MAXIMO (no la suma): las
# filas de la misma empresa traen el mismo valor, y el maximo es ese valor.
agrupado = collections.defaultdict(lambda: {"plantas": [], "dolor": 0.0, "riles": 0.0,
                                            "residuos_t": 0.0, "zonas": set(), "lineas": set(),
                                            "senales": [], "senales_vistas": set(), "rubro": None})
for e in emps:
    k = clave(e["empresa"])
    g = agrupado[k]
    g["empresa"] = e["empresa"]
    g["rubro"] = g["rubro"] or e["rubro"]
    g["plantas"].append({"comuna": e.get("comuna"), "region": e.get("region"),
                         "zona": e.get("zona"), "dolor": e["dolor"]})
    g["dolor"] += e["dolor"]
    # MAXIMO, no suma: el valor es de la empresa y se repite en cada fila de planta.
    g["riles"] = max(g["riles"], e.get("riles") or 0)
    g["residuos_t"] = max(g["residuos_t"], e.get("residuos_t") or 0)
    if e.get("zona"): g["zonas"].add(e["zona"])
    for l in e.get("lineas_supcon", []): g["lineas"].add(l)
    # deduplicar las senales: venian repetidas (219 de 468 empresas tenian 'RILES al agua X'
    # dos veces) porque el universo repite la fila por planta y se hacía append sin control.
    for sg in e.get("senales_dolor", []):
        if sg not in g["senales_vistas"]:
            g["senales_vistas"].add(sg)
            g["senales"].append(sg)

plan = []
sin_tomador = 0
for k, g in agrupado.items():
    toms = tomadores.get(k, [])
    if not toms:
        sin_tomador += 1
        continue
    toms_s = sorted(toms, key=lambda t: -PESO_ROL.get(t.get("rol_compra"), 0))
    principal = toms_s[0]
    # zona principal: la de mayor dolor entre sus plantas (es donde entra el equipo primero)
    plantas_s = sorted(g["plantas"], key=lambda x: -x["dolor"])
    plan.append({
      "empresa": g["empresa"], "rubro": g["rubro"],
      "zona": plantas_s[0]["zona"], "zonas": sorted(g["zonas"]),
      "comuna": plantas_s[0]["comuna"], "region": plantas_s[0]["region"],
      "n_plantas": len(g["plantas"]), "plantas": plantas_s,
      # El dolor de la EMPRESA es el promedio por planta, no la suma: si no, una cadena con 105
      # plantas chicas (estaciones de servicio) supera a Codelco con 11 plantas industriales.
      # Se reportan los tres numeros para que el vendedor decida.
      "dolor": round(g["dolor"] / max(len(g["plantas"]), 1), 1),
      "dolor_total": round(g["dolor"], 1),
      "dolor_max_planta": round(max(p["dolor"] for p in g["plantas"]), 1),
      "senales": g["senales"][:4],
      "lineas": sorted(g["lineas"]),
      "riles": round(g["riles"], 1), "residuos_t": round(g["residuos_t"], 1),
      "tomadores": toms_s,
      "n_tomadores": len(toms_s),
      "rol_principal": ROL.get(principal.get("rol_compra"), "—"),
      "contacto_principal": {"nombre": principal.get("nombre"), "cargo": principal.get("cargo"),
                             "linkedin": principal.get("linkedin")},
      "angulo": None,
    })

print(f"empresas con tomador identificado: {len(plan):,}")
print(f"empresas SIN tomador (solo empresa): {sin_tomador:,}")

# ---------- 4. el ángulo de conversación ----------
def angulo(p):
    partes = []
    if p.get("riles"):
        partes.append(f"emite al agua {p['riles']:,.0f} (DS 90/2000): hoy no lo mide en línea")
    if p.get("residuos_t"):
        partes.append(f"genera {p['residuos_t']:,.0f} t de residuos peligrosos (DS 43/2015)")
    if not partes:
        return "dolor declarado por registro, sin señal de agua ni residuos"
    return " · ".join(partes)

for p in plan:
    p["angulo"] = angulo(p)

# ---------- 5. ordenar y separar ----------
# prioridad = dolor x peso del rol principal (llegar al que decide vale más que al recomendador)
for p in plan:
    peso = PESO_ROL.get(next((t.get("rol_compra") for t in p["tomadores"]
                              if t.get("rol_compra")), ""), 1)
    p["prioridad_contacto"] = round(p["dolor"] * peso, 1)

# ordenar por prioridad; una empresa con MUCHAS plantas sube un poco (mas volumen de proyecto),
# pero con peso acotado para que no domine el ranking
import math
for p in plan:
    p["prioridad_contacto"] = round(p["prioridad_contacto"] + min(math.log10(p["n_plantas"]+1), 1.0), 1)
plan.sort(key=lambda p: -p["prioridad_contacto"])

# por zona
por_zona = collections.Counter(p["zona"] or "sin zona" for p in plan)
por_rol = collections.Counter(p["rol_principal"] for p in plan)
con_li = sum(1 for p in plan if p["contacto_principal"].get("linkedin"))
con_mail = sum(1 for p in plan if any(t.get("correo") for t in p["tomadores"]))

print(f"\n=== PLAN DE CONTACTO ===")
print(f"  empresas con nombre y cargo:  {len(plan):,}")
print(f"  con LinkedIn del contacto:    {con_li:,} ({con_li/len(plan)*100:.0f}%)")
print(f"  con correo:                   {con_mail:,} ({con_mail/len(plan)*100:.0f}%)")
print(f"\n  por rol del contacto principal:")
for k, v in por_rol.most_common(): print(f"    {k:20s} {v:>5,}")
print(f"\n  por zona:")
for k in ["Z1","Z2","Z3","Z4","Z5","Z6","Z7","sin zona"]:
    if k in por_zona: print(f"    {k:9s} {por_zona[k]:>5,}")

print(f"\n=== TOP 25 A LLAMAR ===")
print(f"{'#':>3s} {'EMPRESA':38s} {'CARGO':28s} {'ROL':16s} {'dolor':>5s} {'prio':>6s} zona")
print("-"*116)
for i, p in enumerate(plan[:25], 1):
    cp = p["contacto_principal"]
    print(f"{i:>3d} {str(p['empresa'])[:38]:38s} {str(cp['cargo'])[:28]:28s} "
          f"{p['rol_principal'][:16]:16s} {p['dolor']:>5.0f} {p['prioridad_contacto']:>6.0f} {p['zona'] or '-'}")

json.dump({
 "metodo": ("Union del universo ampliado (6.945 empresas con dolor MEDIDO) con los 1.629 "
   "tomadores de decision del catálogo, por razón social normalizada. El plan ordena por "
   "dolor × peso del rol de compra: llegar al decisor vale más que al recomendador. Cada "
   "llamado trae el nombre, el cargo, el rol y el ángulo de conversación (el dolor medido "
   "de su planta traducido a fraseo comercial)."),
 "lo_que_no_hace": ("NO inventa correos ni teléfonos. Los 1.629 tomadores traen 0 correos y 0 "
   "teléfonos (verificado); el 90% tiene LinkedIn. Enriquecer el correo es un paso aparte."),
 "resumen": {
   "empresas_con_tomador": len(plan),
   "empresas_sin_tomador": sin_tomador,
   "con_linkedin": con_li, "con_correo": con_mail,
   "por_rol": dict(por_rol), "por_zona": dict(por_zona),
   "total_tomadores": n_tom,
 },
 "rol_compra": ROL,
 "plan": plan,
}, open(os.path.join(D,"plan_contacto.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/plan_contacto.json")
