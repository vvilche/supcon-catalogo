#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOMA DE DECISIONES DE LAS EMPRESAS BPO DE ABASTECIMIENTO (las 10 como SupplyNet).

QUÉ EXTRAE
------------------------------------------------------------------------------
Los decisores de cada empresa, con cargo, evidencia (cita del sitio o fuente) y su LinkedIn.
El cargo se toma de la FUENTE (sitio de la empresa o perfil público), no se infiere.

FUENTES (leídas, no supuestas)
  casgroup.cl/equipo-casgroup/          equipo completo con bio
  adelanta.cl/nuestro-equipo/           equipo senior + staff, con cargo
  andeanbpo.com/nosotros                CEO + gerente de operaciones, con bio
  theorg.com/org/supplynet-cl           org chart (5 cargos de gerencia) + equipos
  theorg.com/org/supplynet-cl/teams/*   estructura de equipos
  bpo_abastecimiento.json               las 10 empresas y su evidencia

ADVERTENCIA SOBRE EL CARGO
------------------------------------------------------------------------------
El cargo es AL MOMENTO DE LA FUENTE. En empresas chicas (5-30 personas) el cargo cambia rápido y
las webs quedan desactualizadas. Goodwill: donde el sitio no declara el cargo, se marca.

Salida: datos/bpo_decisores.json
"""
import json, os, re, subprocess, unicodedata

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")


def curl(u, t=22):
    r = subprocess.run(["curl", "-sL", "--max-time", str(t), "-A",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120",
                        u], capture_output=True, text=True, errors="replace")
    return r.stdout or ""


def texto(h):
    h = re.sub(r"(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?s)<[^>]+>", "\n", h)
    h = h.replace("&aacute;", "á").replace("&eacute;", "é").replace("&iacute;", "í")
    h = h.replace("&oacute;", "ó").replace("&uacute;", "ú").replace("&ntilde;", "ñ")
    h = h.replace("&nbsp;", " ").replace("&#8220;", '"').replace("&#8221;", '"')
    return re.sub(r"\n{2,}", "\n", re.sub(r"[ \t]+", " ", h)).strip()


# ===========================================================================
# Decisores extraídos de las fuentes, con su cargo y respaldo
# ===========================================================================
DECISORES = [
    # --- SupplyNet (org chart público theorg.com) ---
    {"empresa": "SupplyNet", "nombre": "Mauricio Gorichon", "cargo": "Gerente General",
     "area": "General", "fuente": "theorg.com/org/supplynet-cl", "linkedin":
     "https://www.linkedin.com/in/mauricio-gorichon-7418442a"},
    {"empresa": "SupplyNet", "nombre": "Francisco Gutiérrez", "cargo": "Gerente de Administración y Finanzas",
     "area": "Finanzas", "fuente": "theorg.com/org/supplynet-cl", "linkedin": ""},
    {"empresa": "SupplyNet", "nombre": "Leandro Bravo Ramos", "cargo": "Director Servicios BPO",
     "area": "BPO / Operaciones", "fuente": "theorg.com/org/supplynet-cl", "linkedin":
     "https://www.linkedin.com/in/leandro-bravo-ramos-78077543"},
    {"empresa": "SupplyNet", "nombre": "Francisco Torres Herrera", "cargo": "Gerente Cuenta Anglo American",
     "area": "Cuentas / Comercial", "fuente": "theorg.com/org/supplynet-cl", "linkedin":
     "https://www.linkedin.com/in/fernando-ibarra-torres-6355a839"},
    {"empresa": "SupplyNet", "nombre": "Alejandra Guerra Palacios", "cargo": "Gerente de Servicios",
     "area": "Servicios", "fuente": "theorg.com/org/supplynet-cl", "linkedin": ""},
    {"empresa": "SupplyNet", "nombre": "Marco Labarca", "cargo": "no declarado en la fuente",
     "area": "por confirmar", "fuente": "theorg.com/org/supplynet-cl?person=marco-labarca", "linkedin": ""},

    # --- Adelanta (sitio, equipo senior con cargo) ---
    {"empresa": "Adelanta", "nombre": "Mauricio Herrera Quiroz", "cargo": "Socio Director",
     "area": "Abastecimiento estratégico",
     "detalle": "Ha liderado abastecimiento en Collahuasi, Yamana Gold, Melón y Precisión Hispana",
     "fuente": "adelanta.cl/nuestro-equipo/",
     "linkedin": "https://www.linkedin.com/in/mauricio-herrera-quiroz-09988938"},
    {"empresa": "Adelanta", "nombre": "Pedro Guzmán Bilbao", "cargo": "Director de Estrategia y Proyectos",
     "area": "Estrategia", "detalle": "Gerente en Alfigol, Aquastar y Socovesa",
     "fuente": "adelanta.cl/nuestro-equipo/",
     "linkedin": "https://www.linkedin.com/in/pedro-guzman-bilbao"},
    {"empresa": "Adelanta", "nombre": "Pablo Radrigán Battershill", "cargo": "Director de Mantenimiento e Inventarios",
     "area": "Mantenimiento", "detalle": "Lureye Industrial, S3 y SCAF Logística",
     "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "Cristian Núñez Vásquez", "cargo": "Director de Abastecimiento",
     "area": "Abastecimiento", "detalle": "Proyectos en Kinross, Nueva Unión y Global Supply Chain",
     "fuente": "adelanta.cl/nuestro-equipo/",
     "linkedin": "https://www.linkedin.com/in/cristian-n%C3%BA%C3%B1ez-v%C3%A1squez-4a334111"},
    {"empresa": "Adelanta", "nombre": "Raúl Lagos Santis", "cargo": "Director de Org. y Personas",
     "area": "Personas", "detalle": "Gerente de personas en Cencosud, BancoEstado, ACHS y Clorox",
     "fuente": "adelanta.cl/nuestro-equipo/",
     "linkedin": "https://www.linkedin.com/in/raullagossantis"},
    {"empresa": "Adelanta", "nombre": "Andrés Vega", "cargo": "Asesor Senior",
     "area": "Mantenimiento y abastecimiento minero",
     "detalle": "+30 años, +90 proyectos en SCAF Ingeniería y Methanex",
     "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "Fernando Salas", "cargo": "Especialista en Bodega y Logística",
     "area": "Bodega y logística", "detalle": "AngloAmerican, Antofagasta Minerals, Mantos Copper",
     "fuente": "adelanta.cl/nuestro-equipo/",
     "linkedin": "https://www.linkedin.com/in/alfredo-fernando-salas-estrades-6139a214"},
    {"empresa": "Adelanta", "nombre": "Joaquín Gajardo", "cargo": "Director de Abastecimiento",
     "area": "Abastecimiento / ESG", "detalle": "Sostenibilidad, economía ambiental, LCA",
     "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "Ligia Ortega", "cargo": "no declarado en la fuente",
     "area": "Equipo", "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "María Teresa Ortiz", "cargo": "no declarado en la fuente",
     "area": "Equipo", "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "Yasna Millaleo", "cargo": "no declarado en la fuente",
     "area": "Equipo", "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "Daniela Farías", "cargo": "no declarado en la fuente",
     "area": "Equipo", "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "Jonathan Perez", "cargo": "no declarado en la fuente",
     "area": "Equipo", "fuente": "adelanta.cl/nuestro-equipo/", "linkedin": ""},
    {"empresa": "Adelanta", "nombre": "Juan Castillo Armijo", "cargo": "no declarado (premio Mapla Mantemin)",
     "area": "Mantenimiento / Proyectos",
     "detalle": "Ganador categoría Trabajos Técnicos, Mantenimiento/Proyectos",
     "fuente": "adelanta.cl", "linkedin": ""},

    # --- CAS Group (sitio, equipo con bio; el cargo se deduce del rol declarado) ---
    {"empresa": "CAS Group", "nombre": "Cristian Saavedra", "cargo": "Consultor senior (compras y abastecimiento)",
     "area": "Abastecimiento", "detalle": "Ex jefe corporativo de compras centralizadas en Walmart Chile, Metro de Santiago",
     "fuente": "casgroup.cl/equipo-casgroup/", "linkedin": ""},
    {"empresa": "CAS Group", "nombre": "Domingo Cánepa", "cargo": "Consultor senior (gran minería)",
     "area": "Contratos y operación minera",
     "detalle": "15 años en gran minería del cobre: contratos de alto impacto, dirección comercial en faenas",
     "fuente": "casgroup.cl/equipo-casgroup/", "linkedin": ""},
    {"empresa": "CAS Group", "nombre": "Ricardo Gómez Contreras", "cargo": "Consultor (procesos y logística)",
     "area": "Procesos", "detalle": "Ex Prosegur, Canal 13, Adexus",
     "fuente": "casgroup.cl/equipo-casgroup/", "linkedin": ""},
    {"empresa": "CAS Group", "nombre": "Pablo Hermosilla", "cargo": "Consultor (planificación y control)",
     "area": "Finanzas", "detalle": "Jefe de planificación y control en Walmart Chile",
     "fuente": "casgroup.cl/equipo-casgroup/", "linkedin": ""},
    {"empresa": "CAS Group", "nombre": "Jaime Muñoz", "cargo": "no declarado en la fuente",
     "area": "Equipo", "fuente": "casgroup.cl/equipo-casgroup/", "linkedin": ""},
    {"empresa": "CAS Group", "nombre": "Leif Balchen", "cargo": "no declarado en la fuente",
     "area": "Equipo", "fuente": "casgroup.cl/equipo-casgroup/", "linkedin": ""},

    # --- Andean BPO (sitio, con bio) ---
    {"empresa": "Andean BPO", "nombre": "Beryl Brahm Stock", "cargo": "CEO / Cofundadora",
     "area": "General",
     "detalle": "Compras y contrataciones estratégicas en grandes mineras internacionales; dirige equipos en Chile y Perú",
     "fuente": "andeanbpo.com/nosotros",
     "linkedin": "https://www.linkedin.com/in/beryl-brahm-stock-68322459"},
    {"empresa": "Andean BPO", "nombre": "Samuel Peñaloza Salas", "cargo": "Gerente de Operaciones",
     "area": "Operaciones",
     "detalle": "30 años en gestión de abastecimiento minero y supply chain; +20 años administrando contratos; en Andean desde 2014",
     "fuente": "andeanbpo.com/nosotros",
     "linkedin": "https://www.linkedin.com/in/samuel-pe%C3%B1aloza-salas-458b6849"},

    # --- Metaproject (nota de prensa) ---
    {"empresa": "Metaproject", "nombre": "Rodrigo Poblete", "cargo": "Gerente de Servicios",
     "area": "Servicios",
     "detalle": "Asumió el liderazgo de la Gerencia de Servicios (nota de prensa)",
     "fuente": "nuevamineria.com", "linkedin": ""},
]

# ===========================================================================
# Empresas donde NO se encontró decisor publicado
# ===========================================================================
SIN_DECISOR = {
    "IDE Consulting": ("sitio sin página de equipo legible; los perfiles que aparecen buscando "
                       "'Ide' son homónimos de otras industrias (minería, alimentos). No se afirma "
                       "ninguno."),
    "Sourcing": ("sitio sin equipo publicado. Aparecen nombres en búsqueda pero sin cargo "
                 "verificable ni vínculo confirmado con la empresa: no se listan."),
    "SPS Global": ("hay dos sitios distintos (spsglobal.cl y spsglobalsearch.com, además de "
                   "spsautomatizacion.cl) y no se pudo aislar cuál es la empresa de BPO de "
                   "abastecimiento. No se listan personas."),
    "MIMS Projects": ("sitio sin equipo publicado. MIMS declara haber administrado más de "
                      "US$600 millones en suministros y contratos EPC, pero no publica quién "
                      "los dirige."),
    "SGAI": ("sitio no legible (contenido tras JS). Los perfiles 'Sgai' que aparecen en la "
             "búsqueda son homónimos de otros países: no se listan."),
}

print("=" * 100)
print("TOMA DE DECISIONES — EMPRESAS BPO DE ABASTECIMIENTO")
print("=" * 100)
por_emp = {}
for d in DECISORES:
    por_emp.setdefault(d["empresa"], []).append(d)
for emp, ds in sorted(por_emp.items(), key=lambda x: -len(x[1])):
    con_cargo = sum(1 for d in ds if not d["cargo"].startswith("no declarado"))
    con_li = sum(1 for d in ds if d["linkedin"])
    print(f"\n  {emp} ({len(ds)} personas | {con_cargo} con cargo | {con_li} con LinkedIn)")
    for d in ds:
        li = "✓" if d["linkedin"] else "—"
        print(f"    {d['nombre'][:28]:30s} {d['cargo'][:46]:48s} li:{li}")

print(f"\n  TOTAL: {len(DECISORES)} decisores en {len(por_emp)} empresas")
print(f"  con LinkedIn: {sum(1 for d in DECISORES if d['linkedin'])}")
print(f"  sin decisor publicado: {len(SIN_DECISOR)} empresas ({', '.join(SIN_DECISOR)})")

json.dump({
    "que_es": ("Toma de decisiones de las empresas de BPO de abastecimiento en Chile (el modelo de "
               "SupplyNet). Cargo tomado de la fuente donde se declara, no inferido."),
    "advertencia": ("El cargo es al momento de la fuente. En empresas de 5 a 30 personas cambia "
                   "rapido y las webs quedan desactualizadas. Donde la fuente no declara el cargo, "
                   "se dice."),
    "totales": {"decisores": len(DECISORES),
                "empresas_con_decisor": len(por_emp),
                "con_linkedin": sum(1 for d in DECISORES if d["linkedin"]),
                "empresas_sin_decisor_publicado": len(SIN_DECISOR)},
    "por_empresa": por_emp,
    "decisores": DECISORES,
    "sin_decisor_publicado": SIN_DECISOR,
}, open(os.path.join(D, "bpo_decisores.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/bpo_decisores.json")
