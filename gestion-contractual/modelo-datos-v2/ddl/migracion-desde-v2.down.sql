-- =====================================================================
-- ARGO v2 · Reverso de migracion-desde-v2.up.sql (#384)
-- Devuelve el esquema al DDL de gestion_contractual_crud (develop 9e20927).
--
-- Datos: contratista y lugar_ejecucion se recrean a partir de las columnas
-- absorbidas en contrato_general (un registro por contrato con datos). Los
-- id, activo y fechas originales de esas filas no se recuperan. Se pierden
-- los datos de las columnas y tablas que no existen en develop
-- (fecha_suscripcion, usuario_rol, estado_poliza_id, columnas nuevas de
-- acta_inicio, parametro_unidad_ejecutora, configuracion_unidad_ejecutora
-- y huella_navegador).
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. Tablas nuevas
-- ---------------------------------------------------------------------

DROP TABLE huella_navegador;
DROP TABLE configuracion_unidad_ejecutora;
DROP TABLE parametro_unidad_ejecutora;

-- ---------------------------------------------------------------------
-- 2. Índices y restricciones a sus nombres originales
-- ---------------------------------------------------------------------

DROP INDEX idx_contrato_general_unidad_ejecutora_id;
DROP INDEX idx_solicitante_contrato_general_id;
DROP INDEX idx_supervisor_contrato_contrato_general_id;
DROP INDEX idx_ordenador_contrato_contrato_general_id;
DROP INDEX idx_convenio_contrato_general_id;
DROP INDEX idx_especificacion_tecnica_contrato_general_id;
DROP INDEX idx_registro_presupuestal_disponibilidad_presupuestal_id;
DROP INDEX idx_acta_inicio_contrato_general_id;

ALTER INDEX idx_contrato_general_tipo_contrato_id RENAME TO idx_contrato_general_tipo_contrato;
ALTER INDEX idx_documento_contrato_contrato_general_id RENAME TO idx_documento_contrato_contrato;
ALTER INDEX idx_estado_contrato_contrato_general_id RENAME TO idx_estado_contrato_contrato;
ALTER INDEX idx_supervisor_contrato_supervisor_id RENAME TO idx_supervisor_contrato_supervisor;
ALTER INDEX idx_disponibilidad_presupuestal_contrato_general_id RENAME TO idx_disponibilidad_presupuestal_contrato;
ALTER INDEX idx_poliza_contrato_general_id RENAME TO idx_poliza_contrato_general;
ALTER INDEX idx_amparo_poliza_contrato_general_id RENAME TO idx_amparo_poliza_contrato_general;
ALTER INDEX idx_amparo_poliza_poliza_id RENAME TO idx_amparo_poliza_poliza;

ALTER TABLE contrato_general DROP CONSTRAINT uq_numero_contrato_vigencia_contrato_general;
ALTER TABLE contrato_arrendamiento RENAME CONSTRAINT uq_contrato_general_id_contrato_arrendamiento TO contrato_arrendamiento_contrato_general_id_key;

ALTER TABLE estado_contrato RENAME CONSTRAINT fk_estado_contrato_contrato_general TO estado_contrato_contrato_general_id_fkey;
ALTER TABLE solicitante RENAME CONSTRAINT fk_solicitante_contrato_general TO solicitante_contrato_general_id_fkey;
ALTER TABLE supervisor_contrato RENAME CONSTRAINT fk_supervisor_contrato_contrato_general TO supervisor_contrato_contrato_general_id_fkey;
ALTER TABLE ordenador_contrato RENAME CONSTRAINT fk_ordenador_contrato_contrato_general TO ordenador_contrato_contrato_general_id_fkey;
ALTER TABLE contrato_arrendamiento RENAME CONSTRAINT fk_contrato_arrendamiento_contrato_general TO contrato_arrendamiento_contrato_general_id_fkey;
ALTER TABLE convenio RENAME CONSTRAINT fk_convenio_contrato_general TO convenio_contrato_general_id_fkey;
ALTER TABLE especificacion_tecnica RENAME CONSTRAINT fk_especificacion_tecnica_contrato_general TO especificacion_tecnica_contrato_general_id_fkey;
ALTER TABLE disponibilidad_presupuestal RENAME CONSTRAINT fk_disponibilidad_presupuestal_contrato_general TO disponibilidad_presupuestal_contrato_general_id_fkey;
ALTER TABLE registro_presupuestal RENAME CONSTRAINT fk_registro_presupuestal_disponibilidad_presupuestal TO registro_presupuestal_cdp_id_fkey;
ALTER TABLE poliza RENAME CONSTRAINT fk_poliza_contrato_general TO poliza_contrato_general_id_fkey;
ALTER TABLE amparo_poliza RENAME CONSTRAINT fk_amparo_poliza_contrato_general TO amparo_poliza_contrato_general_id_fkey;
ALTER TABLE amparo_poliza RENAME CONSTRAINT fk_amparo_poliza_poliza TO amparo_poliza_poliza_id_fkey;
ALTER TABLE documento_contrato RENAME CONSTRAINT fk_documento_contrato_contrato_general TO documento_contrato_contrato_general_id_fkey;
ALTER TABLE acta_inicio RENAME CONSTRAINT fk_acta_inicio_contrato_general TO acta_inicio_contrato_general_id_fkey;

ALTER TABLE contrato_general RENAME CONSTRAINT pk_contrato_general TO contrato_general_pkey;
ALTER TABLE estado_contrato RENAME CONSTRAINT pk_estado_contrato TO estado_contrato_pkey;
ALTER TABLE solicitante RENAME CONSTRAINT pk_solicitante TO solicitante_pkey;
ALTER TABLE supervisor_contrato RENAME CONSTRAINT pk_supervisor_contrato TO supervisor_contrato_pkey;
ALTER TABLE ordenador_contrato RENAME CONSTRAINT pk_ordenador_contrato TO ordenador_contrato_pkey;
ALTER TABLE contrato_arrendamiento RENAME CONSTRAINT pk_contrato_arrendamiento TO contrato_arrendamiento_pkey;
ALTER TABLE convenio RENAME CONSTRAINT pk_convenio TO convenio_pkey;
ALTER TABLE especificacion_tecnica RENAME CONSTRAINT pk_especificacion_tecnica TO especificacion_tecnica_pkey;
ALTER TABLE disponibilidad_presupuestal RENAME CONSTRAINT pk_disponibilidad_presupuestal TO disponibilidad_presupuestal_pkey;
ALTER TABLE registro_presupuestal RENAME CONSTRAINT pk_registro_presupuestal TO registro_presupuestal_pkey;
ALTER TABLE poliza RENAME CONSTRAINT pk_poliza TO poliza_pkey;
ALTER TABLE amparo_poliza RENAME CONSTRAINT pk_amparo_poliza TO amparo_poliza_pkey;
ALTER TABLE documento_contrato RENAME CONSTRAINT pk_documento_contrato TO documento_contrato_pkey;
ALTER TABLE acta_inicio RENAME CONSTRAINT pk_acta_inicio TO acta_inicio_pkey;

-- ---------------------------------------------------------------------
-- 3. Columnas de auditoría y unidad_ejecutora_id como estaban en develop
-- ---------------------------------------------------------------------

ALTER TABLE contrato_general ALTER COLUMN unidad_ejecutora_id DROP NOT NULL;

-- En develop solo estado_contrato, poliza y amparo_poliza tenían valores por defecto.
DO $$
DECLARE
    t text;
BEGIN
    FOREACH t IN ARRAY ARRAY['contrato_general', 'solicitante', 'supervisor_contrato',
        'ordenador_contrato', 'contrato_arrendamiento', 'convenio', 'especificacion_tecnica',
        'disponibilidad_presupuestal', 'registro_presupuestal', 'documento_contrato', 'acta_inicio']
    LOOP
        EXECUTE format('ALTER TABLE %I
            ALTER COLUMN activo DROP DEFAULT,
            ALTER COLUMN fecha_creacion DROP DEFAULT,
            ALTER COLUMN fecha_modificacion DROP DEFAULT', t);
    END LOOP;
END
$$;

ALTER TABLE estado_contrato ALTER COLUMN activo SET DEFAULT true;
ALTER TABLE disponibilidad_presupuestal ALTER COLUMN activo DROP NOT NULL;
ALTER TABLE solicitante ALTER COLUMN fecha_modificacion DROP NOT NULL;
ALTER TABLE supervisor_contrato ALTER COLUMN fecha_modificacion DROP NOT NULL;
ALTER TABLE ordenador_contrato ALTER COLUMN fecha_modificacion DROP NOT NULL;

-- ---------------------------------------------------------------------
-- 4. Tipos originales
-- ---------------------------------------------------------------------

ALTER TABLE contrato_general
    ALTER COLUMN valor_pesos TYPE numeric(16,2),
    ALTER COLUMN valor_contrato_me TYPE numeric(16,3),
    ALTER COLUMN valor_tasa_cambio TYPE numeric(16,10),
    ALTER COLUMN modo_pago TYPE varchar,
    ALTER COLUMN objeto TYPE varchar,
    ALTER COLUMN justificacion TYPE varchar,
    ALTER COLUMN actividades TYPE varchar,
    ALTER COLUMN condiciones TYPE varchar;

ALTER TABLE supervisor_contrato ALTER COLUMN cargo_legado TYPE varchar;

ALTER TABLE ordenador_contrato
    ALTER COLUMN resolucion TYPE varchar,
    ALTER COLUMN documento_identidad TYPE varchar;

ALTER TABLE contrato_arrendamiento
    ALTER COLUMN destinacion TYPE varchar,
    ALTER COLUMN valor_administracion TYPE numeric(16,2),
    ALTER COLUMN valor_arrendamiento TYPE numeric(16,2);

ALTER TABLE especificacion_tecnica
    ALTER COLUMN descripcion TYPE varchar,
    ALTER COLUMN valor_unitario TYPE numeric(16,2),
    ALTER COLUMN valor_total TYPE numeric(16,2);

ALTER TABLE acta_inicio ALTER COLUMN descripcion TYPE varchar;

-- ---------------------------------------------------------------------
-- 5. Nombres de columnas originales
-- ---------------------------------------------------------------------

ALTER TABLE solicitante RENAME COLUMN dependencia_id TO dependencia_solicitante_id;
ALTER TABLE solicitante RENAME COLUMN sede_id TO sede_solicitante_id;
ALTER TABLE registro_presupuestal RENAME COLUMN disponibilidad_presupuestal_id TO cdp_id;
ALTER TABLE registro_presupuestal RENAME COLUMN numero_registro_presupuestal TO registro_presupuestal;

-- ---------------------------------------------------------------------
-- 6. Columnas nuevas
-- ---------------------------------------------------------------------

ALTER TABLE acta_inicio
    DROP COLUMN fecha_suscripcion,
    DROP COLUMN numero_acta,
    DROP COLUMN valor_disponibilidad,
    DROP COLUMN numero_registro_presupuestal,
    DROP COLUMN valor_registro_presupuestal,
    DROP COLUMN valor_anticipo,
    DROP COLUMN nombre_interventor,
    DROP COLUMN usuario_rol;

ALTER TABLE documento_contrato DROP COLUMN usuario_id, DROP COLUMN usuario_rol;
ALTER TABLE amparo_poliza DROP COLUMN usuario_id, DROP COLUMN usuario_rol;
ALTER TABLE poliza DROP COLUMN estado_poliza_id, DROP COLUMN usuario_rol;
ALTER TABLE contrato_general DROP COLUMN usuario_id, DROP COLUMN usuario_rol;

-- ---------------------------------------------------------------------
-- 7. lugar_ejecucion y contratista, recreadas desde contrato_general
-- (mismo DDL de develop)
-- ---------------------------------------------------------------------

CREATE TABLE lugar_ejecucion (
    id SERIAL PRIMARY KEY,
    pais_id INTEGER,
    ciudad_id INTEGER,
    municipio_id INTEGER,
    dependencia_id INTEGER,
    sede_id INTEGER,
    direccion VARCHAR(150),
    contrato_general_id INTEGER REFERENCES contrato_general(id),
    activo BOOLEAN NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL,
    fecha_modificacion TIMESTAMP
);

INSERT INTO lugar_ejecucion (pais_id, ciudad_id, municipio_id, dependencia_id, sede_id, direccion,
                             contrato_general_id, activo, fecha_creacion, fecha_modificacion)
SELECT lugar_ejecucion_pais_id, lugar_ejecucion_ciudad_id, lugar_ejecucion_municipio_id,
       lugar_ejecucion_dependencia_id, lugar_ejecucion_sede_id, lugar_ejecucion_direccion,
       id, true, now(), now()
FROM contrato_general
WHERE COALESCE(lugar_ejecucion_pais_id, lugar_ejecucion_ciudad_id, lugar_ejecucion_municipio_id,
               lugar_ejecucion_dependencia_id, lugar_ejecucion_sede_id) IS NOT NULL
   OR lugar_ejecucion_direccion IS NOT NULL
ORDER BY id;

ALTER TABLE contrato_general
    DROP COLUMN lugar_ejecucion_pais_id,
    DROP COLUMN lugar_ejecucion_ciudad_id,
    DROP COLUMN lugar_ejecucion_municipio_id,
    DROP COLUMN lugar_ejecucion_dependencia_id,
    DROP COLUMN lugar_ejecucion_sede_id,
    DROP COLUMN lugar_ejecucion_direccion;

CREATE TABLE contratista (
    id SERIAL PRIMARY KEY,
    numero_documento VARCHAR(20),
    tipo_persona_id INTEGER,
    contrato_general_id INTEGER REFERENCES contrato_general(id),
    clase_contratista_id INTEGER,
    activo BOOLEAN NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL,
    fecha_modificacion TIMESTAMP
);

INSERT INTO contratista (numero_documento, tipo_persona_id, contrato_general_id, clase_contratista_id,
                         activo, fecha_creacion, fecha_modificacion)
SELECT proveedor_numero_documento, tipo_persona_id, id, clase_proveedor_id, true, now(), now()
FROM contrato_general
WHERE proveedor_numero_documento IS NOT NULL OR tipo_persona_id IS NOT NULL OR clase_proveedor_id IS NOT NULL
ORDER BY id;

ALTER TABLE contrato_general
    DROP COLUMN fecha_suscripcion,
    DROP COLUMN proveedor_numero_documento,
    DROP COLUMN tipo_persona_id,
    DROP COLUMN clase_proveedor_id;

-- ---------------------------------------------------------------------
-- 8. Comentarios originales de develop
-- ---------------------------------------------------------------------

DO $$
DECLARE
    r record;
BEGIN
    FOR r IN
        SELECT c.relname, a.attname
        FROM pg_class c
        JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
        WHERE c.relnamespace = current_schema()::regnamespace AND c.relkind = 'r'
          AND col_description(c.oid, a.attnum) IS NOT NULL
    LOOP
        EXECUTE format('COMMENT ON COLUMN %I.%I IS NULL', r.relname, r.attname);
    END LOOP;
END
$$;

-- inicio comentarios (generado por scripts/sincroniza_comentarios.py desde gestion_contractual_crud develop sql/creacion-tablas.sql)
COMMENT ON TABLE contrato_general IS 'Tabla principal que almacena la información básica de los contratos';
COMMENT ON COLUMN contrato_general.tipo_compromiso_id IS 'Identificador del tipo de compromiso en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.tipo_contrato_id IS 'Identificador del tipo de contrato en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.perfil_contratista_id IS 'Identificador del perfil del contratista en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.fecha_suscripcion_estudio IS 'Fecha de suscripcion de estudio documento previo';
COMMENT ON COLUMN contrato_general.aplica_poliza IS 'Campo que indica si Aplica Póliza para la orden de compra o servicio';
COMMENT ON COLUMN contrato_general.modalidad_seleccion_id IS 'Identificador de modalidad de selección en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.tipo_control_id IS 'Identificador de tipo de control en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.tipologia_especifica_id IS 'Identificador de tipología específica en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.regimen_contratacion_id IS 'Identificador de regimen de contratación en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.procedimiento_id IS 'Identificador de prodedimiento en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.plazo_ejecucion IS 'Numero relacionado con Unidad Ejecución Id para determinar duración del contrato (1,2,4 MES, DIA, AÑo)';
COMMENT ON COLUMN contrato_general.unidad_ejecutora_id IS 'Id Unidad Ejecutora en Parámetros CRUD (Rectoría, IDEXUD)';
COMMENT ON COLUMN contrato_general.tipo_moneda_id IS 'Identificador de tipo de moneda en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.valor_pesos IS 'Valor del contrato en Pesos';
COMMENT ON COLUMN contrato_general.tipo_gasto_id IS 'Identificador de tipo de gasto en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.origen_recursos_id IS 'Identificador de origen de recursos en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.origen_presupuesto_id IS 'Identificador de origen de presupuesto en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.tema_gasto_inversion_id IS 'Identificador de tema gasto inversión en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.valor_contrato_me IS 'Valor del contrato en Moneda Extranjera';
COMMENT ON COLUMN contrato_general.valor_tasa_cambio IS 'Valor de Tasa de Cambio asociado al contrato';
COMMENT ON COLUMN contrato_general.medio_pago_id IS 'Identificador de medio de pago en Parámetros CRUD';
COMMENT ON COLUMN contrato_general.clausula_registro_presupuestal IS 'Booleano que determina si el contrato requiere cláusula adicional de registro presupuestal';
COMMENT ON COLUMN contrato_general.modo_pago IS 'Campo para especificar el modo de pago asociado al contrato';
COMMENT ON COLUMN contrato_general.objeto IS 'Campo para especificar el objeto del contrato';
COMMENT ON COLUMN contrato_general.justificacion IS 'Campo para especificar la justificacion del contrato';
COMMENT ON COLUMN contrato_general.actividades IS 'Campo para especificar las actividades del contrato, se mantienen en un campo dado que desde la fuente están unificadas';
COMMENT ON COLUMN contrato_general.condiciones IS 'Campo para especificar las condiciones del contrato';
COMMENT ON COLUMN contrato_general.observaciones IS 'Campo para especificar las observaciones del contrato';
COMMENT ON COLUMN contrato_general.vigencia IS 'Año vigencia del contato (2024, 2025, etc)';
COMMENT ON COLUMN contrato_general.consecutivo_elaboracion IS 'Campo Legado, usado para compatibilidad con la migración de ARGO v1';
COMMENT ON COLUMN contrato_general.fecha_inicial IS 'Fecha Inicio del Contrato';
COMMENT ON COLUMN contrato_general.fecha_final IS 'Fecha Finalización del Contrato';
COMMENT ON COLUMN contrato_general.usuario_legado IS 'Campo Legado, usado para compatibilidad con la migración de ARGO v1';
COMMENT ON COLUMN contrato_general.numero_contrato IS 'Campo Legado, usado para compatibilidad con la migración de ARGO v1';
COMMENT ON COLUMN contrato_general.unidad_ejecucion_id IS 'Identificador de unidad de ejecución (Dia, Mes, Año) en Parámetros CRUD';
COMMENT ON TABLE documento_contrato IS 'Almacena los documentos asociados a cada contrato';
COMMENT ON COLUMN documento_contrato.tipo_documento_id IS 'Tipo de documento (p.ej. minuta, otros) según Parámetros CRUD';
COMMENT ON COLUMN documento_contrato.contrato_general_id IS 'Referencia del contrato general';
COMMENT ON COLUMN documento_contrato.documento_enlace IS 'Enlace asociado al Gestor Documental';
COMMENT ON COLUMN documento_contrato.documento_id IS 'Id asociado al Gestor Documental';
COMMENT ON TABLE estado_contrato IS 'Registra el historial de estados por los que pasa un contrato';
COMMENT ON COLUMN estado_contrato.motivo IS 'Razón del cambio de estado del contrato';
COMMENT ON COLUMN estado_contrato.contrato_general_id IS 'Referencia del contrato general';
COMMENT ON COLUMN estado_contrato.estado_parametro_id IS 'Tipo de cambio de estado según Parámetros CRUD';
COMMENT ON COLUMN estado_contrato.estado_interno_parametro_id IS 'Tipo de cambio de estado interno (Estados propios de ARGO) según Parámetros CRUD';
COMMENT ON COLUMN estado_contrato.actual IS 'Campo que permite buscar el estado actual de un contrato';
COMMENT ON COLUMN estado_contrato.usuario_rol IS 'Rol del Usuario que Efectua el cambio de estado';
COMMENT ON COLUMN estado_contrato.fecha_evento IS 'Fecha en la que se asocia el cambio de estado';
COMMENT ON TABLE solicitante IS 'Información de la dependencia o área que solicita el contrato';
COMMENT ON COLUMN solicitante.dependencia_solicitante_id IS 'Identificador de la dependencia que solicita el contrato, referencia OIKOS';
COMMENT ON COLUMN solicitante.sede_solicitante_id IS 'Identificador de la sede donde se origina la solicitud, referencia OIKOS';
COMMENT ON COLUMN solicitante.contrato_general_id IS 'Referencia del contrato general';
COMMENT ON TABLE lugar_ejecucion IS 'Especifica la ubicación donde se ejecutará el contrato';
COMMENT ON COLUMN lugar_ejecucion.pais_id IS 'País donde se ejecutará el contrato';
COMMENT ON COLUMN lugar_ejecucion.ciudad_id IS 'Ciudad donde se ejecutará el contrato';
COMMENT ON COLUMN lugar_ejecucion.municipio_id IS 'Municipio donde se ejecutará el contrato';
COMMENT ON COLUMN lugar_ejecucion.dependencia_id IS 'Identificador de la dependencia del lugar de ejecución, referencia OIKOS';
COMMENT ON COLUMN lugar_ejecucion.sede_id IS 'Identificador de la sede del lugar de ejecución, referencia OIKOS';
COMMENT ON COLUMN lugar_ejecucion.direccion IS 'Dirección física donde se ejecutará el contrato';
COMMENT ON TABLE supervisor_contrato IS 'Registro de supervisores asignados a cada contrato';
COMMENT ON COLUMN supervisor_contrato.supervisor_id IS 'Identificador del funcionario que ejerce como supervisor en terceros crud';
COMMENT ON COLUMN supervisor_contrato.sede_legado IS 'Identificador de la sede de la tabla de sedes_SIC del ARGO v1';
COMMENT ON COLUMN supervisor_contrato.dependencia_legado IS 'Identificador de la dependencia de la tabla de dependencias_SIC del ARGO v1';
COMMENT ON COLUMN supervisor_contrato.cargo_legado IS 'Identificador del cargo de la tabla de supervisores del ARGO v1';
COMMENT ON COLUMN supervisor_contrato.cargo_id IS 'Identificador del cargo de paramétros crud';
COMMENT ON COLUMN supervisor_contrato.documento IS 'Documento del funcionario que ejerce como supervisor';
COMMENT ON COLUMN supervisor_contrato.digito_verificacion IS 'Dígito de verificación del funcionario que ejerce como supervisor';
COMMENT ON COLUMN supervisor_contrato.sede_id IS 'Identificador de la sede en OIKOS';
COMMENT ON COLUMN supervisor_contrato.dependencia_id IS 'Identificador de la dependencia en OIKOS';
COMMENT ON TABLE disponibilidad_presupuestal IS 'Certificados de Disponibilidad Presupuestal asociados a los contratos';
COMMENT ON COLUMN disponibilidad_presupuestal.numero_cdp_id IS 'Número único del CDP';
COMMENT ON COLUMN disponibilidad_presupuestal.vigencia_cdp IS 'Año de vigencia del CDP';
COMMENT ON TABLE registro_presupuestal IS 'Registros presupuestales asociados a los CDP';
COMMENT ON COLUMN registro_presupuestal.registro_presupuestal IS 'Número de disponibilidad presupuestal';
COMMENT ON COLUMN registro_presupuestal.vigencia_rp IS 'Año de vigencia del registro presupuestal';
COMMENT ON COLUMN registro_presupuestal.fecha_registro IS 'Fecha registro RP';
COMMENT ON TABLE contrato_arrendamiento IS 'Información específica para contratos de tipo arrendamiento, principalmente para migración';
COMMENT ON COLUMN contrato_arrendamiento.destinacion IS 'Uso previsto del inmueble arrendado';
COMMENT ON COLUMN contrato_arrendamiento.plazo_pago_mensual IS 'Día del mes establecido para el pago';
COMMENT ON COLUMN contrato_arrendamiento.valor_arrendamiento IS 'Valor mensual del arrendamiento';
COMMENT ON TABLE contratista IS 'Información de los contratistas';
COMMENT ON COLUMN contratista.numero_documento IS 'Número de identificación del contratista';
COMMENT ON COLUMN contratista.tipo_persona_id IS 'Tipo de persona (natural o jurídica)';
COMMENT ON TABLE convenio IS 'Información específica para contratos de tipo convenio';
COMMENT ON COLUMN convenio.vigencia IS 'Año de vigencia del convenio';
COMMENT ON COLUMN convenio.tipo_convenio_id IS 'Tipo de convenio (marco, específico, etc.)';
COMMENT ON TABLE especificacion_tecnica IS 'Detalles técnicos y económicos de los items del contrato';
COMMENT ON COLUMN especificacion_tecnica.descripcion IS 'Descripción detallada del item o servicio';
COMMENT ON COLUMN especificacion_tecnica.cantidad IS 'Cantidad de items';
COMMENT ON COLUMN especificacion_tecnica.valor_unitario IS 'Valor unitario del item';
COMMENT ON COLUMN especificacion_tecnica.valor_total IS 'Valor total del item';
COMMENT ON TABLE acta_inicio IS 'Registro de las actas de inicio de los contratos';
COMMENT ON COLUMN acta_inicio.descripcion IS 'Descripción del acta de inicio';
COMMENT ON COLUMN acta_inicio.fecha_inicio IS 'Fecha de inicio de ejecución del contrato';
COMMENT ON COLUMN acta_inicio.fecha_fin IS 'Fecha prevista de finalización del contrato';
COMMENT ON TABLE ordenador_contrato IS 'Información de los ordenadores de gasto para cada contrato';
COMMENT ON COLUMN ordenador_contrato.tercero_id IS 'Identificador del tercero que actúa como ordenador, referencia a terceros crud';
COMMENT ON COLUMN ordenador_contrato.ordenador_argo_id IS 'Referencia al id PK de la tabla ordenadores ARGO v1';
COMMENT ON COLUMN ordenador_contrato.ordenador_sicapital_id IS 'Referencia al id_ordenador de la tabla ordenadores ARGO v1';
COMMENT ON COLUMN ordenador_contrato.resolucion IS 'Número de resolución que autoriza al ordenador';
COMMENT ON COLUMN ordenador_contrato.documento_identidad IS 'Número de documento de identidad del ordenador';
COMMENT ON COLUMN ordenador_contrato.cargo_id IS 'Cargo del ordenador';
COMMENT ON TABLE poliza IS 'Pólizas expedidas para el cumplimiento de las garantías de un contrato';
COMMENT ON COLUMN poliza.numero_poliza IS 'Número con el que la aseguradora identifica la póliza';
COMMENT ON COLUMN poliza.entidad_aseguradora_id IS 'Identificador de la entidad aseguradora en Parámetros CRUD';
COMMENT ON COLUMN poliza.contrato_general_id IS 'Referencia del contrato general que ampara la póliza';
COMMENT ON COLUMN poliza.descripcion IS 'Descripción de la póliza';
COMMENT ON COLUMN poliza.fecha_inicio IS 'Fecha de inicio de vigencia de la póliza';
COMMENT ON COLUMN poliza.fecha_fin IS 'Fecha de finalización de vigencia de la póliza';
COMMENT ON COLUMN poliza.fecha_expedicion IS 'Fecha en la que la aseguradora expide la póliza';
COMMENT ON COLUMN poliza.fecha_aprobacion IS 'Fecha en la que la Universidad aprueba la póliza';
COMMENT ON COLUMN poliza.usuario_id IS 'Identificador del usuario que registra la póliza';
COMMENT ON COLUMN poliza.usuario_legado IS 'Campo Legado, usado para compatibilidad con la migración de ARGO v1';
COMMENT ON TABLE amparo_poliza IS 'Amparos que cubren un contrato. Se registran durante la elaboración de la minuta y posteriormente se asocian a la póliza expedida';
COMMENT ON COLUMN amparo_poliza.contrato_general_id IS 'Referencia del contrato general al que pertenece el amparo. Se registra antes de que exista la póliza';
COMMENT ON COLUMN amparo_poliza.poliza_id IS 'Referencia de la póliza que cubre el amparo. Es nula hasta que la póliza es expedida y asociada';
COMMENT ON COLUMN amparo_poliza.amparo_id IS 'Tipo de amparo según Parámetros CRUD';
COMMENT ON COLUMN amparo_poliza.tipo_valor_amparo_id IS 'Tipo de valor de la suficiencia según Parámetros CRUD (porcentaje, SMLV, etc.)';
COMMENT ON COLUMN amparo_poliza.suficiencia IS 'Valor numérico de la suficiencia del amparo. Se interpreta según tipo_valor_amparo_id (porcentaje o SMLV), por lo que no usa la escala de porcentaje del lineamiento';
COMMENT ON COLUMN amparo_poliza.valor IS 'Valor asegurado del amparo';
COMMENT ON COLUMN amparo_poliza.descripcion IS 'Descripción del amparo';
COMMENT ON COLUMN amparo_poliza.fecha_inicio IS 'Fecha de inicio de vigencia del amparo';
COMMENT ON COLUMN amparo_poliza.fecha_fin IS 'Fecha de finalización de vigencia del amparo';
COMMENT ON INDEX idx_contrato_general_tipo_contrato IS 'Índice para optimizar búsquedas por tipo de contrato';
COMMENT ON INDEX idx_documento_contrato_contrato IS 'Índice para optimizar la relación entre documentos y contratos';
COMMENT ON INDEX idx_estado_contrato_contrato IS 'Índice para optimizar consultas de estado de contratos';
COMMENT ON INDEX idx_supervisor_contrato_supervisor IS 'Índice para optimizar búsquedas por supervisor';
COMMENT ON INDEX idx_disponibilidad_presupuestal_contrato IS 'Índice para optimizar la relación entre CDP (disponibilidad presupuestal) y contratos';
COMMENT ON INDEX idx_poliza_contrato_general IS 'Índice para optimizar la consulta de pólizas por contrato';
COMMENT ON INDEX idx_amparo_poliza_contrato_general IS 'Índice para optimizar la consulta de amparos por contrato';
COMMENT ON INDEX idx_amparo_poliza_poliza IS 'Índice para optimizar la consulta de amparos por póliza';
-- fin comentarios

COMMIT;
