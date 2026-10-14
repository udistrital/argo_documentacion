# Reporte de validación — datos paramétricos ARGO v2 (issue #377)

- **Fecha de extracción:** 2026-10-13 20:00:27 -0500
- **Ambiente:** Pruebas (intranet OAS, requiere VPN)
- **URL:** http://pruebasapi.intranetoas.udistrital.edu.co:8510/v1/
- **Fuente de las constantes:** `udistrital/gestion_contractual_mf`, rama `develop`, commit `17e8e53`, `src/environments/environment.development.ts`
- **Excel generado:** `consolidado_parametros_argo_v2_2026-10-13.xlsx`

## 1. Tipos de parámetro del entorno

| Variable | Id | Existe | Nombre (tipo_parametro) | Activo |
|---|---|---|---|---|
| `UNIDAD_EJECUCION_ID` | 7 | Sí | Tiempo | Sí |
| `TIPO_COMPROMISO_ID` | 111 | Sí | Compromiso | Sí |
| `TIPO_CONTRATO_ID` | 112 | Sí | Contrato | Sí |
| `PERFIL_CONTRATISTA_ID` | 113 | Sí | Perfil del Contratista | Sí |
| `TIPOLOGIA_ESPECIFICA_ID` | 114 | Sí | Tipología Específica | Sí |
| `MODALIDAD_SELECCION_ID` | 115 | Sí | Modalidad de Selección | Sí |
| `REGIMEN_CONTRATACION_ID` | 116 | Sí | Régimen de Contratación | Sí |
| `PROCEDIMIENTO_ID` | 117 | Sí | Procedimiento | Sí |
| `AMPARO_ID` | 118 | Sí | Ámparo | Sí |
| `TIPO_CONTROL_ID` | 119 | Sí | Tipo de Control | Sí |
| `CLASE_CONTRATISTA_ID` | 120 | Sí | Clase Contratista | Sí |
| `VIGENCIA_ID` | 121 | Sí | Vigencia | Sí |
| `TIPO_MONEDA` | 122 | Sí | Tipo de Moneda | Sí |
| `TIPO_GASTO_ID` | 123 | Sí | Tipo de Gasto | Sí |
| `ORIGEN_RECURSOS_ID` | 124 | Sí | Origen Recursos | Sí |
| `ORIGEN_PRESUPUESTO_ID` | 125 | Sí | Origen Presupuesto | Sí |
| `TEMA_GASTO_ID` | 126 | Sí | Tema Gasto Inversión | Sí |
| `MEDIO_PAGO_ID` | 127 | Sí | Medio de Pago | Sí |
| `TIPO_PERSONA_ID` | 132 | Sí | Tipo Persona | Sí |
| `ENUMERACION_CLAUSULAS_ID` | 135 | Sí | Enumeración cláusulas | Sí |
| `TIPO_ESTADO_ID` | 137 | Sí | Estados del contrato | Sí |
| `UNIDAD_EJECUTORA_ID` | 146 | Sí | Unidad Ejecutora | Sí |

## 2. Parámetros específicos del entorno

