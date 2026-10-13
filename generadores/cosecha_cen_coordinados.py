#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COSECHA DE CORREOS DESDE LAS PLANILLAS DEL COORDINADOR ELECTRICO ("Coordinados").

EL HALLAZGO
------------------------------------------------------------------------------
Las planillas oficiales del Coordinador (CEN-Coordinados-*.xlsx, publicas en coordinador.cl)
traen, POR EMPRESA, cuatro personas con NOMBRE y CORREO real:

  Gerente General + correo | Encargado Titular + correo
  Encargado Suplente + correo | Encargado Facturacion + correo

Es dato oficial, publicado, gratuito y verificable. NO se infiere nada.

POR QUE ESTO Y NO HUNTER (todavia)
------------------------------------------------------------------------------
El enfoque anterior era INFERIR el correo (patron + dominio adivinado) y salio mal: generaba
correos a empresas equivocadas. Este enfoque no infiere: COSECHA el correo tal como esta
publicado, y guarda la URL de la fuente para poder auditarlo. Un correo cosechado se puede
verificar abriendo la fuente; uno inferido, no.

HONESTIDAD SOBRE LO QUE ES
------------------------------------------------------------------------------
Estos son contactos REGULATORIOS y COMERCIALES de la empresa, no necesariamente los
compradores tecnicos de planta. Su valor es:
  (a) un correo REAL del dominio correcto -> sirve para deducir el PATRON de la empresa
      (que es lo que despues permite inferir el correo del CT con fundamento, no al azar), y
  (b) contacto directo util por si mismo (gerente general, encargado titular).
Se guarda aparte del plan CT para no confundir una cosa con la otra.

Entrada:  las planillas .xlsx del Coordinador en el directorio que se indique
Salida:   datos/cen_coordinados_correos.json
"""
import openpyxl, os, re, sys, json, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")
SRC = "/Users/victorvilche/.hermes/cache/scratch/valvulas/cen_coordinados"

EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# Correos que NO sirven para deducir el patron de una persona (genericos).
GENERICOS = re.compile(
    r"^(contacto|info|ventas|recepcion|secretaria|administracion|soporte|facturacion|"
    r"area|areas|electrico|electrica|operaciones|peajes|programacion|reportes|"
    r"notificaciones|comunicaciones|rrhh|clientes|servicio|servicios)@", re.I)


def norm_emp(s):
    s = (s or "").upper()
    s = re.sub(r"\b(S\.?A\.?C\.?|S\.?A\.?|SPA|LTDA\.?|LIMITADA|E\.?I\.?R\.?L\.?|SCM|SPA\.?)\b", "", s)
    return re.sub(r"[^A-Z0-9 ]", " ", s).strip()


def tokens(s):
    return {t for t in norm_emp(s).split() if len(t) > 3}


def leer_planilla(path):
    """Devuelve [(empresa, rut, rol, nombre, correo)] de una planilla de Coordinados."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for sh in wb.sheetnames:
        ws = wb[sh]
        filas = list(ws.iter_rows(values_only=True))
        if not filas:
            continue
        # localizar la fila de encabezado (la que trae 'Razón Social')
        hi = None
        for i, r in enumerate(filas[:5]):
            if any(isinstance(c, str) and "az" in c and "Social" in c for c in r if c):
                hi = i
                break
        if hi is None:
            continue
        hdr = [str(c).strip() if c is not None else "" for c in filas[hi]]
        # mapa: indice -> rol, para cada columna 'Correo Electrónico' la persona es la col anterior
        for i, col in enumerate(hdr):
            if not col.lower().startswith("correo"):
                continue
            # la persona es la ultima columna de nombre antes de este correo
            persona_i = None
            for j in range(i - 1, max(i - 4, -1), -1):
                if j < len(hdr) and hdr[j] and not hdr[j].lower().startswith("correo"):
                    persona_i = j
                    break
            rol = hdr[persona_i] if persona_i is not None else "contacto"
            for r in filas[hi + 1:]:
                if r is None or i >= len(r):
                    continue
                cel = r[i]
                if not isinstance(cel, str):
                    continue
                for m in EMAIL.findall(cel):
                    nombre = ""
                    if persona_i is not None and persona_i < len(r) and isinstance(r[persona_i], str):
                        nombre = r[persona_i].strip()
                    empresa = ""
                    if isinstance(r[0], str):
                        empresa = r[0].strip()
                    rut = r[2] if len(r) > 2 and isinstance(r[2], str) else ""
                    out.append({"empresa": empresa, "rut": rut, "rol": rol,
                                "nombre": nombre, "correo": m.strip(), "archivo": os.path.basename(path)})
    wb.close()
    return out


