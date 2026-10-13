#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MAPA DE CANAL — distribucion geografica de los 1.946 importadores del rubro
automatizacion/instrumentacion (Aduanas 2025). Fuente: datos/perfiles_importador_2025.json"""
import json, os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'datos/perfiles_importador_2025.json')))
P = d['perfiles']

COMUNA = {
 '13114':'Las Condes','13123':'Santiago Centro','13101':'Santiago','13119':'Providencia',
 '13122':'Vitacura','13115':'Lo Barnechea','13110':'Nunoa','13124':'Quinta Normal','13126':'Pudahuel',
 '13120':'Macul','13104':'Conchali','13111':'Quilicura','13109':'Renca','13125':'Cerro Navia',
 '13108':'Estacion Central','13116':'Maipu','13105':'La Cisterna','13107':'Lo Prado',
 '13103':'Conchali','13102':'Cerro Navia','13121':'La Reina','13118':'San Joaquin','13106':'San Miguel',
 '13112':'Recoleta','13113':'Independencia','13301':'Puente Alto','13302':'San Bernardo',
 '05101':'Valparaiso','05109':'Vina del Mar','08101':'Concepcion','08110':'San Pedro de la Paz',
 '02101':'Antofagasta','03301':'Copiapo','04101':'La Serena','04301':'Coquimbo','06301':'Rancagua',
 '06310':'San Fernando','07101':'Talca','07301':'Cauquenes','09101':'Temuco','10101':'Puerto Montt',
 '01101':'Iquique','12201':'Punta Arenas','05701':'San Antonio','05501':'Quillota','02102':'Mejillones',
 '13117':'La Florida','13127':'La Pintana','13128':'Lo Espejo','13129':'La Granja','13130':'San Ramon',
 '13131':'Pedro Aguirre Cerda','13132':'El Bosque','13303':'San Ramon','13401':'San Bernardo',
 '13501':'Pudahuel','13403':'Colina','13404':'Lampa','13604':'Talagante','13605':'Penalflor',
 '13201':'San Jose de Maipo','05102':'Casablanca','05103':'Concon','05105':'Puchuncavi','05107':'Quilpue',
 '05108':'Quillota','05301':'San Antonio','05503':'La Calera','05801':'Los Andes','05802':'San Felipe',
 '06101':'Rancagua','06106':'Machali','06110':'San Fernando','07304':'Curico','07401':'Talca',
 '09108':'Villarrica','09119':'Pucon','10109':'Castro','10107':'Ancud','10201':'Osorno',
 '10203':'Puerto Varas','1101':'Iquique','1107':'Alto Hospicio','12101':'Punta Arenas',
 '16101':'Chillan','16105':'San Carlos','16301':'Los Angeles','2101':'Antofagasta','2102':'Mejillones',
 '2104':'Taltal','3101':'Copiapo','4101':'La Serena','4102':'Coquimbo','5101':'Valparaiso',
 '5102':'Casablanca','5103':'Concon','5109':'Vina del Mar','5301':'San Antonio','5503':'La Calera',
 '5801':'Los Andes','5802':'San Felipe','6101':'Rancagua','6106':'Machali','6110':'San Fernando',
 '6301':'Rancagua','7301':'Cauquenes','7304':'Curico','7401':'Talca','8101':'Concepcion',
 '8102':'Coronel','8103':'Chiguayante','8107':'Talcahuano','8108':'Hualpen','8110':'San Pedro de la Paz',
 '8301':'Los Angeles','9101':'Temuco','9108':'Villarrica','9119':'Pucon',
}
REGC = {'01':'Tarapaca','02':'Antofagasta','03':'Atacama','04':'Coquimbo','05':'Valparaiso',
 '06':"O'Higgins",'07':'Maule','08':'Biobio','09':'Araucania','10':'Los Lagos','11':'Aysen',
 '12':'Magallanes','13':'Metropolitana','14':'Los Rios','15':'Arica y Parinacota','16':'Nuble'}
def region(c):
    c = (c or '').strip().zfill(5)
    return REGC.get(c[:2], 'cod.'+c[:2])
def nom(c):
    return COMUNA.get(c, 'cod.'+str(c))

cm = defaultdict(lambda: [0, 0.0])
rg = defaultdict(lambda: [0, 0.0])
for p in P:
    c = p.get('comuna')
    if not c:
        continue
    cm[c][0] += 1; cm[c][1] += p.get('instru_usd', 0)
    r = region(c); rg[r][0] += 1; rg[r][1] += p.get('instru_usd', 0)

TOT_N = sum(v[0] for v in rg.values())
TOT_U = sum(v[1] for v in rg.values())

REG_ACC = {'Valparaiso': 'Valparaíso', 'Biobio': 'Biobío', 'Araucania': 'Araucanía',
           'Tarapaca': 'Tarapacá', 'Nuble': 'Ñuble', 'Los Rios': 'Los Ríos',
           'Aysen': 'Aysén'}
canal_region = [{'region': REG_ACC.get(r, r), 'n_importadores': rg[r][0], 'usd_rubro': round(rg[r][1], 2),
                 'pct_n': round(rg[r][0]/TOT_N*100, 1), 'pct_usd': round(rg[r][1]/TOT_U*100, 1)}
                for r in sorted(rg, key=lambda x: -rg[x][1])]
canal_comuna = [{'comuna': nom(c), 'codigo': c, 'region': region(c), 'n_importadores': cm[c][0],
                 'usd_rubro': round(cm[c][1], 2), 'pct': round(cm[c][1]/TOT_U*100, 1)}
                for c in sorted(cm, key=lambda x: -cm[x][1])]

print('=== CANAL 1.946 importadores del rubro por REGION ===')
print(f'TOTAL n={TOT_N} usd={TOT_U:,.0f}')
for x in canal_region:
    print(f"{x['region']:16s} n={x['n_importadores']:4d} ({x['pct_n']:4.1f}%)  usd={x['usd_rubro']:14,.0f} ({x['pct_usd']:4.1f}%)")
print()
print('=== CANAL TOP 25 comunas ===')
for x in canal_comuna[:25]:
    print(f"{x['comuna']:20s} ({x['codigo']}) {x['region']:14s} n={x['n_importadores']:4d} usd={x['usd_rubro']:14,.0f} {x['pct']:5.1f}%")

out = {'fuente': 'Registro DIN de Importaciones, Aduanas de Chile 2025 (4.847.036 lineas). Rubro automatizacion/instrumentacion.',
       'n_importadores_rubro': TOT_N, 'usd_rubro_2025': round(TOT_U, 2),
       'canal_region': canal_region, 'canal_comuna': canal_comuna}
json.dump(out, open(os.path.join(BASE, 'datos/_canal_geo.json'), 'w'), ensure_ascii=False, indent=2)
print('\n-> datos/_canal_geo.json')
