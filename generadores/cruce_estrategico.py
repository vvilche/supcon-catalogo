#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUCE ESTRATÉGICO: normativa × geografía × capital chino × catálogo SUPCON.

POR QUÉ. Los tres cruces existían por separado (normativo, geográfico, capital chino) pero la
estrategia de penetración no usaba ninguno: era un documento aparte. Este módulo los une para
producir una lista de OBJETIVOS PRIORIZADOS, que es lo que sirve para vender.

El cruce asigna a cada cuenta una puntuación con cuatro señales medidas:
  1. DISPARADOR NORMATIVO (de cruce_normativo_estrategia.json): ¿hay una norma que obliga a
     comprar lo que SUPCON vende? Pesa más si es obligatoria y urgente.
  2. GEOGRAFÍA (de mapa_oportunidades_chile.json): ¿está en una zona priorizada Z1-Z6? Pesa más
     si la zona está recomendada y si el canal local es débil (menos competencia de distribución).
  3. CAPITAL CHINO (de empresas_capital_chino_chile.json): ¿tiene dueño o EPC chino? Es el atajo:
     un EPC especifica el equipamiento sin licitación abierta.
  4. ENCAJE DE CATÁLOGO: ¿cuántas líneas de SUPCON aplican a su operación?

NO inventa datos: cada señal sale de uno de los tres JSON con su fuente. Cuando no hay dato,
la cuenta queda sin esa señal y se declara en `senales_faltantes`.

