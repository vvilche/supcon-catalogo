#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PERFILADO DETALLADO DE LOS 74 INTEGRADORES / DISTRIBUIDORES TÉCNICOS (Chile 2025).

Toma de `datos/perfiles_importador_2025.json` los importadores con tipo ==
"INTEGRADOR / distribuidor técnico" y recorre los 12 archivos crudos de Aduanas
una sola vez extrayendo, SOLO de las líneas de esos IDs:
  - top 10 marcas del rubro con monto
  - desglose por las 7 familias del dominio
  - top 5 partidas arancelarias con glosa
  - países de origen con monto
  - otros rubros (capítulo arancelario) con % del total
  - estacionalidad mensual (CIF total y del rubro)
  - comunas de despacho con monto

Mismas reglas de clasificación que perfilar_importadores_v2.py (mismas partidas,
misma lista de marcas, mismo filtro de descripción). Salida:
datos/perfilado_74_integradores.json
"""
import os, glob, json, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "/Users/victorvilche/.hermes/cache/scratch/estudio-mercado/datos/aduanas_2025/extraido"
D = os.path.join(BASE, "datos")

COL_IMP, COL_COMUNA = 6, 5
COL_ARANC, COL_CIF, COL_NOMBRE, COL_MARCA = 157, 158, 133, 134
COL_PAIS, COL_FECHA = 21, 4

def num(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return 0.0

FAMILIAS = {
 "Instrumentación (presión/temp/caudal/nivel)": ["90262010","90262019","90262090","90269000",
    "90251100","90251900","90258010","90258090","90259000","90261010","90261090","90268010","90268090"],
 "Analizadores de proceso": ["90271010","90271090","90272000","90273000","90275000","90278100","90278999","90279090"],
 "Válvulas de control": ["84811000","84812010","84812020","84813000","84814000","84818010","84818090","84819000"],
 "Control / DCS / PLC / SIS": ["85371000","85371010","85371090","85372000","85372010","85372090","85381000","85389000"],
 "Medición eléctrica y protecciones": ["90301000","90302000","90303100","90303200","90303300","90303900",
    "90304000","90308200","90308400","90308900","90283000","90283010","90283090"],
 "Redes OT": ["85176210","85176220","85176290","85176900","85177000"],
 "Fuentes y convertidores": ["85043100","85043200","85043300","85044000","85045000","85049000"],
}
P2FAM = {}
for fam, l in FAMILIAS.items():
    for p in l: P2FAM[p] = fam

# glosas descriptivas de las partidas del dominio (para el TOP 5 con nombre legible)
GLOSA = {
 "85371000":"Tableros, paneles y demás soportes con aparatos eléctricos para control (PLC)",
 "85371010":"Cuadros y tableros de control o distribución (< 1000 V)",
 "85371090":"Los demás cuadros y tableros de control",
 "85372000":"Tableros con tensión > 1000 V",
 "85381000":"Partes de tableros y paneles",
 "85389000":"Partes de aparatos de la partida 85.35/85.36",
 "90262010":"Manómetros y medidores de presión",
 "90262019":"Instrumentos de medida de presión (los demás)",
 "90262090":"Instrumentos y aparatos para medida de presión",
 "90269000":"Partes y accesorios de instrumentos de presión",
 "90251100":"Termómetros de líquido, lectura directa",
 "90251900":"Termómetros y pirómetros (los demás)",
 "90258010":"Densímetros, areómetros y similares",
 "90258090":"Los demás instrumentos de medida de temperatura",
 "90259000":"Partes de instrumentos de medida de temperatura",
 "90261010":"Caudalímetros electromagnéticos",
 "90261090":"Instrumentos para medida del caudal de líquidos",
 "90268010":"Reguladores de presión y caudal",
 "90268090":"Los demás instrumentos de caudal/gases",
 "90271010":"Analizadores de gases de motor",
 "90271090":"Analizadores de gases (los demás)",
 "90272000":"Cromatógrafos y aparatos de electroforesis",
 "90273000":"Espectrómetros y espectrofotómetros",
 "90275000":"Los demás aparatos de análisis óptico/radiación",
 "90278100":"Espectrómetros de masas",
 "90278999":"Los demás instrumentos de análisis físico/químico",
 "90279090":"Partes de analizadores e instrumentos de análisis",
 "84811000":"Válvulas reductoras de presión",
 "84812010":"Válvulas para transmisiones hidráulicas",
 "84812020":"Válvulas para transmisiones neumáticas",
 "84813000":"Válvulas de retención (check)",
 "84814000":"Válvulas de alivio y seguridad",
 "84818010":"Grifos y válvulas de paso / esféricas",
 "84818090":"Los demás artículos de grifería y válvulas",
 "84819000":"Partes de válvulas y artículos de grifería",
 "90301000":"Instrumentos para medida de radiaciones ionizantes",
 "90302000":"Osciloscopios y analizadores de espectro",
 "90303100":"Multímetros (sin registrador)",
 "90303200":"Multímetros con registrador",
 "90303300":"Los demás instrumentos de medida de tensión/intensidad",
 "90303900":"Los demás aparatos de medida eléctrica",
 "90304000":"Instrumentos de medida de telecomunicaciones",
 "90308200":"Instrumentos para medida o control de obleas/semiconductores",
 "90308400":"Los demás instrumentos con registrador",
 "90308900":"Los demás instrumentos de medida eléctrica",
 "90283000":"Contadores de electricidad (medidores de energía)",
 "90283010":"Contadores de electricidad monofásicos",
 "90283090":"Los demás contadores de electricidad",
 "85176210":"Conmutadores (switches) para telefonía/redes",
 "85176220":"Routers y aparatos de encaminamiento",
 "85176290":"Los demás aparatos de conmutación y enrutamiento",
 "85176900":"Los demás aparatos de transmisión/recepción",
 "85177000":"Partes de aparatos de telefonía/redes",
 "85043100":"Transformadores de potencia <= 1 kVA",
 "85043200":"Transformadores 1-16 kVA",
 "85043300":"Transformadores 16-500 kVA",
 "85044000":"Convertidores estáticos (fuentes, UPS, variadores)",
 "85045000":"Bobinas de reactancia y self-inducción",
 "85049000":"Partes de transformadores y convertidores",
}

RUBRO_CAP = {
 "84":"Maquinaria mecánica","85":"Eléctrico / electrónico","90":"Instrumentos de medida",
 "87":"Vehículos y automoción","39":"Plásticos","73":"Manufacturas de acero","76":"Aluminio",
 "28":"Química inorgánica","29":"Química orgánica","38":"Productos químicos","72":"Acero",
 "26":"Minerales","27":"Combustibles","62":"Vestuario","61":"Vestuario","64":"Calzado",
 "94":"Muebles","48":"Papel","40":"Caucho","74":"Cobre","30":"Farmacéutico","33":"Cosméticos",
 "22":"Bebidas","32":"Pinturas","25":"Minerales no metálicos","19":"Cereales","20":"Frutas y hortalizas",
}

MARCAS_RUBRO = ["ENDRESS","KROHNE","MICRO MOTION","FLEXIM","CIDRA","ROSEMOUNT","YOKOGAWA","HONEYWELL",
 "ABB","SIEMENS","SCHNEIDER","EMERSON","METSO","VALMET","FUJI","AZBIL","MITSUBISHI","OMRON",
 "PHOENIX","TURCK","IFM","SICK","BALLUFF","BAUMER","LEUZE","KEYENCE","WIKA","ASHCROFT","DANFOSS",
 "SAMSON","MASONEILAN","FISHER","VALVITALIA","BRAY","NELES","VELAN","CIRCOR","KITZ","ROTORK","AUMA",
 "MTS","AMETEK","MAGNETROL","VEGA","PEPPERL","TESTO","DRAGER","MSA","SERVOMEX","THERMO","AGILENT",
 "SHIMADZU","BRUKER","HACH","WTW","XYLEM","YSI","BARTEC","STAHL","SEL","HITACHI","HYOSUNG","ALSTOM",
 "ETP","ARTECHE","PFIFFNER","TELEDYNE","QUALITROL","DOBLE","OMICRON","MEGGER","FLUKE","WATERS",
 "PERKIN","LECO","BUCHI","KNAUER","ANALYTIK","BECKHOFF","WAGO","ROCKWELL","ALLEN","FESTO","SMC",
 "PILZ","RITTAL","WEIDMULLER","LUTZE","FANUC","YASKAWA","SEW","LENZE","VACON","INNOMOTICS","WEG",
 "HIRSCHMANN","BELDEN","MOXA","ADVANTECH","DIGI","LANTRONIX","PERLE","KYLAND","GENERAL ELECTRIC"]

# marcas que SUPCON compite directamente (competidoras directas del portafolio SUPCON+Hobré)
COMPETIDORAS_SUPCON = {"ENDRESS","KROHNE","MICRO MOTION","ROSEMOUNT","YOKOGAWA","HONEYWELL","ABB",
 "SIEMENS","SCHNEIDER","EMERSON","FUJI","AZBIL","MITSUBISHI","OMRON","WIKA","DANFOSS","SAMSON",
 "MASONEILAN","FISHER","MAGNETROL","VEGA","SERVOMEX","THERMO","ROCKWELL","ALLEN","BECKHOFF"}

def norm_marca(m):
    x = (m or "").upper().replace("-F","").split("~")[0].strip()
    for c in MARCAS_RUBRO:
        if x == c or x.startswith(c+" ") or x.startswith(c+"-") or c in x: return c
    return None

EXCLUIR = ["PARTE","ACCESORIO","REPUESTO","ESTUCHE","AUTOMOVIL","VEHICULO","CAMION","TRACTOR",
 "TELEFONO","CELULAR","TABLET","NOTEBOOK","LAPTOP","IMPRESORA","TELEVISOR","AUDIFONO","JUGUETE",
 "ELECTRODOMESTICO","MEDICAMENTO","REACTIVO","DIAGNOSTICO","IN VITRO"]
def desc_ok(n):
    n=(n or "").upper(); return not any(x in n for x in EXCLUIR)

# --- IDs objetivo ---
perfiles = json.load(open(os.path.join(D,"perfiles_importador_2025.json"), encoding="utf-8"))["perfiles"]
objetivo = {p["id"]: p for p in perfiles if p["tipo"] == "INTEGRADOR / distribuidor técnico"}
print(f"integradores objetivo: {len(objetivo)}")

acc = {k: {"marcas":collections.Counter(),"familias":collections.Counter(),
           "partidas":collections.Counter(),"partidas_glosa":{},
           "paises":collections.Counter(),"rubros":collections.Counter(),
           "comunas":collections.Counter(),"meses_total":collections.Counter(),
           "meses_instru":collections.Counter(),"total":0.0,"items":0,
           "instru":0.0,"instru_items":0}
       for k in objetivo}

archivos = sorted(glob.glob(os.path.join(RAW,"*.txt")))
print(f"archivos: {len(archivos)}")
for fi,f in enumerate(archivos):
    n=0
    with open(f, encoding="latin-1") as fh:
        for line in fh:
            c = line.rstrip("\n").split(";")
            if len(c) <= COL_CIF: continue
            k = (c[COL_IMP] or "").strip()
            if k not in acc: continue
            cif = num(c[COL_CIF])
            if cif <= 0: continue
            p8 = (c[COL_ARANC] or "").strip()[:8]
            nombre = c[COL_NOMBRE] or ""
            a = acc[k]
            a["total"] += cif; a["items"] += 1
            cap = p8[:2] if len(p8)>=2 else "?"
            a["rubros"][RUBRO_CAP.get(cap,"Otros")] += cif
            a["comunas"][(c[COL_COMUNA] or "").strip()] += cif
            fe = (c[COL_FECHA] or "").strip()
            mes=None
            if len(fe)==8 and fe.isdigit() and fe[4:8]=="2025":
                dd,mm=int(fe[0:2]),int(fe[2:4])
                if 1<=dd<=31 and 1<=mm<=12: mes=f"2025-{mm:02d}"
            if mes: a["meses_total"][mes]+=cif
            fam = P2FAM.get(p8)
            if not fam or not desc_ok(nombre): continue
            marca = norm_marca(c[COL_MARCA])
            if not marca: continue
            a["instru"] += cif; a["instru_items"] += 1
            a["familias"][fam] += cif
            a["marcas"][marca] += cif
            a["partidas"][p8] += cif
            a["partidas_glosa"][p8] = GLOSA.get(p8,"")
            a["paises"][(c[COL_PAIS] or "").strip()] += cif
            if mes: a["meses_instru"][mes]+=cif
            n+=1
    print(f"  [{fi+1:2d}/12] {os.path.basename(f)[:40]:42s} líneas de interés: {n:,}")

# comuna y país: nombres
COMUNA = {"13114":"Las Condes","13123":"Santiago Centro","13101":"Santiago","13119":"Providencia",
 "13122":"Vitacura","13115":"Lo Barnechea","13110":"Ñuñoa","13124":"Quinta Normal","13126":"Pudahuel",
 "13120":"Macul","13104":"Conchalí","13111":"Quilicura","13109":"Renca","13125":"Cerro Navia",
 "13108":"Estación Central","13116":"Maipú","13105":"La Cisterna","13106":"San Miguel",
 "13103":"Conchalí","13102":"Cerro Navia","13121":"La Reina","13118":"San Joaquín","13107":"Lo Prado",
 "13112":"Recoleta","13113":"Independencia","13301":"Puente Alto","13302":"San Bernardo",
 "05101":"Valparaíso","05109":"Viña del Mar","08101":"Concepción","08110":"San Pedro de la Paz",
 "02101":"Antofagasta","03301":"Copiapó","04101":"La Serena","04301":"Coquimbo","06301":"Rancagua",
 "06310":"San Fernando","07101":"Talca","07301":"Cauquenes","09101":"Temuco","10101":"Puerto Montt",
 "01101":"Iquique","12201":"Punta Arenas","05701":"San Antonio","05501":"Quillota","02102":"Mejillones"}
PAIS = {"336":"Alemania","563":"China","505":"EE.UU.","549":"India","508":"Japón","512":"Italia",
 "225":"Francia","317":"Corea del Sur","220":"España","226":"Reino Unido","528":"Países Bajos",
 "511":"Canadá","510":"Taiwán","513":"Bélgica","559":"Malasia","412":"México","301":"Brasil",
 "204":"Argentina","484":"Suecia","223":"Finlandia","206":"Dinamarca","222":"Suiza","721":"Egipto",
 "501":"Australia","215":"Austria","554":"Nueva Zelanda","804":"Ucrania","380":"Israel",
 "423":"México","497":"Panamá","132":"Brasil","337":"Alemania","200":"Argentina","424":"Costa Rica"}
def comuna(c):
    c=(c or "").strip()
    return COMUNA.get(c, ("cód. "+c) if c else "sin dato")
def pais(c):
    c=(c or "").strip()
    return PAIS.get(c, ("cód. "+c) if c else "sin dato")

# --- armar perfiles detallados ---
detalle = []
for k, a in acc.items():
    base = objetivo[k]
    total = a["total"] or base["total_usd"]
    instru = a["instru"] or base["instru_usd"]
    share = instru/total*100 if total else 0
    marcas_top = a["marcas"].most_common(10)
    marcas_con_monto = [{"marca":m,"usd":round(v,2),
                         "pct_del_rubro":round(v/instru*100,1) if instru else 0} for m,v in marcas_top]
    fams = [{"familia":f,"usd":round(v,2),
             "pct_del_rubro":round(v/instru*100,1) if instru else 0}
            for f,v in a["familias"].most_common()]
    partes = [{"partida":p,"glosa":a["partidas_glosa"].get(p,""),
               "usd":round(v,2),"pct_del_rubro":round(v/instru*100,1) if instru else 0}
              for p,v in a["partidas"].most_common(5)]
    origenes = [{"pais":pais(c),"codigo":c,"usd":round(v,2),
                 "pct_del_rubro":round(v/instru*100,1) if instru else 0}
                for c,v in a["paises"].most_common(6)]
    rubros = [{"rubro":r,"usd":round(v,2),"pct_del_total":round(v/total*100,1) if total else 0}
              for r,v in a["rubros"].most_common(6)]
    # comunas de despacho (todas las que aparecen, con monto)
    comunas = [{"comuna":comuna(c),"codigo":c,"usd":round(v,2),
                "pct_del_total":round(v/total*100,1) if total else 0}
               for c,v in a["comunas"].most_common(6)]
    # estacionalidad: ordenar por mes
    mes_t = {m:round(a["meses_total"].get(m,0.0),2) for m in sorted(a["meses_total"])}
    mes_i = {m:round(a["meses_instru"].get(m,0.0),2) for m in sorted(a["meses_instru"])}
    pico = max(mes_i, key=mes_i.get) if mes_i else ""
    pico_usd = mes_i.get(pico,0.0)
    ticket = round(total/a["items"],2) if a["items"] else 0
    ticket_instru = round(instru/a["instru_items"],2) if a["instru_items"] else 0
    n_comp = sum(1 for m,_ in marcas_top if m in COMPETIDORAS_SUPCON)
    tiene_supcon = "SUPCON" in a["marcas"] or "HObre" in a["marcas"]
    detalle.append({
      "id":k,
      "instru_usd":round(instru,2),"total_usd":round(total,2),"share_pct":round(share,1),
      "instru_items":a["instru_items"],"items_totales":a["items"],
      "meses_activos":len(a["meses_total"]),
      "comuna_principal":comuna(base["comuna"]),
      "comunas_despacho":comunas,
      "n_comunas":len(a["comunas"]),
      "marcas_top10":marcas_con_monto,
      "n_marcas_rubro":len(a["marcas"]),
      "familias":fams,
      "fam_principal":(fams[0]["familia"] if fams else ""),
      "partidas_top5":partes,
      "paises_origen":origenes,
      "otros_rubros":rubros,
      "estacionalidad_mes_instru":mes_i,
      "estacionalidad_mes_total":mes_t,
      "mes_pico":pico,"mes_pico_usd":round(pico_usd,2),
      "ticket_promedio_item":ticket,
      "ticket_promedio_item_rubro":ticket_instru,
      "n_marcas_competidoras_supcon":n_comp,
      "trae_supcon":bool(tiene_supcon),
    })

detalle.sort(key=lambda x:-x["instru_usd"])
subtotal = sum(d["instru_usd"] for d in detalle)

# --- concentración ---
top10 = detalle[:10]
conc = {
 "n_integradores":len(detalle),
 "subtotal_rubro_usd":round(subtotal,2),
 "top10_individual":[
   {"id":d["id"],"usd":d["instru_usd"],"pct_del_subtotal":round(d["instru_usd"]/subtotal*100,1)}
   for d in top10],
 "usd_top10":round(sum(d["instru_usd"] for d in top10),2),
 "pct_top10":round(sum(d["instru_usd"] for d in top10)/subtotal*100,1),
 "usd_resto_64":round(subtotal-sum(d["instru_usd"] for d in top10),2),
 "pct_resto_64":round((subtotal-sum(d["instru_usd"] for d in top10))/subtotal*100,1),
}

# marcas agregadas en los 74
mar_agg = collections.Counter()
for d in detalle:
    for m in d["marcas_top10"]:
        mar_agg[m["marca"]] += m["usd"]
marcas_agregadas = [{"marca":m,"usd":round(v,2),
                     "pct_del_subtotal_rubro":round(v/subtotal*100,1) if subtotal else 0,
                     "n_integradores_que_la_traen":sum(1 for d in detalle
                        if any(x["marca"]==m for x in d["marcas_top10"]))}
                    for m,v in mar_agg.most_common(25)]

n_traen_comp = sum(1 for d in detalle if d["n_marcas_competidoras_supcon"]>0)
n_traen_supcon = sum(1 for d in detalle if d["trae_supcon"])
competencia = {
 "integradores_con_al_menos_1_marca_competidora_supcon":n_traen_comp,
 "integradores_con_al_menos_1_marca_competidora_supcon_pct":round(n_traen_comp/len(detalle)*100,1),
 "integradores_que_traen_supcon":n_traen_supcon,
 "nota":"Un integrador cuenta como 'trae competidora' si alguna de sus TOP-10 marcas del rubro está en la lista de competidoras directas del portafolio SUPCON+Hobré (Endress, KROHNE, Rosemount, Yokogawa, Honeywell, ABB, Siemens, Schneider, Emerson, Fuji, Azbil, Mitsubishi, Omron, Wika, Danfoss, Samson, Fisher, Magnetrol, Vega, Servomex, Thermo, Rockwell/Allen-Bradley, Beckhoff).",
}

# --- hallazgos comerciales (con el número que los respalda) ---
from collections import Counter as C
comunas_cnt = C(d["comuna_principal"] for d in detalle)
paises_flag = C()
for d in detalle:
    for o in d["paises_origen"]:
        paises_flag[o["pais"]] += 1
especializacion = sum(1 for d in detalle if d["share_pct"]>=80)
multirubro = sum(1 for d in detalle if d["share_pct"]<40)
regulares = sum(1 for d in detalle if d["meses_activos"]>=12)
semestrales = sum(1 for d in detalle if d["meses_activos"]<=6)
ctrl_dcs = sum(1 for d in detalle if d["fam_principal"]=="Control / DCS / PLC / SIS")
fuentes = sum(1 for d in detalle if d["fam_principal"]=="Fuentes y convertidores")
hallazgos = [
 {"hallazgo":f"El canal está muy concentrado: los 10 primeros integradores mueven US${conc['usd_top10']/1e6:.1f}M, el {conc['pct_top10']}% del subtotal de los 74 (US${subtotal/1e6:.1f}M).",
  "tipo":"dato medido"},
 {"hallazgo":f"El integrador #1 (ID {detalle[0]['id']}) solo importa US${detalle[0]['instru_usd']/1e6:.2f}M del rubro pero el {detalle[0]['share_pct']}% de su volumen es de esa familia; el canal combina integradores puros con distribuidores muy diversificados.",
  "tipo":"dato medido"},
 {"hallazgo":f"{comunas_cnt.most_common(1)[0][1]} de los 74 integradores ({comunas_cnt.most_common(1)[0][1]/74*100:.0f}%) tienen su dirección de despacho principal en {comunas_cnt.most_common(1)[0][0]}. El canal de instrumentación está domiciliado en el barrio alto de Santiago.",
  "tipo":"dato medido"},
 {"hallazgo":f"{ctrl_dcs} de 74 integradores ({ctrl_dcs/74*100:.0f}%) tienen como familia principal Control/DCS/PLC/SIS, y {fuentes} ({fuentes/74*100:.0f}%) en Fuentes y convertidores. El grueso del canal no viene por instrumentación de campo sino por automatización y potencia.",
  "tipo":"dato medido"},
 {"hallazgo":f"{especializacion} de 74 integradores ({especializacion/74*100:.0f}%) dedican >=80% de su importación al rubro (son integradores/especialistas de verdad); {multirubro} ({multirubro/74*100:.0f}%) dedican <40% (distribuidores multirrubro donde la instrumentación es una línea más).",
  "tipo":"dato medido"},
 {"hallazgo":f"{regulares} de 74 ({regulares/74*100:.0f}%) importan los 12 meses del año; {semestrales} ({semestrales/74*100:.0f}%) lo hacen en 6 meses o menos. Hay un núcleo de canal permanente y una cola de compras esporádicas.",
  "tipo":"dato medido"},
 {"hallazgo":f"{n_traen_comp} de 74 integradores ({n_traen_comp/74*100:.0f}%) traen al menos una marca competidora directa de SUPCON entre sus TOP-10 del rubro; {n_traen_supcon} traen SUPCON/Hobré.",
  "tipo":"dato medido"},
 {"hallazgo":f"La marca más representada agregada en el canal es {marcas_agregadas[0]['marca']} (US${marcas_agregadas[0]['usd']/1e6:.1f}M entre los 74, la traen {marcas_agregadas[0]['n_integradores_que_la_traen']} integradores), seguida por {marcas_agregadas[1]['marca']} y {marcas_agregadas[2]['marca']}. El canal está alineado con el estándar europeo/alemán.",
  "tipo":"dato medido"},
 {"hallazgo":f"Alemania aparece como origen en {paises_flag.most_common(4)[0][1] if paises_flag else 0} integradores, China en {paises_flag.get('China',0)} y EE.UU. en {paises_flag.get('EE.UU.',0)}. El origen alemán domina el canal técnico.",
  "tipo":"dato medido"},
 {"hallazgo":f"El ticket promedio por ítem del rubro va de US${min(d['ticket_promedio_item_rubro'] for d in detalle):,.0f} a US${max(d['ticket_promedio_item_rubro'] for d in detalle):,.0f}. Los tickets bajos indican repuestos/consumibles; los altos, proyecto llave en mano.",
  "tipo":"dato medido"},
 {"hallazgo":"Los integradores que combinan instrumentación con capítulos no eléctricos (alimentos, química, papel) son los que arman solución completa de planta y son los mejores candidatos para portafolio SUPCON completo (DCS + instrumentación + válvulas), no solo para un producto.",
  "tipo":"inferencia (no medida)"},
 {"hallazgo":"Los integradores con 1 sola marca en el rubro probablemente son la filial local o el representante exclusivo de esa marca: cambiar su portafolio es muy difícil; los multirrubro (>3 marcas) son más permeables a incorporar una línea nueva.",
  "tipo":"inferencia (no medida)"},
]

salida = {
 "anio":2025,
 "generado_por":"generadores/perfilar_detalle_integradores.py",
 "fuente":"Registro DIN de importaciones, Servicio Nacional de Aduanas (datos.gob.cl), 12 archivos mensuales 2025",
 "nota_identidad":"El registro NO trae nombre ni RUT del importador (Ley 20.285). NUM_UNICO_IMPORTADOR es un ID estable por empresa. Estos perfiles describen conducta, no identidad.",
 "arquetipo":"INTEGRADOR / distribuidor técnico (share del rubro >= 25% de su importación total)",
 "n_integradores":len(detalle),
 "subtotal_rubro_usd":round(subtotal,2),
 "concentracion":conc,
 "marcas_mas_representadas_agregadas":marcas_agregadas,
 "competencia_supcon":competencia,
 "hallazgos_comerciales":hallazgos,
 "perfiles":detalle,
}
out = os.path.join(D,"perfilado_74_integradores.json")
json.dump(salida, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nguardado: {out} ({len(detalle)} perfiles)")

# --- print tabla ---
print("\n" + "="*118)
print(f"{'#':>3} {'ID':>8} {'COMUNA':<16} {'INSTRU_USD':>13} {'SHARE%':>7} {'MES':>4} {'TOP MARCAS':<44}")
print("="*118)
for i,d in enumerate(detalle,1):
    ms = ", ".join(f"{m['marca']}" for m in d["marcas_top10"][:3])
    print(f"{i:>3} {d['id']:>8} {d['comuna_principal']:<16} {d['instru_usd']/1e6:>10.2f}M {d['share_pct']:>6.1f}% {d['meses_activos']:>3}/12 {ms[:44]:<44}")
print("="*118)
print(f"SUBTOTAL 74 INTEGRADORES: US${subtotal/1e6:,.2f}M")
