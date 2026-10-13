#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BARRIDO POR CARGO — buscar a los encargados de cada área EN LINKEDIN, no empresa por empresa.

POR QUÉ ESTE MÉTODO ES MEJOR (medido, y es un cambio de enfoque)
------------------------------------------------------------------------------
El barrido anterior iba empresa por empresa: "para ACME, buscame al jefe de mantenimiento".
Medido, rinde 3,0 personas/empresa en las grandes y **0,1 en el resto**, porque hay que
adivinar que la persona existe y LinkedIn la tiene indexada con el nombre de ESA empresa.

Al revés: buscar POR CARGO a nivel país (`site:linkedin.com/in "jefe de instrumentación y
control" Chile`) devuelve **6 de 6 perfiles reales en cada consulta**, y cada perfil trae la
EMPRESA en el snippet ("Jefe de Instrumentación y Control en ENGIE Chile", "en Albemarle
Corporation", "en Minera Centinela"). Tres ventajas sobre el método anterior:
  1. rinde 6 perfiles por consulta en vez de 0,1 por empresa,
  2. **descubre empresas que NO están en el catálogo** (Albemarle, Soltex, CAIIN),
  3. el dato de empresa viene del propio perfil, no de mi suposición.

CÓMO CLASIFICA LA EMPRESA
Del snippet se extrae "en <EMPRESA>" del headline. Si no aparece, la persona queda con empresa
vacía pero se conserva: sirve para saber cuánta gente con ese cargo hay en el país.

ÁREAS Y CONSULTAS
Las áreas que importan para vender: Instrumentación y Control (DCS/SIS/Instrumentación),
Medio Ambiente y Calidad (Analítica), Mantenimiento (Válvulas), Eléctrico.
Cada área tiene varias consultas con sinónimos porque los cargos varían: "jefe", "encargado",
"supervisor", "líder", "responsable", "gerente".
"""
import json, os, re, time
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
sys.path.insert(0, os.path.join(BASE, "generadores"))
from personas_motor import clasificar_area, limpiar_persona

SAL = os.path.join(D, "personas_por_cargo.jsonl")

# Consultas por área. Se usan varias formulaciones porque los cargos chilenos varían, y se
# combinan con rubros donde el área existe, para no traer perfiles irrelevantes.
CONSULTAS = {
    "Instrumentacion y Control": [
        '"jefe de instrumentación y control" Chile',
        '"jefe de instrumentacion" Chile mineria',
        '"encargado de instrumentación" Chile planta',
        '"jefe de automatizacion" Chile industrial',
        '"supervisor de instrumentacion" Chile',
        '"jefe de control e instrumentacion" Chile',
        '"instrumentista senior" Chile planta',
    ],
    "Medio Ambiente": [
        '"jefe de medio ambiente" Chile industria',
        '"gerente de medio ambiente" Chile mineria',
        '"jefe de gestion ambiental" Chile planta',
        '"encargado de medio ambiente" Chile industrial',
        '"superintendente de medio ambiente" Chile',
        '"jefe de sustentabilidad" Chile industrial',
    ],
    "Calidad": [
        '"jefe de calidad" Chile planta industrial',
        '"jefe de aseguramiento de calidad" Chile mineria',
        '"gerente de calidad" Chile industria',
        '"jefe de control de calidad" Chile planta',
        '"encargado de calidad" Chile proceso',
    ],
    "Mantenimiento": [
        '"jefe de mantenimiento" Chile planta industrial',
        '"jefe de mantenimiento" Chile mineria',
        '"superintendente de mantenimiento" Chile',
        '"jefe de confiabilidad" Chile planta',
        '"jefe de mantencion" Chile planta',
    ],
    "Electrico": [
        '"jefe electrico" Chile planta industrial',
        '"superintendente electrico" Chile mineria',
        '"jefe de mantenimiento electrico" Chile',
        '"jefe de area electrica" Chile',
    ],
    "Produccion": [
        '"jefe de planta" Chile industrial',
        '"jefe de produccion" Chile planta',
        '"jefe de operaciones" Chile planta industrial',
    ],
}

# Empresa desde el headline: "... en EMPRESA" / "at EMPRESA"
RX_EMPRESA = re.compile(
    r"\b(?:en|at|de)\s+([A-Z][\w&.,'\-áéíóúñÁÉÍÓÚÑ ]{2,60}?)"
    r"(?:\s*[|,.\-–]\s*|\s*$|\s+(?:Chile|Chile\.|S\.A|SA|Ltda|SpA|S\.A\.))")
RX_LINK = re.compile(r"(https?://[a-z]{0,3}\.?linkedin\.com/in/[^/?#]+)")


def empresa_de(desc, cargo):
    """Extrae la empresa. DOS FUENTES, en orden de confiabilidad.

    FUENTE 1 (headline): bold con "<cargo> en <EMPRESA>". Ej. "Jefe de Instrumentación y
    Control en Albemarle Corporation".

    FUENTE 2 (sección Experience) — la que faltaba, y es la que más rinde. MEDIDO: el snippet
    trae "### Experience" seguido de "**<cargo>**" y en el bold SIGUIENTE la empresa:
        **Jefe De Mantenimiento** / **CODELCO – Corporación Nacional del Cobre de Chile**
        **Jefe De Calidad** / **Watt's S.A.**
    La primera versión solo miraba el encabezado y perdía el 76% de los perfiles por eso.

    Se exige que el candidato NO sea un cargo (si lo es, es ruido: "Automatización",
    "Instrumentación y Control" aparecían como empresas).
    """
    if not desc:
        return ""
    bolds = [b.strip() for b in re.findall(r"\*\*([^*]{3,160})\*\*", desc)]
    CARGO_RX = re.compile(
        r"^(jefe|gerente|encargad|supervisor|superintend|ingenier|coordinador|director|"
        r"subgerente|especialista|responsable|l[ií]der|analista|t[eé]cnico|instrumentista|"
        r"automatizaci|instrumentaci|control|mantenim|mantenci|calidad|medio ambiente|"
        r"gesti[oó]n|producci|operacion|electric|proceso|divisi[oó]n|la empresa|"
        r"b[uú]squeda|molinos|universidad)", re.I)

    def limpia(x):
        x = re.sub(r"\s+", " ", x).strip(" .,-|")
        # recortar colas de ubicacion ("... S.A., Santiago")
        x = re.split(r",\s*(?:Santiago|Regi[oó]n|Chile|Provincia)", x)[0].strip()
        return x

    # --- FUENTE 1: headline con ' en ' ---
    for b in bolds:
        m = re.search(r"\ben\s+(.+)$", b, re.I)
        if not m:
            continue
        emp = limpia(m.group(1))
        if cargo and (emp.lower() in cargo.lower() or cargo.lower() in emp.lower()):
            continue
        if 2 < len(emp) < 70 and not CARGO_RX.match(emp):
            return emp

    # --- FUENTE 2: seccion Experience (cargo -> empresa en el bold siguiente) ---
    if "### Experience" in desc:
        exp = desc.split("### Experience", 1)[1]
        ex_bolds = [b.strip() for b in re.findall(r"\*\*([^*]{2,160})\*\*", exp)]
        for i, b in enumerate(ex_bolds):
            if CARGO_RX.match(b):
                # el siguiente bold suele ser la empresa
                for j in range(i + 1, min(i + 3, len(ex_bolds))):
                    cand = limpia(ex_bolds[j])
                    if (2 < len(cand) < 70 and not CARGO_RX.match(cand)
                            and not re.match(r"^[A-Z][a-z]+ \d{4}", cand)
                            and "present" not in cand.lower()):
                        return cand
    return ""


def parsear_perfil(desc, url):
    """(nombre, cargo, empresa) del perfil estructurado en el snippet."""
    out = []
    if not desc:
        return out
    bolds = re.findall(r"\*\*([^*]{3,120})\*\*", desc)
    if len(bolds) < 2:
        return out
    CARGOS = re.compile(r"jefe|gerente|supervisor|encargad|ingenier|coordinador|director|"
                        r"subgerente|superintendente|especialista|responsable|l[ií]der|analista|"
                        r"t[eé]cnico|instrumentista|mantenim|mantenci|calidad|ambiente|"
                        r"operacion|producci|electric|control|automatiz|proceso", re.I)
    nombre = cargo = None
    for b in bolds:
        b = b.strip()
        if b.lower() in ("experience", "about", "education", "chile", "santiago"):
            continue
        if CARGOS.search(b):
            if cargo is None:
                cargo = b
            continue
        if nombre is None and 2 <= len(b.split()) <= 5:
            nombre = b
    if nombre and cargo:
        out.append({"nombre": nombre, "cargo": cargo, "empresa": empresa_de(desc, cargo),
                    "linkedin": url})
    return out


ESTADO = os.path.join(D, "personas_por_cargo_estado.json")


def cargar_estado():
    if os.path.exists(ESTADO):
        return json.load(open(ESTADO, encoding="utf-8"))
    return {"consultas_hechas": [], "perfiles": 0, "con_empresa": 0}


def _dedupe(path):
    seen = {}
    if os.path.exists(path):
        for l in open(path, encoding="utf-8"):
            try:
                r = json.loads(l)
            except Exception:
                continue
            k = re.sub(r"\W", "", r["nombre"].lower())
            if k and k not in seen:
                seen[k] = r
    return list(seen.values())


def correr(web_search, areas=None, limit=6, verbose=True):
    """Corre las consultas de las áreas dadas y guarda los perfiles. Reanudable."""
    est = cargar_estado()
    hechas = set(est["consultas_hechas"])
    areas = areas or list(CONSULTAS)
    pend = [(a, q) for a in areas for q in CONSULTAS[a] if q not in hechas]
    if verbose:
        print(f"consultas pendientes: {len(pend)}")
    t0 = time.time()
    nuevas = []
    for area, q in pend:
        try:
            r = web_search(query=f"site:linkedin.com/in {q}", limit=limit)
        except Exception:
            continue
        for w in r.get("data", {}).get("web", []):
            u = w.get("url", "") or ""
            d = w.get("description", "") or ""
            m = RX_LINK.match(u)
            if not m:
                continue
            for p in parsear_perfil(d, m.group(1)):
                # clasificar por el cargo, no por el area de la consulta (regla medida)
                a2 = clasificar_area(p["cargo"])
                p["area"] = a2 or area
                p["consulta"] = q
                nuevas.append(p)
        est["consultas_hechas"].append(q)
    todos = _dedupe(SAL)
    vistos = {re.sub(r"\W", "", r["nombre"].lower()) for r in todos}
    for p in nuevas:
        k = re.sub(r"\W", "", p["nombre"].lower())
        if k and k not in vistos:
            todos.append(p)
            vistos.add(k)
    with open(SAL, "w", encoding="utf-8") as fh:
        for r in todos:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    est["perfiles"] = len(todos)
    est["con_empresa"] = sum(1 for r in todos if r.get("empresa"))
    json.dump(est, open(ESTADO, "w"), ensure_ascii=False)
    if verbose:
        print(f"  +{len(nuevas)} nuevos | {len(todos)} perfiles | "
              f"{est['con_empresa']} con empresa | {time.time()-t0:.0f}s")
    return nuevas


if __name__ == "__main__":
    est = cargar_estado()
    print(f"consultas hechas: {len(est['consultas_hechas'])}")
    print(f"perfiles: {est['perfiles']}  con empresa: {est.get('con_empresa',0)}")
    print("Correr desde execute_code: correr(web_search)")
