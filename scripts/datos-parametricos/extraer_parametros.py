"""Consolida en Excel los datos paramétricos de ARGO v2 (issue #377).

Consulta en parametros_crud los tipos de parámetro y los parámetros específicos que usa
gestion_contractual_mf (ver config_parametros.py) y genera:
  - salida/consolidado_parametros_argo_v2_AAAA-MM-DD.xlsx: un índice y una hoja por tipo,
    con las columnas "Aplica para Rectoría" y "Aplica para IDEXUD" vacías para negocio.
  - salida/reporte_validacion.md: existencia y tipo de cada constante, conteos y diferencias.

Incluye activos e inactivos sin distinguirlos en el Excel.

Uso:
    python3 extraer_parametros.py [--url URL] [--salida DIRECTORIO]

Variables de entorno (o archivo .env junto al script):
    PARAMETROS_URL    URL base de parametros_crud (por defecto la de pruebas)
    PARAMETROS_TOKEN  token Bearer opcional
"""

import argparse
import datetime
import math
import os
import re
import sys
from pathlib import Path

import requests
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import config_parametros as cfg

DIR_SCRIPT = Path(__file__).resolve().parent
LIMITE_PAGINA = 200
MAX_PAGINAS = 500
TIMEOUT_CONEXION = 10
TIMEOUT_LECTURA = 60

COLUMNAS = ["Id", "Nombre", "Descripción", "Código abreviación", "Aplica para Rectoría", "Aplica para IDEXUD"]
COLUMNAS_INDICE = ["Id del tipo", "Nombre del tipo", "Variable de entorno", "Cantidad de parámetros", "Hoja"]
OPCIONES_APLICA = '"Sí,No"'
MARGEN_VALIDACION = 100  # filas extra con lista Sí/No por si negocio agrega registros
ANCHO_MAXIMO = 45
ANCHO_MAXIMO_DESCRIPCION = 50
ANCHO_MINIMO = 8
ALTO_LINEA = 15  # puntos por línea de texto ajustado

RELLENO_CABECERA = PatternFill("solid", fgColor="1F4E78")
FUENTE_CABECERA = Font(bold=True, color="FFFFFF")
LINEA = Side(style="thin", color="808080")
BORDE = Border(left=LINEA, right=LINEA, top=LINEA, bottom=LINEA)


class ErrorServicio(Exception):
    pass


def cargar_env(ruta: Path) -> None:
    """Carga KEY=VALOR de un .env sin pisar variables ya definidas."""
    if not ruta.is_file():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


def desenvolver(cuerpo):
    """Las respuestas de parametros_crud vienen como {"Data": ...}; se aceptan ambas formas."""
    if isinstance(cuerpo, dict) and "Data" in cuerpo:
        return cuerpo["Data"]
    return cuerpo


