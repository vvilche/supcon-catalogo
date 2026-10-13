# -*- coding: utf-8 -*-
"""
Genera artefactos/estrategia_normativa.html desde datos/cruce_normativo_estrategia.json.

Estilo del repo: tema claro, bg #f8fafc, accent #2563eb, SIN rojos (#dc2626/#ef4444).
Tildes correctas.
"""
import json, os, html

BASE = "/Users/victorvilche/Documents/ConocimientoSupcon/supcon-catalogo"
DATA = os.path.join(BASE, "datos", "cruce_normativo_estrategia.json")
OUT = os.path.join(BASE, "artefactos", "estrategia_normativa.html")

d = json.load(open(DATA, encoding="utf-8"))
lineas = d["lineas"]
meta = d["meta"]
hallazgos = d["hallazgos"]
merc = d["mercado_medido"]

ORDEN_LINEAS = ["Instrumentación", "Analítica", "Válvulas", "DCS", "PLC", "SIS", "Software y plataforma"]

URG = {"alta": ("u-alta", "Urgencia alta"), "media": ("u-media", "Urgencia media"), "baja": ("u-baja", "Urgencia baja")}
TIPO = {
    "obligatoria": ("t-obl", "Obligatoria"),
    "incentivada": ("t-inc", "Incentivada"),
    "voluntaria": ("t-vol", "Voluntaria"),
}


def esc(s):
    return html.escape(str(s), quote=True)


def list_items(items):
    return "".join(f"<li>{esc(x)}</li>" for x in items)


