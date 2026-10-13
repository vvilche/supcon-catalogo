#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACCION COMPLETA DEL eCRM (2023-2025) — el registro de cotizaciones de INECO/Emerson.

QUÉ ES
------------------------------------------------------------------------------
`Archivo de ecrm .xlsx`: el registro de TODAS las cotizaciones/oportunidades de INECO
(la operación chilena como Local Business Partner de Emerson) de 2023, 2024 y 2025.

COLUMNAS (las 17 reales; las 16.063 declaradas son artefacto de formato vacío):
  N° | Solicitud o RFQ | Contacto | BU | Cliente | Oportunidad | Descripción | Valor USD |
  Plazo Entrega | OC | Fecha OC | Fecha cierre recepción cotización | ecrm | Cotización |
  Estado ecrm | Estado | Comision   (+ "Mes GP" solo en 2025)

POR QUÉ ES EL DOCUMENTO MÁS VALIOSO DE LA SERIE
------------------------------------------------------------------------------
Los planes de negocio dicen la ESTRATEGIA. Esto es la OPERACIÓN real: qué se cotizó, a quién,
de qué línea (BU), por cuánto, y en qué quedó. Y viene con:
  - el CONTACTO de cada oportunidad (nombre de la persona que pidió),
  - la BU (línea de negocio) de cada venta,
  - el valor en USD,
  - el estado (si se envió, si salió OC, si se perdió).