class ClienteParametros:
    def __init__(self, url: str, token: str = ""):
        self.url = url if url.endswith("/") else url + "/"
        self.sesion = requests.Session()
        reintentos = Retry(total=3, connect=1, read=2, status=3, backoff_factor=1,
                           status_forcelist=(502, 503, 504), allowed_methods=("GET",))
        self.sesion.mount("http://", HTTPAdapter(max_retries=reintentos))
        self.sesion.mount("https://", HTTPAdapter(max_retries=reintentos))
        self.sesion.headers["Accept"] = "application/json"
        if token:
            self.sesion.headers["Authorization"] = f"Bearer {token}"

    def _get(self, ruta: str, params: dict | None = None):
        destino = self.url + ruta
        try:
            resp = self.sesion.get(destino, params=params, timeout=(TIMEOUT_CONEXION, TIMEOUT_LECTURA))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ErrorServicio(
                f"No se pudo conectar con {self.url} ({type(e).__name__}).\n"
                "  El servicio de pruebas está en la intranet: verifique que la VPN de la universidad "
                "esté conectada y que la URL sea correcta (--url o PARAMETROS_URL)."
            ) from e
        if resp.status_code == 404:
            return None
        if resp.status_code in (401, 403):
            raise ErrorServicio(f"El servicio rechazó la petición (HTTP {resp.status_code}) en {destino}. "
                                "Defina un token válido en PARAMETROS_TOKEN.")
        if not resp.ok:
            raise ErrorServicio(f"HTTP {resp.status_code} en {resp.url}: {resp.text[:300]}")
        try:
            return resp.json()
        except ValueError as e:
            raise ErrorServicio(f"Respuesta no JSON en {resp.url}: {resp.text[:300]}") from e

    def _uno(self, ruta: str):
        cuerpo = self._get(ruta)
        if cuerpo is None or (isinstance(cuerpo, dict) and cuerpo.get("Success") is False):
            return None
        registro = desenvolver(cuerpo)
        return registro if isinstance(registro, dict) and registro else None

    def tipo_parametro(self, id_tipo: int):
        return self._uno(f"tipo_parametro/{id_tipo}")

    def parametro(self, id_parametro: int):
        return self._uno(f"parametro/{id_parametro}")

    def _lista(self, params: dict) -> list:
        cuerpo = self._get("parametro", params)
        datos = desenvolver(cuerpo) if cuerpo is not None else []
        # Sin resultados el servicio responde Data: [{}]
        return [r for r in (datos or []) if isinstance(r, dict) and r]

    def parametros_por_tipo(self, id_tipo: int) -> tuple[list, int]:
        """Pagina con offset (orden estable por Id) hasta una página incompleta."""
        registros, offset, paginas = [], 0, 0
        while paginas < MAX_PAGINAS:
            pagina = self._lista({"query": f"TipoParametroId:{id_tipo}", "limit": LIMITE_PAGINA,
                                  "offset": offset, "sortby": "Id", "order": "asc"})
            paginas += 1
            registros.extend(pagina)
            if len(pagina) < LIMITE_PAGINA:
                return registros, paginas
            offset += LIMITE_PAGINA
        raise ErrorServicio(f"El tipo {id_tipo} superó {MAX_PAGINAS} páginas; revise la paginación.")

    def total_limit0(self, id_tipo: int) -> int:
        return len(self._lista({"query": f"TipoParametroId:{id_tipo}", "limit": 0, "fields": "Id"}))


def id_tipo_de(parametro: dict):
    tipo = parametro.get("TipoParametroId")
    return tipo.get("Id") if isinstance(tipo, dict) else None


def agrupar_variables(variables: list[str]) -> str:
    """ESTADOS_INTERNOS.BORRADOR, ESTADOS_INTERNOS.RECHAZADO -> ESTADOS_INTERNOS.* (2)."""
    grupos: dict[str, int] = {}
    for v in variables:
        clave = v.split(".")[0] + ".*" if "." in v else v
        grupos[clave] = grupos.get(clave, 0) + 1
    return ", ".join(f"{k} ({n})" if k.endswith(".*") else k for k, n in grupos.items())


def nombre_hoja(id_tipo: int, nombre: str, usados: set) -> str:
    base = re.sub(r"[\[\]:*?/\\]", " ", f"{id_tipo} {nombre}")
    base = re.sub(r"\s+", " ", base).strip().strip("'")[:31].rstrip()
    candidato, n = base, 2
    while candidato.lower() in usados:
        sufijo = f" ({n})"
        candidato = base[:31 - len(sufijo)].rstrip() + sufijo
        n += 1
    usados.add(candidato.lower())
    return candidato


def escribir_cabecera(ws, columnas: list[str]) -> None:
    ws.append(columnas)
    for celda in ws[1]:
        celda.font = FUENTE_CABECERA
        celda.fill = RELLENO_CABECERA
        celda.border = BORDE
        celda.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"


def ajustar_anchos(ws, filas: int, columna_ajustada: int | None = None) -> None:
    for i, celdas in enumerate(ws.iter_cols(min_row=1, max_row=filas), start=1):
        # La cabecera va en negrita: se le da un poco más de ancho que al contenido
        largo = max([len(str(c.value)) * (1.2 if c.row == 1 else 1) for c in celdas if c.value is not None],
                    default=0)
        tope = ANCHO_MAXIMO_DESCRIPCION if i == columna_ajustada else ANCHO_MAXIMO
        ws.column_dimensions[get_column_letter(i)].width = max(ANCHO_MINIMO, min(round(largo) + 2, tope))


