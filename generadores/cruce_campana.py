#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUCE: CAMPAÑA DE DETECCIÓN PROCESS × EL TRABAJO DE PROSPECCIÓN

QUÉ HACE
------------------------------------------------------------------------------
Cruza las 75 plantas target del Excel de la campaña contra los 2.691 decisores del buscador y
los 220 mineros del RETC, y produce el PLAN DE USO: qué puede aportar cada pieza a la otra.

EL DIAGNÓSTICO QUE SOSTIENE EL PLAN
------------------------------------------------------------------------------
  - El Excel tiene el QUÉ: 75 plantas objetivo, 31 proyectos con inversión, las fuentes.
    Pero está a medio hacer: 2 contactos, 3 siguientes pasos, columnas de línea vacías.
  - El trabajo de prospección tiene el QUIÉN: 2.691 decisores con cargo y LinkedIn, pero no
    tiene "qué planta es target de la campaña" ni la prioridad comercial.

Cada uno cubre el hueco del otro. Eso es el plan.

Salida: datos/cruce_campana.json + artefactos/campana_process.html
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


camp = load("campana_process.json") or {}
targets = camp.get("targets", [])
proyectos = camp.get("proyectos", [])
actividades = camp.get("actividades", [])
fuentes = camp.get("fuentes", [])

buscador = (load("buscador_decisores.json") or {}).get("resultados", [])
mineras = (load("mineras_retc.json") or {}).get("mineras", [])
plan = (load("plan_accion.json") or {}).get("plan", [])
ecrm = (load("ecrm_supcon.json") or {}).get("clientes_hoy", {})

idx_buscador = {norm(x["empresa"]): x for x in buscador}
idx_mineras = {norm(m["empresa"]): m for m in mineras}
idx_plan = {norm(p["empresa"]): p for p in plan}


def buscar(planta_o_dueno, idx, min_tokens=2):
    """Busca una planta/dueño del Excel en un índice de empresas."""
    n = norm(planta_o_dueno)
    if not n or len(n) < 4:
        return None
    if n in idx:
        return idx[n]
    toks = set(t for t in n.split() if len(t) > 3)
    if not toks:
        return None
    mejor, sc = None, 0
    for k, v in idx.items():
        c = len(toks & set(k.split()))
        if c > sc and c >= min_tokens:
            mejor, sc = v, c
    return mejor


# ---------------------------------------------------------------- CRUCE
filas = []
for t in targets:
    nombre = t["planta"]
    dueno = t["dueno"]
    # buscar por nombre de planta primero, después por dueño
    bd = buscar(nombre, idx_buscador) or buscar(dueno, idx_buscador)
    mn = buscar(nombre, idx_mineras) or buscar(dueno, idx_mineras)
    pl = buscar(nombre, idx_plan) or buscar(dueno, idx_plan)
    # proyectos que le pertenecen (por dueño)
    proy = [p for p in proyectos if dueno and norm(p["dueno"]) and
            (norm(dueno) in norm(p["dueno"]) or norm(p["dueno"]) in norm(dueno))]
    filas.append({
        "planta": nombre, "dueno": dueno, "industria": t["industria"],
        "region_target": t["region"],
        "contacto_excel": t["contacto"], "quien_contacto": t["quien"],
        "siguiente_paso": t["siguiente"],
        "lineas_excel": {k: t[k] for k in ("bi", "sys", "fds", "valvulas", "analitica", "scada") if t[k]},
        "decisores": (bd or {}).get("n_decisores", 0),
        "empresa_buscador": (bd or {}).get("empresa", ""),
        "decisores_detalle": (bd or {}).get("hallazgos", [])[:8],
        "dolor_t": (mn or {}).get("respel_t", 0),
        "region_real": ((pl or {}).get("region") or (mn or {}).get("region") or ""),
        "comuna_real": (pl or {}).get("comuna", ""),
        "telefono": (pl or {}).get("telefono_central", ""),
        "n_proyectos": len(proy),
        "proyectos": [{"nombre": p["proyecto"], "inv_usd": p["inv_usd"],
                       "estado": p["estado"], "fuente": p["obs"][:90]} for p in proy][:5],
        "inv_proyectos_usd": sum(p["inv_usd"] for p in proy),
    })

