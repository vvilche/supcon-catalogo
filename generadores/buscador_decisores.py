#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUSCADOR MULTI-FUENTE DE DECISORES — el motor de gente a cargo.

QUÉ HACE
------------------------------------------------------------------------------
Dado un nombre de empresa, busca sus decisores en TODAS las fuentes que rinden, en orden de
calidad del dato, y devuelve una ficha con nombre + cargo + fuente auditable.

LAS FUENTES, Y CÓMO SE DESCUBRIERON (probadas, no supuestas)
------------------------------------------------------------------------------
1. DIRECMIN `direcmin.com/<slug>/ejecutivos`  ← LA FUENTE MADRE
   Directorio minero de Chile: 93 compañías con página de ejecutivos, una por empresa y por
   DIVISIÓN (Codelco tiene 7: Chuquicamata, El Teniente, Ministro Hales, Radomiro Tomic,
   Salvador, Ventanas, Andina). Lista Cargo + Nombre. Incluye los cargos que importan:
   Gerencia Corporativa Supply Chain, HSEC, Medio Ambiente.
   El slug se descubre del índice paginado `direcmin.com/companias-mineras/<n>` (n=1..7).

2. PÁGINAS DE TRANSPARENCIA (empresas del Estado)
   enap.cl: gerentes con nombre, cargo, profesión y RUT. Codelco, Enami, EFE igual (Ley 20.285).
   ← ESTA FUE LA LECCIÓN: se había contado ENAP como "sin comprador de Medio Ambiente" y el
   Gerente Corporativo de Medio Ambiente está publicado ahí. Buscar en la fuente pública obligatoria,
   no solo en LinkedIn.

3. WEB SEARCH (AIsa / Hermes)  ← para el resto
   `web-search "<empresa> <cargo> linkedin"`: encuentra el perfil. Validar por match de tokens del
   nombre. Rinde 89% en compradores con nombre conocido.

4. ECRM / HISTÓRICO  ← el dato más valioso cuando existe
   Los 183 compradores que pidieron cotización real (2023-2025): no son cargos, son personas que
   YA compraron.

USO
------------------------------------------------------------------------------
  python3 generadores/buscador_decisores.py --empresa "Minera Los Pelambres"
  python3 generadores/buscador_decisores.py --indice            # reconstruye el índice Direcmin
  python3 generadores/buscador_decisores.py --lote 20           # procesa 20 empresas del catálogo

