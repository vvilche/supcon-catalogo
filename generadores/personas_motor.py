#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BARRIDO DE PERSONAS POR ÁREA — el motor, importable desde execute_code.

POR QUÉ ES UN MÓDULO Y NO UN SCRIPT
------------------------------------------------------------------------------
`web_search` solo existe dentro del sandbox de execute_code (hermes_tools). Como script de
terminal no está, y el fallback (DuckDuckGo html) devuelve "anomaly detection" desde curl:
MEDIDO, 0 resultados y "anomaly" en el HTML. Así que el bucle de búsqueda tiene que correr en
execute_code, que importa este módulo para la parte determinística (parseo y clasificación).

QUÉ HACE CADA PARTE
  - `parsear_snippet`: saca (nombre, cargo) del perfil estructurado que devuelve el buscador
    (`**Nombre**` / `**Cargo**` en el snippet). Es lo que hace que no haga falta abrir LinkedIn.
  - `limpiar_persona`: quita el ruido medido — snippets donde el "nombre" es en realidad la
    EMPRESA (GNL Quintero S.A., Exportadora Los Fiordos Limitada), cargos cortados con salto de
    línea, y el campo `, Gerencia RMASSO` que el buscador concatena al nombre.
  - `clasificar_area`: asigna el área POR EL CARGO REAL, no por la consulta que la encontró.
    Medido por qué importa: "Subgerente de Contabilidad" entraba como Instrumentación porque lo
    encontró esa consulta; por cargo, no clasifica y se descarta.
"""
import re

AREAS_CONSULTA = [
    ("Medio Ambiente", "jefe de medio ambiente"),
    ("Calidad", "jefe de calidad"),
    ("Instrumentacion y Control", "jefe de instrumentacion y control"),
    ("Mantenimiento", "jefe de mantenimiento"),
]

# Clasificación por cargo. El orden importa: Medio Ambiente y Calidad van primero porque sus
# palabras son las más específicas ("gestión ambiental" no es Mantenimiento aunque diga gestión).
AREA_KW = [
    ("Medio Ambiente", ["medio ambiente", "medioambient", "ambiental", "gestion ambient",
                        "sustentab", "prevencion de riesgo", "hse", "ehs", "riles", "emision"]),
    ("Calidad", ["calidad", "aseguramiento", "laborator", "quimic"]),
    ("Instrumentacion y Control", ["instrument", "electrocontrol", "control e instrument",
                                   "automatiz", " iec", "sistemas de control", " dcs"]),
    ("Electrico", ["electric", "electrico", "electrica", "potencia", "alto voltaje"]),
    ("Mantenimiento", ["mantenim", "mantenc", "confiabilidad", "mecanic", "planificad"]),
    ("Produccion", ["produccion", "operacion", "planta", "proceso", "fabrica"]),
]

CARGOS = re.compile(
    r"jefe|gerente|supervisor|ingenier|coordinador|encargad|director|subgerente|superintendente|"
    r"especialista|analista|t[eé]cnico|prevenci[oó]n|instrument|mantenim|mantenci|calidad|"
    r"ambiente|operacion|producci|electric|control|automatiz|proceso|responsable", re.I)

RUIDO_NOMBRE = re.compile(r",|gerencia\s+[a-z]|asesor\s+amb|gestor\s+de|subgerencia", re.I)
STOP_BOLD = {"experience", "about", "education", "chile", "santiago", "linkedin",
             "see more", "show more"}


def parsear_snippet(desc):
    """(nombre, cargo) del perfil estructurado en el snippet."""
    out = []
    if not desc:
        return out
    bold = re.findall(r"\*\*([^*]{3,70})\*\*", desc)
    if len(bold) < 2:
        return out
    nombre = cargo = None
    for b in bold:
        b = b.strip()
        if b.lower() in STOP_BOLD:
            continue
        if CARGOS.search(b):
            if cargo is None:
                cargo = b
            continue
        if nombre is None and 2 <= len(b.split()) <= 5:
            nombre = b
    if nombre and cargo:
        out.append({"nombre": nombre, "cargo": cargo})
    return out


def es_empresa(nombre, empresa):
    """El 'nombre' es en realidad la razón social? (ruido medido del snippet)."""
    n = re.sub(r"[^A-Za-z0-9 ]", " ", (nombre or "").upper()).split()
    e = re.sub(r"[^A-Za-z0-9 ]", " ", (empresa or "").upper()).split()
    if not n or not e:
        return True
    comunes = len(set(n) & set(e))
    return comunes >= 2 and comunes >= len(n) * 0.6


def limpiar_persona(nombre, cargo, empresa):
    """Devuelve la persona limpia o None si es ruido."""
    nom = re.sub(r"\s+", " ", (nombre or "")).strip()
    car = re.sub(r"\s+", " ", (cargo or "")).strip()
    if not nom or not car:
        return None
    if es_empresa(nom, empresa):
        return None
    if RUIDO_NOMBRE.search(nom):
        return None
    toks = nom.split()
    if not (2 <= len(toks) <= 5):
        return None
    # un nombre de persona no lleva cargos ni siglas societarias
    if re.search(r"\b(s\.?a\.?|ltda|spa|scm|s\.a\.)\b", nom, re.I):
        return None
    area = clasificar_area(car)
    if not area:
        return None
    return {"empresa": empresa, "nombre": nom, "cargo": car, "area": area}


def clasificar_area(cargo):
    c = (cargo or "").lower()
    for area, kws in AREA_KW:
        if any(k in c for k in kws):
            return area
    return None


def fusionar(lista):
    """Dedupe por (persona, empresa), quedándose con el cargo más descriptivo.

    OJO: debe PRESERVAR el linkedin. Medido: la primera version devolvia solo
    (nombre, cargo, area) y se perdian los 258 enlaces de perfil que el buscador SI habia
    entregado — el regex los capturaba bien, los tiraba esta funcion.
    """
    seen = {}
    for r in lista:
        if not r:
            continue
        # 'empresa' puede venir en el registro; si falta, se usa cadena vacia para no romper
        emp = r.get("empresa", "")
        k = (r["nombre"].lower(), emp.upper())
        if k not in seen:
            seen[k] = {"nombre": r["nombre"], "cargo": r["cargo"], "area": r["area"],
                       "linkedin": r.get("linkedin", ""), "empresa": emp}
        else:
            # quedarse con el cargo mas descriptivo, y con el linkedin si aparecio
            if len(r["cargo"]) > len(seen[k]["cargo"]):
                seen[k]["cargo"] = r["cargo"]
                seen[k]["area"] = r["area"]
            if not seen[k]["linkedin"] and r.get("linkedin"):
                seen[k]["linkedin"] = r["linkedin"]
    return list(seen.values())
