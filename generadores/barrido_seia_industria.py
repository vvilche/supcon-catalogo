#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Barrido SEIA por industria: proyectos con region/comuna/titular/inversion.
Fuente: seia.sea.gob.cl (buscarProyectoResumenAction.php, publico, sin auth)."""
import urllib.request, urllib.parse, json, time, os

UA = {'User-Agent': 'Mozilla/5.0'}
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get(url, data=None):
    req = urllib.request.Request(url, headers=UA)
    if data:
        req.data = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode('latin-1')

KWS = {
    'mineria': ['minera', 'cobre', 'concentradora', 'relaves'],
    'quimica': ['quimica', 'petroquimica', 'amoniaco', 'acido sulfurico'],
    'celulosa_papel': ['celulosa', 'papel', 'pulpa'],
    'alimentos': ['alimentos', 'frigorifico', 'planta de proceso de'],
    'cemento': ['cemento', 'cal ', 'clinker'],
    'generacion': ['central', 'termoelectrica', 'ciclo combinado'],
    'agua': ['desaladora', 'planta de tratamiento de agua', 'sanitario'],
    'puertos': ['puerto', 'terminal portuario', 'muelle'],
}

res = {}
for ind, kws in KWS.items():
    acc = []
    for kw in kws:
        try:
            d = json.loads(get('https://seia.sea.gob.cl/busqueda/buscarProyectoResumenAction.php',
                {'nombre': kw, 'titular': '', 'folio': '', 'tipoPresentacion': 'Ambos',
                 'offset': '1', 'limit': '60'}))
        except Exception as e:
            print('ERR', ind, kw, e); continue
        rr = d.get('data', d.get('proyectos', [])) if isinstance(d, dict) else d
        if not isinstance(rr, list):
            rr = []
        for x in rr:
            acc.append({
                'proyecto': (x.get('EXPEDIENTE_NOMBRE') or '').strip(),
                'titular': (x.get('TITULAR') or '').strip(),
                'region': (x.get('REGION_NOMBRE') or '').strip(),
                'comuna': (x.get('COMUNA_NOMBRE') or '').strip(),
                'inversion_mm': x.get('INVERSION_MM'),
                'tipo': (x.get('WORKFLOW_DESCRIPCION') or '').strip(),
            })
        time.sleep(0.4)
    # dedupe por (proyecto, titular)
    seen = set(); ded = []
    for x in acc:
        k = (x['proyecto'].lower(), x['titular'].lower())
        if k in seen:
            continue
        seen.add(k); ded.append(x)
    res[ind] = ded
    print(f'{ind:16s} -> {len(ded)} proyectos (post-dedupe)')

json.dump(res, open(os.path.join(BASE, 'datos/_seia_por_industria.json'), 'w'),
          ensure_ascii=False, indent=2)
print('-> datos/_seia_por_industria.json')
