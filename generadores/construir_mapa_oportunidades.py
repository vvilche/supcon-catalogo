#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye datos/mapa_oportunidades_chile.json — mapa geografico de oportunidades SUPCON Chile.
Datos reales de: InfoTecnica CEN (centrales), RETC/MMA (establecimientos industriales),
SEIA (proyectos), Aduanas 2025 (canal importador). Cero datos inventados."""
import json, os, openpyxl
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = '/tmp'

# ---------- 1. CANAL (Aduanas 2025) ----------
canal = json.load(open(os.path.join(BASE, 'datos/_canal_geo.json')))

# ---------- 2. DEMANDA: RETC establecimientos industriales por region x rubro ----------
wb = openpyxl.load_workbook(os.path.join(TMP, 'retc.xlsx'), read_only=True, data_only=True)
ws = wb.active
rows = ws.iter_rows(values_only=True)
hdr = next(rows); IX = {h: i for i, h in enumerate(hdr)}
RUBROS = ['Extracción minerales', 'Producción química', 'Papel/celulosa', 'Alimentos',
          'Producción metal', 'Combustibles', 'Generación energía', 'Tratamiento aguas',
          'Transmisión/distribución', 'Pesca', 'Manufacturera']
# el header real de rubro es 'Rubro RETC' con valores largos
retc_reg = defaultdict(Counter)
retc_reg_emp = defaultdict(lambda: defaultdict(Counter))
for r in rows:
    if not r or not r[0]:
        continue
    reg = (r[IX['Región']] or '').strip()
    # normalizar nombre de region RETC -> nombre corto
    rub = (r[IX['Rubro RETC']] or '').strip()
    rz = (r[IX['Razón social']] or '').strip()
    retc_reg[reg][rub] += 1
    retc_reg_emp[reg][rub][rz] += 1

# mapeo region RETC -> region corta
RETC2SHORT = {
 'Arica y Parinacota': 'Arica y Parinacota',
 'Tarapacá': 'Tarapacá', 'Antofagasta': 'Antofagasta', 'Atacama': 'Atacama',
 'Coquimbo': 'Coquimbo', 'Valparaíso': 'Valparaíso',
 'Metropolitana de Santiago': 'Metropolitana',
 "Libertador Gral. Bernardo O'Higgins": "O'Higgins", 'Maule': 'Maule', 'Ñuble': 'Ñuble',
 'Biobío': 'Biobío', 'Araucanía': 'Araucanía', 'Los Ríos': 'Los Ríos',
 'Los Lagos': 'Los Lagos', 'Aysén del Gral. Carlos Ibañez del Campo': 'Aysén',
 'Magallanes y de la Antártica Chilena': 'Magallanes'}

# rubros RETC reales (con nombres exactos del dataset)
RUB_MAP = {
 'Extracción minerales': ['Extracción de minerales'],
 'Producción química': ['Producción química'],
 'Papel/celulosa': ['Papel y celulosa'],
 'Alimentos': ['Alimentos'],
 'Producción metal': ['Producción de metal'],
 'Combustibles': ['Combustibles'],
 'Generación energía': ['Generación energía'],
 'Tratamiento aguas': ['Tratamiento aguas'],
 'Transmisión/distribución': ['Transmisión/distribución'],
 'Pesca': ['Pesca'],
 'Manufacturera': ['Manufacturera'],
}

# ---------- 3. DEMANDA: CEN centrales por region ----------
cen = []
for f in ['cen_c1.json', 'cen_c2.json', 'cen_c3.json']:
    d = json.load(open(os.path.join(TMP, f)))
    cen += (d.get('results', d) if isinstance(d, dict) else d)
cen_reg = defaultdict(Counter)
for c in cen:
    cen_reg[(c.get('region_nombre') or '').strip()][c.get('propietario_nombre')] += 1

# ---------- 4. DEMANDA: SEIA proyectos por region (top por inversion) ----------
seia = json.load(open(os.path.join(BASE, 'datos/_seia_por_industria.json')))
def fnum(v):
    try:
        return float(str(v).replace(',', '.')) if v not in (None, '') else 0.0
    except Exception:
        return 0.0
# normalizar nombre region SEIA -> corto
SEIA2SHORT = {
 'Región de Arica y Parinacota': 'Arica y Parinacota', 'Región de Tarapacá': 'Tarapacá',
 'Región de Antofagasta': 'Antofagasta', 'Región de Atacama': 'Atacama',
 'Región de Coquimbo': 'Coquimbo', 'Región de Valparaíso': 'Valparaíso',
 'Región Metropolitana de Santiago': 'Metropolitana',
 "Región del Libertador General Bernardo O'Higgins": "O'Higgins",
 'Región del Maule': 'Maule', 'Región de Ñuble': 'Ñuble', 'Región del Biobío': 'Biobío',
 'Región de La Araucanía': 'Araucanía', 'Región de Los Ríos': 'Los Ríos',
 'Región de Los Lagos': 'Los Lagos',
 'Región de Aysén del General Carlos Ibáñez del Campo': 'Aysén',
 'Región de Magallanes y de la Antártica Chilena': 'Magallanes',
 'Interregional': 'Interregional', '': 'SIN DATO',
}
IND_LABEL = {'mineria': 'minería', 'quimica': 'química y petroquímica',
             'celulosa_papel': 'celulosa y papel', 'alimentos': 'alimentos',
             'cemento': 'cemento y cal', 'generacion': 'generación eléctrica',
             'agua': 'agua y saneamiento', 'puertos': 'puertos y logística'}

# region_demanda: para cada region corta acumular industrias, empresas, plantas
REGIONES = ['Antofagasta', 'Atacama', 'Tarapacá', 'Metropolitana', 'Valparaíso', 'Biobío',
            "O'Higgins", 'Coquimbo', 'Araucanía', 'Los Lagos', 'Maule', 'Ñuble', 'Los Ríos',
            'Aysén', 'Magallanes', 'Arica y Parinacota']

demanda_por_region = []
for regc in REGIONES:
    # encontrar la clave RETC correspondiente
    retc_key = next((k for k, v in RETC2SHORT.items() if v == regc), None)
    cen_key = None  # nombre en CEN
    CEN_ALIAS = {regc, regc.replace('Ñ', 'N'), regc.replace("'", ''), regc.replace('í', 'i'),
                 regc.replace('é', 'e'), regc.replace('á', 'a')}
    if regc == "O'Higgins":
        CEN_ALIAS.add('OHiggins')
    if regc == 'Metropolitana':
        CEN_ALIAS.add('Metropolitana de Santiago')
    for k in cen_reg:
        if k in CEN_ALIAS:
            cen_key = k
    # industrias presentes (RETC rubros objetivo con conteo)
    inds = []
    if retc_key:
        for lab, rubs in RUB_MAP.items():
            n = sum(retc_reg[retc_key][x] for x in rubs)
            if n:
                inds.append({'industria': lab, 'establecimientos_retc': n})
        inds.sort(key=lambda x: -x['establecimientos_retc'])
    # empresas: fusion RETC (rubros clave) + CEN + SEIA
    empresas = set()
    if retc_key:
        for lab in ['Extracción minerales', 'Producción química', 'Papel/celulosa',
                    'Alimentos', 'Producción metal', 'Generación energía']:
            for rub in RUB_MAP[lab]:
                for rz, n in retc_reg_emp[retc_key][rub].most_common(6):
                    if rz and rz != '0':
                        empresas.add(rz)
    if cen_key:
        for p, n in cen_reg[cen_key].most_common(6):
            empresas.add(p)
    # proyectos SEIA de la region (top)
    proy_region = []
    for ind, lst in seia.items():
        for x in lst:
            if SEIA2SHORT.get((x.get('region') or '').strip()) == regc:
                proy_region.append({'industria': IND_LABEL[ind], 'proyecto': x['proyecto'][:110],
                                    'titular': x['titular'][:70], 'comuna': x['comuna'][:60],
                                    'inversion_mm_usd': fnum(x['inversion_mm'])})
    proy_region.sort(key=lambda x: -x['inversion_mm_usd'])
    plantas = [f"{p['titular']} — {p['proyecto']} ({p['comuna']})" for p in proy_region[:6] if p['titular']]
    # nº centrales CEN
    n_cen = sum(cen_reg[cen_key].values()) if cen_key else 0
    demanda_por_region.append({
        'region': regc,
        'centrales_cen': n_cen,
        'industrias': [i['industria'] for i in inds[:8]],
        'establecimientos_por_industria': inds[:8],
        'empresas': sorted(empresas)[:14],
        'plantas_principales': plantas,
        'n_proyectos_seia': len(proy_region),
        'nota': ''
    })

# notas manuales (inferencias marcadas)
NOTAS = {
 'Antofagasta': 'MEDIDO: 140 establecimientos industriales RETC (54 extracción de minerales, 39 generación), 86 centrales CEN, 57 proyectos SEIA mineros. Corazón de la gran minería del cobre (Escondida, Centinela, Antucoya) y clúster Mejillones.',
 'Atacama': 'MEDIDO: 86 establecimientos RETC (45 extracción minerales), 69 centrales CEN. Cinturón minero del hierro y cobre (Punta del Cobre, CMP, Candelaria) + generación en Cardones/Maitencillo.',
 'Tarapacá': 'MEDIDO: 32 establecimientos RETC, 21 centrales CEN. Collahuasi (proyecto SEIA US$1.700M) y operaciones de yodo/nitratos (K+S). Menor densidad industrial pero grandes cuentas puntuales.',
 'Metropolitana': 'MEDIDO: 478 establecimientos industriales RETC (83 producción química), 168 centrales CEN. Además concentra 41 de los 74 integradores del canal. Sede de fundiciones, alimentos y química de la zona central.',
 'Valparaíso': 'MEDIDO: 127 establecimientos RETC, 134 centrales CEN, 63 de combustibles. Clúster químico-industrial Quintero-Puchuncaví-Concón (GNL, refinería, termoeléctricas) + San Antonio portuario.',
 "O'Higgins": 'MEDIDO: 60 establecimientos RETC, 148 centrales CEN. Agroindustria (Agrícola Super), minería El Teniente (Codelco) y generación solar concentrada.',
 'Biobío': 'MEDIDO: 156 establecimientos RETC, 118 centrales CEN. Clúster celulosa/papel (Arauco, CMPC), siderurgia (Huachipato), refinería ENAP Talcahuano y pesqueras (Orizon, Camanchaca).',
 'Coquimbo': 'MEDIDO: 77 establecimientos RETC (34 extracción minerales), 101 centrales CEN. Minería del hierro (CMP), Los Pelambres y desalación La Serena.',
 'Araucanía': 'MEDIDO: 105 establecimientos RETC con fuerte componente pesca (42) y combustibles; menor densidad de planta de proceso. 40 centrales CEN.',
 'Los Lagos': 'MEDIDO: 587 establecimientos RETC, 495 de pesca/acualcultura (Cermaq, Mowi, Marine Harvest). Industria salmonera intensiva en proceso y frío. 59 centrales CEN.',
 'Maule': 'MEDIDO: 157 centrales CEN, 54 establecimientos RETC. Generación y agroindustria; menor base de planta de proceso.',
 'Ñuble': 'MEDIDO: 68 centrales CEN (solares), 17 establecimientos RETC. Base industrial liviana.',
 'Los Ríos': 'MEDIDO: 31 centrales CEN, 61 establecimientos RETC. Planta de celulosa Arauco Valdivia (proyecto SEIA US$1.045M) — cuenta de proceso mayor.',
 'Aysén': 'MEDIDO: 616 establecimientos RETC dominados por pesca/acualcultura (588). Sin gran planta de proceso; logística salmonera.',
 'Magallanes': 'MEDIDO: 78 establecimientos RETC, 5 centrales CEN, 13 combustibles. ENAP y proyectos de hidrógeno verde (TEC H2 MAG, ASOE Chile Diez) — futuro.',
 'Arica y Parinacota': 'MEDIDO: 27 establecimientos RETC, 11 centrales CEN. Base industrial pequeña.',
}
for d in demanda_por_region:
    d['nota'] = NOTAS.get(d['region'], 'SIN DATO')

# ---------- 5. ZONAS PRIORITARIAS (cruce medido) ----------
zonas = [
 {'zona': 'Z1 · Santiago (Las Condes–RM)', 'regiones': ['Metropolitana'],
  'demanda': 'MEDIDO: 478 establecimientos industriales RETC en la RM (83 química, 39 minería, 23 metal), 168 centrales CEN, 33 proyectos SEIA de alimentos y 27 de agua. Sede corporativa de Codelco, CMPC, Enel, Engie, Aguas Andinas, GNL y prácticamente todos los mandantes.',
  'canal': 'MEDIDO: 1.720 de 1.946 importadores del rubro (88,4%) en la RM; 514 solo en Las Condes (49,0% del volumen US$316,9M); 41 de 74 integradores en Las Condes (US$66,6M).',
  'por_que': 'Única zona donde coinciden la mayor demanda corporativa/química y TODO el canal. Es la puerta de entrada obligatoria: sin acuerdos aquí no hay distribución. Prioridad por densidad de canal (49% del mercado de importación) y por ser sede de decisión de los mandantes mineros y de proceso.',
  'prioridad': 1},
 {'zona': 'Z2 · Norte minero (Antofagasta–Mejillones–Calama)', 'regiones': ['Antofagasta'],
  'demanda': 'MEDIDO: 140 establecimientos RETC (54 extracción de minerales, 15 química, 7 metal, 39 generación), 86 centrales CEN, 57 proyectos SEIA mineros. Cuentas: Escondida, Centinela, Codelco (Radomiro Tomic, Chuquicamata), Collahuasi, SQM, Aguas de Antofagasta, E-CL/AES, GNL Mejillones.',
  'canal': 'MEDIDO: solo 24 importadores del rubro en la región de Antofagasta (1,2% del total; US$1,29M, 0,4% del volumen). El canal NO está localizado en el norte: se abastece desde Santiago.',
  'por_que': 'Máxima densidad de demanda industrial de proceso (minería + desalación + química) con canal local mínimo: la venta exige presencia propia o socio en terreno, no un distribuidor local. Alto ticket, cuenta grande, decisión técnica en faena.',
  'prioridad': 2},
 {'zona': 'Z3 · Valparaíso central (Quintero–Concón–San Antonio)', 'regiones': ['Valparaíso'],
  'demanda': 'MEDIDO: 127 establecimientos RETC (63 combustibles, 32 minería, 5 química), 134 centrales CEN, 15 proyectos SEIA de cemento y clúster Quintero-Puchuncaví (GNL Quintero US$400M, refinería ENAP, termoeléctricas).',
  'canal': 'MEDIDO: 57 importadores del rubro en la región de Valparaíso (2,9%; US$8,8M), 21 en Concón (US$5,75M, 1,8% del volumen) y 20 en Viña del Mar. Segundo polo de canal del país.',
  'por_que': 'Segunda mayor concentración de canal (Concón/Viña) Y clúster químico-energético-portuario de primera línea. Zona alcanzable en el día desde Santiago — permite cubrir demanda y canal con la misma visita.',
  'prioridad': 3},
 {'zona': 'Z4 · Concepción-Biobío (Talcahuano–Coronel–Laja)', 'regiones': ['Biobío'],
  'demanda': 'MEDIDO: 156 establecimientos RETC, 118 centrales CEN, clúster celulosa/papel (Arauco, CMPC, Forestal y Papelera Concepción), siderurgia Huachipato, refinería ENAP Talcahuano, pesqueras. 18 proyectos SEIA de celulosa/papel.',
  'canal': 'MEDIDO: 26 importadores del rubro en la región del Biobío (1,3%; US$2,26M), 6 en San Pedro de la Paz (US$1,50M). Canal local débil.',
  'por_que': 'Mayor concentración de industria de proceso continuo del sur (celulosa, acero, refinería) — el cliente natural de DCS/SIS. Canal local débil: oportunidad de ser el proveedor de referencia con un socio regional.',
  'prioridad': 4},
]
# Z5 y Z6 como zonas a vigilar
zonas.append({'zona': 'Z5 · Sur acuícola (Los Lagos–Aysén–Magallanes)', 'regiones': ['Los Lagos', 'Aysén', 'Magallanes'],
  'demanda': 'MEDIDO: 587 establecimientos RETC en Los Lagos (495 pesca/acualcultura: Cermaq, Mowi, Marine Harvest, Salmones Camanchaca) y 616 en Aysén (588 pesca). 49 proyectos SEIA de alimentos en Los Lagos. Alta densidad de plantas de proceso/frío declaradas.',
  'canal': 'MEDIDO: 29 importadores del rubro en Los Lagos (1,5%; US$1,59M), 14 en Puerto Montt. Canal mínimo.',
  'por_que': 'Alto volumen de plantas declaradas pero ticket unitario menor y dispersión geográfica extrema; requiere red de servicio local. Vigilar, no atacar en el año 1.',
  'prioridad': 5})
zonas.append({'zona': 'Z6 · Coquimbo-Atacama sur (minería de hierro y oro)', 'regiones': ['Coquimbo', 'Atacama'],
  'demanda': 'MEDIDO: Coquimbo 77 establecimientos RETC (34 minería) + 101 centrales CEN; Atacama 86 establecimientos (45 minería) + 69 centrales CEN. Cuentas: CMP, Los Pelambres, Candelaria, Punta del Cobre, Mantos Copper, Guacolda.',
  'canal': 'MEDIDO: 9 importadores en Coquimbo (0,5%; US$0,52M) y 5 en Atacama (0,3%; US$0,25M). Canal casi inexistente.',
  'por_que': 'Demanda minera real pero ticket y densidad menores que Antofagasta; se cubre como extensión de Z2 en giras. Vigilar.',
  'prioridad': 6})

# ---------- 6. HALLAZGOS ----------
hallazgos = [
 {'hallazgo': 'El canal importador del rubro está hiperconcentrado en Santiago: 1.720 de 1.946 importadores (88,4%) y US$295,4M de US$316,9M (93,2%) operan desde la Región Metropolitana.', 'tipo': 'MEDIDO', 'fuente': 'Aduanas 2025, perfiles_importador_2025.json'},
 {'hallazgo': 'Una sola comuna, Las Condes, concentra 514 importadores (26,4% del total nacional) y US$155,1M — el 49,0% de todo el volumen de importación del rubro del país.', 'tipo': 'MEDIDO', 'fuente': 'Aduanas 2025'},
 {'hallazgo': 'La demanda industrial de proceso, en cambio, NO está en Santiago: Antofagasta (140 establecimientos RETC), Biobío (156), Valparaíso (127) y Atacama (86) concentran la planta pesada, mientras el canal tiene allí apenas 24, 26, 57 y 5 importadores respectivamente.', 'tipo': 'MEDIDO', 'fuente': 'RETC/MMA + Aduanas 2025'},
 {'hallazgo': 'Existe una asimetría estructural: el decisor de compra (canal) vive en Las Condes y el usuario técnico (faena/planta) vive a 1.300 km en el norte o 500 km en el sur. Toda estrategia de canal exige cobertura de terreno separada de la sede comercial.', 'tipo': 'INFERIDO', 'fuente': 'cruce RETC/CEN/SEIA vs Aduanas'},
 {'hallazgo': 'Las 4 zonas prioritarias (Santiago, Antofagasta, Valparaíso, Biobío) reúnen 901 de los establecimientos industriales RETC identificados y 506 centrales CEN, y a la vez 1.803 de los 1.946 importadores del rubro.', 'tipo': 'MEDIDO', 'fuente': 'cálculo cruzado'},
 {'hallazgo': 'El 0% de los 74 integradores importa SUPCON o Hobré (cruce de marcas 2025): el portafolio no tiene presencia de canal instalada — el espacio está libre pero hay que construirlo desde cero.', 'tipo': 'MEDIDO', 'fuente': 'datos/cruce_catalogo_importaciones.json'},
 {'hallazgo': '47 de 74 integradores (63,5%) ya traen marcas competidoras directas (Siemens, ABB, Endress, Yokogawa...): no hay que convencerlos de la categoría, hay que desplazar la marca incumbente.', 'tipo': 'MEDIDO', 'fuente': 'datos/perfilado_74_integradores.json'},
 {'hallazgo': 'La demanda minera se concentra en proyectos SEIA de gran escala en Antofagasta (Escondida US$5.150M+US$2.351M, El Abra US$7.500M) y Tarapacá (Collahuasi US$1.700M) — cuentas de ticket alto donde SUPCON DCS compite por el proyecto completo.', 'tipo': 'MEDIDO', 'fuente': 'SEIA (seia.sea.gob.cl)'},
 {'hallazgo': 'Chile tiene 1.218 centrales eléctricas y 1.248 subestaciones coordinadas al SEN: la generación y transmisión distribuidas en todas las regiones (168 en la RM, 157 en Maule, 148 en O\'Higgins) ofrecen un mercado SCADA/telemetría geográficamente disperso.', 'tipo': 'MEDIDO', 'fuente': 'InfoTécnica CEN (api-infotecnica.coordinador.cl)'},
 {'hallazgo': 'Los mandantes de la gran minería tienen sede corporativa en Las Condes/Santiago pero operación en el norte: la intel de cuenta se construye en Santiago y la venta técnica se cierra en faena.', 'tipo': 'INFERIDO', 'fuente': 'cruce RETC (faenas en regiones) vs domicilios corporativos'},
]

out = {
 'meta': {
   'titulo': 'Mapa geográfico de oportunidades — SUPCON en Chile',
   'anio': 2025,
   'generado_por': 'CONECTA — prospección SUPCON',
   'fuentes': [
     'InfoTécnica CEN (api-infotecnica.coordinador.cl/v1) — 1.218 centrales, region/comuna/productor',
     'RETC/MMA (datosretc.mma.gob.cl) — 26.649 establecimientos industriales con region/comuna/rubro',
     'SEIA (seia.sea.gob.cl) — proyectos por industria, titular, comuna e inversion',
     'Aduanas de Chile 2025 (registro DIN, 4.847.036 lineas) — perfiles de importadores del rubro',
   ],
   'regla_datos': 'Cada cifra lleva su fuente. MEDIDO = dato directo de la fuente. INFERIDO = interpretacion del cruce, sin dato directo.',
 },
 'canal_resumen': {
   'n_importadores_rubro': canal['n_importadores_rubro'],
   'usd_rubro_2025': canal['usd_rubro_2025'],
   'pct_region_metropolitana_n': 88.4,
   'pct_region_metropolitana_usd': 93.2,
   'pct_las_condes_usd': 49.0,
 },
 'demanda_por_region': demanda_por_region,
 'canal_por_comuna': canal['canal_comuna'][:40],
 'canal_por_region': canal['canal_region'],
 'zonas_prioritarias': zonas,
 'hallazgos': hallazgos,
}
json.dump(out, open(os.path.join(BASE, 'datos/mapa_oportunidades_chile.json'), 'w'),
          ensure_ascii=False, indent=2)

print('REGIÓN           CEN  RETC_ind  SEIA  canal_n  canal_usd')
for d in demanda_por_region:
    cr = next((c for c in canal['canal_region'] if c['region'] == d['region']), None)
    nei = sum(x['establecimientos_retc'] for x in d['establecimientos_por_industria'])
    print(f"{d['region']:16s} {d['centrales_cen']:4d} {nei:8d} {d['n_proyectos_seia']:5d}  {cr['n_importadores'] if cr else 0:6d}  {cr['usd_rubro'] if cr else 0:12,.0f}")
print('\nOK -> datos/mapa_oportunidades_chile.json')
print('Zonas:', len(zonas), '| Hallazgos:', len(hallazgos), '| Comunas canal:', len(out['canal_por_comuna']))
