# Consolidado de datos paramétricos ARGO v2 — Issue #377

**Objeto.** Extraer de `parametros_crud` los datos paramétricos que consume `gestion_contractual_mf` y consolidarlos en un Excel. Negocio los revisa, los depura e indica a qué unidad ejecutora aplica cada uno (Rectoría, IDEXUD).

**Issue:** [udistrital/argo_documentacion#377](https://github.com/udistrital/argo_documentacion/issues/377) — Consolidar datos paramétricos ARGO v2 para su depuración.

**Entregables**

| Archivo | Contenido |
|---|---|
| `extraer_parametros.py` | Extractor: consulta el servicio y genera el Excel y el reporte. |
| `config_parametros.py` | Mapeo constante del entorno → id. La lógica no tiene ids quemados. |
| `salida/consolidado_parametros_argo_v2_AAAA-MM-DD.xlsx` | Consolidado para negocio (ver [Estructura del Excel](#estructura-del-excel)). |
| `salida/reporte_validacion.md` | Validación de la extracción: constantes, conteos, paginación, diferencias e inconsistencias. |
| `requirements.txt`, `.env.example` | Dependencias y variables de entorno. |

## 1. Decisiones del LT

1. Una hoja por **tipo** de parámetro con las columnas Id, Nombre, Descripción, Código abreviación, "Aplica para Rectoría" y "Aplica para IDEXUD". Las dos últimas van vacías, con lista desplegable Sí/No.
2. Fuente: `parametros_crud` del ambiente de pruebas, `http://pruebasapi.intranetoas.udistrital.edu.co:8510/v1/` (intranet, requiere VPN).
3. Los scripts propios de ARGO van en `scripts/` en la raíz del repositorio.
4. Se exportan activos e inactivos **sin distinguirlos** (no hay columna ni marca de activo).

## 2. Requisitos e instalación

- VPN de la universidad conectada (el servicio está en la intranet).
- Python 3.10 o superior.

```bash
cd scripts/datos-parametricos
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # opcional
```

## 3. Uso

```bash
.venv/bin/python extraer_parametros.py
.venv/bin/python extraer_parametros.py --url http://otro-host:8510/v1/ --salida /tmp/salida
```

| Opción / variable | Descripción | Por defecto |
|---|---|---|
| `--url` o `PARAMETROS_URL` | URL base de `parametros_crud` | URL de pruebas |
| `--salida` | Directorio donde se escriben el Excel y el reporte | `./salida` |
| `PARAMETROS_TOKEN` | Token Bearer, solo si el servicio lo exige | vacío |

Las variables se leen del entorno o de un `.env` junto al script (el `.env` no se sube al repositorio). Si no hay conexión, el script termina con código 2 y pide verificar la VPN y la URL. Las peticiones tienen timeout de 10 s para conectar y 60 s para leer, con reintentos ante errores 502, 503 y 504.

**Cómo consulta el servicio**

1. `GET tipo_parametro/<id>` por cada tipo del entorno, para obtener su nombre.
2. `GET parametro/<id>` por cada parámetro específico del entorno, para conocer su tipo real. Si el tipo no está entre los del entorno, se agrega como hoja ("tipo descubierto").
3. `GET parametro?query=TipoParametroId:<id>&limit=200&offset=<n>&sortby=Id&order=asc` por cada tipo, paginando hasta una página incompleta. **No** se filtra por `Activo`.
4. `GET parametro?query=TipoParametroId:<id>&limit=0` para contrastar el total con la paginación.

El servicio responde `{"Success", "Status", "Message", "Data"}`. Sin resultados devuelve `Data: [{}]`; ese objeto vacío se descarta.

## 4. Estructura del Excel

| Hoja | Contenido |
|---|---|
| **Índice** | Id del tipo, nombre del tipo (de `tipo_parametro`), variable de entorno, cantidad de parámetros e hipervínculo a la hoja. Debajo: ambiente, URL usada, fecha de extracción, total y fuente de las constantes. En los tipos descubiertos, la variable indica qué constantes llevaron a ellos. |
| **`<id> <nombre del tipo>`** | Una por tipo, ordenadas por id de tipo. Filas ordenadas por Id. Columnas: Id, Nombre, Descripción, Código abreviación, Aplica para Rectoría, Aplica para IDEXUD. |

Nombre de hoja: `"<id> <nombre>"` sin los caracteres `[]:*?/\`, cortado a 31 caracteres y único (p. ej. `141 Estados internos del contra`).

Formato: cabecera en negrita, blanca sobre azul; fila 1 congelada; autofiltro; anchos ajustados al contenido con tope; texto ajustado en Nombre y Descripción; bordes finos. Las columnas "Aplica para…" tienen validación con la lista `Sí,No` hasta 100 filas después de la última, por si negocio agrega registros.

## 5. Fuente de las constantes

`udistrital/gestion_contractual_mf`, rama `develop`, archivo `src/environments/environment.development.ts`, último cambio en el commit `17e8e53` (2026-09-29). Punta de `develop` al momento de la extracción: `1c54465`.

| Grupo | Constantes |
|---|---|
| Tipos de parámetro (22) | `TIPO_COMPROMISO_ID` 111 … `ENUMERACION_CLAUSULAS_ID` 135, `TIPO_ESTADO_ID` 137, `UNIDAD_EJECUCION_ID` 7, `UNIDAD_EJECUTORA_ID` 146 |
| Parámetros específicos (29) | `ORDEN_ID`, `CONTRATO_ID`, `CONVENIO_ID`, `CONTRATO_PSPAG_ID`, `PESO_COLOMBIANO_ID`, `AMPARO_CREC_ID`, `SUFICIENCIA_*`, `UNIDADES_EJECUTORAS.*`, `ESTADOS_GENERALES.*`, `ESTADOS_INTERNOS.*`, `TIPO_DOCUMENTO_ID_PARAMETROS.*` |
| Excluidas | `TIPO_DOCUMENTO_ID_GESTOR_DOCUMENTAL.*` y `ESPECIFICACIONES_ENLACE_XLSX` (son de gestor_documental) y los estados en texto `ESTADO_CONTRATO_*` |

El detalle está en `config_parametros.py`. Para cada parámetro específico se registra el tipo esperado según su uso en el MF (con qué lista se compara); queda en `None` cuando el MF no permite inferirlo.

## 6. Resultado de la extracción (13/10/2026, ambiente de pruebas)

| Indicador | Valor |
|---|---|
| Tipos de parámetro del entorno | 22, todos existen y están activos |
| Parámetros específicos del entorno | 29, todos existen; los que tienen tipo esperado coinciden |
| Tipos descubiertos | 3: 131 Suficiencia Amparo, 133 Documentos Contrato, 141 Estados internos del contrato |
| Hojas de tipo | 25 |
| Parámetros exportados | 286 (282 activos, 4 inactivos) |
| Paginación vs `limit=0` | 286 = 286, coincide en los 25 tipos |

La paginación también se probó con páginas de 5 registros (tipos 114, 135, 7, 112 y 131): mismos totales, sin repetidos y en orden por Id.

## 7. Hallazgos

### 7.1 Bug en el MF: filtros de parámetros hijos separados con `&`

**Archivo:** `gestion_contractual_mf` (develop, `1c54465`), `src/app/modules/registro-contrato/paso-info-general/paso-info-general.component.ts`

| Línea | Método | Desplegable |
|---|---|---|
| 443 | `CargartipoContratoIds(id_compromiso)` | Tipo de contrato |
| 455 | `CargartipologiaEspecificaId(id_contrato)` | Tipología específica |
| 469 | `CargarPerfilContratista(id_contrato)` | Perfil del contratista |

**Consulta actual** (la de la línea 455; las otras dos son iguales con `TIPO_CONTRATO_ID` y `PERFIL_CONTRATISTA_ID`):

```
parametro?query=ParametroPadreId:${id_contrato}&TipoParametroId:${environment.TIPOLOGIA_ESPECIFICA_ID},Activo:true&limit=0&sortby=numeroOrden&order=asc&fields=Id,Nombre
```

**Consulta corregida:**

```
parametro?query=ParametroPadreId:${id_contrato},TipoParametroId:${environment.TIPOLOGIA_ESPECIFICA_ID},Activo:true&limit=0&sortby=numeroOrden&order=asc&fields=Id,Nombre
```

**Causa.** `parametros_crud` separa los filtros de `query` por comas. Con `&`, el navegador envía `TipoParametroId:…,Activo:true` como otro parámetro de URL que el servicio ignora, y el filtro queda solo en `ParametroPadreId`.

**Verificación contra el servicio de pruebas** (`limit=0`):

| Consulta | Con `&` (actual) | Con `,` (corregida) |
|---|---|---|
| `ParametroPadreId:6535` + `Activo:false` | 10 | 0 |
| `ParametroPadreId:6535` + `TipoParametroId:999` | 10 | 0 |
| `ParametroPadreId:6546` + `TipoParametroId:114,Activo:true` (tipología) | 11 | 3 |
| `ParametroPadreId:6546` + `TipoParametroId:113,Activo:true` (perfil) | 11 | 7 |

**Impacto**

- **Hoy:** al elegir el tipo de contrato *Contrato de Prestación de Servicios Profesionales o Apoyo a la Gestión* (6546), los desplegables de tipología específica y de perfil del contratista muestran los 11 hijos de 6546. Son 3 tipologías (114), 7 perfiles (113) y "Documentos precontractuales" (133), en vez de 3 y 7 opciones.
- **En la depuración:** esos desplegables muestran también los hijos **inactivos**. Una inactivación hecha como resultado de esta revisión no se vería en ellos.
- El desplegable de tipo de contrato (línea 443) no muestra diferencias con los datos actuales, porque los hijos de 6534, 6535 y 6536 son todos del tipo 112 y activos. Tiene el mismo defecto.

No se corrige en el MF desde esta issue; queda documentado para que se programe.

### 7.2 Tipo Persona sin parámetros activos

Los dos parámetros del tipo 132 (6711 Natural, 6712 Jurídica) están inactivos. `consulta-contrato.component.ts:333` los consulta con `Activo:true`, así que ese filtro de la consulta de contratos queda vacío.

### 7.3 Suficiencia Amparo inactiva

El tipo 131 y sus dos parámetros (6708 SMLV y 6709 Porcentaje, constantes `SUFICIENCIA_SMLV_ID` y `SUFICIENCIA_PORCENTAJE_ID`) están inactivos. Esas constantes están declaradas en el entorno, pero el código del MF en `develop` no las usa.

### 7.4 Estados internos con datos incoherentes

- 6821 (`EN_REVISION_ORDENADOR`) y 6822 (`REVISADO_ORDENADOR`) se llaman "IDEXUD", con código "IDEXUD" y descripción "Unidad Ejecutora IDEXUD". No describen el estado que representan.
- 6801 (`EN_FIRMA_ORDENADOR`) tiene el nombre "En Firma Ordenador", pero el código `REV_ORD` y la descripción "En revisión Ordenador".
- 6802 (`EN_FIRMA_CONTRATISTA`) tiene el código `REV_CONT` con el nombre "En Firma Contratista".

### 7.5 Otras inconsistencias para la depuración

La sección 6 del reporte lista los códigos repetidos dentro de un tipo, por ejemplo `CCON` en 6547 Consultoría y 6548 Mutuo (tipo 112), y cuatro códigos repetidos en tipología específica (114). El nombre del tipo 118 está escrito "Ámparo".

## 8. Cómo actualizarlo cuando cambie el entorno

1. Revisar el historial de `src/environments/environment.development.ts` en `gestion_contractual_mf` (`develop`).
2. Actualizar `TIPOS_PARAMETRO`, `PARAMETROS_ESPECIFICOS` o `EXCLUIDAS` en `config_parametros.py` y el commit en `FUENTE_ENTORNO`.
3. Ejecutar el extractor y revisar en `salida/reporte_validacion.md` las constantes que no existen, los tipos que no coinciden y los tipos descubiertos.
4. Actualizar la sección 5 de este documento y subir el Excel nuevo.
