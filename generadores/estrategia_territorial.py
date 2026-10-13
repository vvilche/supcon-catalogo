#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESTRATEGIA TERRITORIAL: dónde poner el esfuerzo y qué producto llevar a cada zona.

Cruza tres cosas que ya están medidas:
  1. El universo de 3.157 empresas con dolor verificado (RETC + CEN) -> dónde está la demanda.
  2. Las zonas priorizadas del mapa geográfico -> dónde está el canal y el acceso.
  3. Las 7 líneas de producto con su mercado medido por partida arancelaria -> qué se puede vender.

La pregunta que responde: para cada zona, QUÉ LÍNEA SUPCON es la puerta de entrada y por qué.
No es "vender todo en todas partes": cada zona tiene un rubro dominante, y cada rubro tiene
un disparador normativo que empuja una línea específica.

NO INVENTA: la asignación de línea por rubro sale del mapeo ya establecido en los generadores
(universo_prospeccion.py, cruce_normativo.py). El peso de cada zona sale del conteo real de
empresas con dolor.

Salida: datos/estrategia_territorial.json
"""
import os, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

uni = json.load(open(os.path.join(D, "universo_senales_completas.json"), encoding="utf-8"))
emp = uni["empresas"]
con_dolor = [e for e in emp if e["dolor"] > 0]

# ---------- el mapeo de línea por rubro (viene del universo, no se inventa) ----------
RUBRO_LINEAS = uni.get("mapeo_rubro_lineas") or {}

ZONA_NOMBRE = {
 "Z1": "Santiago (Región Metropolitana)",
 "Z2": "Norte minero (Antofagasta y Tarapacá)",
 "Z3": "Valparaíso (Quintero-Concón-Ventanas)",
 "Z4": "Biobío y Ñuble (Talcahuano-Coronel-Laja)",
 "Z5": "Sur industrial y acuícola (Los Lagos-Aysén)",
 "Z6": "Coquimbo-Atacama (minería y generación)",
 "Z7": "Maule-O'Higgins (agroindustria y manufactura)",
}

# ---------- disparador normativo por línea (del cruce normativo) ----------
NORM = json.load(open(os.path.join(D, "cruce_normativo_estrategia.json"), encoding="utf-8"))
DISPARADOR = {k: {"tipo": v.get("tipo_obligacion"), "urgencia": v.get("urgencia"),
                  "norma": (v.get("norma_y_fuente") or "")[:150]}
              for k, v in NORM.get("lineas", {}).items()}

# ---------- mercado por línea (por partida arancelaria, medido) ----------
MER = json.load(open(os.path.join(D, "mercado_hardware_partida.json"), encoding="utf-8"))
MERCADO = {k: v["mercado_usd"] for k, v in MER["lineas"].items()}
ESC = json.load(open(os.path.join(D, "escalera_exito_v3.json"), encoding="utf-8"))
MERCADO_LINEA_ESC = {k: v.get("mercado_corregido_usd") for k, v in ESC["lineas"].items()}

# ============================================================================
# ENSAYO DE CADA ZONA
# ============================================================================
zonas = {}
for e in con_dolor:
    z = e.get("zona") or "sin zona"
    zonas.setdefault(z, []).append(e)

salida = {}
for z, emps in zonas.items():
    if z == "sin zona": continue
    n = len(emps)
    dolor_total = sum(e["dolor"] for e in emps)
    rubros = collections.Counter(e["rubro"] for e in emps)
    lineas = collections.Counter()
    for e in emps:
        for l in e["lineas_supcon"]: lineas[l] += 1

    # el rubro que domina define la PUERTA de entrada
    rubro_top = rubros.most_common(1)[0][0] if rubros else None
    # MATCH TOLERANTE: los nombres de rubro no coinciden literalmente entre fuentes
    # ('Papel y celulosa' vs 'Fabricación de celulosa'; con y sin tildes). Se normaliza y,
    # si no hay igualdad exacta, se busca por palabras clave del rubro.
    def norm(s):
        import unicodedata, re
        s = unicodedata.normalize("NFKD", (s or "").lower())
        s = "".join(c for c in s if not unicodedata.combining(c))
        return re.sub(r"[^a-z0-9 ]", " ", s)
    CLAVES = {
      "quimic": "Producción química", "celulos": "Fabricación de celulosa", "papel": "Fabricación de celulosa",
      "mineral": "Extracción de minerales", "metal": "Producción de metal", "acero": "Producción de metal",
      "generacion": "Generación de energía", "electric": "Transmisión y distribución de energía eléctrica",
      "transmision": "Transmisión y distribución de energía eléctrica",
      "agua": "Suministro y tratamiento de aguas", "sanitari": "Suministro y tratamiento de aguas",
      "combustible": "Combustibles", "residuo": "Gestor de residuos", "alimento": "Producción de alimentos",
      "manufactur": "Industria manufacturera", "pesca": "Pesca", "acuicultur": "Pesca",
      "agropecuar": "Industria agropecuaria y silvicultura", "silvicultur": "Industria agropecuaria y silvicultura",
    }
    lineas_puerta = RUBRO_LINEAS.get(rubro_top, [])
    if not lineas_puerta:
        rt = norm(rubro_top)
        for clave, nombre_mapeo in CLAVES.items():
            if clave in rt:
                lineas_puerta = RUBRO_LINEAS.get(nombre_mapeo, [])
                break

    # concentración: qué tan dominante es el rubro principal (define si la zona es homogénea)
    conc = rubros.most_common(1)[0][1] / n if n else 0

    # cuentas ancla: las de mayor dolor de la zona
    emps_s = sorted(emps, key=lambda e: -e["prioridad"])
    anclas = [{"empresa": e["empresa"], "rubro": e["rubro"], "dolor": e["dolor"],
               "prioridad": e["prioridad"], "comuna": e.get("comuna"),
               "riles": e.get("riles"), "residuos_t": e.get("residuos_t"),
               "cen_dolor": e.get("cen_dolor"), "lineas": e["lineas_supcon"]}
              for e in emps_s[:8]]

    salida[z] = {
      "nombre": ZONA_NOMBRE.get(z, z),
      "empresas_con_dolor": n,
      "dolor_total": round(dolor_total, 1),
      "dolor_promedio": round(dolor_total / n, 1) if n else 0,
      "concentracion_rubro": round(conc, 3),
      "rubro_dominante": rubro_top,
      "rubros": [[k, v] for k, v in rubros.most_common(8)],
      "lineas_demandadas": [[k, v] for k, v in lineas.most_common(7)],
      "lineas_puerta": lineas_puerta,
      "anclas": anclas,
    }

# ---------- ordenar zonas por atractivo comercial ----------
# El atractivo no es solo tamaño: una zona con dolor promedio alto y rubro concentrado convierte
# mejor que una con muchas empresas dispersas. Se pondera n x dolor_promedio, ajustado por
# concentración (una zona homogénea replicа el mismo argumento en cada cuenta).
for z, v in salida.items():
    v["atractivo"] = round(v["empresas_con_dolor"] * v["dolor_promedio"] * (0.6 + v["concentracion_rubro"]), 1)

orden = sorted(salida.items(), key=lambda x: -x[1]["atractivo"])

# ---------- qué producto por línea ----------
# Las fichas de producto por línea, con su mercado medido (o declarado no medible)
LINEA_DETALLE = {}
for lin, x in ESC["lineas"].items():
    prods = [p["producto"] for p in x["productos"]]
    LINEA_DETALLE[lin] = {
      "productos": prods,
      "n_productos": len(prods),
      "mercado_corregido_usd": x.get("mercado_corregido_usd"),
      "mercado_antes_usd": x.get("mercado_antes_usd"),
      "medible": x.get("medible"),
      "nota": x.get("nota_correccion"),
    }

print("=== ESTRATEGIA TERRITORIAL ===\n")
print(f"{'ZONA':6s} {'EMPRESAS':>9s} {'DOLOR PROM':>11s} {'ATRACTIVO':>10s}  {'RUBRO DOMINANTE':34s} PUERTA DE ENTRADA")
print("-"*124)
for z, v in orden:
    print(f"{z:6s} {v['empresas_con_dolor']:>9,} {v['dolor_promedio']:>11.0f} {v['atractivo']:>10,.0f}  "
          f"{str(v['rubro_dominante'])[:34]:34s} {', '.join(v['lineas_puerta'][:3])}")

print("\n=== DETALLE POR ZONA ===")
for z, v in orden:
    print(f"\n{z} · {v['nombre']}")
    print(f"   {v['empresas_con_dolor']:,} empresas con dolor · dolor promedio {v['dolor_promedio']:.0f} · "
          f"concentración {v['concentracion_rubro']*100:.0f}% en {v['rubro_dominante']}")
    print(f"   PUERTA: {' + '.join(v['lineas_puerta']) or 'sin mapear'}")
    print(f"   anclas: {', '.join(a['empresa'][:28] for a in v['anclas'][:4])}")
    print(f"   rubros: {', '.join(f'{k[:22]}({n})' for k,n in v['rubros'][:4])}")

json.dump({
 "metodo": ("Estrategia territorial sobre 1.496 empresas con dolor verificado. Para cada zona: "
   "(1) cuántas empresas y con qué dolor promedio (RETC + CEN), (2) el rubro dominante y su "
   "concentración, (3) las líneas SUPCON que ese rubro demanda, y (4) la puerta de entrada. "
   "El atractivo pondera tamaño × intensidad × concentración: una zona homogénea replica el "
   "mismo argumento en cada cuenta."),
 "fuentes": {
   "demanda": "datos/universo_senales_completas.json (RETC/MMA + Coordinador Eléctrico)",
   "normativa": "datos/cruce_normativo_estrategia.json",
   "mercado": "datos/mercado_hardware_partida.json (Aduanas 2025, por partida)",
   "productos": "datos/escalera_exito_v3.json (63 fichas, 7 líneas)",
 },
 "orden_por_atractivo": [z for z, _ in orden],
 "zonas": salida,
 "producto_por_linea": LINEA_DETALLE,
 "disparador_normativo": DISPARADOR,
 "mercado_por_linea_usd": {k: v for k, v in MERCADO.items()},
}, open(os.path.join(D,"estrategia_territorial.json"),"w"), ensure_ascii=False, indent=1)
print(f"\nguardado: datos/estrategia_territorial.json")
print(f"\n=== PRODUCTO POR LÍNEA (del catálogo de 63 fichas) ===")
for lin, v in LINEA_DETALLE.items():
    m = f"US${v['mercado_corregido_usd']/1e6:,.1f}M" if v["mercado_corregido_usd"] else "no medible aparte"
    print(f"  {lin:24s} {v['n_productos']:>2d} productos · mercado {m}")
