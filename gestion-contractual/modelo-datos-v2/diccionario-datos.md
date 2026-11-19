# Diccionario de datos — ARGO v2, gestión contractual (#384 y #389)

> Generado por `scripts/genera_diccionario.js` desde `modelo-argo-v2.dbml`. No se edita a mano.

14 tablas, 13 relaciones. Base de datos y esquema provisionales: `administrativa` / `contratacion` (supuesto S3).

Columnas de la tabla de cada entidad: nombre, tipo PostgreSQL, si admite nulos, valor por defecto, descripción y origen del dato. "Origen" indica el sistema al que apunta una referencia externa (integer sin FK física), la tabla de una FK, o "ARGO v2" si el dato es propio.

## Contenido

- **contrato**: [contrato_general](#contrato_general), [estado_contrato](#estado_contrato), [supervisor_contrato](#supervisor_contrato), [ordenador_contrato](#ordenador_contrato), [contrato_arrendamiento](#contrato_arrendamiento), [convenio](#convenio), [especificacion_tecnica](#especificacion_tecnica)
- **presupuesto**: [disponibilidad_presupuestal](#disponibilidad_presupuestal), [registro_presupuestal](#registro_presupuestal)
- **poliza y amparos**: [poliza](#poliza), [amparo_poliza](#amparo_poliza), [estado_poliza](#estado_poliza)
- **documentos y actas**: [documento_contrato](#documento_contrato), [acta_inicio](#acta_inicio)

## contrato_general

Contrato y su información básica. Absorbe los datos 1 a 1 del proveedor (antes contratista) y del solicitante

Dominio: contrato.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| numero_contrato | varchar(50) | Sí |  | Número oficial del contrato. Se genera con la RN de generación cuando el contrato pasa a SUSCRITO; en ARGO v1 viene migrado. Nulo hasta la suscripción (A14) | ARGO v2 |
| vigencia_id | integer | No |  | Parámetros CRUD, tipo de parámetro Vigencia (tipo por confirmar). Año de vigencia del contrato | Parámetros CRUD |
| consecutivo_elaboracion | varchar(50) | Sí |  | Consecutivo de elaboración, previo a la suscripción | ARGO v2 |
| unidad_ejecutora_id | integer | No |  | Parámetros CRUD, tipo 146 Unidad Ejecutora (6818 Rectoría, 6819 IDEXUD) | Parámetros CRUD |
| tipo_compromiso_id | integer | Sí |  | Parámetros CRUD, tipo 111 Compromiso | Parámetros CRUD |
| tipo_contrato_id | integer | Sí |  | Parámetros CRUD, tipo 112 Contrato | Parámetros CRUD |
| perfil_contratista_id | integer | Sí |  | Parámetros CRUD, tipo 113 Perfil del Contratista (perfil profesional, no la entidad proveedor) | Parámetros CRUD |
| fecha_suscripcion_estudio | date | Sí |  | Fecha de suscripción del estudio o documento previo | ARGO v2 |
| aplica_poliza | boolean | Sí |  | Indica si el contrato exige póliza | ARGO v2 |
| modalidad_seleccion_id | integer | Sí |  | Parámetros CRUD, tipo 115 Modalidad de Selección | Parámetros CRUD |
| tipo_control_id | integer | Sí |  | Parámetros CRUD, tipo 119 Tipo de Control | Parámetros CRUD |
| tipologia_especifica_id | integer | Sí |  | Parámetros CRUD, tipo 114 Tipología Específica | Parámetros CRUD |
| regimen_contratacion_id | integer | Sí |  | Parámetros CRUD, tipo 116 Régimen de Contratación. Negocio propuso retirarlo; se mantiene nullable (supuesto S1) | Parámetros CRUD |
| procedimiento_id | integer | Sí |  | Parámetros CRUD, tipo 117 Procedimiento | Parámetros CRUD |
| plazo_ejecucion | integer | Sí |  | Duración del contrato, expresada en la unidad de unidad_ejecucion_id | ARGO v2 |
| unidad_ejecucion_id | integer | Sí |  | Parámetros CRUD, tipo 7 Tiempo (días, meses, años). No confundir con unidad_ejecutora_id | Parámetros CRUD |
| tipo_moneda_id | integer | Sí |  | Parámetros CRUD, tipo 122 Tipo de Moneda | Parámetros CRUD |
| valor_pesos | numeric(20,7) | Sí |  | Valor del contrato en pesos | ARGO v2 |
| valor_contrato_me | numeric(20,7) | Sí |  | Valor del contrato en moneda extranjera | ARGO v2 |
| valor_tasa_cambio | numeric(20,7) | Sí |  | Tasa de cambio aplicada al valor en moneda extranjera | ARGO v2 |
| tipo_gasto_id | integer | Sí |  | Parámetros CRUD, tipo 123 Tipo de Gasto | Parámetros CRUD |
| origen_recursos_id | integer | Sí |  | Parámetros CRUD, tipo 124 Origen Recursos | Parámetros CRUD |
| origen_presupuesto_id | integer | Sí |  | Parámetros CRUD, tipo 125 Origen Presupuesto | Parámetros CRUD |
| tema_gasto_inversion_id | integer | Sí |  | Parámetros CRUD, tipo 126 Tema Gasto Inversión. Negocio propuso retirarlo; se mantiene nullable (supuesto S1) | Parámetros CRUD |
| medio_pago_id | integer | Sí |  | Parámetros CRUD, tipo 127 Medio de Pago | Parámetros CRUD |
| clausula_registro_presupuestal | boolean | Sí |  | Indica si el contrato requiere la cláusula adicional de registro presupuestal | ARGO v2 |
| modo_pago | varchar | Sí |  | Modo de pago del contrato | ARGO v2 |
| objeto | varchar | Sí |  | Objeto del contrato | ARGO v2 |
| justificacion | varchar | Sí |  | Justificación del contrato | ARGO v2 |
| actividades | varchar | Sí |  | Actividades del contrato, en un solo campo porque la fuente las entrega unificadas | ARGO v2 |
| condiciones | varchar | Sí |  | Condiciones del contrato | ARGO v2 |
| observaciones | varchar(1000) | Sí |  | Observaciones del contrato | ARGO v2 |
| fecha_inicial | date | Sí |  | Fecha de inicio del contrato | ARGO v2 |
| fecha_final | date | Sí |  | Fecha de finalización del contrato | ARGO v2 |
| fecha_suscripcion | date | Sí |  | Fecha en que se suscribe el contrato (A6). También queda en los estados del contrato; aquí permite filtrar y trazar | ARGO v2 |
| proveedor_numero_documento | varchar(20) | Sí |  | Número de documento del proveedor. Antes contratista.numero_documento (ítem 16). El proveedor se consulta en Ágora por este número | ARGO v2 |
| tipo_persona_id | integer | Sí |  | Parámetros CRUD, tipo 132 Tipo Persona (natural o jurídica) del proveedor. Antes contratista.tipo_persona_id | Parámetros CRUD |
| clase_proveedor_id | integer | Sí |  | Parámetros CRUD, tipo 120 Clase Contratista (único o sociedad temporal). Antes contratista.clase_contratista_id | Parámetros CRUD |
| dependencia_solicitante_id | integer | Sí |  | OIKOS, dependencia que solicita el contrato. | OIKOS |
| dependencia_solicitante_legado_id | integer | Sí |  | OIKOS, dependencia que solicita el contrato legado. | OIKOS |
| sede_solicitante_legado_id | integer | Sí |  | OIKOS, sede donde se origina la solicitud legado. | OIKOS |
| usuario_id | integer | Sí |  | Identificador del usuario que registra o modifica el contrato | ARGO v2 |
| usuario_rol | varchar(40) | Sí |  | Rol del usuario que registra o modifica el contrato | ARGO v2 |
| usuario_legado | varchar(15) | Sí |  | Usuario de ARGO v1, para compatibilidad con la migración | ARGO v1 (migración) |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_contrato_general` PRIMARY KEY (id); UNIQUE `uq_numero_contrato_vigencia_id_contrato_general` (numero_contrato, vigencia_id); UNIQUE `uq_consecutivo_elaboracion_contrato_general` (unidad_ejecutora_id, vigencia_id, consecutivo_elaboracion); Índice `idx_contrato_general_unidad_ejecutora_id` (unidad_ejecutora_id); Índice `idx_contrato_general_tipo_contrato_id` (tipo_contrato_id).

## estado_contrato

Historial de estados del contrato: el visible para el usuario y el de la máquina de estados interna (ítem 10)

Dominio: contrato.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_estado_contrato_contrato_general) |
| estado_parametro_id | integer | Sí |  | Parámetros CRUD, tipo 137 Estados del contrato. Estado visible para el usuario (ítem 10) | Parámetros CRUD |
| estado_interno_parametro_id | integer | Sí |  | Parámetros CRUD, tipo 141 Estados internos del contrato. Máquina de estados interna (ítem 10) | Parámetros CRUD |
| actual | boolean | No |  | Marca el estado vigente del contrato | ARGO v2 |
| motivo | varchar(250) | Sí |  | Razón del cambio de estado | ARGO v2 |
| fecha_evento | date | Sí |  | Fecha del cambio de estado | ARGO v2 |
| usuario_id | integer | No |  | Identificador del usuario que efectúa el cambio de estado | ARGO v2 |
| usuario_rol | varchar(40) | Sí |  | Rol del usuario que efectúa el cambio de estado | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_estado_contrato` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_estado_contrato_contrato_general); Índice `idx_estado_contrato_contrato_general_id` (contrato_general_id).

## supervisor_contrato

Supervisores asignados al contrato

Dominio: contrato.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_supervisor_contrato_contrato_general) |
| supervisor_id | integer | Sí |  | Terceros, tercero que ejerce como supervisor | Terceros |
| documento | integer | Sí |  | Documento del supervisor | ARGO v2 |
| digito_verificacion | integer | Sí |  | Dígito de verificación del documento del supervisor | ARGO v2 |
| cargo_id | integer | Sí |  | Parámetros CRUD, cargo del supervisor | Parámetros CRUD |
| dependencia_id | integer | Sí |  | OIKOS, dependencia del supervisor | OIKOS |
| sede_legado | varchar(50) | Sí |  | Sede en sedes_SIC de ARGO v1 | ARGO v2 |
| dependencia_legado | varchar(50) | Sí |  | Dependencia en dependencias_SIC de ARGO v1 | ARGO v2 |
| cargo_legado | varchar(250) | Sí |  | Cargo en la tabla de supervisores de ARGO v1 | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_supervisor_contrato` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_supervisor_contrato_contrato_general); Índice `idx_supervisor_contrato_contrato_general_id` (contrato_general_id); Índice `idx_supervisor_contrato_supervisor_id` (supervisor_id).

## ordenador_contrato

Ordenador del gasto del contrato. Validar soporte de migración ARGO v1. Confirmar si un contrato puede tener varios ordenadores (A12)

Dominio: contrato.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_ordenador_contrato_contrato_general) |
| tercero_id | integer | Sí |  | Terceros, tercero que actúa como ordenador del gasto | Terceros |
| cargo_id | integer | Sí |  | Parámetros CRUD, cargo del ordenador | Parámetros CRUD |
| documento_identidad | varchar(20) | Sí |  | Documento de identidad del ordenador | ARGO v2 |
| resolucion | varchar(250) | Sí |  | Resolución que autoriza al ordenador | ARGO v2 |
| ordenador_argo_id | integer | Sí |  | ARGO v1, PK de la tabla ordenadores | ARGO v1 (migración) |
| ordenador_sicapital_id | integer | Sí |  | ARGO v1, id_ordenador de la tabla ordenadores (SiCapital) | SiCapital |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_ordenador_contrato` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_ordenador_contrato_contrato_general); Índice `idx_ordenador_contrato_contrato_general_id` (contrato_general_id).

## contrato_arrendamiento

Datos propios de un contrato de arrendamiento (1 a 1 con el contrato)

Dominio: contrato.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_contrato_arrendamiento_contrato_general) |
| destinacion | varchar(5000) | Sí |  | Uso previsto del inmueble arrendado | ARGO v2 |
| plazo_pago_mensual | integer | Sí |  | Día del mes establecido para el pago | ARGO v2 |
| reajuste | varchar(255) | Sí |  | Condición de reajuste del canon | ARGO v2 |
| plazo_administracion | integer | Sí |  | Plazo de pago de la administración | ARGO v2 |
| valor_administracion | numeric(20,7) | Sí |  | Valor de la administración | ARGO v2 |
| plazo_entrega | integer | Sí |  | Plazo de entrega del inmueble | ARGO v2 |
| valor_arrendamiento | numeric(20,7) | Sí |  | Valor mensual del arrendamiento | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_contrato_arrendamiento` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_contrato_arrendamiento_contrato_general); UNIQUE `uq_contrato_general_id_contrato_arrendamiento` (contrato_general_id).

## convenio

Convenio en el que se enmarca el contrato

Dominio: contrato.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_convenio_contrato_general) |
| nombre | varchar(250) | Sí |  | Nombre del convenio | ARGO v2 |
| vigencia | integer | Sí |  | Año de vigencia del convenio | ARGO v2 |
| tipo_convenio_id | integer | Sí |  | Parámetros CRUD, tipo de convenio (tipo de parámetro por confirmar) | Parámetros CRUD |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_convenio` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_convenio_contrato_general); Índice `idx_convenio_contrato_general_id` (contrato_general_id).