| Variable | Id | Existe | Nombre | Activo | Tipo real | Tipo esperado | Coincide |
|---|---|---|---|---|---|---|---|
| `ORDEN_ID` | 6534 | Sí | 3 - Orden | Sí | 111 Compromiso | 111 | Sí |
| `CONTRATO_ID` | 6535 | Sí | 2 - Contrato | Sí | 111 Compromiso | 111 | Sí |
| `CONVENIO_ID` | 6536 | Sí | 1 - Convenio | Sí | 111 Compromiso | 111 | Sí |
| `CONTRATO_PSPAG_ID` | 6546 | Sí | Contrato de Prestación de Servicios Profesionales o Apoyo a la Gestión | Sí | 112 Contrato | 112 | Sí |
| `PESO_COLOMBIANO_ID` | 6634 | Sí | Pesos Colombianos | Sí | 122 Tipo de Moneda | 122 | Sí |
| `AMPARO_CREC_ID` | 6609 | Sí | Amparo de Responsabilidad Civil Extra- Contractual | Sí | 118 Ámparo | 118 | Sí |
| `SUFICIENCIA_SMLV_ID` | 6708 | Sí | SMLV | No | 131 Suficiencia Amparo | — | — |
| `SUFICIENCIA_PORCENTAJE_ID` | 6709 | Sí | Porcentaje | No | 131 Suficiencia Amparo | — | — |
| `UNIDADES_EJECUTORAS.RECTORIA` | 6818 | Sí | Rector | Sí | 146 Unidad Ejecutora | 146 | Sí |
| `UNIDADES_EJECUTORAS.IDEXUD` | 6819 | Sí | IDEXUD | Sí | 146 Unidad Ejecutora | 146 | Sí |
| `ESTADOS_GENERALES.POR_SUSCRIBIR` | 6773 | Sí | POR SUSCRIBIR | Sí | 137 Estados del contrato | — | — |
| `ESTADOS_GENERALES.SUSCRITO` | 6774 | Sí | SUSCRITO | Sí | 137 Estados del contrato | — | — |
| `ESTADOS_GENERALES.EN_EJECUCION` | 6777 | Sí | EN EJECUCIÓN | Sí | 137 Estados del contrato | — | — |
| `ESTADOS_GENERALES.LEGALIZADO` | 6776 | Sí | LEGALIZADO | Sí | 137 Estados del contrato | — | — |
| `ESTADOS_GENERALES.DECLINADO` | 6775 | Sí | DECLINADO | Sí | 137 Estados del contrato | — | — |
| `ESTADOS_INTERNOS.BORRADOR` | 6799 | Sí | Borrador | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.EN_REVISION_JEFE` | 6800 | Sí | En Revisión Jefe | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.APROBADO_JEFE` | 6809 | Sí | Aprobado Jefe | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.EN_REVISION_ORDENADOR` | 6821 | Sí | IDEXUD | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.REVISADO_ORDENADOR` | 6822 | Sí | IDEXUD | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.EN_FIRMA_ORDENADOR` | 6801 | Sí | En Firma Ordenador | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.FIRMADO_ORDENADOR` | 6808 | Sí | Firmado por Ordenador | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.EN_FIRMA_CONTRATISTA` | 6802 | Sí | En Firma Contratista | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.FIRMADO_CONTRATISTA` | 6804 | Sí | Firmado por Contratista | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.FIRMAS_COMPLETAS` | 6817 | Sí | Firmas de contrato completas | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.RECHAZADO` | 6803 | Sí | Rechazado | Sí | 141 Estados internos del contrato | — | — |
| `ESTADOS_INTERNOS.DECLINADO` | 6807 | Sí | Declinado | Sí | 141 Estados internos del contrato | — | — |
| `TIPO_DOCUMENTO_ID_PARAMETROS.MINUTA` | 6805 | Sí | Minuta | Sí | 133 Documentos Contrato | — | — |
| `TIPO_DOCUMENTO_ID_PARAMETROS.DOCUMENTOS_PRECONTRACTUALES` | 6716 | Sí | Documentos precontractuales | Sí | 133 Documentos Contrato | — | — |

El tipo esperado sale del uso de la constante en el MF (con qué lista se compara); «—» indica que el MF no permite inferirlo.

## 3. Tipos descubiertos a partir de los parámetros específicos

| Id | Nombre | Activo | Constantes que lo referencian | Parámetros |
|---|---|---|---|---|
| 131 | Suficiencia Amparo | No | `SUFICIENCIA_SMLV_ID`, `SUFICIENCIA_PORCENTAJE_ID` | 2 |
| 133 | Documentos Contrato | Sí | `TIPO_DOCUMENTO_ID_PARAMETROS.MINUTA`, `TIPO_DOCUMENTO_ID_PARAMETROS.DOCUMENTOS_PRECONTRACTUALES` | 2 |
| 141 | Estados internos del contrato | Sí | `ESTADOS_INTERNOS.BORRADOR`, `ESTADOS_INTERNOS.EN_REVISION_JEFE`, `ESTADOS_INTERNOS.APROBADO_JEFE`, `ESTADOS_INTERNOS.EN_REVISION_ORDENADOR`, `ESTADOS_INTERNOS.REVISADO_ORDENADOR`, `ESTADOS_INTERNOS.EN_FIRMA_ORDENADOR`, `ESTADOS_INTERNOS.FIRMADO_ORDENADOR`, `ESTADOS_INTERNOS.EN_FIRMA_CONTRATISTA`, `ESTADOS_INTERNOS.FIRMADO_CONTRATISTA`, `ESTADOS_INTERNOS.FIRMAS_COMPLETAS`, `ESTADOS_INTERNOS.RECHAZADO`, `ESTADOS_INTERNOS.DECLINADO` | 12 |

## 4. Conteo por tipo y verificación de la paginación

Paginación con `limit=200` y `offset`, ordenada por `Id`, frente a una consulta con `limit=0`. Ambas sin filtro de `Activo`.

