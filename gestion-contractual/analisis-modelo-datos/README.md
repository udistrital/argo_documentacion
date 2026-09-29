# Análisis comparativo del modelo de datos — Issue #356

**Objeto.** Comparar el modelo de datos implementado en `gestion_contractual_crud` (Argo V2) con el diccionario de datos del último levantamiento de requerimientos. Identificar brechas y proponer los ajustes al esquema del CRUD.

**Entregables**

| Archivo | Contenido |
|---|---|
| `matriz-analisis-modelo-datos.xlsx` | Matriz campo por campo y hojas de soporte (ver [Contenido de la matriz](#contenido-de-la-matriz)). |
| Este documento | Hallazgos, plan de ajustes, supuestos y preguntas para la socialización. |
| `scripts/` | Scripts que regeneran el inventario y la matriz. |

**Fuentes**

| Fuente | Versión |
|---|---|
| Modelo Argo V2 | `udistrital/gestion_contractual_crud`, rama `develop`, commit `b968d77`: DDL `sql/creacion-tablas.sql`, entidades TypeORM, controladores |
| Diccionario de datos | `Diccionario_Datos_Contratacion_UD V2.0 08-06-2026.xlsx` |
| Casos de uso | `Casos Uso Contratacion Universidad Distrital.docx` (CU-01 a CU-22) |
| Modelo ARGO v1 | Diagrama adjunto a la issue y `modelo-database/README.md` |

## 1. Resultados en cifras

| Indicador | Valor |
|---|---|
| Entidades en el diccionario | 30 |
| Entidades del diccionario que solo tienen identificador | 16 |
| Campos en el diccionario | 161 |
| Tablas en el DDL / entidades TypeORM / endpoints | 16 / 13 / 78 |
| Columnas de negocio del CRUD (sin `id` ni auditoría) | 128 |
| Columnas del CRUD que el diccionario referencia | 32 (25 %) |
| Diferencias entre DDL y entidades | 45 |
| Desviaciones de lineamientos OATI | 64 |

**Campos del diccionario por tipo de brecha**

| Tipo de brecha | Campos | Alta | Media | Baja | Ninguna |
|---|---|---|---|---|---|
| Equivalente | 14 | 0 | 0 | 3 | 11 |
| Nombre distinto | 26 | 0 | 2 | 18 | 6 |
| Tipo / precisión | 2 | 0 | 1 | 1 | 0 |
| Cobertura parcial | 8 | 1 | 2 | 5 | 0 |
| Relación / estructura distinta | 20 | 0 | 18 | 2 | 0 |
| Faltante en CRUD | 19 | 4 | 14 | 1 | 0 |
| Externo al CRUD | 60 | 0 | 0 | 59 | 1 |
| Sin definición en diccionario | 12 | 0 | 7 | 5 | 0 |
| **Total** | **161** | **5** | **44** | **94** | **18** |

## 2. Hallazgos

### 2.1 El diccionario está a nivel conceptual y el CRUD es más detallado

- **El diccionario no define tipos de dato, longitudes ni obligatoriedad.** Solo trae nombre y descripción. Por eso la comparación de tipos se hizo contra el lineamiento OATI, y la de obligatoriedad no fue posible.
- **16 de las 30 entidades solo tienen identificador.** Son: Unión temporal, Consorcio, Evaluación, Caracterización, Certificación, Proyectos de extensión, Proyectos de investigación, Dependencia, Necesidad, SECOP, OTH, RP, Aprobación póliza, Acta de inicio, Liquidación y Terminación. Para estas no se puede hacer una comparación campo a campo.
- **En sentido inverso, el diccionario solo referencia el 25 % de las columnas de negocio del CRUD.**
  - Seis tablas no tienen ningún equivalente en el diccionario: `supervisor_contrato`, `ordenador_contrato`, `lugar_ejecucion`, `especificacion_tecnica`, `contrato_arrendamiento` y `convenio`.
  - `supervisor_contrato` y `ordenador_contrato` sí aparecen en casos de uso: CU-17 para el supervisor y CU-19 para el ordenador.
  - De `contrato_general` quedan fuera 22 columnas: tipología, régimen, procedimiento, moneda extranjera, origen de recursos, medio de pago, entre otras.
  - `amparo_poliza` tampoco está en el diccionario, aunque CU-14 registra amparos.
- **Conclusión:** buena parte de la brecha es del diccionario, no del CRUD. Antes de rediseñar el esquema conviene completar el diccionario (ajuste A13).

### 2.2 Brechas funcionales de severidad alta

| Brecha | Caso de uso | Situación en el CRUD |
|---|---|---|
| Proceso contractual (`Contrato.id_proceso`) | CU-11, CU-13 | No existe. CU-11 crea el proceso desde el estudio previo, con modalidad, supervisor y abogado. |
| Estudio previo como entidad | CU-10, CU-11 | Sus datos están embebidos en `contrato_general` (objeto, justificación, actividades, `fecha_suscripcion_estudio`). Faltan número, necesidad, obligaciones, valor estimado y plazo estimado. |
| Fecha de suscripción del contrato | CU-19 | No hay columna. `fecha_suscripcion_estudio` corresponde al estudio previo. En v1 existía `contrato_suscrito`. |
| Registro presupuestal (RP) | CU-16 | La tabla `registro_presupuestal` existe en el DDL, pero no tiene entidad, módulo ni endpoints. |
| Novedades contractuales | CU-18 | No existen en este CRUD. En v1 estaban `novedad_contractual` y una tabla por tipo (adición, prórroga, suspensión, cesión, cambio de supervisor). Falta confirmar si Argo V2 tiene un CRUD de novedades. |

### 2.3 Divergencias estructurales

- **Documentos.**
  - El diccionario define cinco entidades con la misma estructura: pre-contractual, pública, contractual, privada y pos-contractual. El CRUD tiene una sola tabla, `documento_contrato`.
  - El diccionario asocia documentos a cualquier entidad (`entidad_relacionada` + `id_entidad_relacionada`). El CRUD solo los asocia al contrato.
  - Se recomienda conservar una sola tabla y distinguir etapa y carácter por parámetro. Falta decidir si se necesita la asociación polimórfica.
- **Contratista.**
  - El diccionario pone el proveedor en el contrato. El CRUD pone el contrato en `contratista`.
  - La cardinalidad es 1:1 en la entidad y 1:N en el DDL.
  - CU-06 (consorcios y uniones temporales) obliga a definirla.
- **`numero_contrato`.** El diccionario lo trata como número oficial; en el CRUD está documentado como campo legado de la migración v1.
- **Fechas del contrato.** `fecha_inicial` y `fecha_final` están duplicadas en `acta_inicio.fecha_inicio` y `acta_inicio.fecha_fin`, y las prórrogas las modifican. Hay que definir cuál es la fuente de verdad.
- **Póliza.**
  - El valor asegurado se registra por amparo, no por póliza.
  - No hay estado de la póliza. CU-14 exige poder aprobarla o devolverla, y hoy solo existe `fecha_aprobacion`.
- **Estado del contrato.** Aquí el CRUD es mejor que el diccionario: guarda el estado como historial (`estado_contrato` con `actual`) en lugar de un atributo. Se recomienda reflejarlo así en el diccionario.
- **Datos externos al CRUD.**
  - Del proveedor, persona natural o jurídica y representante legal: 49 campos.
  - Valores del CDP: 5 campos.
  - Dependencia (OIKOS) y nombre de archivo (gestor documental).
  - No son brechas del CRUD, pero falta confirmar qué servicio es dueño del proveedor.

### 2.4 Desalineación entre el DDL y las entidades

Hay 45 diferencias. Con `synchronize: DEVELOPER_MODE`, en desarrollo son las entidades las que crean o alteran las tablas, así que el esquema real depende de cómo se creó cada base de datos.

**Las que pueden romper en ejecución:**
- `contratista.id` y `documento_contrato.id`: `SERIAL` en el DDL, `uuid` en la entidad.
- `supervisor_contrato`: el DDL define `sede_id` y `dependencia_id`; la entidad mapea las columnas `sede` y `dependencia`.
- `estado_contrato`: la entidad mapea la columna `fecha__evento` (doble guion bajo); el DDL la llama `fecha_evento`.
- `documento_contrato`: `usuario_id`, `usuario_rol` y `actual` existen solo en la entidad.

**Otras:**
- Longitudes distintas: `observaciones` es 1000 en el DDL y 500 en la entidad; `acta_inicio.usuario_legado` es 15 y 20.
- Precisión de `especificacion_tecnica`: (16,2) en el DDL, (10,2) y (15,2) en la entidad.
- Nulabilidad distinta en 22 columnas.
- Cuatro relaciones `@OneToOne` sin `UNIQUE` en el DDL.
- Tres tablas sin entidad: `registro_presupuestal`, `contrato_arrendamiento` y `convenio`.

### 2.5 Lineamientos OATI

- **Borrado físico.** Siete servicios ejecutan `repository.delete(id)`, contra la regla de nunca hacer DELETE real: supervisor, contratista, CDP, solicitante, documento, estado y lugar de ejecución. Es la desviación más grave, porque se pierden datos.
- **Montos.** Siete columnas no están en `numeric(20,7)`: `valor_pesos`, `valor_contrato_me`, `valor_tasa_cambio` y los valores de `especificacion_tecnica` y `contrato_arrendamiento`. `valor_tasa_cambio` es una tasa y no un monto: conviene documentarla como excepción.
- **Varchar sin longitud.** 11 columnas.
- **`activo` sin `DEFAULT TRUE`.** En 13 tablas; en `disponibilidad_presupuestal` además es nulable.
- **Auditoría.** `fecha_modificacion` es nulable en 5 tablas.
- **Nombres.**
  - PK y FK declaradas en línea, sin nombre `pk_` / `fk_`.
  - 8 índices no siguen `idx_<tabla>_<campo>`.
  - La FK `registro_presupuestal.cdp_id` debería llamarse `disponibilidad_presupuestal_id`.
- **URIs.**
  - `/disponibilidad_presupuestal` usa guion bajo.
  - `/ordenador-contrato` está en singular.
  - `POST /contratos-generales/conteo-*` usa POST para una consulta.

## 3. Plan de ajustes recomendado

Cada ajuste debería salir como una issue propia. La fase 1 no requiere decisiones de negocio y conviene hacerla antes que las demás, porque las fases 2 y 3 suponen un esquema alineado.

| Ajuste | Fase | Descripción | ¿Rompe consumidores? | Decisión de negocio |
|---|---|---|---|---|
| A1 | 1 | Alinear entidades con el DDL: PK serial, `sede_id`/`dependencia_id`, `fecha_evento`, longitudes, nulabilidad, `UNIQUE` en relaciones 1:1. | Sí (id de `/contratistas` y `/documentos-contratos` pasa de uuid a entero) | Parcial (cardinalidad → A12) |
| A2 | 1 | Borrado lógico en los 7 servicios con DELETE físico. | No | No |
| A3 | 1 | Tipos según lineamiento: montos, varchar, `activo`, auditoría, vigencia, nombres de restricciones e índices. | No | No |
| A4 | 1 | URIs: `/disponibilidades-presupuestales`, `/ordenadores-contratos`, GET para los conteos. | Sí | No (coordinar con MIDs y clientes) |
| A5 | 2 | Exponer `registro_presupuestal` (`/registros-presupuestales`) y renombrar su FK. | No | No |
| A6 | 2 | Fecha de suscripción: columna en `contrato_general` o evento de estado. | No | Sí |
| A7 | 2 | Estado de la póliza (parámetro + motivo; historial si se requiere). | No | Sí |
| A8 | 3 | Estudio previo y proceso contractual como entidades propias. | Posible | Sí |
| A9 | 3 | Documentos: etapa y carácter por parámetro; asociación a otras entidades; estados. | No | Sí |
| A10 | 3 | Novedades, liquidación y terminación: confirmar servicio dueño antes de modelar. | No | Sí |
| A11 | 3 | Vínculo contrato–proyecto de extensión (contratación derivada, CU-15). | No | Sí |
| A12 | 3 | Cardinalidades del contrato con contratista, solicitante, lugar de ejecución y ordenador; servicio dueño del proveedor. | Posible | Sí |
| A13 | 3 | Completar el diccionario: entidades con solo identificador, entidades del CRUD ausentes, tipos y obligatoriedad. | No | Sí (Analista de RQ) |

**Consideraciones para la ejecución**
- **A1:** si hay datos en `contratista` o `documento_contrato`, el cambio de uuid a serial requiere migración de datos. Antes de ejecutarlo hay que confirmar qué lado es la fuente de verdad (pregunta 1).
- **A1 y A4** cambian contratos de API. Hay que inventariar los MIDs y clientes que consumen el CRUD y definir un periodo de convivencia de rutas.
- **A2:** hoy ningún `GET` filtra por `activo` (tampoco `BaseCrudService`). Al pasar a borrado lógico hay que decidir si los listados excluyen los inactivos por defecto; si no, los consumidores empezarán a recibir registros "borrados".

La hoja *Impacto endpoints* de la matriz lista los recursos afectados por cada ajuste.

## 4. Supuestos

1. La línea base es el DDL `sql/creacion-tablas.sql` y las entidades TypeORM de `develop`. No se tuvo acceso a la base de datos desplegada.
2. El diccionario no define tipos ni obligatoriedad. Los tipos del CRUD se contrastan contra el lineamiento OATI.
3. Proveedor, persona natural, persona jurídica y representante legal se tratan como datos de un servicio externo. Es coherente con cómo el CRUD ya referencia al supervisor y al ordenador (terceros_crud) y a las dependencias (OIKOS).
4. Valor, saldo, rubro y proyecto del CDP se tratan como datos del sistema financiero.
5. No se inventariaron los consumidores del CRUD. El impacto se mide sobre la API del propio CRUD.
6. CU-01, CU-12, CU-20, CU-21 y CU-22 no tienen efecto en el modelo del CRUD y no se mapean a campos.

## 5. Preguntas para la socialización

Publicadas como comentario en la issue #356, con contexto y opciones de respuesta. La numeración es la misma.

| # | Pregunta | Dirigida a |
|---|---|---|
| 1 | Origen del esquema: ¿la base se creó con el DDL o con `synchronize`? Define qué lado se corrige en A1. | LT |
| 2 | ¿Qué servicio es dueño del proveedor y de sus especializaciones? | LT |
| 3 | ¿Existe un CRUD de novedades? ¿Liquidación y terminación son novedades? | LT |
| 4 | ¿Qué información financiera del CDP se guarda en el CRUD? | LT |
| 5 | Borrado lógico: ¿los `GET` excluyen los inactivos por defecto? | LT |
| 6 | ¿Qué MIDs o clientes consumen el CRUD? | LT |
| 7 | ¿Cómo se registran los ajustes: una issue por ajuste, por fase o mixto? | LT |
| 8 | ¿El proceso contractual es una entidad propia o es `contrato_general` desde la etapa precontractual? | Analista de RQ |
| 9 | ¿`numero_contrato` es el número oficial vigente o solo el legado de ARGO v1? | Analista de RQ |
| 10 | ¿La fecha de suscripción es un campo del contrato o un evento de estado? | Analista de RQ |
| 11 | ¿Un contrato puede tener varios contratistas, solicitantes, lugares de ejecución u ordenadores? | Analista de RQ |
| 12 | Documentos: ¿una sola tabla con etapa y carácter? ¿Otras entidades? ¿Estados? | Analista de RQ |
| 13 | ¿La póliza necesita historial de aprobaciones y devoluciones? | Analista de RQ |
| 14 | ¿Valor y plazo estimados del estudio previo se conservan aparte de los contratados? | Analista de RQ |
| 15 | ¿Habrá una versión del diccionario con atributos, tipos y obligatoriedad? ¿Qué significa OTH? | Analista de RQ |
| 16 | CU-07 (precotizaciones) y CU-19 (flujo de firmas) no tienen entidad en el diccionario: ¿se modelan? | Analista de RQ |

La hoja *Supuestos y preguntas* de la matriz tiene una columna para registrar las respuestas.

## Contenido de la matriz

| Hoja | Contenido |
|---|---|
| Resumen | Fuentes, volumen y conteo de brechas por tipo y severidad (fórmulas sobre la hoja Matriz). |
| Matriz | Una fila por campo del diccionario (161): tabla y columna del CRUD, tipo y nulabilidad en DDL y entidad, origen v1, tipo de brecha, severidad, recomendación, casos de uso y si requiere validación. |
| CRUD sin diccionario | Columnas del CRUD que el diccionario no contempla (dirección inversa). |
| DDL vs entidad | Diferencias entre `sql/creacion-tablas.sql` y las entidades TypeORM. |
| Lineamientos | Desviaciones frente a los lineamientos de modelo de datos y API. |
| Impacto endpoints | Recursos afectados por cada ajuste del plan. |
| Cobertura por entidad | Resumen por entidad del diccionario. |
| Supuestos y preguntas | Supuestos del análisis y preguntas abiertas, con columna para respuestas. |

## Regenerar la matriz

Los scripts se ejecutan con Python 3 y requieren `openpyxl`. El diccionario está adjunto en la issue #356.

```bash
python3 scripts/inventario_crud.py <ruta/gestion_contractual_crud> inventario.json
cd scripts && python3 construir_matriz.py <ruta/diccionario.xlsx> ../inventario.json ../matriz-analisis-modelo-datos.xlsx
```

- `inventario_crud.py` extrae el DDL, las entidades, los endpoints y los servicios con borrado físico.
- `mapeo.py` contiene el mapeo manual diccionario → CRUD, con la brecha, la severidad y la recomendación de cada campo.
- `ajustes.py` contiene el plan de ajustes, los supuestos y las preguntas.
- `construir_matriz.py` falla si algún campo del diccionario queda sin mapear o mapeado dos veces.
