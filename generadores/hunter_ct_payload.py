#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREPARA EL PAYLOAD DE HUNTER PARA LOS COMPRADORES TECNICOS (CT).

POR QUE LOS CT
------------------------------------------------------------------------------
El plan tecnico tiene 577 contactos de perfil CT (jefes de planta, mantenimiento,
I&C, electricos, automatizacion). De esos, 557 traen LinkedIn y SOLO 2 traen correo.
Para vender instrumentacion y control el que especifica es el CT: abre la puerta, y el
gerente firma despues. Sin correo del CT no hay outreach posible.

QUE HACE ESTE SCRIPT (y que NO hace)
------------------------------------------------------------------------------
SI:  arma la lista de consultas a Hunter, con el dominio de cada contacto tomado de
     fuente dura, y la deja en disco como payload ejecutable.
NO:  llama a la API. Eso lo hace hunter_ct.py, que necesita HUNTER_API_KEY.

REGLA DE DOMINIO
------------------------------------------------------------------------------
El dominio sale de la ficha de la empresa (contacto_corporativo.web) via
datos/dominios_duros.json. NUNCA se infiere del nombre de la empresa: ya se midio que eso
produce dominios de otras empresas (AGUAS PATAGONIA -> patagonia.com).
Un contacto de una empresa sin dominio de fuente NO entra al payload: primero hay que
resolver el dominio, y resolverlo bien.

