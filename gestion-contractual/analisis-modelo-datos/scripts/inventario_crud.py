"""Inventario del modelo de datos de gestion_contractual_crud.

Extrae tres vistas del modelo y las deja en JSON para construir la matriz:
  - DDL de sql/creacion-tablas.sql
  - Entidades TypeORM de src/**/entities/*.ts
  - Endpoints declarados en los controladores

Uso:
    python3 inventario_crud.py <ruta_repo_crud> <salida.json>
"""

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

# Tipos TypeORM inferidos desde el tipo TypeScript cuando @Column no declara `type`
TS_A_PG = {"number": "integer", "string": "varchar", "boolean": "boolean", "Date": "timestamp"}


def parsear_ddl(sql: str) -> dict:
    tablas = {}
    for m in re.finditer(r"CREATE TABLE (\w+) \((.*?)\n\);", sql, re.S):
        nombre, cuerpo = m.group(1), m.group(2)
        columnas = []
        for linea in cuerpo.split("\n"):
            linea = linea.strip().rstrip(",")
            if not linea or linea.startswith("--"):
                continue
            partes = linea.split()
            col, resto = partes[0], " ".join(partes[1:])
            tipo = re.match(r"([A-Z]+(?:\(\d+(?:,\d+)?\))?)", resto).group(1)
            ref = re.search(r"REFERENCES (\w+)\((\w+)\)", resto)
            default = re.search(r"DEFAULT ([\w()]+)", resto)
            columnas.append({
                "columna": col,
                "tipo": tipo.lower(),
                "nullable": "NOT NULL" not in resto and "PRIMARY KEY" not in resto,
                "pk": "PRIMARY KEY" in resto,
                "unique": "UNIQUE" in resto,
                "default": default.group(1) if default else None,
                "fk": f"{ref.group(1)}.{ref.group(2)}" if ref else None,
            })
        tablas[nombre] = {"columnas": columnas}
    comentarios = {}
    for m in re.finditer(r"COMMENT ON COLUMN (\w+)\.(\w+) IS '(.*?)';", sql):
        comentarios[f"{m.group(1)}.{m.group(2)}"] = m.group(3)
    for m in re.finditer(r"COMMENT ON TABLE (\w+) IS '(.*?)';", sql):
        if m.group(1) in tablas:
            tablas[m.group(1)]["comentario"] = m.group(2)
    for t, d in tablas.items():
        for c in d["columnas"]:
            c["comentario"] = comentarios.get(f"{t}.{c['columna']}")
    indices = re.findall(r"CREATE INDEX (\w+) ON (\w+)\((\w+)\);", sql)
    return {"tablas": tablas, "indices": [dict(nombre=i, tabla=t, columna=c) for i, t, c in indices]}


def _opcion(bloque: str, clave: str):
    m = re.search(rf"\b{clave}\s*:\s*('([^']*)'|[\w.]+|\(\)\s*=>\s*'[^']*')", bloque)
    if not m:
        return None
    return m.group(2) if m.group(2) is not None else m.group(1)


