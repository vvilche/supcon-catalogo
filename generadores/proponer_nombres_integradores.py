#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROPUESTA DE NOMBRE CANDIDATO por integrador — capa de INFERENCIA sobre
datos/perfilado_74_integradores.json.

ADVERTENCIA METODOLÓGICA (leer antes de usar):
El registro DIN de Aduanas NO trae nombre ni RUT del importador (Ley 20.285).
Todo nombre aquí es una HIPÓTESIS construida cruzando la EVIDENCIA MEDIDA del
propio importador (marca dominante, familia de producto, comuna, nº de marcas,
regularidad) con el conocimiento del mercado chileno de instrumentación:
qué empresas actúan como representantes/distribuidores de cada marca en Chile.

No es identificación: es inferencia. El nivel de confianza dice cuán fuerte es
el respaldo:
  - ALTA   : 1 sola marca en el rubro, o marca dominante >70%, y su representante
             chileno es de conocimiento público/directo -> la evidencia apunta a
             una empresa concreta.
  - MEDIA  : marca dominante clara pero con 2-3 representantes posibles en Chile,
             o perfil de integrador multirubro -> nombre probable, no exclusivo.
  - BAJA   : muchas marcas, ninguna dominante, perfil genérico -> sólo se puede
             acotar el TIPO de empresa (representante de X, distribuidor de proceso,
             integrador eléctrico), sin nombre fiable.

El nombre propuesto se acompaña SIEMPRE de:
  - evidencia (los números medidos que lo sustentan)
  - alternativas (otras empresas chilenas compatibles con la misma evidencia)
  - como_confirmar (el paso concreto para verificar/descartar la hipótesis)

