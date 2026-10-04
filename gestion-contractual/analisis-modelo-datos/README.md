# Análisis comparativo del modelo de datos — Issue #356

**Objeto.** Comparar el modelo de datos implementado en `gestion_contractual_crud` (Argo V2) con el diccionario de datos del último levantamiento de requerimientos. Identificar brechas y proponer los ajustes al esquema del CRUD.

**Entregables**

| Archivo | Contenido |
|---|---|
| `matriz-analisis-modelo-datos.xlsx` | Matriz campo por campo y hojas de soporte (ver [Contenido de la matriz](#contenido-de-la-matriz)). |
| Este documento | Hallazgos, plan de ajustes, supuestos, respuestas del LT y temas para la sesión. |
| `fuentes/` | Transcripción de los diagramas compartidos en la issue: BD de pruebas (`bd_pruebas.json`) y tablas de Ágora (`agora.json`). |
| `scripts/` | Scripts que regeneran el inventario y la matriz. |

**Fuentes**

| Fuente | Versión |
|---|---|
| Modelo Argo V2 | `udistrital/gestion_contractual_crud`, rama `develop`, commit `09a4d66` (incluye la estabilización, issue #361, PR #46): DDL `sql/creacion-tablas.sql`, entidades TypeORM, controladores |
| BD de pruebas | Diagrama "modelo actual" que compartió el LT en la issue (respuesta 1) |
| Ágora | Tres diagramas con las tablas del proveedor que compartió el LT (respuesta 2) |
| Respuestas | Comentario del LT en la issue (1 de octubre de 2026) y sesión con el LT |
| Diccionario de datos | `Diccionario_Datos_Contratacion_UD V2.0 08-06-2026.xlsx` |
| Casos de uso | `Casos Uso Contratacion Universidad Distrital.docx` (CU-01 a CU-22) |
| Modelo ARGO v1 | Diagrama adjunto a la issue y `modelo-database/README.md`. Es el sistema que está hoy en producción. |

La primera versión del análisis usó el commit `b968d77`, anterior a la estabilización.

## 1. Resultados en cifras

| Indicador | Valor |
|---|---|
| Entidades en el diccionario | 30 |
| Entidades del diccionario que solo tienen identificador | 16 |
| Campos en el diccionario | 161 |
| Tablas en el DDL / entidades TypeORM / endpoints | 16 / 13 / 78 |
| Columnas de negocio del CRUD (sin `id` ni auditoría) | 128 |
| Columnas del CRUD que el diccionario referencia | 32 (25 %) |
| Diferencias entre DDL y entidades | 39 (45 antes de la estabilización) |
| Tablas en el diagrama de la BD de pruebas | 14 |
| Diferencias entre la BD de pruebas y el código | 2 (PK de `contratista` y `documento_contrato`) |
| Campos del diccionario mapeados a Ágora | 56 (13 sin columna visible) |
| Desviaciones de lineamientos OATI | 64 |

**Campos del diccionario por tipo de brecha**

| Tipo de brecha | Campos | Alta | Media | Baja | Ninguna |
|---|---|---|---|---|---|
| Equivalente | 14 | 0 | 0 | 3 | 11 |
| Nombre distinto | 26 | 0 | 2 | 18 | 6 |
| Tipo / precisión | 2 | 0 | 1 | 1 | 0 |
| Cobertura parcial | 3 | 1 | 1 | 1 | 0 |
| Relación / estructura distinta | 20 | 0 | 2 | 18 | 0 |
| Faltante en CRUD | 9 | 3 | 5 | 1 | 0 |
| Externo al CRUD | 60 | 0 | 0 | 59 | 1 |
| Sin definición en diccionario | 11 | 0 | 5 | 6 | 0 |
| Fuera de alcance | 11 | 0 | 0 | 0 | 11 |
| Descartado | 5 | 0 | 0 | 0 | 5 |
| **Total** | **161** | **4** | **16** | **107** | **34** |

Frente a la primera versión, las brechas de severidad alta bajan de 5 a 4 (novedades queda fuera de alcance) y las de severidad media, de 44 a 16. La baja se debe a las respuestas del LT y a que el plan ya no propone cambios de estructura.

## 2. Hallazgos

### 2.1 El diccionario está a nivel conceptual y el CRUD es más detallado

- **El diccionario no define tipos de dato, longitudes ni obligatoriedad.** Solo trae nombre y descripción. Por eso la comparación de tipos se hizo contra el lineamiento OATI, y la de obligatoriedad no fue posible.
- **16 de las 30 entidades solo tienen identificador.** Son: Unión temporal, Consorcio, Evaluación, Caracterización, Certificación, Proyectos de extensión, Proyectos de investigación, Dependencia, Necesidad, SECOP, OTH, RP, Aprobación póliza, Acta de inicio, Liquidación y Terminación. Según el LT (respuesta 15), estas se profundizan con el modelo general y se validan contra las entidades de Argo v2. No se sabe qué significa OTH.
- **En sentido inverso, el diccionario solo referencia el 25 % de las columnas de negocio del CRUD.**
  - Seis tablas no tienen ningún equivalente en el diccionario: `supervisor_contrato`, `ordenador_contrato`, `lugar_ejecucion`, `especificacion_tecnica`, `contrato_arrendamiento` y `convenio`.
  - `supervisor_contrato` y `ordenador_contrato` sí aparecen en casos de uso: CU-17 para el supervisor y CU-19 para el ordenador.
  - De `contrato_general` quedan fuera 22 columnas: tipología, régimen, procedimiento, moneda extranjera, origen de recursos, medio de pago, entre otras.
  - `amparo_poliza` tampoco está en el diccionario, aunque CU-14 registra amparos.
- **Conclusión:** buena parte de la brecha es del diccionario, no del CRUD (ajuste A13).

### 2.2 BD del ambiente de pruebas

**Alcance de la comparación.** El diagrama solo permite comparar nombres de tablas y columnas, la PK y la categoría del tipo (numérico, texto, fecha o booleano). No muestra longitudes, precisión, nulabilidad, valores por defecto, restricciones UNIQUE, índices ni cardinalidad, así que nada de eso se verifica contra la BD. La transcripción está en `fuentes/bd_pruebas.json`.

- **La BD coincide con el DDL** en las 14 tablas del diagrama y en sus 165 columnas: mismos nombres, misma PK y misma categoría de tipo.
- **Frente a las entidades de `develop`, solo difiere la PK** de `contratista` y `documento_contrato`. En la BD es numérica, como en el DDL, y en la entidad es `uuid` (ajuste A1).
- **La estabilización (PR #46) ya cerró las demás diferencias de nombre** que tenía la primera versión:
  - `supervisor_contrato` mapea `sede_id` y `dependencia_id`.
  - `estado_contrato` mapea `fecha_evento`.
  - En `documento_contrato` se comentaron `usuario_id`, `usuario_rol` y `actual`.
- **`registro_presupuestal`, `contrato_arrendamiento` y `convenio`** existen en la BD y en el DDL, pero no tienen entidad, módulo ni endpoints.
- **`poliza` y `amparo_poliza`** no aparecen en el diagrama de pruebas. Falta confirmar si la migración de la issue #351 (PR #38) ya se aplicó en ese ambiente. No se cuentan como discrepancia.
- **`vigencia`** es texto en `contrato_general` y numérica en `disponibilidad_presupuestal`, `registro_presupuestal` y `convenio`, tanto en la BD como en el DDL.
- **Limitaciones:**
  - Las diferencias de longitud y nulabilidad entre el DDL y las entidades (sección 2.6) no se pueden contrastar con la BD.
  - El diagrama tampoco permite saber si `contrato_general_id` tiene UNIQUE en `contratista`, `solicitante`, `lugar_ejecucion` y `ordenador_contrato`. Esto queda en stand by con la pregunta 11.

### 2.3 Proveedor en Ágora

El LT confirmó que los datos del proveedor se consultan de Ágora, y que con la referencia actual (`contratista.numero_documento`) Argo puede manejarlos. También indicó que en la nueva versión de Ágora pueden migrarse a terceros (respuesta 2). La hoja *Mapeo Ágora* relaciona cada campo del diccionario con la tabla y la columna de Ágora. La transcripción está en `fuentes/agora.json`.

| Entidad del diccionario | Tablas de Ágora | Campos | Con columna | Aproximados | No visibles |
|---|---|---|---|---|---|
| Proveedor | `informacion_proveedor`, `informacion_persona_natural`, `proveedor_telefono`, `ciudad` | 17 | 10 | 6 | 1 |
| PersonaNatural | `informacion_persona_natural`, `inhabilidad` | 14 | 7 | 3 | 4 |
| PersonaJuridica | `informacion_proveedor`, `proveedor_actividad_ciiu` | 11 | 5 | 2 | 4 |
| RepresentanteLegal | `proveedor_representante_le…`, `informacion_persona_natural` | 10 | 2 | 4 | 4 |
| Unión temporal, Consorcio, Evaluación, Caracterización | `informacion_sociedad_temp…`, `informacion_sociedad_particip…`, `informacion_proveedor`, `informacion_persona_natural` | 4 | 2 | 2 | 0 |

Los nombres de tabla que el diagrama corta se dejan con "…".

**Observaciones**
- `informacion_proveedor.fecha_registro` y `fecha_ultima_modificacion` son de tipo texto, no fecha.
- La evaluación (`puntaje_evaluacion`, `clasificacion_evaluacion`) está por proveedor, mientras que CU-08 la asocia al contrato.
- Existen `objeto_cotizacion` y `solicitud_cotizacio…`, que tienen que ver con CU-07 (precotizaciones).
- No hay una tabla propia de persona jurídica. Tampoco se ve una columna que una `informacion_persona_natural` con `informacion_proveedor`.
- **Consorcios y uniones temporales:** se registran en `informacion_sociedad_temp…`, con representante y suplente, y en `informacion_sociedad_particip…`, con el porcentaje de participación. Esto cubre CU-06.

### 2.4 Brechas funcionales de severidad alta

| Brecha | Caso de uso | Situación |
|---|---|---|
| Proceso contractual (`Contrato.id_proceso`) | CU-11, CU-13 | No existe en el CRUD. En stand by (pregunta 8). No se propone entidad nueva. |
| Estudio previo | CU-10, CU-11 | Sus datos están en `contrato_general`. En stand by (pregunta 8). Si se confirma, los campos faltantes se agregan al modelo actual. |
| Fecha de suscripción del contrato | CU-19 | No hay columna. Se decidió agregarla en `contrato_general` (respuesta 10, ajuste A6). |
| Registro presupuestal (RP) | CU-16 | La tabla existe en el DDL y en la BD de pruebas, pero no tiene entidad, módulo ni endpoints (ajuste A5). |

Las novedades contractuales (CU-18), que en la primera versión eran de severidad alta, quedan fuera de alcance. Según la respuesta 3, el sistema de novedades gestiona hoy las de CPS, y las del nuevo Argo se analizan desde requerimientos sin afectar el módulo contractual.

### 2.5 Otras divergencias

- **Documentos.**
  - `documento_contrato` se mantiene como única tabla, asociada al contrato.
  - La etapa y el carácter (público/privado) se expresan con `tipo_documento_id`.
  - Los documentos no tienen estado (respuesta 12): `estado_documento` queda como "Descartado".
- **Contratista.**
  - El proveedor vive en Ágora.
  - La cardinalidad 1:1 que usan las entidades está en stand by (pregunta 11).
- **`numero_contrato`.**
  - Según el LT, es un identificador único por vigencia (respuesta 9). En la tabla `contrato_general` de ARGO v1 que aparece en los diagramas de Ágora, la PK es (`numero_contrato`, `vigencia`).
  - La restricción se propone en A14, por confirmar en sesión con el LT y el Analista.
- **Fechas del contrato.** `fecha_inicial` y `fecha_final` están duplicadas en `acta_inicio.fecha_inicio` y `acta_inicio.fecha_fin`. Hay que definir cuál es la fuente de verdad.
- **Póliza.**
  - El valor asegurado se registra por amparo, no por póliza.
  - Lo relativo al estado de la póliza está en stand by (pregunta 13). Si se confirma, se agrega un campo de estado, sin tabla de historial.
- **Estado del contrato.**
  - El CRUD guarda el estado como historial (`estado_contrato` con `actual`) y tiene dos columnas de estado: `estado_parametro_id` y `estado_interno_parametro_id`.
  - Nota del LT en sesión (respuesta 10): "2 estados, el que ve el usuario".
  - *Interpretación pendiente de confirmar en sesión:* la nota se refiere a que `estado_parametro_id` es el estado visible para el usuario, frente a `estado_interno_parametro_id`.
- **Datos externos al CRUD.**
  - Proveedor y sus especializaciones, en Ágora: 49 campos.
  - Valores del CDP, en SICAPITAL: 5 campos. Se consultan por `numero_cdp_id` (respuesta 4).
  - Dependencia, en OIKOS.
  - Nombre de archivo, en el gestor documental.

### 2.6 Desalineación entre el DDL y las entidades

En `develop` quedan 39 diferencias, frente a las 45 anteriores a la estabilización:

| Tipo de diferencia | Cantidad | Detalle |
|---|---|---|
| PK | 2 | `serial` en el DDL y `uuid` en la entidad (`contratista` y `documento_contrato`). La BD de pruebas coincide con el DDL. |
| Tipo, longitud o precisión | 7 | Por ejemplo, `observaciones` es 1000 en el DDL y 500 en la entidad; `especificacion_tecnica` tiene (16,2) en el DDL y (10,2)/(15,2) en la entidad. |
| Nulabilidad | 25 | Dos de ellas coinciden con las de precisión. |
| Relaciones | 4 | `@OneToOne` sin `UNIQUE` en el DDL. |
| Tablas | 3 | Tablas sin entidad. |

Salvo la PK, ninguna de estas diferencias se puede contrastar con el diagrama de la BD de pruebas.

`scripts/inventario_crud.py` ahora ignora las columnas comentadas en las entidades. Antes las contaba, y por eso habría seguido reportando `usuario_id`, `usuario_rol` y `actual` en `documento_contrato`.

### 2.7 Lineamientos OATI

- **Borrado físico.** Siete servicios ejecutan `repository.delete(id)`, contra la regla de nunca hacer DELETE real: supervisor, contratista, CDP, solicitante, documento, estado y lugar de ejecución. El LT confirmó que se debe manejar borrado lógico y consultar solo activos (respuesta 5).
- **Montos.** Siete columnas no están en `numeric(20,7)`: `valor_pesos`, `valor_contrato_me`, `valor_tasa_cambio` y los valores de `especificacion_tecnica` y `contrato_arrendamiento`. `valor_tasa_cambio` es una tasa y no un monto: conviene documentarla como excepción.
- **Varchar sin longitud.** 11 columnas.
- **`activo` sin `DEFAULT TRUE`.** En 13 tablas; en `disponibilidad_presupuestal` además es nulable.
- **Auditoría.** `fecha_modificacion` es nulable en 5 tablas.
- **Nombres.**
  - PK y FK declaradas en línea, sin nombre `pk_` / `fk_`.
  - 8 índices no siguen `idx_<tabla>_<campo>`.
  - La FK `registro_presupuestal.cdp_id` debería llamarse `disponibilidad_presupuestal_id`. No se recomienda renombrarla por ahora.
- **URIs.**
  - `/disponibilidad_presupuestal` usa guion bajo.
  - `/ordenador-contrato` está en singular.
  - `POST /contratos-generales/conteo-*` usa POST para una consulta.
  - No se recomienda corregirlas por ahora (ajuste A4).

## 3. Plan de ajustes recomendado

**Criterio.** En la sesión, el LT indicó que ARGO v1 es el sistema que está hoy en producción y que proponer un modelo diferente daña, porque tiene muchas integraciones. Por eso el plan no propone rediseños: nada de entidades nuevas que reemplacen o partan las existentes, ni cambios de estructura. Solo se admite:
- alinear el CRUD con la BD de pruebas;
- corregir lineamientos que no rompan integraciones;
- agregar campos faltantes al modelo actual cuando se confirmen.

Según la respuesta 7, los ajustes se integran sobre la estabilización y se resuelven a nivel de modelo, de modo que sirvan tanto si se mantiene el framework actual como si hay una migración posterior a la presentación al usuario.

| Ajuste | Fase | Estado | Descripción | ¿Rompe consumidores? |
|---|---|---|---|---|
| A1 | 1 | Recomendado | Alinear las entidades con la BD de pruebas: en la BD la PK de `contratista` y `documento_contrato` ya es numérica; la entidad pasa de `uuid` a serial. | Sí: el id de `/contratistas` y `/documentos-contratos` pasa a entero (lo consume el MID) |
| A2 | 1 | Recomendado | Borrado lógico en los 7 servicios con DELETE físico, y listados que consultan solo activos (respuesta 5). | No |
| A3 | 1 | Recomendado | Lineamientos sin cambio de estructura: montos `numeric(20,7)`, varchar con longitud, `activo DEFAULT TRUE`, auditoría NOT NULL, nombres de restricciones e índices. No incluye unificar el tipo de `vigencia`. | No |
| A4 | 1 | No se recomienda por ahora | Renombrar URIs. Por las integraciones, queda para una eventual migración de framework (respuesta 7). | Sí |
| A5 | 2 | Recomendado | Exponer `registro_presupuestal` (`/registros-presupuestales`). La tabla ya existe en la BD. | No |
| A6 | 2 | Recomendado | Agregar `fecha_suscripcion` en `contrato_general` (respuesta 10). Falta confirmar el momento del registro. | No |
| A9 | 2 | Recomendado | Sin cambio de esquema: una sola tabla de documentos, sin estados. Verificar que `tipo_documento_id` cubra etapa y carácter. | No |
| A7 | 3 | Stand by | Si se confirma (pregunta 13), un campo de estado en `poliza`. Sin tabla de historial. | No |
| A8 | 3 | Stand by | Si se confirma (pregunta 8), agregar al modelo actual número de estudio, necesidad, obligaciones, y valor y plazo estimados, separados de los contratados (pregunta 14). No se crean entidades de estudio previo ni de proceso. | No |
| A10 | 3 | Fuera de alcance | Novedades y terminación (respuesta 3). Liquidación queda para la sesión. | No |
| A11 | 3 | Por confirmar | Campo en `contrato_general` que referencie el proyecto de extensión (CU-15). | No |
| A12 | 3 | Stand by | Si se confirma 1:1 (pregunta 11), `UNIQUE` en `contrato_general_id` de `contratista`, `solicitante`, `lugar_ejecucion` y `ordenador_contrato`. | No |
| A13 | 3 | Recomendado | Completar el diccionario según la respuesta 15, incluir las entidades que ya existen en el CRUD y retirar `estado_documento`. | No |
| A14 | 3 | Por confirmar | `UNIQUE (numero_contrato, vigencia)` en `contrato_general` (respuesta 9). Por confirmar en sesión con LT y Analista. | No |

**Consideraciones para la ejecución**
- **A1** cambia el tipo del id en dos recursos. Hay que coordinarlo con el MID, que según el LT es el único consumidor actual (respuesta 6).
- **A2** cambia el comportamiento de los `GET`, que dejan de devolver registros inactivos. Hoy ningún listado filtra por `activo`, tampoco `BaseCrudService`.
- **A14:** antes de crear la restricción hay que verificar que no existan contratos duplicados por número y vigencia.

La hoja *Impacto endpoints* de la matriz lista los recursos afectados por cada ajuste.

## 4. Supuestos

1. La línea base es el DDL `sql/creacion-tablas.sql` y las entidades TypeORM de `develop` después de la estabilización, más el diagrama de la BD de pruebas que compartió el LT.
2. El diagrama de la BD de pruebas solo permite comparar nombres de tablas y columnas, la PK y la categoría del tipo. Longitudes, precisión, nulabilidad, valores por defecto, UNIQUE, índices y cardinalidad no se verifican contra la BD.
3. El diccionario no define tipos ni obligatoriedad. Los tipos del CRUD se contrastan contra el lineamiento OATI.
4. El mapeo a Ágora se basa solo en las tres imágenes de la respuesta 2. Lo que no aparece se marca como no visible.
5. Terminación se trata como novedad (fuera de alcance), como en ARGO v1 (`terminacion_anticipada`). Por validar en sesión.
6. Las relaciones del contrato con contratista, solicitante, lugar de ejecución y ordenador se tratan como 1:1 de forma provisional (respuesta 11, stand by).
7. CU-01, CU-12, CU-20, CU-21 y CU-22 no tienen efecto en el modelo del CRUD y no se mapean a campos.

## 5. Respuestas del LT

Numeración del comentario de preguntas publicado en la issue #356. Las respuestas provienen del comentario del LT en la issue y de la sesión.

| # | Tema | Respuesta | Estado |
|---|---|---|---|
| 1 | Origen del esquema | El LT compartió el diagrama de la BD de pruebas como referencia del estado actual y pidió sincronizar con la estabilización. | Resuelta |
| 2 | Dueño del proveedor | Ágora. La referencia actual basta; en la nueva versión de Ágora pueden migrarse a terceros. | Resuelta |
| 3 | Novedades | El sistema de novedades atiende hoy las de CPS; las del nuevo Argo se analizan desde requerimientos y no afectan el módulo contractual. No se respondió sobre liquidación y terminación. | Resuelta (fuera de alcance) |
| 4 | Información financiera del CDP | `numero_cdp_id` es la referencia para consultar SICAPITAL. | Resuelta |
| 5 | Borrado lógico | Eliminado lógico, y los filtros consultan solo activos. | Resuelta |
| 6 | Consumidores | Hoy solo lo consume el MID. El resto se valida en sesión. | Parcial: validar en sesión |
| 7 | Organización de los ajustes | Integrar sobre la estabilización; ajustes a nivel de modelo por una posible migración de framework. No se definió el formato de las issues. | Parcial |
| 8 | Proceso contractual | Stand by. | Stand by |
| 9 | Número de contrato | Identificador único por vigencia; validar con LT y Analista. | Validar en sesión |
| 10 | Fecha de suscripción | Opción a): campo del contrato. Nota: "2 estados, el que ve el usuario". Confirmar si se registra al firmar, una vez terminado el flujo de aprobación. | Resuelta (momento del registro por confirmar) |
| 11 | Cardinalidad | Todas 1:1, en stand by. | Stand by |
| 12 | Documentos | Los documentos no tienen estado. | Parcial |
| 13 | Póliza | Confirmar el flujo con el Analista (@cjgonzalezp). Stand by. | Stand by |
| 14 | Valor y plazo estimados | Stand by, pero son valores separados de los contratados. | Stand by |
| 15 | Entidades sin atributos | Se profundizan con el modelo general y se validan contra Argo v2. No se sabe qué significa OTH. | Parcial |
| 16 | CU-07 y CU-19 | La firma se hace mediante la integración con otro servicio; validar en sesión ("tener presente la tabla documento_..."). No se respondió sobre CU-07. | Validar en sesión |

La hoja *Supuestos y preguntas* de la matriz tiene estas respuestas, su estado y los temas para la sesión.

## Contenido de la matriz

| Hoja | Contenido |
|---|---|
| Resumen | Fuentes, volumen y conteo de brechas por tipo y severidad (fórmulas sobre la hoja Matriz). |
| Matriz | Una fila por campo del diccionario (161): tabla y columna del CRUD, tipo y nulabilidad en DDL y entidad, origen v1, tipo de brecha, severidad, recomendación, casos de uso, si requiere validación y si la columna aparece en la BD de pruebas. |
| CRUD sin diccionario | Columnas del CRUD que el diccionario no contempla (dirección inversa). |
| DDL vs entidad | Diferencias entre `sql/creacion-tablas.sql` y las entidades TypeORM. |
| BD de pruebas | Cada tabla y columna de la BD de pruebas frente al DDL y a la entidad (nombre, PK y categoría del tipo). |
| Mapeo Ágora | Campos del proveedor y sus especializaciones en las tablas de Ágora, con cobertura y observaciones. |
| Lineamientos | Desviaciones frente a los lineamientos de modelo de datos y API. |
| Impacto endpoints | Fase, estado y recursos afectados por cada ajuste del plan. |
| Cobertura por entidad | Resumen por entidad del diccionario. |
| Supuestos y preguntas | Supuestos del análisis, preguntas con respuesta y estado, y temas para la sesión. |

## Regenerar la matriz

Los scripts se ejecutan con Python 3 y requieren `openpyxl`. El diccionario está adjunto en la issue #356. `construir_matriz.py` lee además `fuentes/bd_pruebas.json` y `fuentes/agora.json`.

```bash
python3 scripts/inventario_crud.py <ruta/gestion_contractual_crud> inventario.json
cd scripts && python3 construir_matriz.py <ruta/diccionario.xlsx> ../inventario.json ../matriz-analisis-modelo-datos.xlsx
```

- `inventario_crud.py` extrae el DDL, las entidades (sin el código comentado), los endpoints y los servicios con borrado físico.
- `mapeo.py` contiene el mapeo manual diccionario → CRUD, con la brecha, la severidad y la recomendación de cada campo, y el mapeo a Ágora.
- `ajustes.py` contiene el criterio, el plan de ajustes, los supuestos, las preguntas con sus respuestas y los temas para la sesión.
- `construir_matriz.py` falla si algún campo del diccionario queda sin mapear o mapeado dos veces, o si el mapeo a Ágora cita una tabla o columna que no está en `fuentes/agora.json`.

## Temas para la sesión

1. **Pregunta 6:** consumidores del CRUD además del MID.
2. **Pregunta 8:** proceso contractual (stand by).
3. **Pregunta 9:** `numero_contrato` único por vigencia (A14).
4. **Pregunta 10:** momento del registro de `fecha_suscripcion` (A6) y alcance de la nota "2 estados, el que ve el usuario".
5. **Pregunta 11:** cardinalidad 1:1 de contratista, solicitante, lugar de ejecución y ordenador (A12).
6. **Pregunta 13:** estado de la póliza (A7).
7. **Pregunta 14:** valor y plazo estimados del estudio previo (A8).
8. **Pregunta 16:** flujo de firmas e integración con otro servicio (tabla `documento_...`).
9. **Liquidación:** ¿es una novedad o se modela en el módulo contractual?
10. **Terminación:** confirmar el supuesto de que es una novedad.
11. **Pregunta 7:** formato de las issues para registrar los ajustes.
12. **Tablas de pólizas en pruebas:** `poliza` y `amparo_poliza` no aparecen en el diagrama; confirmar si la migración de la issue #351 (PR #38) ya se aplicó en ese ambiente.