## especificacion_tecnica

Ítems técnicos y económicos del contrato

Dominio: contrato.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | Sí |  |  | FK a contrato_general.id (fk_especificacion_tecnica_contrato_general) |
| descripcion | varchar | Sí |  | Descripción del ítem o servicio | ARGO v2 |
| cantidad | integer | Sí |  | Cantidad de ítems | ARGO v2 |
| valor_unitario | numeric(20,7) | Sí |  | Valor unitario del ítem | ARGO v2 |
| valor_total | numeric(20,7) | Sí |  | Valor total del ítem | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_especificacion_tecnica` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_especificacion_tecnica_contrato_general); Índice `idx_especificacion_tecnica_contrato_general_id` (contrato_general_id).

## disponibilidad_presupuestal

Certificados de disponibilidad presupuestal (CDP) del contrato

Dominio: presupuesto.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_disponibilidad_presupuestal_contrato_general) |
| numero_cdp_id | integer | Sí |  | SiCapital, número del CDP con el que se consulta la fuente | SiCapital |
| vigencia_cdp_id | integer | Sí |  | Año de vigencia del CDP | ARGO v2 |
| fecha_registro | date | Sí |  | Fecha de registro del CDP | ARGO v2 |
| valor_a_tomar | numeric(20,7) | Sí |  | Valor en pesos que el contrato toma del CDP (puede ser menor que el valor del CDP) | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_disponibilidad_presupuestal` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_disponibilidad_presupuestal_contrato_general); Índice `idx_disponibilidad_presupuestal_contrato_general_id` (contrato_general_id).

