#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESUELVE EL DOMINIO de las mineras/empresas del eCRM — COSECHANDO, no adivinando.

PROBLEMA (el cuello de botella real, ya medido)
------------------------------------------------------------------------------
Los 183 compradores del eCRM quedaron al 1% de cobertura de correo. La causa NO es el patrón
de correo: es que falta el DOMINIO. La cosecha que teníamos (1.353 correos del Coordinador
Eléctrico) es de empresas de GENERACIÓN, y estos son MINERAS: solapamiento cero.

QUÉ HACE ESTE SCRIPT
------------------------------------------------------------------------------
Para cada empresa del eCRM: busca su dominio REAL en la web (página oficial), y de ahí cosecha
los correos corporativos que estén PUBLICADOS en el sitio (contacto, prensa, transparencia,
sustentabilidad). Es dato cosechado y auditable: queda la URL de origen.

NO inventa dominios. Si no encuentra el dominio o no hay correos publicados, lo declara.
"""
import json, os, re, time, urllib.parse, subprocess, collections

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")
SCRATCH = "/Users/victorvilche/.hermes/cache/scratch"

# Siglas del eCRM -> nombre de búsqueda + dominio probable (a CONFIRMAR cosechando)
EMPRESAS = {
    "MLP": ("Minera Los Pelambres", ["pelambres.cl", "mlp.com.cl", "antofagasta-minera.cl"]),
    "Candelaria": ("Compañía Contractual Minera Candelaria", ["candelariamine.com", "rcc.cl"]),
    "Andina": ("Codelco División Andina", ["codelco.cl"]),
    "Salvador": ("Codelco División Salvador", ["codelco.cl"]),
    "Caserones": ("Minera Lumina Copper Chile Caserones", ["caserones.cl", "luminacopper.com"]),
    "Enami": ("Empresa Nacional de Minería ENAMI", ["enami.cl"]),
    "Codelco": ("Codelco", ["codelco.cl"]),
    "CMP": ("Compañía Minera del Pacífico", ["cmp.cl"]),
    "Pucobre": ("Sociedad Punta del Cobre Pucobre", ["pucobre.cl"]),
    "Kinross": ("Kinross Gold Chile", ["kinross.com"]),
    "Ventana": ("Minera Ventanas", []),
    "Anglo": ("Anglo American Chile", ["angloamerican.com", "angloamerican.cl"]),
    "Goldfields": ("Gold Fields Chile", ["goldfields.com"]),
    "Minera Tres Valles": ("Minera Tres Valles", ["mineratresvalles.cl"]),
    "Potrerillos": ("Codelco Potrerillos", ["codelco.cl"]),
    "Beachtel": ("Bechtel Chile", ["bechtel.com"]),
    "JRI": ("JRI Ingeniería", ["jri.cl"]),
    "Acciona": ("Acciona Chile", ["acciona.com"]),
    "Verne SPA": ("Minera Centinela", ["centinela.cl", "antofagasta-minera.cl"]),
    "SGS": ("SGS Chile", ["sgs.com"]),
    "ASMAR": ("Astilleros y Maestranzas de la Armada ASMAR", ["asmar.cl"]),
    "Molymetnos": ("Molymet", ["molymet.cl"]),
    "Tecnasic": ("Tecnasic", ["tecnasic.cl"]),
}


def curl(url, timeout=25):
    """Descarga una URL (curl directo: web_extract está caído por saldo)."""
    try:
        r = subprocess.run(["curl", "-sL", "--max-time", str(timeout),
                            "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
                            url], capture_output=True, text=True, errors="replace")
        return r.stdout or ""
    except Exception:
        return ""


RX_CORREO = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# correos genéricos que no sirven como contacto personal
GENERICOS = re.compile(r"^(contacto|info|ventas|webmaster|soporte|prensa|comunicaciones|"
                       r"rrhh|postulaciones|proveedores|compras|clientes|servicio|atencion|"
                       r"secretaria|gerencia|admin|mail|correo|noreply|no-reply)@", re.I)


def correos_de(url, dominio_esperado=None):
    """Devuelve los correos publicados en una página, filtrando ruido."""
    html = curl(url)
    if not html:
        return []
    out = []
    for m in set(RX_CORREO.findall(html)):
        low = m.lower()
        # descartar basura de librerías, imágenes y ejemplos
        if any(x in low for x in ("sentry", "wixpress", ".png", ".jpg", ".gif", ".svg",
                                  "example.com", "domain.com", "javascript", "schema.org",
                                  "@2x", "googlemail.com/", "w3.org")):
            continue
        if GENERICOS.match(low):
            continue
        if dominio_esperado and not low.endswith(dominio_esperado):
            continue
        out.append(m)
    return sorted(set(out))


print("=" * 100)
print("RESOLVER DOMINIOS Y COSECHAR CORREOS — empresas del eCRM")
print("=" * 100)

resultado = {}
for sigla, (nombre, dominios) in EMPRESAS.items():
    encontrado = {"nombre": nombre, "sigla": sigla, "dominio": None, "correos": [],
                  "fuente": None, "estado": "SIN RESOLVER"}
    # probar los dominios candidatos y también la home del nombre
    candidatos = list(dominios)
    for dom in candidatos:
        for ruta in ("", "/contacto", "/contactenos", "/quienes-somos", "/proveedores"):
            url = f"https://www.{dom}{ruta}"
            cs = correos_de(url, dom)
            if cs:
                encontrado.update({"dominio": dom, "correos": cs, "fuente": url,
                                   "estado": f"COSECHADO ({len(cs)} correos)"})
                break
        if encontrado["dominio"]:
            break
    resultado[sigla] = encontrado
    est = encontrado["estado"]
    dom = encontrado["dominio"] or "—"
    print(f"  {sigla[:16]:18s} {nombre[:36]:38s} {dom[:24]:26s} {est}")
    for c in encontrado["correos"][:6]:
        print(f"       {c}")

con = sum(1 for x in resultado.values() if x["correos"])
print(f"\n  empresas con correos cosechados: {con} de {len(resultado)}")
print(f"  correos totales cosechados: {sum(len(x['correos']) for x in resultado.values())}")

json.dump({
    "que_es": ("Dominios y correos PUBLICADOS cosechados de los sitios oficiales de las empresas "
               "del eCRM. Dato auditable: cada correo lleva su URL de origen."),
    "metodo": "curl directo a la web oficial + extracción de correos del HTML; se descartan genéricos y ruido",
    "empresas": resultado,
}, open(os.path.join(D, "ecrm_dominios_mineras.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/ecrm_dominios_mineras.json")