def main():
    archivos = sorted(glob.glob(os.path.join(SRC, "*.xlsx")))
    if not archivos:
        print(f"ERROR: no hay planillas en {SRC}", file=sys.stderr)
        sys.exit(1)

    todas = []
    for a in archivos:
        r = leer_planilla(a)
        print(f"  {os.path.basename(a):44s} {len(r):4d} registros")
        todas += r

    # dedupe por correo (una misma persona puede venir en la planilla vieja y la nueva)
    vistos = {}
    for t in todas:
        k = t["correo"].lower()
        if k not in vistos:
            vistos[k] = t
    regs = list(vistos.values())

    dominios = {}
    for t in regs:
        dm = t["correo"].split("@")[-1].lower()
        dominios.setdefault(dm, []).append(t)

    con_nombre = [t for t in regs if t["nombre"]]
    personales = [t for t in con_nombre if not GENERICOS.match(t["correo"])]

    print(f"\n  registros totales:            {len(todas)}")
    print(f"  correos unicos:               {len(regs)}")
    print(f"  con nombre de persona:        {len(con_nombre)}")
    print(f"  personales (no genericos):    {len(personales)}")
    print(f"  dominios distintos:           {len(dominios)}")

    # ---- CRUCE CON EL PLAN TECNICO ----
    pt_path = os.path.join(D, "plan_contacto_tecnico.json")
    cruce = {}
    if os.path.exists(pt_path):
        pt = json.load(open(pt_path, encoding="utf-8"))
        for cta in pt["cuentas"]:
            emp = cta["empresa"]
            te = tokens(emp)
            if not te:
                continue
            for dm, lista in dominios.items():
                # cotejar por dominio contra el nombre: el dominio debe contener un token
                # distintivo de la empresa (regla estricta: token completo, no substring corto)
                if any(t.lower() in dm for t in te):
                    cruce[emp] = {"dominio": dm, "empresa_planilla": lista[0]["empresa"],
                                  "correos": [{"nombre": x["nombre"], "correo": x["correo"],
                                               "rol": x["rol"]} for x in lista if x["nombre"]][:8]}

        empresas_ct = {c["empresa"] for c in pt["cuentas"]}
        tecnicos_tot = sum(len(c.get("tomadores", []) or []) for c in pt["cuentas"])
        hit = len(cruce)
        print(f"\n  === CRUCE CON EL PLAN TECNICO ({len(empresas_ct)} empresas, {tecnicos_tot} CT) ===")
        print(f"  empresas CT con dominio confirmado por la planilla del CEN: {hit}")
        # patrones deducidos de correos REALES
        print("\n  === PATRON DE CORREO DEDUCIDO DE CORREOS REALES (no inferido) ===")
        from collections import Counter
        pat = Counter()
        for dm, lista in dominios.items():
            for x in lista:
                if not x["nombre"] or GENERICOS.match(x["correo"]):
                    continue
                loc, dom = x["correo"].lower().split("@")
                partes = re.sub(r"[^a-z ]", " ", x["nombre"].lower()).split()
                if len(partes) < 2:
                    continue
                fn, ln = partes[0], partes[-1]
                if loc == fn[0] + ln:
                    pat["inicial_apellido"] += 1
                elif loc == fn + "." + ln:
                    pat["nombre.apellido"] += 1
                elif loc == fn + ln:
                    pat["nombreapellido"] += 1
                elif loc == fn + "." + partes[1][0] + ln if len(partes) > 2 else False:
                    pat["nombre.inicial_apellido"] += 1
                elif loc.startswith(fn[0]) and ln in loc:
                    pat["inicial_apellido+extra"] += 1
                else:
                    pat["otro"] += 1
        for k, v in pat.most_common():
            print(f"     {k:30s} {v}")

    json.dump({
        "fuente": ("Planillas oficiales 'Coordinados' del Coordinador Electrico Nacional "
                   "(https://www.coordinador.cl). Archivos: " +
                   ", ".join(os.path.basename(a) for a in archivos)),
        "que_es": ("DATO COSECHADO, no inferido: nombre y correo tal como estan publicados, "
                   "con el archivo de origen guardado para poder auditarlo."),
        "que_no_es": ("NO son necesariamente los compradores tecnicos de planta. Son los "
                      "contactos regulatorios/comerciales que la empresa declara al Coordinador "
                      "(gerente general, encargado titular, suplente, facturacion). Su valor "
                      "principal es doble: (a) dan el PATRON de correo real de la empresa, con "
                      "el que se puede inferir el del CT con fundamento, y (b) sirven de "
                      "contacto directo por si mismos."),
        "totales": {"registros": len(todas), "unicos": len(regs),
                    "con_nombre": len(con_nombre), "personales": len(personales),
                    "dominios": len(dominios)},
        "por_dominio": {k: [{"nombre": x["nombre"], "correo": x["correo"], "rol": x["rol"],
                             "empresa": x["empresa"]} for x in v] for k, v in dominios.items()},
        "cruce_plan_tecnico": cruce,
    }, open(os.path.join(D, "cen_coordinados_correos.json"), "w"), ensure_ascii=False, indent=1)
    print(f"\nguardado: datos/cen_coordinados_correos.json")


if __name__ == "__main__":
    main()