# ---------------------------------------------------------------- MÉTRICAS
con_dec = [f for f in filas if f["decisores"]]
sin_dec = [f for f in filas if not f["decisores"]]
con_proy = [f for f in filas if f["n_proyectos"]]
print("=" * 104)
print("CRUCE: CAMPAÑA PROCESS × PROSPECCIÓN")
print("=" * 104)
print(f"  plantas en el target:        {len(filas)}")
print(f"  con decisores ya mapeados:   {len(con_dec)} ({len(con_dec)/len(filas)*100:.0f}%)")
print(f"  SIN decisores (a cubrir):    {len(sin_dec)}")
print(f"  con proyecto en carpeta:     {len(con_proy)}")
print(f"  con teléfono:                {sum(1 for f in filas if f['telefono'])}")

print(f"\n  {'planta':34s} {'industria':16s} {'dec':>4s} {'proy':>4s} {'tel':>16s}  siguiente paso")
for f in sorted(filas, key=lambda x: (-x["decisores"], -x["n_proyectos"]))[:24]:
    print(f"  {f['planta'][:32]:34s} {f['industria'][:14]:16s} {f['decisores']:>4} "
          f"{f['n_proyectos']:>4} {f['telefono'][:16]:>16s}  {f['siguiente_paso'][:30]}")

# ---------------------------------------------------------------- LAS 3 OPORTUNIDADES DE USO
print(f"\n{'='*104}")
print("LAS 3 JUGADAS DEL CRUCE")
print(f"{'='*104}")

# 1. completar contacto donde el Excel no lo tiene
sin_contacto_con_dec = [f for f in filas if not f["contacto_excel"] and f["decisores"]]
print(f"\n  JUGADA 1 — COMPLETAR EL CONTACTO QUE FALTA")
print(f"    plantas sin contacto en el Excel pero con decisores mapeados: {len(sin_contacto_con_dec)}")
print(f"    (el Excel tiene 2 contactos de 75; hay {sum(f['decisores'] for f in sin_contacto_con_dec)} "
      f"decisores disponibles para esas plantas)")
for f in sorted(sin_contacto_con_dec, key=lambda x: -x["decisores"])[:6]:
    d0 = f["decisores_detalle"][0] if f["decisores_detalle"] else {}
    print(f"      {f['planta'][:30]:32s} -> {d0.get('nombre','')[:26]:28s} {d0.get('cargo','')[:32]}")

# 2. priorizar proyectos por inversión real (no por el Excel)
print(f"\n  JUGADA 2 — PRIORIZAR POR LA PLATA DEL PROYECTO")
grandes = sorted([f for f in filas if f["inv_proyectos_usd"]], key=lambda x: -x["inv_proyectos_usd"])
for f in grandes[:8]:
    print(f"      US${f['inv_proyectos_usd']/1e6:>7,.0f}M  {f['planta'][:28]:30s} {f['decisores']:>3} dec")

# 3. las que no cruzaron: huecos reales
print(f"\n  JUGADA 3 — LAS QUE NO CRUZARON (huecos a cubrir)")
print(f"    {len(sin_dec)} plantas del target sin ningún decisor mapeado:")
for f in sin_dec[:12]:
    print(f"      {f['planta'][:34]:36s} {f['industria'][:18]:20s} dueño: {f['dueno'][:22]}")
if len(sin_dec) > 12:
    print(f"      ... y {len(sin_dec)-12} más")

json.dump({
    "que_es": ("Cruce entre la campaña de detección Process (Excel) y el trabajo de prospección "
               "(buscador de decisores, mineras del RETC, plan de acción)."),
    "diagnostico": ("El Excel tiene el QUÉ (75 plantas target, 31 proyectos con inversión, "
                    "fuentes) pero está a medio hacer: 2 contactos, 3 siguientes pasos. El trabajo "
                    "de prospección tiene el QUIÉN (2.691 decisores) pero no sabe qué planta es "
                    "target. Cada uno cubre el hueco del otro."),
    "totales": {"plantas_target": len(filas), "con_decisores": len(con_dec),
                "sin_decisores": len(sin_dec), "con_proyecto": len(con_proy),
                "con_telefono": sum(1 for f in filas if f["telefono"]),
                "con_contacto": sum(1 for f in filas if f["contacto_excel"]),
                "con_siguiente": sum(1 for f in filas if f["siguiente_paso"]),
                "decisores_disponibles": sum(f["decisores"] for f in sin_contacto_con_dec)},
    "filas": filas,
}, open(os.path.join(D, "cruce_campana.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/cruce_campana.json")