| Id | Tipo | Hoja | Paginación | Páginas | limit=0 | Coincide | Activos | Inactivos |
|---|---|---|---|---|---|---|---|---|
| 7 | Tiempo | 7 Tiempo | 19 | 1 | 19 | Sí | 19 | 0 |
| 111 | Compromiso | 111 Compromiso | 3 | 1 | 3 | Sí | 3 | 0 |
| 112 | Contrato | 112 Contrato | 12 | 1 | 12 | Sí | 12 | 0 |
| 113 | Perfil del Contratista | 113 Perfil del Contratista | 7 | 1 | 7 | Sí | 7 | 0 |
| 114 | Tipología Específica | 114 Tipología Específica | 73 | 1 | 73 | Sí | 73 | 0 |
| 115 | Modalidad de Selección | 115 Modalidad de Selección | 8 | 1 | 8 | Sí | 8 | 0 |
| 116 | Régimen de Contratación | 116 Régimen de Contratación | 5 | 1 | 5 | Sí | 5 | 0 |
| 117 | Procedimiento | 117 Procedimiento | 6 | 1 | 6 | Sí | 6 | 0 |
| 118 | Ámparo | 118 Ámparo | 12 | 1 | 12 | Sí | 12 | 0 |
| 119 | Tipo de Control | 119 Tipo de Control | 3 | 1 | 3 | Sí | 3 | 0 |
| 120 | Clase Contratista | 120 Clase Contratista | 2 | 1 | 2 | Sí | 2 | 0 |
| 121 | Vigencia | 121 Vigencia | 19 | 1 | 19 | Sí | 19 | 0 |
| 122 | Tipo de Moneda | 122 Tipo de Moneda | 8 | 1 | 8 | Sí | 8 | 0 |
| 123 | Tipo de Gasto | 123 Tipo de Gasto | 5 | 1 | 5 | Sí | 5 | 0 |
| 124 | Origen Recursos | 124 Origen Recursos | 7 | 1 | 7 | Sí | 7 | 0 |
| 125 | Origen Presupuesto | 125 Origen Presupuesto | 5 | 1 | 5 | Sí | 5 | 0 |
| 126 | Tema Gasto Inversión | 126 Tema Gasto Inversión | 23 | 1 | 23 | Sí | 23 | 0 |
| 127 | Medio de Pago | 127 Medio de Pago | 4 | 1 | 4 | Sí | 4 | 0 |
| 131 | Suficiencia Amparo | 131 Suficiencia Amparo | 2 | 1 | 2 | Sí | 0 | 2 |
| 132 | Tipo Persona | 132 Tipo Persona | 2 | 1 | 2 | Sí | 0 | 2 |
| 133 | Documentos Contrato | 133 Documentos Contrato | 2 | 1 | 2 | Sí | 2 | 0 |
| 135 | Enumeración cláusulas | 135 Enumeración cláusulas | 40 | 1 | 40 | Sí | 40 | 0 |
| 137 | Estados del contrato | 137 Estados del contrato | 5 | 1 | 5 | Sí | 5 | 0 |
| 141 | Estados internos del contrato | 141 Estados internos del contra | 12 | 1 | 12 | Sí | 12 | 0 |
| 146 | Unidad Ejecutora | 146 Unidad Ejecutora | 2 | 1 | 2 | Sí | 2 | 0 |
| **Total** | | | **286** | | **286** | **Sí** | | |

Los inactivos se exportan en el Excel igual que los activos, sin marca que los distinga.

## 5. Diferencias y observaciones

- El parámetro `SUFICIENCIA_SMLV_ID` (6708, SMLV) está inactivo.
- El parámetro `SUFICIENCIA_PORCENTAJE_ID` (6709, Porcentaje) está inactivo.
- El tipo 131 (Suficiencia Amparo) está inactivo en tipo_parametro.
- Tipo 131 (Suficiencia Amparo): todos sus parámetros (2) están inactivos.
- Tipo 132 (Tipo Persona): todos sus parámetros (2) están inactivos.

## 6. Posibles inconsistencias para la depuración

Revisión automática de nombres y códigos repetidos dentro de cada tipo y de campos vacíos. No siempre son errores (p. ej. ordinales con el mismo prefijo); se listan para que negocio los revise.

- Tipo 7 (Tiempo): Código abreviación «m» repetido en 2 parámetros (178, 180).
- Tipo 112 (Contrato): Código abreviación «CCON» repetido en 2 parámetros (6547, 6548).
- Tipo 114 (Tipología Específica): Código abreviación «CBM» repetido en 2 parámetros (6551, 6552).
- Tipo 114 (Tipología Específica): Código abreviación «SSV» repetido en 2 parámetros (6556, 6557).
- Tipo 114 (Tipología Específica): Código abreviación «OS» repetido en 2 parámetros (6560, 6570).
- Tipo 114 (Tipología Específica): Código abreviación «CIS» repetido en 2 parámetros (6882, 6883).
- Tipo 135 (Enumeración cláusulas): Código abreviación «VIGÉSIMA» repetido en 10 parámetros (6749, 6750, 6751, 6752, 6753, 6754, 6755, 6756, 6757, 6758).
- Tipo 135 (Enumeración cláusulas): Código abreviación «TRIGÉSIMA» repetido en 10 parámetros (6759, 6760, 6761, 6762, 6763, 6764, 6765, 6766, 6767, 6768).
- Tipo 141 (Estados internos del contrato): Nombre «IDEXUD» repetido en 2 parámetros (6821, 6822).
- Tipo 141 (Estados internos del contrato): Código abreviación «IDEXUD» repetido en 2 parámetros (6821, 6822).

## 7. Constantes del entorno excluidas

| Constante | Motivo |
|---|---|
| `TIPO_DOCUMENTO_ID_GESTOR_DOCUMENTAL.*` | Ids de tipo documental de gestor_documental (183, 174, 175, 176, 177) |
| `ESPECIFICACIONES_ENLACE_XLSX` | UUID de un documento en gestor_documental |
| `ESTADO_CONTRATO_*` | Estados en texto ('EN EJECUCION', 'SUSCRITO', 'POR SUSCRIBIR', 'LEGALIZADO') |