## registro_presupuestal

Registros presupuestales (RP) expedidos sobre un CDP

Dominio: presupuesto.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| disponibilidad_presupuestal_id | integer | No |  | Antes cdp_id | FK a disponibilidad_presupuestal.id (fk_registro_presupuestal_disponibilidad_presupuestal) |
| numero_registro_presupuestal | integer | Sí |  | Número del registro presupuestal (RP). Antes registro_presupuestal | ARGO v2 |
| vigencia_rp_id | integer | Sí |  | Año de vigencia del RP | ARGO v2 |
| fecha_registro | date | Sí |  | Fecha de registro del RP | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_registro_presupuestal` PRIMARY KEY (id); FK `disponibilidad_presupuestal_id` → disponibilidad_presupuestal.id (fk_registro_presupuestal_disponibilidad_presupuestal); Índice `idx_registro_presupuestal_disponibilidad_presupuestal_id` (disponibilidad_presupuestal_id).

## poliza

Pólizas expedidas para las garantías del contrato

Dominio: poliza y amparos.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_poliza_contrato_general) |
| numero_poliza | varchar(50) | Sí |  | Número con el que la aseguradora identifica la póliza. Sin restricción de unicidad (#351) | ARGO v2 |
| entidad_aseguradora_id | integer | Sí |  | Parámetros CRUD, entidad aseguradora (tipo de parámetro por confirmar) | Parámetros CRUD |
| descripcion | varchar | Sí |  | Descripción de la póliza | ARGO v2 |
| fecha_inicio | date | Sí |  | Inicio de vigencia de la póliza | ARGO v2 |
| fecha_fin | date | Sí |  | Fin de vigencia de la póliza | ARGO v2 |
| fecha_expedicion | date | Sí |  | Fecha en que la aseguradora expide la póliza | ARGO v2 |
| fecha_aprobacion | date | Sí |  | Fecha en que la Universidad aprueba la póliza | ARGO v2 |
| usuario_id | integer | Sí |  | Identificador del usuario que registra o modifica la póliza | ARGO v2 |
| usuario_rol | varchar(40) | Sí |  | Rol del usuario que registra o modifica la póliza | ARGO v2 |
| usuario_legado | varchar(15) | Sí |  | Usuario de ARGO v1, para compatibilidad con la migración | ARGO v1 (migración) |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_poliza` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_poliza_contrato_general); Índice `idx_poliza_contrato_general_id` (contrato_general_id).

