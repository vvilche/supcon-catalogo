#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAN DE CONTACTO TÉCNICO: jefes de planta y mantenimiento, no gerencias.

POR QUÉ. El plan general priorizaba por dolor × peso del rol, y el peso mayor lo tienen los
Aprobadores (gerentes generales). Pero quien SUFRE el problema y lo especifica es el jefe
técnico: el jefe de planta que tiene el efluente sin medir, el jefe de mantenimiento que
persigue el dato que no llega, el jefe de I&C que arma la especificación.

Para vender instrumentación y control, el técnico operativo es el que abre la puerta; el
gerente firma después. Este plan invierte el orden: filtra a los perfiles TÉCNICOS OPERATIVOS
y los ordena por dolor de su planta.

Perfiles incluidos (del campo `tipo` de cada tomador):
  jefe_planta, jefe_mantenimiento, jefe_produccion, jefe_ingenieria, jefe_ic, jefe_electrico,
  ingeniero_automatizacion, ingeniero_procesos, superintendente, jefe_calidad, jefe_medioambiente
Perfiles EXCLUIDOS: gerente_general, gerente_comercial, directorio, dueno, abastecimiento,
  gerente_proyectos (son comerciales o de firma, no técnicos de operación).

Salida: datos/plan_contacto_tecnico.json
"""
import os, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

plan = json.load(open(os.path.join(D, "plan_contacto.json"), encoding="utf-8"))["plan"]

# perfiles TÉCNICOS OPERATIVOS: los que viven el problema
TECNICOS = {
 "jefe_planta": "Jefe de Planta",
 "jefe_mantenimiento": "Jefe de Mantenimiento",
 "jefe_produccion": "Jefe de Producción",
 "jefe_ingenieria": "Jefe de Ingeniería",
 "jefe_ic": "Jefe de Instrumentación y Control",
 "jefe_electrico": "Jefe Eléctrico",
 "ingeniero_automatizacion": "Ingeniero de Automatización",
 "ingeniero_procesos": "Ingeniero de Procesos",
 "superintendente": "Superintendente",
 "jefe_calidad": "Jefe de Calidad",
 "jefe_medioambiente": "Jefe de Medio Ambiente",
}
# perfiles de firma o comerciales: quedan fuera de este plan
EXCLUIDOS = {"gerente_general","gerente_comercial","directorio","dueno","abastecimiento",
             "gerente_proyectos","otro"}

tecnicos = []
for p in plan:
    toms = [t for t in p["tomadores"] if (t.get("tipo") or "") in TECNICOS]
    if not toms:
        continue
    tecnicos.append({
      **{k: v for k, v in p.items() if k != "tomadores"},
      "tomadores": toms,
      "n_tecnicos": len(toms),
      "perfil_tecnico": TECNICOS.get(toms[0].get("tipo"), "—"),
    })

# ordenar por dolor de planta (el técnico ve el problema, no el presupuesto)
tecnicos.sort(key=lambda p: -p["dolor"])

por_perfil = collections.Counter()
for p in tecnicos:
    for t in p["tomadores"]:
        por_perfil[TECNICOS.get(t.get("tipo"), "—")] += 1

con_li = sum(1 for p in tecnicos if any(t.get("linkedin") for t in p["tomadores"]))
zonas = collections.Counter(p.get("zona") or "sin zona" for p in tecnicos)

print("=== PLAN DE CONTACTO TÉCNICO ===")
print(f"  empresas con contacto técnico:  {len(tecnicos):,}")
print(f"  contactos técnicos totales:     {sum(p['n_tecnicos'] for p in tecnicos):,}")
print(f"  con LinkedIn:                   {con_li:,}")
print()
print("=== POR PERFIL ===")
for k, v in por_perfil.most_common(): print(f"  {k:34s} {v:>5,}")
print()
print("=== POR ZONA ===")
for k in ["Z1","Z2","Z3","Z4","Z5","Z6","Z7","sin zona"]:
    if k in zonas: print(f"  {k:9s} {zonas[k]:>5,}")

print(f"\n=== TOP 40 TÉCNICOS A LLAMAR ===")
print(f"{'#':>3s} {'EMPRESA':36s} {'CARGO':34s} {'dolor':>5s} zona")
print("-"*96)
for i, p in enumerate(tecnicos[:40], 1):
    t = p["tomadores"][0]
    print(f"{i:>3d} {str(p['empresa'])[:36]:36s} {str(t.get('cargo'))[:34]:34s} "
          f"{p['dolor']:>5.0f} {p.get('zona') or '-'}")

json.dump({
 "metodo": ("Filtro del plan de contacto a los perfiles TÉCNICOS OPERATIVOS: jefes de planta, "
   "mantenimiento, producción, ingeniería, I&C, eléctricos, ingenieros de automatización y "
   "procesos, superintendentes. Ordenado por DOLOR DE PLANTA, no por peso del rol: para vender "
   "instrumentación y control, el que especifica abre la puerta y el gerente firma después."),
 "por_que": ("El plan general priorizaba gerentes generales por peso de rol. Pero quien sufre el "
   "problema y arma la especificación es el técnico: el jefe de planta con el efluente sin medir, "
   "el de mantenimiento persiguiendo el dato que no llega, el de I&C que define el instrumento."),
 "perfiles_incluidos": TECNICOS,
 "perfiles_excluidos": sorted(EXCLUIDOS),
 "resumen": {"empresas": len(tecnicos), "contactos_tecnicos": sum(p["n_tecnicos"] for p in tecnicos),
   "con_linkedin": con_li, "por_perfil": dict(por_perfil), "por_zona": dict(zonas)},
 "cuentas": tecnicos,
}, open(os.path.join(D,"plan_contacto_tecnico.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/plan_contacto_tecnico.json")
