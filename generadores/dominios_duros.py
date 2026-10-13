#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOMINIOS DUROS: el dominio de cada empresa del plan de contacto, tomado de su PROPIA FICHA.

POR QUE ESTE ARCHIVO EXISTE
------------------------------------------------------------------------------
El intento anterior (generadores/resolver_dominios.py) adivinaba el dominio a partir del
nombre de la empresa. Eso NO es confiable y quedo medido:

  AGUAS PATAGONIA DE AYSEN  -> patagonia.com   (marca de ropa)
  CECINAS WINTER            -> winter.com      (otra cosa)
  BOTTAI HERMANOS           -> hermanos.cl     (otra cosa)

Los tres dominios EXISTEN y tienen MX, asi que la verificacion DNS pasaba: MX prueba que el
dominio existe, NO que sea de esa empresa. Un correo a la empresa equivocada es peor que no
tener correo (rebota, o llega a un tercero con datos de un cliente).

LA FUENTE DURA que si sirve ya estaba en el Mac y no se estaba usando:

  ~/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo/catalogo-*/research/*.json
  (3.157 fichas de empresa)

Cada ficha trae un bloque `contacto_corporativo` con web, telefono y correo, y el campo
`fuente` dice de donde salio (RETC, el sitio de la empresa, etc.). El dominio se toma de ahi:
es el dominio que la propia fuente declara, no uno construido con el nombre.

Salida: datos/dominios_duros.json
"""
import json, glob, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
WS = os.path.expanduser("~/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo")

DOM = re.compile(r"^(?:https?://)?(?:www\.)?([a-z0-9][a-z0-9\-]*\.[a-z0-9\-\.]*[a-z]{2,})", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# Sufijos y palabras societarias que no aportan al matching.
BASURA = re.compile(
    r"\b(S\.?A\.?C\.?|S\.?A\.?|SPA|LTDA\.?|LIMITADA|E\.?I\.?R\.?L\.?|SCM|SOCIEDAD|COMPANIA|CIA\.?|"
    r"EMPRESA|INDUSTRIAS?|COMERCIAL|SERVICIOS?|CHILE|DE|DEL|LA|EL|LOS|LAS|Y)\b", re.I)


def dominio_de_web(w):
    """Extrae el dominio de un campo web que puede traer texto y cita, ej.
    'www.cmpc.com ([cmpccelulosa.cl])'."""
    w = (w or "").strip()
    if not w:
        return ""
    w = re.sub(r"\(.*?\)", "", w).strip()
    partes = w.split()
    if not partes:
        return ""
    m = DOM.match(partes[0])
    return m.group(1).lower() if m else ""


def tokens(s):
    """Tokens distintivos del nombre, sin sufijos societarios ni ruido."""
    s = BASURA.sub(" ", (s or "").upper())
    return [t for t in re.sub(r"[^A-Z0-9 ]", " ", s).split() if len(t) > 3]


def main():
    fichas = glob.glob(os.path.join(WS, "catalogo-*/research/*.json"))
    if not fichas:
        print(f"ERROR: no hay fichas en {WS}/catalogo-*/research/", file=sys.stderr)
        sys.exit(1)

    # --- indice de dominios desde las fichas (fuente dura) ---
    por_empresa = {}
    idx = {}   # token -> [(nombre, dominio)]
    for f in fichas:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        nom = (d.get("empresa") or "").strip()
        cc = d.get("contacto_corporativo") or {}
        dm = dominio_de_web(cc.get("web"))
        if not (nom and dm):
            continue
        clave = nom.upper()
        por_empresa[clave] = {
            "dominio": dm,
            "web": cc.get("web", ""),
            "telefono": cc.get("telefono", ""),
            "correo": cc.get("correo", ""),
            "fuente": cc.get("fuente", ""),
            "ficha": os.path.relpath(f, WS),
        }
        for t in tokens(nom):
            idx.setdefault(t, []).append(clave)

    print(f"fichas leidas:                {len(fichas)}")
    print(f"empresas con dominio en ficha: {len(por_empresa)}")

    # --- cruzar con el plan de contacto ---
    pc = json.load(open(os.path.join(D, "plan_contacto.json"), encoding="utf-8"))
    plan = pc["plan"]

    resueltas = {}
    sin = []
    for e in plan:
        nombre = e["empresa"]
        clave = nombre.upper().strip()
        hit = por_empresa.get(clave)

        if not hit:
            toks = set(tokens(nombre))
            cand = {}
            for t in toks:
                for k in idx.get(t, []):
                    cand[k] = cand.get(k, 0) + 1
            if cand:
                mejor = max(cand.items(), key=lambda kv: kv[1])
                # exigir 2 tokens en comun: con 1 token la ambiguedad es alta
                if mejor[1] >= 2:
                    hit = por_empresa[mejor[0]]

        if hit:
            resueltas[nombre] = dict(hit, match="exacto" if hit is por_empresa.get(clave) else "tokens")
        else:
            sin.append(nombre)

    print(f"\nplan de contacto:             {len(plan)} empresas")
    print(f"  CON dominio duro:           {len(resueltas)}")
    print(f"  SIN dominio:                {len(sin)}")

    # --- correos que la propia ficha ya declara (sin costo, sin API) ---
    con_correo = 0
    for nom, v in resueltas.items():
        if (v.get("correo") or "").strip():
            con_correo += 1
    print(f"  de esas, con correo ya declarado en la ficha: {con_correo}")

    json.dump({
        "metodo": ("Dominio tomado de la ficha de la empresa (campo contacto_corporativo.web), "
                   "NO inferido del nombre. El match contra el plan es por razon social exacta "
                   "o por 2+ tokens distintivos en comun."),
        "limite": ("Solo 236 de las 3.157 fichas traen web. El resto no tiene fuente de dominio "
                   "y no se inventa: va a la lista 'sin_dominio'. MX no se usa como validacion "
                   "porque prueba que el dominio existe, no que sea de esa empresa."),
        "fuente": os.path.relpath(WS, os.path.expanduser("~")) + "/catalogo-*/research/*.json",
        "empresas": resueltas,
        "sin_dominio": sin,
    }, open(os.path.join(D, "dominios_duros.json"), "w"), ensure_ascii=False, indent=1)
    print(f"\nguardado: datos/dominios_duros.json")


if __name__ == "__main__":
    main()