## estado_poliza

Historial de estados de la póliza. El estado vigente es el registro más reciente

Dominio: poliza y amparos.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| poliza_id | integer | No |  |  | FK a poliza.id (fk_estado_poliza_poliza) |
| estado_parametro_id | integer | No |  | Parámetros CRUD, estado de la póliza (tipo de parámetro por confirmar; estados por definir con la Analista) | Parámetros CRUD |
| motivo | varchar(250) | Sí |  | Razón del cambio de estado | ARGO v2 |
| usuario_id | integer | No |  | Identificador del usuario que efectúa el cambio de estado | ARGO v2 |
| usuario_rol | varchar(40) | Sí |  | Rol del usuario que efectúa el cambio de estado | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_estado_poliza` PRIMARY KEY (id); FK `poliza_id` → poliza.id (fk_estado_poliza_poliza); Índice `idx_estado_poliza_poliza_id` (poliza_id).

## amparo_poliza

Amparos exigidos al contrato y cubiertos luego por la póliza

Dominio: poliza y amparos.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  | El amparo se registra con la minuta, antes de que exista la póliza (#351) | FK a contrato_general.id (fk_amparo_poliza_contrato_general) |
| poliza_id | integer | Sí |  | Nulo hasta que la póliza se expide y se asocia | FK a poliza.id (fk_amparo_poliza_poliza) |
| amparo_id | integer | No |  | Parámetros CRUD, tipo 118 Amparo | Parámetros CRUD |
| tipo_valor_amparo_id | integer | Sí |  | Parámetros CRUD, tipo de valor de la suficiencia (porcentaje o SMLV; tipo de parámetro por confirmar) | Parámetros CRUD |
| suficiencia | numeric(20,7) | Sí |  | Suficiencia del amparo. Se interpreta según tipo_valor_amparo_id; excepción a numeric(5,4) documentada en la #351 | ARGO v2 |
| valor | numeric(20,7) | Sí |  | Valor asegurado del amparo | ARGO v2 |
| descripcion | varchar | Sí |  | Descripción del amparo | ARGO v2 |
| fecha_inicio | date | Sí |  | Inicio de vigencia del amparo | ARGO v2 |
| fecha_fin | date | Sí |  | Fin de vigencia del amparo | ARGO v2 |
| usuario_id | integer | Sí |  | Identificador del usuario que registra o modifica el amparo | ARGO v2 |
| usuario_rol | varchar(40) | Sí |  | Rol del usuario que registra o modifica el amparo | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_amparo_poliza` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_amparo_poliza_contrato_general); FK `poliza_id` → poliza.id (fk_amparo_poliza_poliza); Índice `idx_amparo_poliza_contrato_general_id` (contrato_general_id); Índice `idx_amparo_poliza_poliza_id` (poliza_id).