Salida: datos/ecrm_extraido.json + datos/ecrm_oportunidades.csv
"""
import openpyxl, json, csv, os, re, collections

P = "/Users/victorvilche/Downloads/Archivo de ecrm .xlsx"
BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")

COLS = ["n", "rfq", "contacto", "bu", "cliente", "oportunidad", "descripcion", "valor_usd",
        "plazo_entrega", "oc", "fecha_oc", "fecha_cierre", "ecrm", "cotizacion",
        "estado_ecrm", "estado", "comision", "mes_gp"]

wb = openpyxl.load_workbook(P, read_only=True, data_only=True)
todas = []
for hoja in ["2023", "2024", "2025"]:
    ws = wb[hoja]
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue  # encabezado
        vals = list(row[:18])
        if not any(v is not None and str(v).strip() for v in vals):
            continue
        reg = {}
        for j, nombre in enumerate(COLS):
            v = vals[j] if j < len(vals) else None
            if v is None:
                reg[nombre] = ""
            elif hasattr(v, "isoformat"):
                reg[nombre] = v.isoformat()[:10]
            else:
                reg[nombre] = str(v).strip()
        reg["anio"] = hoja
        # el valor puede venir como texto con separadores
        v = reg["valor_usd"].replace("US$", "").replace(".", "").replace(",", ".")
        try:
            reg["valor_num"] = float(v)
        except Exception:
            reg["valor_num"] = None
        # LIMPIAR FILAS DE TOTALES (vienen mezcladas en la hoja y contaminan conteo y suma):
        # "Total USD" / "Cantidad de Negocios" son resúmenes, no oportunidades.
        marca = f"{reg['descripcion']} {reg['oportunidad']} {reg['cliente']} {reg['contacto']}".lower()
        if re.search(r"total\s*(usd|general|venta)|cantidad de negocios|^\s*subtotal", marca):
            continue
        todas.append(reg)
wb.close()

print("=" * 96)
print("eCRM INECO — REGISTRO DE COTIZACIONES 2023-2025")
print("=" * 96)
print(f"  oportunidades totales: {len(todas):,}")
por_anio = collections.Counter(r["anio"] for r in todas)
for a in ["2023", "2024", "2025"]:
    print(f"    {a}: {por_anio[a]:>5,}")

con_valor = [r for r in todas if r["valor_num"]]
total = sum(r["valor_num"] for r in con_valor)
print(f"\n  con valor USD declarado: {len(con_valor):,} ({len(con_valor)/len(todas)*100:.0f}%)")
print(f"  valor total cotizado:    US${total:,.0f}")

print(f"\n  === VALOR POR AÑO ===")
for a in ["2023", "2024", "2025"]:
    v = [r["valor_num"] for r in todas if r["anio"] == a and r["valor_num"]]
    print(f"    {a}: {len(v):>5,} cotizadas con valor | US${sum(v):>14,.0f}")

print(f"\n  === CLIENTES MÁS COTIZADOS (por monto) ===")
por_cli = collections.defaultdict(lambda: {"n": 0, "usd": 0.0})
for r in todas:
    c = (r["cliente"] or "(sin cliente)").strip()
    por_cli[c]["n"] += 1
    por_cli[c]["usd"] += r["valor_num"] or 0
for c, v in sorted(por_cli.items(), key=lambda x: -x[1]["usd"])[:25]:
    print(f"    {c[:38]:40s} {v['n']:>4} oport.  US${v['usd']:>13,.0f}")

print(f"\n  === LÍNEAS DE NEGOCIO (BU) ===")
por_bu = collections.defaultdict(lambda: {"n": 0, "usd": 0.0})
for r in todas:
    b = (r["bu"] or "(sin BU)").strip()
    por_bu[b]["n"] += 1
    por_bu[b]["usd"] += r["valor_num"] or 0
for b, v in sorted(por_bu.items(), key=lambda x: -x[1]["usd"])[:20]:
    print(f"    {b[:24]:26s} {v['n']:>4} oport.  US${v['usd']:>13,.0f}")

print(f"\n  === CONTACTOS (los que piden cotización) ===")
por_ct = collections.Counter((r["contacto"] or "").strip() for r in todas if r["contacto"])
for c, n in por_ct.most_common(25):
    print(f"    {c[:36]:38s} {n:>4}")

print(f"\n  === ESTADOS (en qué quedó cada una) ===")
por_est = collections.Counter((r["estado_ecrm"] or r["estado"] or "(vacío)")[:60] for r in todas)
for e, n in por_est.most_common(20):
    print(f"    {n:>5,}  {e}")

print(f"\n  === ÓRDENES DE COMPRA (las que se ganaron) ===")
con_oc = [r for r in todas if (r["oc"] or "").strip()]
print(f"    con OC: {len(con_oc):,}")
v_oc = sum(r["valor_num"] or 0 for r in con_oc)
print(f"    valor de las OC: US${v_oc:,.0f}")
if todas:
    print(f"    tasa de conversión (con OC / total): {len(con_oc)/len(todas)*100:.1f}%")

json.dump({
    "que_es": ("Registro de cotizaciones/oportunidades del eCRM de INECO (Local Business Partner "
               "de Emerson en Chile) para 2023, 2024 y 2025. Es la OPERACIÓN real: qué se cotizó, "
               "a quién, de qué línea (BU), por cuánto y en qué quedó."),
    "fuente": "Archivo de ecrm .xlsx (hojas 2023, 2024, 2025)",
    "columnas": COLS,
    "totales": {"oportunidades": len(todas), "con_valor": len(con_valor),
                "valor_total_usd": round(total, 2), "con_oc": len(con_oc),
                "valor_oc_usd": round(v_oc, 2),
                "por_anio": {a: por_anio[a] for a in ["2023", "2024", "2025"]}},
    "clientes": {c: v for c, v in por_cli.items()},
    "lineas_bu": {b: v for b, v in por_bu.items()},
    "contactos": dict(por_ct),
    "estados": dict(por_est),
    "oportunidades": todas,
}, open(os.path.join(D, "ecrm_extraido.json"), "w"), ensure_ascii=False, indent=1)

with open(os.path.join(D, "ecrm_oportunidades.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["anio"] + COLS + ["valor_num"])
    w.writeheader()
    for r in todas:
        w.writerow(r)
print(f"\nguardado: datos/ecrm_extraido.json + datos/ecrm_oportunidades.csv")
