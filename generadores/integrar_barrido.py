#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integra los decisores VALIDADOS del barrido al cruce de la campaña.

QUÉ HACE
------------------------------------------------------------------------------
Toma `datos/barrido_campana_auditado.json` (que ya separó válidos de ajenos) y los mete en el
cruce: la planta del target queda con sus decisores reales, más el detalle de a quién llamar.

POR QUÉ ESTÁ SEPARADO DEL CRUCE
------------------------------------------------------------------------------
El cruce (`cruce_campana.py`) matchea contra el buscador por nombre de empresa, y para las
empresas del barrido el match por nombre no siempre aplica (el barrido guardó con el nombre
comercial limpio, el Excel con el nombre de la planta). Acá se ata explícito por la lista de
empresas barridas, que ya se auditaron una por una.

Salida: reescribe datos/cruce_campana.json con el campo "decisores_barrido".
"""
import json, os, re, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


aud = json.load(open(os.path.join(D, "barrido_campana_auditado.json"), encoding="utf-8"))
cr = json.load(open(os.path.join(D, "cruce_campana.json"), encoding="utf-8"))
F = cr["filas"]

# indice: empresa auditada -> validos
por_empresa = {norm(a["empresa"]): a for a in aud if a["n_validos"] > 0}

# atasco por nombre: la empresa barrida vs la planta/dueño del target
def atar(f):
    # 1) por dueño exacto o contenido
    candidates = [norm(f["dueno"]), norm(f["planta"])]
    for ne, a in por_empresa.items():
        for c in candidates:
            if c and (ne in c or c in ne):
                return a
    # 2) por token distintivo (marca principal)
    for c in candidates:
        toks = [t for t in c.split() if len(t) > 4]
        for ne, a in por_empresa.items():
            marca = ne.split()[0] if ne.split() else ""
            if marca and marca in c and len(marca) > 4:
                return a
    return None


n_atados, n_dec = 0, 0
for f in F:
    a = atar(f)
    if a:
        f["decisores_barrido"] = {
            "empresa": a["empresa"], "n": a["n_validos"],
            "personas": [{"nombre": h["nombre"], "cargo": h["cargo"], "linkedin": h.get("linkedin", "")}
                         for h in a["validos"]],
        }
        n_atados += 1
        n_dec += a["n_validos"]
    else:
        f["decisores_barrido"] = None

cr["totales"]["plantas_con_decisores"] = sum(1 for f in F if f["decisores"] or f["decisores_barrido"])
cr["totales"]["decisores_del_barrido"] = n_dec

json.dump(cr, open(os.path.join(D, "cruce_campana.json"), "w"), ensure_ascii=False, indent=1)

print(f"empresas auditadas con validos: {len(por_empresa)}")
print(f"plantas del target atadas a un barrido: {n_atados}")
print(f"decisores validos integrados: {n_dec}")
print(f"plantas del target con decisores (cruce + barrido): {cr['totales']['plantas_con_decisores']} de {len(F)}")
print("\ndetalle atado:")
for f in F:
    if f["decisores_barrido"]:
        print(f"  {f['planta'][:32]:34s} <- {f['decisores_barrido']['empresa'][:30]:32s} ({f['decisores_barrido']['n']})")
