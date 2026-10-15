#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDA los decisores de LinkedIn usando el HEADLINE COMPLETO (que sí trae "en <empresa>").

LA CLAVE: en los hallazgos de LinkedIn, el campo `cargo` guarda el headline ENTERO (ej. "Jefe
Mantención en Komatsu Chile S.A", "Gerente de bodega en STRABAG"). Eso permite validar pertenencia
sin salir a buscar nada — solo hay que mirar el "en <empresa>".

Criterio de VÁLIDO (para las de LinkedIn):
  1. El headline dice "en <empresa>" (o "<empresa>" aparece) -> pertenece.
  2. El cargo es de compra técnica, no ventas/RRHH/legal.
  3. El "nombre" es un nombre de persona, no un cargo copiado por el parser
     (caso real: nombre="JEFE DE OPERACION at MAXAM", que es el cargo).

Salida: datos/personas_validadas.json
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
GENERICOS = {"minera", "minero", "mineria", "compania", "compañia", "sociedad", "anonima", "chile",
             "empresa", "empresas", "grupo", "holding", "nacional", "sur", "norte", "central", "del",
             "las", "los", "san", "santa", "servicios", "industrial", "industria", "spa", "ltda"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


NO_COMPRA = re.compile(
    r"ventas|sales|marketing|seo|digital|reclutamiento|selecci[oó]n|compensaci|recursos humanos|"
    r"rrhh|talento|people|comunicaci|legal|fiscal|abogad|finanz|contab|tesorer|auditor|"
    r"relaciones p[uú]blicas|asuntos p[uú]blicos|brand|publicidad|directorio", re.I)
CARGO_COMO_NOMBRE = re.compile(
    r"^(jefe|gerente|superintendente|jefa|director|supervisor|ing|operador|tecnico|t[eé]cnico|"
    r"encargado|coordinador|responsable|head|manager|planner|asistente|analista|subgerente)\b", re.I)


def marca_de(nombre):
    toks = [t for t in norm(nombre).split() if len(t) > 3 and t not in GENERICOS]
    return max(toks, key=len) if toks else None


bdr = json.load(open(os.path.join(D, "buscador_decisores.json"), encoding="utf-8"))["resultados"]
plan = json.load(open(os.path.join(D, "plan_accion.json"), encoding="utf-8"))["plan"]
idx = {}
for x in bdr:
    for h in x["hallazgos"]:
        idx[(norm(x["empresa"]), norm(h["nombre"]))] = (h, x["empresa"])

print("=" * 100)
print("VALIDACIÓN DE LOS DECISORES DE LINKEDIN")
print("=" * 100)

tot = garant = ok_li = ajeno = nc = basura = sin = 0
empresas_mal, revisado = [], []
for e in plan:
    ne = norm(e["empresa"])
    marca = marca_de(e["empresa"])
    buenos, malos, no_compran, sucios, sin_d = [], [], [], [], []
    for c in e.get("contactos", []):
        tot += 1
        par = idx.get((ne, norm(c["nombre"])))
        if par is None:
            sin_d.append(c); sin += 1; continue
        h, emp = par
        f = h.get("fuente", "")
        # 1. garantizadas por la fuente
        if f.startswith("direcmin.com") or "Transparencia" in f:
            garant += 1
            (no_compran if NO_COMPRA.search(c["cargo"]) else buenos).append({**c, "tipo": "garantizada"})
            continue
        # 2. LinkedIn: validar con el headline
        txt = norm(h["cargo"])
        # el "nombre" es en realidad un cargo (basura del parser)
        if CARGO_COMO_NOMBRE.match(c["nombre"]):
            sucios.append({**c, "headline": h["cargo"]}); basura += 1; continue
        pert = (marca and marca in txt) or ne in txt
        if not pert:
            malos.append({**c, "headline": h["cargo"]}); ajeno += 1; continue
        if NO_COMPRA.search(c["cargo"]):
            no_compran.append(c); nc += 1; continue
        buenos.append({**c, "tipo": "linkedin validado", "headline": h["cargo"]}); ok_li += 1
    if malos or sucios:
        empresas_mal.append({"empresa": e["empresa"],
                             "ajenos": [f"{m['nombre']} | {m['cargo']} -> {m.get('headline','')}" for m in malos],
                             "basura": [f"{m['nombre']} | {m['cargo']}" for m in sucios]})
    revisado.append({"empresa": e["empresa"], "buenos": buenos, "ajenos": malos,
                     "no_compra": no_compran, "basura": sucios, "sin_dato": sin_d})

print(f"  en el plan:                        {tot:,}")
print(f"  GARANTIZADAS (Direcmin/Transp.):   {garant:,}")
print(f"  LINKEDIN VALIDADAS:                {ok_li:,}")
print(f"  -> TOTAL USABLES:                  {garant + ok_li:,} ({(garant+ok_li)/tot*100:.0f}%)")
print(f"\n  DESCARTADAS:")
print(f"    ajenas (otra empresa):           {ajeno:,}")
print(f"    cargo que no compra:             {nc:,}")
print(f"    nombre que es un cargo (parser): {basura:,}")
print(f"    sin dato:                        {sin:,}")

print(f"\n=== LAS DESCARTADAS POR AJENAS (muestra) ===")
c = 0
for x in empresas_mal:
    for a in x["ajenos"]:
        if c < 14:
            print(f"  {x['empresa'][:30]:32s} {a[:88]}")
            c += 1

print(f"\n=== LAS DESCARTADAS POR 'NOMBRE = CARGO' (parser) ===")
c = 0
for x in empresas_mal:
    for a in x["basura"]:
        if c < 12:
            print(f"  {x['empresa'][:30]:32s} {a[:80]}")
            c += 1

json.dump({"totales": {"en_plan": tot, "garantizadas": garant, "linkedin_validadas": ok_li,
                       "usables": garant + ok_li, "ajenas": ajeno, "no_compra": nc,
                       "basura_parser": basura, "sin_dato": sin},
           "empresas": revisado},
          open(os.path.join(D, "personas_validadas.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/personas_validadas.json")