def formatear_cuerpo(ws, ultima: int, columnas_ajustadas: tuple) -> None:
    """Bordes, texto ajustado y alto de fila. El alto se fija porque LibreOffice no lo
    recalcula al abrir el archivo y cortaría el texto ajustado."""
    for fila in ws.iter_rows(min_row=2, max_row=ultima):
        lineas = 1
        for celda in fila:
            celda.border = BORDE
            ajustada = celda.column in columnas_ajustadas
            celda.alignment = Alignment(vertical="top", wrap_text=ajustada)
            if ajustada and celda.value:
                ancho = ws.column_dimensions[celda.column_letter].width - 1
                lineas = max(lineas, math.ceil(len(str(celda.value)) / ancho))
        if lineas > 1:
            ws.row_dimensions[fila[0].row].height = ALTO_LINEA * lineas


def hoja_tipo(wb: Workbook, nombre: str, registros: list) -> None:
    ws = wb.create_sheet(nombre)
    escribir_cabecera(ws, COLUMNAS)
    for r in sorted(registros, key=lambda r: r["Id"]):
        ws.append([r["Id"], r.get("Nombre") or "", r.get("Descripcion") or "",
                   r.get("CodigoAbreviacion") or "", None, None])
    ultima = ws.max_row
    ajustar_anchos(ws, ultima, columna_ajustada=3)
    ws.column_dimensions["E"].width = ws.column_dimensions["F"].width = 22
    formatear_cuerpo(ws, ultima, columnas_ajustadas=(2, 3))
    ws.auto_filter.ref = f"A1:F{ultima}"
    validacion = DataValidation(type="list", formula1=OPCIONES_APLICA, allow_blank=True,
                                error="Seleccione Sí o No.", errorTitle="Valor no válido",
                                prompt="Sí o No", promptTitle="¿Aplica?")
    validacion.add(f"E2:F{ultima + MARGEN_VALIDACION}")
    ws.add_data_validation(validacion)


def hoja_indice(ws, tipos: list, url: str, fecha: str, total: int) -> None:
    ws.title = "Índice"
    escribir_cabecera(ws, COLUMNAS_INDICE)
    for t in tipos:
        ws.append([t["id"], t["nombre"], t["variable"], t["cantidad"], t["hoja"]])
        celda = ws.cell(row=ws.max_row, column=5)
        celda.hyperlink = Hyperlink(ref=celda.coordinate, location=f"'{t['hoja']}'!A1", display=t["hoja"])
        celda.style = "Hyperlink"
    ultima = ws.max_row
    ajustar_anchos(ws, ultima, columna_ajustada=3)
    formatear_cuerpo(ws, ultima, columnas_ajustadas=(3,))
    ws.auto_filter.ref = f"A1:E{ultima}"
    fuente = cfg.FUENTE_ENTORNO
    metadatos = [
        ("Ambiente", cfg.AMBIENTE),
        ("URL usada", url),
        ("Fecha de extracción", fecha),
        ("Total de parámetros", total),
        ("Fuente de las constantes",
         f"{fuente['repositorio']} ({fuente['rama']}, commit {fuente['commit']}) {fuente['archivo']}"),
    ]
    # Etiquetas en B y valores en C para no ensanchar la columna del id
    fila = ultima + 2
    for etiqueta, valor in metadatos:
        ws.cell(row=fila, column=2, value=etiqueta).font = Font(bold=True)
        ws.cell(row=fila, column=3, value=valor).alignment = Alignment(horizontal="left")
        fila += 1
    ancho_etiquetas = round(max(len(e) for e, _ in metadatos) * 1.2) + 2
    ws.column_dimensions["B"].width = max(ws.column_dimensions["B"].width, ancho_etiquetas)


def sino(valor: bool) -> str:
    return "Sí" if valor else "No"