Salida: datos/cruce_estrategico_objetivos.json
"""
import os, json, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))

norm_d = json.load(open(os.path.join(D, "cruce_normativo_estrategia.json"), encoding="utf-8"))
geo    = json.load(open(os.path.join(D, "mapa_oportunidades_chile.json"), encoding="utf-8"))
chino  = json.load(open(os.path.join(D, "empresas_capital_chino_chile.json"), encoding="utf-8"))

# ---------- zonas geográficas: a qué regiones aplica cada una ----------
ZONA_REGIONES = {
 "Z1": ["metropolitana", "santiago", "las condes"],
 "Z2": ["antofagasta", "calama", "mejillones", "tocopilla"],
 "Z3": ["valparaiso", "quintero", "concon", "san antonio", "vina del mar"],
 "Z4": ["biobio", "concepcion", "talcahuano", "coronel", "laja", "arauco"],
 "Z5": ["los lagos", "aysen", "magallanes", "puerto montt", "chiloe"],
 "Z6": ["coquimbo", "atacama", "vallenar", "huasco", "la serena"],
}
ZONA_INFO = {z.get("zona","")[:2]: z for z in geo.get("zonas_prioritarias", [])}

# Cuentas cuya operacion es MULTIRREGIONAL o NACIONAL: no se pueden asignar a una zona.
# Forzar una zona seria inventar. CGE opera de Arica a Magallanes y Codelco tiene faenas en
# varias regiones: se marcan como "multi-region" y se tratan aparte en la estrategia.
MULTIREGION = ["nacional","15 regiones","varias regiones","todo el pais","multirreg",
               "arica y parinacota a magallanes","a nivel nacional"]

def zona_de(region, comuna, plantas):
    """La zona prioritaria sale de donde esta la OPERACION, con dos guardas.

    1. Se evalua primero la operacion (plantas) y despues la region declarada.
    2. Si la operacion es multirregional, NO se asigna zona: se devuelve "multi".
       Si no, "Arica a Magallanes" matcheaba Magallanes (Z5) y ponia a CGE, una distribuidora
       de la zona central, en el sur del pais.
    """
    op = norm(" ".join(map(str, plantas or [])))
    reg = norm(f"{region} {comuna}")
    if any(g in op or g in reg for g in MULTIREGION):
        return "multi", "multirregional"
    for z, regs in ZONA_REGIONES.items():
        if any(r in op for r in regs):
            return z, "operacion"
    for z, regs in ZONA_REGIONES.items():
        if any(r in reg for r in regs):
            return z, "sede"
    return None, None

# ---------- disparadores normativos por línea ----------
DISPARADORES = {}
for lin, x in norm_d.get("lineas", {}).items():
    DISPARADORES[lin] = {
      "tipo": x.get("tipo_obligacion", "?"),
      "urgencia": x.get("urgencia", "?"),
      "norma": (x.get("norma_y_fuente") or "")[:180],
      "empresas_candidatas": x.get("empresas_candidatas", []) or [],
      "industrias": x.get("industrias_afectadas", []) or [],
    }

def puntos_norma(tipo, urg):
    base = {"obligatoria": 30, "incentivada": 12}.get((tipo or "").lower(), 8)
    return base + {"alta": 12, "media": 6, "baja": 2}.get((urg or "").lower(), 0)

# ---------- puntuar cada empresa ----------
cuentas = []
for e in chino.get("empresas", []):
    plantas = e.get("plantas") or []
    region = e.get("region") or ""
    z, z_origen = zona_de(region, e.get("comuna"), plantas)
    prods = e.get("productos_supcon_aplicables") or []

    # señal 1: normativa. Se busca la empresa en las listas de candidatas del cruce normativo.
    nombre_n = norm(e.get("nombre", ""))
    razon_n = norm(e.get("nombre", "").split("(")[0])
    lineas_norma, normas_txt = [], []
    for lin, dd in DISPARADORES.items():
        for cand in dd["empresas_candidatas"]:
            cn = norm(cand)
            clave = razon_n[:12]
            if clave and (clave in cn or razon_n in cn or nombre_n[:12] in cn):
                lineas_norma.append(lin)
                normas_txt.append(f"{lin}: {dd['tipo']} / urgencia {dd['urgencia']}")
                break

    # señal 2: normativa aplicable por INDUSTRIA. Antes cualquier palabra larga daba match y
    # las 34 cuentas recibian el mismo puntaje. Ahora se exige una palabra CLAVE del rubro
    # (no de la descripción de la norma) presente en el sector o las plantas declaradas.
    sujeto = norm(" ".join([str(e.get("sector","")), " ".join(map(str,plantas))]))
    CLAVES_RUBRO = {
      "Instrumentacion": ["quimic","petroquim","celulos","papel","miner","agua","sanitari","aliment",
                          "bebida","vinicol","cervecer","curtiembre","textil","metalurgic","fundicion"],
      "Analitica":       ["termoelectric","generacion","fundicion","cement","cal","celulos","papel",
                          "refiner","petroquim","quimic","energi","coquizacion","vidrio","ceramic"],
      "Valvulas":        ["generacion","vapor","calder","quimic","petroquim","celulos","papel",
                          "miner","aliment","bebida","agua","refiner","tratamiento"],
      "DCS":             ["generacion","transmision","electric","celulos","papel","quimic","petroquim",
                          "miner","cement","acero","aliment","bebida","refiner","agua"],
      "PLC":             ["oil","gas","ducto","agua","residual","ferroviar","tunel","tratamiento"],
      "SIS":             ["refiner","petroquim","quimic","miner","subterran","gas","combustible",
                          "celulos","papel","acero"],
      "Software y plataforma": ["electric","generacion","transmision","distribucion","combustible",
                          "agua","sanitari","energi"],
    }
    lineas_por_industria = []
    for lin, dd in DISPARADORES.items():
        claves = CLAVES_RUBRO.get(lin, [])
        if any(k in sujeto for k in claves):
            lineas_por_industria.append(lin)

    # señal 3: capital chino
    est = (e.get("estado_participacion") or "").lower()
    p_chino = {"verificado": 25, "parcial": 15}.get(est, 0)
    es_epc = "EPC" in (e.get("sector","") + " " + " ".join(plantas) + " " + (e.get("participacion") or "")).upper()

    # señal 4: encaje de catálogo
    p_cat = min(len(set(prods)), 6) * 4

    # señal 5: geografía
    zinfo = ZONA_INFO.get(z or "", {})
    # pesa mas si la operacion esta en la zona (aqui entra el equipo) que si solo esta la sede
    if z in ("Z1","Z2","Z3","Z4"):
        p_geo = 18 if z_origen == "operacion" else 11
    else:
        p_geo = 8 if z else 0

    total = p_chino + p_cat + p_geo + (puntos_norma(
        DISPARADORES[lineas_norma[0]]["tipo"] if lineas_norma else "?",
        DISPARADORES[lineas_norma[0]]["urgencia"] if lineas_norma else "?") if lineas_norma
        else (12 if lineas_por_industria else 0))

    faltantes = []
    if not z: faltantes.append("geografía no mapeada a zona")
    if not lineas_norma and not lineas_por_industria: faltantes.append("sin disparador normativo identificado")
    if est not in ("verificado","parcial"): faltantes.append("participación china no verificada")

    cuentas.append({
      "nombre": e.get("nombre"),
      "grupo_chino": e.get("grupo_chino"),
      "participacion": e.get("participacion"),
      "estado_participacion": e.get("estado_participacion"),
      "sector": e.get("sector"),
      "region": region,
      "zona": z,
      "zona_nombre": zinfo.get("zona"), "zona_por": z_origen,
      "productos_supcon": prods,
      "lineas_norma": sorted(set(lineas_norma)),
      "lineas_por_industria": sorted(set(lineas_por_industria)),
      "normas": normas_txt,
      "es_epc": es_epc,
      "web": e.get("web"),
      "fuente": e.get("fuente"),
      "razon_prioridad_original": e.get("razon_prioridad"),
      "score": total,
      "detalle_score": {"capital_chino": p_chino, "catalogo": p_cat, "geografia": p_geo},
      "senales_faltantes": faltantes,
    })

# --- filtro de rubro: SUPCON vende a PROCESO CONTINUO (mineria, quimica, celulosa, energia,
# agua, cemento, acero). Una vina, un retailer de construccion o un importador de buses no son
# cuentas de automatizacion de proceso: se separan para no inflar la lista de prioridades.
RUBRO_PROCESO = ["miner","quimic","petroquim","celulos","papel","energi","electric","generacion",
  "transmision","distribucion","agua","sanitari","cement","acero","fundicion","refiner","gas",
  "combustible","petroleo","litio","desaliniz","tratamiento","chuquicamata","radomiro","teniente",
  "andina","división","division","hidroelectric","hidroelectrica","planta de proceso","pesquer",
  "acuicultur","piscicultur","salmon","bess","solar","eolic"]
# rubros que NO son proceso continuo: la razon social gana siempre sobre cualquier otra señal
RUBRO_EXCLUIDO = ["vinicol","vitivinicol","vinos","vina ","vinas ","wine","bethwines","yantai",
  "agricol","retail","ferreteri","construmart","miniso","construccion civil","automotriz",
  "vehiculo","yutong","chery","great wall","gwm","omoda","jaecoo","bus ","camion","telecomunic",
  "celular","zte","huawei","mineria bf","software de consumo","data center","computacion",
  "electrodomestic","supermercad","tienda","concesionaria","ruta 5","hospital","peaje",
  "inmobiliaria","embalse — industria vitivi","puerto exterior"]
# rubros que NO son proceso continuo aunque caigan en el sector: se excluyen explicitamente

def es_proceso(c):
    """SUPCON vende a proceso continuo industrial.

    El campo `sector` del JSON de origen NO es confiable: asigna 'Química y manufactura' a dos
    viñas y 'Energía y eléctrico' a un importador de buses. Por eso la decision se toma por la
    RAZON SOCIAL y las PLANTAS declaradas; el sector solo se usa como ultimo apoyo y nunca
    alcanza por si solo para incluir una cuenta.
    """
    razon = norm(str(c.get("nombre","")) + " " + str(c.get("grupo_chino","")))
    plantas = norm(" ".join(map(str, c.get("plantas") or [])))
    sector = norm(str(c.get("sector","")))
    # 1. exclusion explicita por razon social: GANA SIEMPRE.
    #    Necesario porque el campo `sector` del JSON de origen esta mal en varias cuentas
    #    (asigna 'Química y manufactura' a dos viñas). La razon social no miente.
    if any(k in razon for k in RUBRO_EXCLUIDO): return False
    # 2. prueba positiva: razon social, plantas o sector declaran rubro de proceso.
    #    Se aceptan los tres porque las cuentas legitimas declaran su rubro en alguno de ellos
    #    (Codelco en 'División Chuquicamata', Transelec en 'líneas de transmisión').
    return any(k in (razon + " " + plantas + " " + sector) for k in RUBRO_PROCESO)

for c in cuentas:
    c["es_proceso_continuo"] = es_proceso(c)
    if not c["es_proceso_continuo"]:
        c["nota_rubro"] = ("Cuenta con capital chino pero NO de proceso continuo: se conserva en "
                           "el listado por completitud, fuera de la lista de prioridad comercial.")

# ordenar: primero las de proceso continuo, dentro de ellas por score
cuentas.sort(key=lambda c: (not c["es_proceso_continuo"], -c["score"]))

# ---------- resumen ----------
por_zona = {}
for c in cuentas:
    z = c["zona"] or "sin zona"
    por_zona.setdefault(z, []).append(c["nombre"])

con_norma = [c for c in cuentas if c["lineas_norma"] or c["lineas_por_industria"]]
epcs = [c for c in cuentas if c["es_epc"]]

PROC = [c for c in cuentas if c["es_proceso_continuo"]]
NOPROC = [c for c in cuentas if not c["es_proceso_continuo"]]
print("=== CRUCE ESTRATÉGICO: 4 señales sobre las 34 empresas con capital chino ===\n")
print(f"  cuentas cruzadas:            {len(cuentas)}")
print(f"  con disparador normativo:    {len(con_norma)}")
print(f"  EPC chinos (atajo):          {len(epcs)}")
print(f"  en zona prioritaria Z1-Z4:   {len([c for c in cuentas if c['zona'] in ('Z1','Z2','Z3','Z4')])}")
print(f"  operacion multirregional:    {len([c for c in cuentas if c['zona']=='multi'])}")
print()
print(f"{'#':>3s} {'CUENTA':44s} {'Z':>3s} {'score':>6s}  señales")
print("-"*96)
for i, c in enumerate(PROC[:20], 1):
    sen = []
    if c["estado_participacion"] in ("verificado","parcial"): sen.append("chino")
    if c["zona"]: sen.append(c["zona"])
    if c["lineas_norma"]: sen.append("norma")
    elif c["lineas_por_industria"]: sen.append("norma-ind")
    if c["es_epc"]: sen.append("EPC")
    sen.append(f"{len(c['productos_supcon'])} prod")
    print(f"{i:>3d} {c['nombre'][:44]:44s} {c['zona'] or '-':>3s} {c['score']:>6.0f}  {', '.join(sen)}")

print(f"\n  de PROCESO CONTINUO (cuentas reales): {len(PROC)} | fuera de rubro: {len(NOPROC)}")
if NOPROC:
    print("  fuera de rubro (se conservan, no se priorizan): " + ", ".join(c["nombre"][:26] for c in NOPROC))
print()
print("=== cuentas por zona prioritaria ===")
for z in ["Z1","Z2","Z3","Z4","Z5","Z6","multi","sin zona"]:
    if z in por_zona:
        print(f"  {z} ({len(por_zona[z])}): {', '.join(n[:34] for n in por_zona[z][:5])}")

json.dump({
 "metodo": ("Cruce de 4 señales medidas sobre las empresas con capital chino en Chile: "
   "(1) disparador normativo del cruce normativo, (2) zona geográfica priorizada del mapa, "
   "(3) participación china verificada, (4) número de líneas SUPCON aplicables. "
   "Puntaje = capital chino (0-25) + catálogo (0-24) + geografía (0-18) + normativa (0-42). "
   "No hay dato inventado: cada señal sale de uno de los tres JSON con su fuente."),
 "fuentes": {
   "normativa": "datos/cruce_normativo_estrategia.json",
   "geografia": "datos/mapa_oportunidades_chile.json",
   "capital_chino": "datos/empresas_capital_chino_chile.json",
   "capacidad": "datos/cobertura_catalogo.json",
 },
 "resumen": {
   "cuentas": len(cuentas),
   "con_disparador_normativo": len(con_norma),
   "epcs": len(epcs),
   "en_zona_prioritaria": len([c for c in cuentas if c["zona"] in ("Z1","Z2","Z3","Z4")]),
   "por_zona": {z: len(v) for z, v in por_zona.items()},
 },
 "disparadores_por_linea": DISPARADORES,
 "cuentas": cuentas,
}, open(os.path.join(D,"cruce_estrategico_objetivos.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/cruce_estrategico_objetivos.json")
