-- =====================================================================
-- ARGO v2 · Gestión contractual · Modelo de datos refinado (#384)
-- DDL de la base nueva para la #385 (CRUD en Beego v2).
-- Fuente del modelo: ../modelo-argo-v2.dbml
--
-- Base de datos: administrativa (provisional, supuesto S3).
-- Esquema: contratacion (provisional, supuesto S3). Para cambiarlo basta
-- con editar la línea SET search_path; el bloque DO crea ese esquema.
--
-- Referencias externas (Parámetros CRUD, Terceros, OIKOS, SiCapital,
-- Gestor Documental) son integer sin FK física; el COMMENT de cada
-- columna indica a qué apuntan.
-- =====================================================================

SET search_path TO contratacion;

DO $$
BEGIN
    EXECUTE format('CREATE SCHEMA IF NOT EXISTS %I', current_setting('search_path'));
END
$$;

-- ---------------------------------------------------------------------
-- Contrato
-- ---------------------------------------------------------------------

CREATE TABLE contrato_general (
    id                              serial          NOT NULL,
    numero_contrato                 varchar(50),
    vigencia                        varchar(4),
    consecutivo_elaboracion         varchar(50),
    unidad_ejecutora_id             integer         NOT NULL,
    tipo_compromiso_id              integer,
    tipo_contrato_id                integer,
    perfil_contratista_id           integer,
    fecha_suscripcion_estudio       date,
    aplica_poliza                   boolean,
    modalidad_seleccion_id          integer,
    tipo_control_id                 integer,
    tipologia_especifica_id         integer,
    regimen_contratacion_id         integer,
    procedimiento_id                integer,
    plazo_ejecucion                 integer,
    unidad_ejecucion_id             integer,
    tipo_moneda_id                  integer,
    valor_pesos                     numeric(20,7),
    valor_contrato_me               numeric(20,7),
    valor_tasa_cambio               numeric(20,7),
    tipo_gasto_id                   integer,
    origen_recursos_id              integer,
    origen_presupuesto_id           integer,
    tema_gasto_inversion_id         integer,
    medio_pago_id                   integer,
    clausula_registro_presupuestal  boolean,
    modo_pago                       varchar(1000),
    objeto                          varchar(2000),
    justificacion                   varchar(4000),
    actividades                     varchar(8000),
    condiciones                     varchar(4000),
    observaciones                   varchar(1000),
    fecha_inicial                   date,
    fecha_final                     date,
    fecha_suscripcion               date,
    proveedor_numero_documento      varchar(20),
    tipo_persona_id                 integer,
    clase_proveedor_id              integer,
    lugar_ejecucion_pais_id         integer,
    lugar_ejecucion_ciudad_id       integer,
    lugar_ejecucion_municipio_id    integer,
    lugar_ejecucion_dependencia_id  integer,
    lugar_ejecucion_sede_id         integer,
    lugar_ejecucion_direccion       varchar(150),
    usuario_id                      integer,
    usuario_rol                     varchar(40),
    usuario_legado                  varchar(15),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_contrato_general PRIMARY KEY (id),
    CONSTRAINT uq_numero_contrato_vigencia_contrato_general UNIQUE (numero_contrato, vigencia)
);

CREATE INDEX idx_contrato_general_unidad_ejecutora_id ON contrato_general (unidad_ejecutora_id);
CREATE INDEX idx_contrato_general_tipo_contrato_id ON contrato_general (tipo_contrato_id);

COMMENT ON TABLE contrato_general IS 'Contrato y su información básica. Absorbe los datos 1 a 1 del proveedor (antes contratista) y del lugar de ejecución';
COMMENT ON COLUMN contrato_general.numero_contrato IS 'Número oficial del contrato. Se genera con la RN de generación cuando el contrato pasa a SUSCRITO; en ARGO v1 viene migrado. Nulo hasta la suscripción (A14)';
COMMENT ON COLUMN contrato_general.vigencia IS 'Año de vigencia del contrato (2025, 2026, ...)';
COMMENT ON COLUMN contrato_general.consecutivo_elaboracion IS 'Consecutivo de elaboración, previo a la suscripción';
COMMENT ON COLUMN contrato_general.unidad_ejecutora_id IS 'Parámetros CRUD, tipo 146 Unidad Ejecutora (6818 Rectoría, 6819 IDEXUD)';
COMMENT ON COLUMN contrato_general.tipo_compromiso_id IS 'Parámetros CRUD, tipo 111 Compromiso';
COMMENT ON COLUMN contrato_general.tipo_contrato_id IS 'Parámetros CRUD, tipo 112 Contrato';
COMMENT ON COLUMN contrato_general.perfil_contratista_id IS 'Parámetros CRUD, tipo 113 Perfil del Contratista (perfil profesional, no la entidad proveedor)';
COMMENT ON COLUMN contrato_general.fecha_suscripcion_estudio IS 'Fecha de suscripción del estudio o documento previo';
COMMENT ON COLUMN contrato_general.aplica_poliza IS 'Indica si el contrato exige póliza';
COMMENT ON COLUMN contrato_general.modalidad_seleccion_id IS 'Parámetros CRUD, tipo 115 Modalidad de Selección';
COMMENT ON COLUMN contrato_general.tipo_control_id IS 'Parámetros CRUD, tipo 119 Tipo de Control';
COMMENT ON COLUMN contrato_general.tipologia_especifica_id IS 'Parámetros CRUD, tipo 114 Tipología Específica';
COMMENT ON COLUMN contrato_general.regimen_contratacion_id IS 'Parámetros CRUD, tipo 116 Régimen de Contratación. Negocio propuso retirarlo; se mantiene nullable (supuesto S1)';
COMMENT ON COLUMN contrato_general.procedimiento_id IS 'Parámetros CRUD, tipo 117 Procedimiento';
COMMENT ON COLUMN contrato_general.plazo_ejecucion IS 'Duración del contrato, expresada en la unidad de unidad_ejecucion_id';
COMMENT ON COLUMN contrato_general.unidad_ejecucion_id IS 'Parámetros CRUD, tipo 7 Tiempo (días, meses, años). No confundir con unidad_ejecutora_id';
COMMENT ON COLUMN contrato_general.tipo_moneda_id IS 'Parámetros CRUD, tipo 122 Tipo de Moneda';
COMMENT ON COLUMN contrato_general.valor_pesos IS 'Valor del contrato en pesos';
COMMENT ON COLUMN contrato_general.valor_contrato_me IS 'Valor del contrato en moneda extranjera';
COMMENT ON COLUMN contrato_general.valor_tasa_cambio IS 'Tasa de cambio aplicada al valor en moneda extranjera';
COMMENT ON COLUMN contrato_general.tipo_gasto_id IS 'Parámetros CRUD, tipo 123 Tipo de Gasto';
COMMENT ON COLUMN contrato_general.origen_recursos_id IS 'Parámetros CRUD, tipo 124 Origen Recursos';
COMMENT ON COLUMN contrato_general.origen_presupuesto_id IS 'Parámetros CRUD, tipo 125 Origen Presupuesto';
COMMENT ON COLUMN contrato_general.tema_gasto_inversion_id IS 'Parámetros CRUD, tipo 126 Tema Gasto Inversión. Negocio propuso retirarlo; se mantiene nullable (supuesto S1)';
COMMENT ON COLUMN contrato_general.medio_pago_id IS 'Parámetros CRUD, tipo 127 Medio de Pago';
COMMENT ON COLUMN contrato_general.clausula_registro_presupuestal IS 'Indica si el contrato requiere la cláusula adicional de registro presupuestal';
COMMENT ON COLUMN contrato_general.modo_pago IS 'Modo de pago del contrato';
COMMENT ON COLUMN contrato_general.objeto IS 'Objeto del contrato';
COMMENT ON COLUMN contrato_general.justificacion IS 'Justificación del contrato';
COMMENT ON COLUMN contrato_general.actividades IS 'Actividades del contrato, en un solo campo porque la fuente las entrega unificadas';
COMMENT ON COLUMN contrato_general.condiciones IS 'Condiciones del contrato';
COMMENT ON COLUMN contrato_general.observaciones IS 'Observaciones del contrato';
COMMENT ON COLUMN contrato_general.fecha_inicial IS 'Fecha de inicio del contrato';
COMMENT ON COLUMN contrato_general.fecha_final IS 'Fecha de finalización del contrato';
COMMENT ON COLUMN contrato_general.fecha_suscripcion IS 'Fecha en que se suscribe el contrato (A6). También queda en los estados del contrato; aquí permite filtrar y trazar';
COMMENT ON COLUMN contrato_general.proveedor_numero_documento IS 'Número de documento del proveedor. Antes contratista.numero_documento (ítem 16). El proveedor se consulta en Ágora por este número';
COMMENT ON COLUMN contrato_general.tipo_persona_id IS 'Parámetros CRUD, tipo 132 Tipo Persona (natural o jurídica) del proveedor. Antes contratista.tipo_persona_id';
COMMENT ON COLUMN contrato_general.clase_proveedor_id IS 'Parámetros CRUD, tipo 120 Clase Contratista (único o sociedad temporal). Antes contratista.clase_contratista_id';
COMMENT ON COLUMN contrato_general.lugar_ejecucion_pais_id IS 'País del lugar de ejecución (referencia externa por confirmar: OIKOS o Parámetros). Antes lugar_ejecucion.pais_id. Pendiente validar depuración de datos (supuesto S7)';
COMMENT ON COLUMN contrato_general.lugar_ejecucion_ciudad_id IS 'Ciudad del lugar de ejecución (referencia externa por confirmar). Antes lugar_ejecucion.ciudad_id (supuesto S7)';
COMMENT ON COLUMN contrato_general.lugar_ejecucion_municipio_id IS 'Municipio del lugar de ejecución (referencia externa por confirmar). Antes lugar_ejecucion.municipio_id (supuesto S7)';
COMMENT ON COLUMN contrato_general.lugar_ejecucion_dependencia_id IS 'OIKOS, dependencia del lugar de ejecución. Antes lugar_ejecucion.dependencia_id (supuesto S7)';
COMMENT ON COLUMN contrato_general.lugar_ejecucion_sede_id IS 'OIKOS, sede del lugar de ejecución. Antes lugar_ejecucion.sede_id (supuesto S7)';
COMMENT ON COLUMN contrato_general.lugar_ejecucion_direccion IS 'Dirección del lugar de ejecución. Antes lugar_ejecucion.direccion (supuesto S7)';
COMMENT ON COLUMN contrato_general.usuario_id IS 'Identificador del usuario que registra o modifica el contrato';
COMMENT ON COLUMN contrato_general.usuario_rol IS 'Rol del usuario que registra o modifica el contrato';
COMMENT ON COLUMN contrato_general.usuario_legado IS 'Usuario de ARGO v1, para compatibilidad con la migración';

CREATE TABLE estado_contrato (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    estado_parametro_id             integer,
    estado_interno_parametro_id     integer,
    actual                          boolean         NOT NULL,
    motivo                          varchar(250),
    fecha_evento                    date,
    usuario_id                      integer         NOT NULL,
    usuario_rol                     varchar(40),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_estado_contrato PRIMARY KEY (id),
    CONSTRAINT fk_estado_contrato_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_estado_contrato_contrato_general_id ON estado_contrato (contrato_general_id);

COMMENT ON TABLE estado_contrato IS 'Historial de estados del contrato (general e interno)';
COMMENT ON COLUMN estado_contrato.estado_parametro_id IS 'Parámetros CRUD, tipo 137 Estados del contrato (estado general)';
COMMENT ON COLUMN estado_contrato.estado_interno_parametro_id IS 'Parámetros CRUD, tipo 141 Estados internos del contrato';
COMMENT ON COLUMN estado_contrato.actual IS 'Marca el estado vigente del contrato';
COMMENT ON COLUMN estado_contrato.motivo IS 'Razón del cambio de estado';
COMMENT ON COLUMN estado_contrato.fecha_evento IS 'Fecha del cambio de estado';
COMMENT ON COLUMN estado_contrato.usuario_id IS 'Identificador del usuario que efectúa el cambio de estado';
COMMENT ON COLUMN estado_contrato.usuario_rol IS 'Rol del usuario que efectúa el cambio de estado';

CREATE TABLE solicitante (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    dependencia_id                  integer         NOT NULL,
    sede_id                         integer         NOT NULL,
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_solicitante PRIMARY KEY (id),
    CONSTRAINT fk_solicitante_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_solicitante_contrato_general_id ON solicitante (contrato_general_id);

COMMENT ON TABLE solicitante IS 'Dependencia y sede que solicitan el contrato. Cardinalidad 1 a 1 por validar (A12)';
COMMENT ON COLUMN solicitante.dependencia_id IS 'OIKOS, dependencia que solicita el contrato. Antes dependencia_solicitante_id';
COMMENT ON COLUMN solicitante.sede_id IS 'OIKOS, sede donde se origina la solicitud. Antes sede_solicitante_id';

CREATE TABLE supervisor_contrato (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    supervisor_id                   integer,
    documento                       integer,
    digito_verificacion             integer,
    cargo_id                        integer,
    sede_id                         integer         NOT NULL,
    dependencia_id                  integer         NOT NULL,
    sede_legado                     varchar(50),
    dependencia_legado              varchar(50),
    cargo_legado                    varchar(250),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_supervisor_contrato PRIMARY KEY (id),
    CONSTRAINT fk_supervisor_contrato_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_supervisor_contrato_contrato_general_id ON supervisor_contrato (contrato_general_id);
CREATE INDEX idx_supervisor_contrato_supervisor_id ON supervisor_contrato (supervisor_id);

COMMENT ON TABLE supervisor_contrato IS 'Supervisores asignados al contrato';
COMMENT ON COLUMN supervisor_contrato.supervisor_id IS 'Terceros, tercero que ejerce como supervisor';
COMMENT ON COLUMN supervisor_contrato.documento IS 'Documento del supervisor';
COMMENT ON COLUMN supervisor_contrato.digito_verificacion IS 'Dígito de verificación del documento del supervisor';
COMMENT ON COLUMN supervisor_contrato.cargo_id IS 'Parámetros CRUD, cargo del supervisor';
COMMENT ON COLUMN supervisor_contrato.sede_id IS 'OIKOS, sede del supervisor';
COMMENT ON COLUMN supervisor_contrato.dependencia_id IS 'OIKOS, dependencia del supervisor';
COMMENT ON COLUMN supervisor_contrato.sede_legado IS 'Sede en sedes_SIC de ARGO v1';
COMMENT ON COLUMN supervisor_contrato.dependencia_legado IS 'Dependencia en dependencias_SIC de ARGO v1';
COMMENT ON COLUMN supervisor_contrato.cargo_legado IS 'Cargo en la tabla de supervisores de ARGO v1';

CREATE TABLE ordenador_contrato (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    tercero_id                      integer,
    cargo_id                        integer,
    documento_identidad             varchar(20),
    resolucion                      varchar(250),
    ordenador_argo_id               integer,
    ordenador_sicapital_id          integer,
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_ordenador_contrato PRIMARY KEY (id),
    CONSTRAINT fk_ordenador_contrato_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_ordenador_contrato_contrato_general_id ON ordenador_contrato (contrato_general_id);

COMMENT ON TABLE ordenador_contrato IS 'Ordenador del gasto del contrato. Validar soporte de migración ARGO v1. Confirmar si un contrato puede tener varios ordenadores (A12)';
COMMENT ON COLUMN ordenador_contrato.tercero_id IS 'Terceros, tercero que actúa como ordenador del gasto';
COMMENT ON COLUMN ordenador_contrato.cargo_id IS 'Parámetros CRUD, cargo del ordenador';
COMMENT ON COLUMN ordenador_contrato.documento_identidad IS 'Documento de identidad del ordenador';
COMMENT ON COLUMN ordenador_contrato.resolucion IS 'Resolución que autoriza al ordenador';
COMMENT ON COLUMN ordenador_contrato.ordenador_argo_id IS 'ARGO v1, PK de la tabla ordenadores';
COMMENT ON COLUMN ordenador_contrato.ordenador_sicapital_id IS 'ARGO v1, id_ordenador de la tabla ordenadores (SiCapital)';

CREATE TABLE contrato_arrendamiento (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    destinacion                     varchar(1000),
    plazo_pago_mensual              integer,
    reajuste                        varchar(255),
    plazo_administracion            integer,
    valor_administracion            numeric(20,7),
    plazo_entrega                   integer,
    valor_arrendamiento             numeric(20,7),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_contrato_arrendamiento PRIMARY KEY (id),
    CONSTRAINT uq_contrato_general_id_contrato_arrendamiento UNIQUE (contrato_general_id),
    CONSTRAINT fk_contrato_arrendamiento_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

COMMENT ON TABLE contrato_arrendamiento IS 'Datos propios de un contrato de arrendamiento (1 a 1 con el contrato)';
COMMENT ON COLUMN contrato_arrendamiento.destinacion IS 'Uso previsto del inmueble arrendado';
COMMENT ON COLUMN contrato_arrendamiento.plazo_pago_mensual IS 'Día del mes establecido para el pago';
COMMENT ON COLUMN contrato_arrendamiento.reajuste IS 'Condición de reajuste del canon';
COMMENT ON COLUMN contrato_arrendamiento.plazo_administracion IS 'Plazo de pago de la administración';
COMMENT ON COLUMN contrato_arrendamiento.valor_administracion IS 'Valor de la administración';
COMMENT ON COLUMN contrato_arrendamiento.plazo_entrega IS 'Plazo de entrega del inmueble';
COMMENT ON COLUMN contrato_arrendamiento.valor_arrendamiento IS 'Valor mensual del arrendamiento';

CREATE TABLE convenio (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    nombre                          varchar(250),
    vigencia                        integer,
    tipo_convenio_id                integer,
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_convenio PRIMARY KEY (id),
    CONSTRAINT fk_convenio_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_convenio_contrato_general_id ON convenio (contrato_general_id);

COMMENT ON TABLE convenio IS 'Convenio en el que se enmarca el contrato';
COMMENT ON COLUMN convenio.nombre IS 'Nombre del convenio';
COMMENT ON COLUMN convenio.vigencia IS 'Año de vigencia del convenio';
COMMENT ON COLUMN convenio.tipo_convenio_id IS 'Parámetros CRUD, tipo de convenio (tipo de parámetro por confirmar)';

CREATE TABLE especificacion_tecnica (
    id                              serial          NOT NULL,
    contrato_general_id             integer,
    descripcion                     varchar(2000),
    cantidad                        integer         NOT NULL,
    valor_unitario                  numeric(20,7),
    valor_total                     numeric(20,7),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_especificacion_tecnica PRIMARY KEY (id),
    CONSTRAINT fk_especificacion_tecnica_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_especificacion_tecnica_contrato_general_id ON especificacion_tecnica (contrato_general_id);

COMMENT ON TABLE especificacion_tecnica IS 'Ítems técnicos y económicos del contrato';
COMMENT ON COLUMN especificacion_tecnica.descripcion IS 'Descripción del ítem o servicio';
COMMENT ON COLUMN especificacion_tecnica.cantidad IS 'Cantidad de ítems';
COMMENT ON COLUMN especificacion_tecnica.valor_unitario IS 'Valor unitario del ítem';
COMMENT ON COLUMN especificacion_tecnica.valor_total IS 'Valor total del ítem';

-- ---------------------------------------------------------------------
-- Presupuesto
-- ---------------------------------------------------------------------

CREATE TABLE disponibilidad_presupuestal (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    numero_cdp_id                   integer,
    vigencia_cdp                    integer,
    fecha_registro                  date,
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_disponibilidad_presupuestal PRIMARY KEY (id),
    CONSTRAINT fk_disponibilidad_presupuestal_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_disponibilidad_presupuestal_contrato_general_id ON disponibilidad_presupuestal (contrato_general_id);

COMMENT ON TABLE disponibilidad_presupuestal IS 'Certificados de disponibilidad presupuestal (CDP) del contrato';
COMMENT ON COLUMN disponibilidad_presupuestal.numero_cdp_id IS 'SiCapital, número del CDP con el que se consulta la fuente';
COMMENT ON COLUMN disponibilidad_presupuestal.vigencia_cdp IS 'Año de vigencia del CDP';
COMMENT ON COLUMN disponibilidad_presupuestal.fecha_registro IS 'Fecha de registro del CDP';

CREATE TABLE registro_presupuestal (
    id                              serial          NOT NULL,
    disponibilidad_presupuestal_id  integer         NOT NULL,
    numero_registro_presupuestal    integer,
    vigencia_rp                     integer,
    fecha_registro                  date,
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_registro_presupuestal PRIMARY KEY (id),
    CONSTRAINT fk_registro_presupuestal_disponibilidad_presupuestal FOREIGN KEY (disponibilidad_presupuestal_id) REFERENCES disponibilidad_presupuestal (id)
);

CREATE INDEX idx_registro_presupuestal_disponibilidad_presupuestal_id ON registro_presupuestal (disponibilidad_presupuestal_id);

COMMENT ON TABLE registro_presupuestal IS 'Registros presupuestales (RP) expedidos sobre un CDP';
COMMENT ON COLUMN registro_presupuestal.disponibilidad_presupuestal_id IS 'Antes cdp_id';
COMMENT ON COLUMN registro_presupuestal.numero_registro_presupuestal IS 'Número del registro presupuestal (RP). Antes registro_presupuestal';
COMMENT ON COLUMN registro_presupuestal.vigencia_rp IS 'Año de vigencia del RP';
COMMENT ON COLUMN registro_presupuestal.fecha_registro IS 'Fecha de registro del RP';

-- ---------------------------------------------------------------------
-- Póliza
-- ---------------------------------------------------------------------

CREATE TABLE poliza (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    numero_poliza                   varchar(50),
    entidad_aseguradora_id          integer,
    estado_poliza_id                integer,
    descripcion                     varchar(255),
    fecha_inicio                    date,
    fecha_fin                       date,
    fecha_expedicion                date,
    fecha_aprobacion                date,
    usuario_id                      integer,
    usuario_rol                     varchar(40),
    usuario_legado                  varchar(15),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_poliza PRIMARY KEY (id),
    CONSTRAINT fk_poliza_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_poliza_contrato_general_id ON poliza (contrato_general_id);

COMMENT ON TABLE poliza IS 'Pólizas expedidas para las garantías del contrato';
COMMENT ON COLUMN poliza.numero_poliza IS 'Número con el que la aseguradora identifica la póliza. Sin restricción de unicidad (#351)';
COMMENT ON COLUMN poliza.entidad_aseguradora_id IS 'Parámetros CRUD, entidad aseguradora (tipo de parámetro por confirmar)';
COMMENT ON COLUMN poliza.estado_poliza_id IS 'Parámetros CRUD, estado de la póliza. Estados por definir con la Analista (A7, supuesto S5)';
COMMENT ON COLUMN poliza.descripcion IS 'Descripción de la póliza';
COMMENT ON COLUMN poliza.fecha_inicio IS 'Inicio de vigencia de la póliza';
COMMENT ON COLUMN poliza.fecha_fin IS 'Fin de vigencia de la póliza';
COMMENT ON COLUMN poliza.fecha_expedicion IS 'Fecha en que la aseguradora expide la póliza';
COMMENT ON COLUMN poliza.fecha_aprobacion IS 'Fecha en que la Universidad aprueba la póliza';
COMMENT ON COLUMN poliza.usuario_id IS 'Identificador del usuario que registra o modifica la póliza';
COMMENT ON COLUMN poliza.usuario_rol IS 'Rol del usuario que registra o modifica la póliza';
COMMENT ON COLUMN poliza.usuario_legado IS 'Usuario de ARGO v1, para compatibilidad con la migración';

CREATE TABLE amparo_poliza (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    poliza_id                       integer,
    amparo_id                       integer         NOT NULL,
    tipo_valor_amparo_id            integer,
    suficiencia                     numeric(20,7),
    valor                           numeric(20,7),
    descripcion                     varchar(255),
    fecha_inicio                    date,
    fecha_fin                       date,
    usuario_id                      integer,
    usuario_rol                     varchar(40),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_amparo_poliza PRIMARY KEY (id),
    CONSTRAINT fk_amparo_poliza_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id),
    CONSTRAINT fk_amparo_poliza_poliza FOREIGN KEY (poliza_id) REFERENCES poliza (id)
);

CREATE INDEX idx_amparo_poliza_contrato_general_id ON amparo_poliza (contrato_general_id);
CREATE INDEX idx_amparo_poliza_poliza_id ON amparo_poliza (poliza_id);

COMMENT ON TABLE amparo_poliza IS 'Amparos exigidos al contrato y cubiertos luego por la póliza';
COMMENT ON COLUMN amparo_poliza.contrato_general_id IS 'El amparo se registra con la minuta, antes de que exista la póliza (#351)';
COMMENT ON COLUMN amparo_poliza.poliza_id IS 'Nulo hasta que la póliza se expide y se asocia';
COMMENT ON COLUMN amparo_poliza.amparo_id IS 'Parámetros CRUD, tipo 118 Amparo';
COMMENT ON COLUMN amparo_poliza.tipo_valor_amparo_id IS 'Parámetros CRUD, tipo de valor de la suficiencia (porcentaje o SMLV; tipo de parámetro por confirmar)';
COMMENT ON COLUMN amparo_poliza.suficiencia IS 'Suficiencia del amparo. Se interpreta según tipo_valor_amparo_id; excepción a numeric(5,4) documentada en la #351';
COMMENT ON COLUMN amparo_poliza.valor IS 'Valor asegurado del amparo';
COMMENT ON COLUMN amparo_poliza.descripcion IS 'Descripción del amparo';
COMMENT ON COLUMN amparo_poliza.fecha_inicio IS 'Inicio de vigencia del amparo';
COMMENT ON COLUMN amparo_poliza.fecha_fin IS 'Fin de vigencia del amparo';
COMMENT ON COLUMN amparo_poliza.usuario_id IS 'Identificador del usuario que registra o modifica el amparo';
COMMENT ON COLUMN amparo_poliza.usuario_rol IS 'Rol del usuario que registra o modifica el amparo';

-- ---------------------------------------------------------------------
-- Documentos y actas
-- ---------------------------------------------------------------------

CREATE TABLE documento_contrato (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    tipo_documento_id               integer,
    documento_id                    integer,
    documento_enlace                varchar(50),
    usuario_id                      integer,
    usuario_rol                     varchar(40),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_documento_contrato PRIMARY KEY (id),
    CONSTRAINT fk_documento_contrato_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_documento_contrato_contrato_general_id ON documento_contrato (contrato_general_id);

COMMENT ON TABLE documento_contrato IS 'Documentos del contrato en una sola tabla, sin estados (A9 "con ajustes"; supuesto S6)';
COMMENT ON COLUMN documento_contrato.tipo_documento_id IS 'Parámetros CRUD, tipo de documento (tipo 133 Documentos Contrato)';
COMMENT ON COLUMN documento_contrato.documento_id IS 'Gestor Documental, identificador del documento';
COMMENT ON COLUMN documento_contrato.documento_enlace IS 'Gestor Documental, enlace del documento';
COMMENT ON COLUMN documento_contrato.usuario_id IS 'Identificador del usuario que registra el documento';
COMMENT ON COLUMN documento_contrato.usuario_rol IS 'Rol del usuario que registra el documento';

CREATE TABLE acta_inicio (
    id                              serial          NOT NULL,
    contrato_general_id             integer         NOT NULL,
    descripcion                     varchar(2000),
    fecha_inicio                    date,
    fecha_fin                       date,
    fecha_suscripcion               date,
    numero_acta                     varchar(50),
    valor_disponibilidad            numeric(20,7),
    numero_registro_presupuestal    varchar(50),
    valor_registro_presupuestal     numeric(20,7),
    valor_anticipo                  numeric(20,7),
    nombre_interventor              varchar(250),
    usuario_id                      integer,
    usuario_rol                     varchar(40),
    usuario_legado                  varchar(15),
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_acta_inicio PRIMARY KEY (id),
    CONSTRAINT fk_acta_inicio_contrato_general FOREIGN KEY (contrato_general_id) REFERENCES contrato_general (id)
);

CREATE INDEX idx_acta_inicio_contrato_general_id ON acta_inicio (contrato_general_id);

COMMENT ON TABLE acta_inicio IS 'Acta con la que inicia la ejecución del contrato';
COMMENT ON COLUMN acta_inicio.descripcion IS 'Descripción del acta de inicio';
COMMENT ON COLUMN acta_inicio.fecha_inicio IS 'Fecha de inicio de ejecución del contrato';
COMMENT ON COLUMN acta_inicio.fecha_fin IS 'Fecha prevista de finalización del contrato';
COMMENT ON COLUMN acta_inicio.fecha_suscripcion IS 'Fecha de suscripción del acta de inicio (no la del contrato). Supuesto S2';
COMMENT ON COLUMN acta_inicio.numero_acta IS 'Número del acta de inicio. Supuesto S2';
COMMENT ON COLUMN acta_inicio.valor_disponibilidad IS 'Valor del CDP registrado en el acta. Duplica información de disponibilidad_presupuestal (supuesto S2)';
COMMENT ON COLUMN acta_inicio.numero_registro_presupuestal IS 'Número del RP digitado en el acta. Duplica información de registro_presupuestal (supuesto S2)';
COMMENT ON COLUMN acta_inicio.valor_registro_presupuestal IS 'Valor del RP registrado en el acta. Supuesto S2';
COMMENT ON COLUMN acta_inicio.valor_anticipo IS 'Valor del anticipo del contrato. Supuesto S2';
COMMENT ON COLUMN acta_inicio.nombre_interventor IS 'Nombre del interventor, cuando aplica. Supuesto S2';
COMMENT ON COLUMN acta_inicio.usuario_id IS 'Identificador del usuario que registra el acta';
COMMENT ON COLUMN acta_inicio.usuario_rol IS 'Rol del usuario que registra el acta';
COMMENT ON COLUMN acta_inicio.usuario_legado IS 'Usuario de ARGO v1, para compatibilidad con la migración';

-- ---------------------------------------------------------------------
-- Unidad ejecutora
-- ---------------------------------------------------------------------

CREATE TABLE parametro_unidad_ejecutora (
    id                              serial          NOT NULL,
    parametro_id                    integer         NOT NULL,
    unidad_ejecutora_id             integer         NOT NULL,
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_parametro_unidad_ejecutora PRIMARY KEY (id),
    CONSTRAINT uq_parametro_id_unidad_ejecutora_id_parametro_unidad_ejecutora UNIQUE (parametro_id, unidad_ejecutora_id)
);

CREATE INDEX idx_parametro_unidad_ejecutora_unidad_ejecutora_id ON parametro_unidad_ejecutora (unidad_ejecutora_id);

COMMENT ON TABLE parametro_unidad_ejecutora IS 'Valores paramétricos que aplican a cada unidad ejecutora (propuesta del 21/10, supuesto S4). Sin registro significa que no aplica';
COMMENT ON COLUMN parametro_unidad_ejecutora.parametro_id IS 'Parámetros CRUD, parametros.parametro.id (otra BD, sin FK física)';
COMMENT ON COLUMN parametro_unidad_ejecutora.unidad_ejecutora_id IS 'Parámetros CRUD, tipo 146 Unidad Ejecutora';

CREATE TABLE configuracion_unidad_ejecutora (
    id                              serial          NOT NULL,
    unidad_ejecutora_id             integer         NOT NULL,
    prefijo_numero_contrato         varchar(10)     NOT NULL DEFAULT '',
    sufijo_numero_contrato          varchar(10)     NOT NULL DEFAULT '',
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_configuracion_unidad_ejecutora PRIMARY KEY (id),
    CONSTRAINT uq_unidad_ejecutora_id_configuracion_unidad_ejecutora UNIQUE (unidad_ejecutora_id)
);

COMMENT ON TABLE configuracion_unidad_ejecutora IS 'Formato del número de contrato por unidad ejecutora; reemplaza conf.ts del MID (propuesta del 21/10, supuesto S4)';
COMMENT ON COLUMN configuracion_unidad_ejecutora.unidad_ejecutora_id IS 'Parámetros CRUD, tipo 146 Unidad Ejecutora';
COMMENT ON COLUMN configuracion_unidad_ejecutora.prefijo_numero_contrato IS 'Prefijo del número de contrato (hoy Rectoría vacío, IDEXUD "ID-")';
COMMENT ON COLUMN configuracion_unidad_ejecutora.sufijo_numero_contrato IS 'Sufijo del número de contrato (hoy vacío en ambas)';

-- ---------------------------------------------------------------------
-- Auditoría
-- ---------------------------------------------------------------------

CREATE TABLE huella_navegador (
    id                              serial          NOT NULL,
    huella                          varchar(64)     NOT NULL,
    libreria                        varchar(50)     NOT NULL,
    version_libreria                varchar(20)     NOT NULL,
    confianza                       numeric(5,4),
    componentes                     jsonb,
    direccion_ip                    varchar(45),
    direccion_ip_servidor           varchar(45),
    user_agent                      varchar(512)    NOT NULL,
    usuario_id                      integer,
    usuario_rol                     varchar(40),
    microcliente                    varchar(100)    NOT NULL,
    ruta                            varchar(255),
    fecha_captura                   timestamp       NOT NULL,
    activo                          boolean         NOT NULL DEFAULT true,
    fecha_creacion                  timestamp       NOT NULL DEFAULT now(),
    fecha_modificacion              timestamp       NOT NULL DEFAULT now(),
    CONSTRAINT pk_huella_navegador PRIMARY KEY (id)
);

CREATE INDEX idx_huella_navegador_huella ON huella_navegador (huella);
CREATE INDEX idx_huella_navegador_usuario_id ON huella_navegador (usuario_id);

COMMENT ON TABLE huella_navegador IS 'Huella digital del navegador e IP para auditoría (#376, PR gestion_contractual_crud#49; supuesto S8)';
COMMENT ON COLUMN huella_navegador.huella IS 'Identificador calculado por la librería de fingerprinting';
COMMENT ON COLUMN huella_navegador.libreria IS 'Librería con la que se calculó la huella';
COMMENT ON COLUMN huella_navegador.version_libreria IS 'Versión de la librería';
COMMENT ON COLUMN huella_navegador.confianza IS 'Puntaje de confianza entre 0 y 1. Nulo si la librería no lo entrega';
COMMENT ON COLUMN huella_navegador.componentes IS 'Componentes como hash SHA-256 truncado, duración y error. No guarda valores crudos';
COMMENT ON COLUMN huella_navegador.direccion_ip IS 'IP pública reportada por el cliente';
COMMENT ON COLUMN huella_navegador.direccion_ip_servidor IS 'IP con la que llega la petición al servidor';
COMMENT ON COLUMN huella_navegador.user_agent IS 'User agent del navegador';
COMMENT ON COLUMN huella_navegador.usuario_id IS 'Identificador del usuario autenticado al capturar la huella';
COMMENT ON COLUMN huella_navegador.usuario_rol IS 'Rol del usuario autenticado al capturar la huella';
COMMENT ON COLUMN huella_navegador.microcliente IS 'Microcliente que capturó la huella';
COMMENT ON COLUMN huella_navegador.ruta IS 'Ruta de la página, sin query string';
COMMENT ON COLUMN huella_navegador.fecha_captura IS 'Fecha y hora de la captura en el navegador';