def revisar_calidad(tipos: dict) -> list[str]:
    """Señales para la depuración: nombres o códigos repetidos dentro de un tipo y campos vacíos."""
    hallazgos = []
    for t in sorted(tipos.values(), key=lambda t: t["id"]):
        registros = sorted(t["registros"], key=lambda r: r["Id"])
        for campo, etiqueta in (("Nombre", "Nombre"), ("CodigoAbreviacion", "Código abreviación")):
            grupos: dict[str, list] = {}
            for r in registros:
                valor = (r.get(campo) or "").strip()
                if valor:
                    grupos.setdefault(valor.lower(), []).append(r)
            for repetidos in (g for g in grupos.values() if len(g) > 1):
                ids = ", ".join(str(r["Id"]) for r in repetidos)
                hallazgos.append(f"Tipo {t['id']} ({t['nombre']}): {etiqueta} «{repetidos[0][campo].strip()}» "
                                 f"repetido en {len(repetidos)} parámetros ({ids}).")
        for campo, etiqueta in (("CodigoAbreviacion", "código abreviación"), ("Descripcion", "descripción")):
            vacios = [str(r["Id"]) for r in registros if not (r.get(campo) or "").strip()]
            if vacios:
                hallazgos.append(f"Tipo {t['id']} ({t['nombre']}): sin {etiqueta} en {', '.join(vacios)}.")
    return hallazgos


def escribir_reporte(ruta: Path, url: str, fecha: str, tipos: dict, especificos: list, archivo_excel: str) -> list:
    diferencias = []
    lineas = [
        "# Reporte de validación — datos paramétricos ARGO v2 (issue #377)",
        "",
        f"- **Fecha de extracción:** {fecha}",
        f"- **Ambiente:** {cfg.AMBIENTE}",
        f"- **URL:** {url}",
        f"- **Fuente de las constantes:** `{cfg.FUENTE_ENTORNO['repositorio']}`, rama "
        f"`{cfg.FUENTE_ENTORNO['rama']}`, commit `{cfg.FUENTE_ENTORNO['commit']}`, "
        f"`{cfg.FUENTE_ENTORNO['archivo']}`",
        f"- **Excel generado:** `{archivo_excel}`",
        "",
        "## 1. Tipos de parámetro del entorno",
        "",
        "| Variable | Id | Existe | Nombre (tipo_parametro) | Activo |",
        "|---|---|---|---|---|",
    ]
    for t in sorted((t for t in tipos.values() if t["origen"] == "entorno"), key=lambda t: t["id"]):
        lineas.append(f"| `{t['variable']}` | {t['id']} | {sino(t['existe'])} | {t['nombre']} | "
                      f"{sino(t['activo']) if t['existe'] else '—'} |")
        if not t["existe"]:
            diferencias.append(f"El tipo `{t['variable']}` ({t['id']}) no existe en tipo_parametro.")

    lineas += ["", "## 2. Parámetros específicos del entorno", "",
               "| Variable | Id | Existe | Nombre | Activo | Tipo real | Tipo esperado | Coincide |",
               "|---|---|---|---|---|---|---|---|"]
    for e in especificos:
        if not e["existe"]:
            lineas.append(f"| `{e['variable']}` | {e['id']} | No | — | — | — | {e['esperado'] or '—'} | — |")
            diferencias.append(f"El parámetro `{e['variable']}` ({e['id']}) no existe en parametro.")
            continue
        tipo = tipos.get(e["tipo"], {})
        coincide = "—" if e["esperado"] is None else sino(e["tipo"] == e["esperado"])
        lineas.append(f"| `{e['variable']}` | {e['id']} | Sí | {e['nombre']} | {sino(e['activo'])} | "
                      f"{e['tipo']} {tipo.get('nombre', '')} | {e['esperado'] or '—'} | {coincide} |")
        if e["esperado"] is not None and e["tipo"] != e["esperado"]:
            diferencias.append(f"`{e['variable']}` ({e['id']}) es del tipo {e['tipo']}, se esperaba {e['esperado']}.")
        if not e["activo"]:
            diferencias.append(f"El parámetro `{e['variable']}` ({e['id']}, {e['nombre']}) está inactivo.")
    lineas += ["", "El tipo esperado sale del uso de la constante en el MF (con qué lista se compara); "
               "«—» indica que el MF no permite inferirlo."]

    descubiertos = sorted((t for t in tipos.values() if t["origen"] == "descubierto"), key=lambda t: t["id"])
    lineas += ["", "## 3. Tipos descubiertos a partir de los parámetros específicos", ""]
    if descubiertos:
        lineas += ["| Id | Nombre | Activo | Constantes que lo referencian | Parámetros |", "|---|---|---|---|---|"]
        for t in descubiertos:
            lineas.append(f"| {t['id']} | {t['nombre']} | {sino(t['activo'])} | "
                          f"{', '.join(f'`{v}`' for v in t['variables'])} | {t['cantidad']} |")
    else:
        lineas.append("Ninguno: todos los parámetros específicos pertenecen a tipos del entorno.")

    lineas += ["", "## 4. Conteo por tipo y verificación de la paginación", "",
               f"Paginación con `limit={LIMITE_PAGINA}` y `offset`, ordenada por `Id`, frente a una consulta "
               "con `limit=0`. Ambas sin filtro de `Activo`.", "",
               "| Id | Tipo | Hoja | Paginación | Páginas | limit=0 | Coincide | Activos | Inactivos |",
               "|---|---|---|---|---|---|---|---|---|"]
    total_pag = total_l0 = 0
    for t in sorted(tipos.values(), key=lambda t: t["id"]):
        total_pag += t["cantidad"]
        total_l0 += t["limit0"]
        coincide = t["cantidad"] == t["limit0"]
        lineas.append(f"| {t['id']} | {t['nombre']} | {t['hoja']} | {t['cantidad']} | {t['paginas']} | "
                      f"{t['limit0']} | {sino(coincide)} | {t['activos']} | {t['cantidad'] - t['activos']} |")
        if not coincide:
            diferencias.append(f"Tipo {t['id']}: la paginación trajo {t['cantidad']} y limit=0 trajo {t['limit0']}.")
        if t["existe"] and not t["activo"]:
            diferencias.append(f"El tipo {t['id']} ({t['nombre']}) está inactivo en tipo_parametro.")
        if t["cantidad"] == 0:
            diferencias.append(f"Tipo {t['id']} ({t['nombre']}) no tiene parámetros.")
        elif t["activos"] == 0:
            diferencias.append(f"Tipo {t['id']} ({t['nombre']}): todos sus parámetros ({t['cantidad']}) están inactivos.")
        if t["duplicados"]:
            diferencias.append(f"Tipo {t['id']}: {t['duplicados']} registros repetidos entre páginas (se dejó uno).")
        if t["otro_tipo"]:
            diferencias.append(f"Tipo {t['id']}: {t['otro_tipo']} registros devueltos traen otro TipoParametroId.")
    lineas += [f"| **Total** | | | **{total_pag}** | | **{total_l0}** | **{sino(total_pag == total_l0)}** | | |",
               "", "Los inactivos se exportan en el Excel igual que los activos, sin marca que los distinga.",
               "", "## 5. Diferencias y observaciones", ""]
    lineas += [f"- {d}" for d in diferencias] or ["Sin diferencias."]

    calidad = revisar_calidad(tipos)
    lineas += ["", "## 6. Posibles inconsistencias para la depuración", "",
               "Revisión automática de nombres y códigos repetidos dentro de cada tipo y de campos vacíos. "
               "No siempre son errores (p. ej. ordinales con el mismo prefijo); se listan para que negocio los revise.",
               ""]
    lineas += [f"- {h}" for h in calidad] or ["Sin hallazgos."]

    lineas += ["", "## 7. Constantes del entorno excluidas", "", "| Constante | Motivo |", "|---|---|"]
    lineas += [f"| `{k}` | {v} |" for k, v in cfg.EXCLUIDAS.items()]
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return diferencias


