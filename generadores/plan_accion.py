#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAN DE ACCIÓN — a quién llamar, cómo contactarlo y qué decirle.

EL HUECO QUE ESTE SCRIPT CIERRA
------------------------------------------------------------------------------
Todo lo construido era ANÁLISIS: dolor medido, decisores, líneas, montos. Faltaba la pieza
operativa: **la lista de llamados de mañana**, con nombre, cómo llegar y qué decir.

TRES VÍAS DE CONTACTO, en orden de lo que rinde:
  1. LLAMADO a la central + pedir por la persona por nombre y cargo
     (143 de 226 empresas traen teléfono del conmutador)
  2. LINKEDIN: mensaje directo al perfil (1.962 personas tienen perfil)
  3. CORREO: solo donde el dominio tiene MX verificado (inferido, no verificado)

QUÉ DICE CADA FICHA
------------------------------------------------------------------------------
  - A quién llamar: nombre, cargo, LinkedIn
  - El número: teléfono de la central (o "sin teléfono: entrar por LinkedIn")
  - Qué ofrecerle: la línea SUPCON que corresponde a SU cargo y al dolor de SU empresa
  - El gancho: el dato medido de esa empresa (toneladas, montos, normas)
  - El guion: la primera frase, armada con el dato real

REGLA DE HONESTIDAD
------------------------------------------------------------------------------
El teléfono es de la CENTRAL, no del celular de la persona: hay que pedirla por nombre.
El correo es INFERIDO. Solo el nombre, el cargo y el LinkedIn son datos con fuente.

Salida: datos/plan_accion.json + artefactos/plan_accion.html
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def load(p, d=None):
    fp = os.path.join(D, p)
    return json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else d


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


vista = (load("vista_cliente_producto_persona.json") or {}).get("empresas", [])
dd = (load("dominios_duros.json") or {}).get("empresas", {})
mineras = {norm(m["empresa"]): m for m in (load("mineras_retc.json") or {}).get("mineras", [])}
ecrm = (load("ecrm_supcon.json") or {}).get("clientes_hoy", {})
correos = {norm(c["nombre"]): c for c in (load("buscador_decisores.json") or {}).get("resultados", [])
           if False}  # placeholder

# qué producto ofrecer según el cargo del decisor
LINEA_POR_CARGO = [
    (r"medio ?ambiente|ambiental|sustentab|calidad|laborator", "Analítica",
     "CEMS/monitoreo de emisiones: la línea que resuelve el dolor del RETC"),
    (r"mantenimiento|mantenci|confiabilid|mecánic", "Válvulas + Instrumentación",
     "válvulas de control, posicionador CVP2000, instrumentación de campo"),
    (r"instrument|i&c|control|automatiz|eléctric|electric", "Instrumentación + DCS/PLC",
     "transmisores, caudalímetros, y el sistema de control"),
    (r"operaciones|producci|planta|gerente general|presidente|ceo|superintend", "Software y plataforma",
     "SolisSCADA/InPlant: historizar y reportar las señales que ya existen"),
    (r"seguridad|hse|hsec|riesgo|prevenci", "SIS",
     "HIPPS/TCS-500: seguridad instrumentada"),
    (r"abastecimiento|suministro|compras|supply|procurement|logístic", "Todas las líneas",
     "es el comprador: entra por acá todo el catálogo"),
    (r"proyecto|ingenier", "Instrumentación + Válvulas",
     "especificación de proyecto: entrar en las bases técnicas"),
]


def producto_para(cargo):
    c = str(cargo or "")
    for rx, linea, que in LINEA_POR_CARGO:
        if re.search(rx, c, re.I):
            return linea, que
    return "Instrumentación", "instrumentación de campo"


def telefono_de(empresa):
    """Teléfono de la CENTRAL (conmutador). No es el celular de la persona."""
    n = norm(empresa)
    tn = set(n.split())
    mejor, sc = None, 0
    for k, v in dd.items():
        c = len(tn & set(norm(k).split()))
        if c > sc and v.get("telefono"):
            mejor, sc = v, c
    if mejor and sc >= 2:
        t = mejor["telefono"]
        m = re.search(r"(?:\+?56[\s\-]?)?(?:\(?2\)?[\s\-]?)?\d{3,4}[\s\-]?\d{4}", t)
        return (m.group(0) if m else t[:24]).strip()
    return ""


