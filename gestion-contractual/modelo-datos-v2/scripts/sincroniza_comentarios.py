#!/usr/bin/env python3
"""Copia los COMMENT ON de los DDL a los scripts de migración.

- migracion-desde-v2.up.sql recibe los comentarios de ddl/creacion-tablas.sql (modelo nuevo).
- migracion-desde-v2.down.sql recibe los comentarios del DDL de develop de gestion_contractual_crud.

Uso:
    python3 scripts/sincroniza_comentarios.py <ruta a sql/creacion-tablas.sql de gestion_contractual_crud develop>

Reemplaza el bloque entre las marcas "-- inicio comentarios" y "-- fin comentarios"
(o la marca @@...@@ la primera vez), así que se puede volver a ejecutar.
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DDL_NUEVO = BASE / "ddl" / "creacion-tablas.sql"
UP = BASE / "ddl" / "migracion-desde-v2.up.sql"
DOWN = BASE / "ddl" / "migracion-desde-v2.down.sql"


def comentarios(ddl: str) -> str:
    """Devuelve las sentencias COMMENT ON de un DDL, una por línea."""
    lineas = [l.rstrip() for l in ddl.splitlines() if l.startswith("COMMENT ON ")]
    if not lineas:
        sys.exit("El DDL no tiene sentencias COMMENT ON")
    return "\n".join(lineas)


def inserta(destino: Path, marca: str, origen: str, bloque: str) -> None:
    texto = destino.read_text(encoding="utf-8")
    nuevo = (f"-- inicio comentarios (generado por scripts/sincroniza_comentarios.py desde {origen})\n"
             f"{bloque}\n"
             f"-- fin comentarios")
    patron = re.compile(r"-- inicio comentarios.*?-- fin comentarios", re.S)
    if patron.search(texto):
        texto = patron.sub(lambda _: nuevo, texto)
    elif marca in texto:
        texto = texto.replace(marca, nuevo)
    else:
        sys.exit(f"No encontré la marca en {destino.name}")
    destino.write_text(texto, encoding="utf-8")
    print(f"{destino.name}: {bloque.count(chr(10)) + 1} comentarios")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    develop = Path(sys.argv[1]).read_text(encoding="utf-8")
    inserta(UP, "-- @@COMENTARIOS_MODELO_NUEVO@@", "ddl/creacion-tablas.sql",
            comentarios(DDL_NUEVO.read_text(encoding="utf-8")))
    inserta(DOWN, "-- @@COMENTARIOS_DEVELOP@@", "gestion_contractual_crud develop sql/creacion-tablas.sql",
            comentarios(develop))


if __name__ == "__main__":
    main()
