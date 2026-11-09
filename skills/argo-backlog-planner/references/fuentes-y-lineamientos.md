# Fuentes, plantillas y lineamientos

## Plantillas de Issues

Copias consultadas mediante MCP el 2026-11-08, incluidas como respaldo en `assets/issue-templates/`:

| Plantilla | Uso | SHA del archivo |
|---|---|---|
| [Analista](https://github.com/udistrital/argo_documentacion/blob/main/.github/ISSUE_TEMPLATE/template-for-analyst-.md) | Análisis, diseño, refinamiento, documentación de reglas o especificaciones | 7c8e6a0241f0baf6c09595c1adaa4590d6f0a0eb |
| [Desarrollador](https://github.com/udistrital/argo_documentacion/blob/main/.github/ISSUE_TEMPLATE/template-for-developer-.md) | Solo por solicitud explícita del usuario al crear la Issue | 649d9174affe4a8552c95ce29804546498d5cd7d |
| [Desarrollador plus](https://github.com/udistrital/argo_documentacion/blob/main/.github/ISSUE_TEMPLATE/template-for-developer-plus.md) | Predeterminada para desarrollo; incluir solo lineamientos aplicables | 4dfe32f304c733d9716dfc34a4b1cc706c789212 |

Consultar la versión vigente mediante MCP cuando haya acceso; en modo sin conexión, utilizar el respaldo e indicar su fecha. Las copias conservan el contenido original, incluidas casillas premarcadas; al redactar, no afirmar que el equipo refinó, aprobó o resolvió dependencias sin evidencia. Mantener textos y orden del DoR/DoD y ajustar únicamente las marcas a hechos comprobados. No copiar el frontmatter de configuración de GitHub como cuerpo de la Issue.

## Selección de lineamientos

Consultar solo los documentos que afecten la tarea. Incorporar sus enlaces en las secciones correspondientes de la Issue y derivar subtareas o criterios concretos cuando el alcance lo requiera. No convertir cada Issue en una actualización integral de todo el repositorio.

| Tipo de trabajo | Referencias |
|---|---|
| Todo desarrollo | [Branches](https://github.com/udistrital/lineamientos_oas/blob/master/repositorios_institucionales/nombre_branch.md), [commits](https://github.com/udistrital/lineamientos_oas/blob/master/repositorios_institucionales/etiqueta_commits.md), [README](https://github.com/udistrital/lineamientos_oas/blob/master/repositorios_institucionales/contenido_readme.md) |
| Microclientes Single-SPA | [Microclientes](https://github.com/udistrital/lineamientos_oas#microclientes), [introducción](https://github.com/udistrital/lineamientos_oas/blob/master/single_spa/single_spa.md); según componente: [Root](https://github.com/udistrital/lineamientos_oas/blob/master/single_spa/root_config.md), [Parcel](https://github.com/udistrital/lineamientos_oas/blob/master/single_spa/parcel.md), [Core](https://github.com/udistrital/lineamientos_oas/blob/master/single_spa/core.md), [Shared](https://github.com/udistrital/lineamientos_oas/blob/master/single_spa/shared.md) |
| Microservicios REST | [Endpoints](https://github.com/udistrital/lineamientos_oas/blob/master/generacion_de_apis/lineamientos-endpoints.md), [ambientes dockerizados](https://github.com/udistrital/lineamientos_oas/blob/master/ambientes_dockerizados/dockerizacion.md), [health check](https://github.com/udistrital/lineamientos_oas/blob/master/generacion_de_apis/endpoint_validacions.md#health-check-validación-de-estado-en-apis) |
| Go/Beego | [APIs Beego](https://github.com/udistrital/lineamientos_oas#5-apis-beego-mortar_board), [pruebas unitarias](https://github.com/udistrital/lineamientos_oas/blob/master/pruebas_unitarias_api_beego/unit_test_beego.md) |
| NestJS | [Guía API NestJS](https://github.com/udistrital/lineamientos_oas/blob/master/api_nest/api_nest.md); consultar los documentos relacionados desde el índice institucional |
| Python | Identificar el framework en el repositorio; [guía Flask](https://github.com/udistrital/lineamientos_oas/blob/master/api_flask/api_flask.md) solo si corresponde a Flask. No asumir que todo backend Python usa Flask |
| Datos relacionales | [Lineamientos de modelos relacionales](https://github.com/udistrital/lineamientos_oas/blob/master/modelo_de_datos/lineamientos_modelos_relacionales.md) |
| MongoDB | [Lineamientos Mongo](https://github.com/udistrital/lineamientos_oas/blob/master/modelo_de_datos/lineamientos_mongo.md) |

El enlace proporcionado originalmente a `modelo_de_datos/estandar.md` devolvió “Not Found” durante la creación. El índice institucional apunta al documento de modelos relacionales de la tabla, que sí fue consultado. Si el usuario necesita una versión histórica específica, resolver esa diferencia antes de atribuirle reglas.

La [hoja resumen REST de SharePoint](https://udistritaleduco-my.sharepoint.com/:p:/g/personal/computo_udistrital_edu_co/EYwQbkAKVCJCqrmJ7NgnjQ4B8WSd81vxGVx-hqi0WBAcfQ?e=lJZdx8) no pudo leerse al crear la skill. Puede mantenerse como material de apoyo aportado; no afirmar haber aplicado su contenido sin consultarlo.

La guía histórica de health check muestra código Beego antiguo. Verificar framework y versión reales antes de convertir ejemplos en especificaciones. No imponer imports antiguos a Beego v2, NestJS o Python. Para endpoints nuevos, el documento consultado pide recursos en español sin tildes/ñ, minúsculas y guiones, y métodos HTTP adecuados; para endpoints existentes, evaluar compatibilidad y consumidores antes de proponer renombres.

## Repositorios y contexto

- Fuente del equipo: [repositorios ARGO](https://github.com/orgs/udistrital/teams/argo/repositories).
- Tablero de referencia: [Project 63](https://github.com/orgs/udistrital/projects/63).
- Contexto opcional: `context/resumen_global_proyecto_argo_63.md` en la raíz de argo_documentacion o [versión en GitHub](https://github.com/udistrital/argo_documentacion/blob/main/context/resumen_global_proyecto_argo_63.md).
- Reglas y especificaciones adicionales: `docs/business-rules/`, si contienen material pertinente.

El usuario proporcionó los 11 repositorios utilizados por ARGO, recogidos en el [catálogo de repositorios](repositorios-argo.md). Usar ese catálogo para definir dónde se requiere el desarrollo. La falta de acceso al listado del equipo no bloquea su selección ni exige reconfirmar los nombres proporcionados.

Los nombres adicionales que aparezcan en el resumen son contexto histórico, no ampliaciones automáticas del catálogo. Confirmar responsabilidad, rama y tecnología con README y manifiestos (`package.json`, `go.mod`, `pyproject.toml` o `requirements.txt`) antes de fijar detalles técnicos. Separar repositorio de seguimiento de la Issue de los repositorios de implementación.

Cuando se aporte contexto del tablero, usarlo para evitar duplicados y reconocer dependencias, respetando su fecha de corte. Una Issue cerrada o un resumen histórico no prueba despliegue ni estado vigente. No refrescar todo el tablero si la tarea ya tiene contexto suficiente; consultar los elementos que afectan la decisión.

