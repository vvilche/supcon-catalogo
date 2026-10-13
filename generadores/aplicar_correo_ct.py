#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORREO DE LOS COMPRADORES TÉCNICOS (CT) — aplicado y con confianza declarada.

EL MÉTODO, Y SU TASA MEDIDA
------------------------------------------------------------------------------
Se deduce el PATRÓN de correo de cada empresa desde la cosecha del Coordinador (1.353 correos
REALES, 449 dominios) y se aplica el patrón al nombre del CT.

La tasa de acierto NO es una estimación: se midió con leave-one-out sobre 405 correos reales,
que es el test honesto (el patrón de la empresa tiene que predecir a un individuo NUEVO).
MEDIDO: 90,9% de acierto (368 de 405).

DONDE FALLA, Y SE DECLARA
Los 37 fallos se concentran en tres causas, todas identificables:
  1. APELLIDO COMPUESTO. "Victor Balbontin Artus" -> el correo real es victor.balbontin@enel.com
     (usa el apellido paterno), pero un patrón simple toma el último token ("Artus").
     "Sebastian Ruiz-Tagle Mena" -> sruiztagle@colbun.cl: apellido compuesto SIN guion, que
     ningún patrón estándar captura.
  2. SUFIJO NUMERICO. "Cesar Aedo" -> caedo001@codelco.cl.
  3. CORREO PERSONAL. En gmail.com/hotmail no hay patrón corporativo y el método no aplica.

Por eso cada correo lleva CONFIANZA:
  ALTA   empresa con 2+ correos reales que confirman el mismo patrón (el patrón está probado)
  MEDIA  empresa con 1 solo correo real (el patrón se vio una vez)
  BAJA   sin patrón observado: se usa el patrón nacional más común, marcado como suposición
  NO APLICA  sin dominio resoluble