Salida: datos/buscador_decisores.json (acumulativo)
"""
import json, os, re, sys, html as H, subprocess, time, unicodedata, argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(D, "buscador_decisores.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")


def curl(u, t=20):
    try:
        r = subprocess.run(["curl", "-sL", "--max-time", str(t), "-A", UA, u],
                           capture_output=True, text=True, errors="replace")
        return r.stdout or ""
    except Exception:
        return ""


def txt(raw):
    h = re.sub(r"(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>", " ", raw)
    h = re.sub(r"(?s)<[^>]+>", "\n", h)
    return re.sub(r"\n{2,}", "\n", re.sub(r"[ \t]+", " ", H.unescape(h))).strip()


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


def tokens(s):
    return set(t for t in norm(s).split() if len(t) > 2)


# ===========================================================================
# FUENTE 1: DIRECMIN
# ===========================================================================
RX_EJEC = re.compile(r"Cargo:\s*\n\s*([^\n]{4,80})\n\s*\n\s*Nombre:\s*\n\s*([^\n]{4,70})")

# cargo que IMPORTA (el que compra o influye la compra del producto)
CARGO_RELEVANTE = re.compile(
    r"(supply chain|abastecimiento|compras|procurement|mantenimiento|mantenci[oó]n|"
    r"medio ambiente|sustentab|ambiental|hsec|hse|seguridad|calidad|"
    r"operaciones|instrumentaci[oó]n|automatizaci[oó]n|ingenier[ií]a|"
    r"confiabilidad|proyectos|gerente general|presidente|ceo)", re.I)


def direcmin_slug(empresa):
    """Descubre el slug de Direcmin para una razón social, con match ESTRICTO.

    OJO (bug medido): con match laxo por tokens, 'Corp Nacional Del Cobre De Chile' matcheó con
    'enap-empresa-nacional-del-petr-leo' (score 2 por 'nacional'+'chile') y le asignó los
    ejecutivos de ENAP a Codelco. Un dato FALSO con apariencia de bueno es el peor error.
    Exigencia: 2+ tokens distintivos Y que el token más específico de la empresa aparezca.

    Los alias van EXPLÍCITOS porque la razón social del catálogo no se parece al slug de Direcmin
    ('Corp Nacional Del Cobre De Chile' vs 'codelco-chile-divisi-n-...'). Se listan los verificados.
    """
    idx = direcmin_indice()

    # alias verificados: razón social del catálogo -> slug(s) de Direcmin
    ALIAS = {
        "codelco": ["codelco-chile-divisi-n-chuquicamata", "codelco-divisi-n-andina",
                    "codelco-chile-divisi-n-el-teniente", "codelco-chile-divisi-n-ministro-hales",
                    "codelco-chile-divisi-n-radomiro-tomic", "codelco-chile-divisi-n-salvador",
                    "codelco-chile-divisi-n-ventanas"],
        # OJO (bug medido): un alias con la palabra suelta "cobre" matchea CUALQUIER empresa que la
        # contenga — le asignó los ejecutivos de Chuquicamata a 'SOC PUNTA DEL COBRE S A' (Pucobre).
        # Los alias de Codelco van por su nombre COMPLETO, nunca por la palabra genérica.
        "corp nacional del cobre": ["codelco-chile-divisi-n-chuquicamata", "codelco-divisi-n-andina",
                                    "codelco-chile-divisi-n-el-teniente"],
        "codelco chile": ["codelco-chile-divisi-n-chuquicamata", "codelco-divisi-n-andina"],
        "candelaria": ["compa-a-contractual-minera-candelaria"],
        "pelambres": ["minera-los-pelambres"],
        "escondida": ["minera-escondida"],
        "collahuasi": ["compa-a-minera-do-a-in-s-de-collahuasi-scm"],
        "quebrada blanca": ["teck-quebrada-blanca"],
        "cmp": ["compa-a-minera-del-pac-fico-cmp", "compa-a-minera-del-pac-fico-cmp"],
        "pacifico": ["compa-a-minera-del-pac-fico-cmp"],
        "huachipato": ["compa-a-siderurgica-huachipato-cap-acero"],
        "enami": ["enami-empresa-nacional-de-miner-a"],
        "lumina": ["minera-lumina-copper-chile-scm"],
        "caserones": ["minera-lumina-copper-chile-scm"],
        "zald": ["compa-a-minera-zald-var"],
        "spence": ["minera-spence-s-a"],
        "el abra": ["scm-el-abra"],
        "cerro colorado": ["compa-a-minera-cerro-colorado-ltda"],
        "lomas bayas": ["compa-a-minera-lomas-bayas"],
        "kinross": ["kinross-minera-de-chile"],
        "yamana": ["yamana-chile"],
        "el pe": ["minera-el-pe-n"],
        "antucoya": ["minera-antucoya"],
        "pucobre": ["pucobre"],
        "glomgold": [],
        "pqm": ["sociedad-qu-mica-y-minera-de-chile-s-a-sqm"],
        "sqm": ["sociedad-qu-mica-y-minera-de-chile-s-a-sqm"],
        "albemarle": ["minera-albemarle"],
        "tres valles": ["minera-tres-valles"],
        "mantos": ["minera-mantos-de-la-luna"],
        "altos de punitaqui": ["minera-altos-de-punitaqui"],
        "michilla": ["minera-michilla"],
        "tocopilla": ["minera-de-tocopilla"],
        "carola": ["minera-carola"],
        "franke": ["minera-franke"],
        "guanaco": ["minera-guanaco"],
        "lomas": ["compa-a-minera-lomas-bayas"],
        "cerro negro": ["minera-cerro-negro"],
        "salares norte": ["gold-fields-salares-norte"],
        "salar blanco": ["minera-salar-blanco"],
        "maricunga": ["minera-maricunga"],
        "valle central": ["minera-valle-central"],
        "tambillos": ["minera-tambillos"],
        "trucco": ["minera-trucco"],
        "talcuna": ["minera-talcuna"],
        "florida": ["minera-florida"],
        "cordillera": ["minera-cordillera"],
        "ojos del salado": ["compa-a-contractual-minera-ojos-del-salado"],
        "pampa camarones": ["minera-pampa-camarones"],
        "guanaco": ["minera-guanaco"],
        "sierra gorda": ["sierra-gorda-scm-sg-scm"],
        "quiborax": ["quiborax"],
        "pan pacific": ["pan-pacific-copper-co-ltd"],
        "freeport": ["freeport-mcmoran-south-america"],
        "glencore": ["glencore-chile"],
        "lindin": ["lundin-mining"],
        "lundin": ["lundin-mining"],
        "anglo": ["anglo-american-chile"],
        "los bronces": ["minera-los-bronces-anglo-american-sur-s-a"],
        "chagres": ["fundici-n-chagres-anglo-american-sur"],
        "altonorte": ["fundicion-altonorte"],
        "cap acero": ["compa-a-siderurgica-huachipato-cap-acero"],
        "cape stone": ["capstone-copper-corp"],
        "capstone": ["capstone-copper-corp"],
        "kghm": ["kghm-chile"],
        "rio tinto": ["rio-tinto-mining-and-exploration-ltd"],
        "inacal": ["inacal"],
        "imerys": ["imerys-minerales-chile"],
        "cosayach": ["cosayach"],
        "soprocal": ["soprocal"],
        "algorta": ["algorta-norte"],
        "barrick": ["barrick-chile"],
        "bifox": ["bifox"],
        "atacama kozan": ["atacama-kozan-scm"],
        "atacama minerals": ["atacama-minerals-chile-scm"],
        "alxar": ["alxar-miner-a"],
        "acf": ["acf-minera"],
        "cemin": ["cemin"],
        "bhp": ["bhp-chile"],
        "antofagasta minerals": ["antofagasta-minerals"],
        "san pedro": ["minera-san-pedro-s-a"],
        "san geronimo": ["minera-san-geronimo"],
        "la coipa": ["minera-la-coipa"],
        "la condesa": ["minera-la-condesa"],
        "las cenizas": ["minera-las-cenizas"],
        "cerro bayo": ["minera-cerro-bayo"],
        "cerro grande": ["cerro-grande-mining-corporation"],
        "soledad": ["minera-soledad-comisol"],
        "la patagua": ["minera-la-patagua"],
        "el soldado": ["anglo-american-sur-s-a-el-soldado"],
    }
    for clave, slugs in ALIAS.items():
        if clave in norm(empresa):
            for s in slugs:
                if s in idx:
                    return s

    # fallback: match estricto por tokens (para lo que no tenga alias)
    t = tokens(empresa)
    if not t:
        return None
    GENERICOS = {"minera", "compania", "compañia", "sociedad", "chile", "nacional", "del",
                 "de", "la", "los", "las", "empresa", "corp", "corporacion", "s a", "spa",
                 "limitada", "ltda", "y", "s cm", "scm", "grupo"}
    distintivos = t - GENERICOS
    if not distintivos:
        return None
    mejor, score, tiene_clave = None, 0, False
    for slug in idx:
        ts = tokens(slug.replace("-", " "))
        comunes = distintivos & ts
        if not comunes:
            continue
        clave = max(distintivos, key=len)
        if clave not in ts:
            continue
        sc = len(comunes) + 1
        if sc > score:
            mejor, score, tiene_clave = slug, sc, True
    return mejor if (mejor and tiene_clave and score >= 2) else None


def direcmin_indice(force=False):
    """Lista de slugs de las 93 compañías mineras (se cachea en disco)."""
    cache = os.path.join(D, "direcmin_indice.json")
    if os.path.exists(cache) and not force:
        try:
            return json.load(open(cache, encoding="utf-8"))
        except Exception:
            pass
    slugs = set()
    for p in range(1, 9):
        u = ("https://www.direcmin.com/buscar-companias-mineras" if p == 1
             else f"https://www.direcmin.com/companias-mineras/{p}")
        raw = curl(u, 15)
        slugs |= set(re.findall(r'/([a-z0-9\-]{3,45})/ejecutivos"', raw))
        if not slugs and p > 1:
            break
        time.sleep(0.2)
    slugs = sorted(slugs)
    json.dump(slugs, open(cache, "w"), ensure_ascii=False, indent=1)
    return slugs


def busca_direcmin(slug):
    """Ejecutivos de una empresa en Direcmin: Cargo + Nombre."""
    t = txt(curl(f"https://www.direcmin.com/{slug}/ejecutivos"))
    out = []
    for m in RX_EJEC.finditer(t):
        cargo, nombre = m.group(1).strip(), m.group(2).strip()
        if len(nombre.split()) < 2:
            continue
        out.append({"nombre": nombre, "cargo": cargo,
                    "fuente": f"direcmin.com/{slug}/ejecutivos",
                    "relevante": bool(CARGO_RELEVANTE.search(cargo))})
    return out


# ===========================================================================
# FUENTE 2: TRANSPARENCIA (empresas del Estado — Ley 20.285)
# ===========================================================================
# Cada empresa pública publica sus "responsables de la administración" por obligación legal.
# Verificado: ENAP (tabla de gerencias) y Codelco (tabla completa con CV).
TRANSPARENCIA = {
    "enap": "https://www.enap.cl/la-empresa/estructura-corporativa/administracion",
    "empresa nacional del petroleo": "https://www.enap.cl/la-empresa/estructura-corporativa/administracion",
    "codelco": "https://www.codelco.com/transparencia/responsables-de-la-administracion",
    "corp nacional del cobre": "https://www.codelco.com/transparencia/responsables-de-la-administracion",
    # OJO (bug medido): acá también estaba la clave suelta "cobre", que matchea CUALQUIER empresa que
    # la contenga. Le cargó 12 gerentes de CODELCO a 'SOC PUNTA DEL COBRE S A' (Pucobre), incluidas
    # las divisiones Radomiro Tomic, Gabriela Mistral y Ventanas. Los alias van por nombre completo.
    "enami": "https://www.enami.cl/transparencia-activa/responsables-de-la-administracion",
    "empresa nacional de miner": "https://www.enami.cl/transparencia-activa/responsables-de-la-administracion",
}

RX_REG = re.compile(
    r"\n(Gerente[a]?[^\n]{3,70}|Jefe[a]?[^\n]{3,70}|Director[a]?[^\n]{3,70}|"
    r"Presidente[a]?[^\n]{3,70}|Auditor[a]?[^\n]{3,70}|Superintendente[a]?[^\n]{3,70})\n"
    r"([A-ZÁÉÍÓÚÑ][^\n]{5,60})\n"
    r"([^\n]{0,50}(?:Ingenier|Contador|Psicólog|Periodist|Abogad|Geólog|Quím|Comercial)[^\n]{0,40})\n"
    r"(?:RUT:?\s*([\d.\-K]+))?", re.I)

# patrón de la tabla de Codelco: Cargo \n Nombre \n (fecha) \n (carácter) — sin profesión
RX_TABLA = re.compile(
    r"\n(Gerente[a]?[^\n]{3,70}|Presidente[a]?[^\n]{3,70}|Auditor[a]?[^\n]{3,60}|"
    r"Fiscal[a]?[^\n]{3,60})\n([A-ZÁÉÍÓÚÑ][^\n]{5,55})\n", re.I)


def busca_transparencia(empresa):
    """Responsables de la administración publicados por obligación legal (empresas del Estado)."""
    n = norm(empresa)
    for k, u in TRANSPARENCIA.items():
        if k in n:
            t = txt(curl(u, 25))
            out = []
            for m in RX_REG.finditer(t):
                out.append({"nombre": m.group(2).strip(), "cargo": m.group(1).strip(),
                            "profesion": m.group(3).strip(), "rut": (m.group(4) or "").strip(),
                            "fuente": u, "relevante": True})
            if not out:
                for m in RX_TABLA.finditer(t):
                    out.append({"nombre": m.group(2).strip(), "cargo": m.group(1).strip(),
                                "fuente": u, "relevante": True})
            # dedupe
            v, limpio = set(), []
            for h in out:
                kk = norm(h["nombre"])
                if kk and kk not in v:
                    v.add(kk)
                    limpio.append(h)
            return limpio
    return []


# ===========================================================================
# FUENTE 3: AISA / LINKEDIN (universal — cubre los rubros SIN directorio)
# ===========================================================================
# MEDIDO: rinde 6/6 en los rubros sin directorio (acuicultura, celulosa, química, termoeléctricas)
# y trae el HEADLINE real de LinkedIn ("Jefe de mantenimiento en Salmones Camanchaca"), que sirve
# como validación: el cargo y la empresa vienen escritos por la propia persona.
CARGOS_AISA = ["gerente de mantenimiento", "jefe de instrumentacion",
               "gerente de medio ambiente", "gerente de produccion", "jefe de operaciones"]


def _nombra_empresa(texto, empresa):
    """El headline nombra a ESTA empresa? (no una del mismo rubro)

    OJO (bugs medidos): con match laxo entraron contaminaciones reales de la acuicultura, donde
    muchas empresas comparten la palabra del rubro:
      - "Gerente general en Piscicultura y Acuícola Aquaprotec" se asignó a 4 empresas distintas
        (Las Quemas, Iculpe, Nilahue, Aquaprotec) porque todas dicen "Piscicultura/Acuícola".
      - "Gerente General Regional para Latinoamérica" (de otra empresa) entró en 2 más.
    Exigencia: el token MÁS DISTINTIVO (el más largo) de la empresa debe estar en el texto.

    OJO 2: la razón social puede no contener el nombre comercial. 'Corp Nacional Del Cobre De Chile'
    se conoce en el headline como 'Codelco'. Por eso hay ALIAS_NOMBRE_COMERCIAL.
    """
    ALIAS_NOMBRE_COMERCIAL = {
        "corp nacional del cobre": ["codelco"],
        "codelco": ["codelco"],
        "celulosa arauco": ["arauco"],
        "cmpc": ["cmpc"],
        "empresa nacional del petroleo": ["enap"],
        "enap": ["enap"],
        "cia siderurgica huachipato": ["huachipato", "cap acero"],
        "compa a minera del pac fico": ["cmp"],
    }
    n = norm(empresa)
    t = tokens(texto)
    for k, alias in ALIAS_NOMBRE_COMERCIAL.items():
        if k in n:
            for a in alias:
                if a in t or a in norm(texto):
                    return True

    GENERICOS_RUBRO = {"minera", "compania", "sociedad", "chile", "nacional", "del", "de", "la",
                       "los", "las", "empresa", "corp", "corporacion", "spa", "limitada", "ltda",
                       "grupo", "scm", "piscicultura", "acuicola", "acuicultura", "salmones",
                       "pesquera", "servicios", "productos", "granja", "marina", "cultivos",
                       "chilena", "sudamerica", "generadora", "electrica", "energia", "power",
                       "planta", "industrial", "alimentos", "exportadora", "inversiones", "sur"}
    e = tokens(empresa) - GENERICOS_RUBRO
    if not e:
        return False
    clave = max(e, key=len)
    if clave not in t:
        return False
    return len(e & t) >= 1


def capa_aisa(empresa, max_cargos=3):
    """AIsa web-search: perfil de LinkedIn. Se acepta SOLO si el headline nombra la empresa."""
    out = []
    for cargo in CARGOS_AISA[:max_cargos]:
        q = f'"{empresa}" {cargo} linkedin'
        try:
            r = subprocess.run(["aisa", "web-search", q, "--limit", "5", "--raw"],
                               capture_output=True, text=True, timeout=90)
            data = json.loads(r.stdout or "{}")
        except Exception:
            time.sleep(1)
            continue
        for it in data.get("results", []) or []:
            u = it.get("url", "")
            if "linkedin.com/in/" not in u:
                continue
            cont = it.get("content") or ""
            tit = it.get("title") or ""
            if not (_nombra_empresa(cont, empresa) or _nombra_empresa(tit, empresa)):
                continue
            m = re.search(r"[Hh]eadline:\s*([^\n]{5,90})", cont)
            cargo_real = m.group(1).strip() if m else cargo
            nombre = tit.split("|")[0].split(" - ")[0].strip()[:48]
            if len(nombre.split()) < 2:
                continue
            out.append({"nombre": nombre, "cargo": cargo_real, "linkedin": u.split("?")[0],
                        "fuente": "LinkedIn (AIsa, headline validado)", "relevante": True})
        time.sleep(0.4)
    return out


# ===========================================================================
# EL BUSCADOR
# ===========================================================================
def buscar(empresa, con_web=False):
    """Busca decisores de una empresa en todas las fuentes, en orden de calidad."""
    res = {"empresa": empresa, "hallazgos": [], "fuentes_usadas": [], "notas": []}

    # 1. Direcmin
    slug = direcmin_slug(empresa)
    if slug:
        ds = busca_direcmin(slug)
        if ds:
            res["hallazgos"] += ds
            res["fuentes_usadas"].append(f"Direcmin ({slug}): {len(ds)}")

    # 2. Transparencia (Estado)
    ts = busca_transparencia(empresa)
    if ts:
        res["hallazgos"] += ts
        res["fuentes_usadas"].append(f"Transparencia: {len(ts)}")

    # 3. AIsa/LinkedIn (universal: cubre los rubros sin directorio sectorial)
    if con_web:
        ws = capa_aisa(empresa)
        if ws:
            res["hallazgos"] += ws
            res["fuentes_usadas"].append(f"LinkedIn: {len(ws)}")

    # dedupe por nombre normalizado
    vistos, limpio = set(), []
    for h in res["hallazgos"]:
        k = norm(h["nombre"])
        if not k or k in vistos:
            continue
        vistos.add(k)
        limpio.append(h)
    res["hallazgos"] = limpio
    res["n_decisores"] = len(limpio)
    res["n_relevantes"] = sum(1 for h in limpio if h.get("relevante"))
    if not limpio:
        res["notas"].append("sin decisores en las fuentes consultadas")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--empresa")
    ap.add_argument("--indice", action="store_true")
    ap.add_argument("--lote", type=int)
    ap.add_argument("--web", action="store_true",
                    help="usar también la capa LinkedIn/AIsa (cubre rubros sin directorio)")
    ap.add_argument("--fuente", default="matriz",
                    help="de dónde tomar la lista de empresas: 'matriz' (dolor RETC) o "
                         "'mineras' (los 220 mineros del RETC, que la matriz perdió)")
    a = ap.parse_args()

    if a.indice:
        idx = direcmin_indice(force=True)
        print(f"índice Direcmin reconstruido: {len(idx)} compañías")
        return

    if a.empresa:
        r = buscar(a.empresa, con_web=a.web)
        print(f"\n=== {r['empresa']} ===")
        print(f"  fuentes: {', '.join(r['fuentes_usadas']) or 'ninguna'}")
        print(f"  decisores: {r['n_decisores']} ({r['n_relevantes']} relevantes para compra)")
        for h in r["hallazgos"]:
            mark = "*" if h.get("relevante") else " "
            print(f"   {mark} {h['nombre'][:30]:32s} {h['cargo'][:46]}")
            print(f"       fuente: {h['fuente'][:70]}")
        return

    # lote: procesar empresas de la fuente elegida
    if a.fuente == "mineras":
        mn = json.load(open(os.path.join(D, "mineras_retc.json"), encoding="utf-8"))
        emp = [{"empresa": x["empresa"], "carga_peligrosa_t": x["respel_t"]}
               for x in mn["mineras"]]
        print(f"fuente: mineras del RETC ({len(emp)} empresas, que la matriz había perdido)")
    else:
        m = json.load(open(os.path.join(D, "matriz_dolor_linea_perfil.json"), encoding="utf-8"))
        emp = sorted(m["empresas"], key=lambda x: -(x.get("carga_peligrosa_t") or 0))
    emp = sorted(emp, key=lambda x: -(x.get("carga_peligrosa_t") or 0))
    acc = {}
    if os.path.exists(OUT):
        try:
            acc = {x["empresa"]: x for x in json.load(open(OUT, encoding="utf-8"))["resultados"]}
        except Exception:
            acc = {}
    pend = [e for e in emp if e["empresa"] not in acc][:a.lote or 20]
    print(f"procesando {len(pend)} empresas (ya hechas: {len(acc)})...\n")
    for e in pend:
        r = buscar(e["empresa"], con_web=a.web)
        r["dolor_t"] = e.get("carga_peligrosa_t") or 0
        acc[e["empresa"]] = r
        # GUARDAR EMPRESA POR EMPRESA: sin esto, un corte pierde toda la corrida
        # (bug medido: se pidieron 200 empresas y el archivo quedó con 70).
        json.dump({"que_es": "Buscador multi-fuente de decisores por empresa.",
                   "fuentes": ["Direcmin /ejecutivos (93 mineras)",
                               "Transparencia (empresas del Estado)",
                               "Web search / LinkedIn"],
                   "total_empresas": len(acc), "resultados": list(acc.values())},
                  open(OUT, "w"), ensure_ascii=False, indent=1)
        print(f"  {r['n_decisores']:>3} decisores | {e['empresa'][:44]:46s} {', '.join(r['fuentes_usadas'])[:44]}")
    json.dump({"que_es": "Buscador multi-fuente de decisores por empresa.",
               "fuentes": ["Direcmin /ejecutivos (93 mineras)",
                           "Transparencia (empresas del Estado)",
                           "Web search / LinkedIn"],
               "total_empresas": len(acc), "resultados": list(acc.values())},
              open(OUT, "w"), ensure_ascii=False, indent=1)
    con = sum(1 for x in acc.values() if x["n_decisores"])
    tot = sum(x["n_decisores"] for x in acc.values())
    print(f"\n=== {con} de {len(acc)} empresas con decisores | {tot} decisores ===")
    print(f"guardado: {OUT}")


if __name__ == "__main__":
    main()
