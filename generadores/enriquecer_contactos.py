#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENRIQUECEDOR DE CONTACTOS: dominios + patrón de correo + más gente.

PROBLEMA. Los 1.628 tomadores del catálogo traen nombre y cargo, pero 0 correos. Sin correo no
se puede contactar. Se resuelve en dos frentes:

  A. BUSCAR MÁS GENTE: hay otras fuentes de contactos en el Mac con personas y correos reales
     que no se habían usado (657 leads del workspace de Innovación, 684 del CRM, los SSCC).
  B. INFERIR EL CORREO: con el dominio de la empresa (196 conocidos) y el patrón que esa
     empresa usa (observado en correos reales), se construye el correo probable.

REGLA DURA: un correo inferido NO es un correo verificado. Se marca siempre el nivel:
  - `verificado`   : vino así en una fuente
  - `inferido`     : se construyó con el patrón de la empresa, mismo dominio
  - `sin_dominio`  : no se conoce el dominio, no se inventa nada
NUNCA se publica un inferido como si fuera verificado.

Salida: datos/contactos_enriquecidos.json
"""
import os, json, glob, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
WS = "/Users/victorvilche/orca/workspaces/FuentesdeInfoProyectos/ProyectosInfo"

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s).strip()

STOP = {"s","a","sa","ltda","limitada","spa","cia","compania","sociedad","empresa","de","del",
        "la","el","los","las","y","chile","servicios","comercial","industrial","inversiones"}
def clave(s):
    return " ".join(sorted(t for t in norm(s).split() if t not in STOP and len(t) > 2))

# ============================================================================
# A. JUNTAR TODAS LAS FUENTES DE PERSONAS DEL MAC
# ============================================================================
print("=== A. fuentes de personas ===")
personas = []          # {empresa, nombre, cargo, correo, telefono, linkedin, origen}

# A1. el catálogo (1.628 tomadores, con LinkedIn, sin correo)
n_cat = 0
for f in glob.glob(os.path.join(WS, "catalogo-*/research/*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    emp = d.get("empresa")
    for t in (d.get("tomadores") or []):
        if not t.get("nombre"): continue
        personas.append({"empresa": emp, "nombre": t["nombre"], "cargo": t.get("cargo"),
          "correo": t.get("correo") or "", "telefono": t.get("telefono") or "",
          "linkedin": t.get("linkedin") or "", "rol_compra": t.get("rol_compra"),
          "tipo": t.get("tipo"), "origen": "catalogo_prospeccion"})
        n_cat += 1
print(f"  catálogo de prospección:  {n_cat:>5,}")

# A2. leads con correo real (workspace de Innovación)
FUENTES_EXTRA = [
 ("/Users/victorvilche/orca/workspaces/InnovaciónAGentica/RagInnovación/datos/leads_en_falta.json",
  "empresa", "contacto", "email", "innovacion_leads"),
]
n_extra = collections.Counter()
for ruta, k_emp, k_nom, k_mail, origen in FUENTES_EXTRA:
    if not os.path.exists(ruta): continue
    try: dd = json.load(open(ruta, encoding="utf-8"))
    except Exception: continue
    if isinstance(dd, dict): dd = dd.get("leads") or dd.get("confirmados") or []
    for x in (dd if isinstance(dd, list) else []):
        emp = x.get(k_emp); nom = x.get(k_nom); mail = x.get(k_mail)
        if emp and (nom or mail):
            personas.append({"empresa": emp, "nombre": nom or "", "cargo": x.get("cargo") or "",
              "correo": mail or "", "telefono": x.get("telefono") or "",
              "linkedin": "", "rol_compra": None, "tipo": None, "origen": origen})
            n_extra[origen] += 1
for k, v in n_extra.items(): print(f"  {k:26s} {v:>5,}")

n_crm = 0
f_crm = "/Users/victorvilche/CONECTA_Proyecto/CONECTA_Conocimiento/leads_produccion.json"
if os.path.exists(f_crm):
    dd = json.load(open(f_crm, encoding="utf-8"))
    for x in (dd.get("leads") or []):
        n = x.get("name") or x.get("partner_name")
        if n:
            personas.append({"empresa": x.get("partner_name") or n, "nombre": n,
              "cargo": x.get("function") or "", "correo": x.get("email_from") or "",
              "telefono": x.get("phone") or "", "linkedin": "", "rol_compra": None,
              "tipo": None, "origen": "crm_odoo"})
            n_crm += 1
print(f"  CRM Odoo:                 {n_crm:>5,}")

print(f"  TOTAL personas:           {len(personas):>5,}")

# ============================================================================
# B. DOMINIOS Y PATRONES DE CORREO
# ============================================================================
print("\n=== B. dominios y patrones ===")
dominios = {}   # empresa (clave normalizada) -> dominio
for f in glob.glob(os.path.join(WS, "catalogo-*/research/*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    cc = d.get("contacto_corporativo") or {}
    w = (cc.get("web") or "").strip()
    if w:
        m = re.search(r"(?:https?://)?(?:www\.)?([a-z0-9-]+\.[a-z.]{2,})", w.lower())
        if m: dominios[clave(d["empresa"])] = m.group(1)

# completar con dominios de correos REALES (los que ya vinieron verificados)
for p in personas:
    if p["correo"] and "@" in p["correo"]:
        dom = p["correo"].split("@")[-1].lower().strip()
        # descartar dominios genericos de correo
        if not any(g in dom for g in ["gmail","hotmail","yahoo","outlook","live."]):
            dominios.setdefault(clave(p["empresa"]), dom)
print(f"  dominios conocidos: {len(dominios):,}")

# patrón de correo POR EMPRESA, observado en los correos reales
def partes(nombre):
    n = norm(nombre)
    t = [x for x in n.split() if x]
    if len(t) < 2: return None
    return t[0], t[-1]

def patron_de(loc, nombre):
    pp = partes(nombre)
    if not pp: return None
    nom, ape = pp
    if loc == nom[0] + ape: return "inicial_apellido"
    if loc == nom + ape: return "nombre_apellido"
    if loc == nom + "." + ape: return "nombre.apellido"
    if loc == nom[0] + "." + ape: return "inicial.apellido"
    if loc == nom[0] + ape[0]: return "iniciales"
    if loc.startswith(nom): return "nombre_sufijo"
    if loc.startswith(nom[0]): return "inicial_sufijo"
    return None

patrones = {}   # empresa -> patron (el primero observado)
for p in personas:
    if p["correo"] and "@" in p["correo"] and p.get("nombre"):
        loc = p["correo"].split("@")[0].lower()
        pt = patron_de(loc, p["nombre"])
        if pt: patrones.setdefault(clave(p["empresa"]), pt)
print(f"  patrones aprendidos: {len(patrones):,}")

# patrón por defecto: el más común en Chile (inicial + apellido)
GEN = collections.Counter(patrones.values())
print(f"  distribución de patrones: {dict(GEN.most_common(5))}")

def construir(nombre, dominio, patron):
    pp = partes(nombre)
    if not pp: return None
    nom, ape = pp
    ap = {"inicial_apellido": nom[0]+ape, "nombre_apellido": nom+ape,
          "nombre.apellido": nom+"."+ape, "inicial.apellido": nom[0]+"."+ape,
          "iniciales": nom[0]+ape[0]}.get(patron)
    return f"{ap}@{dominio}" if ap else None

# ============================================================================
# C. ENRIQUECER
# ============================================================================
print("\n=== C. enriquecer ===")
stats = collections.Counter()
for p in personas:
    k = clave(p["empresa"])
    dom = dominios.get(k)
    if p["correo"]:
        p["correo_estado"] = "verificado"
        stats["verificado"] += 1
    elif dom and p.get("nombre"):
        pt = patrones.get(k) or "inicial_apellido"
        mail = construir(p["nombre"], dom, pt)
        if mail:
            p["correo_inferido"] = mail
            p["correo_patron"] = pt
            p["correo_estado"] = "inferido"
            stats["inferido"] += 1
        else:
            p["correo_estado"] = "sin_patron"; stats["sin_patron"] += 1
    else:
        p["correo_estado"] = "sin_dominio" if not dom else "sin_nombre"
        stats[p["correo_estado"]] += 1

print(f"  correo VERIFICADO:  {stats['verificado']:>5,}")
print(f"  correo INFERIDO:    {stats['inferido']:>5,}")
print(f"  sin dominio:        {stats['sin_dominio']:>5,}")
print(f"  sin nombre:         {stats['sin_nombre']:>5,}")

# agrupar por empresa
por_emp = collections.defaultdict(list)
for p in personas:
    por_emp[clave(p["empresa"])].append(p)
print(f"\n  empresas con al menos una persona: {len(por_emp):,}")
con_mail = sum(1 for v in por_emp.values() if any(x["correo_estado"] in ("verificado","inferido") for x in v))
print(f"  empresas con al menos un correo:   {con_mail:,}")

json.dump({
 "metodo": ("Junta todas las fuentes de personas del Mac (catálogo de prospección con 1.628 "
   "tomadores, 657 leads con correo real, 684 del CRM) y les infiere el correo con dos datos: "
   "el DOMINIO de la empresa (196 conocidos) y el PATRÓN de correo que esa empresa usa "
   "(observado en correos reales: inicial+apellido, nombre.apellido, etc)."),
 "regla": ("Un correo inferido NO es verificado. Cada contacto lleva `correo_estado`: "
   "verificado / inferido / sin_dominio / sin_nombre. Nunca se publica un inferido como real."),
 "resumen": dict(stats),
 "patrones_por_empresa": {k: v for k, v in list(patrones.items())[:200]},
 "personas": personas,
}, open(os.path.join(D,"contactos_enriquecidos.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/contactos_enriquecidos.json")
