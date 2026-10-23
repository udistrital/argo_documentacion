-- =====================================================================
-- ARGO v2 · Migración del modelo actual (gestion_contractual_crud,
-- develop 9e20927, sql/creacion-tablas.sql) al modelo refinado (#384).
--
-- Se ejecuta sobre el esquema donde están hoy las tablas (por defecto
-- public), con el search_path apuntando a ese esquema. Mover las tablas
-- al esquema definitivo es un paso aparte (ver notas-migracion.md).
--
-- Todo corre en una sola transacción: si una verificación falla, se
-- aborta con un mensaje y no queda ningún cambio aplicado.
-- Reverso: migracion-desde-v2.down.sql
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. Verificaciones previas (abortan si los datos no permiten migrar)
-- ---------------------------------------------------------------------

DO $$
DECLARE
    n integer;
    detalle text;
BEGIN
    -- 1.1 contratista se absorbe en contrato_general (relación 1 a 1, ítem 16)
    SELECT count(*) INTO n FROM contratista WHERE contrato_general_id IS NULL;
    IF n > 0 THEN
        RAISE EXCEPTION 'Migración #384 abortada: % registro(s) de contratista sin contrato_general_id. Asígnelos o elimínelos antes de migrar.', n;
    END IF;
    SELECT string_agg(contrato_general_id || ' (' || total || ')', ', ') INTO detalle
    FROM (SELECT contrato_general_id, count(*) AS total FROM contratista GROUP BY 1 HAVING count(*) > 1) d;
    IF detalle IS NOT NULL THEN
        RAISE EXCEPTION 'Migración #384 abortada: contratos con más de un contratista (contrato_general_id (cantidad)): %. La relación es 1 a 1.', detalle;
    END IF;

    -- 1.2 lugar_ejecucion se absorbe en contrato_general (supuesto S7)
    SELECT count(*) INTO n FROM lugar_ejecucion WHERE contrato_general_id IS NULL;
    IF n > 0 THEN
        RAISE EXCEPTION 'Migración #384 abortada: % registro(s) de lugar_ejecucion sin contrato_general_id.', n;
    END IF;
    SELECT string_agg(contrato_general_id || ' (' || total || ')', ', ') INTO detalle
    FROM (SELECT contrato_general_id, count(*) AS total FROM lugar_ejecucion GROUP BY 1 HAVING count(*) > 1) d;
    IF detalle IS NOT NULL THEN
        RAISE EXCEPTION 'Migración #384 abortada: contratos con más de un lugar de ejecución (contrato_general_id (cantidad)): %.', detalle;
    END IF;

    -- 1.3 unidad_ejecutora_id pasa a NOT NULL (supuesto S4)
    SELECT string_agg(id::text, ', ' ORDER BY id) INTO detalle FROM contrato_general WHERE unidad_ejecutora_id IS NULL;
    IF detalle IS NOT NULL THEN
        RAISE EXCEPTION 'Migración #384 abortada: contratos sin unidad_ejecutora_id (id): %. Asigne 6818 (Rectoría) o 6819 (IDEXUD) antes de migrar.', detalle;
    END IF;

    -- 1.4 UNIQUE (numero_contrato, vigencia) (A14)
    SELECT string_agg(numero_contrato || '/' || coalesce(vigencia, 'sin vigencia') || ' (' || total || ')', ', ') INTO detalle
    FROM (SELECT numero_contrato, vigencia, count(*) AS total FROM contrato_general
          WHERE numero_contrato IS NOT NULL GROUP BY 1, 2 HAVING count(*) > 1) d;
    IF detalle IS NOT NULL THEN
        RAISE EXCEPTION 'Migración #384 abortada: números de contrato duplicados por vigencia (numero/vigencia (cantidad)): %.', detalle;
    END IF;

    -- 1.5 Textos que superan la nueva longitud
    SELECT string_agg(campo || ' (' || total || ')', ', ') INTO detalle FROM (
        SELECT 'contrato_general.modo_pago > 1000' AS campo, count(*) AS total FROM contrato_general WHERE length(modo_pago) > 1000
        UNION ALL SELECT 'contrato_general.objeto > 2000', count(*) FROM contrato_general WHERE length(objeto) > 2000
        UNION ALL SELECT 'contrato_general.justificacion > 4000', count(*) FROM contrato_general WHERE length(justificacion) > 4000
        UNION ALL SELECT 'contrato_general.actividades > 8000', count(*) FROM contrato_general WHERE length(actividades) > 8000
        UNION ALL SELECT 'contrato_general.condiciones > 4000', count(*) FROM contrato_general WHERE length(condiciones) > 4000
        UNION ALL SELECT 'supervisor_contrato.cargo_legado > 250', count(*) FROM supervisor_contrato WHERE length(cargo_legado) > 250
        UNION ALL SELECT 'ordenador_contrato.resolucion > 250', count(*) FROM ordenador_contrato WHERE length(resolucion) > 250
        UNION ALL SELECT 'ordenador_contrato.documento_identidad > 20', count(*) FROM ordenador_contrato WHERE length(documento_identidad) > 20
        UNION ALL SELECT 'contrato_arrendamiento.destinacion > 1000', count(*) FROM contrato_arrendamiento WHERE length(destinacion) > 1000
        UNION ALL SELECT 'especificacion_tecnica.descripcion > 2000', count(*) FROM especificacion_tecnica WHERE length(descripcion) > 2000
        UNION ALL SELECT 'acta_inicio.descripcion > 2000', count(*) FROM acta_inicio WHERE length(descripcion) > 2000
    ) d WHERE total > 0;
    IF detalle IS NOT NULL THEN
        RAISE EXCEPTION 'Migración #384 abortada: textos más largos que la nueva longitud: %.', detalle;
    END IF;

    -- 1.6 Montos que no caben en numeric(20,7) o que perderían decimales
    SELECT string_agg(campo || ' (' || total || ')', ', ') INTO detalle FROM (
        SELECT 'contrato_general.valor_pesos >= 1e13' AS campo, count(*) AS total FROM contrato_general WHERE abs(valor_pesos) >= 1e13
        UNION ALL SELECT 'contrato_general.valor_tasa_cambio con más de 7 decimales', count(*) FROM contrato_general WHERE valor_tasa_cambio <> round(valor_tasa_cambio, 7)
        UNION ALL SELECT 'contrato_arrendamiento.valor_administracion >= 1e13', count(*) FROM contrato_arrendamiento WHERE abs(valor_administracion) >= 1e13
        UNION ALL SELECT 'contrato_arrendamiento.valor_arrendamiento >= 1e13', count(*) FROM contrato_arrendamiento WHERE abs(valor_arrendamiento) >= 1e13
        UNION ALL SELECT 'especificacion_tecnica.valor_unitario >= 1e13', count(*) FROM especificacion_tecnica WHERE abs(valor_unitario) >= 1e13
        UNION ALL SELECT 'especificacion_tecnica.valor_total >= 1e13', count(*) FROM especificacion_tecnica WHERE abs(valor_total) >= 1e13
    ) d WHERE total > 0;
    IF detalle IS NOT NULL THEN
        RAISE EXCEPTION 'Migración #384 abortada: montos fuera de numeric(20,7): %.', detalle;
    END IF;
END
$$;

-- ---------------------------------------------------------------------
-- 2. Proveedor (antes contratista) absorbido en contrato_general
-- ---------------------------------------------------------------------

ALTER TABLE contrato_general
    ADD COLUMN fecha_suscripcion date,
    ADD COLUMN proveedor_numero_documento varchar(20),
    ADD COLUMN tipo_persona_id integer,
    ADD COLUMN clase_proveedor_id integer;

UPDATE contrato_general cg
SET proveedor_numero_documento = c.numero_documento,
    tipo_persona_id = c.tipo_persona_id,
    clase_proveedor_id = c.clase_contratista_id
FROM contratista c
WHERE c.contrato_general_id = cg.id;

DROP TABLE contratista;

-- ---------------------------------------------------------------------
-- 3. Lugar de ejecución absorbido en contrato_general (supuesto S7)
-- ---------------------------------------------------------------------

ALTER TABLE contrato_general
    ADD COLUMN lugar_ejecucion_pais_id integer,
    ADD COLUMN lugar_ejecucion_ciudad_id integer,
    ADD COLUMN lugar_ejecucion_municipio_id integer,
    ADD COLUMN lugar_ejecucion_dependencia_id integer,
    ADD COLUMN lugar_ejecucion_sede_id integer,
    ADD COLUMN lugar_ejecucion_direccion varchar(150);

UPDATE contrato_general cg
SET lugar_ejecucion_pais_id = l.pais_id,
    lugar_ejecucion_ciudad_id = l.ciudad_id,
    lugar_ejecucion_municipio_id = l.municipio_id,
    lugar_ejecucion_dependencia_id = l.dependencia_id,
    lugar_ejecucion_sede_id = l.sede_id,
    lugar_ejecucion_direccion = l.direccion
FROM lugar_ejecucion l
WHERE l.contrato_general_id = cg.id;

DROP TABLE lugar_ejecucion;

-- ---------------------------------------------------------------------
-- 4. Columnas nuevas (usuario_id y usuario_rol, estado de póliza, acta)
-- ---------------------------------------------------------------------

ALTER TABLE contrato_general
    ADD COLUMN usuario_id integer,
    ADD COLUMN usuario_rol varchar(40);

ALTER TABLE poliza
    ADD COLUMN estado_poliza_id integer,
    ADD COLUMN usuario_rol varchar(40);

ALTER TABLE amparo_poliza
    ADD COLUMN usuario_id integer,
    ADD COLUMN usuario_rol varchar(40);

ALTER TABLE documento_contrato
    ADD COLUMN usuario_id integer,
    ADD COLUMN usuario_rol varchar(40);

ALTER TABLE acta_inicio
    ADD COLUMN fecha_suscripcion date,
    ADD COLUMN numero_acta varchar(50),
    ADD COLUMN valor_disponibilidad numeric(20,7),
    ADD COLUMN numero_registro_presupuestal varchar(50),
    ADD COLUMN valor_registro_presupuestal numeric(20,7),
    ADD COLUMN valor_anticipo numeric(20,7),
    ADD COLUMN nombre_interventor varchar(250),
    ADD COLUMN usuario_rol varchar(40);

-- ---------------------------------------------------------------------
-- 5. Renombres de columnas (nomenclatura <tabla>_id y nombres claros)
-- ---------------------------------------------------------------------

ALTER TABLE solicitante RENAME COLUMN dependencia_solicitante_id TO dependencia_id;
ALTER TABLE solicitante RENAME COLUMN sede_solicitante_id TO sede_id;
ALTER TABLE registro_presupuestal RENAME COLUMN cdp_id TO disponibilidad_presupuestal_id;
ALTER TABLE registro_presupuestal RENAME COLUMN registro_presupuestal TO numero_registro_presupuestal;

-- ---------------------------------------------------------------------
-- 6. Tipos según lineamiento (montos numeric(20,7), varchar con longitud)
-- ---------------------------------------------------------------------

ALTER TABLE contrato_general
    ALTER COLUMN valor_pesos TYPE numeric(20,7),
    ALTER COLUMN valor_contrato_me TYPE numeric(20,7),
    ALTER COLUMN valor_tasa_cambio TYPE numeric(20,7),
    ALTER COLUMN modo_pago TYPE varchar(1000),
    ALTER COLUMN objeto TYPE varchar(2000),
    ALTER COLUMN justificacion TYPE varchar(4000),
    ALTER COLUMN actividades TYPE varchar(8000),
    ALTER COLUMN condiciones TYPE varchar(4000);

ALTER TABLE supervisor_contrato ALTER COLUMN cargo_legado TYPE varchar(250);

ALTER TABLE ordenador_contrato
    ALTER COLUMN resolucion TYPE varchar(250),
    ALTER COLUMN documento_identidad TYPE varchar(20);

ALTER TABLE contrato_arrendamiento
    ALTER COLUMN destinacion TYPE varchar(1000),
    ALTER COLUMN valor_administracion TYPE numeric(20,7),
    ALTER COLUMN valor_arrendamiento TYPE numeric(20,7);

ALTER TABLE especificacion_tecnica
    ALTER COLUMN descripcion TYPE varchar(2000),
    ALTER COLUMN valor_unitario TYPE numeric(20,7),
    ALTER COLUMN valor_total TYPE numeric(20,7);

ALTER TABLE acta_inicio ALTER COLUMN descripcion TYPE varchar(2000);

-- ---------------------------------------------------------------------
-- 7. Columnas de auditoría: activo NOT NULL DEFAULT true y fechas NOT NULL
-- ---------------------------------------------------------------------

UPDATE disponibilidad_presupuestal SET activo = true WHERE activo IS NULL;
UPDATE solicitante SET fecha_modificacion = fecha_creacion WHERE fecha_modificacion IS NULL;
UPDATE supervisor_contrato SET fecha_modificacion = fecha_creacion WHERE fecha_modificacion IS NULL;
UPDATE ordenador_contrato SET fecha_modificacion = fecha_creacion WHERE fecha_modificacion IS NULL;

DO $$
DECLARE
    t text;
BEGIN
    FOREACH t IN ARRAY ARRAY['contrato_general', 'estado_contrato', 'solicitante', 'supervisor_contrato',
        'ordenador_contrato', 'contrato_arrendamiento', 'convenio', 'especificacion_tecnica',
        'disponibilidad_presupuestal', 'registro_presupuestal', 'poliza', 'amparo_poliza',
        'documento_contrato', 'acta_inicio']
    LOOP
        EXECUTE format('ALTER TABLE %I
            ALTER COLUMN activo SET DEFAULT true,
            ALTER COLUMN activo SET NOT NULL,
            ALTER COLUMN fecha_creacion SET DEFAULT now(),
            ALTER COLUMN fecha_modificacion SET DEFAULT now(),
            ALTER COLUMN fecha_modificacion SET NOT NULL', t);
    END LOOP;
END
$$;

ALTER TABLE contrato_general ALTER COLUMN unidad_ejecutora_id SET NOT NULL;

-- ---------------------------------------------------------------------
-- 8. Restricciones e índices con la nomenclatura del lineamiento
-- ---------------------------------------------------------------------

ALTER TABLE contrato_general RENAME CONSTRAINT contrato_general_pkey TO pk_contrato_general;
ALTER TABLE estado_contrato RENAME CONSTRAINT estado_contrato_pkey TO pk_estado_contrato;
ALTER TABLE solicitante RENAME CONSTRAINT solicitante_pkey TO pk_solicitante;
ALTER TABLE supervisor_contrato RENAME CONSTRAINT supervisor_contrato_pkey TO pk_supervisor_contrato;
ALTER TABLE ordenador_contrato RENAME CONSTRAINT ordenador_contrato_pkey TO pk_ordenador_contrato;
ALTER TABLE contrato_arrendamiento RENAME CONSTRAINT contrato_arrendamiento_pkey TO pk_contrato_arrendamiento;
ALTER TABLE convenio RENAME CONSTRAINT convenio_pkey TO pk_convenio;
ALTER TABLE especificacion_tecnica RENAME CONSTRAINT especificacion_tecnica_pkey TO pk_especificacion_tecnica;
ALTER TABLE disponibilidad_presupuestal RENAME CONSTRAINT disponibilidad_presupuestal_pkey TO pk_disponibilidad_presupuestal;
ALTER TABLE registro_presupuestal RENAME CONSTRAINT registro_presupuestal_pkey TO pk_registro_presupuestal;
ALTER TABLE poliza RENAME CONSTRAINT poliza_pkey TO pk_poliza;
ALTER TABLE amparo_poliza RENAME CONSTRAINT amparo_poliza_pkey TO pk_amparo_poliza;
ALTER TABLE documento_contrato RENAME CONSTRAINT documento_contrato_pkey TO pk_documento_contrato;
ALTER TABLE acta_inicio RENAME CONSTRAINT acta_inicio_pkey TO pk_acta_inicio;

ALTER TABLE estado_contrato RENAME CONSTRAINT estado_contrato_contrato_general_id_fkey TO fk_estado_contrato_contrato_general;
ALTER TABLE solicitante RENAME CONSTRAINT solicitante_contrato_general_id_fkey TO fk_solicitante_contrato_general;
ALTER TABLE supervisor_contrato RENAME CONSTRAINT supervisor_contrato_contrato_general_id_fkey TO fk_supervisor_contrato_contrato_general;
ALTER TABLE ordenador_contrato RENAME CONSTRAINT ordenador_contrato_contrato_general_id_fkey TO fk_ordenador_contrato_contrato_general;
ALTER TABLE contrato_arrendamiento RENAME CONSTRAINT contrato_arrendamiento_contrato_general_id_fkey TO fk_contrato_arrendamiento_contrato_general;
ALTER TABLE convenio RENAME CONSTRAINT convenio_contrato_general_id_fkey TO fk_convenio_contrato_general;
ALTER TABLE especificacion_tecnica RENAME CONSTRAINT especificacion_tecnica_contrato_general_id_fkey TO fk_especificacion_tecnica_contrato_general;
ALTER TABLE disponibilidad_presupuestal RENAME CONSTRAINT disponibilidad_presupuestal_contrato_general_id_fkey TO fk_disponibilidad_presupuestal_contrato_general;
ALTER TABLE registro_presupuestal RENAME CONSTRAINT registro_presupuestal_cdp_id_fkey TO fk_registro_presupuestal_disponibilidad_presupuestal;
ALTER TABLE poliza RENAME CONSTRAINT poliza_contrato_general_id_fkey TO fk_poliza_contrato_general;
ALTER TABLE amparo_poliza RENAME CONSTRAINT amparo_poliza_contrato_general_id_fkey TO fk_amparo_poliza_contrato_general;
ALTER TABLE amparo_poliza RENAME CONSTRAINT amparo_poliza_poliza_id_fkey TO fk_amparo_poliza_poliza;
ALTER TABLE documento_contrato RENAME CONSTRAINT documento_contrato_contrato_general_id_fkey TO fk_documento_contrato_contrato_general;
ALTER TABLE acta_inicio RENAME CONSTRAINT acta_inicio_contrato_general_id_fkey TO fk_acta_inicio_contrato_general;

ALTER TABLE contrato_arrendamiento RENAME CONSTRAINT contrato_arrendamiento_contrato_general_id_key TO uq_contrato_general_id_contrato_arrendamiento;
ALTER TABLE contrato_general ADD CONSTRAINT uq_numero_contrato_vigencia_contrato_general UNIQUE (numero_contrato, vigencia);

ALTER INDEX idx_contrato_general_tipo_contrato RENAME TO idx_contrato_general_tipo_contrato_id;
ALTER INDEX idx_documento_contrato_contrato RENAME TO idx_documento_contrato_contrato_general_id;
ALTER INDEX idx_estado_contrato_contrato RENAME TO idx_estado_contrato_contrato_general_id;
ALTER INDEX idx_supervisor_contrato_supervisor RENAME TO idx_supervisor_contrato_supervisor_id;
ALTER INDEX idx_disponibilidad_presupuestal_contrato RENAME TO idx_disponibilidad_presupuestal_contrato_general_id;
ALTER INDEX idx_poliza_contrato_general RENAME TO idx_poliza_contrato_general_id;
ALTER INDEX idx_amparo_poliza_contrato_general RENAME TO idx_amparo_poliza_contrato_general_id;
ALTER INDEX idx_amparo_poliza_poliza RENAME TO idx_amparo_poliza_poliza_id;

CREATE INDEX idx_contrato_general_unidad_ejecutora_id ON contrato_general (unidad_ejecutora_id);
CREATE INDEX idx_solicitante_contrato_general_id ON solicitante (contrato_general_id);
CREATE INDEX idx_supervisor_contrato_contrato_general_id ON supervisor_contrato (contrato_general_id);
CREATE INDEX idx_ordenador_contrato_contrato_general_id ON ordenador_contrato (contrato_general_id);
CREATE INDEX idx_convenio_contrato_general_id ON convenio (contrato_general_id);
CREATE INDEX idx_especificacion_tecnica_contrato_general_id ON especificacion_tecnica (contrato_general_id);
CREATE INDEX idx_registro_presupuestal_disponibilidad_presupuestal_id ON registro_presupuestal (disponibilidad_presupuestal_id);
CREATE INDEX idx_acta_inicio_contrato_general_id ON acta_inicio (contrato_general_id);

-- ---------------------------------------------------------------------
-- 9. Tablas nuevas
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

-- huella_navegador (#376) no existe en develop. Si el ambiente ya tiene la
-- tabla del PR gestion_contractual_crud#49, solo se ajusta fecha_modificacion.
CREATE TABLE IF NOT EXISTS huella_navegador (
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

UPDATE huella_navegador SET fecha_modificacion = fecha_creacion WHERE fecha_modificacion IS NULL;
ALTER TABLE huella_navegador ALTER COLUMN fecha_modificacion SET DEFAULT now(), ALTER COLUMN fecha_modificacion SET NOT NULL;
CREATE INDEX IF NOT EXISTS idx_huella_navegador_huella ON huella_navegador (huella);
CREATE INDEX IF NOT EXISTS idx_huella_navegador_usuario_id ON huella_navegador (usuario_id);

-- ---------------------------------------------------------------------
-- 10. Comentarios del modelo refinado
-- Se limpian los comentarios anteriores y se aplican los de creacion-tablas.sql.
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
    FOR r IN
        SELECT c.relname FROM pg_class c
        WHERE c.relnamespace = current_schema()::regnamespace AND c.relkind = 'i'
          AND obj_description(c.oid, 'pg_class') IS NOT NULL
    LOOP
        EXECUTE format('COMMENT ON INDEX %I IS NULL', r.relname);
    END LOOP;
END
$$;

-- inicio comentarios (generado por scripts/sincroniza_comentarios.py desde ddl/creacion-tablas.sql)
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
COMMENT ON TABLE estado_contrato IS 'Historial de estados del contrato (general e interno)';
COMMENT ON COLUMN estado_contrato.estado_parametro_id IS 'Parámetros CRUD, tipo 137 Estados del contrato (estado general)';
COMMENT ON COLUMN estado_contrato.estado_interno_parametro_id IS 'Parámetros CRUD, tipo 141 Estados internos del contrato';
COMMENT ON COLUMN estado_contrato.actual IS 'Marca el estado vigente del contrato';
COMMENT ON COLUMN estado_contrato.motivo IS 'Razón del cambio de estado';
COMMENT ON COLUMN estado_contrato.fecha_evento IS 'Fecha del cambio de estado';
COMMENT ON COLUMN estado_contrato.usuario_id IS 'Identificador del usuario que efectúa el cambio de estado';
COMMENT ON COLUMN estado_contrato.usuario_rol IS 'Rol del usuario que efectúa el cambio de estado';
COMMENT ON TABLE solicitante IS 'Dependencia y sede que solicitan el contrato. Cardinalidad 1 a 1 por validar (A12)';
COMMENT ON COLUMN solicitante.dependencia_id IS 'OIKOS, dependencia que solicita el contrato. Antes dependencia_solicitante_id';
COMMENT ON COLUMN solicitante.sede_id IS 'OIKOS, sede donde se origina la solicitud. Antes sede_solicitante_id';
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
COMMENT ON TABLE ordenador_contrato IS 'Ordenador del gasto del contrato. Validar soporte de migración ARGO v1. Confirmar si un contrato puede tener varios ordenadores (A12)';
COMMENT ON COLUMN ordenador_contrato.tercero_id IS 'Terceros, tercero que actúa como ordenador del gasto';
COMMENT ON COLUMN ordenador_contrato.cargo_id IS 'Parámetros CRUD, cargo del ordenador';
COMMENT ON COLUMN ordenador_contrato.documento_identidad IS 'Documento de identidad del ordenador';
COMMENT ON COLUMN ordenador_contrato.resolucion IS 'Resolución que autoriza al ordenador';
COMMENT ON COLUMN ordenador_contrato.ordenador_argo_id IS 'ARGO v1, PK de la tabla ordenadores';
COMMENT ON COLUMN ordenador_contrato.ordenador_sicapital_id IS 'ARGO v1, id_ordenador de la tabla ordenadores (SiCapital)';
COMMENT ON TABLE contrato_arrendamiento IS 'Datos propios de un contrato de arrendamiento (1 a 1 con el contrato)';
COMMENT ON COLUMN contrato_arrendamiento.destinacion IS 'Uso previsto del inmueble arrendado';
COMMENT ON COLUMN contrato_arrendamiento.plazo_pago_mensual IS 'Día del mes establecido para el pago';
COMMENT ON COLUMN contrato_arrendamiento.reajuste IS 'Condición de reajuste del canon';
COMMENT ON COLUMN contrato_arrendamiento.plazo_administracion IS 'Plazo de pago de la administración';
COMMENT ON COLUMN contrato_arrendamiento.valor_administracion IS 'Valor de la administración';
COMMENT ON COLUMN contrato_arrendamiento.plazo_entrega IS 'Plazo de entrega del inmueble';
COMMENT ON COLUMN contrato_arrendamiento.valor_arrendamiento IS 'Valor mensual del arrendamiento';
COMMENT ON TABLE convenio IS 'Convenio en el que se enmarca el contrato';
COMMENT ON COLUMN convenio.nombre IS 'Nombre del convenio';
COMMENT ON COLUMN convenio.vigencia IS 'Año de vigencia del convenio';
COMMENT ON COLUMN convenio.tipo_convenio_id IS 'Parámetros CRUD, tipo de convenio (tipo de parámetro por confirmar)';
COMMENT ON TABLE especificacion_tecnica IS 'Ítems técnicos y económicos del contrato';
COMMENT ON COLUMN especificacion_tecnica.descripcion IS 'Descripción del ítem o servicio';
COMMENT ON COLUMN especificacion_tecnica.cantidad IS 'Cantidad de ítems';
COMMENT ON COLUMN especificacion_tecnica.valor_unitario IS 'Valor unitario del ítem';
COMMENT ON COLUMN especificacion_tecnica.valor_total IS 'Valor total del ítem';
COMMENT ON TABLE disponibilidad_presupuestal IS 'Certificados de disponibilidad presupuestal (CDP) del contrato';
COMMENT ON COLUMN disponibilidad_presupuestal.numero_cdp_id IS 'SiCapital, número del CDP con el que se consulta la fuente';
COMMENT ON COLUMN disponibilidad_presupuestal.vigencia_cdp IS 'Año de vigencia del CDP';
COMMENT ON COLUMN disponibilidad_presupuestal.fecha_registro IS 'Fecha de registro del CDP';
COMMENT ON TABLE registro_presupuestal IS 'Registros presupuestales (RP) expedidos sobre un CDP';
COMMENT ON COLUMN registro_presupuestal.disponibilidad_presupuestal_id IS 'Antes cdp_id';
COMMENT ON COLUMN registro_presupuestal.numero_registro_presupuestal IS 'Número del registro presupuestal (RP). Antes registro_presupuestal';
COMMENT ON COLUMN registro_presupuestal.vigencia_rp IS 'Año de vigencia del RP';
COMMENT ON COLUMN registro_presupuestal.fecha_registro IS 'Fecha de registro del RP';
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
COMMENT ON TABLE documento_contrato IS 'Documentos del contrato en una sola tabla, sin estados (A9 "con ajustes"; supuesto S6)';
COMMENT ON COLUMN documento_contrato.tipo_documento_id IS 'Parámetros CRUD, tipo de documento (tipo 133 Documentos Contrato)';
COMMENT ON COLUMN documento_contrato.documento_id IS 'Gestor Documental, identificador del documento';
COMMENT ON COLUMN documento_contrato.documento_enlace IS 'Gestor Documental, enlace del documento';
COMMENT ON COLUMN documento_contrato.usuario_id IS 'Identificador del usuario que registra el documento';
COMMENT ON COLUMN documento_contrato.usuario_rol IS 'Rol del usuario que registra el documento';
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
COMMENT ON TABLE parametro_unidad_ejecutora IS 'Valores paramétricos que aplican a cada unidad ejecutora (propuesta del 21/10, supuesto S4). Sin registro significa que no aplica';
COMMENT ON COLUMN parametro_unidad_ejecutora.parametro_id IS 'Parámetros CRUD, parametros.parametro.id (otra BD, sin FK física)';
COMMENT ON COLUMN parametro_unidad_ejecutora.unidad_ejecutora_id IS 'Parámetros CRUD, tipo 146 Unidad Ejecutora';
COMMENT ON TABLE configuracion_unidad_ejecutora IS 'Formato del número de contrato por unidad ejecutora; reemplaza conf.ts del MID (propuesta del 21/10, supuesto S4)';
COMMENT ON COLUMN configuracion_unidad_ejecutora.unidad_ejecutora_id IS 'Parámetros CRUD, tipo 146 Unidad Ejecutora';
COMMENT ON COLUMN configuracion_unidad_ejecutora.prefijo_numero_contrato IS 'Prefijo del número de contrato (hoy Rectoría vacío, IDEXUD "ID-")';
COMMENT ON COLUMN configuracion_unidad_ejecutora.sufijo_numero_contrato IS 'Sufijo del número de contrato (hoy vacío en ambas)';
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
-- fin comentarios

COMMIT;
