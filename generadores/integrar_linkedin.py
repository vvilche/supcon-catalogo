#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integra los LinkedIn validados al plan de acción y regenera el HTML.

QUÉ APORTA
------------------------------------------------------------------------------
De los 210 contactos de Direcmin (que no traían perfil), la búsqueda encontró 181 y la validación
dejó:
  - 90 BUENOS            -> se agrega el LinkedIn
  - 43 SE FUERON         -> se marca "ya no está en la empresa" (dato de valor: no perder la llamada)
  - 38 DUDOSOS           -> se agrega el LinkedIn pero con la marca de "sin confirmar"
  - 10 MALOS             -> NO se agrega (el perfil es de otra persona o está jubilado)
  - 29 sin resultado     -> quedan sin perfil

Salida: datos/plan_accion_limpio.json (actualizado) + regenera los dos HTML
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


val = json.load(open(os.path.join(D, "linkedin_direcmin_validado.json"), encoding="utf-8"))
plan = json.load(open(os.path.join(D, "plan_accion_limpio.json"), encoding="utf-8"))

# índice: empresa|nombre -> estado del LinkedIn
idx = {}
for c in val["contactos"]:
    idx[(norm(c["empresa"]), norm(c["nombre"]))] = c

cuenta = collections.Counter()
for p in plan["plan"]:
    for c in p["contactos"]:
        v = idx.get((norm(p["empresa"]), norm(c["nombre"])))
        if not v:
            cuenta["sin busqueda"] += 1
            continue
        est = v["estado"]
        cuenta[est] += 1
        if est in ("bueno", "dudoso"):
            c["linkedin"] = v["linkedin"]
            c["linkedin_estado"] = "confirmado" if est == "bueno" else "sin confirmar"
        elif est == "se-fue":
            c["linkedin"] = v["linkedin"]
            c["linkedin_estado"] = "se fue"
            c["nota"] = v["motivo"]
        else:
            c["linkedin_estado"] = "descartado"

plan["totales"]["con_linkedin"] = sum(1 for p in plan["plan"] for c in p["contactos"]
                                      if c.get("linkedin"))
plan["que_es"] = (plan.get("que_es", "") +
                  " Los LinkedIn de Direcmin se buscaron por nombre y se validaron: se marca si la "
                  "persona sigue en la empresa (43 ya no están) y si el perfil está confirmado.")
json.dump(plan, open(os.path.join(D, "plan_accion_limpio.json"), "w"), ensure_ascii=False, indent=1)

print("=" * 100)
print("LINKEDIN INTEGRADO AL PLAN DE ACCIÓN")
print("=" * 100)
for k, v in cuenta.most_common():
    print(f"  {k:16s} {v}")
tot = sum(len(p["contactos"]) for p in plan["plan"])
con = sum(1 for p in plan["plan"] for c in p["contactos"] if c.get("linkedin"))
print(f"\n  contactos: {tot} | con LinkedIn ahora: {con} (antes 308) | +{con-308}")
print(f"\n  guardado: datos/plan_accion_limpio.json")