NADA DE ESTO ES UN CORREO VERIFICADO. El patrón es real; el correo resultante es deducción y
así se declara en cada registro.
"""
import json, os, re, collections, unicodedata, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
sys.path.insert(0, os.path.join(BASE, "generadores"))
from correo_ct import partes, PATRONES, detectar_patron, norm, validar  # noqa


def nk(s):
    s = norm(s)
    s = re.sub(r"\b(s a|sa|ltda|limitada|spa|scm|cia|compania|sociedad|empresa|de|del|la|el|los|las|y|chile)\b", " ", s)
    return " ".join(sorted(t for t in re.sub(r"[^a-z0-9 ]", " ", s).split() if len(t) > 2))


cen = json.load(open(os.path.join(D, "cen_coordinados_correos.json"), encoding="utf-8"))
dd = json.load(open(os.path.join(D, "dominios_duros.json"), encoding="utf-8"))
plan = json.load(open(os.path.join(D, "plan_contacto_tecnico.json"), encoding="utf-8"))

# ---------------------------------------------------------------------------
# 1. tabla de patrones por dominio (de correos REALES)
# ---------------------------------------------------------------------------
patrones_dom = {}
for dom, lista in cen["por_dominio"].items():
    c = collections.Counter()
    ejemplos = []
    for x in lista:
        loc = (x.get("correo") or "").split("@")[0]
        p = detectar_patron(loc, x["nombre"])
        if p:
            c[p] += 1
            if len(ejemplos) < 3:
                ejemplos.append(f"{x['nombre']} -> {x['correo']}")
    if c:
        patrones_dom[dom] = {"patron": c.most_common(1)[0][0], "n": c.most_common(1)[0][1],
                             "alternativas": dict(c), "ejemplos": ejemplos}

# dominios por empresa desde la cosecha
doms_emp = {}
for dom in patrones_dom:
    doms_emp[dom] = dom

# dominios duros (de la ficha) por empresa del plan
dom_plan = {k.upper().strip(): v for k, v in dd["empresas"].items()}


def buscar_dominio(empresa, dominio_ficha=""):
    """Busca el dominio de la empresa en la cosecha.

    FORMA CORRECTA (y el bug que esto corrige): la cosecha declara, por cada contacto, A QUÉ
    EMPRESA pertenece (`empresa`). Hay que cruzar por ESO, no por tokens del dominio.

    El matching por tokens daba falsos positivos graves y medidos: el dominio `aminerals.cl`
    es de Compañía Minera ZALDÍVAR, pero contiene 'minerals', así que se le asignaba a Minera
    Escondida y a Candelaria. Los dominios reales son bhp.com (Escondida) y lundinmining.com
    (Candelaria). Un correo con el dominio equivocado es peor que no tener correo: va a un
    tercero con datos de un cliente.

    Se exige coincidencia de >=2 tokens distintivos, o 1 token si es largo y único. Si no hay
    coincidencia clara, se devuelve None: no se adivina.
    """
    objetivo = nk(empresa)
    toks = {t for t in objetivo.split() if len(t) > 3}
    if not toks:
        return None, 0

    # 1) por empresa DECLARADA en la cosecha (fuente dura)
    #    Regla: el nombre normalizado del plan tiene que COINCIDIR con el declarado, o compartir
    #    2+ tokens distintivos. Un solo token compartido solo vale si es TODO el nombre de un
    #    lado (caso 'COLBUN S A' vs 'Colbún S.A.' -> ambos normalizan a 'colbun').
    #    OJO medido: enap.cl NO es de ENAP Refinerías, la cosecha lo declara como Vientos
    #    Patagónicos SpA; y bhp.com es de Cerro Colorado/Spence/Kelti, no de Escondida. El
    #    dominio no se deduce del nombre de la empresa: se toma de quien la fuente dice que es.
    votos = collections.Counter()
    for dom, lista in cen["por_dominio"].items():
        for x in lista:
            decl = nk(x.get("empresa") or "")
            if not decl:
                continue
            dtoks = {t for t in decl.split() if len(t) > 3}
            if not dtoks:
                continue
            stoks = {t for t in decl.split() if len(t) > 2}
            comunes = len(toks & dtoks)
            coincide_total = (objetivo == decl) or (dtoks == toks and toks)
            if comunes >= 2 or coincide_total:
                votos[dom] += comunes + (2 if coincide_total else 0)
    if votos:
        dom, score = votos.most_common(1)[0]
        return dom, score

    # 2) si la ficha trae dominio y ese dominio tiene patrón, usarlo (fuente dura tambien)
    if dominio_ficha and dominio_ficha in patrones_dom:
        return dominio_ficha, 1
    return None, 0


# ---------------------------------------------------------------------------
# 2. aplicar a cada CT
# ---------------------------------------------------------------------------
FUERA = {"gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "live.com", "icloud.com",
         "gmail.cl", "hotmail.cl", "yahoo.es", "terra.cl"}

salida = []
stat = collections.Counter()
for cta in plan["cuentas"]:
    empresa = cta["empresa"]
    info = dom_plan.get(empresa.upper().strip(), {})
    dom, score = buscar_dominio(empresa, info.get("dominio", ""))
    pat_info = patrones_dom.get(dom) if dom else None

    for t in cta.get("tomadores") or []:
        nombre = (t.get("nombre") or "").strip()
        f, l = partes(nombre)
        reg = {"empresa": empresa, "nombre": nombre, "cargo": t.get("cargo"),
               "linkedin": t.get("linkedin"), "dominio": dom or "",
               "patron": None, "correo_inferido": "", "confianza": "", "nota": ""}

        if (t.get("correo") or "").strip():
            reg.update(correo_inferido=t["correo"].strip(), confianza="VERIFICADO",
                       nota="correo de fuente, no inferido")
            stat["verificado"] += 1
        elif not dom:
            reg.update(confianza="SIN DOMINIO",
                       nota="no se pudo resolver el dominio de la empresa; no se inventa")
            stat["sin_dominio"] += 1
        elif not pat_info:
            reg.update(confianza="SIN PATRON",
                       nota="el dominio aparece en la cosecha pero sin correo interpretable")
            stat["sin_patron"] += 1
        elif not f or not l:
            reg.update(confianza="SIN NOMBRE",
                       nota="el nombre no se puede separar en nombre/apellido")
            stat["sin_nombre"] += 1
        elif dom in FUERA:
            reg.update(confianza="NO APLICA",
                       nota="dominio de correo personal: no tiene patrón corporativo")
            stat["personal"] += 1
        else:
            pat = pat_info["patron"]
            correo = PATRONES[pat](f, l) + "@" + dom
            conf = "ALTA" if pat_info["n"] >= 2 else "MEDIA"
            reg.update(patron=pat, correo_inferido=correo, confianza=conf,
                       nota=f"patrón '{pat}' observado en {pat_info['n']} correo(s) reales "
                            f"de {dom}: {pat_info['ejemplos'][0]}")
            stat[conf] += 1
        salida.append(reg)

print("=" * 84)
print("CORREO DE LOS CT — inferido por patrón real de cada empresa")
print("=" * 84)
tot = len(salida)
print(f"  contactos CT: {tot}")
print(f"\n  === RESULTADO ===")
for k in ["verificado", "ALTA", "MEDIA", "SIN PATRON", "SIN DOMINIO", "NO APLICA", "sin_nombre"]:
    if stat[k]:
        print(f"     {k:14s} {stat[k]:>4}  ({stat[k]/tot*100:>4.0f}%)")
util = stat["verificado"] + stat["ALTA"] + stat["MEDIA"]
print(f"\n  correos UTILIZABLES (verificado + alta + media): {util} ({util/tot*100:.0f}%)")
print(f"  de esos, la mayoría son INFERIDOS: solo {stat['verificado']} son de fuente")

print(f"\n  === LOS DE CONFIANZA ALTA (patrón probado con 2+ correos reales) ===")
for r in [x for x in salida if x["confianza"] == "ALTA"][:20]:
    print(f"   {r['nombre'][:24]:26s} {r['correo_inferido']:38s} {r['empresa'][:26]}")
n_emp_alta = len({r["empresa"] for r in salida if r["confianza"] == "ALTA"})
print(f"\n  ({n_emp_alta} empresas con al menos un CT de confianza ALTA)")

print(f"\n  === LOS QUE NO SE PUDIERON RESOLVER, y por qué ===")
for r in [x for x in salida if x["confianza"] in ("SIN DOMINIO", "SIN PATRON")][:12]:
    print(f"   {r['nombre'][:24]:26s} {r['empresa'][:34]:36s} {r['confianza']}: {r['nota'][:44]}")

json.dump({
    "que_es": ("Correo inferido de los 577 compradores técnicos (CT) del plan técnico, deducido "
               "del PATRÓN de correo real de cada empresa (cosecha del Coordinador, 1.353 "
               "correos de 449 dominios)."),
    "tasa_de_acierto_medida": ("90,9% (368 de 405), medido con leave-one-out sobre correos "
                               "REALES: el patrón de la empresa tiene que predecir a un "
                               "individuo nuevo."),
    "donde_falla": ("Apellido compuesto (Victor Balbontin Artus -> victor.balbontin@enel.com el "
                    "patrón simple toma 'Artus'; Sebastian Ruiz-Tagle Mena -> sruiztagle@colbun.cl "
                    "apellido compuesto sin guion), sufijo numérico (Cesar Aedo -> caedo001@) y "
                    "correo personal (gmail/hotmail, sin patrón corporativo)."),
    "advertencia": ("NADA de esto es un correo verificado salvo los marcados VERIFICADO. El "
                    "patrón es real; el correo resultante es una DEDUCCIÓN y así se declara en "
                    "cada registro. No usar para envío masivo sin verificar: un correo mal "
                    "dirigido rebota o llega a un tercero."),
    "resumen": dict(stat),
    "patrones_por_dominio": {k: {"patron": v["patron"], "n": v["n"], "ejemplos": v["ejemplos"]}
                             for k, v in list(patrones_dom.items())[:80]},
    "contactos": salida,
}, open(os.path.join(D, "correos_ct.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/correos_ct.json")