Entrada:  datos/plan_contacto_tecnico.json + datos/dominios_duros.json
Salida:   datos/hunter_ct_payload.json
"""
import json, os, re, sys
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "datos")

# Dominios que NO son de la empresa: son del Estado, portales, o agregadores.
# Un correo a uno de estos no llega a la empresa.
DOMINIO_VETADO = {
    "hacienda.cl", "beta.hacienda.cl", "empresas.beta.hacienda.cl", "mma.gob.cl",
    "datosretc.mma.gob.cl", "guiachileenergia.cl", "linkedin.com", "cl.linkedin.com",
    "seia.sea.gob.cl", "sea.gob.cl", "bcentral.cl", "sii.cl", "dt.gob.cl",
    "chilecompra.cl", "mercadopublico.cl", "sec.cl", "cen.cl", "coordinador.cl",
}


def sin_tildes(s):
    n = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in n if not unicodedata.combining(c))


# Sufijos y titulos que el scraping pego al nombre y NO son el apellido.
# Medido en el plan: "Victor C. Santiago, PMP" daba apellido "PMP" y
# "Rafael Guzman M." daba apellido "M." — los dos rompen la consulta a Hunter.
SUFIJOS = {"PMP", "MBA", "MSC", "ING", "SR", "SRA", "DON", "DRA", "DR", "MG", "MAG",
           "PE", "PMI", "CISA", "CIA", "CPA", "PHD", "MSC", "ESP", "TEC", "EX", "JR",
           "II", "III", "IV", "SNR", "LEED", "PMP®", "MF"}


def partes_nombre(nombre):
    """Separa el nombre completo en first/last para el endpoint de Hunter.

    Hunter espera 'first_name' y 'last_name' por separado, y SOLO usa esos dos campos.
    Los nombres chilenos traen dos nombres y dos apellidos, asi que hay que decidir
    cual de los cuatro tokens es 'el apellido' que Hunter reconoce.

    Criterio: se descartan titulos (PMP, Ing, Sr), iniciales sueltas ("C.", "M.") y
    sufijos romanos; de lo que queda, el primer token es el nombre y el ULTIMO token
    completo es el apellido paterno (que es el que aparece en el correo corporativo
    chileno: juan.perez@, y no juan.perez.gonzalez@).
    """
    s = sin_tildes(nombre or "").strip()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[.,;]", " ", s)
    s = re.sub(r"\s+", " ", s)

    toks = []
    for t in s.split():
        u = t.upper()
        if u in SUFIJOS:            # titulo o sufijo
            continue
        if len(t) < 2:              # inicial suelta ("C.", "M.")
            continue
        if re.fullmatch(r"[IVX]+", u):   # romano suelto
            continue
        toks.append(t)

    if len(toks) < 2:
        return "", ""
    return toks[0], toks[-1]


def main():
    pt = json.load(open(os.path.join(D, "plan_contacto_tecnico.json"), encoding="utf-8"))
    dd = json.load(open(os.path.join(D, "dominios_duros.json"), encoding="utf-8"))
    dom_emp = {k.upper().strip(): v for k, v in dd["empresas"].items()}

    consultas = []
    sin_dominio = []
    ya_tienen = []

    for cta in pt["cuentas"]:
        empresa = cta["empresa"]
        info = dom_emp.get(empresa.upper().strip())
        dominio = (info or {}).get("dominio", "")
        dominio_ok = bool(dominio) and dominio not in DOMINIO_VETADO

        for t in cta.get("tomadores", []) or []:
            nombre = (t.get("nombre") or "").strip()
            correo = (t.get("correo") or "").strip()
            if correo:
                ya_tienen.append({"empresa": empresa, "nombre": nombre, "correo": correo,
                                  "origen": "fuente"})
                continue
            if not dominio_ok:
                sin_dominio.append({"empresa": empresa, "nombre": nombre,
                                    "cargo": t.get("cargo", ""), "perfil": t.get("perfil", ""),
                                    "linkedin": t.get("linkedin", ""),
                                    "motivo": ("sin dominio de fuente" if not dominio
                                               else f"dominio vetado: {dominio}")})
                continue
            fn, ln = partes_nombre(nombre)
            if not fn or not ln:
                sin_dominio.append({"empresa": empresa, "nombre": nombre,
                                    "cargo": t.get("cargo", ""), "perfil": t.get("perfil", ""),
                                    "linkedin": t.get("linkedin", ""),
                                    "motivo": "nombre no separable en nombre/apellido"})
                continue
            consultas.append({
                "empresa": empresa,
                "nombre_completo": nombre,
                "first_name": fn,
                "last_name": ln,
                "dominio": dominio,
                "cargo": t.get("cargo", ""),
                "perfil": t.get("perfil", ""),
                "rol_compra": t.get("rol_compra", ""),
                "linkedin": t.get("linkedin", ""),
                "dolor": cta.get("dolor"),
                "prioridad_contacto": cta.get("prioridad_contacto"),
            })

    # dedupe: mismo (dominio, first, last)
    visto = set()
    unicas = []
    for q in consultas:
        k = (q["dominio"], q["first_name"].lower(), q["last_name"].lower())
        if k in visto:
            continue
        visto.add(k)
        unicas.append(q)

    print("=" * 72)
    print("PAYLOAD DE HUNTER PARA COMPRADORES TECNICOS (CT)")
    print("=" * 72)
    print(f"  contactos CT en el plan:            {sum(len(c.get('tomadores', []) or []) for c in pt['cuentas'])}")
    print(f"  ya tienen correo de fuente:         {len(ya_tienen)}")
    print(f"  CONSULTABLES en Hunter:             {len(unicas)}")
    print(f"  sin dominio resoluble:              {len(sin_dominio)}")
    print()
    print(f"  empresas con dominio duro en el plan tecnico: "
          f"{sum(1 for c in pt['cuentas'] if (dom_emp.get(c['empresa'].upper().strip()) or {}).get('dominio'))}/{len(pt['cuentas'])}")

    from collections import Counter
    print("\n  por perfil (consultables):")
    # El plan tecnico guarda el perfil en la cuenta (perfil_tecnico / n_tecnicos), no dentro
    # de cada tomador: por eso el conteo por tomador salia vacio. Se cuenta por cargo.
    for k, v in Counter((q.get("cargo") or "sin cargo") for q in unicas).most_common(12):
        print(f"     {str(k)[:44]:46s} {v}")
    print("\n  dominios distintos a consultar:", len({q['dominio'] for q in unicas}))
    print("\n  muestra de las 12 primeras consultas:")
    for q in unicas[:12]:
        print(f"     {q['nombre_completo'][:26]:28s} {q['first_name']}.{q['last_name']}@{q['dominio']:<24s} {q['empresa'][:30]}")

    json.dump({
        "metodo": ("Consulta a Hunter Email Finder (endpoint /v2/email-finder) con dominio de "
                   "fuente dura + nombre y apellido. El dominio NO se infiere del nombre."),
        "endpoint": "https://api.hunter.io/v2/email-finder",
        "parametros": {"domain": "<dominio>", "first_name": "<first>", "last_name": "<last>"},
        "regla_dominio": "dominio tomado de la ficha de la empresa; los de dominio vetado (portales del Estado) quedan fuera",
        "consultas": unicas,
        "ya_tienen_correo": ya_tienen,
        "sin_dominio": sin_dominio,
    }, open(os.path.join(D, "hunter_ct_payload.json"), "w"), ensure_ascii=False, indent=1)
    print(f"\nguardado: datos/hunter_ct_payload.json")


if __name__ == "__main__":
    main()
