#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el FORMATO COMPLETO del Excel de la campaña, para replicarlo.

Qué se extrae de cada hoja:
  - encabezados reales (texto y posición)
  - tipo de dato esperado (texto/fecha/número/lista)
  - los valores válidos observados en cada columna (para armar las listas desplegables)
  - el ancho de columna, si está definido
  - filas de ejemplo (las primeras con dato)

Salida: datos/formato_campana.json
"""
import openpyxl, json, os, collections, datetime

XLSX = "/Users/victorvilche/Downloads/Campaña de Detección Process.xlsx"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "datos", "formato_campana.json")

wb = openpyxl.load_workbook(XLSX, data_only=True)  # sin read_only: se necesitan dimensiones y estilos

formato = {"archivo": os.path.basename(XLSX), "hojas": []}

for nombre in wb.sheetnames:
    ws = wb[nombre]
    h = {"hoja": nombre, "filas": ws.max_row, "columnas": ws.max_column,
         "anchos": {}, "encabezados": [], "valores_por_columna": {}, "ejemplos": []}

    # anchos de columna definidos
    for letra, dim in ws.column_dimensions.items():
        if dim.width:
            h["anchos"][letra] = round(dim.width, 1)

    # encontrar la fila de encabezado: la primera con 2+ celdas de texto no vacías
    fila_hdr = None
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=min(12, ws.max_row)), 1):
        textos = [c.value for c in row if isinstance(c.value, str) and c.value.strip()]
        if len(textos) >= 2:
            fila_hdr = i
            break

    if fila_hdr:
        h["fila_encabezado"] = fila_hdr
        for j, c in enumerate(ws[fila_hdr], 1):
            if c.value is not None and str(c.value).strip():
                h["encabezados"].append({"col": j, "letra": c.column_letter,
                                         "titulo": str(c.value).strip(),
                                         "ancho": h["anchos"].get(c.column_letter)})
        # valores observados por columna (para listas desplegables)
        for e in h["encabezados"]:
            j = e["col"]
            vals = []
            for r in ws.iter_rows(min_row=fila_hdr + 1, max_row=ws.max_row, min_col=j, max_col=j):
                v = r[0].value
                if v is None or str(v).strip() == "":
                    continue
                if isinstance(v, datetime.datetime):
                    e["tipo"] = "fecha"
                    vals.append(v.strftime("%Y-%m-%d"))
                elif isinstance(v, (int, float)):
                    e["tipo"] = e.get("tipo") or "numero"
                else:
                    e["tipo"] = e.get("tipo") or "texto"
                    vals.append(str(v).strip())
            # si son pocos valores únicos y repetidos, es una lista
            if vals:
                c_uni = collections.Counter(vals)
                if len(c_uni) <= 12 and len(vals) > len(c_uni):
                    e["valores_posibles"] = [k for k, _ in c_uni.most_common()]
                e["ejemplos"] = list(dict.fromkeys(vals))[:4]
            e.setdefault("tipo", "texto")
        # 3 filas de ejemplo completas
        for r in ws.iter_rows(min_row=fila_hdr + 1, max_row=min(fila_hdr + 4, ws.max_row), values_only=True):
            if any(c is not None and str(c).strip() for c in r):
                h["ejemplos"].append([str(c).strip() if c is not None else "" for c in r])
    formato["hojas"].append(h)
    print(f"\n=== {nombre} ({ws.max_row}x{ws.max_column}) ===")
    print(f"  encabezado en fila {h.get('fila_encabezado')}: {len(h['encabezados'])} columnas")
    for e in h["encabezados"]:
        extra = ""
        if e.get("valores_posibles"):
            extra = f"  LISTA: {e['valores_posibles'][:6]}"
        print(f"    [{e['letra']}] {e['titulo'][:34]:36s} {e['tipo']:8s}{extra}")

wb.close()
json.dump(formato, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: {OUT}")
