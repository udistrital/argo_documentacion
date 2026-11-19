#!/usr/bin/env python3
"""Genera ddl/carga-inicial-unidad-ejecutora.sql desde el consolidado depurado por negocio.

Toma la columna "Aplica para IDEXUD" del Excel adjunto a la issue #384
(consolidado_parametros_argo_v2_2026-10-13 (1).xlsx). Solo se cargan las filas
marcadas Sí (SI, si o Sí). Las celdas con texto libre y las filas sin Id quedan
en el resumen para revisión y no se cargan. La columna de Rectoría está vacía
(pendiente de la #383), así que Rectoría no se carga.

Uso:
    python3 scripts/genera_carga_unidad_ejecutora.py <consolidado_depurado.xlsx>
"""
import sys
import unicodedata
from pathlib import Path

import openpyxl

SALIDA = Path(__file__).resolve().parent.parent / "ddl" / "carga-inicial-unidad-ejecutora.sql"
IDEXUD = 6819
RECTORIA = 6818


def normaliza(valor):
    if valor is None or str(valor).strip() == "":
        return "vacío"
    texto = unicodedata.normalize("NFKD", str(valor).strip().lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    if texto == "si":
        return "Sí"
    if texto in ("no", "no aplica"):
        return "No"
    return "texto"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    libro = openpyxl.load_workbook(sys.argv[1], read_only=True)
    filas, texto_libre, por_tipo = [], [], {}
    for hoja in libro.worksheets[1:]:
        tipo = hoja.title.split(" ", 1)
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            if not fila or fila[0] is None:
                continue
            marca = normaliza(fila[5])
            if marca == "Sí":
                filas.append((int(fila[0]), str(fila[1]).strip(), hoja.title))
                por_tipo[hoja.title] = por_tipo.get(hoja.title, 0) + 1
            elif marca == "texto":
                texto_libre.append((int(fila[0]), str(fila[1]).strip(), str(fila[5]).strip()))

    lineas = [
        "-- Carga inicial de unidad ejecutora (#384). Generado por scripts/genera_carga_unidad_ejecutora.py",
        "-- desde el consolidado depurado por negocio (columna \"Aplica para IDEXUD\").",
        "-- Rectoría (6818): pendiente de la #383; no se carga. Unidad ejecutora 03: pendiente.",
        "-- Requiere el search_path del esquema del modelo (contratacion o el que se defina).",
        "",
        "BEGIN;",
        "",
        "-- Formato del número de contrato: valores actuales de gestion_contractual_mid/src/contrato-general/conf.ts",
        "INSERT INTO configuracion_unidad_ejecutora (unidad_ejecutora_id, prefijo_numero_contrato, sufijo_numero_contrato)",
        f"VALUES ({RECTORIA}, '', ''), ({IDEXUD}, 'ID-', '');",
        "",
        f"-- Parámetros que aplican a IDEXUD ({len(filas)} filas)",
        "INSERT INTO parametro_unidad_ejecutora (parametro_id, unidad_ejecutora_id) VALUES",
    ]
    valores = [f"    ({pid}, {IDEXUD})  -- {hoja}: {nombre.replace(chr(10), ' ')}" for pid, nombre, hoja in filas]
    for i, v in enumerate(valores):
        coma = "," if i < len(valores) - 1 else ";"
        # La coma va antes del comentario de la línea
        cuerpo, comentario = v.split("  -- ", 1)
        lineas.append(f"{cuerpo}{coma}  -- {comentario}")
    lineas += ["", "COMMIT;", ""]
    if texto_libre:
        lineas.append("-- No cargados (texto libre en la columna de IDEXUD, por revisar con negocio):")
        lineas += [f"--   {pid} {nombre}: \"{texto}\"" for pid, nombre, texto in texto_libre]
        lineas.append("")
    SALIDA.write_text("\n".join(lineas), encoding="utf-8")
    print(f"{SALIDA.name}: {len(filas)} parámetros de IDEXUD en {len(por_tipo)} tipos; {len(texto_libre)} con texto libre")
    for hoja, total in por_tipo.items():
        print(f"  {hoja}: {total}")


if __name__ == "__main__":
    main()
