#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eCRM × SUPCON: qué se cotizó en 2023-2025 y qué de eso vende SUPCON hoy.

QUÉ HACE
------------------------------------------------------------------------------
Toma las 681 oportunidades del eCRM de INECO (2023-2025) y hace tres cosas:
  1. TRADUCE las siglas de BU a productos, con la evidencia (descripciones reales) al lado.
  2. MIDE qué porción del negocio histórico es reemplazable por línea SUPCON.
  3. CRUZA los clientes del eCRM contra el catálogo de hoy (personas y dolor).

POR QUÉ SIRVE
------------------------------------------------------------------------------
El eCRM no dice la estrategia: dice DÓNDE ESTÁ LA PLATA. Estos son los clientes que cotizaron
de verdad, con su contacto, su línea y su monto. Es la lista de a quién volver con producto
SUPCON, ordenada por lo que ya compraban.

BU = Business Unit (línea de negocio Emerson). Siglas descifradas por las descripciones reales:
  FCS = Fisher Control Solutions  → válvulas de control + posicionadores + actuadores
  ISV = Isolation Valves          → válvulas de aislamiento (bola, cuchilla, mariposa, compuerta)
  RMD = Rosemount Measurement     → instrumentación de campo (presión, temp, flujo, nivel)
  RFD = Rosemount Flow Devices    → caudalímetros
  FI  = Field Instruments / consumibles → válvulas solenoides, accesorios, cables
  RQ  = Requisiciones / equipos rotativos → bombas, repuestos
  SYS = Sistemas (AMS, Trex, monitoreo)  → software/gestión de activos
  REG = Reguladores de presión
  RAI = Rosemount Analytical      → analítica de gases/líquidos
  PRV = Pressure Relief Valves    → válvulas de seguridad/alivio
  MSOL = Measurement Solutions (proyectos + ingeniería)
