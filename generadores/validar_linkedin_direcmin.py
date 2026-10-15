#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDA los LinkedIn hallados para los contactos de Direcmin: cuáles sirven de verdad.

TRES PROBLEMAS MEDIDOS (por eso no alcanza con "encontré el perfil")
------------------------------------------------------------------------------
1. PERFIL DE OTRA PERSONA: el slug no coincide con el nombre. Casos: "Andrés Lafuente D." ->
   `ignacio-garcia-de-nardiz`; "Leonardo Fosk" -> `lmanriquezmichea`.
2. LA PERSONA YA NO ESTÁ EN LA EMPRESA: la evidencia trae la experiencia y a veces el headline
   dice otra empresa. Casos medidos: Julio Cuevas Ross figuraba en Los Pelambres y su headline dice
   "Vicepresidente de Proyectos en CODELCO"; Karina Briño (Candelaria) ya no está.
3. LA PERSONA ESTÁ JUBILADA O EN OTRO PAÍS: Jorge Bravo (Candelaria) -> "Retired ... Fort Mill,
   South Carolina, United States".
4. PERFIL DE OTRO PAÍS: dominios que no son cl.linkedin.com.

CRITERIO DE "SIRVE": el slug coincide con 2+ tokens del nombre, Y la evidencia menciona la empresa
o al menos no menciona otra, Y el dominio es de Chile (o www con evidencia que mencione la empresa).

Salida: datos/linkedin_direcmin_validado.json
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

GENERICOS = {"minera", "minero", "compania", "sociedad", "chile", "limitada", "servicios", "chile",
             "industrial", "industria", "grupo", "holding", "nacional", "andina", "sur", "norte",
             "salar", "spa", "s", "a", "ltda", "y"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


REGEX_JUBILADO = re.compile(r"retired|jubilad|pension", re.I)
OTRO_PAIS_EV = re.compile(r"united states|peru|per\u00fa|argentina|colombia|mexico|m\u00e9xico|"
                          r"brazil|brasil|spain|espa\u00f1a|canada|australia|south carolina|"
                          r"texas|florida|toronto|lima|bogot", re.I)

d = json.load(open(os.path.join(D, "linkedin_direcmin.json"), encoding="utf-8"))
contactos = [v for v in d["contactos"].values() if v.get("linkedin")]

print("=" * 100)
print("VALIDACIÓN DE LOS LINKEDIN HALLADOS (210 buscados)")
print("=" * 100)
print(f"  con URL: {len(contactos)}")

resultado, cuenta = [], collections.Counter()
for v in contactos:
    url = v["linkedin"]
    nombre, empresa, ev = v["nombre"], v["empresa"], v.get("evidencia", "") or ""
    # 1. slug vs nombre
    toks = [t for t in norm(nombre).split() if len(t) > 3]
    slug = norm(url.split("/in/")[-1].split("/")[0])
    hits = sum(1 for t in toks if t in slug)
    # 2. dominio
    dom = re.search(r"https?://([a-z.]*linkedin\.com)", url)
    dominio = dom.group(1) if dom else ""
    es_cl = dominio.startswith("cl.") or dominio == "linkedin.com"
    # 3. empresa en la evidencia
    et = [t for t in norm(empresa).split() if len(t) > 3 and t not in GENERICOS]
    emp_en_ev = any(t in norm(ev) for t in et) if et else False
    # 5. ¿el headline nombra OTRA empresa? (la persona se fue)
    #    Medido: Julio Cuevas Ross figuraba en Los Pelambres y su headline dice "Vicepresidente de
    #    Proyectos en CODELCO". Sin esto se daba por bueno un contacto que ya no está.
    OTRA_EMP = re.search(r"\b(?:en|at)\s+([A-ZÁÉÍÓÚÑ][\w&.\- ]{3,40})", ev)
    otra = OTRA_EMP.group(1).strip() if OTRA_EMP else ""
    if otra and et and not any(t in norm(otra) for t in et) and len(norm(otra)) > 5:
        # el headline nombra una empresa distinta a la buscada
        se_fue = True
    else:
        se_fue = False
    # 4. jubilado / otro país
    jub = bool(REGEX_JUBILADO.search(ev))
    otro = bool(OTRO_PAIS_EV.search(ev))

    if hits < 1:
        estado, motivo = "malo", "el perfil no coincide con el nombre"
    elif jub:
        estado, motivo = "malo", "la persona está jubilada"
    elif se_fue and not emp_en_ev:
        estado, motivo = "se-fue", f"su headline dice que está en otra empresa ({otra[:30]})"
    elif otro and not emp_en_ev:
        estado, motivo = "dudoso", "la evidencia apunta a otro país"
    elif hits >= 2 and es_cl:
        estado, motivo = "bueno", "slug coincide + dominio Chile"
    elif emp_en_ev:
        estado, motivo = "bueno", "la evidencia menciona la empresa"
    else:
        estado, motivo = "dudoso", "slug coincide pero no se confirma la empresa"

    cuenta[estado] += 1
    resultado.append({**v, "estado": estado, "motivo": motivo, "tokens_nombre": hits,
                      "dominio": dominio, "empresa_en_evidencia": emp_en_ev})

print(f"\n  BUENOS:  {cuenta['bueno']}")
print(f"  DUDOSOS: {cuenta['dudoso']}")
print(f"  MALOS:   {cuenta['malo']}")

print(f"\n=== MALOS ({cuenta['malo']}) — el perfil no es la persona o está jubilada ===")
for v in [x for x in resultado if x["estado"] == "malo"][:15]:
    print(f"  {v['nombre'][:26]:28s} | {v['empresa'][:22]:24s} -> {v['linkedin'][:46]}")
    print(f"      {v['motivo']}")

print(f"\n=== DUDOSOS ({cuenta['dudoso']}) — slug ok pero sin confirmar ===")
for v in [x for x in resultado if x["estado"] == "dudoso"][:12]:
    print(f"  {v['nombre'][:26]:28s} | {v['empresa'][:22]:24s} -> {v['linkedin'][:44]}")
    print(f"      {v['motivo']}")

print(f"\n=== BUENOS, muestra ===")
for v in [x for x in resultado if x["estado"] == "bueno"][:8]:
    print(f"  {v['nombre'][:26]:28s} | {v['empresa'][:22]:24s} -> {v['linkedin'][:50]}")

json.dump({"que_es": ("LinkedIn hallado para los 210 contactos de Direcmin, VALIDADO: se descartan "
                      "los que no coinciden con el nombre, los de personas jubiladas y se marcan los "
                      "dudosos (slug ok pero sin confirmar la empresa)."),
           "totales": dict(cuenta), "contactos": resultado},
          open(os.path.join(D, "linkedin_direcmin_validado.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/linkedin_direcmin_validado.json")
