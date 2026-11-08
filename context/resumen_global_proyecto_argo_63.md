# Resumen global del proyecto ARGO — GitHub Project 63

**Proyecto:** [udistrital / Projects / 63](https://github.com/orgs/udistrital/projects/63)  
**Fecha de consulta:** 8 de noviembre de 2026 (America/Bogota).  
**Fuente:** MCP de GitHub, búsqueda de issues vinculadas mediante `project:udistrital/63 is:issue`.

## 1. Resumen ejecutivo

El trabajo registrado corresponde a la modernización de ARGO v1 hacia ARGO v2 para gestionar la contratación de la Universidad Distrital. Comprende el conocimiento del sistema anterior, levantamiento de requerimientos, diseño de procesos y modelos de datos, construcción de microfrontends y microservicios, integración con sistemas institucionales, generación documental y pruebas.

El núcleo funcional es la gestión de contratos y órdenes de compra y servicios: registro, consulta, información del proveedor, presupuesto, cláusulas, especificaciones técnicas, supervisores, ordenadores del gasto, aprobaciones y firma. Se complementa con pólizas y amparos, actas de inicio y generación de minutas y documentos PDF. El proyecto incorpora diferencias operativas entre Rectoría e IDEXUD y permisos según rol y unidad ejecutora.

El historial muestra una base funcional desarrollada e integrada, con numerosas actividades cerradas. Al corte continúa un ciclo de refinamiento del modelo de datos, consolidación de módulos, actualización tecnológica, integración entre capas y estabilización en pruebas. Por ello, el volumen de cierres no permite afirmar que toda la solución esté terminada o desplegada en producción.

## 2. Alcance y método

Se recuperaron las cuatro páginas de resultados (100 + 100 + 100 + 76), sin resultados incompletos reportados, y se verificaron **376 identificadores únicos**. Se revisaron títulos, estados, hitos y fechas del conjunto, y descripciones de las actividades para identificar frentes y profundizar en hitos representativos y pendientes recientes.

- **375 issues** pertenecen a `udistrital/argo_documentacion`.
- **1 issue** pertenece a `udistrital/sisifo_documentacion`: [#380, ajuste del componente de texto enriquecido de ARGO](https://github.com/udistrital/sisifo_documentacion/issues/380).
- La consulta `project:udistrital/63 is:pull-request` devolvió **0 resultados**. Esto no significa que los repositorios del sistema carezcan de PR; solo describe esa consulta de vinculación al proyecto.
- Las fechas de creación de las issues recuperadas van del **25 de abril de 2024 al 6 de noviembre de 2026**.

**Límites de la consulta:** las herramientas disponibles no expusieron los campos personalizados, vistas, iteraciones ni borradores de GitHub Projects. Los estados de este informe son los de las issues (abierta/cerrada), no las columnas del tablero. No se realizó auditoría del código ni comprobación de ambientes. El intento de consultar comentarios de las issues #337, #368, #390 y #398 mediante el otro conector MCP de GitHub devolvió 404; no se incorporaron sus comentarios ni se revisaron los documentos externos adjuntos. La cobertura corresponde a las issues que la búsqueda devolvió como vinculadas, no a una exportación integral del tablero.

## 3. Panorama cuantitativo

| Indicador | Resultado |
|---|---:|
| Issues recuperadas | 376 |
| Cerradas | 326 |
| Abiertas | 50 |
| Proporción de issues cerradas | 86,7 % |
| Proporción de issues abiertas | 13,3 % |

Estos porcentajes representan conteos de tareas; **no son un porcentaje de avance funcional, esfuerzo, aceptación ni despliegue**.

### Distribución por hito

| Hito registrado | Total | Cerradas | Abiertas |
|---|---:|---:|---:|
| Gestión Contractual | 290 | 262 | 28 |
| Exploración Inicial | 28 | 22 | 6 |
| Pólizas y amparos | 22 | 16 | 6 |
| Informes | 16 | 16 | 0 |
| Actas de inicio | 9 | 7 | 2 |
| Soporte y arquitectura general | 3 | 1 | 2 |
| Transversal | 1 | 1 | 0 |
| Sin hito | 7 | 1 | 6 |
| **Total** | **376** | **326** | **50** |

Gestión Contractual agrupa el 77,1 % de las issues. Los hitos reflejan la clasificación del repositorio: algunas tareas de pólizas, actas o arquitectura están clasificadas dentro de Gestión Contractual.

### Distribución por año de creación

| Año de creación | Total | Cerradas al corte | Abiertas al corte |
|---|---:|---:|---:|
| 2024 | 276 | 270 | 6 |
| 2025 | 45 | 44 | 1 |
| 2026 | 55 | 12 | 43 |

Esta tabla agrupa por creación; no mide cuántas tareas se ejecutaron o cerraron en cada año.

## 4. Frentes abordados

### 4.1. Descubrimiento, requerimientos y rediseño funcional

Se revisó documentación de ARGO v1, se realizaron sesiones con usuarios, se construyeron flujos y mockups y se identificaron dependencias con otros sistemas. Se analizaron posibilidades de unificación entre gestión contractual y órdenes de compra y servicios, además de la separación técnica en microclientes y servicios. La incorporación de IDEXUD llevó a refinar procesos y reglas particulares.

Evidencias: [#1](https://github.com/udistrital/argo_documentacion/issues/1), [#9](https://github.com/udistrital/argo_documentacion/issues/9), [#15](https://github.com/udistrital/argo_documentacion/issues/15), [#20](https://github.com/udistrital/argo_documentacion/issues/20), [#24](https://github.com/udistrital/argo_documentacion/issues/24), [#86](https://github.com/udistrital/argo_documentacion/issues/86), [#96](https://github.com/udistrital/argo_documentacion/issues/96), [#167](https://github.com/udistrital/argo_documentacion/issues/167) y [#171](https://github.com/udistrital/argo_documentacion/issues/171). En 2026 continúa el refinamiento con usuarios en [#371](https://github.com/udistrital/argo_documentacion/issues/371) y [#374](https://github.com/udistrital/argo_documentacion/issues/374). La investigación del proceso precontractual permanece abierta en [#355](https://github.com/udistrital/argo_documentacion/issues/355); no debe presentarse como un módulo implementado.

### 4.2. Arquitectura, persistencia y modernización tecnológica

Se diseñaron diagramas de arquitectura y modelos para contratos, cláusulas, pólizas, supervisores y ordenadores. Se construyeron capas CRUD y MID y microfrontends con Single-SPA. Los modelos y scripts evolucionaron a medida que se precisaron los requerimientos, las referencias al contrato general y las integraciones institucionales.

El historial reciente contempla actualización de Angular, atención de dependencias, migración del CRUD a Go/Beego y un nuevo CRUD basado en el modelo refinado. También propone consolidar pólizas y actas de inicio dentro de los componentes de gestión contractual. Estas decisiones tienen estados distintos y no se deben tratar como una migración totalmente concluida.

Evidencias: [#32](https://github.com/udistrital/argo_documentacion/issues/32), [#33](https://github.com/udistrital/argo_documentacion/issues/33), [#50](https://github.com/udistrital/argo_documentacion/issues/50), [#124](https://github.com/udistrital/argo_documentacion/issues/124), [#127](https://github.com/udistrital/argo_documentacion/issues/127), [#136](https://github.com/udistrital/argo_documentacion/issues/136), [#157](https://github.com/udistrital/argo_documentacion/issues/157), [#313](https://github.com/udistrital/argo_documentacion/issues/313), [#344](https://github.com/udistrital/argo_documentacion/issues/344), [#345](https://github.com/udistrital/argo_documentacion/issues/345), [#349](https://github.com/udistrital/argo_documentacion/issues/349), [#350](https://github.com/udistrital/argo_documentacion/issues/350), [#351](https://github.com/udistrital/argo_documentacion/issues/351), [#353](https://github.com/udistrital/argo_documentacion/issues/353), [#368](https://github.com/udistrital/argo_documentacion/issues/368) y [#385](https://github.com/udistrital/argo_documentacion/issues/385).

### 4.3. Registro y consulta de contratos

Se trabajó en el formulario por pasos, reglas de visibilidad, validaciones, almacenamiento asociado al identificador del contrato, consulta y edición. El alcance incluye información contractual, proveedor, disponibilidad presupuestal, lugar de ejecución, solicitante, supervisor, ordenador, especificaciones, cláusulas, garantías y documentos.

También se abordaron consulta por contratista, estado, fecha y unidad ejecutora; consecutivos y número de contrato; carga masiva de especificaciones y descarga de plantillas. La integración de registro, actualización y visualización figura cerrada en [#390](https://github.com/udistrital/argo_documentacion/issues/390), y la revisión funcional básica del registro en [#398](https://github.com/udistrital/argo_documentacion/issues/398). Persisten nuevas actividades de integración y rediseño en [#381](https://github.com/udistrital/argo_documentacion/issues/381), [#388](https://github.com/udistrital/argo_documentacion/issues/388) y [#397](https://github.com/udistrital/argo_documentacion/issues/397).

Evidencias adicionales: [#34](https://github.com/udistrital/argo_documentacion/issues/34), [#88](https://github.com/udistrital/argo_documentacion/issues/88), [#103](https://github.com/udistrital/argo_documentacion/issues/103), [#170](https://github.com/udistrital/argo_documentacion/issues/170), [#192](https://github.com/udistrital/argo_documentacion/issues/192), [#233](https://github.com/udistrital/argo_documentacion/issues/233), [#274](https://github.com/udistrital/argo_documentacion/issues/274), [#284](https://github.com/udistrital/argo_documentacion/issues/284), [#324](https://github.com/udistrital/argo_documentacion/issues/324) y [#325](https://github.com/udistrital/argo_documentacion/issues/325).

### 4.4. Integraciones institucionales

| Integración abordada | Propósito documentado | Evidencias |
|---|---|---|
| Ágora / proveedores MID | Consultar proveedor, tipo de persona y contratos asociados; validar información del contratista | [#53](https://github.com/udistrital/argo_documentacion/issues/53), [#61](https://github.com/udistrital/argo_documentacion/issues/61), [#80](https://github.com/udistrital/argo_documentacion/issues/80), [#138](https://github.com/udistrital/argo_documentacion/issues/138), [#292](https://github.com/udistrital/argo_documentacion/issues/292) |
| Sicapital / presupuesto contractual MID | Consultar disponibilidades por vigencia y unidad ejecutora, detalle del CDP y datos presupuestales | [#52](https://github.com/udistrital/argo_documentacion/issues/52), [#62](https://github.com/udistrital/argo_documentacion/issues/62), [#77](https://github.com/udistrital/argo_documentacion/issues/77), [#91](https://github.com/udistrital/argo_documentacion/issues/91), [#174](https://github.com/udistrital/argo_documentacion/issues/174) |
| Parámetros CRUD | Centralizar tipologías, selectores y datos paramétricos | [#35](https://github.com/udistrital/argo_documentacion/issues/35), [#75](https://github.com/udistrital/argo_documentacion/issues/75), [#76](https://github.com/udistrital/argo_documentacion/issues/76), [#98](https://github.com/udistrital/argo_documentacion/issues/98), [#99](https://github.com/udistrital/argo_documentacion/issues/99) |
| OIKOS, terceros y ordenador/supervisor MID | Resolver sedes, dependencias, personas, ordenadores y supervisores | [#70](https://github.com/udistrital/argo_documentacion/issues/70), [#194](https://github.com/udistrital/argo_documentacion/issues/194), [#253](https://github.com/udistrital/argo_documentacion/issues/253), [#259](https://github.com/udistrital/argo_documentacion/issues/259), [#289](https://github.com/udistrital/argo_documentacion/issues/289) |
| Gestor documental / Nuxeo | Almacenar y consultar soportes y minutas | [#126](https://github.com/udistrital/argo_documentacion/issues/126), [#235](https://github.com/udistrital/argo_documentacion/issues/235) |
| Plantillas y renderizado | Componer HTML y generar PDF a partir de datos contractuales | [#218](https://github.com/udistrital/argo_documentacion/issues/218), [#285](https://github.com/udistrital/argo_documentacion/issues/285), [#290](https://github.com/udistrital/argo_documentacion/issues/290), [#302](https://github.com/udistrital/argo_documentacion/issues/302) |

Las integraciones son parte central del alcance. El pendiente [#326](https://github.com/udistrital/argo_documentacion/issues/326) sobre actividades y objeto del CDP y los pendientes [#377](https://github.com/udistrital/argo_documentacion/issues/377), [#383](https://github.com/udistrital/argo_documentacion/issues/383) y [#387](https://github.com/udistrital/argo_documentacion/issues/387) muestran que aún hay ajustes de datos y de agregación entre fuentes.

### 4.5. Cláusulas, plantillas y minutas

Se desarrollaron modelos y servicios de cláusulas y parágrafos, edición de texto enriquecido, versionado de plantillas, parametrización por tipo de contrato, reglas de edición y asociación de cláusulas a contratos y unidades ejecutoras.

La generación documental incorpora reemplazo de variables y doble renderizado: primero se obtiene HTML y después se genera el PDF. Se separó el procesamiento de minutas en `minuta_contractual_mid`, incluyendo preparación de datos de amparos y especificaciones. Se registraron integración, almacenamiento documental y pruebas de generación por tipo de contrato.

Evidencias: [#122](https://github.com/udistrital/argo_documentacion/issues/122), [#139](https://github.com/udistrital/argo_documentacion/issues/139), [#156](https://github.com/udistrital/argo_documentacion/issues/156), [#193](https://github.com/udistrital/argo_documentacion/issues/193), [#200](https://github.com/udistrital/argo_documentacion/issues/200), [#224](https://github.com/udistrital/argo_documentacion/issues/224), [#285](https://github.com/udistrital/argo_documentacion/issues/285), [#302](https://github.com/udistrital/argo_documentacion/issues/302), [#307](https://github.com/udistrital/argo_documentacion/issues/307) y [#337](https://github.com/udistrital/argo_documentacion/issues/337). Continúan abiertas la evaluación del renderizado y pruebas de estabilización en [#354](https://github.com/udistrital/argo_documentacion/issues/354), [#361](https://github.com/udistrital/argo_documentacion/issues/361) y [#373](https://github.com/udistrital/argo_documentacion/issues/373).

### 4.6. Roles, estados, aprobación y firma

Se definieron matrices de roles y permisos, estados internos, acciones permitidas, observaciones y vistas de revisión del abogado, jefe de contratación y ordenador del gasto. Se incorporó firma mediante carga documental y tratamiento de flujos por unidad ejecutora.

La issue [#268](https://github.com/udistrital/argo_documentacion/issues/268) documenta diferencias entre Rectoría e IDEXUD: en IDEXUD el ordenador tiene una revisión previa y una firma posterior a la del contratista. Por tanto, el flujo no debe reducirse a una secuencia única para todas las unidades. También se abordó auditoría, consulta por unidad y controles de acceso.

Evidencias: [#201](https://github.com/udistrital/argo_documentacion/issues/201), [#228](https://github.com/udistrital/argo_documentacion/issues/228), [#242](https://github.com/udistrital/argo_documentacion/issues/242), [#243](https://github.com/udistrital/argo_documentacion/issues/243), [#257](https://github.com/udistrital/argo_documentacion/issues/257), [#268](https://github.com/udistrital/argo_documentacion/issues/268), [#278](https://github.com/udistrital/argo_documentacion/issues/278), [#304](https://github.com/udistrital/argo_documentacion/issues/304), [#315](https://github.com/udistrital/argo_documentacion/issues/315), [#366](https://github.com/udistrital/argo_documentacion/issues/366) y [#370](https://github.com/udistrital/argo_documentacion/issues/370). La maquetación de aprobación/rechazo masivo está cerrada en [#382](https://github.com/udistrital/argo_documentacion/issues/382); ese cierre no demuestra por sí solo que el flujo masivo completo esté integrado.

### 4.7. Pólizas, amparos y actas de inicio

El proyecto abordó modelos de datos, microclientes, servicios y flujos de registro y aprobación de pólizas, así como actas de inicio. Se trabajó en generación de PDF, relación con el contrato y soporte de múltiples supervisores.

Las implementaciones históricas de generación de acta de aprobación de póliza y acta de inicio aparecen cerradas en [#318](https://github.com/udistrital/argo_documentacion/issues/318) y [#319](https://github.com/udistrital/argo_documentacion/issues/319). En el ciclo reciente siguen abiertas la consolidación de componentes y las actualizaciones documentales en [#349](https://github.com/udistrital/argo_documentacion/issues/349)–[#353](https://github.com/udistrital/argo_documentacion/issues/353), [#359](https://github.com/udistrital/argo_documentacion/issues/359), [#360](https://github.com/udistrital/argo_documentacion/issues/360) y [#367](https://github.com/udistrital/argo_documentacion/issues/367). Esto evidencia continuidad del trabajo sobre funcionalidades ya abordadas, no una ausencia total de desarrollo.

Evidencias adicionales: [#101](https://github.com/udistrital/argo_documentacion/issues/101), [#102](https://github.com/udistrital/argo_documentacion/issues/102), [#119](https://github.com/udistrital/argo_documentacion/issues/119), [#123](https://github.com/udistrital/argo_documentacion/issues/123), [#179](https://github.com/udistrital/argo_documentacion/issues/179), [#185](https://github.com/udistrital/argo_documentacion/issues/185), [#294](https://github.com/udistrital/argo_documentacion/issues/294) y [#296](https://github.com/udistrital/argo_documentacion/issues/296).

### 4.8. Calidad, despliegue, documentación y gestión

Se registraron pruebas unitarias, funcionales y de integración, revisiones de código, correcciones de CORS, estilos, permisos, selectores y estados. También preparación de ambientes, integración del microfrontend raíz, actualización de dependencias y documentación técnica y operativa.

El proyecto incluye historias de usuario, manual del abogado, diagramas, sesiones de demostración, actas de entregables e informes ejecutivos y de cierre de gestión. La existencia de informes de cierre no implica que el producto completo esté cerrado: el tablero recuperado conserva actividad posterior.

Evidencias: [#71](https://github.com/udistrital/argo_documentacion/issues/71), [#131](https://github.com/udistrital/argo_documentacion/issues/131), [#141](https://github.com/udistrital/argo_documentacion/issues/141), [#161](https://github.com/udistrital/argo_documentacion/issues/161), [#204](https://github.com/udistrital/argo_documentacion/issues/204), [#226](https://github.com/udistrital/argo_documentacion/issues/226), [#267](https://github.com/udistrital/argo_documentacion/issues/267), [#295](https://github.com/udistrital/argo_documentacion/issues/295), [#320](https://github.com/udistrital/argo_documentacion/issues/320), [#329](https://github.com/udistrital/argo_documentacion/issues/329), [#335](https://github.com/udistrital/argo_documentacion/issues/335), [#357](https://github.com/udistrital/argo_documentacion/issues/357) y [#398](https://github.com/udistrital/argo_documentacion/issues/398).

## 5. Lectura de la evolución

1. **2024 — comprensión y construcción de la base:** revisión de ARGO v1, flujos y mockups, arquitectura, datos, formularios, servicios e integraciones. Desarrollo de cláusulas, documentos, aprobaciones, pólizas y actas.
2. **2025 — integración y consolidación:** múltiples supervisores, generación de minutas y actas, scripts y despliegues, consultas por unidad ejecutora, pruebas, instructivos e informes de gestión.
3. **2026 — actualización y nuevo refinamiento:** revisión documental, actualización tecnológica, consolidación de módulos, migración y ajuste del modelo, nuevos requerimientos de usuarios, datos paramétricos, tableros e integración en pruebas. De las 55 issues creadas ese año, 43 siguen abiertas al corte.

Esta lectura es una síntesis de las actividades registradas; no presupone ejecución continua entre fechas ni identifica versiones efectivamente desplegadas.

## 6. Pendientes y prioridades sugeridas

Las siguientes prioridades son una interpretación del análisis, no una priorización oficial extraída del tablero.

| Frente | Pendientes representativos | Resultado que conviene verificar |
|---|---|---|
| Modelo de datos y CRUD | [#356](https://github.com/udistrital/argo_documentacion/issues/356), [#384](https://github.com/udistrital/argo_documentacion/issues/384), [#385](https://github.com/udistrital/argo_documentacion/issues/385), [#389](https://github.com/udistrital/argo_documentacion/issues/389), [#396](https://github.com/udistrital/argo_documentacion/issues/396) | Modelo acordado, migraciones validadas y API coherente con sus consumidores |
| Integración y ambiente de pruebas | [#357](https://github.com/udistrital/argo_documentacion/issues/357), [#388](https://github.com/udistrital/argo_documentacion/issues/388), [#391](https://github.com/udistrital/argo_documentacion/issues/391), [#392](https://github.com/udistrital/argo_documentacion/issues/392), [#397](https://github.com/udistrital/argo_documentacion/issues/397), [#399](https://github.com/udistrital/argo_documentacion/issues/399) | Versión integrada y trazabilidad de despliegue y pruebas |
| Datos paramétricos y presupuesto | [#326](https://github.com/udistrital/argo_documentacion/issues/326), [#377](https://github.com/udistrital/argo_documentacion/issues/377), [#383](https://github.com/udistrital/argo_documentacion/issues/383), [#387](https://github.com/udistrital/argo_documentacion/issues/387) | Catálogos depurados, CDP completo y datos consistentes entre fuentes |
| Consolidación de pólizas y actas | [#349](https://github.com/udistrital/argo_documentacion/issues/349), [#350](https://github.com/udistrital/argo_documentacion/issues/350), [#351](https://github.com/udistrital/argo_documentacion/issues/351), [#352](https://github.com/udistrital/argo_documentacion/issues/352), [#353](https://github.com/udistrital/argo_documentacion/issues/353) | Rutas y consumidores migrados con evidencias de regresión |
| Minutas, actas y transiciones | [#354](https://github.com/udistrital/argo_documentacion/issues/354), [#359](https://github.com/udistrital/argo_documentacion/issues/359), [#360](https://github.com/udistrital/argo_documentacion/issues/360), [#361](https://github.com/udistrital/argo_documentacion/issues/361), [#367](https://github.com/udistrital/argo_documentacion/issues/367), [#373](https://github.com/udistrital/argo_documentacion/issues/373) | PDF correcto y acciones habilitadas conforme al estado y rol |
| Consulta y seguimiento | [#381](https://github.com/udistrital/argo_documentacion/issues/381), [#386](https://github.com/udistrital/argo_documentacion/issues/386), [#362](https://github.com/udistrital/argo_documentacion/issues/362) | Consultas por rol, metadatos y acuerdo de consumo con analítica |
| Arquitectura y mantenimiento | [#347](https://github.com/udistrital/argo_documentacion/issues/347), [#363](https://github.com/udistrital/argo_documentacion/issues/363), [#364](https://github.com/udistrital/argo_documentacion/issues/364), [#365](https://github.com/udistrital/argo_documentacion/issues/365), [#372](https://github.com/udistrital/argo_documentacion/issues/372), [#393](https://github.com/udistrital/argo_documentacion/issues/393) | Dependencias revisadas y convenciones homogéneas entre componentes |
| Alcance por precisar | [#355](https://github.com/udistrital/argo_documentacion/issues/355), [#376](https://github.com/udistrital/argo_documentacion/issues/376) | Validación del alcance precontractual y de la propuesta de huella de navegador |

Una secuencia razonable es alinear primero modelo, parámetros y contratos de API; completar después la integración y migración; y validar finalmente el recorrido contractual completo por unidad ejecutora y rol. Las pruebas antiguas aún abiertas ([#208](https://github.com/udistrital/argo_documentacion/issues/208) a [#213](https://github.com/udistrital/argo_documentacion/issues/213)) requieren conciliación con los ciclos de pruebas posteriores para determinar si conservan alcance pendiente o si corresponde actualizar su seguimiento.

## 7. Hallazgos de seguimiento

- **Cierre y aceptación no son equivalentes.** [#368](https://github.com/udistrital/argo_documentacion/issues/368) y [#370](https://github.com/udistrital/argo_documentacion/issues/370) están cerradas, pero sus descripciones conservan listas de actividades y aceptación sin marcar. [#390](https://github.com/udistrital/argo_documentacion/issues/390) está cerrada con actividades marcadas, aunque conserva puntos de DoD pendientes. Debe contrastarse la evidencia de entrega antes de afirmar finalización integral.
- **Una issue abierta puede contener avances.** [#351](https://github.com/udistrital/argo_documentacion/issues/351) registra subtareas marcadas y aprobación del líder pendiente; [#357](https://github.com/udistrital/argo_documentacion/issues/357) marca despliegue y conectividad, aunque sigue abierta con elementos de DoD sin completar. Las 50 abiertas no equivalen necesariamente a 50 trabajos sin iniciar.
- **El histórico contiene iteraciones sobre los mismos componentes.** Hay implementaciones cerradas seguidas por nuevos ajustes, migraciones y pruebas. Esto describe evolución del alcance y no prueba por sí mismo duplicación de esfuerzo.
- **El enfoque actual se concentra en integración y estabilización.** La issue más reciente, [#399](https://github.com/udistrital/argo_documentacion/issues/399), solicita integrar MID y MF, desplegar el nuevo CRUD, resolver PR pendientes y validar el ambiente de pruebas.
- **No se verificó puesta en producción.** Las evidencias consultadas describen principalmente desarrollo e integración en pruebas. No se confirma aceptación operativa final ni cobertura completa de todos los procesos contractuales.

## 8. Conclusión global

El proyecto ha abordado una transformación funcional y técnica amplia de ARGO: desde el análisis del legado hasta una solución modular que articula contratos, proveedores, presupuesto, cláusulas, aprobaciones, garantías y documentos. Su principal volumen de trabajo está en gestión contractual, con integraciones institucionales y adaptación a Rectoría e IDEXUD como aspectos determinantes.

El estado documental al corte combina una base histórica extensa de actividades cerradas con un conjunto vigente de refinamientos y tareas de estabilización. La prioridad práctica es consolidar la coherencia entre el modelo de datos, los servicios y la interfaz, y respaldar los cierres con pruebas del flujo completo y aceptación verificable.

## Anexo. Inventario trazable de issues consultadas

El inventario permite rastrear los conteos y consultar las fuentes originales. “Cerrada” representa el estado de GitHub, sin inferir despliegue. Se ordena por repositorio y número.

| Issue | Tema | Estado | Hito | Creación |
|---|---|---|---|---|
| [#1](https://github.com/udistrital/argo_documentacion/issues/1) | Revisión documentación Argo v1 - Primera etapa | Cerrada | Exploración Inicial | 2024-04-25 |
| [#2](https://github.com/udistrital/argo_documentacion/issues/2) | Revisión documentación Argo v1 - Primera etapa | Cerrada | Exploración Inicial | 2024-04-25 |
| [#3](https://github.com/udistrital/argo_documentacion/issues/3) | Revisión Lineamientos aplicativos | Cerrada | Exploración Inicial | 2024-04-29 |
| [#4](https://github.com/udistrital/argo_documentacion/issues/4) | Revisión documentación Argo v1 - Segunda etapa | Cerrada | Exploración Inicial | 2024-04-29 |
| [#5](https://github.com/udistrital/argo_documentacion/issues/5) | Revisión documentación Argo v1 - Segunda etapa | Cerrada | Exploración Inicial | 2024-04-29 |
| [#6](https://github.com/udistrital/argo_documentacion/issues/6) | Concertar, desarrollar y levantar acta de sesión exploratoria con cliente | Cerrada | Exploración Inicial | 2024-05-02 |
| [#7](https://github.com/udistrital/argo_documentacion/issues/7) | Construir diagrama de flujo módulo gestión contractual y gestión de pólizas según requerimientos del cliente | Cerrada | Exploración Inicial | 2024-05-02 |
| [#8](https://github.com/udistrital/argo_documentacion/issues/8) | Diseñar el mockup de la vista del modulo contractual | Cerrada | Gestión Contractual | 2024-05-02 |
| [#9](https://github.com/udistrital/argo_documentacion/issues/9) | División del Cliente Argo v1 en Microfrontends - Microcliente Gestión contractual PT1 | Cerrada | Exploración Inicial | 2024-05-03 |
| [#10](https://github.com/udistrital/argo_documentacion/issues/10) | Construir diagrama de flujo módulo gestión compras y gestión novedades según requerimientos del cliente | Cerrada | Exploración Inicial | 2024-05-03 |
| [#11](https://github.com/udistrital/argo_documentacion/issues/11) | Concertar, desarrollar y levantar acta de sesión requerimientos con cliente | Cerrada | Exploración Inicial | 2024-05-03 |
| [#12](https://github.com/udistrital/argo_documentacion/issues/12) | División del Cliente Argo v1 en Microfrontends - Microcliente Gestión de Pólizas PT1 | Cerrada | Exploración Inicial | 2024-05-06 |
| [#13](https://github.com/udistrital/argo_documentacion/issues/13) | División del Cliente Argo v1 en Microfrontends - Microcliente Gestión orden PT1 | Cerrada | Exploración Inicial | 2024-05-06 |
| [#14](https://github.com/udistrital/argo_documentacion/issues/14) | División del Cliente Argo v1 en Microfrontends - Microcliente Gestión actas de inicio PT1 | Cerrada | Exploración Inicial | 2024-05-06 |
| [#15](https://github.com/udistrital/argo_documentacion/issues/15) | División del sistema en Microservicios - Gestión contractual - Gestión orden compras y servicios - Parte 1 | Cerrada | Exploración Inicial | 2024-05-10 |
| [#16](https://github.com/udistrital/argo_documentacion/issues/16) | Actualizar el flujo del modulo contractual según requerimientos cliente | Cerrada | Gestión Contractual | 2024-05-10 |
| [#17](https://github.com/udistrital/argo_documentacion/issues/17) | Diseño modelo de base de datos - Gestión contractual y orden de compras y servicios - parte 1 | Cerrada | Gestión Contractual | 2024-05-14 |
| [#20](https://github.com/udistrital/argo_documentacion/issues/20) | Revisión dependencias de datos del módulo de Gestión Contractual - Dependencia de y sobre ARGO | Cerrada | Gestión Contractual | 2024-05-17 |
| [#21](https://github.com/udistrital/argo_documentacion/issues/21) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2024-05-17 |
| [#22](https://github.com/udistrital/argo_documentacion/issues/22) | Gestionar la actualización del flujo del proceso de vinculación contractual entre OC y OP | Cerrada | Exploración Inicial | 2024-05-17 |
| [#23](https://github.com/udistrital/argo_documentacion/issues/23) | Proyectar y socializar formato de historias de usuario con cliente y equipo | Cerrada | Exploración Inicial | 2024-05-17 |
| [#24](https://github.com/udistrital/argo_documentacion/issues/24) | Revisión dependencias de datos del módulo de Gestión Orden de compras y servicios - Dependencia de y sobre ARGO | Cerrada | Gestión Contractual | 2024-05-20 |
| [#25](https://github.com/udistrital/argo_documentacion/issues/25) | Revisión dependencias de datos del módulo de Gestión Supervisores - Dependencia de y sobre ARGO | Cerrada | Gestión Contractual | 2024-05-20 |
| [#26](https://github.com/udistrital/argo_documentacion/issues/26) | Revisión dependencias de datos del módulo de Gestión Actas de inicio y pólizas - Dependencia de y sobre ARGO | Cerrada | Gestión Contractual | 2024-05-20 |
| [#27](https://github.com/udistrital/argo_documentacion/issues/27) | Revisión dependencias de datos del módulo de Gestión Ordenadores del gasto - Dependencia de y sobre ARGO | Cerrada | Gestión Contractual | 2024-05-20 |
| [#28](https://github.com/udistrital/argo_documentacion/issues/28) | Concertar, desarrollar y levantar acta de sesión requerimientos con cliente | Cerrada | Gestión Contractual | 2024-05-24 |
| [#30](https://github.com/udistrital/argo_documentacion/issues/30) | Culminar el diseño del mockup del submódulo Gestión de contratos | Cerrada | Gestión Contractual | 2024-05-24 |
| [#32](https://github.com/udistrital/argo_documentacion/issues/32) | Diseño modelo de datos de cada módulo de ARGO | Cerrada | Gestión Contractual | 2024-05-27 |
| [#33](https://github.com/udistrital/argo_documentacion/issues/33) | Diseño diagrama de microservicios de ARGO | Cerrada | Gestión Contractual | 2024-05-27 |
| [#34](https://github.com/udistrital/argo_documentacion/issues/34) | Creación microcliente gestión contractual y órdenes de compras y servicios - Parte 1 | Cerrada | Gestión Contractual | 2024-06-04 |
| [#35](https://github.com/udistrital/argo_documentacion/issues/35) | Diseño modelo de datos de cada módulo de ARGO - Revisión parámetros | Cerrada | Gestión Contractual | 2024-06-04 |
| [#36](https://github.com/udistrital/argo_documentacion/issues/36) | Creación microservicio gestión contractual y órdenes de compras y servicios - Parte 1 | Cerrada | Gestión Contractual | 2024-06-04 |
| [#37](https://github.com/udistrital/argo_documentacion/issues/37) | Diseñar submódulos relacionados con acta de aprobación de pólizas | Cerrada | Gestión Contractual | 2024-06-04 |
| [#38](https://github.com/udistrital/argo_documentacion/issues/38) | Creación microcliente gestión contractual y órdenes de compras y servicios - Parte 2 | Cerrada | Gestión Contractual | 2024-06-06 |
| [#39](https://github.com/udistrital/argo_documentacion/issues/39) | Creación microcliente gestión contractual y órdenes de compras y servicios - Parte 3 | Cerrada | Gestión Contractual | 2024-06-06 |
| [#40](https://github.com/udistrital/argo_documentacion/issues/40) | Integración microservicio gestión contractual con microcliente gestión contractual - Paso 1 | Cerrada | Gestión Contractual | 2024-06-06 |
| [#41](https://github.com/udistrital/argo_documentacion/issues/41) | Ajustes modelo de datos de ARGO v2 -Módulos gestión contractual y órdenes, pólizas y amparos | Cerrada | Gestión Contractual | 2024-06-06 |
| [#42](https://github.com/udistrital/argo_documentacion/issues/42) | Se requiere realizar la concertación, desarrollo y levantamiento acta de sesión de refinamiento con cliente | Cerrada | Gestión Contractual | 2024-06-07 |
| [#43](https://github.com/udistrital/argo_documentacion/issues/43) | Revisión estilos para el microcliente gestión contractual y órdenes de compras y servicios | Cerrada | Gestión Contractual | 2024-06-10 |
| [#44](https://github.com/udistrital/argo_documentacion/issues/44) | Ajustes modelo de datos de ARGO v2 -Módulos gestión contractual y órdenes, pólizas y amparos - Parte 2 | Cerrada | Gestión Contractual | 2024-06-11 |
| [#45](https://github.com/udistrital/argo_documentacion/issues/45) | Proyectar un informe técnico ejecutivo del proyecto para el periodo | Cerrada | Informes | 2024-06-12 |
| [#46](https://github.com/udistrital/argo_documentacion/issues/46) | Revisión estilos para el microcliente gestión contractual y órdenes de compras y servicios - Parte 2 | Cerrada | Gestión Contractual | 2024-06-15 |
| [#47](https://github.com/udistrital/argo_documentacion/issues/47) | Pruebas y ajustes de estilos formulario del microcliente gestión contractual y órdenes de compras y servicios | Cerrada | Gestión Contractual | 2024-06-15 |
| [#48](https://github.com/udistrital/argo_documentacion/issues/48) | Continuar con el refinamiento del mockup del modulo de Gestión contractual, relacionado con actualizar contrato, constratos suscritos y contratos por vigencia, acorde a lo indicado en la reunión cliente | Cerrada | Actas de inicio | 2024-06-15 |
| [#49](https://github.com/udistrital/argo_documentacion/issues/49) | Ajustes modelo de datos de ARGO v2 -Módulos gestión contractual y órdenes, pólizas y amparos - Parte 3 | Cerrada | Gestión Contractual | 2024-06-15 |
| [#50](https://github.com/udistrital/argo_documentacion/issues/50) | Diseño modelo de datos ARGO v2 (gestión contractual, acta de inicio, pólizas, amparos, supervisores, ordenadores) con migración ARGO v1 | Cerrada | Gestión Contractual | 2024-06-21 |
| [#51](https://github.com/udistrital/argo_documentacion/issues/51) | Concertar, desarrollar y levantar el acta de sesión de requerimientos y/o refinamiento con el cliente | Cerrada | Gestión Contractual | 2024-06-21 |
| [#52](https://github.com/udistrital/argo_documentacion/issues/52) | Revisión Integración con Sicapital | Cerrada | Gestión Contractual | 2024-06-21 |
| [#53](https://github.com/udistrital/argo_documentacion/issues/53) | Revisión Integración Ágora - Datos contratista | Cerrada | Gestión Contractual | 2024-06-21 |
| [#55](https://github.com/udistrital/argo_documentacion/issues/55) | Revisión plantillas para generación de minutas ARGO actual | Cerrada | Exploración Inicial | 2024-06-21 |
| [#56](https://github.com/udistrital/argo_documentacion/issues/56) | Modelo de datos Cláusulas y Parágrafos ARGO v2 | Cerrada | Gestión Contractual | 2024-06-26 |
| [#57](https://github.com/udistrital/argo_documentacion/issues/57) | Investigación generación de minuta desde la plantilla | Cerrada | Exploración Inicial | 2024-06-26 |
| [#58](https://github.com/udistrital/argo_documentacion/issues/58) | Crear y refinar la parametrización de datos para el sistema Argo | Cerrada | Exploración Inicial | 2024-06-26 |
| [#59](https://github.com/udistrital/argo_documentacion/issues/59) | Actualizar los diagramas de flujo del sistema según novedades y refinamiento de mockups | Cerrada | Exploración Inicial | 2024-06-29 |
| [#60](https://github.com/udistrital/argo_documentacion/issues/60) | Revisión Integración Ágora - Datos contratista - Parte 2 | Cerrada | Gestión Contractual | 2024-07-02 |
| [#61](https://github.com/udistrital/argo_documentacion/issues/61) | Implementación microservicio Ágora MID | Cerrada | Gestión Contractual | 2024-07-02 |
| [#62](https://github.com/udistrital/argo_documentacion/issues/62) | Implementación microservicio Sicapital MID | Cerrada | Gestión Contractual | 2024-07-02 |
| [#63](https://github.com/udistrital/argo_documentacion/issues/63) | Revisión y refinamiento modelo de datos módulo de parámetros | Cerrada | Gestión Contractual | 2024-07-04 |
| [#64](https://github.com/udistrital/argo_documentacion/issues/64) | Diseñar mockup de vista consulta contrato de módulo de gestión contractual | Cerrada | Gestión Contractual | 2024-07-05 |
| [#65](https://github.com/udistrital/argo_documentacion/issues/65) | Pruebas generación de minuta desde la plantilla | Cerrada | Gestión Contractual | 2024-07-05 |
| [#66](https://github.com/udistrital/argo_documentacion/issues/66) | Ajuste modelo de datos core ARGO v2 | Cerrada | Gestión Contractual | 2024-07-05 |
| [#67](https://github.com/udistrital/argo_documentacion/issues/67) | Diseñar mockup de submódulo de actas de inicio del módulo gestión contractual | Cerrada | Gestión Contractual | 2024-07-05 |
| [#68](https://github.com/udistrital/argo_documentacion/issues/68) | Crear script de creación de base de datos microservicio de parametros_crud - registros no transversales | Cerrada | Gestión Contractual | 2024-07-08 |
| [#70](https://github.com/udistrital/argo_documentacion/issues/70) | Implementación microservicio MID ordenadores y supervisores | Cerrada | Gestión Contractual | 2024-07-12 |
| [#71](https://github.com/udistrital/argo_documentacion/issues/71) | Pruebas Unitarias microservicio MID de Sicapital | Cerrada | Gestión Contractual | 2024-07-13 |
| [#72](https://github.com/udistrital/argo_documentacion/issues/72) | Agregar endpoint HealthCheck microservicio  | Cerrada | Gestión Contractual | 2024-07-13 |
| [#73](https://github.com/udistrital/argo_documentacion/issues/73) | Ajustes microservicio MID de Sicapital - Excepciones | Cerrada | Gestión Contractual | 2024-07-13 |
| [#74](https://github.com/udistrital/argo_documentacion/issues/74) | Implementación microservicio Ágora MID - Parte 2 | Cerrada | Gestión Contractual | 2024-07-13 |
| [#75](https://github.com/udistrital/argo_documentacion/issues/75) | Registrar datos paramétricos de ARGO en parametros_crud | Cerrada | Gestión Contractual | 2024-07-13 |
| [#76](https://github.com/udistrital/argo_documentacion/issues/76) | Integración de parametros_crud con el microcliente de gestión contractual - Parte 1 | Cerrada | Gestión Contractual | 2024-07-13 |
| [#77](https://github.com/udistrital/argo_documentacion/issues/77) | Implementación endpoint consulta de número de disponibilidad por vigencia y unidad ejecutora - micromid sicapital | Cerrada | Gestión Contractual | 2024-07-13 |
| [#78](https://github.com/udistrital/argo_documentacion/issues/78) | Ajuste modelo de datos cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-07-13 |
| [#79](https://github.com/udistrital/argo_documentacion/issues/79) | Pruebas de integración microservicio MID de Ágora - Proveedores | Cerrada | Gestión Contractual | 2024-07-22 |
| [#80](https://github.com/udistrital/argo_documentacion/issues/80) | Integración de proveedores MID con el microcliente de gestión contractual. | Cerrada | Gestión Contractual | 2024-07-22 |
| [#81](https://github.com/udistrital/argo_documentacion/issues/81) | Integración de parametros_crud con el microcliente de gestión contractual - Parte 2 | Cerrada | Gestión Contractual | 2024-07-22 |
| [#83](https://github.com/udistrital/argo_documentacion/issues/83) | Revisión modelo de datos CORE gestión contractual | Cerrada | Gestión Contractual | 2024-07-22 |
| [#85](https://github.com/udistrital/argo_documentacion/issues/85) | Concertar, desarrollar y levantar acta de sesión de refinamiento con el cliente para mockup consulta contrato, póliza y acta de inicio | Cerrada | Gestión Contractual | 2024-07-23 |
| [#86](https://github.com/udistrital/argo_documentacion/issues/86) | Concertar, desarrollar y levantar acta de sesión de requerimientos con el cliente Idexud para inclusión en ARGO | Cerrada | Gestión Contractual | 2024-07-23 |
| [#87](https://github.com/udistrital/argo_documentacion/issues/87) | Diseñar mockup de vista consulta póliza de módulo de gestión contractual | Cerrada | Pólizas y amparos | 2024-07-23 |
| [#88](https://github.com/udistrital/argo_documentacion/issues/88) | Reestructuración del Formulario de Registro de Contrato | Cerrada | Gestión Contractual | 2024-07-28 |
| [#89](https://github.com/udistrital/argo_documentacion/issues/89) | Implementación pasos Especificaciones Técnicas y Cláusulas y Parágrafos del Formulario de Registro de Contrato | Cerrada | Gestión Contractual | 2024-07-28 |
| [#90](https://github.com/udistrital/argo_documentacion/issues/90) | Ajustes paso Información de Contrato del Formulario de Registro de Contrato | Cerrada | Gestión Contractual | 2024-07-29 |
| [#91](https://github.com/udistrital/argo_documentacion/issues/91) | Integración de presupuesto contractual MID con el microcliente de gestión contractual | Cerrada | Gestión Contractual | 2024-07-29 |
| [#92](https://github.com/udistrital/argo_documentacion/issues/92) | Integración de proveedores MID con el microcliente de gestión contractual - Parte 2 | Cerrada | Gestión Contractual | 2024-07-29 |
| [#93](https://github.com/udistrital/argo_documentacion/issues/93) | Ajuste modelo de datos de Gestión contractual | Cerrada | Gestión Contractual | 2024-07-29 |
| [#94](https://github.com/udistrital/argo_documentacion/issues/94) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2024-07-29 |
| [#95](https://github.com/udistrital/argo_documentacion/issues/95) | Construir el diseño de las vistas según el rol y el avance del flujo de aprobación Parte 1 | Cerrada | Informes | 2024-07-30 |
| [#96](https://github.com/udistrital/argo_documentacion/issues/96) | Construir Diagrama de flujo general del proceso de contratación del Idexud | Cerrada | Exploración Inicial | 2024-08-02 |
| [#97](https://github.com/udistrital/argo_documentacion/issues/97) | Ajustes endpoint de proveedor mid y presupuesto contractual mid | Cerrada | Gestión Contractual | 2024-08-06 |
| [#98](https://github.com/udistrital/argo_documentacion/issues/98) | Integración parámetros CRUD con información presupuestal - microcliente de gestión contractual  | Cerrada | Gestión Contractual | 2024-08-06 |
| [#99](https://github.com/udistrital/argo_documentacion/issues/99) | Integración parámetros CRUD amparos microcliente de gestión contractual | Cerrada | Gestión Contractual | 2024-08-06 |
| [#100](https://github.com/udistrital/argo_documentacion/issues/100) | Ajuste modelo de datos de Gestión contractual - Parte 2 | Cerrada | Gestión Contractual | 2024-08-08 |
| [#101](https://github.com/udistrital/argo_documentacion/issues/101) | Implementación microcliente gestión de Póliza - Registro | Cerrada | Pólizas y amparos | 2024-08-11 |
| [#102](https://github.com/udistrital/argo_documentacion/issues/102) | Implementación microcliente gestión de Actas de inicio - Registro | Cerrada | Gestión Contractual | 2024-08-11 |
| [#103](https://github.com/udistrital/argo_documentacion/issues/103) | Implementación vista de Consulta de contratos microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-08-11 |
| [#104](https://github.com/udistrital/argo_documentacion/issues/104) | Implementación control de escenarios microcliente de gestión contractual | Cerrada | Gestión Contractual | 2024-08-11 |
| [#105](https://github.com/udistrital/argo_documentacion/issues/105) | Ajuste modelo de datos de pólizas y amparos | Cerrada | Pólizas y amparos | 2024-08-11 |
| [#106](https://github.com/udistrital/argo_documentacion/issues/106) | Concertar, desarrollar y levantar acta de sesión de requerimientos con el cliente Idexud | Cerrada | Gestión Contractual | 2024-08-12 |
| [#107](https://github.com/udistrital/argo_documentacion/issues/107) | Diseñar mockup de vista del flujo de aprobación de submódulo Gestión de pólizas | Cerrada | Pólizas y amparos | 2024-08-12 |
| [#108](https://github.com/udistrital/argo_documentacion/issues/108) | Ajuste modelo de datos cláusulas y parágrafos - Parte 2 | Cerrada | Gestión Contractual | 2024-08-19 |
| [#109](https://github.com/udistrital/argo_documentacion/issues/109) | Presentación modelo de datos cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-08-20 |
| [#110](https://github.com/udistrital/argo_documentacion/issues/110) | Ajuste modelo de datos de pólizas y amparos - Parte 2 | Cerrada | Pólizas y amparos | 2024-08-20 |
| [#111](https://github.com/udistrital/argo_documentacion/issues/111) | Presentación modelo de datos pólizas y amparos | Cerrada | Pólizas y amparos | 2024-08-20 |
| [#112](https://github.com/udistrital/argo_documentacion/issues/112) | Diseño Modelo de datos ordenador | Cerrada | Gestión Contractual | 2024-08-20 |
| [#113](https://github.com/udistrital/argo_documentacion/issues/113) | Continuar con el refinamiento de la parametrización de datos para el sistema Argo | Cerrada | Gestión Contractual | 2024-08-21 |
| [#114](https://github.com/udistrital/argo_documentacion/issues/114) | Investigación serverless para implementación microservicio de pólizas y amparos | Cerrada | Pólizas y amparos | 2024-08-25 |
| [#115](https://github.com/udistrital/argo_documentacion/issues/115) | Ajustes modelo de datos CORE | Cerrada | Gestión Contractual | 2024-08-26 |
| [#116](https://github.com/udistrital/argo_documentacion/issues/116) | Integración información lugar ejecución microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-08-26 |
| [#117](https://github.com/udistrital/argo_documentacion/issues/117) | Revisión flujo ordenador para ARGO v2 | Cerrada | Gestión Contractual | 2024-08-26 |
| [#118](https://github.com/udistrital/argo_documentacion/issues/118) | Revisión microservicios mids ambiente de pruebas | Cerrada | Gestión Contractual | 2024-08-26 |
| [#119](https://github.com/udistrital/argo_documentacion/issues/119) | Implementación microservicio de gestión de pólizas y amparos | Cerrada | Pólizas y amparos | 2024-08-26 |
| [#120](https://github.com/udistrital/argo_documentacion/issues/120) | Diseñar el mockup para el módulo parametrización para ordenadores y supervisores | Cerrada | Gestión Contractual | 2024-08-26 |
| [#121](https://github.com/udistrital/argo_documentacion/issues/121) | Implementación vista de documentos microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-08-29 |
| [#122](https://github.com/udistrital/argo_documentacion/issues/122) | Implementación microservicio de gestión de cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-01 |
| [#123](https://github.com/udistrital/argo_documentacion/issues/123) | Integración microservicio de pólizas y amparos con microclientes de ARGO | Cerrada | Gestión Contractual | 2024-09-02 |
| [#124](https://github.com/udistrital/argo_documentacion/issues/124) | Ajustes Modelo de datos CORE ARGO | Cerrada | Gestión Contractual | 2024-09-02 |
| [#125](https://github.com/udistrital/argo_documentacion/issues/125) | Ajustes microservicio de pólizas | Cerrada | Pólizas y amparos | 2024-09-02 |
| [#126](https://github.com/udistrital/argo_documentacion/issues/126) | Integración microcliente gestión contractual con microservicios de gestión documental y nuxeo. | Cerrada | Gestión Contractual | 2024-09-02 |
| [#127](https://github.com/udistrital/argo_documentacion/issues/127) | Implementación microservicio gestión contractual crud - CORE ARGO | Cerrada | Gestión Contractual | 2024-09-02 |
| [#128](https://github.com/udistrital/argo_documentacion/issues/128) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2024-09-02 |
| [#129](https://github.com/udistrital/argo_documentacion/issues/129) | Concertar, desarrollar y levantar acta de sesión de refinamiento con el cliente | Cerrada | Gestión Contractual | 2024-09-03 |
| [#130](https://github.com/udistrital/argo_documentacion/issues/130) | Definición de permisos en el microcliente de gestión de usuarios | Cerrada | Gestión Contractual | 2024-09-03 |
| [#131](https://github.com/udistrital/argo_documentacion/issues/131) | Implementación pruebas de integración microservicio de gestión de cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-03 |
| [#132](https://github.com/udistrital/argo_documentacion/issues/132) | Implementación pipe para visualización de documentos PDF en microcliente de gestión contractual | Cerrada | Gestión Contractual | 2024-09-05 |
| [#133](https://github.com/udistrital/argo_documentacion/issues/133) | Ajustes microservicio de gestión de cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-09 |
| [#134](https://github.com/udistrital/argo_documentacion/issues/134) | Implementación pruebas de integración microservicio de gestión de cláusulas y parágrafos - parte 2 | Cerrada | Gestión Contractual | 2024-09-09 |
| [#135](https://github.com/udistrital/argo_documentacion/issues/135) | Ajustes modelos de datos CORE gestión contractual | Cerrada | Gestión Contractual | 2024-09-09 |
| [#136](https://github.com/udistrital/argo_documentacion/issues/136) | Diseño Diagrama arquitectura ARGO v2 | Cerrada | Gestión Contractual | 2024-09-09 |
| [#137](https://github.com/udistrital/argo_documentacion/issues/137) | Generación de plantillas para parametrización de contratos según su tipo | Cerrada | Gestión Contractual | 2024-09-09 |
| [#138](https://github.com/udistrital/argo_documentacion/issues/138) | Implementación endpoint de consulta de contratos de un contratista en microservicio Proveedores MID | Cerrada | Gestión Contractual | 2024-09-15 |
| [#139](https://github.com/udistrital/argo_documentacion/issues/139) | Implementación componente TextArea enriquecido para Cláusulas y parágrafos. | Cerrada | Gestión Contractual | 2024-09-15 |
| [#140](https://github.com/udistrital/argo_documentacion/issues/140) | Integración microservicio de cláusulas y parágrafos con microcliente de gestión contractual | Cerrada | Gestión Contractual | 2024-09-15 |
| [#141](https://github.com/udistrital/argo_documentacion/issues/141) | Implementación pruebas microservicio gestión contractual crud - CORE ARGO | Cerrada | Gestión Contractual | 2024-09-15 |
| [#142](https://github.com/udistrital/argo_documentacion/issues/142) | Implementación de datos complementarios endpoints GetOne del microservicio de cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-16 |
| [#143](https://github.com/udistrital/argo_documentacion/issues/143) | Generación de plantillas para parametrización de contratos según su tipo Parte II | Cerrada | Gestión Contractual | 2024-09-17 |
| [#144](https://github.com/udistrital/argo_documentacion/issues/144) | Ajuste mockup paso de cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-17 |
| [#145](https://github.com/udistrital/argo_documentacion/issues/145) | Ajustes flujo y campos de obligaciones en el mockup de registro de contrato | Cerrada | Gestión Contractual | 2024-09-18 |
| [#146](https://github.com/udistrital/argo_documentacion/issues/146) | Actualizar versión  microcliente root y póliza | Cerrada | Gestión Contractual | 2024-09-20 |
| [#147](https://github.com/udistrital/argo_documentacion/issues/147) | Apoyo revisión fallo mf root ambiente de pruebas | Cerrada | Gestión Contractual | 2024-09-20 |
| [#148](https://github.com/udistrital/argo_documentacion/issues/148) | Ajuste referencia contrato general en microservicio CRUD de Cláusulas y Parágrafos | Cerrada | Gestión Contractual | 2024-09-23 |
| [#149](https://github.com/udistrital/argo_documentacion/issues/149) | Ajuste referencia contrato general en microservicio CRUD de Póliza y Amparos | Cerrada | Pólizas y amparos | 2024-09-23 |
| [#150](https://github.com/udistrital/argo_documentacion/issues/150) | Integración microservicio CRUD gestión contractual para la vista de consulta del microcliente | Cerrada | Gestión Contractual | 2024-09-23 |
| [#151](https://github.com/udistrital/argo_documentacion/issues/151) | Integración registro cláusulas por contrato en microcliente gestión contractual y microservicio cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-23 |
| [#152](https://github.com/udistrital/argo_documentacion/issues/152) | Ajuste endpoints consulta de plantilla y contrato en microservicio CRUD cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-23 |
| [#153](https://github.com/udistrital/argo_documentacion/issues/153) | Definición validaciones contratista y CDP | Cerrada | Gestión Contractual | 2024-09-24 |
| [#154](https://github.com/udistrital/argo_documentacion/issues/154) | Actualización mockups de notificación por correo | Cerrada | Gestión Contractual | 2024-09-25 |
| [#155](https://github.com/udistrital/argo_documentacion/issues/155) | Implementación consulta de plantilla y contrato microservicio CRUD cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-29 |
| [#156](https://github.com/udistrital/argo_documentacion/issues/156) | Implementación versionado de plantillas en el microservicio de cláusulas y parágrafos CRUD | Cerrada | Gestión Contractual | 2024-09-29 |
| [#157](https://github.com/udistrital/argo_documentacion/issues/157) | Implementación microservicio gestión contractual MID | Cerrada | Gestión Contractual | 2024-09-29 |
| [#158](https://github.com/udistrital/argo_documentacion/issues/158) | Diseño mensaje del paso de cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-09-29 |
| [#159](https://github.com/udistrital/argo_documentacion/issues/159) | Implementación de validaciones paso de cláusulas y parágrafo en microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-09-29 |
| [#160](https://github.com/udistrital/argo_documentacion/issues/160) | Pruebas funcionales paso cláusulas y parágrafos microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-09-29 |
| [#161](https://github.com/udistrital/argo_documentacion/issues/161) | Code review implementación consulta de cláusulas y páragrafos para plantilla y contratos | Cerrada | Gestión Contractual | 2024-09-29 |
| [#162](https://github.com/udistrital/argo_documentacion/issues/162) | Integración registro cláusulas por contrato en microcliente gestión contractual y microservicio cláusulas y parágrafos - Parte 2 | Cerrada | Gestión Contractual | 2024-09-30 |
| [#163](https://github.com/udistrital/argo_documentacion/issues/163) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2024-09-30 |
| [#164](https://github.com/udistrital/argo_documentacion/issues/164) | Actualización documento de avances ARGO v2 | Cerrada | Gestión Contractual | 2024-10-01 |
| [#165](https://github.com/udistrital/argo_documentacion/issues/165) | Integración registro cláusulas por contrato en microcliente gestión contractual y microservicio cláusulas y parágrafos - Parte 3 | Cerrada | Gestión Contractual | 2024-10-07 |
| [#166](https://github.com/udistrital/argo_documentacion/issues/166) | Revisión de estados permitidos para la validación del contratista al crear un nuevo contrato | Cerrada | Gestión Contractual | 2024-10-08 |
| [#167](https://github.com/udistrital/argo_documentacion/issues/167) | Creación de historias de usuario de Registro de contrato - parte 1 | Cerrada | Informes | 2024-10-08 |
| [#168](https://github.com/udistrital/argo_documentacion/issues/168) | Definición tipos de contrato donde aplica el paso de especificaciones técnicas | Cerrada | Gestión Contractual | 2024-10-08 |
| [#169](https://github.com/udistrital/argo_documentacion/issues/169) | Adición campos de auditoría microservicio de cláusulas y parágrafos | Cerrada | Gestión Contractual | 2024-10-15 |
| [#170](https://github.com/udistrital/argo_documentacion/issues/170) | Registro información presupuestal en microcliente gestión contratos | Cerrada | Gestión Contractual | 2024-10-15 |
| [#171](https://github.com/udistrital/argo_documentacion/issues/171) | Creación de historias de usuario de Registro de contrato - parte 2 | Cerrada | Gestión Contractual | 2024-10-16 |
| [#172](https://github.com/udistrital/argo_documentacion/issues/172) | Ajustes despliegue microcliente gestión contractual ambiente pruebas | Cerrada | Gestión Contractual | 2024-10-17 |
| [#173](https://github.com/udistrital/argo_documentacion/issues/173) | Implementación CRUD cdp microservicio gestión contratual | Cerrada | Gestión Contractual | 2024-10-21 |
| [#174](https://github.com/udistrital/argo_documentacion/issues/174) | Integración CDP y estado contrato microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-10-21 |
| [#175](https://github.com/udistrital/argo_documentacion/issues/175) | Integración cláusula reversión de saldos | Cerrada | Gestión Contractual | 2024-10-21 |
| [#176](https://github.com/udistrital/argo_documentacion/issues/176) | Integración manejo de contratista según tipo de persona microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-10-21 |
| [#177](https://github.com/udistrital/argo_documentacion/issues/177) | Creación de historias de usuario de legalización e inicio de ejecución de contrato | Cerrada | Pólizas y amparos | 2024-10-21 |
| [#178](https://github.com/udistrital/argo_documentacion/issues/178) | Concertar, desarrollar y levantar acta de sesión de muestra de avance del sistema con funcionamiento | Cerrada | Gestión Contractual | 2024-10-22 |
| [#179](https://github.com/udistrital/argo_documentacion/issues/179) | Diseño, implementación módulo acta de inicio | Cerrada | Actas de inicio | 2024-10-23 |
| [#180](https://github.com/udistrital/argo_documentacion/issues/180) | Preparación presentación estado actual ARGO v2 | Cerrada | Gestión Contractual | 2024-10-28 |
| [#181](https://github.com/udistrital/argo_documentacion/issues/181) | Integración endpoint de consulta de contratos proveedor persona natural - Parte 2 | Cerrada | Gestión Contractual | 2024-10-28 |
| [#182](https://github.com/udistrital/argo_documentacion/issues/182) | Ajustes en los microclientes error CORS | Cerrada | Gestión Contractual | 2024-10-28 |
| [#183](https://github.com/udistrital/argo_documentacion/issues/183) | Implementación query params contrato general - microservicio gestion_contractual_crud | Cerrada | Gestión Contractual | 2024-10-28 |
| [#184](https://github.com/udistrital/argo_documentacion/issues/184) | Integración datos contratista con microservicio gestion_contractual_crud | Cerrada | Gestión Contractual | 2024-10-28 |
| [#185](https://github.com/udistrital/argo_documentacion/issues/185) | Integración microservicio con el microcliente - Actas de inicio | Cerrada | Actas de inicio | 2024-10-28 |
| [#186](https://github.com/udistrital/argo_documentacion/issues/186) | Diseño e implementación especificaciones técnicas - microservicio gestion contractual crud | Cerrada | Actas de inicio | 2024-10-28 |
| [#187](https://github.com/udistrital/argo_documentacion/issues/187) | Apoyo presentación estado actual ARGO v2 | Cerrada | Gestión Contractual | 2024-10-28 |
| [#188](https://github.com/udistrital/argo_documentacion/issues/188) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2024-10-28 |
| [#189](https://github.com/udistrital/argo_documentacion/issues/189) | Concertar, desarrollar y levantar acta de sesión de requerimientos con el cliente relacionados con el submódulo de elementos y servicios | Cerrada | Exploración Inicial | 2024-10-28 |
| [#191](https://github.com/udistrital/argo_documentacion/issues/191) | Implementación metadata para consulta de contratos en microservicio CRUD | Cerrada | Gestión Contractual | 2024-11-04 |
| [#192](https://github.com/udistrital/argo_documentacion/issues/192) | Implementación manejo de pasos según criterio - ocultar/mostrar paso - microcliente gestión contractual mf | Cerrada | Gestión Contractual | 2024-11-04 |
| [#193](https://github.com/udistrital/argo_documentacion/issues/193) | Implementar campo de no edición de cláusulas y parágrafos - microservicio cláusulas CRUD | Cerrada | Gestión Contractual | 2024-11-04 |
| [#194](https://github.com/udistrital/argo_documentacion/issues/194) | Integración OIKOS paso Información Solicitante y Supervisor - microcliente gestión contractual MF | Cerrada | Gestión Contractual | 2024-11-04 |
| [#195](https://github.com/udistrital/argo_documentacion/issues/195) | Implementación endpoints consulta ordenador y supervisor microservicio MID | Cerrada | Gestión Contractual | 2024-11-05 |
| [#196](https://github.com/udistrital/argo_documentacion/issues/196) | Implementación cláusula aplica póliza - microservicio cláusulas CRUD | Cerrada | Gestión Contractual | 2024-11-05 |
| [#197](https://github.com/udistrital/argo_documentacion/issues/197) | Gestionar la actualización de procedimientos y flujos ante el SIGUD | Cerrada | Gestión Contractual | 2024-11-05 |
| [#198](https://github.com/udistrital/argo_documentacion/issues/198) | Implementación registro de ordenador en el microservicio crud | Cerrada | Gestión Contractual | 2024-11-08 |
| [#199](https://github.com/udistrital/argo_documentacion/issues/199) | Ajustes de estilos e integración paso de garantías | Cerrada | Gestión Contractual | 2024-11-08 |
| [#200](https://github.com/udistrital/argo_documentacion/issues/200) | Integración cláusulas con información del contrato - microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-11-08 |
| [#201](https://github.com/udistrital/argo_documentacion/issues/201) | Implementación manejo de roles vista de registro de contrato y consulta | Cerrada | Gestión Contractual | 2024-11-08 |
| [#202](https://github.com/udistrital/argo_documentacion/issues/202) | Integración especificaciones técnicas con microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-11-08 |
| [#204](https://github.com/udistrital/argo_documentacion/issues/204) | Gestionar manual o instructivo de operación del sistema para rol de abogado | Cerrada | Gestión Contractual | 2024-11-08 |
| [#205](https://github.com/udistrital/argo_documentacion/issues/205) | Mockup vista contratrista | Cerrada | Gestión Contractual | 2024-11-08 |
| [#206](https://github.com/udistrital/argo_documentacion/issues/206) | Fecha de suscripción modificable, revisar con el usuario ARGO V2 | Cerrada | Gestión Contractual | 2024-11-08 |
| [#207](https://github.com/udistrital/argo_documentacion/issues/207) | Revisión estilos módulo de registro de contrato ambiente pruebas | Cerrada | Gestión Contractual | 2024-11-08 |
| [#208](https://github.com/udistrital/argo_documentacion/issues/208) | Revisión pruebas funcionales ambiente de pruebas módulo de registro de contrato | Abierta | Sin hito | 2024-11-08 |
| [#209](https://github.com/udistrital/argo_documentacion/issues/209) | Revisión pruebas funcionales ambiente de pruebas módulo de consulta | Abierta | Sin hito | 2024-11-08 |
| [#210](https://github.com/udistrital/argo_documentacion/issues/210) | Revisión pruebas funcionales ambiente de pruebas módulo de revisión ordenador | Abierta | Sin hito | 2024-11-08 |
| [#211](https://github.com/udistrital/argo_documentacion/issues/211) | Revisión pruebas funcionales ambiente de pruebas módulo de revisión jefe oficina | Abierta | Sin hito | 2024-11-08 |
| [#212](https://github.com/udistrital/argo_documentacion/issues/212) | Revisión pruebas funcionales ambiente de pruebas módulo de acta de inicio | Abierta | Sin hito | 2024-11-08 |
| [#213](https://github.com/udistrital/argo_documentacion/issues/213) | Revisión pruebas funcionales ambiente de pruebas módulo de pólizas | Abierta | Sin hito | 2024-11-08 |
| [#214](https://github.com/udistrital/argo_documentacion/issues/214) | Revisión y creación de plantillas minutas Idexud - Parte 1 | Cerrada | Gestión Contractual | 2024-11-08 |
| [#216](https://github.com/udistrital/argo_documentacion/issues/216) | Documentación módulo de registro de contratos | Cerrada | Gestión Contractual | 2024-11-11 |
| [#217](https://github.com/udistrital/argo_documentacion/issues/217) | Manejo de datos complementarios en paso de cláusulas y generación de minuta  | Cerrada | Gestión Contractual | 2024-11-12 |
| [#218](https://github.com/udistrital/argo_documentacion/issues/218) | Creación plantillas HTML minuta de contratos e integración con microcliente | Cerrada | Gestión Contractual | 2024-11-12 |
| [#219](https://github.com/udistrital/argo_documentacion/issues/219) | Inducción integrante nuevo sobre ARGO v2 | Cerrada | Gestión Contractual | 2024-11-12 |
| [#220](https://github.com/udistrital/argo_documentacion/issues/220) | Preparación presentación estado de desarrollo ARGO v2 al usuario final | Cerrada | Gestión Contractual | 2024-11-12 |
| [#224](https://github.com/udistrital/argo_documentacion/issues/224) | Implementación reemplazo de variables en las cláusulas | Cerrada | Gestión Contractual | 2024-11-18 |
| [#225](https://github.com/udistrital/argo_documentacion/issues/225) | Integración microservicio CRUD gestión contractual para la vista de consulta del microcliente - Parte 2 | Cerrada | Gestión Contractual | 2024-11-18 |
| [#226](https://github.com/udistrital/argo_documentacion/issues/226) | Preparación despliegue microservicios CORE ARGO | Cerrada | Gestión Contractual | 2024-11-18 |
| [#227](https://github.com/udistrital/argo_documentacion/issues/227) | Maquetación vista de aprobación jefe contratación | Cerrada | Gestión Contractual | 2024-11-18 |
| [#228](https://github.com/udistrital/argo_documentacion/issues/228) | Maquetación vista de aprobación ordenador | Cerrada | Gestión Contractual | 2024-11-18 |
| [#229](https://github.com/udistrital/argo_documentacion/issues/229) | Ajuste diseño mockup especificaciones técnicas y minuta | Cerrada | Gestión Contractual | 2024-11-18 |
| [#230](https://github.com/udistrital/argo_documentacion/issues/230) | Construir diagrama modular y de procesos del sistema | Cerrada | Gestión Contractual | 2024-11-18 |
| [#231](https://github.com/udistrital/argo_documentacion/issues/231) | Revisión y creación de plantillas minutas Idexud - Parte 2 | Cerrada | Gestión Contractual | 2024-11-19 |
| [#232](https://github.com/udistrital/argo_documentacion/issues/232) | Apoyo revisión microcliente root - Despliegue | Cerrada | Soporte y arquitectura general | 2024-11-25 |
| [#233](https://github.com/udistrital/argo_documentacion/issues/233) | Implementación integración pasos de registro con el id del contrato | Cerrada | Gestión Contractual | 2024-11-25 |
| [#234](https://github.com/udistrital/argo_documentacion/issues/234) | Integración vista de consulta contrato | Cerrada | Gestión Contractual | 2024-11-25 |
| [#235](https://github.com/udistrital/argo_documentacion/issues/235) | Integración gestor documental para almacenamiento de minuta | Cerrada | Gestión Contractual | 2024-11-25 |
| [#236](https://github.com/udistrital/argo_documentacion/issues/236) | Pruebas endpoint de consulta con filtro de contratista y estado | Cerrada | Gestión Contractual | 2024-11-25 |
| [#237](https://github.com/udistrital/argo_documentacion/issues/237) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2024-11-25 |
| [#238](https://github.com/udistrital/argo_documentacion/issues/238) | Integración especificaciones técnicas y microservicio crud | Cerrada | Gestión Contractual | 2024-11-26 |
| [#239](https://github.com/udistrital/argo_documentacion/issues/239) | Preparación presentación estado actual desarrollo ARGO | Cerrada | Gestión Contractual | 2024-12-02 |
| [#240](https://github.com/udistrital/argo_documentacion/issues/240) | Presentación ARGO v2 al usuario | Cerrada | Gestión Contractual | 2024-12-02 |
| [#241](https://github.com/udistrital/argo_documentacion/issues/241) | Apoyo preparación presentación ARGO v2 al usuario | Cerrada | Gestión Contractual | 2024-12-02 |
| [#242](https://github.com/udistrital/argo_documentacion/issues/242) | Implementación estados internos microservicio gestion_contractual_crud | Cerrada | Gestión Contractual | 2024-12-02 |
| [#243](https://github.com/udistrital/argo_documentacion/issues/243) | Implementación de acciones según rol y estado del contrato | Cerrada | Gestión Contractual | 2024-12-02 |
| [#244](https://github.com/udistrital/argo_documentacion/issues/244) | Integración visualización de minuta en vistas de aprobación | Cerrada | Gestión Contractual | 2024-12-02 |
| [#245](https://github.com/udistrital/argo_documentacion/issues/245) | Implementación vista de histórico de observaciones abogado - parte 1 | Cerrada | Gestión Contractual | 2024-12-02 |
| [#246](https://github.com/udistrital/argo_documentacion/issues/246) | Implementación consulta de contrato por fecha de registro | Cerrada | Gestión Contractual | 2024-12-02 |
| [#247](https://github.com/udistrital/argo_documentacion/issues/247) | Implementación endpoint de consulta de estados en microservicio mid | Cerrada | Gestión Contractual | 2024-12-02 |
| [#248](https://github.com/udistrital/argo_documentacion/issues/248) | Concertar, desarrollar y levantarl acta de sesión de muestra con el cliente | Cerrada | Gestión Contractual | 2024-12-02 |
| [#249](https://github.com/udistrital/argo_documentacion/issues/249) | Implementación vista de histórico de observaciones abogado - parte 2 | Cerrada | Gestión Contractual | 2024-12-09 |
| [#250](https://github.com/udistrital/argo_documentacion/issues/250) | Implementación de acciones según estado del contrato | Cerrada | Gestión Contractual | 2024-12-09 |
| [#251](https://github.com/udistrital/argo_documentacion/issues/251) | Ajuste errores y Pruebas endpoint de consulta de estados en microservicio mid | Cerrada | Gestión Contractual | 2024-12-09 |
| [#252](https://github.com/udistrital/argo_documentacion/issues/252) | Implementación búsqueda en selectores por número en el submódulo de registro de contratos | Cerrada | Gestión Contractual | 2024-12-09 |
| [#253](https://github.com/udistrital/argo_documentacion/issues/253) | Implementación e integración consulta y asignación de ordenador en el registro de contrato | Cerrada | Gestión Contractual | 2024-12-09 |
| [#254](https://github.com/udistrital/argo_documentacion/issues/254) | Ajuste modelo de datos tabla supervisor | Cerrada | Gestión Contractual | 2024-12-09 |
| [#255](https://github.com/udistrital/argo_documentacion/issues/255) | Revisión y ajuste de la documentación ténica del sistema | Cerrada | Gestión Contractual | 2024-12-09 |
| [#256](https://github.com/udistrital/argo_documentacion/issues/256) | Actualizar los mockups del sistema según comentarios del cliente | Cerrada | Gestión Contractual | 2024-12-09 |
| [#257](https://github.com/udistrital/argo_documentacion/issues/257) | Actualización matriz de roles y permisos y flujo de estados internos | Cerrada | Gestión Contractual | 2024-12-10 |
| [#259](https://github.com/udistrital/argo_documentacion/issues/259) | Ajuste modelo de datos supervisor sede y dependencia OIKOS actual | Cerrada | Gestión Contractual | 2024-12-16 |
| [#260](https://github.com/udistrital/argo_documentacion/issues/260) | Ajustes endpoint de ordenadores | Cerrada | Gestión Contractual | 2024-12-16 |
| [#261](https://github.com/udistrital/argo_documentacion/issues/261) | Ajuste selectores en el submódulo de registro de contrato | Cerrada | Gestión Contractual | 2024-12-16 |
| [#262](https://github.com/udistrital/argo_documentacion/issues/262) | Actualización roles y estado de finalización de firmantes | Cerrada | Gestión Contractual | 2024-12-16 |
| [#263](https://github.com/udistrital/argo_documentacion/issues/263) | Apoyo ajustes de estilos microcliente gestión contractual crud | Cerrada | Gestión Contractual | 2024-12-16 |
| [#264](https://github.com/udistrital/argo_documentacion/issues/264) | Actualización estilos en ARGO v2 basado en los ajustes realizados en Sísifo v2 | Cerrada | Gestión Contractual | 2024-12-16 |
| [#265](https://github.com/udistrital/argo_documentacion/issues/265) | Actualización documento de avances de Argo v2 | Cerrada | Informes | 2024-12-17 |
| [#267](https://github.com/udistrital/argo_documentacion/issues/267) | Construir acta de entregable para el primer alcance del sistema Argo V2 | Cerrada | Gestión Contractual | 2024-12-17 |
| [#268](https://github.com/udistrital/argo_documentacion/issues/268) | Implementación flujo de aprobación por unidad ejecutora | Cerrada | Gestión Contractual | 2024-12-18 |
| [#269](https://github.com/udistrital/argo_documentacion/issues/269) | Apoyo validación integración de ordenadores con el microcliente | Cerrada | Gestión Contractual | 2024-12-19 |
| [#270](https://github.com/udistrital/argo_documentacion/issues/270) | Actualización estilos en ARGO v2 basado en los ajustes realizados en Sísifo v2 - Póliza MF | Cerrada | Pólizas y amparos | 2024-12-21 |
| [#271](https://github.com/udistrital/argo_documentacion/issues/271) | Actualización estilos en ARGO v2 basado en los ajustes realizados en Sísifo v2 - Acta Inicio MF | Cerrada | Actas de inicio | 2024-12-23 |
| [#272](https://github.com/udistrital/argo_documentacion/issues/272) | Documentación submódulo de cláusulas | Cerrada | Gestión Contractual | 2024-12-23 |
| [#273](https://github.com/udistrital/argo_documentacion/issues/273) | Documentación técnica roles y permisos | Cerrada | Gestión Contractual | 2024-12-23 |
| [#274](https://github.com/udistrital/argo_documentacion/issues/274) | Implementación unidad ejecutora registro de contrato | Cerrada | Gestión Contractual | 2024-12-23 |
| [#275](https://github.com/udistrital/argo_documentacion/issues/275) | Implementación consulta de supervisor - parte 1 | Cerrada | Gestión Contractual | 2024-12-23 |
| [#276](https://github.com/udistrital/argo_documentacion/issues/276) | Ajustes cambio de estado contrato | Cerrada | Gestión Contractual | 2024-12-23 |
| [#277](https://github.com/udistrital/argo_documentacion/issues/277) | Integración cargue masivo especificaciones técnicas | Cerrada | Gestión Contractual | 2024-12-23 |
| [#278](https://github.com/udistrital/argo_documentacion/issues/278) | Implementación firma con cargue de documento | Cerrada | Gestión Contractual | 2024-12-23 |
| [#280](https://github.com/udistrital/argo_documentacion/issues/280) | Revisión estilos y parámetros del ambiente de pruebas | Cerrada | Gestión Contractual | 2024-12-23 |
| [#281](https://github.com/udistrital/argo_documentacion/issues/281) | Revisión documentación técnica módulo consulta y registro de contratos teniendo presente flujo IDEXUD y Contratación | Cerrada | Gestión Contractual | 2024-12-23 |
| [#282](https://github.com/udistrital/argo_documentacion/issues/282) | Implementación consulta de supervisor - parte 2 | Cerrada | Gestión Contractual | 2024-12-27 |
| [#283](https://github.com/udistrital/argo_documentacion/issues/283) | Implementación spinner e interceptor microcliente gestión contractual | Cerrada | Gestión Contractual | 2024-12-28 |
| [#284](https://github.com/udistrital/argo_documentacion/issues/284) | Integración cargue masivo especificaciones técnicas - Parte 2 | Cerrada | Gestión Contractual | 2024-12-28 |
| [#285](https://github.com/udistrital/argo_documentacion/issues/285) | Implementación endpoints de renderizado minuta para ARGO | Cerrada | Gestión Contractual | 2024-12-29 |
| [#286](https://github.com/udistrital/argo_documentacion/issues/286) | Ajuste peticiones de registro de formularios | Cerrada | Gestión Contractual | 2024-12-30 |
| [#287](https://github.com/udistrital/argo_documentacion/issues/287) | Integración unidad ejecutora y ajustes en vista de consulta | Cerrada | Gestión Contractual | 2024-12-30 |
| [#288](https://github.com/udistrital/argo_documentacion/issues/288) | Complementar información de ordenadores y supervisores en el microservicio gestion_contractual_mid | Cerrada | Gestión Contractual | 2024-12-30 |
| [#289](https://github.com/udistrital/argo_documentacion/issues/289) | Integración tercero en ordenadores y supervisores | Cerrada | Gestión Contractual | 2024-12-30 |
| [#290](https://github.com/udistrital/argo_documentacion/issues/290) | Integración endpoints de renderizado de minuta | Cerrada | Gestión Contractual | 2024-12-30 |
| [#291](https://github.com/udistrital/argo_documentacion/issues/291) | Implementación y organización datos para generación de minuta según tipo de contrato | Cerrada | Gestión Contractual | 2024-12-30 |
| [#292](https://github.com/udistrital/argo_documentacion/issues/292) | Integración tipo de persona en la información consultada del proveedor | Cerrada | Gestión Contractual | 2024-12-30 |
| [#293](https://github.com/udistrital/argo_documentacion/issues/293) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2024-12-30 |
| [#294](https://github.com/udistrital/argo_documentacion/issues/294) | Implementación múltiple supervisor | Cerrada | Gestión Contractual | 2025-01-07 |
| [#295](https://github.com/udistrital/argo_documentacion/issues/295) | Pruebas funcionales locales al submódulo de registro de contrato | Cerrada | Gestión Contractual | 2025-01-07 |
| [#296](https://github.com/udistrital/argo_documentacion/issues/296) | Integración submódulo de registro de acta de aprobación de póliza | Cerrada | Pólizas y amparos | 2025-01-07 |
| [#297](https://github.com/udistrital/argo_documentacion/issues/297) | Gestionar manual o instructivo de operación del sistema para rol de abogado parte 2 | Cerrada | Gestión Contractual | 2025-01-07 |
| [#299](https://github.com/udistrital/argo_documentacion/issues/299) | Migración microservicio pólizas CRUD | Cerrada | Pólizas y amparos | 2025-01-09 |
| [#300](https://github.com/udistrital/argo_documentacion/issues/300) | Investigación de información para la creación documento informe de cierre de proyecto | Cerrada | Informes | 2025-01-09 |
| [#301](https://github.com/udistrital/argo_documentacion/issues/301) | Alimentar el instrumento de seguimiento al proyecto según los lineamientos | Cerrada | Informes | 2025-01-10 |
| [#302](https://github.com/udistrital/argo_documentacion/issues/302) | Creación microservicio minuta contractual mid | Cerrada | Gestión Contractual | 2025-01-10 |
| [#303](https://github.com/udistrital/argo_documentacion/issues/303) | Implementación unidad ejecutora en las cláusulas | Cerrada | Gestión Contractual | 2025-01-12 |
| [#304](https://github.com/udistrital/argo_documentacion/issues/304) | Actualización matriz de roles agregando rol auditoría | Cerrada | Gestión Contractual | 2025-01-12 |
| [#305](https://github.com/udistrital/argo_documentacion/issues/305) | Gestionar manual o instructivo de operación del sistema para rol de abogado parte 3 | Cerrada | Gestión Contractual | 2025-01-12 |
| [#306](https://github.com/udistrital/argo_documentacion/issues/306) | Apoyo documentación del instructivo del rol abogado | Cerrada | Gestión Contractual | 2025-01-12 |
| [#307](https://github.com/udistrital/argo_documentacion/issues/307) | Implementación endpoint de generación de minuta por contrato_general_id | Cerrada | Gestión Contractual | 2025-01-12 |
| [#308](https://github.com/udistrital/argo_documentacion/issues/308) | Documentación técnica módulo de pólizas | Cerrada | Pólizas y amparos | 2025-01-12 |
| [#309](https://github.com/udistrital/argo_documentacion/issues/309) | Documentación técnica módulo de acta de inicio | Cerrada | Actas de inicio | 2025-01-12 |
| [#310](https://github.com/udistrital/argo_documentacion/issues/310) | Implementación endpoint de consulta de ordenador | Cerrada | Gestión Contractual | 2025-01-12 |
| [#311](https://github.com/udistrital/argo_documentacion/issues/311) | Ajustes errores roles y texto enriquecido | Cerrada | Gestión Contractual | 2025-01-13 |
| [#312](https://github.com/udistrital/argo_documentacion/issues/312) | Documentación pruebas funcionales roles módulo consulta y registro | Cerrada | Gestión Contractual | 2025-01-13 |
| [#313](https://github.com/udistrital/argo_documentacion/issues/313) | Actualización scripts de creación de base de datos de ARGO | Cerrada | Gestión Contractual | 2025-01-15 |
| [#314](https://github.com/udistrital/argo_documentacion/issues/314) | Ajuste para despliegue del microservicio gestión contractual CRUD y validación | Cerrada | Gestión Contractual | 2025-01-20 |
| [#315](https://github.com/udistrital/argo_documentacion/issues/315) | Integración flujo de aprobación con soporte de firma manual de minuta | Cerrada | Gestión Contractual | 2025-01-20 |
| [#316](https://github.com/udistrital/argo_documentacion/issues/316) | Ajustes y validación microservicio ordenador_supervisor_mid en ambiente de pruebas | Cerrada | Gestión Contractual | 2025-01-20 |
| [#317](https://github.com/udistrital/argo_documentacion/issues/317) | Implementación endpoint de consulta completa de información en gestión contractual MID | Cerrada | Gestión Contractual | 2025-01-20 |
| [#318](https://github.com/udistrital/argo_documentacion/issues/318) | Implementación generación de acta de aprobación de Póliza PDF | Cerrada | Pólizas y amparos | 2025-01-20 |
| [#319](https://github.com/udistrital/argo_documentacion/issues/319) | Implementación generación de acta de Inicio PDF | Cerrada | Actas de inicio | 2025-01-20 |
| [#320](https://github.com/udistrital/argo_documentacion/issues/320) | Construir el informe de cierre de gestión del proyecto | Cerrada | Informes | 2025-01-21 |
| [#321](https://github.com/udistrital/argo_documentacion/issues/321) | Ajuste para despliegue del microservicio minuta mid y validación | Cerrada | Gestión Contractual | 2025-01-23 |
| [#322](https://github.com/udistrital/argo_documentacion/issues/322) | Estabilización e integración microservicios con microcliente en ambiente de pruebas | Cerrada | Gestión Contractual | 2025-01-27 |
| [#323](https://github.com/udistrital/argo_documentacion/issues/323) | Registro de tipologías específicas | Cerrada | Gestión Contractual | 2025-01-27 |
| [#324](https://github.com/udistrital/argo_documentacion/issues/324) | Implementación descarga de plantilla de especificaciones técnicas | Cerrada | Gestión Contractual | 2025-01-27 |
| [#325](https://github.com/udistrital/argo_documentacion/issues/325) | Generar consecutivo y número de contrato | Cerrada | Gestión Contractual | 2025-01-27 |
| [#326](https://github.com/udistrital/argo_documentacion/issues/326) | Integración y ajustes información del CDP - actividades y objeto | Abierta | Gestión Contractual | 2025-01-27 |
| [#327](https://github.com/udistrital/argo_documentacion/issues/327) | Estabilización y validación submódulo de consulta | Cerrada | Gestión Contractual | 2025-01-27 |
| [#328](https://github.com/udistrital/argo_documentacion/issues/328) | Implementación e integración consulta por unidad ejecutora - submódulo de consulta de contratos | Cerrada | Gestión Contractual | 2025-01-27 |
| [#329](https://github.com/udistrital/argo_documentacion/issues/329) | Construir el informe de cierre de gestión del proyecto. Parte II. | Cerrada | Informes | 2025-01-27 |
| [#330](https://github.com/udistrital/argo_documentacion/issues/330) | Apoyo construcción del informe de cierre del proyecto | Cerrada | Gestión Contractual | 2025-01-29 |
| [#331](https://github.com/udistrital/argo_documentacion/issues/331) | Documentación registro cláusulas - División de grupos de cláusulas según criterios del contrato | Cerrada | Gestión Contractual | 2025-01-31 |
| [#332](https://github.com/udistrital/argo_documentacion/issues/332) | Estabilización e integración microservicios con microcliente en ambiente de pruebas - Parte 2 | Cerrada | Gestión Contractual | 2025-02-03 |
| [#333](https://github.com/udistrital/argo_documentacion/issues/333) | Implementación e integración consulta por unidad ejecutora - submódulo de consulta de contratos - Parte 2 | Cerrada | Gestión Contractual | 2025-02-03 |
| [#334](https://github.com/udistrital/argo_documentacion/issues/334) | Documentación técnica servicios de renderizado | Cerrada | Gestión Contractual | 2025-02-03 |
| [#335](https://github.com/udistrital/argo_documentacion/issues/335) | Documentación técnica generación de minuta | Cerrada | Gestión Contractual | 2025-02-03 |
| [#336](https://github.com/udistrital/argo_documentacion/issues/336) | Pruebas funcionales cláusulas ambiente de pruebas | Cerrada | Gestión Contractual | 2025-02-03 |
| [#337](https://github.com/udistrital/argo_documentacion/issues/337) | Pruebas funcionales e integración generación de minuta | Cerrada | Gestión Contractual | 2025-02-03 |
| [#338](https://github.com/udistrital/argo_documentacion/issues/338) | Proyectar un informe técnico ejecutivo sobre cada línea de acción del proyecto | Cerrada | Informes | 2025-02-04 |
| [#339](https://github.com/udistrital/argo_documentacion/issues/339) | Revisión documentación Argo v1 - V2 | Abierta | Exploración Inicial | 2026-09-11 |
| [#340](https://github.com/udistrital/argo_documentacion/issues/340) | Revisión documentación Argo v1 - V2 | Abierta | Exploración Inicial | 2026-09-11 |
| [#341](https://github.com/udistrital/argo_documentacion/issues/341) | Revisión documentación Argo v1 - V2 | Abierta | Exploración Inicial | 2026-09-11 |
| [#342](https://github.com/udistrital/argo_documentacion/issues/342) | Revisión documentación Argo v1 - V2 | Abierta | Exploración Inicial | 2026-09-11 |
| [#343](https://github.com/udistrital/argo_documentacion/issues/343) | Revisión documentación Argo v1 - V2 | Abierta | Exploración Inicial | 2026-09-11 |
| [#344](https://github.com/udistrital/argo_documentacion/issues/344) | Actualización gestion_contractual_root_mf angular | Cerrada | Gestión Contractual | 2026-09-11 |
| [#345](https://github.com/udistrital/argo_documentacion/issues/345) | Actualización gestion_contractual_mf angular | Cerrada | Gestión Contractual | 2026-09-11 |
| [#346](https://github.com/udistrital/argo_documentacion/issues/346) | Implementación ajustes dependabot ms gestion_contractual_mid | Cerrada | Gestión Contractual | 2026-09-11 |
| [#347](https://github.com/udistrital/argo_documentacion/issues/347) | Implementación ajustes dependabot ms  gestion_contractual_crud | Abierta | Gestión Contractual | 2026-09-11 |
| [#348](https://github.com/udistrital/argo_documentacion/issues/348) | Implementación ajustes dependabot ms minuta_contractual_mid | Cerrada | Gestión Contractual | 2026-09-11 |
| [#349](https://github.com/udistrital/argo_documentacion/issues/349) | Migración póliza mf a gestion_contractual_mf | Abierta | Pólizas y amparos | 2026-09-18 |
| [#350](https://github.com/udistrital/argo_documentacion/issues/350) | Migración póliza mid a gestion_contractual_mid | Abierta | Pólizas y amparos | 2026-09-18 |
| [#351](https://github.com/udistrital/argo_documentacion/issues/351) | Migración póliza crud a gestion_contractual_crud | Abierta | Pólizas y amparos | 2026-09-18 |
| [#352](https://github.com/udistrital/argo_documentacion/issues/352) | Integración migración póliza | Abierta | Pólizas y amparos | 2026-09-18 |
| [#353](https://github.com/udistrital/argo_documentacion/issues/353) | Migración acta de inicio mf a gestion_contractual_mf | Abierta | Actas de inicio | 2026-09-18 |
| [#354](https://github.com/udistrital/argo_documentacion/issues/354) | Evaluación y ajuste renderizado de minutas | Abierta | Gestión Contractual | 2026-09-18 |
| [#355](https://github.com/udistrital/argo_documentacion/issues/355) | Investigar y analizar el proceso precontractual para su implementación en ARGO V2 | Abierta | Exploración Inicial | 2026-09-18 |
| [#356](https://github.com/udistrital/argo_documentacion/issues/356) | Análisis comparativo modelo de datos | Abierta | Gestión Contractual | 2026-09-28 |
| [#357](https://github.com/udistrital/argo_documentacion/issues/357) | Estabilización y despliegues ambiente de pruebas ARGO v2 | Abierta | Gestión Contractual | 2026-09-28 |
| [#359](https://github.com/udistrital/argo_documentacion/issues/359) | Actualización e integración generación de acta de inicio | Abierta | Actas de inicio | 2026-09-30 |
| [#360](https://github.com/udistrital/argo_documentacion/issues/360) | Actualización e integración generación de acta de aprobación de póliza | Abierta | Pólizas y amparos | 2026-09-30 |
| [#361](https://github.com/udistrital/argo_documentacion/issues/361) | Pruebas funcionales y estabilización del registro de contrato incluyendo los pasos de registro de información y minuta en pdf | Abierta | Gestión Contractual | 2026-09-30 |
| [#362](https://github.com/udistrital/argo_documentacion/issues/362) | Reunión revisión requerimientos ARGO integración de requerimientos con equipo de analitica | Abierta | Gestión Contractual | 2026-10-02 |
| [#363](https://github.com/udistrital/argo_documentacion/issues/363) | Implementación y actualización de dependencias y alertas dependabot - proveedores_mid | Abierta | Gestión Contractual | 2026-10-02 |
| [#364](https://github.com/udistrital/argo_documentacion/issues/364) | Implementación y actualización de dependencias y alertas dependabot - clausulas_paragrafos_crud | Abierta | Gestión Contractual | 2026-10-02 |
| [#365](https://github.com/udistrital/argo_documentacion/issues/365) | Implementación y actualización de dependencias y alertas dependabot - ordenador_supervisor_mid | Abierta | Gestión Contractual | 2026-10-02 |
| [#366](https://github.com/udistrital/argo_documentacion/issues/366) | Integración y estabilización vista de consulta y flujo de aprobación del contrato | Cerrada | Gestión Contractual | 2026-10-02 |
| [#367](https://github.com/udistrital/argo_documentacion/issues/367) | Integración y estabilización de aprobación de póliza y generación de minuta basado en los estados del contrato | Abierta | Pólizas y amparos | 2026-10-02 |
| [#368](https://github.com/udistrital/argo_documentacion/issues/368) | Actualización de modelo de datos requerimientos equipo de arquitectura | Cerrada | Gestión Contractual | 2026-10-02 |
| [#369](https://github.com/udistrital/argo_documentacion/issues/369) | Integración y pruebas ms mid y mf con microcliente crud migrado | Cerrada | Gestión Contractual | 2026-10-02 |
| [#370](https://github.com/udistrital/argo_documentacion/issues/370) | Implementación control de acceso a contratos por unidad ejecutora | Cerrada | Gestión Contractual | 2026-10-02 |
| [#371](https://github.com/udistrital/argo_documentacion/issues/371) | Presentación de ARGO v2 y refinación de requerimientos módulo contractual con los usuarios product owner de las unidades de ejecución (Rectoría/IDEXUD) | Abierta | Gestión Contractual | 2026-10-02 |
| [#372](https://github.com/udistrital/argo_documentacion/issues/372) | Reestructuración microcliente gestion_contractual_mf | Abierta | Gestión Contractual | 2026-10-07 |
| [#373](https://github.com/udistrital/argo_documentacion/issues/373) | Pruebas funcionales y estabilización del registro de contrato incluyendo los pasos de registro de información y minuta en pdf - Parte 2 | Abierta | Gestión Contractual | 2026-10-07 |
| [#374](https://github.com/udistrital/argo_documentacion/issues/374) | Actualización de mockups del módulo de registro de contrato – Rol Abogado | Abierta | Gestión Contractual | 2026-10-09 |
| [#375](https://github.com/udistrital/argo_documentacion/issues/375) | Ajustar diseño del módulo de registro de contrato - Rol Abogado. | Cerrada | Sin hito | 2026-10-09 |
| [#376](https://github.com/udistrital/argo_documentacion/issues/376) | Investigación, evaluación técnica e implementación de una solución de Browser Fingerprinting Open Source en Angular con Single SPA | Abierta | Soporte y arquitectura general | 2026-10-13 |
| [#377](https://github.com/udistrital/argo_documentacion/issues/377) | Consolidar datos paramétricos ARGO v2 para su depuración | Abierta | Gestión Contractual | 2026-10-13 |
| [#381](https://github.com/udistrital/argo_documentacion/issues/381) | Rediseño de la vista de consulta de contratos y tablero de resumen por rol | Abierta | Gestión Contractual | 2026-10-16 |
| [#382](https://github.com/udistrital/argo_documentacion/issues/382) | Diseñar/Maquetar la vista de aprobación/rechazo masivo de contratos para el Jefe de Contratación | Cerrada | Gestión Contractual | 2026-10-16 |
| [#383](https://github.com/udistrital/argo_documentacion/issues/383) | Consolidación y depuración de datos paramétricos de Registro de Contrato (Unidad Ejecutora Rectoría) | Abierta | Gestión Contractual | 2026-10-16 |
| [#384](https://github.com/udistrital/argo_documentacion/issues/384) | Revisión y ajuste del modelo de datos basado en análisis de Issues de documentación | Abierta | Gestión Contractual | 2026-10-16 |
| [#385](https://github.com/udistrital/argo_documentacion/issues/385) | Implementación de microservicio CRUD en Beego v2 basado en modelo refinado | Abierta | Gestión Contractual | 2026-10-16 |
| [#386](https://github.com/udistrital/argo_documentacion/issues/386) | Definición e implementación de endpoints de consulta de metadatos para tableros de seguimiento | Abierta | Gestión Contractual | 2026-10-16 |
| [#387](https://github.com/udistrital/argo_documentacion/issues/387) | Implementación y ajuste de microservicio Mid para consolidación de datos paramétricos y contractuales | Abierta | Gestión Contractual | 2026-10-16 |
| [#388](https://github.com/udistrital/argo_documentacion/issues/388) | Integración entre microcliente y microservicios para registro de contratos, junto con estabilización y generación de services | Abierta | Gestión Contractual | 2026-10-16 |
| [#389](https://github.com/udistrital/argo_documentacion/issues/389) | Continuidad en el refinamiento del modelo de datos de contratación | Abierta | Gestión Contractual | 2026-10-23 |
| [#390](https://github.com/udistrital/argo_documentacion/issues/390) | Integración entre microcliente y microservicios para registro, actualización y visualización de contratos, junto con estabilización y generación de services | Cerrada | Gestión Contractual | 2026-10-23 |
| [#391](https://github.com/udistrital/argo_documentacion/issues/391) | Apoyo al despliegue en ambiente de pruebas y ejecución de pruebas funcionales | Abierta | Gestión Contractual | 2026-10-23 |
| [#392](https://github.com/udistrital/argo_documentacion/issues/392) | Apoyo al despliegue en ambiente de pruebas y ejecución de pruebas funcionales | Abierta | Gestión Contractual | 2026-10-23 |
| [#393](https://github.com/udistrital/argo_documentacion/issues/393) | Elaboración de la guía de estandarización y buenas prácticas para el desarrollo Frontend (Microclientes) | Abierta | Soporte y arquitectura general | 2026-10-23 |
| [#396](https://github.com/udistrital/argo_documentacion/issues/396) | Creación de scripts SQL de migración/actualización de base de datos para ARGO v2 | Abierta | Gestión Contractual | 2026-10-29 |
| [#397](https://github.com/udistrital/argo_documentacion/issues/397) | Integración registro y visualización de contratos | Abierta | Gestión Contractual | 2026-11-04 |
| [#398](https://github.com/udistrital/argo_documentacion/issues/398) | Pruebas funcionales ARGO - Registro de contrato | Cerrada | Gestión Contractual | 2026-11-04 |
| [#399](https://github.com/udistrital/argo_documentacion/issues/399) | Integración de cambios MID - MF, despliegue de nuevo CRUD | Abierta | Gestión Contractual | 2026-11-06 |
| [sisifo #380](https://github.com/udistrital/sisifo_documentacion/issues/380) | Apoyo ajuste fallo componente texto enriquecido | Cerrada | Transversal | 2025-01-16 |

