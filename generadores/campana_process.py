#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAMPAÑA DE DETECCIÓN PROCESS (CONECTA) — análisis y cruce con el trabajo de prospección.

QUÉ ES EL ARCHIVO
------------------------------------------------------------------------------
`Campaña de Detección Process.xlsx` es el CRM de una campaña de CONECTA para detectar
oportunidades de la línea **Process** (instrumentación, válvulas, analítica, SCADA, sistemas):
  Plan        -> la estructura (Planta | Industria | Ubicación | Prioridad)
  Targets     -> 75 PLANTAS objetivo, con dueño, industria, y 6 columnas de línea
                 (BI, SYS, FDS, Válvulas, Analítica, Scada) para marcar lo detectado
  Proyectos   -> 31 proyectos con inversión, estado (Aprobado/EIA), EPCM y link a la fuente
  Fuentes     -> 1.000 URLs de seguimiento
  Actividades -> siguiente acción por cliente, con responsable (CAO, EQR, FTM, MC, Victor)

EL HALLAZGO CENTRAL
------------------------------------------------------------------------------
La campaña está **a medio hacer, y ahí está el valor**:
  - 75 plantas en el target, pero **solo 2 con contacto** y **3 con siguiente paso**
  - las 6 columnas de línea están **casi todas vacías** (la detección no se hizo)
O sea: el Excel tiene el QUÉ (las plantas) y el trabajo construido tiene el QUIÉN (los decisores).
Se completan uno al otro.

REGLA DE HONESTIDAD
------------------------------------------------------------------------------
El campo "siguiente paso" y el contacto son datos de ESTE archivo, al momento del archivo.
No se inventan: se cruzan contra lo construido y se marca lo que falta.

