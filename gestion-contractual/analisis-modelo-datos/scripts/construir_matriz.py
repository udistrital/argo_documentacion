"""Construye la matriz comparativa (gap analysis) de la issue #356.

Uso:
    python3 construir_matriz.py <diccionario.xlsx> <inventario.json> <salida.xlsx>

Lee además las transcripciones de ../fuentes/ (BD de pruebas y tablas de Ágora).
"""

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from mapeo import CRUD_SIN_DICCIONARIO, M, MAPEO_AGORA, OBSERVACIONES_AGORA, SEVERIDADES, TIPOS_BRECHA

FUENTES = Path(__file__).resolve().parent.parent / "fuentes"

FUENTE = "Arial"
AZUL = "1F3864"
F_HEADER = PatternFill("solid", fgColor=AZUL)
F_SEV = {"Alta": "F8CBAD", "Media": "FFE699", "Baja": "DDEBF7", "Ninguna": "E2EFDA"}
BORDE = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
AUDITORIA = {"activo", "fecha_creacion", "fecha_modificacion"}
MONTO = re.compile(r"^(valor|saldo)")


def cabecera(ws, fila, columnas, anchos):
    for i, (col, ancho) in enumerate(zip(columnas, anchos), start=1):
        c = ws.cell(row=fila, column=i, value=col)
        c.font = Font(name=FUENTE, bold=True, color="FFFFFF")
        c.fill = F_HEADER
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BORDE
        ws.column_dimensions[get_column_letter(i)].width = ancho
    ws.freeze_panes = ws.cell(row=fila + 1, column=3)
    ws.row_dimensions[fila].height = 30


def cuerpo(ws, fila_ini, filas):
    for r, valores in enumerate(filas, start=fila_ini):
        for c, v in enumerate(valores, start=1):
            celda = ws.cell(row=r, column=c, value=v)
            celda.font = Font(name=FUENTE, size=10)
            celda.alignment = Alignment(wrap_text=True, vertical="top")
            celda.border = BORDE
    if filas:
        ws.auto_filter.ref = f"A{fila_ini - 1}:{get_column_letter(len(filas[0]))}{fila_ini + len(filas) - 1}"


def colorear_severidad(ws, col_letra, fila_ini, fila_fin):
    for sev, color in F_SEV.items():
        ws.conditional_formatting.add(
            f"{col_letra}{fila_ini}:{col_letra}{fila_fin}",
            FormulaRule(formula=[f'${col_letra}{fila_ini}="{sev}"'], fill=PatternFill("solid", fgColor=color)))


def titulo(ws, texto, sub=None):
    ws["A1"] = texto
    ws["A1"].font = Font(name=FUENTE, bold=True, size=14, color=AZUL)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(name=FUENTE, italic=True, size=10, color="595959")


def leer_diccionario(ruta):
    wb = openpyxl.load_workbook(ruta, data_only=True)
    dic = OrderedDict()
    for ws in wb.worksheets:
        filas = list(ws.iter_rows(values_only=True))[1:]
        dic[ws.title] = [(r[0], r[1] if len(r) > 1 else None) for r in filas if r and r[0]]
    return dic


def normalizar(tipo):
    if tipo is None:
        return None
    t = tipo.lower().replace("character varying", "varchar").replace("decimal", "numeric")
    return {"int": "integer", "int4": "integer", "bool": "boolean"}.get(t, t)


def categoria(tipo):
    """Categoría del tipo, que es lo único que muestra el diagrama de la BD de pruebas."""
    t = normalizar(tipo) or ""
    if t == "uuid":
        return "uuid"
    if t.startswith(("integer", "serial", "numeric", "bigint", "smallint")):
        return "numerico"
    if t.startswith(("varchar", "text", "char")):
        return "texto"
    if t.startswith(("timestamp", "date", "time")):
        return "fecha"
    if t.startswith("bool"):
        return "booleano"
    return t


