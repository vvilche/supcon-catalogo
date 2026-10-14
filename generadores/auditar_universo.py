#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITA el barrido del universo: separa los decisores REALES de los ajenos.

DOS PROBLEMAS MEDIDOS QUE ESTO CIERRA
------------------------------------------------------------------------------
1. DIRECMIN CONTAMINA por slug mal asignado: "CMPC TISSUE S A", "CMPC CELULOSA S A" e
   "INVERSIONES DEL PACIFICO LIMITADA" recibieron los MISMOS 21/18/17 ejecutivos de
   "compa-a-minera-del-pac-fico-cmp" (CAP, Compañía Minera del Pacífico) — otra empresa.
   Señal: dos empresas DISTINTAS con el MISMO conteo y la MISMA fuente Direcmin.

2. LINKEDIN TRAE HOMÓNIMOS: razones sociales que son un APELLIDO ("CONTRERAS", "GOMEZ",
   "FERNANDEZ", "ZUNIGA", "SALOMON SACK") devuelven el headline de cualquier persona con ese
   apellido. Señal: el nombre de la empresa es 1 token que también es nombre de persona.

Salida: datos/barrido_universo_auditado.json
"""
import json, os, re, unicodedata, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


DECISOR = re.compile(
    r"gerente|subgerente|jefe|jefa|superintendente|director|directora|coordinador|coordinadora|"
    r"responsable|encargado|head|manager|chief|lider|líder|presidente|fiscal|vicepresidente|VP", re.I)
OPERATIVO = re.compile(r"operador|operadora|tecnico|técnico|asistente|analista|practicante|"
                       r"conductor|secretaria|recepcionista|operario", re.I)

# razones sociales que son un APELLIDO suelto: el keyword search devuelve cualquiera
APELLIDOS = {"contreras", "fernandez", "gomez", "zuniga", "hidalgo", "villalba", "salomon",
             "sack", "quintana", "roa", "najle", "varas", "godia", "lagos", "munoz", "gonzalez"}

estado = set(json.load(open(os.path.join(D, "barrido_universo_estado.json"), encoding="utf-8")))
bd = json.load(open(os.path.join(D, "buscador_decisores.json"), encoding="utf-8"))["resultados"]
buscador = {norm(x["empresa"]): x for x in bd}

# --- detectar el contaminado de Direcmin: misma fuente + mismo conteo en >1 empresa
fuente_conteo = collections.Counter()
for x in bd:
    for f in x.get("fuentes_usadas", []):
        if f.startswith("Direcmin"):
            fuente_conteo[(f, x["n_decisores"])] += 1
slugs_contaminados = {k[0] for k, v in fuente_conteo.items() if v > 1}

reporte, tot_ok, tot_ajeno, tot_bajo = [], 0, 0, 0
for x in bd:
    ne = norm(x["empresa"])
    if ne not in estado:
        continue
    ok, ajenos, bajos, motivos = [], [], [], []

    # problema 1: Direcmin con slug compartido
    fuente_dir = [f for f in x.get("fuentes_usadas", []) if f.startswith("Direcmin")]
    if fuente_dir and any(f in slugs_contaminados for f in fuente_dir):
        motivos.append(f"slug Direcmin compartido por varias empresas: {fuente_dir[0]}")
        ajenos = list(x["hallazgos"])
    # problema 2: razón social que es apellido
    elif ne in APELLIDOS or (len(ne.split()) == 1 and ne.split()[0] in APELLIDOS):
        motivos.append("razón social es un apellido: el keyword search devuelve homónimos")
        ajenos = list(x["hallazgos"])
    else:
        for h in x["hallazgos"]:
            txt = norm(h["nombre"] + " " + h["cargo"] + " " + h.get("fuente", ""))
            marca = ne.split()[0] if ne.split() else ""
            pert = bool(marca) and marca in txt
            if not pert:
                ajenos.append(h)
            elif OPERATIVO.search(h["cargo"]) or not DECISOR.search(h["cargo"]):
                bajos.append(h)
            else:
                ok.append(h)

    tot_ok += len(ok)
    tot_ajeno += len(ajenos)
    tot_bajo += len(bajos)
    reporte.append({"empresa": x["empresa"], "validos": ok, "ajenos": ajenos,
                    "no_decisor": bajos, "n_validos": len(ok), "n_ajenos": len(ajenos),
                    "motivos": motivos})

print("=" * 100)
print("AUDITORÍA DEL BARRIDO DEL UNIVERSO")
print("=" * 100)
print(f"  empresas auditadas: {len(reporte)}")
print(f"  DECISORES VÁLIDOS:  {tot_ok:,}")
print(f"  ajenos (descartados): {tot_ajeno:,}")
print(f"  cargo no decisor:   {tot_bajo:,}")

malas = [r for r in reporte if r["n_ajenos"] > 0 or r["motivos"]]
print(f"\n=== EMPRESAS CON PROBLEMA ({len(malas)}) ===")
for r in sorted(malas, key=lambda z: -z["n_ajenos"])[:25]:
    m = r["motivos"][0] if r["motivos"] else f"{r['n_ajenos']} ajenos"
    print(f"  {r['empresa'][:40]:42s} válidos={r['n_validos']:2d} ajenos={r['n_ajenos']:2d} | {m[:52]}")

print(f"\n=== TOP EMPRESAS CON DECISORES VÁLIDOS ===")
for r in sorted(reporte, key=lambda z: -z["n_validos"])[:30]:
    if r["n_validos"]:
        print(f"  {r['empresa'][:44]:46s} {r['n_validos']:2d}")

json.dump({"totales": {"validos": tot_ok, "ajenos": tot_ajeno, "no_decisor": tot_bajo},
           "empresas": reporte}, open(os.path.join(D, "barrido_universo_auditado.json"), "w"),
          ensure_ascii=False, indent=1)
print(f"\nguardado: datos/barrido_universo_auditado.json")
