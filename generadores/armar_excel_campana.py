#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arma el Excel de la campaña con los decisores REALES de la campaña.

CORRECCIÓN IMPORTANTE RESPECTO DEL PRIMER INTENTO
------------------------------------------------------------------------------
El primer armado matcheaba los 75 targets contra `plan_geo_limpio.json` (166 empresas del plan de
acción, OTRO universo) y solo cruzaba 7 plantas. Los decisores de la campaña ya están resueltos en
`cruce_campana.json`: **49 de 75 plantas tienen decisores**. Ese es el dato que va al Excel.

El Excel tiene 3 hojas:
  1. `Targets`   — las 75 plantas de la campaña, con el decisor y las columnas de línea marcadas.
  2. `Contactos` — TODOS los decisores de la campaña (empresa, nombre, cargo, línea, qué ofrecer,
                   LinkedIn, guion).
  3. `Leyenda`   — qué es cada cosa y qué se descartó.
"""
import json, os, re, unicodedata
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "campana_process_con_contactos.xlsx")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def linea_por_cargo(cargo):
    """La línea que le toca SEGÚN SU CARGO (no todos compran lo mismo)."""
    c = norm(cargo)
    if re.search(r"abastec|suministro|procurement|supply|compras|adquisic|logistica", c):
        return "Todas las líneas", "es el comprador: entra por acá todo el catálogo"
    if re.search(r"ambient|sustentab|calidad|hsec|permiso", c):
        return "Analítica", "CEMS/monitoreo de emisiones: la línea que resuelve el dolor del RETC"
    # fundición/planta de proceso: mantenimiento de equipos + control de proceso
    if re.search(r"fundicion|fundici.n|planta de proceso", c):
        return "Válvulas + Instrumentación + DCS", ("control de proceso de la fundición: válvulas, "
                                                    "instrumentación y el sistema de control")
    if re.search(r"manten|confiabilidad|planta|producci|operaci|mecanic|electric", c):
        return "Válvulas + Instrumentación", "válvulas de control, posicionador CVP2000, instrumentación de campo"
    if re.search(r"instrument|automatiz|control|proceso", c):
        return "Instrumentación + DCS/PLC", "transmisores, caudalímetros y el sistema de control"
    if re.search(r"proyecto|ingenier|superintend", c):
        return "Instrumentación + Válvulas", "especificación de proyecto: entrar en las bases técnicas"
    if re.search(r"seguridad|salud|riesgo|prevencion", c):
        return "SIS", "HIPPS/TCS-500: seguridad instrumentada"
    if re.search(r"gerente general|director|presidente|vicepresidente|ceo", c):
        return "Software y plataforma", "SolisSCADA/InPlant: historizar y reportar las señales que ya existen"
    # fiscal/auditoría/legal no compran: se marcan para que no se llamen
    if re.search(r"fiscal|auditor|legal|abogad|contralor", c):
        return "— (no compra)", "cargo de control interno: no decide compras técnicas"
    return "Instrumentación", "instrumentación de campo"


def marca_lineas(linea):
    l = norm(linea)
    valv = "SI" if "valvula" in l else ""
    anal = "SI" if "analitica" in l else ""
    fds = "SI" if ("valvula" in l or "instrumentacion" in l or "sis" in l) else ""
    sys_ = "SI" if ("software" in l or "plataforma" in l or "dcs" in l or "plc" in l or "todas" in l) else ""
    scada = "SI" if ("software" in l or "plataforma" in l or "scada" in l or "todas" in l) else ""
    bi = "SI" if "todas" in l else ""
    return bi, sys_, fds, valv, anal, scada


camp = json.load(open(os.path.join(D, "campana_process.json"), encoding="utf-8"))
cruce = json.load(open(os.path.join(D, "cruce_campana.json"), encoding="utf-8"))["filas"]
geo = json.load(open(os.path.join(D, "plan_geo_limpio.json"), encoding="utf-8"))["plan"]
geo_por_emp = {norm(p["empresa"]): p for p in geo}


def tel_de(nombre):
    n = norm(nombre)
    if n in geo_por_emp:
        return geo_por_emp[n].get("telefono_central", "")
    toks = [t for t in n.split() if len(t) > 5]
    for k, p in geo_por_emp.items():
        if toks and len(set(toks) & set(k.split())) >= 2:
            return p.get("telefono_central", "")
    return ""


def decisores_de(f):
    out = []
    for d in f.get("decisores_detalle", []) or []:
        out.append({"nombre": d.get("nombre", ""), "cargo": d.get("cargo", ""),
                    "linkedin": d.get("linkedin", ""), "fuente": "buscador (fuente garantizada)"})
    bar = f.get("decisores_barrido")
    if bar:
        for p in bar.get("personas", []):
            out.append({"nombre": p.get("nombre", ""), "cargo": p.get("cargo", ""),
                        "linkedin": p.get("linkedin", ""),
                        "fuente": "barrido LinkedIn (headline validado)"})
    return out


# CASOS QUE EL ARCHIVO NO TIENE EN `Targets` PERO SÍ EN `Actividades`/`Proyectos`.
# Medido: ENAMI (Fundición Hernán Videla Lira, US$1.700M, con deadline 25-11) está en Actividades y
# Proyectos pero NO en la hoja Targets — por eso nunca entró al cruce. Se agrega a mano, con sus
# decisores tomados del buscador (que sí los tiene).
EXTRAS = [
    {"planta": "Fundición Hernán Videla Lira (ENAMI)", "dueno": "ENAMI",
     "industria": "Minería (fundición)", "region_target": "Atacama",
     "siguiente": "Presentación presencial en Paipote (deadline 25-11)",
     "match_buscador": "ENAMI"},
]


def decisores_extra(nombre_match):
    """Busca los decisores de una empresa en el buscador (para los casos fuera de Targets)."""
    bd = json.load(open(os.path.join(D, "buscador_decisores.json"), encoding="utf-8"))["resultados"]
    ne = norm(nombre_match)
    for x in bd:
        if ne in norm(x["empresa"]):
            return [{"nombre": h["nombre"], "cargo": h["cargo"], "linkedin": h.get("linkedin", ""),
                     "fuente": h.get("fuente", "")} for h in x["hallazgos"]]
    return []


def limpiar_nombre(n, cargo):
    """Saca títulos académicos del nombre (medido: 'Christopher Petrola, P.E.')."""
    n = re.sub(r",?\s*(P\.?E\.?|MBA|MSc|PhD|Ing\.?|Sr\.?|Sra\.?)\s*$", "", str(n or ""), flags=re.I)
    return n.strip(" ,.")


def es_contacto_util(c):
    """Descarta los que no sirven para llamar."""
    cargo = norm(c["cargo"])
    # cargos de control interno que no compran
    if re.search(r"^fiscal|auditor|abogad|contralor", cargo):
        return False, "cargo de control interno"
    # LinkedIn de otro país (pe. = Perú, com = EE.UU.): la persona no está en Chile
    li = c.get("linkedin", "") or ""
    if re.search(r"linkedin\.com/(in|company)/", li) and not re.search(r"cl\.linkedin", li):
        if re.search(r"pe\.linkedin|co\.linkedin|ar\.linkedin|www\.linkedin\.com/in", li):
            # se acepta solo si el cargo menciona Chile o la empresa chilena
            if not re.search(r"chile|sur\b|anglo american chile", cargo):
                return False, "perfil de otro país"
    return True, ""


wb = Workbook()
h_font = Font(bold=True, color="FFFFFF", size=11)
h_fill = PatternFill("solid", fgColor="111827")
thin = Side(style="thin", color="E5E7EB")
borde = Border(left=thin, right=thin, top=thin, bottom=thin)

# ============================================================ HOJA 1: Targets
ws = wb.active
ws.title = "Targets"
COLS = ["Dueño", "Planta/Cia", "Región", "Industria", "Prioridad", "BI", "SYS", "FDS",
        "Válvulas", "Analítica", "Scada", "Contacto", "Cargo", "Línea", "Qué ofrecer",
        "Teléfono", "Siguiente Paso", "N° decisores"]
ws.append(COLS)
for i, c in enumerate(COLS, 1):
    cell = ws.cell(row=1, column=i)
    cell.font = h_font
    cell.fill = h_fill
    cell.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)

tmap = {norm(t["planta"]): t for t in camp["targets"]}
filas_t, con_dec = 0, 0
# los del cruce + los EXTRAS (que el archivo no tiene en Target pero sí en Actividades/Proyectos)
filas_fuente = list(cruce) + EXTRAS
for f in filas_fuente:
    t = tmap.get(norm(f["planta"]), {})
    decs = decisores_de(f) if "decisores_detalle" in f or "decisores_barrido" in f \
        else decisores_extra(f.get("match_buscador", f["dueno"]))
    if decs:
        con_dec += 1
        orden = sorted(decs, key=lambda c: 0 if re.search(
            r"manten|instrument|abastec|suministro|proceso|operaci|ambiental|jefe|gerente",
            c["cargo"], re.I) else 1)
        c0 = orden[0]
        linea, ofrecer = linea_por_cargo(c0["cargo"])
        bi, sys_, fds, valv, anal, scada = marca_lineas(linea)
        ws.append([f["dueno"], f["planta"], f.get("region_real") or f.get("region_target") or "",
                   f["industria"], t.get("prioridad", ""), bi, sys_, fds, valv, anal, scada,
                   c0["nombre"], c0["cargo"][:60], linea, ofrecer,
                   tel_de(f["dueno"]) or f.get("telefono", ""), t.get("siguiente", ""), len(decs)])
    else:
        ws.append([f["dueno"], f["planta"], f.get("region_target") or "", f["industria"],
                   t.get("prioridad", ""), "", "", "", "", "", "", "", "", "", "",
                   tel_de(f["dueno"]) or f.get("telefono", ""), t.get("siguiente", ""), 0])
    filas_t += 1

for i, a in enumerate([30, 32, 20, 22, 10, 6, 6, 6, 10, 11, 8, 26, 36, 26, 42, 16, 30, 12], 1):
    ws.column_dimensions[get_column_letter(i)].width = a
ws.freeze_panes = "C2"
ws.auto_filter.ref = f"A1:R{filas_t+1}"
for row in ws.iter_rows(min_row=2):
    for c in row:
        c.border = borde
        c.alignment = Alignment(vertical="top", wrap_text=(c.column in (13, 15, 17)))

# ========================================================= HOJA 2: Contactos
ws2 = wb.create_sheet("Contactos")
C2 = ["Empresa", "Planta (target)", "Región", "Industria", "Nombre", "Cargo", "Línea",
      "Qué ofrecer", "Fuente", "LinkedIn", "Guion"]
ws2.append(C2)
for i, c in enumerate(C2, 1):
    cell = ws2.cell(row=1, column=i)
    cell.font = h_font
    cell.fill = h_fill
    cell.alignment = Alignment(vertical="center", horizontal="center")

n = 0
for f in filas_fuente:
    decs = decisores_de(f) if "decisores_detalle" in f or "decisores_barrido" in f \
        else decisores_extra(f.get("match_buscador", f["dueno"]))
    reg = f.get("region_real") or f.get("region_target") or ""
    for c in decs:
        util, motivo = es_contacto_util(c)
        if not util:
            continue
        n += 1
        c["nombre"] = limpiar_nombre(c["nombre"], c["cargo"])
        linea, ofrecer = linea_por_cargo(c["cargo"])
        guion = (f"Hola, llamo de CONECTA. Busco a {c['nombre']}, {c['cargo'][:60]}, por "
                 f"{(f['dueno'] or f['planta']).title()}. Trabajamos instrumentación, válvulas y "
                 f"control: {ofrecer}. ¿Me puede derivar con él o dejarme un correo?")
        ws2.append([f["dueno"] or f["planta"], f["planta"], reg, f["industria"],
                    c["nombre"], c["cargo"][:70], linea, ofrecer, c["fuente"],
                    c["linkedin"], guion])

for i, a in enumerate([32, 30, 18, 22, 26, 40, 26, 46, 30, 34, 70], 1):
    ws2.column_dimensions[get_column_letter(i)].width = a
ws2.freeze_panes = "A2"
ws2.auto_filter.ref = f"A1:K{n+1}"
for row in ws2.iter_rows(min_row=2):
    for c in row:
        c.border = borde
        c.alignment = Alignment(vertical="top", wrap_text=(c.column in (8, 11)))

# ========================================================== HOJA 3: Leyenda
ws3 = wb.create_sheet("Leyenda")
ley = [
    ["Campo", "Qué es"],
    ["Contacto / Cargo", "El decisor de esa planta, con su cargo real"],
    ["Línea", "La línea que le corresponde SEGÚN SU CARGO: no todos compran lo mismo"],
    ["Qué ofrecer", "El argumento concreto para esa persona"],
    ["Fuente", "De dónde salió: fuente garantizada (Direcmin/Transparencia) o LinkedIn validado"],
    ["Guion", "La primera frase de la llamada, con el nombre, el cargo y la oferta"],
    ["", ""],
    ["SE DESCARTARON", "366 contactos del plan anterior, de 899"],
    ["  · ajenos (339)", "Eran de OTRA empresa. Ej: un 'Gerente Autonomía BHP' cargado en Minera Spence"],
    ["  · no compra (21)", "Cargos de ventas, RRHH, legal o marketing"],
    ["  · parser (2)", "El cargo estaba guardado como nombre ('JEFE DE OPERACION at MAXAM')"],
    ["  · sin dato (4)", "Sin registro para validar"],
    ["", ""],
    ["TOTAL ACTUAL", f"{n} decisores en {filas_t} plantas de la campaña"],
    ["PLANTAS CON DECISORES", f"{con_dec} de {filas_t} (las 26 restantes son 21 de generación: sin directorio ni LinkedIn útil)"],
]
for r in ley:
    ws3.append(r)
for i in range(1, 3):
    cell = ws3.cell(row=1, column=i)
    cell.font = h_font
    cell.fill = h_fill
ws3.column_dimensions["A"].width = 26
ws3.column_dimensions["B"].width = 84
for row in ws3.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(vertical="top", wrap_text=True)
ws3["A8"].font = Font(bold=True, color="92400E")
ws3["A14"].font = Font(bold=True, color="065F46")
ws3["A15"].font = Font(bold=True, color="065F46")

wb.save(OUT)
print(f"escrito: {OUT}")
print(f"  Targets:   {filas_t} plantas, {con_dec} con decisores")
print(f"  Contactos: {n} decisores")
print(f"  Leyenda:   {len(ley)} filas")
