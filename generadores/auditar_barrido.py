#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITORÍA: qué decisores del barrido PERTENECEN de verdad a la empresa target.

EL PROBLEMA (medido en la salida del barrido):
El buscador cuenta como válido cualquier hit del keyword search de LinkedIn. Casos malos:
  - Norvind -> "Norvind Yogeni Mejia Chavez, CEO Multiservicios M&M"  (NO es de Norvind)
  - Canal del Maipo -> "Jefe de operaciones en Coener"                (otra empresa)
  - Gas Sur -> "Ing. control en Linde Gas Chile"                      (otra empresa)
  - Eléctrica Puntilla -> "Operador Centro de Control"                (cargo no decisor)

LA REGLA DE VALIDACIÓN:
Un decisor es VÁLIDO si su headline/empresa menciona la empresa buscada (o su marca), Y si su
cargo es de nivel decisor (jefe/gerente/superintendente/director/subgerente/coordinador), no
operativo (operador/técnico/asistente/analista).

Salida: datos/barrido_campana_auditado.json
"""
import json, os, re, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

# marca buscada -> tokens que validan pertenencia
MARCAS = {
    "Minera Las Cenizas": ["cenizas"], "Minera San Gerónimo": ["geronimo"],
    "Minera Tres Valles": ["tres valles"], "Minera Valle Central": ["valle central"],
    "Codelco": ["codelco"], "CEMIN Holding Minero": ["cemin"], "Molymet": ["molymet"],
    "Anglo American Sur": ["anglo"], "Andes Iron": ["andes iron", "dominga"],
    "Carozzi": ["carozzi"], "Watts": ["watts"], "Ariztía": ["ariztia"],
    "Empresas Lucchetti": ["lucchetti"], "Evercrisp": ["evercrisp"], "Fruna": ["fruna"],
    "Corpora": ["corpora"], "Agrícola AASA": ["aasa", "agro"] if False else ["aasa"],
    "Nestlé Chile": ["nestle"], "Agrosuper": ["agrosuper"],
    "CMPC": ["cmpc"], "Compañía Papelera del Pacífico": ["papelera", "pacifico"],
    "Pisa": ["pisa"], "Fibrocementos Volcán": ["volcan", "fibrocemento"],
    "Oxiquim": ["oxiquim"], "Indura": ["indura"], "Gasco": ["gasco"], "Quimetal": ["quimetal"],
    "GNL Quintero": ["quintero"], "Lipigas": ["lipigas"],
    "Aguas Andinas": ["aguas andinas"], "Aguas Santiago Poniente": ["santiago poniente"],
    "Melón": ["melon"], "Cintac": ["cintac"], "Harsco Metals Chile": ["harsco"],
    "Múltiplas": ["multiplas"],
    "Enel Generacion Chile": ["enel"], "Enel Green Power": ["enel"],
    "Statkraft": ["statkraft"], "Acciona Energia Chile": ["acciona"],
    "GM Holdings": ["gm holdings"], "Besalco": ["besalco"], "Tacora Energy": ["tacora"],
    "Cerro Dominador": ["cerro dominador"], "Aela Generacion": ["aela"],
    "Luz del Norte": ["luz del norte"], "Imelsa Energia": ["imelsa"],
    "Atria Energia": ["atria"], "Norvind": ["norvind"], "Gas Sur": ["gas sur"],
    "Eléctrica Puntilla": ["puntilla"], "Canal del Maipo": ["canal del maipo", "canalistas"],
    "Comasa": ["comasa"],
}

# cargo decisor vs operativo
DECISOR = re.compile(
    r"gerente|subgerente|jefe|jefa|superintendente|director|directora|coordinador|coordinadora|"
    r"responsable|encargado|head|manager|chief|lider|líder|presidente|fiscal|"
    r"supervisor|VP|vicepresidente", re.I)
OPERATIVO = re.compile(
    r"operador|operadora|tecnico|técnico|asistente|analista|practicante|"
    r"ingeniero de turno|conductor|secretaria|recepcionista", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


d = json.load(open(os.path.join(D, "buscador_decisores.json"), encoding="utf-8"))
res = d["resultados"]
buscadas = {norm(e): e for e in json.load(open("/tmp/empresas_final.json", encoding="utf-8"))}

print("=" * 104)
print("AUDITORÍA DEL BARRIDO: ¿pertenece de verdad a la empresa?")
print("=" * 104)

reporte, tot_ok, tot_mal = [], 0, 0
for x in res:
    ne = norm(x["empresa"])
    if ne not in buscadas:
        continue
    original = buscadas[ne]
    marcas = MARCAS.get(original, [ne.split()[0]])
    ok, mal, sin_cargo = [], [], []
    for h in x["hallazgos"]:
        txt = norm(h["nombre"] + " " + h["cargo"] + " " + h.get("fuente", ""))
        pert = any(m in txt for m in marcas)
        # el headline "en <empresa>" es la señal fuerte
        en_emp = any(re.search(rf"en [a-z ]*{re.escape(m)}", txt) for m in marcas)
        cargo_dec = bool(DECISOR.search(h["cargo"]))
        cargo_op = bool(OPERATIVO.search(h["cargo"]))
        if (pert or en_emp) and cargo_dec and not cargo_op:
            ok.append(h)
        elif not (pert or en_emp):
            mal.append(h)
        else:
            sin_cargo.append(h)
    tot_ok += len(ok)
    tot_mal += len(mal)
    reporte.append({"empresa": original, "validos": ok, "ajenos": mal, "no_decisor": sin_cargo,
                    "n_validos": len(ok), "n_ajenos": len(mal), "n_no_decisor": len(sin_cargo)})
    print(f"\n  {original[:34]:36s} {len(ok):2d} válidos | {len(mal):2d} ajenos | {len(sin_cargo):2d} no-decisor")
    for h in ok[:3]:
        print(f"       ✓ {h['nombre'][:26]:28s} {h['cargo'][:46]}")
    for h in mal[:2]:
        print(f"       ✗ AJENO: {h['nombre'][:24]:26s} {h['cargo'][:44]}")
    for h in sin_cargo[:1]:
        print(f"       ~ cargo bajo: {h['nombre'][:22]:24s} {h['cargo'][:40]}")

json.dump(reporte, open(os.path.join(D, "barrido_campana_auditado.json"), "w"),
          ensure_ascii=False, indent=1)
print(f"\n{'='*104}")
print(f"TOTAL: {tot_ok} válidos | {tot_mal} ajenos (descartados)")
print(f"guardado: datos/barrido_campana_auditado.json")
