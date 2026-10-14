#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera artefactos/plan_accion.html — LA LISTA DE LLAMADOS.

Diseñado para ACCIONAR, no para leer: por empresa, quién atender, a qué número, qué ofrecerle
y el primer guion. Con botón de copiar el guion.
"""
import os, json, html

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
OUT = os.path.join(BASE, "artefactos", "plan_accion.html")

d = json.load(open(os.path.join(D, "plan_accion.json"), encoding="utf-8"))
P, T = d["plan"], d["totales"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


def n(v, dec=0):
    try:
        return f"{v:,.{dec}f}"
    except Exception:
        return "—"


def guion(p, c):
    """Primera frase, armada con el dato REAL de esa empresa."""
    partes = []
    if p["usd_cotizado"]:
        partes.append(f"ya les cotizamos US${n(p['usd_cotizado'])} en 2023-2025")
    if p["dolor_t"]:
        partes.append(f"tienen {n(p['dolor_t'],0)} toneladas de residuos peligrosos declarados al RETC")
    dato = ("; ".join(partes)) if partes else "están en el mapa de cuentas"
    return (f"Hola, llamo de CONECTA por {p['empresa']}. "
            f"Sé que {dato}. "
            f"Busco a {c['nombre']}, {c['cargo']}, para ver si les sirve "
            f"{c['que_ofrecer']}.")


bloques = ""
for i, p in enumerate(P, 1):
    # cabecera de la ficha
    tel = (f'<span class="tel">{esc(p["telefono_central"])}</span>'
           if p["telefono_central"] else '<span class="notel">sin teléfono: entrar por LinkedIn</span>')
    monto = (f'US${n(p["usd_cotizado"])} cotizado · US${n(p["usd_ganado"])} ganado · {p["n_oc"]} OC'
             if p["usd_cotizado"] else "nunca cotizado")
    dolor = f'{n(p["dolor_t"],0)} t residuos peligrosos' if p["dolor_t"] else "sin dolor declarado"
    lin = " · ".join(p["lineas_empresa"]) if p["lineas_empresa"] else "línea por definir"

    contactos = ""
    for c in p["contactos"]:
        li = (f'<a href="{esc(c["linkedin"])}" target="_blank">LinkedIn</a>'
              if c["linkedin"] else '<span class="gris">sin perfil</span>')
        g = guion(p, c)
        contactos += f'''
        <tr>
          <td><b>{esc(c["nombre"])}</b><span class="sub">{esc(c["cargo"])}</span></td>
          <td><span class="ofr">{esc(c["linea"])}</span><span class="sub">{esc(c["que_ofrecer"])}</span></td>
          <td>{li}</td>
          <td class="guion" data-g="{esc(g)}">
            <button class="copy" onclick="copiar(this)">copiar guion</button>
            <span class="gtxt">{esc(g[:74])}…</span>
          </td>
        </tr>'''

    bloques += f'''
    <div class="ficha">
      <div class="fh">
        <span class="idx">{i}</span>
        <span class="emp"><b>{esc(p["empresa"])}</b>
          {f'<span class="sig">{esc(p["sigla"])}</span>' if p["sigla"] else ''}
          {f'<span class="tipo">{esc(p["tipo_empresa"])}</span>' if p["tipo_empresa"] else ''}</span>
        <span class="via">{esc(p["via"])}</span>
        <span class="num">{tel}</span>
      </div>
      <div class="fd">
        <span class="dato"><span class="lb">Dinero</span> {esc(monto)}</span>
        <span class="dato"><span class="lb">Dolor</span> {esc(dolor)}</span>
        <span class="dato"><span class="lb">Línea</span> {esc(lin)}</span>
      </div>
      <table>{contactos}</table>
    </div>'''

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Plan de acción · a quién llamar</title><style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f7f8fa;--cd:#fff;--bd:#e5e7eb;--tx:#111827;--mu:#6b7280;--ac:#1d4ed8;--vd:#047857}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14.5px;line-height:1.6;padding:24px 16px 70px}}
.wrap{{max-width:1240px;margin:0 auto}}
h1{{font-size:26px;font-weight:680;letter-spacing:-.4px;margin-bottom:5px}}
.sub0{{color:var(--mu);font-size:14px;margin-bottom:16px;max-width:960px}}
.kpis{{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:16px}}
.kpis div{{background:var(--cd);border:1px solid var(--bd);border-radius:10px;padding:10px 15px;font-size:12px;color:var(--mu)}}
.kpis b{{display:block;font-size:20px;font-weight:700;color:var(--tx)}}
.aviso{{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid #b45309;border-radius:9px;padding:12px 16px;margin:14px 0;font-size:13.5px}}
.aviso b{{color:#92400e}}
.ficha{{background:var(--cd);border:1px solid var(--bd);border-radius:12px;padding:13px 16px;margin-bottom:10px}}
.fh{{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:6px}}
.idx{{font-size:11px;font-weight:700;color:var(--mu);background:#f3f4f6;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}}
.emp b{{font-size:15.5px}}
.sig{{font-size:10.5px;background:#eef2ff;color:#3730a3;border-radius:4px;padding:1px 7px;margin-left:6px;font-weight:700}}
.tipo{{font-size:10.5px;background:#f0fdf4;color:#065f46;border-radius:4px;padding:1px 6px;margin-left:5px}}
.via{{font-size:11.5px;color:var(--mu);margin-left:auto}}
.tel{{font-family:ui-monospace,Menlo,monospace;font-size:13.5px;font-weight:700;color:var(--vd);background:#f0fdf4;border-radius:6px;padding:2px 10px}}
.notel{{font-size:12px;color:#b45309;background:#fffbeb;border-radius:6px;padding:2px 9px}}
.fd{{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:#374151;padding:6px 0;border-bottom:1px solid #f3f4f6;margin-bottom:6px}}
.lb{{font-size:10px;text-transform:uppercase;letter-spacing:.4px;color:var(--mu);font-weight:700;margin-right:5px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
td{{padding:6px 7px;border-bottom:1px solid #f9fafb;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
.sub{{display:block;font-size:11.5px;color:var(--mu);margin-top:1px}}
.ofr{{display:inline-block;font-size:11.5px;background:#eff6ff;color:#1e40af;border-radius:5px;padding:2px 8px;font-weight:600}}
.guion{{position:relative}}
.copy{{font-size:10.5px;background:#1d4ed8;color:#fff;border:none;border-radius:5px;padding:3px 9px;cursor:pointer;font-weight:600;margin-bottom:3px}}
.copy:hover{{background:#1e40af}}
.gtxt{{display:block;font-size:11.5px;color:var(--mu);font-style:italic}}
.gris{{color:var(--mu);font-style:italic;font-size:12px}}
a{{color:var(--ac);text-decoration:none;font-size:12.5px}} a:hover{{text-decoration:underline}}
footer{{margin-top:26px;padding-top:14px;border-top:1px solid var(--bd);font-size:12.5px;color:var(--mu)}}
footer a{{color:var(--ac)}}
</style></head><body><div class="wrap">

<h1>Plan de acción: a quién llamar</h1>
<p class="sub0">La lista de contacto, en orden de valor. Por empresa: <b>a qué número llamar</b>,
<b>quién atender</b>, <b>qué ofrecerle</b> (la línea SUPCON que corresponde a su cargo) y un
<b>guion de primera frase</b> con el dato real de esa empresa. Botón para copiarlo.</p>

<div class="kpis">
  <div><b>{T['empresas']}</b>empresas</div>
  <div><b>{T['contactos']}</b>personas a contactar</div>
  <div><b>{T['con_telefono']}</b>con teléfono de central</div>
  <div><b>{sum(1 for p in P for c in p['contactos'] if c['linkedin'])}</b>con LinkedIn</div>
</div>

<div class="aviso">
  <b>Cómo usarlo, y qué es cada dato:</b>
  <ul style="margin:6px 0 0 18px">
    <li><b>El teléfono es del conmutador de la empresa</b>, no el celular de la persona. Hay que
    pedirla <b>por nombre y cargo</b> — así se llega.</li>
    <li><b>El nombre, el cargo y el LinkedIn tienen fuente</b> (Direcmin, transparencia por ley,
    o el headline del propio perfil).</li>
    <li><b>Donde no hay teléfono</b>, la vía es LinkedIn: el perfil está verificado.</li>
    <li>El <b>guion</b> usa el dato medido de esa empresa: sirve para que no te confundan con un
    vendedor genérico.</li>
  </ul>
</div>

{bloques}

<footer>
  Fuentes: Direcmin · Transparencia Ley 20.285 · LinkedIn · RETC MMA · eCRM INECO ·
  <a href="cliente_producto_persona.html">vista empresa→producto→persona</a> ·
  <a href="buscador_decisores.html">buscador de decisores</a> ·
  <a href="../index.html">catálogo</a>.
</footer>
</div>
<script>
function copiar(b){{
  const g = b.parentElement.getAttribute('data-g');
  navigator.clipboard.writeText(g).then(()=>{{
    const t=b.textContent; b.textContent='copiado'; b.style.background='#047857';
    setTimeout(()=>{{b.textContent=t; b.style.background='#1d4ed8';}}, 1200);
  }});
}}
</script>
</body></html>'''

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"escrito: {OUT} ({len(HTML.encode()):,} bytes)")
print(f"  {len(P)} empresas | {T['contactos']} contactos | {T['con_telefono']} con teléfono")
