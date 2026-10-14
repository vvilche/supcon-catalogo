#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
¿El RETC trae a las mineras? Verificación del universo completo.

MOTIVO: la matriz de dolor tiene solo 5 mineras grandes (Escondida, Candelaria, Quebrada Blanca,
Centinela) y le FALTAN todas las demás: Codelco, Los Pelambres, Collahuasi, Los Bronces, Spence,
Gaby, El Abra, Antucoya, Caserones. Si el universo sale del RETC y el RETC no reporta minería,
entonces el cruce central del proyecto está construido sobre una base incompleta.
"""
import openpyxl, os, re, json

B = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo/datos/retc/"
GRANDES = ["codelco", "pelambres", "collahuasi", "escondida", "chuquicamata", "los bronces",
           "spence", "gaby", "el abra", "centinela", "candelaria", "quebrada blanca",
           "antucoya", "caserones", "mantos", "lomas bayas", "zald", "franke", "andina",
           "salvador", "anglo", "teck", "glencore", "bhp", "antofagasta minerals"]

for arch in ["riles_2024.xlsx", "respeligrosos_2025.xlsx", "ventanilla.xlsx"]:
    p = os.path.join(B, arch)
    if not os.path.exists(p):
        print(f"  FALTA {arch}")
        continue
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    for hoja in wb.sheetnames[:3]:
        ws = wb[hoja]
        hdr = None
        n = 0
        hits = {g: 0 for g in GRANDES}
        muestra = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                hdr = [str(c)[:30] for c in row if c is not None]
                continue
            n += 1
            blob = " ".join(str(c) for c in row if c is not None).lower()
            for g in GRANDES:
                if g in blob:
                    hits[g] += 1
                    if len(muestra) < 4:
                        muestra.append((g, blob[:130]))
        enc = [h for h in (hdr or []) if h and not h.startswith("Columna")]
        print(f"\n{'='*92}")
        print(f"### {arch} · hoja '{hoja}'  ({n:,} filas de datos)")
        print(f"  columnas reales ({len(enc)}): {enc[:10]}")
        encontradas = {k: v for k, v in hits.items() if v}
        print(f"  MINERAS GRANDES encontradas: {len(encontradas)} de {len(GRANDES)} -> {encontradas}")
        for g, t in muestra[:3]:
            print(f"     [{g}] {t}")
    wb.close()
