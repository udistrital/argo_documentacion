# Repositorios utilizados por ARGO

Fuente: listado proporcionado explícitamente por el usuario el 8 de noviembre de 2026. Los nombres y enlaces están confirmados como repositorios utilizados por ARGO. Las orientaciones siguientes sirven para seleccionar candidatos; no constituyen una auditoría del código ni certifican versiones, endpoints o límites funcionales actuales.

## Catálogo y orientación de selección

| Repositorio | Cambios para los que debe considerarse |
|---|---|
| [cargue_archivo_mid_serverless](https://github.com/udistrital/cargue_archivo_mid_serverless) | Procesamiento de cargue de archivos en el componente serverless; confirmar formatos y operaciones implementadas. |
| [clausulas_paragrafos_crud](https://github.com/udistrital/clausulas_paragrafos_crud) | Persistencia y operaciones sobre cláusulas, parágrafos y sus estructuras asociadas. |
| [gestion_contractual_mf](https://github.com/udistrital/gestion_contractual_mf) | Formularios, vistas, interacción y consumo de servicios del microcliente de gestión contractual. |
| [gestion_contractual_crud](https://github.com/udistrital/gestion_contractual_crud) | Modelo de datos, persistencia, migraciones y operaciones CRUD del dominio contractual. |
| [gestion_contractual_mid](https://github.com/udistrital/gestion_contractual_mid) | Lógica contractual, agregación de datos y orquestación de servicios para los flujos de gestión contractual. |
| [gestion_contractual_root_mf](https://github.com/udistrital/gestion_contractual_root_mf) | Contenedor raíz y composición, carga o montaje de microclientes Single-SPA. |
| [minuta_contractual_mid](https://github.com/udistrital/minuta_contractual_mid) | Preparación y transformación de información contractual para la generación de minutas y coordinación del proceso documental. |
| [ordenador_supervisor_mid](https://github.com/udistrital/ordenador_supervisor_mid) | Consultas e integración de información de ordenadores del gasto y supervisores. |
| [presupuesto_contractual_mid](https://github.com/udistrital/presupuesto_contractual_mid) | Consultas e integración de información presupuestal, disponibilidades y CDP. |
| [proveedores_mid](https://github.com/udistrital/proveedores_mid) | Consultas e integración de información de proveedores o contratistas. |
| [renderizado_plantillas_html](https://github.com/udistrital/renderizado_plantillas_html) | Motor de renderizado de plantillas HTML; verificar las salidas y operaciones soportadas antes de atribuir generación de PDF u otras funciones. |

## Cómo asignar cada Issue

1. Identificar el resultado esperado y el componente que necesita cambios. Usar la tabla para seleccionar el candidato y contrastar su responsabilidad con el contexto o el código pertinente cuando exista ambigüedad.
2. Identificar un repositorio principal de implementación por Issue, con enlace y una justificación breve. Por ejemplo, un ajuste visual del formulario corresponde al microcliente; un cambio de reglas o de persistencia puede requerir Issues adicionales en MID o CRUD.
3. Separar entregables por repositorio y vincular dependencias. No crear una Issue para cada servicio consultado si no requiere modificaciones. Registrar esos servicios como dependencias de integración.
4. Distinguir preparación de datos de minuta, renderizado y visualización. Un problema de documento no implica automáticamente cambios en los tres repositorios. Precisar el origen antes de dividirlo.
5. Verificar framework, versión y rama con README, manifiestos y archivos pertinentes mediante MCP o checkout local. Los sufijos `mid`, `crud` o `serverless` no bastan para afirmar Go, NestJS, Python, Beego, Flask ni una plataforma concreta.
6. Si falta evidencia para elegir entre repositorios, documentar candidatos y la pregunta específica pendiente. No inventar rutas o contratos para justificar la asignación.
7. Si el trabajo necesita un repositorio fuera del catálogo, distinguir dependencia externa de desarrollo adicional. Justificar el alcance y confirmar la asignación si no está autorizada o respaldada por los insumos; no suponer que el catálogo prohíbe integraciones externas.

`udistrital/argo_documentacion` sigue siendo el repositorio de seguimiento propuesto. Los archivos de Issues se guardan localmente en su carpeta `backlog/`, aunque el desarrollo corresponda a otro repositorio del catálogo. Las tareas exclusivamente documentales pueden identificar `argo_documentacion` como destino del artefacto.
