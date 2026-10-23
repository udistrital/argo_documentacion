# Notas de migración — modelo de datos ARGO v2 refinado (#384)

Este documento acompaña a los scripts de `ddl/`. Explica cómo pasar al modelo refinado, tanto en una base nueva (#385) como en una base que ya tiene el modelo actual de `gestion_contractual_crud`.

## 1. Archivos

| Archivo | Uso |
|---|---|
| `ddl/creacion-tablas.sql` | DDL de la base nueva para la #385. Crea el esquema (`contratacion`, provisional) y las 17 tablas. |
| `ddl/migracion-desde-v2.up.sql` | Lleva una base con el DDL actual de develop (`gestion_contractual_crud` 9e20927) al modelo refinado, conservando los datos. |
| `ddl/migracion-desde-v2.down.sql` | Reverso del anterior. |
| `ddl/carga-inicial-unidad-ejecutora.sql` | Carga inicial de `configuracion_unidad_ejecutora` y de `parametro_unidad_ejecutora` para IDEXUD. |
| `scripts/genera_carga_unidad_ejecutora.py` | Regenera la carga inicial desde el consolidado depurado por negocio. |
| `scripts/sincroniza_comentarios.py` | Copia los `COMMENT ON` de los DDL a los scripts de migración. |
| `scripts/datos-prueba-migracion.sql` | Datos mínimos para probar la migración. |

## 2. Requisitos

- PostgreSQL 12 o superior. Las pruebas se hicieron con PostgreSQL 16.13.
- Ejecutar con `psql -v ON_ERROR_STOP=1`, con un usuario dueño de las tablas.
- **Base existente:**
  - Respaldo previo (`pg_dump`).
  - Ventana sin escrituras de los servicios (MID y MF detenidos o en mantenimiento).
  - `search_path` apuntando al esquema donde están hoy las tablas (por defecto `public`).
- **Base y esquema:** `administrativa` y `contratacion` son provisionales (supuesto S3). En `creacion-tablas.sql` el esquema se cambia en una sola línea (`SET search_path TO contratacion;`); el bloque `DO` siguiente crea ese esquema si no existe.

## 3. Orden de ejecución

### 3.1 Base nueva (#385)

1. Crear la base (provisional: `administrativa`).
2. `psql -v ON_ERROR_STOP=1 -d <base> -f ddl/creacion-tablas.sql`
3. `psql -v ON_ERROR_STOP=1 -d <base> -c "SET search_path TO contratacion" -f ddl/carga-inicial-unidad-ejecutora.sql`
4. Ajuste de códigos en Parámetros (sección 6), coordinado con el administrador de Parámetros.

### 3.2 Base con el modelo actual de develop

1. Respaldo: `pg_dump -Fc <base> > respaldo_antes_384.dump`.
2. `psql -v ON_ERROR_STOP=1 -d <base> -f ddl/migracion-desde-v2.up.sql`. El script corre en una transacción. Si una verificación falla, aborta con un mensaje y no aplica nada (sección 4).
3. Opcional, cuando se confirme el esquema: mover las tablas al esquema definitivo con `ALTER TABLE <tabla> SET SCHEMA contratacion;` para cada tabla. Las secuencias se mueven con su tabla.
4. Carga inicial de unidad ejecutora (paso 3 de 3.1).
5. Reverso, si hace falta: `psql -v ON_ERROR_STOP=1 -d <base> -f ddl/migracion-desde-v2.down.sql`.

## 4. Qué hace el up y qué verifica

**Verificaciones previas.** Cada una aborta con un mensaje que dice qué registros corregir.

| Verificación | Motivo |
|---|---|
| `contratista` sin `contrato_general_id`, o más de un contratista por contrato | La relación es 1 a 1 y la tabla se absorbe en `contrato_general` (ítem 16) |
| `lugar_ejecucion` sin contrato, o más de uno por contrato | Se absorbe en `contrato_general` (supuesto S7) |
| Contratos con `unidad_ejecutora_id` nulo | La columna pasa a NOT NULL (supuesto S4) |
| Duplicados de `(numero_contrato, vigencia)` con número no nulo | Se crea `uq_numero_contrato_vigencia_contrato_general` (A14). Los contratos sin número, que todavía no están suscritos, no chocan entre sí |
| Textos más largos que la nueva longitud | Los varchar sin longitud pasan a varchar(n) |
| Montos que no caben en `numeric(20,7)` o que perderían decimales | `numeric(16,2)` admite 14 dígitos enteros y `numeric(20,7)` 13; `valor_tasa_cambio` tenía 10 decimales |

**Cambios.** En este orden:

1. `contratista` y `lugar_ejecucion` se absorben en `contrato_general` y se eliminan.
2. Se agregan las columnas nuevas.
3. Se renombran columnas.
4. Se ajustan los tipos.
5. Las columnas de auditoría quedan `NOT NULL` con valor por defecto:
   - `activo` nulo pasa a `true`;
   - `fecha_modificacion` nula pasa a `fecha_creacion`.
6. Se renombran las restricciones e índices a la nomenclatura del lineamiento y se crean los índices de FK que faltaban.
7. Se crean las tablas nuevas.
8. Se reemplazan los comentarios.

El resultado es igual al de `creacion-tablas.sql`, salvo el orden físico de las columnas. Se verificó comparando el catálogo; ver `evidencias/04-migracion-up-down.txt`.

**Down.**
- Devuelve el esquema exacto de develop: `pg_dump --schema-only` idéntico.
- Recrea `contratista` y `lugar_ejecucion` desde las columnas absorbidas, una fila por contrato con datos. No recupera los `id`, `activo` ni fechas originales de esas filas.
- Se pierde lo que no existe en develop: columnas nuevas, `parametro_unidad_ejecutora`, `configuracion_unidad_ejecutora` y `huella_navegador`.

## 5. Datos de ARGO v1 (mapeo, sin scripts)

Fuente: diagrama del modelo de ARGO v1 compartido por el LT en la #356 (comentario del 28/09/2026) y comentarios del DDL actual. **Este mapeo no está validado con el LT;** lo marcado "Por confirmar" depende de esa validación.

| ARGO v1 | Modelo refinado | Estado |
|---|---|---|
| `contrato_general.numero_contrato` + `vigencia` (PK compuesta en v1) | `contrato_general.consecutivo_elaboracion` + `vigencia` | Por confirmar. El LT indicó que antes de la suscripción solo existe el consecutivo de elaboración |
| `contrato_suscrito.numero_contrato_suscrito` | `contrato_general.numero_contrato` (UNIQUE con `vigencia`) | Por confirmar. Generado por la RN de generación al pasar a SUSCRITO |
| `contrato_suscrito.fecha_suscripcion` | `contrato_general.fecha_suscripcion` (A6) | Por confirmar |
| `contrato_general.ordenador_gasto` (texto) | `ordenador_contrato` (`ordenador_argo_id`, `ordenador_sicapital_id`) | **Sin verificar.** El DDL actual dice que `ordenador_argo_id` y `ordenador_sicapital_id` apuntan a la tabla `ordenadores` de ARGO v1, pero esa tabla no aparece en el diagrama compartido. El LT pidió "validar soporte de migración ARGO v1" |
| `contrato_general.contratista` (entero) | `contrato_general.proveedor_numero_documento` (texto) | Por confirmar. En v1 es un identificador numérico; en v2 se guarda el número de documento con el que se consulta Ágora |
| `lugar_ejecucion` (`direccion`, `sede`, `dependencia`, `ciudad`) | `contrato_general.lugar_ejecucion_*` | Pendiente validar la depuración de datos contra resoluciones en producción (Analista) |
| `contrato_general.unidad_ejecutora` (entero) | `contrato_general.unidad_ejecutora_id` (6818, 6819) | Requiere una tabla de equivalencia entre los códigos de v1 y los parámetros del tipo 146 |
| `usuario` | `usuario_legado` | Campo legado, igual que hoy |

## 6. Ajuste de códigos "Rectoría 01, IDEXUD 02" en Parámetros (supuesto S4)

El LT indicó "Ajuste registros a: Rectoría 01, IDEXUD 02". Se interpreta como el `codigo_abreviacion` de los parámetros del tipo 146:

| Parámetro | Nombre | Código hoy | Código nuevo |
|---|---|---|---|
| 6818 | Rector | RECTOR | 01 |
| 6819 | IDEXUD | IDEXUD | 02 |

- Es un ajuste de datos en `parametros_crud`, no un cambio de esquema. Lo hace el administrador de Parámetros en cada ambiente. **No se ejecutó en esta issue.**
- Los valores "hoy" salen del consolidado del 13/10. No se pudieron consultar en vivo.
- En `gestion_contractual_mf` y `gestion_contractual_mid` (develop) no hay código que lea el `CodigoAbreviacion` del tipo 146: ambos usan los Id (6818, 6819). El MF usa la unidad `'01'` fija para consultar CDP en `paso-info-presupuestal`; con el ajuste, ese valor coincidiría con el código de Rectoría.

## 7. Carga inicial de unidad ejecutora

| Tabla | Unidad | Origen | Estado |
|---|---|---|---|
| `configuracion_unidad_ejecutora` | Rectoría (6818): prefijo `''`, sufijo `''` | `gestion_contractual_mid/src/contrato-general/conf.ts` | Incluida en `carga-inicial-unidad-ejecutora.sql` |
| `configuracion_unidad_ejecutora` | IDEXUD (6819): prefijo `'ID-'`, sufijo `''` | Mismo archivo | Incluida |
| `parametro_unidad_ejecutora` | IDEXUD (6819) | Columna "Aplica para IDEXUD" del consolidado depurado (adjunto de la #384) | **75 parámetros en 14 tipos**, incluidos |
| `parametro_unidad_ejecutora` | Rectoría (6818) | Columna "Aplica para Rectoría" (vacía) | Pendiente de la #383 |
| `parametro_unidad_ejecutora` | Unidad ejecutora 03 | — | Pendiente: no existe el parámetro en el tipo 146 |

**IDEXUD — lo que no se carga:**
- 6658 "es fondo de extensión" y 6661 "Solo uso esta": texto libre en lugar de Sí/No. Quedan listados al final del SQL.
- Los tipos sin marcas (116, 117, 121, 124, 126, 133, 135, 141 y 146).
- Los valores nuevos que pidió negocio, porque no existen en Parámetros.

**Regla de uso:** que no haya registro significa "no aplica". Mientras Rectoría no tenga su carga, filtrar sus listas con esta tabla las dejaría vacías. Los consumidores deben aplicar el filtro solo a las unidades que tengan carga.

## 8. Impacto en los consumidores

Revisado en develop de `gestion_contractual_mid` (133bb75) y `gestion_contractual_mf` (f546335), y en `poliza_mid` (a47b471).

| Tabla o cambio | gestion_contractual_mid | gestion_contractual_mf | poliza_mid |
|---|---|---|---|
| `contratista` → columnas de `contrato_general` (`proveedor_numero_documento`, `tipo_persona_id`, `clase_proveedor_id`) | `contrato-general.service.ts` (`include=contratista`, `clase_contratista_id`, `numero_documento`) y `variables-clausulas.service.ts` (`contratistas`) | `paso-contratistas`, `registro-actas`, `consulta-contrato`, `detalle-contrato`, `contrato-general-crud.service.ts` (`contratistas/`) y `types.ts` | Sin uso |
| `lugar_ejecucion` → `contrato_general.lugar_ejecucion_*` | `variables-clausulas.service.ts` (`lugares-ejecucion`) | `contrato-general-crud.service.ts` (`lugares-ejecucion`). El formulario ya no captura estos campos (#375) | Sin uso |
| `solicitante.dependencia_id`, `sede_id` (antes `*_solicitante_id`) | Sin uso | `paso-supervisores` y `types.ts` | Sin uso |
| `registro_presupuestal.disponibilidad_presupuestal_id`, `numero_registro_presupuestal` | `cdp_id` en `responses.interface.ts` y `variables-clausulas.service.ts` (por revisar si se refiere a esta columna) | `paso-info-presupuestal`, `paso-clausulas-paragrafos` (`cdp_id`) y `types.ts` | Sin uso |
| `contrato_general.unidad_ejecutora_id` NOT NULL | `generarConsecutivo` y `generarNumeroContrato` ya lo exigen | `paso-info-general` siempre envía una unidad | Sin uso |
| `uq_numero_contrato_vigencia_contrato_general` | `generarNumeroContrato` arma el número con un conteo; dos solicitudes simultáneas ahora fallan por la restricción en vez de duplicar | Sin cambio | Sin uso |
| `fecha_suscripcion`, `usuario_id`, `usuario_rol` y `estado_poliza_id` nuevas | Opcionales; ningún consumidor las envía hoy | Opcionales | Sin uso |
| Columnas nuevas de `acta_inicio` | El `minuta_contractual_mid` las envía en el PR #13 (abierto) | `registro-actas` | Sin uso |
| `parametro_unidad_ejecutora` y `configuracion_unidad_ejecutora` | Reemplazar `conf.ts` por la consulta a la configuración | Filtrar listas por unidad cuando haya carga | Sin uso |
| Pólizas y amparos | `amparos-contratos.service.ts` todavía consume `poliza_crud`; el PR gestion_contractual_mid#23 (abierto) lo cambia a `gestion_contractual_crud` | `polizas.service.ts` (`polizas`, `amparos-polizas`) | Consume `poliza_crud` y Parámetros, no `gestion_contractual_crud` |

La #385 reemplaza la API NestJS por una en Beego v2, así que las rutas y el formato de las respuestas cambian de todas formas. La tabla sirve para identificar qué pantallas y servicios dependen de cada cambio de modelo.
