#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESOLUCIÓN DE DOMINIOS: conseguir el dominio corporativo de las empresas que no lo tienen.

PROBLEMA. 1.541 de 2.327 personas quedaron sin correo porque no se conoce el dominio de su
empresa (945 empresas distintas, entre ellas Collahuasi, Soprole, Agrosuper, Masisa).
Sin dominio no hay correo que inferir.

ESTRATEGIA, en orden de confiabilidad (y de costo):
  1. REGLA DURA: no se inventa un dominio. Un dominio equivocado genera un correo que rebota.
  2. Cache de dominios YA conocidos en el Mac (catálogo, correos reales, otras fuentes).
  3. Normalización del nombre: muchas empresas usan su razón social sin el sufijo legal
     (SOPROLE S.A. → soprole.cl). Se prueba con .cl y .com.
  4. Verificación DNS/MX: un dominio inventado no tiene registros MX. Se verifica antes de darlo
     por bueno. Esto convierte el paso 3 de "adivinanza" en "hipótesis verificada".
  5. Lo que no se puede verificar queda FUERA. No se publica un dominio sin MX.

Salida: datos/dominios_empresas.json
"""
import os, json, re, unicodedata, collections, socket, subprocess

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

# ---------- 1. cache de dominios ya conocidos ----------
print("=== 1. dominios ya conocidos ===")
dom = {}
import glob
for f in glob.glob(os.path.join(WS, "catalogo-*/research/*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    cc = d.get("contacto_corporativo") or {}
    w = (cc.get("web") or "").strip()
    if w:
        m = re.search(r"(?:https?://)?(?:www\.)?([a-z0-9-]+\.[a-z.]{2,})", w.lower())
        if m: dom[clave(d["empresa"])] = m.group(1)
print(f"  del catálogo: {len(dom):,}")

con = json.load(open(os.path.join(D, "contactos_enriquecidos.json"), encoding="utf-8"))
for p in con["personas"]:
    if p.get("correo") and "@" in p["correo"]:
        dm = p["correo"].split("@")[-1].lower().strip()
        if not any(g in dm for g in ["gmail","hotmail","yahoo","outlook","live."]):
            dom.setdefault(clave(p["empresa"]), dm)
print(f"  + de correos reales: {len(dom):,}")

# ---------- 2. las empresas que faltan ----------
sin = collections.Counter()
for p in con["personas"]:
    if p["correo_estado"] == "sin_dominio":
        sin[p["empresa"]] += 1
print(f"\n=== 2. empresas sin dominio: {len(sin):,} ===")

# ---------- 3. hipótesis de dominio ----------
# Palabras GENERICAS del rubro: si el dominio se construye con una de estas, apunta a otra
# empresa. Medido: 'CIA MINERA Collahuasi' daba minera.cl y 'ALIMENTOS Agrosuper' alimentos.cl.
GENERICAS = {"alimentos","alimento","cementos","cemento","minera","mineria","aguas","agua",
  "cecinas","cecina","aserraderos","aserradero","constructora","construccion","servicios",
  "comercial","industria","industrial","sociedad","compania","grupo","holding","chile",
  "nacional","central","planta","productos","producto","frigorifico","pesquera","salmonera",
  "transportes","transporte","energia","electricidad","generadora","distribuidora","quimica",
  "papelera","forestal","maderas","madera","acero","aceros","vidrios","plasticos","textil"}

def candidatos(empresa):
    """Dominios probables a partir de la razón social, usando el token MAS DISTINTIVO."""
    n = norm(empresa)
    t = [x for x in n.split() if x not in STOP and len(x) > 2]
    if not t: return []
    # ordenar: primero los NO genéricos, más largos primero (más distintivos)
    # Palabras de una silaba y muy comunes: no identifican a nadie ('AGUAS SAN PEDRO' -> san/pedro)
    DEBILES = {"san","santa","don","dona","del","las","los","sur","norte","este","oeste"}
    distintivos = [x for x in t if x not in GENERICAS and x not in DEBILES and len(x) >= 4]
    # APELLIDOS: en razones de 3+ tokens el ultimo suele ser apellido ('BOTTAI HERMANOS ANONIMA')
    if len(distintivos) >= 3:
        distintivos = distintivos[:-1]
    cands = []
    # PRIORIDAD 1: el nombre COMPUESTO de los distintivos (aguaspatagonia, aguassanpedro).
    # Es lo que mas empresas chilenas usan para su dominio cuando la razon social tiene 2 palabras.
    if len(distintivos) >= 2:
        for tld in [".cl",".com"]:
            cands.append("".join(distintivos) + tld)
            cands.append("".join(distintivos[:2]) + tld)
    # PRIORIDAD 2: el token mas largo solo
    orden = sorted(distintivos, key=len, reverse=True) + [x for x in t if x in GENERICAS]
    for base in orden[:2]:
        if len(base) < 6: continue      # menos de 6 letras es demasiado ambiguo
        for tld in [".cl", ".com", ".com.cl"]:
            cands.append(base + tld)
    # combinaciones de dos tokens distintivos (ej. aguaspatagonia)
    if len(distintivos) >= 2:
        for tld in [".cl",".com"]:
            cands.append("".join(distintivos[:2]) + tld)
            cands.append(distintivos[0] + distintivos[1] + tld)
    return list(dict.fromkeys(cands))

def tiene_mx(dominio):
    """Verifica que el dominio tenga registros MX: sin MX no recibe correo."""
    try:
        out = subprocess.run(["dig","+short","MX",dominio], capture_output=True, text=True, timeout=8)
        return bool(out.stdout.strip())
    except Exception:
        return False

# ---------- 4. verificar (solo las que tienen más gente, para no tardar de más) ----------
top = [e for e, _ in sin.most_common(120)]
print(f"\n=== 3. verificando MX de las {len(top)} empresas con más gente ===")
resueltos = {}
for i, emp in enumerate(top, 1):
    # el dominio debe CONTENER el token distintivo: evita aceptar un dominio genérico que
    # existe pero es de otra empresa (minera.cl para Collahuasi)
    n = norm(emp)
    DEBILES2 = {"san","santa","don","dona","del","las","los","sur","norte","este","oeste"}
    dist = [x for x in n.split() if x not in STOP and len(x) > 2 and x not in GENERICAS
            and x not in DEBILES2 and len(x) >= 4]
    if len(dist) >= 3: dist = dist[:-1]
    for c in candidatos(emp):
        # REGLA ESTRICTA: el dominio debe contener el token DISTINTIVO MAS LARGO completo.
        # MX solo prueba que el dominio existe y recibe correo, NO que sea de esa empresa.
        # Medido: 'AGUAS PATAGONIA DE AYSEN' pasaba con patagonia.com (una marca de ropa) porque
        # ese dominio tiene MX. Un correo a la empresa equivocada es peor que no tener correo.
        if not dist: break
        principal = max(dist, key=len)
        if principal not in c: continue
        # y si hay dos tokens distintivos largos, el dominio debe contener ambos o el compuesto
        largos = [d for d in dist if len(d) >= 6]
        if len(largos) >= 2:
            comp = "".join(largos)
            if not (all(d in c for d in largos) or comp in c): continue
        if tiene_mx(c):
            resueltos[emp] = c
            break
    if i % 20 == 0: print(f"  {i}/{len(top)} verificadas, {len(resueltos)} con dominio")

print(f"\n=== RESULTADO ===")
print(f"  empresas verificadas con dominio: {len(resueltos):,} de {len(top):,} probadas")
print(f"  empresas que siguen sin dominio:  {len(sin)-len(resueltos):,}")
print(f"\n  ejemplos resueltos:")
for emp, dn in list(resueltos.items())[:15]:
    print(f"    {emp[:42]:44s} -> {dn}")

json.dump({"metodo": ("Dominio por razón social normalizada, VERIFICADO con registros MX via dig. "
   "Sin MX el dominio no recibe correo y se descarta: no se publica un dominio sin verificar."),
   "dominios_cache": dom, "resueltos_por_mx": resueltos},
  open(os.path.join(D,"dominios_empresas.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/dominios_empresas.json")
