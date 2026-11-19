#!/usr/bin/env node
// Genera diccionario-datos.md a partir de modelo-argo-v2.dbml (A13 de la #384).
//
// Uso (desde gestion-contractual/modelo-datos-v2/):
//   npm install --prefix /tmp/dbml @dbml/core@3
//   NODE_PATH=/tmp/dbml/node_modules node scripts/genera_diccionario.js
//
// No se edita a mano: si cambia el modelo, se cambia el DBML y se vuelve a generar.

const fs = require('fs');
const path = require('path');
const { Parser } = require('@dbml/core');

const BASE = path.resolve(__dirname, '..');
const DBML = path.join(BASE, 'modelo-argo-v2.dbml');
const SALIDA = path.join(BASE, 'diccionario-datos.md');

const AUDITORIA = {
  id: 'Identificador del registro (llave primaria)',
  activo: 'Indica si el registro está activo (borrado lógico)',
  fecha_creacion: 'Fecha y hora de creación del registro',
  fecha_modificacion: 'Fecha y hora de la última modificación; al crear es igual a fecha_creacion',
};

const ORIGENES = [
  ['Parámetros CRUD', 'Parámetros CRUD'],
  ['Terceros', 'Terceros'],
  ['OIKOS', 'OIKOS'],
  ['SiCapital', 'SiCapital'],
  ['Gestor Documental', 'Gestor Documental'],
  ['ARGO v1', 'ARGO v1 (migración)'],
  ['referencia externa por confirmar', 'Externa, por confirmar'],
];

function tipo(campo) {
  // type_name ya incluye la longitud o la precisión, por ejemplo varchar(50)
  return campo.type.type_name;
}

function porDefecto(campo) {
  if (!campo.dbdefault) return '';
  const d = campo.dbdefault;
  if (d.type === 'string') return `'${d.value}'`;
  return String(d.value);
}

function origen(campo, fks) {
  if (fks.has(campo.name)) return `FK a ${fks.get(campo.name)}`;
  if (campo.pk || campo.name in AUDITORIA) return 'Auditoría / llave';
  const nota = campo.note || '';
  for (const [prefijo, etiqueta] of ORIGENES) {
    if (nota.startsWith(prefijo) || nota.includes(`(${prefijo}`) || nota.includes(`${prefijo},`)) return etiqueta;
  }
  return 'ARGO v2';
}

function celda(texto) {
  return String(texto || '').replace(/\|/g, '\\|').replace(/\n/g, ' ');
}

function main() {
  const db = new Parser().parse(fs.readFileSync(DBML, 'utf8'), 'dbmlv2');
  const esquema = db.schemas[0];

  const fksPorTabla = new Map();
  for (const ref of esquema.refs) {
    // El extremo que no es la PK lleva la FK
    const [a, b] = ref.endpoints;
    const origenFk = a.fieldNames[0] === 'id' && b.fieldNames[0] !== 'id' ? b : a;
    const destino = origenFk === a ? b : a;
    if (!fksPorTabla.has(origenFk.tableName)) fksPorTabla.set(origenFk.tableName, new Map());
    fksPorTabla.get(origenFk.tableName).set(origenFk.fieldNames[0], `${destino.tableName}.${destino.fieldNames[0]} (${ref.name})`);
  }

  const grupoDe = new Map();
  for (const g of esquema.tableGroups) for (const t of g.tables) grupoDe.set(t.name, g.name);

  const out = [];
  out.push('# Diccionario de datos — ARGO v2, gestión contractual (#384 y #389)');
  out.push('');
  out.push('> Generado por `scripts/genera_diccionario.js` desde `modelo-argo-v2.dbml`. No se edita a mano.');
  out.push('');
  out.push(`${esquema.tables.length} tablas, ${esquema.refs.length} relaciones. Base de datos y esquema provisionales: \`administrativa\` / \`contratacion\` (supuesto S3).`);
  out.push('');
  out.push('Columnas de la tabla de cada entidad: nombre, tipo PostgreSQL, si admite nulos, valor por defecto, descripción y origen del dato. "Origen" indica el sistema al que apunta una referencia externa (integer sin FK física), la tabla de una FK, o "ARGO v2" si el dato es propio.');
  out.push('');
  out.push('## Contenido');
  out.push('');
  for (const g of esquema.tableGroups) {
    out.push(`- **${g.name.replace(/_/g, ' ')}**: ${g.tables.map((t) => `[${t.name}](#${t.name})`).join(', ')}`);
  }
  out.push('');

  for (const tabla of esquema.tables) {
    const fks = fksPorTabla.get(tabla.name) || new Map();
    out.push(`## ${tabla.name}`);
    out.push('');
    out.push(`${tabla.note || ''}`);
    out.push('');
    out.push(`Dominio: ${(grupoDe.get(tabla.name) || '').replace(/_/g, ' ')}.`);
    out.push('');
    out.push('| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |');
    out.push('|---|---|---|---|---|---|');
    for (const campo of tabla.fields) {
      const nulo = campo.pk || campo.not_null ? 'No' : 'Sí';
      const desc = campo.note || AUDITORIA[campo.name] || '';
      const defecto = campo.increment || campo.type.type_name === 'serial' ? 'secuencia' : porDefecto(campo);
      out.push(`| ${campo.name} | ${tipo(campo)} | ${nulo} | ${celda(defecto)} | ${celda(desc)} | ${celda(origen(campo, fks))} |`);
    }
    const restricciones = [`\`pk_${tabla.name}\` PRIMARY KEY (id)`];
    for (const [col, destino] of fks) restricciones.push(`FK \`${col}\` → ${destino}`);
    for (const idx of tabla.indexes) {
      const cols = idx.columns.map((c) => c.value).join(', ');
      restricciones.push(`${idx.unique ? 'UNIQUE' : 'Índice'} \`${idx.name}\` (${cols})`);
    }
    out.push('');
    out.push(`Restricciones e índices: ${restricciones.join('; ')}.`);
    out.push('');
  }

  if (db.notes && db.notes.length) {
    out.push('## Temas en stand by o pendientes');
    out.push('');
    out.push('No se modelan; están como notas en el diagrama.');
    out.push('');
    for (const nota of db.notes) {
      const lineas = nota.content.trim().split('\n').map((l) => l.trim()).filter(Boolean);
      out.push(`- **${lineas[0]}**. ${lineas.slice(1).join(' ')}`);
    }
    out.push('');
  }

  fs.writeFileSync(SALIDA, out.join('\n'));
  const columnas = esquema.tables.reduce((n, t) => n + t.fields.length, 0);
  console.log(`diccionario-datos.md: ${esquema.tables.length} tablas, ${columnas} columnas`);
}

main();
