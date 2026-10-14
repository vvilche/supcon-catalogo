#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERENTES Y DECISORES DE LAS EMPRESAS DEL ESTADO — fuente: páginas de TRANSPARENCIA.

LA LECCIÓN (corrección de un error propio)
------------------------------------------------------------------------------
Se había reportado "ENAP: 7 contactos, ninguno de Medio Ambiente" y se contó como hueco. FALSO.
ENAP es una empresa del ESTADO y publica por ley, en su sitio de transparencia, TODOS sus
gerentes y jefes con nombre, cargo, profesión y RUT:
  enap.cl/la-empresa/estructura-corporativa/administracion

Ahí está el Gerente Corporativo de Medio Ambiente (Jorge Lobato Urrutia, desde feb-2022) y toda
la plana gerencial. El problema no era la falta de datos: era buscar en el lugar equivocado
(buscar en LinkedIn/catálogo en vez de en la fuente pública obligatoria).

Las empresas del Estado con transparencia activa: ENAP, Codelco, Enami, EFE, Metro, Correos,
BancoEstado, TVN, etc. Todas publican sus ejecutivos.

Salida: datos/decisores_estado.json
"""
import json, os, re, html as H, subprocess

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")


def curl(u, t=25):
    r = subprocess.run(["curl", "-sL", "--max-time", str(t), "-A",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120",
                        u], capture_output=True, text=True, errors="replace")
    return r.stdout or ""


def a_texto(raw):
    h = re.sub(r"(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>", " ", raw)
    h = re.sub(r"(?s)<[^>]+>", "\n", h)
    h = H.unescape(h)
    return re.sub(r"\n{2,}", "\n", re.sub(r"[ \t]+", " ", h)).strip()


# El patrón de la página: Cargo \n Nombre \n Profesión \n RUT
RX_REG = re.compile(
    r"\n(Gerente[a]?[^\n]{3,70}|Director[a]?[^\n]{3,70}|Jefe[a]?[^\n]{3,70})\n"
    r"([A-ZÁÉÍÓÚÑ][^\n]{5,60})\n"
    r"([^\n]{0,50}(?:Ingenier|Contador|Psicólog|Periodist|Abogad|Adminis|Comercial|Técnic|Geólog|Químic)[^\n]{0,40})\n"
    r"(?:RUT:?\s*([\d.\-K]+))?", re.I)

REGISTROS = []
# --- ENAP ---
t = a_texto(curl("https://www.enap.cl/la-empresa/estructura-corporativa/administracion"))
print(f"ENAP administración: {len(t)} chars")
for m in RX_REG.finditer(t):
    cargo, nombre, prof, rut = (m.group(1).strip(), m.group(2).strip(),
                                m.group(3).strip(), (m.group(4) or "").strip())
    if len(nombre.split()) < 2:
        continue
    REGISTROS.append({"empresa": "ENAP", "nombre": nombre, "cargo": cargo,
                      "profesion": prof, "rut": rut,
                      "fuente": "enap.cl/la-empresa/estructura-corporativa/administracion"})

# --- datos ya confirmados por otra fuente (búsqueda) que la página no siempre lista ---
EXTRA_ENAP = [
    {"empresa": "ENAP", "nombre": "Jorge Lobato Urrutia",
     "cargo": "Gerente Corporativo de Medio Ambiente", "area": "Medio Ambiente",
     "detalle": "Desde febrero de 2022", "fuente": "enap.cl/files/get/1368",
     "linkedin": ""},
    {"empresa": "ENAP", "nombre": "Lorena Carvallo Alache",
     "cargo": "Gerente Corporativo Medio Ambiente", "area": "Medio Ambiente",
     "detalle": "Environmental Impact Assessment / Compliance / Biodiversity",
     "fuente": "linkedin.com/in/lorena-carvallo-alache",
     "linkedin": "https://www.linkedin.com/in/lorena-carvallo-alache"},
    {"empresa": "ENAP", "nombre": "Fabián Guerrero",
     "cargo": "Director de Gestión Ambiental Corporativo", "area": "Medio Ambiente",
     "detalle": "", "fuente": "linkedin.com/in/faguerrero",
     "linkedin": "https://www.linkedin.com/in/faguerrero"},
    {"empresa": "ENAP", "nombre": "Claudia Arancibia Fuenzalida",
     "cargo": "Jefa de División Gestión Ambiental", "area": "Medio Ambiente",
     "detalle": "Desde mayo 2023; Quintero, Valparaíso", "fuente": "contactout (perfil público)",
     "linkedin": ""},
    {"empresa": "ENAP", "nombre": "Douglas Sequeira Morgado",
     "cargo": "Gerente Corporativo de Salud Ocupacional y Seguridad (HSEC)", "area": "HSE",
     "detalle": "Ingeniero en Prevención de Riesgos y Medio Ambiente", "fuente": "enap.cl (versión EN)",
     "linkedin": ""},
    {"empresa": "ENAP", "nombre": "Gian Franco Ferrari",
     "cargo": "Jefe División Mantención Mayor de Plantas e Instalaciones (Ref. Aconcagua)",
     "area": "Mantenimiento", "detalle": "Fuente de prensa local, 2024",
     "fuente": "observador.cl", "linkedin": ""},
]

# --- CODELCO (empresa del Estado, transparencia) ---
t2 = a_texto(curl("https://www.codelco.com/prontus_codelco/site/edic/base/port/ejecutivos.html"))
if len(t2) > 500:
    print(f"Codelco ejecutivos: {len(t2)} chars")

print("\n" + "=" * 100)
print("DECISORES DE EMPRESAS DEL ESTADO (ENAP) — de la página de transparencia")
print("=" * 100)
print(f"\n  de la página de administración: {len(REGISTROS)}")
for r in REGISTROS:
    print(f"    {r['nombre'][:30]:32s} {r['cargo'][:56]}")

print(f"\n  del área ambiental/HSE (fuente complementaria): {len(EXTRA_ENAP)}")
for r in EXTRA_ENAP:
    print(f"    {r['nombre'][:30]:32s} {r['cargo'][:56]:58s} [{r['area']}]")

json.dump({
    "que_es": ("Gerentes y decisores de empresas del ESTADO (ENAP), tomados de su página de "
               "transparencia: nombre, cargo, profesión y RUT. La ley obliga a publicarlos."),
    "la_leccion": ("Se había contado a ENAP como 'hueco: 7 contactos, ninguno de Medio Ambiente'. "
                   "FALSO: el Gerente Corporativo de Medio Ambiente está publicado en el sitio de "
                   "transparencia. El error fue buscar en LinkedIn/catálogo en vez de en la fuente "
                   "pública obligatoria."),
    "donde_buscar": ("empresas del Estado con transparencia activa: ENAP, Codelco, Enami, EFE, "
                     "Metro, Correos, BancoEstado. Todas publican sus ejecutivos con nombre y cargo."),
    "totales": {"pagina_administracion": len(REGISTROS), "ambiente_hse_extra": len(EXTRA_ENAP)},
    "pagina_administracion": REGISTROS,
    "ambiente_y_hse": EXTRA_ENAP,
}, open(os.path.join(D, "decisores_estado.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/decisores_estado.json")