parts = []
parts.append("<!DOCTYPE html><html lang=\"es\"><head><meta charset=\"utf-8\">")
parts.append("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
parts.append("<title>Estrategia normativa — SUPCON en Chile</title><style>")
parts.append("""
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f8fafc;--cd:#fff;--bd:#e2e8f0;--tx:#0f172a;--mu:#64748b;--ac:#2563eb;--acs:#eff6ff;--am:#d97706;--ams:#fffbeb;--ok:#047857;--oks:#ecfdf5}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:15px;line-height:1.62;padding:28px 20px 80px}
.wrap{max-width:1040px;margin:0 auto}
h1{font-size:27px;font-weight:680;letter-spacing:-.5px;margin-bottom:6px}
.sub{color:var(--mu);font-size:14.5px;margin-bottom:8px;max-width:880px}
h2{font-size:20px;font-weight:660;margin:38px 0 10px;letter-spacing:-.2px}
h3{font-size:16.5px;font-weight:650;margin:0 0 7px}
h4{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);margin:0 0 7px}
p{margin-bottom:11px}
ul{list-style:none;margin:9px 0 12px}
ul li{position:relative;padding-left:17px;margin-bottom:6px}
ul li:before{content:"";position:absolute;left:4px;top:9px;width:5px;height:5px;border-radius:50%;background:var(--ac)}
code{background:#f1f5f9;padding:1px 6px;border-radius:4px;font-size:12.5px;font-family:ui-monospace,monospace}
table{width:100%;border-collapse:collapse;margin:13px 0;font-size:13.5px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--bd)}
td{padding:9px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top}
tr:last-child td{border-bottom:none}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.box{background:var(--cd);border:1px solid var(--bd);border-radius:11px;padding:15px 18px;margin:14px 0}
.aviso{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid var(--am);border-radius:9px;padding:14px 17px;margin:15px 0;font-size:14px}
.aviso b{color:#92400e}
.ok{background:var(--oks);border:1px solid #a7f3d0;border-left:4px solid var(--ok);border-radius:9px;padding:14px 17px;margin:15px 0;font-size:14px}
.ok b{color:var(--ok)}
.info{background:var(--acs);border:1px solid #bfdbfe;border-left:4px solid var(--ac);border-radius:9px;padding:14px 17px;margin:15px 0;font-size:14px}
.info b{color:var(--ac)}
.card{background:var(--cd);border:1px solid var(--bd);border-radius:14px;padding:18px 21px;margin-bottom:15px;border-left:4px solid var(--ac)}
.card.sin{border-left-color:#94a3b8}
.ch{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;margin-bottom:9px}
.et{font-size:11px;border-radius:5px;padding:2px 9px;font-weight:700;text-transform:uppercase;letter-spacing:.3px}
.t-obl{background:#eff6ff;color:var(--ac)}
.t-inc{background:var(--ams);color:var(--am)}
.t-vol{background:#f1f5f9;color:#475569}
.u-alta{background:var(--oks);color:var(--ok)}
.u-media{background:var(--ams);color:var(--am)}
.u-baja{background:#f1f5f9;color:#475569}
.disparador{font-size:14.5px;margin:8px 0 12px}
.fuente{font-size:12px;color:var(--mu);word-break:break-word;margin-top:4px}
.fuente a{color:var(--ac);text-decoration:none}
.dos{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:11px}
@media(max-width:760px){.dos{grid-template-columns:1fr}}
.nota{background:#f8fafc;border:1px dashed var(--bd);border-radius:9px;padding:12px 15px;font-size:13.5px;margin-top:11px}
.nota .med{color:var(--ok);font-weight:700}
.nota .inf{color:var(--am);font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.chip{background:#f1f5f9;border:1px solid var(--bd);border-radius:100px;padding:2px 11px;font-size:12.5px}
.hall{background:var(--cd);border:1px solid var(--bd);border-radius:13px;padding:16px 19px;margin-bottom:13px}
.hall .tag{font-size:10.5px;border-radius:5px;padding:2px 8px;font-weight:700;text-transform:uppercase;letter-spacing:.3px;background:#eff6ff;color:var(--ac)}
.hall .tag.sin{background:var(--ams);color:var(--am)}
.hall h3{font-size:15.5px;margin:7px 0}
.hall .src{font-size:12.5px;color:var(--mu);margin-top:5px}
.hall .uso{font-size:13.5px;margin-top:7px;padding-top:7px;border-top:1px solid #f1f5f9}
.hall .uso b{color:var(--ac)}
.pie{margin-top:40px;padding-top:18px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
@media(max-width:760px){.kpi{grid-template-columns:repeat(2,1fr)}}
.kpi .k{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:13px 15px}
.kpi .k .v{font-size:22px;font-weight:700;letter-spacing:-.5px}
.kpi .k .l{font-size:11.5px;color:var(--mu);text-transform:uppercase;letter-spacing:.3px;margin-top:2px}
""")
parts.append("</style></head><body><div class=\"wrap\">")

parts.append("<h1>Estrategia normativa — el disparador que empuja cada línea SUPCON en Chile</h1>")
parts.append(
    "<p class=\"sub\">Cruce de las <b>7 líneas</b> del catálogo SUPCON (63 productos) con el dolor "
    "regulatorio chileno: para cada línea, la norma que obliga o incentiva la compra, las industrias "
    "afectadas y las empresas concretas obligadas. Tercer ángulo de la estrategia, junto a la "
    "escalera al éxito (dificultad por producto) y la estrategia de penetración (escalones).</p>"
)
parts.append(
    "<div class=\"info\"><b>El principio.</b> Un cliente no compra un analizador porque sea bueno: lo "
    "compra porque una norma lo obliga o porque una multa se lo hizo urgente. Este cruce busca ese "
    "disparador para cada línea. Donde no existe, se dice — no se inventa.</div>"
)

# KPIs
n_con = meta["n_lineas_con_sustento"]
n_sin = meta["n_lineas_sin_sustento"]
parts.append("<div class=\"kpi\">")
parts.append(f"<div class=\"k\"><div class=\"v\">{len(ORDEN_LINEAS)}</div><div class=\"l\">Líneas cruzadas</div></div>")
parts.append(f"<div class=\"k\"><div class=\"v\">{n_con}</div><div class=\"l\">Con disparador verificado</div></div>")
parts.append(f"<div class=\"k\"><div class=\"v\">{n_sin}</div><div class=\"l\">Sin disparador propio</div></div>")
parts.append(f"<div class=\"k\"><div class=\"v\">{len(meta['fuentes_normativas'])}</div><div class=\"l\">Normas con fuente</div></div>")
parts.append("</div>")

# El disparador por línea
parts.append("<h2>El disparador normativo, línea por línea</h2>")
for nombre in ORDEN_LINEAS:
    L = lineas[nombre]
    tipo_cls, tipo_lbl = TIPO.get(L["tipo_obligacion"], ("t-vol", L["tipo_obligacion"]))
    urg_cls, urg_lbl = URG.get(L["urgencia"], ("u-baja", L["urgencia"]))
    sin = nombre == "PLC"
    parts.append(f"<div class=\"card{' sin' if sin else ''}\">")
    parts.append("<div class=\"ch\">")
    parts.append(f"<h3>{esc(nombre)}</h3>")
    parts.append(f"<span class=\"et {tipo_cls}\">{esc(tipo_lbl)}</span>")
    parts.append(f"<span class=\"et {urg_cls}\">{esc(urg_lbl)}</span>")
    parts.append("</div>")
    parts.append(f"<div class=\"disparador\">{esc(L['disparador_normativo'])}</div>")
    parts.append(f"<div class=\"fuente\"><b>Norma y fuente:</b> {esc(L['norma_y_fuente'])}</div>")
    parts.append("<div class=\"dos\">")
    parts.append("<div><h4>Industrias afectadas</h4><ul>" + list_items(L["industrias_afectadas"]) + "</ul></div>")
    parts.append("<div><h4>Empresas candidatas</h4><div class=\"chips\">" +
                 "".join(f"<span class=\"chip\">{esc(x)}</span>" for x in L["empresas_candidatas"]) + "</div></div>")
    parts.append("</div>")
    nota = esc(L["nota"])
    nota = nota.replace("MEDIDO:", "<span class=\"med\">MEDIDO:</span>")
    nota = nota.replace("INFERIDO:", "<span class=\"inf\">INFERIDO:</span>")
    nota = nota.replace("CONCLUSION:", "<b>CONCLUSIÓN:</b>")
    nota = nota.replace("CONCLUSIÓN:", "<b>CONCLUSIÓN:</b>")
    nota = nota.replace("SIN SUSTENTO:", "<b>SIN SUSTENTO:</b>")
    parts.append(f"<div class=\"nota\">{nota}</div>")
    parts.append("</div>")

# Hallazgos
parts.append("<h2>Lo que revela el cruce</h2>")
for h in hallazgos:
    is_sin = "SIN SUSTENTO" in h["tipo"]
    parts.append("<div class=\"hall\">")
    parts.append(f"<span class=\"tag{' sin' if is_sin else ''}\">{esc(h['tipo'])}</span>")
    parts.append(f"<h3>{esc(h['hallazgo'])}</h3>")
    parts.append(f"<div class=\"src\"><b>Sustento:</b> {esc(h['sustento'])}</div>")
    parts.append(f"<div class=\"uso\"><b>Uso comercial:</b> {esc(h['uso_comercial'])}</div>")
    parts.append("</div>")

# Mercado medido
parts.append("<h2>El mercado, medido (no de memoria)</h2>")
parts.append(f"<p>{esc(merc['fuente'])}.</p>")
parts.append("<table>")
parts.append("<tr><th>Línea / familia de producto</th><th class=\"num\">Importado 2025 (US$)</th></tr>")
for k, v in merc["por_linea_usd"].items():
    parts.append(f"<tr><td>{esc(k)}</td><td class=\"num\">{v:,.0f}</td></tr>".replace(",", "."))
parts.append("</table>")
canal = merc["canal"]
parts.append("<div class=\"ok\"><b>El canal.</b> ")
parts.append(f"{canal['integradores_tecnicos']} integradores técnicos mueven "
             f"US${canal['volumen_canal_usd']:,.0f} al año. ".replace(",", "."))
parts.append(f"{canal['pct_las_condes']}% despacha desde Las Condes; "
             f"{canal['pct_con_marca_competidora']}% ya trae marca competidora; "
             f"<b>{canal['integradores_con_supcon']} traen SUPCON</b>. ")
parts.append(f"Base instalada SUPCON/Hobré: <b>{esc(merc['base_instalada_supcon_hobre'])}</b>. ")
parts.append("Sin base instalada que defender, el disparador normativo es lo único que hay que llevar a la reunión.</div>")

# Cómo se lee
parts.append("<h2>Cómo se lee este cruce</h2>")
parts.append(
    "<div class=\"box\"><p><b>1. El disparador ordena la conversación, no la reemplaza.</b> La norma "
    "abre la puerta (te obligan a un resultado y a demostrarlo); el producto la cierra con la "
    "especificación. Nunca prometer que 'la norma exige' el equipo exacto cuando lo que exige es la "
    "función o el resultado.</p>"
    "<p><b>2. Lo obligatorio va primero.</b> Analítica (CEMS, obligación de resultado + reporte en "
    "línea con la SMA), Instrumentación (caudal, la variable que más fiscalizadores exigen) y "
    "Software/plataforma (Ley 21.663 sobre 147 OIV eléctricos y Ley 21.305 sobre CCGE) son las "
    "líneas donde el disparador es verificable y la lista de obligados existe.</p>"
    "<p><b>3. Lo que no tiene disparador se declara.</b> El PLC no tiene norma que lo obligue por "
    "nombre: se vende por obsolescencia o dentro de una solución mayor. El DCS y las válvulas tienen "
    "disparador de resultado o de seguridad, no ambiental. Decirlo así evita el error que corrige el "
    "jefe de instrumentación en la reunión.</p></div>"
)

# Pie
parts.append("<div class=\"pie\">")
parts.append(f"<b>Verificación:</b> {esc(d['verificacion']['metodo'])}<br>")
parts.append(f"<b>Advertencia:</b> {esc(d['verificacion']['advertencia'])}<br>")
parts.append("Generado por <code>generadores/cruce_normativo.py</code> desde <code>datos/cruce_normativo_estrategia.json</code>. ")
parts.append("Mercado: Registro DIN de Aduanas Chile 2025. Normativa: bcn.cl/leychile, SMA, CNE, SEC, MINSAL, ANCI.")
parts.append("</div>")

parts.append("</div></body></html>")

html_out = "".join(parts)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_out)

# Verificación de nodos
import re
n_cards = html_out.count("<div class=\"card")
n_hall = html_out.count("<div class=\"hall\"")
n_li = html_out.count("<li>")
print("OK ->", OUT, len(html_out), "bytes")
print("cards:", n_cards, "| hallazgos:", n_hall, "| <li>:", n_li)
print("rojo presente:", ("#dc2626" in html_out) or ("#ef4444" in html_out))
print("tildes ok:", "Instrumentación" in html_out, "| Analítica" in html_out)
