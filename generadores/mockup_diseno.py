#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOCKUP de diseno (no producto final).
Muestra el layout que tendria la matriz de analizadores SUPCON/Hobre.
Datos de ejemplo estaticos: solo para validar el DISENO con Victor.
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mockup_diseno.html")

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MOCKUP - Matriz Analizadores SUPCON / Hobre</title>
<style>
  :root{
    --bg:#f8fafc; --card:#ffffff; --border:#e2e8f0; --txt:#0f172a;
    --muted:#64748b; --accent:#2563eb; --accent-soft:#eff6ff; --amber:#d97706;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--txt);font-family:Inter,-apple-system,sans-serif;
       font-size:15px;line-height:1.55;padding:32px 28px 80px}
  .wrap{max-width:1240px;margin:0 auto}

  /* ---------- MOCKUP BANNER ---------- */
  .mock{background:#fffbeb;border:1px dashed var(--amber);color:#92400e;
        border-radius:12px;padding:10px 14px;font-size:13px;margin-bottom:22px}

  /* ---------- HERO ---------- */
  .hero{background:var(--card);border:1px solid var(--border);border-radius:20px;
        padding:28px 30px;margin-bottom:20px}
  .hero h1{font-size:26px;font-weight:650;letter-spacing:-.4px;margin-bottom:6px}
  .hero p{color:var(--muted);font-size:14.5px;max-width:820px}
  .stats{display:flex;gap:34px;margin-top:22px;padding-top:20px;border-top:1px solid var(--border)}
  .stat b{display:block;font-size:27px;font-weight:650;font-family:"IBM Plex Mono",monospace}
  .stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px}

  /* ---------- FILTROS ---------- */
  .filtros{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;align-items:center}
  .chip{border:1px solid var(--border);background:var(--card);border-radius:100px;
        padding:7px 16px;font-size:13.5px;cursor:pointer;color:var(--muted)}
  .chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
  .search{border:1px solid var(--border);border-radius:100px;padding:8px 16px;
          font-size:13.5px;font-family:inherit;min-width:230px}

  /* ---------- BLOQUE FAMILIA ---------- */
  .fam{margin-bottom:30px}
  .fam-h{display:flex;align-items:baseline;gap:12px;margin-bottom:5px}
  .fam-h h2{font-size:18px;font-weight:620}
  .fam-h .org{font-size:11.5px;background:var(--accent-soft);color:var(--accent);
              border-radius:100px;padding:3px 11px;font-weight:550}
  .fam-n{color:var(--muted);font-size:13.5px;margin-bottom:14px}

  /* ---------- TARJETA PRODUCTO ---------- */
  details.prod{background:var(--card);border:1px solid var(--border);border-radius:20px;
               margin-bottom:11px;overflow:hidden}
  details.prod[open]{border-color:#cbd5e1}
  summary.p-sum{padding:17px 22px;cursor:pointer;display:flex;align-items:center;
                gap:14px;list-style:none}
  summary.p-sum::-webkit-details-marker{display:none}
  .p-name{font-size:16px;font-weight:620;min-width:150px}
  .p-rol{color:var(--muted);font-size:13.5px;flex:1}
  .p-badge{font-size:11px;border:1px solid var(--border);border-radius:100px;
           padding:3px 10px;color:var(--muted);white-space:nowrap}
  .caret{color:var(--muted);font-size:12px;transition:transform .15s}
  details[open] .caret{transform:rotate(90deg)}

  .p-body{padding:0 22px 22px;border-top:1px solid var(--border)}
  .p-body h4{font-size:12px;text-transform:uppercase;letter-spacing:.6px;
             color:var(--muted);margin:18px 0 9px;font-weight:600}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1px;
        background:var(--border);border:1px solid var(--border);border-radius:12px;overflow:hidden}
  .kv{background:var(--card);padding:10px 13px}
  .kv .k{font-size:11.5px;color:var(--muted);margin-bottom:2px}
  .kv .v{font-size:13.5px;font-family:"IBM Plex Mono",monospace}
  .tags{display:flex;flex-wrap:wrap;gap:7px}
  .tag{background:var(--accent-soft);color:#1e40af;border-radius:100px;
       padding:4px 12px;font-size:12.5px}
  .fuente{margin-top:16px;font-size:11.5px;color:var(--muted);font-family:"IBM Plex Mono",monospace}
  .aviso{background:#fffbeb;border-left:3px solid var(--amber);border-radius:8px;
         padding:10px 13px;font-size:13px;color:#92400e;margin-top:14px}

  /* ---------- TABLA MAESTRA ---------- */
  .tblwrap{background:var(--card);border:1px solid var(--border);border-radius:20px;
           padding:22px;margin-top:34px;overflow-x:auto}
  .tblwrap h2{font-size:18px;font-weight:620;margin-bottom:14px}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.5px;
     color:var(--muted);padding:9px 11px;border-bottom:1px solid var(--border);font-weight:600;
     white-space:nowrap}
  td{padding:10px 11px;border-bottom:1px solid #f1f5f9;vertical-align:top}
  td.n{font-family:"IBM Plex Mono",monospace;font-size:12px}
  tr:last-child td{border-bottom:none}

  /* ---------- ANGULO CONECTA ---------- */
  .angulo{background:var(--card);border:1px solid var(--border);border-radius:20px;
          padding:22px;margin-top:34px}
  .angulo h2{font-size:18px;font-weight:620;margin-bottom:4px}
  .angulo > p{color:var(--muted);font-size:13.5px;margin-bottom:16px}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
  .c{background:var(--bg);border:1px solid var(--border);border-radius:14px;padding:15px}
  .c h5{font-size:13.5px;font-weight:600;margin-bottom:5px}
  .c p{font-size:12.5px;color:var(--muted)}
  .c .prod-n{font-size:12px;color:var(--accent);font-weight:600;margin-bottom:7px;
             font-family:"IBM Plex Mono",monospace}
</style>
</head>
<body>
<div class="wrap">

  <div class="mock"><b>MOCKUP DE DISENO</b> &mdash; datos de ejemplo, layout a validar.
  Si el layout te sirve, genero el HTML real leyendo el JSON completo (12 productos).
  Si quieres cambios de estructura, estilo o agrupacion, los hago ahora.</div>

  <div class="hero">
    <h1>Analizadores y medicion &mdash; SUPCON / Hobre</h1>
    <p>Catalogo tecnico del material de producto de SUPCON. Hobre es filial 100% de SUPCON
    desde abril 2023. Tres origenes conviven: Hobre (gama alta de proceso), SUPCON propio
    (emisiones y medicion estandar) y la unidad MIV que empaqueta todo.</p>
    <div class="stats">
      <div class="stat"><b>12</b><span>Productos</span></div>
      <div class="stat"><b>3</b><span>Familias</span></div>
      <div class="stat"><b>5</b><span>Relevantes Chile</span></div>
      <div class="stat"><b>8</b><span>Docs fuente</span></div>
    </div>
  </div>

  <div class="filtros">
    <span class="chip on">Todas las familias</span>
    <span class="chip">Hobre &middot; proceso</span>
    <span class="chip">SUPCON &middot; propio</span>
    <span class="chip">MIV &middot; sistema</span>
    <input class="search" placeholder="Buscar producto, componente, aplicacion...">
  </div>

  <!-- FAMILIA 1 -->
  <div class="fam">
    <div class="fam-h"><h2>Hobre &mdash; Analizadores de proceso</h2>
      <span class="org">filial SUPCON desde abr-2023</span></div>
    <div class="fam-n">Gama alta. Oil &amp; Gas, petroquimica y metales. Fabrica en Purmerend (NL),
      Szeged (HU) y Houston (US).</div>

    <details class="prod" open>
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">C-QUAND</span>
        <span class="p-rol">Analisis elemental multi-elemento en liquidos (XRF)</span>
        <span class="p-badge">mineria</span>
        <span class="p-badge">ED-XRF</span>
      </summary>
      <div class="p-body">
        <h4>Especificaciones clave</h4>
        <div class="grid">
          <div class="kv"><div class="k">Rango de elementos</div><div class="v">Si (Z=14) a U (Z=92)</div></div>
          <div class="kv"><div class="k">Rango de medicion</div><div class="v">&lt;1 ppmWt a &gt;10 %Wt</div></div>
          <div class="kv"><div class="k">Elementos simultaneos</div><div class="v">hasta 15</div></div>
          <div class="kv"><div class="k">Tubo de rayos X</div><div class="v">15 W / 50 kV, anodo Ag</div></div>
          <div class="kv"><div class="k">Tiempo de medicion</div><div class="v">tipico 5 min</div></div>
          <div class="kv"><div class="k">Disponibilidad</div><div class="v">&gt;99,5%</div></div>
        </div>
        <h4>Aplicaciones con fit en Chile</h4>
        <div class="tags">
          <span class="tag">Fe, Ni, Co, Cu, Mo, V, W, As, Zn, Sn y PGM en mineria</span>
          <span class="tag">Uranio en mineria</span>
          <span class="tag">Azufre en crudos y combustibles</span>
          <span class="tag">Cloro en crudo (corrosion)</span>
          <span class="tag">Aguas residuales</span>
        </div>
        <div class="fuente">fuente: Hobre C-Quand brochure.pdf (4 pp) + Training C-Quand (63 pp) + hobre.com</div>
      </div>
    </details>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">TISOMIC</span>
        <span class="p-rol">Analisis H2S, H2O y CO2 en gas y liquidos</span>
        <span class="p-badge">PA-TDL</span>
      </summary>
      <div class="p-body">
        <h4>Especificaciones clave</h4>
        <div class="grid">
          <div class="kv"><div class="k">Mide</div><div class="v">H2S, H2O, CO2, CH4</div></div>
          <div class="kv"><div class="k">Rango alta precision</div><div class="v">0-100 ppm</div></div>
          <div class="kv"><div class="k">Repetibilidad</div><div class="v">0,3 ppm</div></div>
          <div class="kv"><div class="k">MTBF</div><div class="v">&gt;5 anos</div></div>
          <div class="kv"><div class="k">Calibracion</div><div class="v">cada 3-6 meses</div></div>
          <div class="kv"><div class="k">Partes moviles</div><div class="v">ninguna</div></div>
        </div>
        <div class="aviso">Se vende siempre en paquete con <b>HIFISC</b> (acondicionamiento de muestra).
        Sin ficha tecnica propia en el material.</div>
        <div class="fuente">fuente: Hobre TISOMIC Analyzer Brochure.pdf (6 pp) + Training TISOMIC (54 pp)</div>
      </div>
    </details>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">WIM COMPAS</span>
        <span class="p-rol">Indice de Wobbe / poder calorifico / combustion</span>
        <span class="p-badge">4 modelos</span>
      </summary>
      <div class="p-body"><h4>Modelos</h4>
        <div class="tags"><span class="tag">Xpress &middot; continuo &middot; LNG</span>
        <span class="tag">Flex &middot; continuo &middot; mas opciones</span>
        <span class="tag">Pulse &middot; inyeccion &middot; gas amargo</span>
        <span class="tag">Pulse HT &middot; rocio 150 C</span></div>
        <div class="fuente">fuente: Hobre WIM COMPAS Brochure.pdf (8 pp)</div>
      </div>
    </details>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">PRISM</span>
        <span class="p-rol">Composicion de gas multicomponente (Raman)</span>
        <span class="p-badge">hidrogeno</span>
      </summary>
      <div class="p-body"><h4>Especificaciones clave</h4>
        <div class="grid">
          <div class="kv"><div class="k">Mide</div><div class="v">C1..C5+, N2, H2, CO2</div></div>
          <div class="kv"><div class="k">Respuesta</div><div class="v">T90 tipico 10 s</div></div>
          <div class="kv"><div class="k">Presion</div><div class="v">sin reduccion, 10-75 barG</div></div>
          <div class="kv"><div class="k">H2</div><div class="v">0-100% de fabrica</div></div>
        </div>
        <div class="fuente">fuente: Hobre PRISM Raman Brochure.pdf (4 pp)</div>
      </div>
    </details>
  </div>

  <!-- FAMILIA 2 -->
  <div class="fam">
    <div class="fam-h"><h2>SUPCON &mdash; Analizadores propios</h2>
      <span class="org">desarrollo propio</span></div>
    <div class="fam-n">Linea de emisiones y medicion estandar. No compite con Hobre en el mismo segmento.</div>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">CEMS 5000</span>
        <span class="p-rol">Monitoreo continuo de emisiones</span>
        <span class="p-badge">UV-DOAS</span>
      </summary>
      <div class="p-body"><h4>Componentes del sistema</h4>
        <div class="tags"><span class="tag">EM-5 analizador de gas</span>
        <span class="tag">LGT-510 modulo laser</span><span class="tag">GSP-100 sonda</span>
        <span class="tag">DMS-100 medidor de polvo</span><span class="tag">PT-500 flujo</span></div>
        <div class="fuente">fuente: CEMS_20230530.pptx (19 slides)</div>
      </div>
    </details>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">Flare CEMS</span>
        <span class="p-rol">Monitoreo de gas de antorcha</span>
        <span class="p-badge">integra Hobre</span>
      </summary>
      <div class="p-body"><h4>Equipos principales</h4>
        <div class="grid">
          <div class="kv"><div class="k">Analizador de BTU</div><div class="v">Hobre</div></div>
          <div class="kv"><div class="k">Cromatografo</div><div class="v">Siemens / ABB / SUPCON</div></div>
          <div class="kv"><div class="k">Caudalimetro</div><div class="v">GE / SICK</div></div>
          <div class="kv"><div class="k">Valvula control</div><div class="v">SUPCON</div></div>
        </div>
        <div class="fuente">fuente: Flare CEMS for Korean project R1 20240624.pptx (28 slides)</div>
      </div>
    </details>
  </div>

  <!-- FAMILIA 3 -->
  <div class="fam">
    <div class="fam-h"><h2>MIV &mdash; Sistema y complementos</h2>
      <span class="org">unidad MIV</span></div>
    <div class="fam-n">MIV = Main Instrument Vendor. Empaqueta analizador + casa + skid + valvulas + instrumentos.</div>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">Casa de analisis</span>
        <span class="p-rol">Analyzer house anti-explosion (TRACETECH)</span>
        <span class="p-badge">proveedor</span>
      </summary>
      <div class="p-body"><h4>Capacidades</h4>
        <div class="tags"><span class="tag">Zona I y II</span><span class="tag">Interlock de gases</span>
        <span class="tag">Pre-tratamiento</span><span class="tag">Taller 3.800 m2</span></div>
        <div class="fuente">fuente: TRACETECH 防爆分析小屋-中文版.pdf (6 pp, en chino)</div>
      </div>
    </details>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">TAS and Metering</span>
        <span class="p-rol">Carga/descarga de camiones y pesaje</span>
        <span class="p-badge">cruce COMASA</span>
      </summary>
      <div class="p-body"><h4>Alcance</h4>
        <div class="tags"><span class="tag">Pesaje automatico no atendido</span>
        <span class="tag">Anti-fraude</span><span class="tag">Reconocimiento de patente</span>
        <span class="tag">Integracion ERP/SAP</span></div>
        <div class="aviso">Mismo dominio del proyecto <b>COMASA</b> (carga de camiones y basculas).</div>
        <div class="fuente">fuente: InPlant TAS Introduction .pptx (24 slides) + SDO Tank Farm.pptx</div>
      </div>
    </details>

    <details class="prod">
      <summary class="p-sum">
        <span class="caret">&#9656;</span>
        <span class="p-name">HIPPS</span>
        <span class="p-rol">Sistema instrumentado de seguridad de alta integridad</span>
        <span class="p-badge">sin ficha</span>
      </summary>
      <div class="p-body"><div class="aviso">Solo hay propuesta tecnica, lista de I/O y un plano DWG.
        No hay ficha de producto.</div>
        <div class="fuente">fuente: Technical Proposal for HIPPS Rev.0.0 09.05.2024.pdf</div>
      </div>
    </details>
  </div>

  <!-- TABLA MAESTRA -->
  <div class="tblwrap">
    <h2>Matriz comparativa</h2>
    <table>
      <thead><tr><th>Producto</th><th>Familia</th><th>Rol</th><th>Principio</th>
      <th>Mide</th><th>Zona peligrosa</th></tr></thead>
      <tbody>
        <tr><td><b>C-QUAND</b></td><td>Hobre</td><td class="n">elemental en liquidos</td>
            <td class="n">ED-XRF</td><td class="n">Si a U, 15 elem.</td><td class="n">ATEX II 2G T4</td></tr>
        <tr><td><b>TISOMIC</b></td><td>Hobre</td><td class="n">H2S / H2O / CO2</td>
            <td class="n">PA-TDL</td><td class="n">ppm a %</td><td class="n">ATEX Zone 1 IIB+H2</td></tr>
        <tr><td><b>WIM COMPAS</b></td><td>Hobre</td><td class="n">Wobbe / BTU</td>
            <td class="n">oxigeno residual</td><td class="n">Wobbe, BTU, CARI</td><td class="n">ATEX Zone 1 IIC</td></tr>
        <tr><td><b>PRISM</b></td><td>Hobre</td><td class="n">composicion de gas</td>
            <td class="n">Raman</td><td class="n">C1..C5+, H2, N2</td><td class="n">ATEX/IECEx II 2G</td></tr>
        <tr><td><b>CEMS 5000</b></td><td>SUPCON</td><td class="n">emisiones</td>
            <td class="n">UV-DOAS</td><td class="n">SO2, NOx, CO, CO2</td><td class="n">no declarada</td></tr>
        <tr><td><b>Flare CEMS</b></td><td>SUPCON</td><td class="n">gas de antorcha</td>
            <td class="n">BTU + GC</td><td class="n">18-20 componentes</td><td class="n">no declarada</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ANGULO CONECTA -->
  <div class="angulo">
    <h2>Angulo CONECTA</h2>
    <p>Donde calza cada producto con el pipeline actual. Solo lo que tiene fundamento en el material.</p>
    <div class="cards">
      <div class="c"><div class="prod-n">C-QUAND</div><h5>Mineria</h5>
        <p>La ficha lista Fe, Ni, Co, Cu, Mo, V, W, As, Zn, Sn y PGM en mineria. Fit: SX/EW, molibdeno, aguas, relaves.</p></div>
      <div class="c"><div class="prod-n">WIM COMPAS</div><h5>Fundiciones</h5>
        <p>Control de gas de combustion, BFG, COG, control de hornos y flare. Fit: fundiciones y plantas con hornos.</p></div>
      <div class="c"><div class="prod-n">PRISM</div><h5>Hidrogeno</h5>
        <p>Mide H2 0-100% de fabrica, hydrogen blending y syngas, con cero emision. Fit: proyectos H2 en Chile.</p></div>
      <div class="c"><div class="prod-n">CEMS 5000</div><h5>Emisiones</h5>
        <p>Monitoreo continuo con UV-DOAS. Normativa china HJ75/HJ76. Hay que verificar equivalencia con la normativa chilena.</p></div>
      <div class="c"><div class="prod-n">TAS and Metering</div><h5>Cruce COMASA</h5>
        <p>Mismo dominio del proyecto COMASA: carga de camiones y basculas. Vale mirarlo cruzado.</p></div>
    </div>
  </div>

</div>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)

# verificacion de tags
import re
ab = len(re.findall(r'<details\b', HTML)); ce = len(re.findall(r'</details>', HTML))
print("escrito:", OUT)
print("details abiertos:", ab, "| cerrados:", ce, "|", "OK" if ab==ce else "DESCUADRE")
print("bytes:", len(HTML.encode()))