Salida: datos/campana_process.json
"""
import openpyxl, os, re, json, collections, unicodedata

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
XLSX = "/Users/victorvilche/Downloads/Campaña de Detección Process.xlsx"


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


def num_monto(txt):
    m = re.search(r"([\d.,]+)\s*([MBK])?", str(txt or ""), re.I)
    if not m:
        return 0.0
    try:
        v = float(m.group(1).replace(",", "."))
    except Exception:
        return 0.0
    return v * {"M": 1e6, "B": 1e9, "K": 1e3}.get((m.group(2) or "M").upper(), 1e6)


wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)

# ---------------------------------------------------------------- TARGETS
ws = wb["Targets"]
rows = list(ws.iter_rows(values_only=True))
CT = {"dueno": 0, "planta": 1, "region": 2, "industria": 3, "bi": 4, "prioridad": 5,
      "sys": 6, "fds": 7, "valvulas": 8, "analitica": 9, "scada": 10, "contacto": 11,
      "quien": 12, "siguiente": 13}
targets = []
for r in rows[4:]:
    if len(r) < 2 or not r[CT["planta"]]:
        continue
    d = {k: (str(r[j]).strip() if j < len(r) and r[j] is not None else "") for k, j in CT.items()}
    if d["planta"].upper().startswith(("PLANTA", "REGION", "INDUSTRIA")):
        continue
    # normalizar el "sí" de las columnas de línea
    for lin in ("bi", "sys", "fds", "valvulas", "analitica", "scada"):
        v = d[lin].strip().lower()
        d[lin] = "si" if v in ("si", "sí", "x") else ("no" if v == "no" else "")
    targets.append(d)

# ---------------------------------------------------------------- PROYECTOS
ws2 = wb["Proyectos"]
rows2 = list(ws2.iter_rows(values_only=True))
CP = {"proyecto": 1, "fecha": 2, "dueno": 3, "pais": 4, "inv": 5, "estudio": 6,
      "area_neg": 7, "region": 8, "estado": 9, "epcm": 10, "area": 11, "target": 12, "obs": 13}
proyectos = []
for r in rows2[2:]:
    if len(r) < 2 or not r[CP["proyecto"]]:
        continue
    d = {k: (str(r[j]).strip() if j < len(r) and r[j] is not None else "") for k, j in CP.items()}
    d["inv_usd"] = num_monto(d["inv"])
    proyectos.append(d)

# ---------------------------------------------------------------- ACTIVIDADES
# Tiene DOS bloques: (a) cliente/proyecto/siguiente actividad, y (b) una sección de "Puntos Claves"
# con Acciones Pendientes y deadline. Se capturan los dos.
ws3 = wb["Actividades"]
rows3 = list(ws3.iter_rows(values_only=True))
CA = {"area": 0, "cliente": 1, "proyecto": 2, "inversion": 3, "siguiente": 4, "quien": 5}
actividades = []
puntos = []
for r in rows3[2:]:
    if len(r) < 2:
        continue
    cel = [str(c).strip() if c is not None else "" for c in r]
    # bloque de puntos claves: trae "Acciones Pendientes" / "Proxima Accion" / "Dead line"
    if any("acciones pendientes" in c.lower() or "proxima acci" in c.lower()
           or "dead line" in c.lower() for c in cel):
        continue
    if any("puntos claves" in c.lower() for c in cel):
        continue
    d = {k: (cel[j] if j < len(cel) else "") for k, j in CA.items()}
    if not (d["cliente"] or d["siguiente"] or d["proyecto"]):
        # puede ser una fila de la sección de puntos: nº | tema | accion pendiente | proxima | deadline
        if cel[1] and cel[2] and len(cel) > 4:
            puntos.append({"n": cel[1], "tema": cel[2], "accion": cel[4],
                           "proxima": cel[5] if len(cel) > 5 else "",
                           "deadline": cel[6] if len(cel) > 6 else ""})
        continue
    actividades.append(d)

# ---------------------------------------------------------------- FUENTES
# OJO: las URLs están en la COLUMNA 1, no en la 0 (la hoja declara 1000 filas pero solo 5 tienen dato).
ws4 = wb["Fuentes"]
fuentes = []
for r in ws4.iter_rows(values_only=True):
    if not r:
        continue
    for c in r:
        v = str(c).strip() if c is not None else ""
        if v.startswith("http"):
            fuentes.append(v)
            break

wb.close()

print("=" * 100)
print("CAMPAÑA DE DETECCIÓN PROCESS — análisis")
print("=" * 100)
print(f"  targets (plantas):  {len(targets)}")
print(f"  proyectos:          {len(proyectos)}  (US${sum(p['inv_usd'] for p in proyectos)/1e9:,.1f} mil M)")
print(f"  actividades:        {len(actividades)}")
print(f"  fuentes:            {len(fuentes)}")

print("\n=== ESTADO DE LA CAMPAÑA (el hallazgo) ===")
print(f"  plantas con CONTACTO:        {sum(1 for t in targets if t['contacto'])} de {len(targets)}")
print(f"  plantas con SIGUIENTE PASO:  {sum(1 for t in targets if t['siguiente'])} de {len(targets)}")
lin_marcadas = sum(1 for t in targets for k in ("bi", "sys", "fds", "valvulas", "analitica", "scada")
                   if t[k])
print(f"  líneas marcadas (de 6x{len(targets)}={6*len(targets)}): {lin_marcadas}")
print(f"  -> la DETECCIÓN de líneas está por hacer, y los decisores también")

print("\n=== TARGETS POR INDUSTRIA ===")
for k, v in collections.Counter(t["industria"] for t in targets if t["industria"]).most_common():
    print(f"  {k[:40]:42s} {v}")

print("\n=== PROYECTOS POR ESTADO ===")
for k, v in collections.Counter(p["estado"] for p in proyectos if p["estado"]).most_common():
    print(f"  {k[:34]:36s} {v}")

print("\n=== TOP PROYECTOS POR INVERSIÓN ===")
for p in sorted(proyectos, key=lambda x: -x["inv_usd"])[:12]:
    print(f"  US${p['inv_usd']/1e6:>7,.0f}M  {p['proyecto'][:40]:42s} {p['dueno'][:18]:20s} {p['estado'][:12]}")

json.dump({
    "que_es": ("CRM de la campaña de detección de la línea Process de CONECTA: 75 plantas target, "
               "31 proyectos con inversión, actividades y fuentes."),
    "hallazgo": ("La campaña está a medio hacer: 75 plantas target pero solo 2 con contacto y 3 con "
                 "siguiente paso; las 6 columnas de línea (BI/SYS/FDS/Válvulas/Analítica/Scada) están "
                 "casi vacías. El Excel tiene el QUÉ (plantas); el trabajo de prospección tiene el "
                 "QUIÉN (decisores). Se completan."),
    "totales": {"targets": len(targets), "proyectos": len(proyectos),
                "actividades": len(actividades), "fuentes": len(fuentes),
                "puntos_claves": len(puntos),
                "con_contacto": sum(1 for t in targets if t["contacto"]),
                "con_siguiente": sum(1 for t in targets if t["siguiente"]),
                "lineas_marcadas": lin_marcadas},
    "targets": targets, "proyectos": proyectos,
    "actividades": actividades, "puntos_claves": puntos, "fuentes": fuentes,
}, open(os.path.join(D, "campana_process.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/campana_process.json")
print(f"  fuentes: {len(fuentes)} | puntos claves: {len(puntos)} | actividades: {len(actividades)}")