"""
import os, json, collections, re

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")

d = json.load(open(os.path.join(D, "ecrm_extraido.json"), encoding="utf-8"))
opp = d["oportunidades"]

BU_NOMBRE = {
    "FCS": "Fisher Control Solutions — válvulas de control, posicionadores, actuadores",
    "ISV": "Isolation Valves — válvulas de aislamiento (bola, cuchilla, mariposa, compuerta)",
    "RMD": "Rosemount Measurement — instrumentación de campo (presión, temp, flujo, nivel)",
    "RFD": "Rosemount Flow Devices — caudalímetros magnéticos y másicos",
    "FI": "Field Instruments / consumibles — solenoides, accesorios, cables",
    "RQ": "Requisiciones — equipos rotativos (bombas) y repuestos mecánicos",
    "SYS": "Sistemas — AMS, Trex, monitoreo de condición, wireless",
    "REG": "Reguladores de presión (Fisher 67CFR, Tescom)",
    "RAI": "Rosemount Analytical — analítica de gases y líquidos",
    "PRV": "Pressure Relief Valves — válvulas de seguridad y alivio",
    "MSOL": "Measurement Solutions — proyectos con ingeniería",
}

# Qué SUPCON cubre cada BU (el mapeo comercial, explícito)
SUPCON_CUBRE = {
    "FCS": ("SUPCON Valves + CVP2000", "reemplazo directo: válvulas de control y posicionador"),
    "ISV": ("SUPCON Valves", "reemplazo directo: válvulas de aislamiento"),
    "PRV": ("SUPCON Valves (parcial)", "requiere validar rango y certificación"),
    "REG": ("SUPCON Valves (parcial)", "reguladores: validar catálogo"),
    "ACT": ("SUPCON Valves", "actuadores eléctricos y neumáticos"),
    "RMD": ("SUPCON Instruments (CXT/CJT)", "presión, temperatura, nivel"),
    "RFD": ("SUPCON Instruments", "caudal: validar magnético vs Coriolis"),
    "RAI": ("SUPCON Analítica (parcial)", "validar línea de gases"),
    "SYS": ("SUPCON Software / Tier0", "AMS ≈ PRIDE/supOS; monitoreo ≈ Tier0 UNS"),
    "FI": ("SUPCON Instruments (parcial)", "soluciones y consumibles"),
    "RQ": ("—", "no es línea SUPCON: bombas y rotativos"),
    "MSOL": ("SUPCON + Tier0", "proyectos: instrumentación y automatización"),
}

# --- cobertura SUPCON sobre el valor REAL (sin doble conteo de BU compuestos) ---
# OJO: un mismo monto puede venir con BU compuesta ("FCS/ISV/RMD"), así que NO se puede sumar
# por parte (contaría 3 veces). Se calcula sobre el TOTAL, clasificando cada oportunidad una vez.
def bu_limpia(bu):
    """Devuelve las siglas válidas de un BU; descarta basura (números, 'All', 'USD$ GP')."""
    bu = (bu or "").strip().upper()
    partes = [p.strip() for p in re.split(r"[/\-]", bu) if p.strip()]
    ok = [p for p in partes if p in BU_NOMBRE or p in SUPCON_CUBRE]
    return ok

NO_SUPCON = {"RQ"}  # bombas y rotativos: no es línea SUPCON

total_usd = 0.0
cubre_usd = 0.0
sin_clasificar = 0.0
tot_bu = collections.Counter()
usd_bu = collections.defaultdict(float)
for r in opp:
    v = r.get("valor_num") or 0
    total_usd += v
    partes = bu_limpia(r.get("bu"))
    for p in partes:                       # el conteo por línea sí puede repetir (es multietiqueta)
        tot_bu[p] += 1
        usd_bu[p] += v / max(len(partes), 1)   # el monto se reparte para no inflar
    if not partes:
        sin_clasificar += v
    elif set(partes) <= NO_SUPCON:
        pass                                   # fuera del alcance SUPCON
    else:
        cubre_usd += v                         # alguna línea SUPCON lo cubre
print("=" * 100)
print("eCRM 2023-2025 × SUPCON")
print("=" * 100)
print(f"  oportunidades: {len(opp)}   valor cotizado: US${total_usd:,.0f}")

print(f"\n=== LAS LÍNEAS (BU), ordenadas por monto ===")
for bu, v in sorted(usd_bu.items(), key=lambda x: -x[1]):
    nom = BU_NOMBRE.get(bu, "?")
    sup = SUPCON_CUBRE.get(bu, ("?", ""))
    marca = "" if sup[0].startswith("—") else " ✓"
    print(f"  {bu:6s} {tot_bu[bu]:>4} oport  US${v:>12,.0f}  {nom[:52]}")
    print(f"         → SUPCON: {sup[0]:34s} {sup[1][:44]}{marca}")

print(f"\n  VALOR CUBIERTO POR LÍNEA SUPCON: US${cubre_usd:,.0f} de US${total_usd:,.0f} "
      f"({cubre_usd/total_usd*100:.0f}%)")
print(f"  sin línea identificada: US${sin_clasificar:,.0f} ({sin_clasificar/total_usd*100:.0f}%)")
print(f"  fuera de línea SUPCON (solo bombas/rotativos RQ): US${total_usd-cubre_usd-sin_clasificar:,.0f}")

# --- clientes del eCRM cruzados con hoy ---
def load(p):
    fp = os.path.join(D, p)
    return json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else None

per = load("personas_todas.json")
da = load("dolor_ambiental_empresas.json")
per_emp = per["por_empresa"] if per else {}
dolor = {e["empresa"].upper(): e for e in (da["empresas"] if da else [])}

# cliente del eCRM -> patrones para buscar en el catalogo de hoy
ALIAS = {
    "MLP": ["pelambres"], "ANDINA": ["andina"], "CANDELARIA": ["candelaria"],
    "SALVADOR": ["salvador"], "ENAMI": ["enami"], "CASERONES": ["caserones"],
    "CODELCO": ["codelco"], "KINROSS": ["kinross"], "CMP": ["cmpc", "acero", "huachipato"],
    "PUCobre": ["pucobre"], "Ventana": ["ventana"], "SGS": [" sgs "],
}

byc = collections.defaultdict(lambda: {"n": 0, "usd": 0.0, "oc": 0, "usd_oc": 0.0})
for r in opp:
    c = (r.get("cliente") or "(sin)").strip()
    v = r.get("valor_num") or 0
    if not c or c == "(sin)":
        continue
    byc[c]["n"] += 1
    byc[c]["usd"] += v
    if (r.get("oc") or "").strip():
        byc[c]["oc"] += 1
        byc[c]["usd_oc"] += v

print(f"\n=== CLIENTES DEL eCRM × HOY (los 18 mayores) ===")
cruces = {}
for c, x in sorted(byc.items(), key=lambda y: -y[1]["usd"])[:18]:
    pats = None
    for k, v in ALIAS.items():
        if k.lower() in c.lower() or c.lower() in k.lower():
            pats = v
            break
    if pats is None:
        pats = [c.lower()[:9]]
    personas = areas = 0
    emp = ""
    for e2 in per_emp:
        if any(p in e2.lower() for p in pats):
            emp = emp or e2
            areas = max(areas, len(per_emp[e2]))
            personas += sum(len(v) for v in per_emp[e2].values())
    tox = None
    for u, e2 in dolor.items():
        if any(p in u.lower() for p in pats):
            tox = e2.get("carga_peligrosa_t")
            break
    cruces[c] = {"cotizaciones": x["n"], "usd_cotizado": round(x["usd"], 2),
                 "oc": x["oc"], "usd_oc": round(x["usd_oc"], 2),
                 "empresa_hoy": emp, "areas": areas, "personas": personas,
                 "carga_toxica": tox}
    tx = f"{tox:>9,.1f}" if tox is not None else "        —"
    print(f"  {c[:20]:22s} {x['n']:>4} cot | US${x['usd']:>12,.0f} | {x['oc']:>3} OC "
          f"US${x['usd_oc']:>11,.0f} | hoy: {areas} á, {personas:>3} p, tóxicas {tx}")

# --- contactos del eCRM (nombres reales) ---
ct = collections.Counter()
ct_usd = collections.defaultdict(float)
for r in opp:
    c = (r.get("contacto") or "").strip()
    if not c or c.lower() in ("abastecimiento", "compras", "contacto", "sin contacto"):
        continue
    if not re.match(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ]+(\s+[A-Za-zÁÉÍÓÚÑáéíóúñ]+)+$", c):
        continue
    ct[c] += 1
    ct_usd[c] += r.get("valor_num") or 0

print(f"\n=== CONTACTOS REALES DEL eCRM (nombre de la persona), top 20 ===")
cont = {}
for c, n in ct.most_common(20):
    cont[c] = {"cotizaciones": n, "usd": round(ct_usd[c], 2)}
    print(f"    {c[:34]:36s} {n:>4} cot   US${ct_usd[c]:>12,.0f}")

# --- contratos marco / licitaciones recurrentes ---
print(f"\n=== RECURRENTES: contratos marco y licitaciones con folio ===")
rec = [r for r in opp if re.search(r"contrato marco|licitaci[oó]n|^[0-9]{9,}", 
        f"{r.get('descripcion','')} {r.get('oportunidad','')}", re.I)]
print(f"    {len(rec)} oportunidades con contrato marco / licitación / folio")
for r in rec[:8]:
    print(f"      {r['anio']} | {(r.get('cliente') or '?')[:16]:18s} | {(r.get('descripcion') or '')[:66]}")

json.dump({
    "que_es": ("Extracción completa del eCRM de INECO (2023-2025): 681 oportunidades reales "
               "(tras limpiar filas de totales) con cliente, contacto, BU, monto y estado."),
    "bu_descifradas": BU_NOMBRE,
    "supcon_cubre": {k: {"linea": v[0], "nota": v[1]} for k, v in SUPCON_CUBRE.items()},
    "totales": {"oportunidades": len(opp), "valor_cotizado_usd": round(total_usd, 2),
                "valor_cubierto_supcon_usd": round(cubre_usd, 2),
                "pct_cubierto": round(cubre_usd / total_usd * 100, 1)},
    "por_bu": {k: {"oportunidades": tot_bu[k], "usd": round(usd_bu[k], 2)} for k in usd_bu},
    "clientes_hoy": cruces,
    "contactos": cont,
}, open(os.path.join(D, "ecrm_supcon.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/ecrm_supcon.json")