def parsear_entidad(ts: str, archivo: str) -> dict | None:
    ent = re.search(r"@Entity\(\s*(?:'(\w+)')?\s*\)\s*export class (\w+)", ts)
    if not ent:
        return None
    clase = ent.group(2)
    # Sin nombre explícito TypeORM usa snake_case de la clase
    tabla = ent.group(1) or re.sub(r"(?<!^)(?=[A-Z])", "_", clase).lower()
    columnas, relaciones = [], []
    patron = re.compile(
        r"@(PrimaryGeneratedColumn|Column|CreateDateColumn|UpdateDateColumn|ManyToOne|OneToOne|OneToMany)"
        r"\((.*?)\)\s*\n((?:\s*@(?!Column|PrimaryGeneratedColumn|CreateDateColumn|UpdateDateColumn|ManyToOne|OneToOne|OneToMany)\w+\((?:.|\n)*?\)\s*\n)*?)\s*(\w+)\s*:\s*([^;=]+);",
        re.S,
    )
    for m in patron.finditer(ts):
        deco, args, extra, prop, tipo_ts = m.groups()
        tipo_ts = tipo_ts.split("|")[0].strip()
        if deco in ("ManyToOne", "OneToOne", "OneToMany"):
            join = re.search(r"@JoinColumn\(\{\s*name:\s*'(\w+)'", extra)
            relaciones.append({"tipo": deco, "propiedad": prop, "destino": tipo_ts.replace("[]", ""),
                               "join_column": join.group(1) if join else None})
            continue
        if deco == "PrimaryGeneratedColumn":
            estrategia = re.search(r"'(\w+)'", args)
            columnas.append({"columna": prop, "propiedad": prop, "pk": True, "nullable": False,
                             "tipo": "uuid" if estrategia and estrategia.group(1) == "uuid" else "serial",
                             "default": None})
            continue
        nombre = _opcion(args, "name") or prop
        tipo = _opcion(args, "type")
        if not tipo:
            m_tipo = re.match(r"\s*'(\w+)'", args)
            tipo = m_tipo.group(1) if m_tipo else TS_A_PG.get(tipo_ts, tipo_ts)
        if deco in ("CreateDateColumn", "UpdateDateColumn"):
            tipo = "timestamp"
        length, precision, scale = _opcion(args, "length"), _opcion(args, "precision"), _opcion(args, "scale")
        if length:
            tipo += f"({length})"
        elif precision:
            tipo += f"({precision},{scale or 0})"
        nullable = _opcion(args, "nullable") == "true"
        default = _opcion(args, "default")
        if deco in ("CreateDateColumn", "UpdateDateColumn"):
            default = "now()"
        columnas.append({"columna": nombre, "propiedad": prop, "pk": False, "nullable": nullable,
                         "tipo": tipo.lower().replace("decimal", "numeric"), "default": default})
    return {"clase": clase, "tabla": tabla, "archivo": archivo, "columnas": columnas, "relaciones": relaciones}


def parsear_endpoints(repo: Path) -> list:
    endpoints = []
    for ctrl in sorted(repo.glob("src/**/*.controller.ts")):
        ts = ctrl.read_text(encoding="utf-8")
        base = re.search(r"@Controller\(\s*'([^']*)'\s*\)", ts)
        base = base.group(1) if base else ""
        for m in re.finditer(r"@(Get|Post|Put|Patch|Delete)\(\s*(?:'([^']*)')?\s*\)", ts):
            ruta = "/" + "/".join(p for p in [base, m.group(2) or ""] if p)
            endpoints.append({"controlador": ctrl.relative_to(repo).as_posix(),
                              "verbo": m.group(1).upper(), "ruta": ruta})
    return endpoints


def main():
    repo, salida = Path(sys.argv[1]), Path(sys.argv[2])
    ddl = parsear_ddl((repo / "sql/creacion-tablas.sql").read_text(encoding="utf-8"))
    entidades = []
    for f in sorted(repo.glob("src/**/entities/*.ts")):
        e = parsear_entidad(f.read_text(encoding="utf-8"), f.relative_to(repo).as_posix())
        if e:
            entidades.append(e)
    # Servicios que hacen DELETE físico en lugar de borrado lógico
    borrado_fisico = sorted(
        f.relative_to(repo).as_posix() for f in repo.glob("src/**/*.service.ts")
        if re.search(r"Repository\.delete\(", f.read_text(encoding="utf-8")))
    commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    data = {"commit": commit, "fecha": datetime.date.today().isoformat(), "ddl": ddl, "entidades": entidades,
            "endpoints": parsear_endpoints(repo), "borrado_fisico": borrado_fisico}
    salida.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"tablas DDL: {len(ddl['tablas'])} | entidades: {len(entidades)} | endpoints: {len(data['endpoints'])}")


if __name__ == "__main__":
    main()