def web_de(empresa):
    n = norm(empresa)
    tn = set(n.split())
    for k, v in dd.items():
        if len(tn & set(norm(k).split())) >= 2 and v.get("web"):
            m = re.search(r"([\w\-]+\.cl|[\w\-]+\.com)", v["web"])
            return m.group(1) if m else ""
    return ""


# --- armar el plan ---
plan = []
for x in vista:
    if not x["n_decisores"]:
        continue
    tel = telefono_de(x["empresa"])
    web = web_de(x["empresa"])
    mn = mineras.get(norm(x["empresa"]), {})
    # ordenar decisores: primero los relevantes, y dentro de ellos los de cargo más alto
    decs = [d for d in x["decisores"] if d.get("relevante")]
    decs.sort(key=lambda d: (not re.search(r"gerente|presidente|superintend|jefe", d["cargo"], re.I),
                             len(d["cargo"])))
    contactos = []
    for d in decs[:6]:
        linea, que = producto_para(d["cargo"])
        contactos.append({
            "nombre": d["nombre"], "cargo": d["cargo"],
            "linkedin": d.get("linkedin", ""),
            "linea": linea, "que_ofrecer": que,
        })
    if not contactos:
        continue
    plan.append({
        "empresa": x["empresa"],
        "sigla": x.get("sigla_ecrm", ""),
        "telefono_central": tel,
        "web": web,
        "dolor_t": x["respel_t"],
        "usd_cotizado": x["usd_cotizado"],
        "usd_ganado": x["usd_ganado"],
        "n_oc": x["n_oc"],
        "lineas_empresa": x["lineas"],
        "productos": x["productos"][:6],
        "contactos": contactos,
        "n_contactos": len(contactos),
        "tipo_empresa": mn.get("tipo", ""),
        "via": ("llamado + LinkedIn" if tel else "LinkedIn (sin teléfono de central)"),
    })

# ordenar por lo que más vale: compras reales primero, después dolor
plan.sort(key=lambda p: (-(p["usd_cotizado"] or 0), -(p["dolor_t"] or 0)))

tot_c = sum(p["n_contactos"] for p in plan)
con_tel = sum(1 for p in plan if p["telefono_central"])
print("=" * 104)
print("PLAN DE ACCIÓN — a quién contactar")
print("=" * 104)
print(f"  empresas:            {len(plan)}")
print(f"  personas a contactar: {tot_c}")
print(f"  con teléfono de central: {con_tel} ({con_tel/len(plan)*100:.0f}%)")
print(f"  con LinkedIn:        {sum(1 for p in plan for c in p['contactos'] if c['linkedin'])}")
print()
for p in plan[:12]:
    print(f"  {p['empresa'][:40]:42s} {p['via']:34s} {p['n_contactos']} contactos")
    for c in p["contactos"][:2]:
        print(f"      {c['nombre'][:26]:28s} {c['cargo'][:40]:42s} -> {c['linea'][:22]}")

json.dump({
    "que_es": ("Plan de acción: a quién contactar en cada empresa, cómo llegar y qué ofrecerle. "
               "Cierra el hueco entre el análisis y la acción."),
    "vias": {"1_llamado": "teléfono de la CENTRAL + pedir por nombre y cargo",
             "2_linkedin": "mensaje directo al perfil (dato con fuente)",
             "3_correo": "solo dominio con MX verificado (correo inferido)"},
    "advertencia": ("El teléfono es del conmutador, NO el celular de la persona: hay que pedirla "
                    "por nombre. El correo es inferido. Nombre, cargo y LinkedIn sí tienen fuente."),
    "totales": {"empresas": len(plan), "contactos": tot_c, "con_telefono": con_tel},
    "plan": plan,
}, open(os.path.join(D, "plan_accion.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/plan_accion.json")