def main():
    ruta_dic, ruta_inv, salida = sys.argv[1:4]
    dic = leer_diccionario(ruta_dic)
    inv = json.load(open(ruta_inv, encoding="utf-8"))
    ddl = inv["ddl"]["tablas"]
    ents = {e["tabla"]: e for e in inv["entidades"]}
    bd_json = json.load(open(FUENTES / "bd_pruebas.json", encoding="utf-8"))
    bd = {t: OrderedDict((c[0], {"categoria": c[1], "pk": len(c) > 2 and c[2]}) for c in d["columnas"])
          for t, d in bd_json["tablas"].items()}
    bd_no_aparecen = bd_json["no_aparecen"]
    agora_json = json.load(open(FUENTES / "agora.json", encoding="utf-8"))
    agora = {t: {c[0]: c[1] for c in d["columnas"]} for t, d in agora_json["tablas"].items()}

    def col_ddl(t, c):
        return next((x for x in ddl.get(t, {}).get("columnas", []) if x["columna"] == c), None)

    def col_ent(t, c):
        return next((x for x in ents.get(t, {}).get("columnas", []) if x["columna"] == c), None)

    # Validación de cobertura: cada campo del diccionario tiene exactamente una fila de mapeo
    claves_dic = [(h, c) for h, campos in dic.items() for c, _ in campos]
    claves_map = [(m["hoja"], m["campo"]) for m in M]
    faltan = set(claves_dic) - set(claves_map)
    sobran = set(claves_map) - set(claves_dic)
    duplicados = {k for k in claves_map if claves_map.count(k) > 1}
    assert not faltan and not sobran and not duplicados, (faltan, sobran, duplicados)
    assert len(claves_dic) == len(M)
    # El mapeo a Ágora solo puede citar tablas y columnas transcritas en fuentes/agora.json
    for (h, c), (tabla, cols, _, _) in MAPEO_AGORA.items():
        assert (h, c) in claves_map, (h, c)
        assert not tabla or all(col in agora.get(tabla, {}) for col in cols), (h, c, tabla, cols)

    wb = openpyxl.Workbook()

    # ---------------- Matriz (diccionario -> CRUD) ----------------
    wm = wb.active
    wm.title = "Matriz"
    titulo(wm, "Matriz comparativa: diccionario de datos RQ v2.0 → gestion_contractual_crud",
           "Una fila por campo del diccionario. Tipos y nulabilidad tomados del DDL (sql/creacion-tablas.sql) y de las entidades TypeORM.")
    cols = ["Entidad (diccionario)", "Campo (diccionario)", "Descripción (diccionario)", "Tabla CRUD", "Columna CRUD",
            "Tipo DDL", "Nulo DDL", "Tipo entidad", "Nulo entidad", "DDL = entidad", "Origen ARGO v1",
            "Tipo de brecha", "Severidad", "Recomendación", "Casos de uso", "Requiere validación de negocio",
            "En BD de pruebas"]
    anchos = [22, 26, 30, 26, 26, 15, 9, 15, 9, 10, 26, 22, 11, 70, 14, 12, 14]
    cabecera(wm, 4, cols, anchos)
    descripciones = {(h, c): d for h, campos in dic.items() for c, d in campos}
    filas = []
    for m in M:
        d = col_ddl(m["tabla"], m["columna"]) if m["columna"] else None
        e = col_ent(m["tabla"], m["columna"]) if m["columna"] else None
        igual = ""
        if d or e:
            igual = "Sí" if d and e and normalizar(d["tipo"]) == normalizar(e["tipo"]) and d["nullable"] == e["nullable"] else "No"
        en_bd = ""
        if m["tabla"] in bd_no_aparecen["tablas"]:
            en_bd = "Tabla no aparece en el diagrama"
        elif m["tabla"] in bd and m["columna"]:
            en_bd = "Sí" if m["columna"] in bd[m["tabla"]] else "No"
        filas.append([
            m["hoja"], m["campo"], descripciones[(m["hoja"], m["campo"])], m["tabla"], m["columna"],
            d["tipo"] if d else ("—" if m["columna"] else ""), ("Sí" if d["nullable"] else "No") if d else "",
            e["tipo"] if e else ("—" if m["columna"] else ""), ("Sí" if e["nullable"] else "No") if e else "",
            igual, m["v1"], m["brecha"], m["severidad"], m["recomendacion"], m["cu"], m["validar"], en_bd])
    cuerpo(wm, 5, filas)
    fin_matriz = 4 + len(filas)
    colorear_severidad(wm, "M", 5, fin_matriz)
    dv_b = DataValidation(type="list", formula1='"' + ",".join(TIPOS_BRECHA) + '"', allow_blank=False)
    dv_s = DataValidation(type="list", formula1='"' + ",".join(SEVERIDADES) + '"', allow_blank=False)
    wm.add_data_validation(dv_b)
    wm.add_data_validation(dv_s)
    dv_b.add(f"L5:L{fin_matriz}")
    dv_s.add(f"M5:M{fin_matriz}")

    # ---------------- CRUD sin diccionario (dirección inversa) ----------------
    wi = wb.create_sheet("CRUD sin diccionario")
    titulo(wi, "Columnas del CRUD que el diccionario no contempla",
           "Dirección inversa de la matriz. Se omiten id y columnas de auditoría (activo, fecha_creacion, fecha_modificacion).")
    cabecera(wi, 4, ["Tabla CRUD", "Columna", "Tipo DDL", "Nulo DDL", "Comentario DDL", "Tiene entidad",
                     "Referenciada en el diccionario", "Observación de la tabla", "Severidad"],
             [26, 30, 15, 9, 60, 10, 14, 60, 11])
    usadas = {(m["tabla"], m["columna"]) for m in M if m["columna"]}
    tablas_usadas = {m["tabla"] for m in M}
    filas_i = []
    for t, d in ddl.items():
        obs, sev = CRUD_SIN_DICCIONARIO.get(t, ("", ""))
        for c in d["columnas"]:
            if c["pk"] or c["columna"] in AUDITORIA:
                continue
            ref = (t, c["columna"]) in usadas
            if ref:
                continue
            filas_i.append([t, c["columna"], c["tipo"], "Sí" if c["nullable"] else "No", c["comentario"] or "",
                            "Sí" if t in ents else "No", "No",
                            obs or ("Tabla referenciada en el diccionario; esta columna no." if t in tablas_usadas else ""),
                            sev or "Baja"])
    cuerpo(wi, 5, filas_i)
    colorear_severidad(wi, "I", 5, 4 + len(filas_i))

    # ---------------- DDL vs entidad ----------------
    wd = wb.create_sheet("DDL vs entidad")
    titulo(wd, "Desalineación entre el DDL y las entidades TypeORM",
           "Comparación del código (DDL frente a entidades). La hoja BD de pruebas contrasta ambos con el diagrama de la base del ambiente de pruebas.")
    cabecera(wd, 4, ["Tabla", "Columna", "En DDL", "En entidad", "Tipo DDL", "Tipo entidad", "Nulo DDL", "Nulo entidad",
                     "Diferencia", "Severidad"], [26, 30, 9, 10, 15, 15, 9, 10, 60, 11])
    filas_d = []
    for t in sorted(set(ddl) | set(ents)):
        if t not in ents:
            filas_d.append([t, "(tabla)", "Sí", "No", "", "", "", "", "Tabla sin entidad, módulo ni endpoints.", "Media"])
            continue
        if t not in ddl:
            filas_d.append([t, "(tabla)", "No", "Sí", "", "", "", "", "Entidad sin tabla en el DDL.", "Alta"])
            continue
        nombres = list(OrderedDict.fromkeys([c["columna"] for c in ddl[t]["columnas"]] + [c["columna"] for c in ents[t]["columnas"]]))
        for n in nombres:
            d, e = col_ddl(t, n), col_ent(t, n)
            difs, sev = [], "Baja"
            if not d:
                difs.append("Columna solo en la entidad")
                sev = "Alta"
            elif not e:
                difs.append("Columna solo en el DDL")
                sev = "Alta" if not d["nullable"] else "Media"
            else:
                td, te = normalizar(d["tipo"]), normalizar(e["tipo"])
                if d["pk"] and te == "uuid":
                    difs.append("PK serial en DDL, uuid en la entidad")
                    sev = "Alta"
                elif td != te and not (d["pk"] and te == "serial"):
                    difs.append(f"Tipo {td} vs {te}")
                    sev = "Media"
                if d["nullable"] != e["nullable"] and not d["pk"]:
                    difs.append("Nulabilidad distinta")
                    sev = "Media" if sev == "Baja" else sev
            if difs:
                filas_d.append([t, n, "Sí" if d else "No", "Sí" if e else "No", d["tipo"] if d else "",
                                e["tipo"] if e else "", ("Sí" if d["nullable"] else "No") if d else "",
                                ("Sí" if e["nullable"] else "No") if e else "", "; ".join(difs), sev])
        # Cardinalidad: OneToOne en la entidad sin UNIQUE en el DDL
        for r in ents[t]["relaciones"]:
            if r["tipo"] == "OneToOne" and r["join_column"]:
                c = col_ddl(t, r["join_column"])
                if c and not c["unique"]:
                    filas_d.append([t, r["join_column"], "Sí", "Sí", "", "", "", "",
                                    "Relación 1:1 (@OneToOne) en la entidad; 1:N en el DDL (sin UNIQUE).", "Media"])
    cuerpo(wd, 5, filas_d)
    colorear_severidad(wd, "J", 5, 4 + len(filas_d))

    # ---------------- BD de pruebas ----------------
    wb_ = wb.create_sheet("BD de pruebas")
    titulo(wb_, "BD del ambiente de pruebas frente al DDL y a las entidades TypeORM",
           "Fuente: diagrama compartido por el LT (respuesta 1), transcrito en fuentes/bd_pruebas.json. El diagrama solo permite "
           "comparar nombres de tablas y columnas, la PK y la categoría del tipo; no permite verificar longitudes, precisión, "
           "nulabilidad, valores por defecto, UNIQUE, índices ni cardinalidad.")
    cabecera(wb_, 4, ["Tabla", "Columna", "En BD pruebas", "En DDL", "En entidad", "Categoría BD", "Tipo DDL",
                      "Tipo entidad", "Resultado", "Observación"], [26, 30, 10, 9, 10, 12, 15, 15, 16, 70])
    filas_b = []
    for t in sorted(set(bd) | set(ddl) | set(ents)):
        if t in bd_no_aparecen["tablas"]:
            filas_b.append([t, "(tabla)", "No", "Sí" if t in ddl else "No", "Sí" if t in ents else "No", "", "", "",
                            "No aparece en el diagrama", bd_no_aparecen["nota"]])
            continue
        if t not in bd:
            filas_b.append([t, "(tabla)", "No", "Sí" if t in ddl else "No", "Sí" if t in ents else "No", "", "", "",
                            "Difiere", "Tabla del código que no aparece en el diagrama."])
            continue
        if t not in ents:
            filas_b.append([t, "(tabla)", "Sí", "Sí" if t in ddl else "No", "No", "", "", "", "Sin entidad",
                            "Existe en la BD de pruebas y en el DDL, sin entidad, módulo ni endpoints."])
        nombres = list(OrderedDict.fromkeys(list(bd[t]) + [c["columna"] for c in ddl.get(t, {}).get("columnas", [])]
                                            + [c["columna"] for c in ents.get(t, {}).get("columnas", [])]))
        for n in nombres:
            b, d, e = bd[t].get(n), col_ddl(t, n), col_ent(t, n)
            obs = []
            if not b:
                obs.append("Columna del código que no aparece en la BD de pruebas")
            if t in ddl and not d:
                obs.append("Columna que no está en el DDL")
            if t in ents and not e:
                obs.append("Columna que no está en la entidad")
            if b and d and categoria(d["tipo"]) != b["categoria"]:
                obs.append(f"Categoría distinta entre BD ({b['categoria']}) y DDL ({d['tipo']})")
            if b and e and categoria(e["tipo"]) != b["categoria"]:
                if b["pk"] and e["tipo"] == "uuid":
                    obs.append("PK numérica en la BD (como en el DDL); uuid en la entidad")
                else:
                    obs.append(f"Categoría distinta entre BD ({b['categoria']}) y entidad ({e['tipo']})")
            filas_b.append([t, n, "Sí" if b else "No", "Sí" if d else "No",
                            ("Sí" if e else "No") if t in ents else "—", b["categoria"] if b else "",
                            d["tipo"] if d else "", e["tipo"] if e else "", "Difiere" if obs else "Coincide",
                            "; ".join(obs)])
    cuerpo(wb_, 5, filas_b)
    fin_b = 4 + len(filas_b)
    for res, color in {"Difiere": "F8CBAD", "Coincide": "E2EFDA", "Sin entidad": "FFE699",
                       "No aparece en el diagrama": "DDEBF7"}.items():
        wb_.conditional_formatting.add(f"I5:I{fin_b}", FormulaRule(formula=[f'$I5="{res}"'],
                                                                  fill=PatternFill("solid", fgColor=color)))

    # ---------------- Mapeo Ágora ----------------
    wa = wb.create_sheet("Mapeo Ágora")
    titulo(wa, "Campos del proveedor y sus especializaciones en Ágora",
           "Fuente: tablas de Ágora compartidas por el LT (respuesta 2), transcritas en fuentes/agora.json. Solo se muestra la "
           "categoría del tipo. Los nombres de tabla cortados en el diagrama se dejan con '…'.")
    cabecera(wa, 4, ["Entidad (diccionario)", "Campo (diccionario)", "Descripción (diccionario)", "Tabla Ágora",
                     "Columna(s) Ágora", "Categoría", "Cobertura", "Observación"], [22, 26, 30, 30, 34, 14, 12, 70])
    filas_a = []
    for (h, c) in [k for k in claves_dic if k in MAPEO_AGORA]:
        tabla, cols, cob, obs = MAPEO_AGORA[(h, c)]
        cats = ", ".join(sorted({agora[tabla][x] for x in cols})) if tabla else ""
        filas_a.append([h, c, descripciones[(h, c)], tabla, ", ".join(cols), cats, cob, obs])
    cuerpo(wa, 5, filas_a)
    fin_a = 4 + len(filas_a)
    for cob, color in {"Sí": "E2EFDA", "Aproximada": "FFE699", "No visible": "F8CBAD"}.items():
        wa.conditional_formatting.add(f"G5:G{fin_a}", FormulaRule(formula=[f'$G5="{cob}"'],
                                                                 fill=PatternFill("solid", fgColor=color)))
    r = fin_a + 2
    wa.cell(row=r, column=1, value="Observaciones").font = Font(name=FUENTE, bold=True, size=12, color=AZUL)
    for i, o in enumerate(OBSERVACIONES_AGORA, start=r + 1):
        celda = wa.cell(row=i, column=1, value=f"• {o}")
        celda.font = Font(name=FUENTE, size=10)

    # ---------------- Lineamientos ----------------
    wl = wb.create_sheet("Lineamientos")
    titulo(wl, "Desviaciones frente a los lineamientos OATI (modelo de datos y API)")
    cabecera(wl, 4, ["Ámbito", "Tabla / recurso", "Columna / ruta", "Valor actual", "Lineamiento", "Severidad"],
             [14, 30, 34, 30, 50, 11])
    filas_l = []
    for t, d in ddl.items():
        for c in d["columnas"]:
            n, tipo = c["columna"], c["tipo"]
            if MONTO.match(n) and tipo.startswith("numeric") and tipo != "numeric(20,7)":
                filas_l.append(["Modelo", t, n, tipo, "Montos en numeric(20,7)", "Media"])
            if tipo == "varchar":
                filas_l.append(["Modelo", t, n, tipo, "Varchar siempre con longitud explícita", "Baja"])
            if n == "activo" and (c["default"] or "").upper() != "TRUE":
                filas_l.append(["Modelo", t, n, f"boolean, nulo={'Sí' if c['nullable'] else 'No'}, sin default",
                                "activo boolean DEFAULT TRUE", "Media" if c["nullable"] else "Baja"])
            if n in ("fecha_creacion", "fecha_modificacion") and c["nullable"]:
                filas_l.append(["Modelo", t, n, "timestamp nulo", "Columna de auditoría obligatoria", "Baja"])
            if c["fk"]:
                ref = c["fk"].split(".")[0]
                if n != f"{ref}_id":
                    filas_l.append(["Modelo", t, n, f"FK a {ref}", f"Llave foránea nombrada {ref}_id", "Baja"])
        if t in ents and any(x["pk"] and x["tipo"] == "uuid" for x in ents[t]["columnas"]):
            filas_l.append(["Modelo", t, "id", "uuid (entidad)", "PK id de tipo serial", "Alta"])
    filas_l.append(["Modelo", "Todas las tablas", "PRIMARY KEY / REFERENCES", "Restricciones declaradas en línea, sin nombre",
                    "pk_<tabla>, fk_<origen>_<referenciada>", "Baja"])
    for i in inv["ddl"]["indices"]:
        esperado = f"idx_{i['tabla']}_{i['columna']}"
        if i["nombre"] != esperado:
            filas_l.append(["Modelo", i["tabla"], i["nombre"], i["nombre"], f"Nombre esperado: {esperado}", "Baja"])
    for ep in inv["endpoints"]:
        ruta = ep["ruta"]
        if ruta == "/":
            continue
        if "_" in ruta.split(":")[0]:
            filas_l.append(["API", ep["controlador"], f"{ep['verbo']} {ruta}", ruta, "URI con guion (-), nunca guion bajo", "Media"])
    vistos = set()
    for ep in inv["endpoints"]:
        base = ep["ruta"].split("/")[1] if ep["ruta"] != "/" else ""
        if base == "ordenador-contrato" and base not in vistos:
            vistos.add(base)
            filas_l.append(["API", ep["controlador"], "/ordenador-contrato", "/ordenador-contrato",
                            "Recursos en plural (/ordenadores-contratos)", "Media"])
        if "conteo" in ep["ruta"]:
            filas_l.append(["API", ep["controlador"], f"{ep['verbo']} {ep['ruta']}", "POST para una consulta",
                            "Verbo HTTP según la acción: una consulta de conteo es GET", "Baja"])
    for servicio in inv.get("borrado_fisico", []):
        filas_l.append(["API", servicio, "DELETE /:id", "repository.delete(id)",
                        "NUNCA DELETE real: borrado lógico (activo = false)", "Alta"])
    cuerpo(wl, 5, filas_l)
    colorear_severidad(wl, "F", 5, 4 + len(filas_l))

    # ---------------- Impacto en endpoints ----------------
    wp = wb.create_sheet("Impacto endpoints")
    titulo(wp, "Impacto de los ajustes recomendados sobre la API del CRUD",
           "Ver el informe (sección Plan de ajustes) para el detalle de cada ajuste.")
    cabecera(wp, 4, ["Ajuste", "Fase", "Estado", "Descripción", "Tablas", "Endpoints afectados", "Tipo de impacto",
                     "¿Rompe consumidores?", "Requiere decisión de negocio"], [8, 6, 16, 60, 30, 50, 30, 12, 16])
    rutas_por_tabla = {}
    for ep in inv["endpoints"]:
        ctrl = ep["controlador"].split("/")[1]
        rutas_por_tabla.setdefault(ctrl, set()).add(ep["ruta"].split("/")[1] if ep["ruta"] != "/" else "")
    modulo = {"contratista": "contratista", "documento_contrato": "documento-contrato", "supervisor_contrato": "supervisor",
              "estado_contrato": "estado-contrato", "solicitante": "solicitante", "lugar_ejecucion": "lugar-ejecucion",
              "ordenador_contrato": "ordenador-contrato", "contrato_general": "contrato-general",
              "disponibilidad_presupuestal": "cdp", "poliza": "poliza", "acta_inicio": "acta-inicio",
              "especificacion_tecnica": "especificacion-tecnica", "amparo_poliza": "amparo-poliza"}

    def eps(tablas):
        out = []
        for t in tablas:
            for r in sorted(rutas_por_tabla.get(modulo.get(t, ""), [])):
                out.append(f"/{r}")
        return ", ".join(out) if out else "Nuevo recurso"

    from ajustes import AJUSTES, CRITERIO
    wp["A3"] = f"Criterio acordado con el LT: {CRITERIO}"
    wp["A3"].font = Font(name=FUENTE, italic=True, size=10, color="595959")
    filas_p = [[a["id"], a["fase"], a["estado"], a["descripcion"], ", ".join(a["tablas"]),
                a.get("endpoints") or eps(a["tablas"]), a["impacto"], a["rompe"], a["decision"]]
               for a in sorted(AJUSTES, key=lambda a: int(a["id"][1:]))]
    cuerpo(wp, 5, filas_p)

    # ---------------- Cobertura por entidad ----------------
    wc = wb.create_sheet("Cobertura por entidad")
    titulo(wc, "Cobertura por entidad del diccionario", "Conteos calculados con fórmulas sobre la hoja Matriz.")
    cabecera(wc, 4, ["Entidad (diccionario)", "Campos"] + TIPOS_BRECHA + ["Alta", "Media", "Tabla(s) CRUD"],
             [28, 9] + [12] * len(TIPOS_BRECHA) + [8, 8, 40])
    rng = lambda col: f"Matriz!${col}$5:${col}${fin_matriz}"
    filas_c = []
    for idx, hoja in enumerate(dic, start=5):
        tablas = sorted({m["tabla"] for m in M if m["hoja"] == hoja and m["tabla"]})
        fila_c = [hoja, f'=COUNTIF({rng("A")},A{idx})']
        for j, _ in enumerate(TIPOS_BRECHA):
            col_hdr = get_column_letter(3 + j)
            fila_c.append(f'=COUNTIFS({rng("A")},$A{idx},{rng("L")},{col_hdr}$4)')
        fila_c += [f'=COUNTIFS({rng("A")},$A{idx},{rng("M")},"Alta")',
                   f'=COUNTIFS({rng("A")},$A{idx},{rng("M")},"Media")', ", ".join(tablas)]
        filas_c.append(fila_c)
    cuerpo(wc, 5, filas_c)
    tot = 5 + len(filas_c)
    wc.cell(row=tot, column=1, value="Total").font = Font(name=FUENTE, bold=True)
    for j in range(2, 3 + len(TIPOS_BRECHA) + 2):
        L = get_column_letter(j)
        c = wc.cell(row=tot, column=j, value=f"=SUM({L}5:{L}{tot - 1})")
        c.font = Font(name=FUENTE, bold=True)

    # ---------------- Supuestos y preguntas ----------------
    wq = wb.create_sheet("Supuestos y preguntas")
    titulo(wq, "Supuestos del análisis, preguntas con las respuestas del LT y decisiones abiertas",
           "Respuestas del comentario del LT en la issue #356 y de la sesión de socialización (1 de octubre de 2026). "
           "Se propone cerrar las decisiones abiertas en issues de seguimiento, sin bloquear la aprobación del análisis.")
    cabecera(wq, 4, ["#", "Tipo", "Descripción", "Dirigida a", "Respuesta", "Estado"], [5, 14, 70, 16, 70, 22])
    from ajustes import DECISIONES_ABIERTAS, PREGUNTAS, SUPUESTOS
    # Supuestos S1..Sn; preguntas 1..n con la misma numeración del comentario de la issue #356; decisiones D1..Dn
    filas_q = [[f"S{i}", "Supuesto", s, "", "", ""] for i, s in enumerate(SUPUESTOS, start=1)]
    filas_q += [[i, "Pregunta", p, a, r, e] for i, (p, a, r, e) in enumerate(PREGUNTAS, start=1)]
    filas_q += [[d, "Decisión abierta", f"{tema}. Para cerrarla: {nec}", resp, "", est]
                for d, tema, resp, nec, est in DECISIONES_ABIERTAS]
    cuerpo(wq, 5, filas_q)

    # ---------------- Resumen ----------------
    wr = wb.create_sheet("Resumen", 0)
    titulo(wr, "Issue #356 — Análisis comparativo del modelo de datos",
           "gestion_contractual_crud (develop) frente al Diccionario de Datos Contratación UD v2.0 (08-06-2026)")
    from ajustes import DECISIONES_ABIERTAS, SESION
    info = [
        ("Repositorio analizado", f"udistrital/gestion_contractual_crud · rama develop · commit {inv.get('commit', '')}"),
        ("Diccionario", "Diccionario_Datos_Contratacion_UD V2.0 08-06-2026.xlsx"),
        ("Casos de uso", "Casos Uso Contratacion Universidad Distrital.docx (CU-01 a CU-22)"),
        ("Modelo ARGO v1 (producción)", "Diagrama adjunto a la issue + modelo-database/README.md"),
        ("BD de pruebas", "Diagrama del LT en la issue #356 (respuesta 1) · fuentes/bd_pruebas.json"),
        ("Ágora", "Tablas del proveedor compartidas por el LT (respuesta 2) · fuentes/agora.json"),
        ("Respuestas", "Comentario del LT en la issue #356 y sesión de socialización"),
        ("Sesión de socialización", f"{SESION['fecha']} · {SESION['asistentes']}"),
        ("Fecha de corte", inv.get("fecha", "")),
    ]
    for i, (k, v) in enumerate(info, start=4):
        wr.cell(row=i, column=1, value=k).font = Font(name=FUENTE, bold=True)
        wr.cell(row=i, column=2, value=v).font = Font(name=FUENTE)
    fila = 4 + len(info) + 1
    wr.cell(row=fila, column=1, value="Volumen").font = Font(name=FUENTE, bold=True, size=12, color=AZUL)
    vol = [
        ("Entidades en el diccionario", len(dic)),
        ("Entidades del diccionario con solo identificador", sum(1 for c in dic.values() if len(c) == 1)),
        ("Campos en el diccionario", f"=COUNTA(Matriz!B5:B{fin_matriz})"),
        ("Tablas en el DDL del CRUD", len(ddl)),
        ("Entidades TypeORM", len(ents)),
        ("Endpoints del CRUD", len([e for e in inv["endpoints"] if e["ruta"] != "/"])),
        ("Columnas del CRUD sin referencia en el diccionario", f"=COUNTA('CRUD sin diccionario'!A5:A{4 + len(filas_i)})"),
        ("Diferencias DDL vs entidad", f"=COUNTA('DDL vs entidad'!A5:A{4 + len(filas_d)})"),
        ("Desviaciones de lineamientos", f"=COUNTA(Lineamientos!A5:A{4 + len(filas_l)})"),
        ("Tablas en el diagrama de la BD de pruebas", len(bd)),
        ("Columnas que difieren entre la BD de pruebas y el código", f"=COUNTIF('BD de pruebas'!I5:I{fin_b},\"Difiere\")"),
        ("Tablas de la BD de pruebas sin entidad", f"=COUNTIF('BD de pruebas'!I5:I{fin_b},\"Sin entidad\")"),
        ("Decisiones abiertas", len(DECISIONES_ABIERTAS)),
        ("Campos del diccionario mapeados a Ágora", len(filas_a)),
        ("Campos sin columna visible en Ágora", f"=COUNTIF('Mapeo Ágora'!G5:G{fin_a},\"No visible\")"),
    ]
    for i, (k, v) in enumerate(vol, start=fila + 1):
        wr.cell(row=i, column=1, value=k).font = Font(name=FUENTE)
        c = wr.cell(row=i, column=2, value=v)
        c.font = Font(name=FUENTE, color="0000FF" if not str(v).startswith("=") else "000000")
    fila = fila + len(vol) + 2
    wr.cell(row=fila, column=1, value="Brechas del diccionario (hoja Matriz)").font = Font(name=FUENTE, bold=True, size=12, color=AZUL)
    hdr = fila + 1
    for j, h in enumerate(["Tipo de brecha", "Campos"] + SEVERIDADES, start=1):
        c = wr.cell(row=hdr, column=j, value=h)
        c.font = Font(name=FUENTE, bold=True, color="FFFFFF")
        c.fill = F_HEADER
    for i, tb in enumerate(TIPOS_BRECHA, start=hdr + 1):
        wr.cell(row=i, column=1, value=tb).font = Font(name=FUENTE)
        wr.cell(row=i, column=2, value=f'=COUNTIF({rng("L")},A{i})').font = Font(name=FUENTE)
        for j, sev in enumerate(SEVERIDADES, start=3):
            wr.cell(row=i, column=j, value=f'=COUNTIFS({rng("L")},$A{i},{rng("M")},{get_column_letter(j)}${hdr})').font = Font(name=FUENTE)
    t_row = hdr + 1 + len(TIPOS_BRECHA)
    for r in range(hdr, t_row + 1):
        for j in range(2, 3 + len(SEVERIDADES)):
            wr.cell(row=r, column=j).alignment = Alignment(horizontal="center")
    wr.cell(row=t_row, column=1, value="Total").font = Font(name=FUENTE, bold=True)
    for j in range(2, 3 + len(SEVERIDADES)):
        L = get_column_letter(j)
        c = wr.cell(row=t_row, column=j, value=f"=SUM({L}{hdr + 1}:{L}{t_row - 1})")
        c.font = Font(name=FUENTE, bold=True)
        c.alignment = Alignment(horizontal="center")
    fila = t_row + 2
    wr.cell(row=fila, column=1, value="Leyenda").font = Font(name=FUENTE, bold=True, size=12, color=AZUL)
    from ajustes import LEYENDA
    for i, (k, v) in enumerate(LEYENDA, start=fila + 1):
        wr.cell(row=i, column=1, value=k).font = Font(name=FUENTE, bold=True)
        c = wr.cell(row=i, column=2, value=v)
        c.font = Font(name=FUENTE)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wr.column_dimensions["A"].width = 48
    wr.column_dimensions["B"].width = 70
    for L in "CDEF":
        wr.column_dimensions[L].width = 11
    for ws in wb.worksheets:
        ws.sheet_view.zoomScale = 90
        ws.page_setup.orientation = "landscape"
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0

    wb.save(salida)
    print(f"matriz: {len(filas)} | inversa: {len(filas_i)} | ddl vs entidad: {len(filas_d)} | bd pruebas: {len(filas_b)} "
          f"(difiere: {sum(1 for f in filas_b if f[8] == 'Difiere')}) | ágora: {len(filas_a)} | lineamientos: {len(filas_l)} "
          f"| ajustes: {len(filas_p)}")


if __name__ == "__main__":
    main()