def main() -> int:
    cargar_env(DIR_SCRIPT / ".env")
    parser = argparse.ArgumentParser(description="Consolida en Excel los datos paramétricos de ARGO v2 (issue #377).")
    parser.add_argument("--url", default=os.environ.get("PARAMETROS_URL") or cfg.URL_POR_DEFECTO,
                        help="URL base de parametros_crud (por defecto PARAMETROS_URL o la de pruebas)")
    parser.add_argument("--salida", type=Path, default=DIR_SCRIPT / "salida",
                        help="directorio donde se escriben el Excel y el reporte (por defecto ./salida)")
    args = parser.parse_args()

    cliente = ClienteParametros(args.url, os.environ.get("PARAMETROS_TOKEN", ""))
    ahora = datetime.datetime.now().astimezone()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S %z")
    print(f"Extractor de datos paramétricos ARGO v2 — {fecha}")
    print(f"Servicio: {cliente.url}\n")

    try:
        tipos: dict[int, dict] = {}

        def registrar_tipo(id_tipo: int, variable: str, origen: str) -> dict:
            registro = cliente.tipo_parametro(id_tipo)
            tipos[id_tipo] = {"id": id_tipo, "origen": origen, "variables": [variable],
                              "existe": registro is not None,
                              "nombre": (registro or {}).get("Nombre") or "(no existe)",
                              "activo": bool((registro or {}).get("Activo"))}
            return tipos[id_tipo]

        print("1. Tipos de parámetro del entorno")
        for variable, id_tipo in cfg.TIPOS_PARAMETRO.items():
            t = registrar_tipo(id_tipo, variable, "entorno")
            print(f"   {id_tipo:>4} {variable:<26} {t['nombre'] if t['existe'] else 'NO EXISTE'}")

        print("\n2. Parámetros específicos del entorno")
        especificos = []
        for variable, (id_param, esperado) in cfg.PARAMETROS_ESPECIFICOS.items():
            p = cliente.parametro(id_param)
            e = {"variable": variable, "id": id_param, "esperado": esperado, "existe": p is not None,
                 "nombre": (p or {}).get("Nombre", ""), "activo": bool((p or {}).get("Activo")),
                 "tipo": id_tipo_de(p) if p else None}
            especificos.append(e)
            nota = ""
            if e["tipo"] is not None:
                if e["tipo"] in tipos:
                    if variable not in tipos[e["tipo"]]["variables"]:
                        tipos[e["tipo"]]["variables"].append(variable)
                else:
                    registrar_tipo(e["tipo"], variable, "descubierto")
                    nota = "  <- tipo nuevo"
            print(f"   {id_param:>5} {variable:<56} " +
                  (f"tipo {e['tipo']} ({tipos[e['tipo']]['nombre']}){nota}" if e["existe"] else "NO EXISTE"))

        print("\n3. Parámetros por tipo (paginación vs limit=0)")
        for id_tipo in sorted(tipos):
            t = tipos[id_tipo]
            crudos, paginas = cliente.parametros_por_tipo(id_tipo)
            unicos = {r["Id"]: r for r in crudos}
            t.update(registros=list(unicos.values()), paginas=paginas, cantidad=len(unicos),
                     duplicados=len(crudos) - len(unicos), limit0=cliente.total_limit0(id_tipo),
                     activos=sum(1 for r in unicos.values() if r.get("Activo")),
                     otro_tipo=sum(1 for r in unicos.values() if id_tipo_de(r) not in (None, id_tipo)))
            estado = "OK" if t["cantidad"] == t["limit0"] else "DIFERENCIA"
            print(f"   {id_tipo:>4} {t['nombre'][:30]:<30} {t['cantidad']:>4} registros "
                  f"({paginas} pág.)  limit=0: {t['limit0']:>4}  {estado}")
    except ErrorServicio as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 2

    usados = {"índice"}
    for id_tipo in sorted(tipos):
        t = tipos[id_tipo]
        t["hoja"] = nombre_hoja(id_tipo, t["nombre"], usados)
        t["variable"] = t["variables"][0] if t["origen"] == "entorno" else \
            "Descubierto vía " + agrupar_variables(t["variables"])

    wb = Workbook()
    orden = [tipos[i] for i in sorted(tipos)]
    total = sum(t["cantidad"] for t in orden)
    hoja_indice(wb.active, orden, cliente.url, fecha, total)
    for t in orden:
        hoja_tipo(wb, t["hoja"], t["registros"])

    args.salida.mkdir(parents=True, exist_ok=True)
    archivo = args.salida / f"consolidado_parametros_argo_v2_{ahora:%Y-%m-%d}.xlsx"
    wb.save(archivo)
    diferencias = escribir_reporte(args.salida / "reporte_validacion.md", cliente.url, fecha,
                                   tipos, especificos, archivo.name)

    print(f"\n{len(orden)} hojas de tipo, {total} parámetros.")
    print(f"Excel:   {archivo}")
    print(f"Reporte: {args.salida / 'reporte_validacion.md'}")
    print(f"Diferencias u observaciones: {len(diferencias)}" + (" (ver sección 5 del reporte)" if diferencias else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