Salida: reescribe datos/perfilado_74_integradores.json agregando, a cada perfil,
el campo "nombre_candidato".
"""
import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
PATH = os.path.join(D, "perfilado_74_integradores.json")

d = json.load(open(PATH, encoding="utf-8"))
perfiles = d["perfiles"]


def marca_ppal(p):
    return p["marcas_top10"][0]["marca"] if p["marcas_top10"] else ""


def marca_ppal_pct(p):
    return p["marcas_top10"][0]["pct_del_rubro"] if p["marcas_top10"] else 0.0


# --- reglas de inferencia ---
# Cada regla: (fn que matchea el perfil, dict con el candidato).
# El orden importa: la primera regla que matchea gana (de la más específica a la más genérica).

def reglas():
    R = []

    # --- representantes/distribuidores conocidos por MARCA dominante y comuna ---
    # El "gancho" es: una sola marca -> probable filial o representante exclusivo.

    def add(cond, nombre, conf, ev, alts, confirmar):
        R.append((cond, dict(nombre=nombre, confianza=conf, evidencia=ev,
                             alternativas=alts, como_confirmar=confirmar)))

    # Siemens (control/DCS/PLC) — varias empresas chilenas representan Siemens
    add(lambda p: p["share_pct"] >= 50 and marca_ppal(p) == "SIEMENS" and p["n_marcas_rubro"] == 1,
        "Representante / distribuidor Siemens para automatización (posible filial Siemens Chile o distribuidor autorizado de tableros y PLC)",
        "MEDIA",
        "una sola marca en el rubro (Siemens), share {s}%, {f} como familia principal, {c}",
        "Siemens Chile (filial directa); distribuidores autorizados de Siemens para tableros/PLM (p.ej. empresas de tableros eléctricos de Las Condes)",
        "cruzar el ID {id} con el registro de importadores por partida 8537/8538; pedir a un proveedor Siemens Chile su lista de importadores autorizados; o googlear 'importador tableros Siemens Chile Las Condes'")

    add(lambda p: marca_ppal(p) == "SIEMENS",
        "Distribuidor multirrubro de tecnología con línea Siemens (integrador eléctrico/automatización)",
        "BAJA",
        "principal marca Siemens pero share {s}% y {n} marcas en el rubro -> no es representante exclusivo",
        "cualquier integrador eléctrico chileno con cartera Siemens (Sistemas Expertos, Icom, Cidiel, etc.)",
        "sin marca exclusiva no hay identificacion fiable; usar el perfil de conducta para el abordaje, no el nombre")

    # ABB
    add(lambda p: marca_ppal(p) == "ABB" and marca_ppal_pct(p) >= 60,
        "Representante / mayorista ABB en Chile (automatización, variadores, tableros)",
        "MEDIA",
        "principal marca ABB con {mp}% de su rubro, share {s}%, {c}",
        "ABB Chile (filial); distribuidores mayoristas de ABB en Chile",
        "cotejar partidas 8504/8537 con la lista pública de distribuidores ABB Chile")

    add(lambda p: marca_ppal(p) == "ABB",
        "Integrador que importa ABB junto a otras marcas (automatización + potencia)",
        "BAJA",
        "principal marca ABB pero comparte con {n} marcas en el rubro",
        "integrador eléctrico chileno genérico",
        "no fiable por nombre; usar conducta")

    # Endress+Hauser -> representantes chilenos conocidos
    add(lambda p: marca_ppal(p) == "ENDRESS" and marca_ppal_pct(p) >= 75,
        "Representante / distribuidor Endress+Hauser en Chile",
        "MEDIA",
        "principal marca Endress con {mp}% de su rubro, share {s}%, {c} (perfil de instrumentación de proceso)",
        "Grupo Ferrostaal Chile; Soltex; representantes Endress+Hauser con domicilio en Lo Prado/Las Condes",
        "Endress+Hauser Chile publica su canal; comparar el ticket y las partidas 9026/9025 con el catálogo del representante")

    add(lambda p: marca_ppal(p) == "ENDRESS",
        "Distribuidor de instrumentación de proceso con línea Endress+Hauser",
        "MEDIA",
        "principal marca Endress, share {s}%, {n} marcas en el rubro, {f}",
        "representantes Endress+Hauser de tamaño medio en Chile",
        "confirmar por partida 9026 y comuna de despacho")

    # KROHNE / CIDRA (medición de flujo, minería)
    add(lambda p: marca_ppal(p) in ("KROHNE", "CIDRA"),
        "Representante / distribuidor de medición de flujo (KROHNE / CIDRA) para minería y proceso",
        "MEDIA",
        "principal marca {m} en el rubro, share {s}%, {c}",
        "distribuidores chilenos de KROHNE; representantes de CIDRA (medición de pulpas, minería)",
        "cruzar con proyecto mineros (CIDRA = flujo en minería); confirmar representacion por partida 9026")

    # Rockwell / Allen-Bradley
    add(lambda p: marca_ppal(p) in ("ROCKWELL", "ALLEN"),
        "Distribuidor de automatización con línea Rockwell/Allen-Bradley (PLC)",
        "MEDIA",
        "principal marca {m} (Allen-Bradley es de Rockwell), share {s}%, {f} como familia dominante",
        "representantes chilenos de Rockwell Automation (Allen-Bradley se vende por distribuidor autorizado)",
        "Rockwell Automation Chile tiene canal de distribuidores autorizados; cotejar partida 8537 con ese canal")

    # Emerson / Rosemount / Micro Motion / Fisher / Flexim
    add(lambda p: marca_ppal(p) in ("EMERSON", "ROSEMOUNT", "MICRO MOTION", "FISHER", "FLEXIM"),
        "Representante / distribuidor de instrumentación Emerson (Rosemount, Micro Motion, Fisher, Flexim)",
        "MEDIA",
        "principal marca {m} del ecosistema Emerson, share {s}%, {c}",
        "representantes chilenos del grupo Emerson (Rosemount/Micro Motion/Fisher) y de Flexim",
        "el grupo Emerson tiene canal chileno identificable; confirmar por partida 9026/9025/8481")

    # Valmet / Neles / Metso — válvulas y control para minería/celulosa
    add(lambda p: marca_ppal(p) in ("VALMET", "NELES", "METSO"),
        "Representante / distribuidor de válvulas y control de proceso (Valmet/Neles/Metso)",
        "MEDIA",
        "principal marca {m}, share {s}%, familia {f} (válvulas y control, proceso continuo)",
        "representantes chilenos de Valmet/Neles y Metso, fuertemente ligados a celulosa y minería",
        "cotejar partida 8481 y 8481 con el canal chileno de Valmet/Neles/Metso")

    # Bray / Valvitalia / AUMA / rotork -> válvulas y actuadores
    add(lambda p: marca_ppal(p) in ("BRAY", "VALVITALIA", "AUMA", "ROTORK"),
        "Representante / distribuidor de válvulas y actuadores industriales ({m})",
        "MEDIA",
        "principal marca {m}, share {s}%, familia {f}",
        "distribuidores chilenos de válvulas/actuadores industriales",
        "confirmar por partida 8481 para válvulas")

    # Danfoss / Vacon / Innomotics -> accionamientos y potencia
    add(lambda p: marca_ppal(p) in ("DANFOSS", "VACON"),
        "Distribuidor de accionamientos y potencia (Danfoss / Vacon) para electromecánica",
        "MEDIA",
        "principal marca {m}, share {s}%, familia {f}",
        "representantes chilenos de Danfoss Drives / Vacon (hoy parte de Danfoss)",
        "cotejar partida 8504 (convertidores) con el canal Danfoss Chile")

    add(lambda p: marca_ppal(p) == "INNOMOTICS",
        "Representante / canal de Innomotics (ex Siemens Large Drives) en Chile",
        "MEDIA",
        "principal marca Innomotics (spin-off de Siemens de motorización y accionamientos), share {s}%, {c}",
        "Innomotics Chile (ex Siemens Large Drives)",
        "Innomotics es marca reciente y con canal corto: el importador = casi siempre el canal del propio grupo")

    # Medición eléctrica / protecciones: SEL, Doble, Omicron, Megger, Arteche, Fluke, Alstom, Hyosung
    add(lambda p: marca_ppal(p) in ("SEL", "DOBLE", "OMICRON", "MEGGER", "FLUKE", "ARTECHE", "ALSTOM", "HYOSUNG"),
        "Representante / distribuidor de medición eléctrica, protecciones y equipos de prueba ({m})",
        "MEDIA",
        "principal marca {m}, share {s}%, familia {f}, {c}",
        "representantes chilenos de protecciones y equipos de prueba (SEL para relés; Doble/OMICRON/Megger para pruebas de campo)",
        "cotejar partida 9030/9028 con el canal chileno de cada marca; las marcas de prueba (Doble/OMICRON/Megger) las importan empresas de servicios eléctricos")

    # Hinch/analizadores de laboratorio: Thermo, Waters, Hach, Analytik, Leco, Teledyne, Bruker, Shimadzu
    add(lambda p: marca_ppal(p) in ("THERMO", "WATERS", "HACH", "ANALYTIK", "LECO", "TELEDYNE", "BRUKER", "SHIMADZU", "AGILENT", "PERKIN"),
        "Representante / distribuidor de instrumentación analítica de laboratorio ({m})",
        "BAJA",
        "principal marca {m}, share {s}% -> perfil de distribuidor de laboratorio, no de planta de proceso",
        "representantes chilenos de instrumentación analítica (varias empresas compiten por cada marca)",
        "OJO: puede ser importador de laboratorio, NO del rubro de proceso SUPCON; verificar fit antes de invertir tiempo")

    # DIGI -> redes/comunicación industrial
    add(lambda p: marca_ppal(p) == "DIGI",
        "Distribuidor de conectividad industrial / redes OT (DIGI, y otras marcas de enlace)",
        "MEDIA",
        "principal marca DIGI, share {s}%, familia {f} (Redes OT)",
        "distribuidores chilenos de conectividad y redes industriales",
        "confirmar por partida 8517")

    # ETP (transmisores de presión/posicionadores, marca sueca)
    add(lambda p: marca_ppal(p) == "ETP",
        "Representante / distribuidor de instrumentación y accesorios de proceso (marca ETP)",
        "MEDIA",
        "principal marca ETP, share {s}%, {n} marcas en el rubro, {f}, {c}",
        "distribuidores chilenos de instrumentación de proceso con línea ETP",
        "confirmar por partida (típicamente 9026/8481) y comuna de despacho")

    # Yokogawa
    add(lambda p: marca_ppal(p) == "YOKOGAWA",
        "Representante / distribuidor de automatización y control Yokogawa en Chile",
        "MEDIA",
        "principal marca Yokogawa, share {s}%, {f}, {c}",
        "Yokogawa Chile (filial) o su distribuidor autorizado local",
        "Yokogawa tiene canal chileno identificable; cotejar partida 8537/9026")

    # HITACHI / general electric (equipos de potencia)
    add(lambda p: marca_ppal(p) in ("HITACHI", "GENERAL ELECTRIC"),
        "Importador de equipos de potencia y transmisión (Hitachi Energy / GE) para el SE chileno",
        "BAJA",
        "principal marca {m}, share {s}%, familia {f}",
        "canal de Hitachi Energy / GE Vernova en Chile (típicamente proyectos de transmisión)",
        "el rubro de este importador es transmisión/potencia, no instrumentación de proceso: verificar fit")

    return R


REGLAS = reglas()


def evaluar(p):
    for cond, cand in REGLAS:
        try:
            if cond(p):
                fmt = dict(s=p["share_pct"], n=p["n_marcas_rubro"], c=p["comuna_principal"],
                           f=p["fam_principal"], m=marca_ppal(p), mp=marca_ppal_pct(p), id=p["id"])
                c = {k: (v.format(**fmt) if isinstance(v, str) else v) for k, v in cand.items()}
                return c
        except Exception:
            continue
    return dict(nombre="Integrador de instrumentación/automatización con cartera multi-marca",
                confianza="BAJA",
                evidencia=f"perfil multi-marca sin marca dominante clara; share {p['share_pct']}%, {p['n_marcas_rubro']} marcas en el rubro, {p['comuna_principal']}",
                alternativas="no identificable por nombre",
                como_confirmar="solo perfil de conducta")


for p in perfiles:
    nc = evaluar(p)
    p["nombre_candidato"] = {
        "nombre": nc["nombre"],
        "confianza": nc["confianza"],
        "evidencia": nc["evidencia"],
        "alternativas": nc["alternativas"],
        "como_confirmar": nc["como_confirmar"],
    }

# resumen de confianza
from collections import Counter
cnt = Counter(p["nombre_candidato"]["confianza"] for p in perfiles)
d["resumen_confianza_nombres"] = {
    "nota": ("Los nombres son HIPÓTESIS inferidas de la conducta medida (marca dominante, familia, "
             "comuna). El registro de Aduanas no trae nombre ni RUT. 'ALTA'=marca única/dominante con "
             "representante chileno conocido; 'MEDIA'=marca dominante con 2-3 representantes posibles; "
             "'BAJA'=perfil multi-marca sin nombre fiable."),
    "ALTA": cnt.get("ALTA", 0), "MEDIA": cnt.get("MEDIA", 0), "BAJA": cnt.get("BAJA", 0),
}

json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"actualizado: {PATH}")
print("confianza de nombres:", dict(cnt))

print("\n" + "=" * 130)
print(f"{'#':>3} {'ID':>8} {'MARCA PPAL':<12} {'CONF':<6} NOMBRE CANDIDATO")
print("=" * 130)
for i, p in enumerate(perfiles, 1):
    nc = p["nombre_candidato"]
    print(f"{i:>3} {p['id']:>8} {marca_ppal(p):<12} {nc['confianza']:<6} {nc['nombre'][:95]}")
print("=" * 130)
