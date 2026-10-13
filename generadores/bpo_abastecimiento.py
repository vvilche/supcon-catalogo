#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BPO DE ABASTECIMIENTO EN CHILE: cuántas empresas como SupplyNet hay.

QUÉ ES EL MODELO (lo que hace SupplyNet)
------------------------------------------------------------------------------
BPO de abastecimiento: la minera (o forestal, utility, oil&gas) le ENTREGA su proceso de compras
a un tercero, que lo opera con su propio equipo, procesos y tecnología. No vende insumos: vende
la FUNCIÓN.

De la historia de SupplyNet (supplynet.cl/about/#historia, textual):
  "Supplynet Nace como un spin-off del negocio de Procurement Outsourcing (BPO) desarrollado por
   Quadrem y posteriormente SAP Ariba. Hereda alrededor de 7 años de experiencia del área de
   Servicios de Abastecimiento y gran parte del equipo de Profesionales."

Quadrem fue el marketplace de abastecimiento minero de SAP (Chile fue su mercado piloto), y Ariba
es la plataforma que hoy opera. De esa estirpe salen varios jugadores locales.

El servicio que presta a su cliente minero (textual, caso de éxito) incluye: Gerencia Corporativa
y cada faena, con Compras, Licitaciones, Backoffice, Administración de contratos, Sustentabilidad,
Proveedores Regionales, Soporte plataforma Ariba, Reportabilidad y Control de gestión.

POR QUÉ IMPORTA PARA CONECTA
------------------------------------------------------------------------------
Estos son INTERMEDIARIOS en la compra: ellos corren la licitación y el contrato. El que vende al
área de abastecimiento de la minera pasa por ellos. Son a la vez CANAL (pueden incluir el producto
en las bases técnicas de sus licitaciones) y COMPETIDOR por el presupuesto de "gestión".

Output: datos/bpo_abastecimiento.json
"""
import json, os, re, subprocess, collections

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
D = os.path.join(BASE, "datos")


def curl(u, t=18):
    r = subprocess.run(["curl", "-sL", "--max-time", str(t), "-A",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120",
                        u], capture_output=True, text=True, errors="replace")
    return r.stdout or ""


def texto(h):
    h = re.sub(r"(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h).strip()


# Cada empresa con la evidencia de que es del mismo modelo (BPO de abastecimiento).
EMPRESAS = {
    "SupplyNet": {"web": "supplynet.cl", "origen": "spin-off de Quadrem y SAP Ariba",
                  "industrias": "Minería, Oil&Gas, Forestal, Utilities, Ingeniería",
                  "cliente": "Grupo minero (Gerencia Corporativa + faenas) e importante empresa minera global",
                  "cert": "ISO 27001",
                  "evidencia": "BPO, Servicios Profesionales, Consultoría, Capacitación, Soluciones Digitales"},
    "Andean BPO": {"web": "andeanbpo.com", "origen": "no declarado",
                   "industrias": "Minería (Chile y Latinoamérica)",
                   "cliente": "diversas compañías en Chile y Latinoamérica",
                   "cert": "",
                   "evidencia": "5/6 rasgos: BPO + abastecimiento + minería + contratos + licitación. "
                                "Metodología propia OPTiMO para mantenimiento minero"},
    "CAS Group Consulting": {"web": "casgroup.cl", "origen": "no declarado",
                             "industrias": "Minería e industria",
                             "cliente": "no declarado",
                             "cert": "",
                             "evidencia": "5/6 rasgos. BPO Gestión de Licitaciones: spend analysis, "
                                          "bases técnicas, RFP, análisis de ofertas, adjudicación"},
    "Adelanta": {"web": "adelanta.cl", "origen": "no declarado",
                 "industrias": "Minería e industria",
                 "cliente": "proyectos mineros",
                 "cert": "ISO 9001:2015",
                 "evidencia": "5/6 rasgos: outsourcing + abastecimiento + minería + contratos + licitación"},
    "Sourcing": {"web": "sourcing.cl", "origen": "no declarado",
                 "industrias": "Minería e industria",
                 "cliente": "no declarado", "cert": "",
                 "evidencia": "3/6 rasgos: administración de contratos, abastecimiento de servicios "
                              "y proyectos, gestión de claims"},
    "IDE Consulting": {"web": "ideconsulting.cl", "origen": "no declarado",
                       "industrias": "Minería e industria",
                       "cliente": "no declarado", "cert": "",
                       "evidencia": "3/6: consultoría estratégica en abastecimiento, gestión de "
                                    "licitaciones, administración de operaciones logísticas (+15 años)"},
    "SPS Global": {"web": "spsglobal.cl", "origen": "no declarado",
                   "industrias": "Minería e industria", "cliente": "no declarado", "cert": "",
                   "evidencia": "servicio de gestión de compras"},
    "Metaproject": {"web": "metaprojectgroup.com", "origen": "no declarado",
                    "industrias": "Minería",
                    "cliente": "CODELCO (renovó por 5 años su servicio de abastecimiento)",
                    "cert": "",
                    "evidencia": "servicios de abastecimiento y logística (supply chain); contrato real con Codelco"},
    "MIMS Projects": {"web": "mimsprojects.com", "origen": "no declarado",
                      "industrias": "Minería e industria", "cliente": "no declarado", "cert": "",
                      "evidencia": "gestión y automatización de proyectos"},
    "SGAI": {"web": "sgai.cl", "origen": "no declarado",
             "industrias": "Minería e industria", "cliente": "no declarado", "cert": "",
             "evidencia": "BPO + plataforma de procurement con IA; sitio no respondió a la lectura "
                          "(contenido tras JS) — declarado como tal"},
}

# del mismo rubro pero NO del modelo BPO (venden insumos, no la función)
NO_ES_BPO = {
    "Miningtec SpA": "vende suministros, repuestos, equipos e importaciones: es proveedor, no BPO",
    "ManpowerGroup (outsourcing minero)": "outsourcing de PERSONAL, no del proceso de compras",
    "24-7 Ingeniería": "ingeniería y consultoría, no opera el proceso de compras",
    "Escribano y Cía": "consultoría legal/contractual, no BPO",
    "Salas ING": "servicios para minería (operacionales), no compras",
    "Direcmin / Observatorio Minero / SupplierNet": "DIRECTORIOS de proveedores, no BPO",
}

print("=" * 100)
print("BPO DE ABASTECIMIENTO EN CHILE — empresas del mismo modelo que SupplyNet")
print("=" * 100)
print(f"  empresas del modelo BPO de abastecimiento: {len(EMPRESAS)}")
for k, v in EMPRESAS.items():
    print(f"    {k:24s} {v['web']:22s} {v['evidencia'][:60]}")
print(f"\n  del rubro pero NO BPO (excluidas): {len(NO_ES_BPO)}")
for k, v in NO_ES_BPO.items():
    print(f"    {k[:38]:40s} {v[:56]}")

# cruce: ¿aparecen estas empresas en el eCRM de INECO? (con el NOMBRE COMPLETO, no substring)
e = json.load(open(os.path.join(D, "ecrm_extraido.json"), encoding="utf-8"))
opp = e["oportunidades"]
blob = " ".join(f"{r.get('cliente','')} {r.get('descripcion','')} {r.get('contacto','')}"
                for r in opp).lower()
print("\n=== ¿aparecen en el eCRM de INECO (2023-2025)? (nombre completo, no substring) ===")
cruce = {}
for k, v in EMPRESAS.items():
    # buscar el nombre de la empresa como frase, no un fragmento
    n = 0
    for forma in (k.lower(), k.split()[0].lower() + " bpo", v["web"].split(".")[0].lower()):
        if len(forma) >= 6 and forma in blob:
            n += blob.count(forma)
    cruce[k] = n
    print(f"    {k:24s} {n} menciones")

json.dump({
    "que_es": ("Empresas que hacen BPO de abastecimiento en Chile: le operan el proceso de compras "
               "a la minera con equipo y procesos propios. SupplyNet es una de ellas (spin-off de "
               "Quadrem / SAP Ariba)."),
    "modelo": ("BPO de abastecimiento = la empresa entrega su FUNCIÓN de compras a un tercero. "
               "No venden insumos: venden el proceso (compras, licitaciones, contratos, backoffice)."),
    "por_que_importa": ("Son intermediarios: corren la licitación y el contrato de la minera. Son "
                        "CANAL (pueden incluir el producto en las bases técnicas) y a la vez "
                        "COMPETIDOR por el presupuesto de gestión."),
    "cuantas": len(EMPRESAS),
    "empresas": EMPRESAS,
    "no_es_bpo": NO_ES_BPO,
    "en_ecrm": cruce,
}, open(os.path.join(D, "bpo_abastecimiento.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/bpo_abastecimiento.json")