## documento_contrato

Documentos del contrato en una sola tabla, sin estados (A9). Relación polimórfica: un documento pertenece a un contrato_general, una poliza o un acta_inicio. Se incorpora firma manual; si se integra otro servicio se registra igualmente en documento_contrato (ítem 42)

Dominio: documentos y actas.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| entidad_tipo | varchar(50) | No |  | Tabla a la que pertenece el documento: contrato_general, poliza o acta_inicio | ARGO v2 |
| entidad_id | integer | No |  | Identificador del registro en la tabla indicada por entidad_tipo (sin FK física) | ARGO v2 |
| tipo_documento_id | integer | Sí |  | Parámetros CRUD, tipo de documento (tipo 133 Documentos Contrato) | Parámetros CRUD |
| documento_id | integer | Sí |  | Gestor Documental, identificador del documento | Gestor Documental |
| documento_enlace | varchar(50) | Sí |  | Gestor Documental, enlace del documento | Gestor Documental |
| usuario_id | integer | Sí |  | Identificador del usuario que registra el documento | ARGO v2 |
| usuario_rol | varchar(40) | Sí |  | Rol del usuario que registra el documento | ARGO v2 |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_documento_contrato` PRIMARY KEY (id); Índice `idx_documento_contrato_entidad_tipo_entidad_id` (entidad_tipo, entidad_id).

## acta_inicio

Acta con la que inicia la ejecución del contrato

Dominio: documentos y actas.

| Columna | Tipo | Nulo | Por defecto | Descripción | Origen |
|---|---|---|---|---|---|
| id | serial | No | secuencia | Identificador del registro (llave primaria) | Auditoría / llave |
| contrato_general_id | integer | No |  |  | FK a contrato_general.id (fk_acta_inicio_contrato_general) |
| descripcion | varchar | Sí |  | Descripción del acta de inicio | ARGO v2 |
| fecha_inicio | date | Sí |  | Fecha de inicio de ejecución del contrato | ARGO v2 |
| fecha_fin | date | Sí |  | Fecha prevista de finalización del contrato | ARGO v2 |
| fecha_suscripcion | date | Sí |  | Fecha de suscripción del acta de inicio (no la del contrato). Supuesto S2 | ARGO v2 |
| numero_acta | varchar(50) | Sí |  | Número del acta de inicio. Supuesto S2 | ARGO v2 |
| valor_disponibilidad | numeric(20,7) | Sí |  | Valor del CDP registrado en el acta. Duplica información de disponibilidad_presupuestal (supuesto S2) | ARGO v2 |
| numero_registro_presupuestal | varchar(50) | Sí |  | Número del RP digitado en el acta. Duplica información de registro_presupuestal (supuesto S2) | ARGO v2 |
| valor_registro_presupuestal | numeric(20,7) | Sí |  | Valor del RP registrado en el acta. Supuesto S2 | ARGO v2 |
| valor_anticipo | numeric(20,7) | Sí |  | Valor del anticipo del contrato. Supuesto S2 | ARGO v2 |
| nombre_interventor | varchar(250) | Sí |  | Nombre del interventor, cuando aplica. Supuesto S2 | ARGO v2 |
| usuario_id | integer | Sí |  | Identificador del usuario que registra el acta | ARGO v2 |
| usuario_rol | varchar(40) | Sí |  | Rol del usuario que registra el acta | ARGO v2 |
| usuario_legado | varchar(15) | Sí |  | Usuario de ARGO v1, para compatibilidad con la migración | ARGO v1 (migración) |
| activo | boolean | No | true | Indica si el registro está activo (borrado lógico) | Auditoría / llave |
| fecha_creacion | timestamp | No | now() | Fecha y hora de creación del registro | Auditoría / llave |
| fecha_modificacion | timestamp | No | now() | Fecha y hora de la última modificación; al crear es igual a fecha_creacion | Auditoría / llave |

Restricciones e índices: `pk_acta_inicio` PRIMARY KEY (id); FK `contrato_general_id` → contrato_general.id (fk_acta_inicio_contrato_general); Índice `idx_acta_inicio_contrato_general_id` (contrato_general_id).

## Temas en stand by o pendientes

No se modelan; están como notas en el diagrama.

- **A8 · Estudio previo y proceso contractual (stand by)**. Pendiente de validación con Ágora. No se modelan campos nuevos.
- **A11 · Proyecto de extensión (por confirmar con la Analista)**. Validar si se registra en un campo actual o como un selector nuevo exclusivo de IDEXUD.
- **A12 · Cardinalidad (stand by)**. Proveedor: 1 a 1, absorbido en contrato_general. Ordenador: confirmar si un contrato puede tener varios. Solicitante: 1 a 1, absorbido en contrato_general (dependencia_solicitante_id, dependencia_solicitante_legado_id y sede_solicitante_legado_id; sede_solicitante_id sale en la #396). No se crean UNIQUE en contrato_general_id.
- **Lugar de ejecución**. La tabla lugar_ejecucion no se incluye (ítem 2) y sus columnas no pasan a contrato_general: el modelo final del LT (#389) retira las columnas lugar_ejecucion_. La validación de la depuración de datos contra resoluciones en producción queda con la Analista.
