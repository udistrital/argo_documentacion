-- Datos mínimos para probar la migración sobre el DDL de develop (9e20927).
-- No se usa sql/datos-mock.sql porque no carga contra ese DDL.
-- Cubre: contratos con y sin contratista y lugar de ejecución, activo nulo en
-- disponibilidad_presupuestal, fecha_modificacion nula y textos sin longitud.

INSERT INTO contrato_general (id, numero_contrato, vigencia, consecutivo_elaboracion, unidad_ejecutora_id,
    tipo_compromiso_id, tipo_contrato_id, valor_pesos, valor_contrato_me, valor_tasa_cambio,
    objeto, modo_pago, actividades, activo, fecha_creacion, fecha_modificacion)
VALUES
    (1, '101', '2026', 'CE-2026-001', 6818, 6535, 6546, 54600000.00, NULL, NULL,
     'Prestación de servicios profesionales', 'Mensual', 'Actividad 1; actividad 2', true,
     '2026-03-01 08:00', '2026-03-01 08:00'),
    (2, 'ID-102', '2026', 'CE-2026-002', 6819, 6535, 6544, 120000000.50, 30000.125, 4000.1234567,
     'Suministro de equipos', 'Pago único', NULL, true, '2026-03-02 09:00', '2026-03-05 10:00'),
    (3, NULL, '2026', 'CE-2026-003', 6818, 6534, 6537, 1500000.00, NULL, NULL,
     'Orden de servicio en elaboración', NULL, NULL, true, '2026-03-03 10:00', '2026-03-03 10:00');
SELECT setval('contrato_general_id_seq', 3);

INSERT INTO contratista (numero_documento, tipo_persona_id, contrato_general_id, clase_contratista_id,
    activo, fecha_creacion, fecha_modificacion)
VALUES
    ('1012345678', 6711, 1, 6615, true, '2026-03-01 08:05', NULL),
    ('900123456', 6712, 2, 6616, true, '2026-03-02 09:05', '2026-03-02 09:05');

INSERT INTO lugar_ejecucion (pais_id, ciudad_id, municipio_id, dependencia_id, sede_id, direccion,
    contrato_general_id, activo, fecha_creacion, fecha_modificacion)
VALUES
    (170, 11001, 11001, 45, 3, 'Carrera 7 # 40B-53', 1, true, '2026-03-01 08:06', NULL),
    (170, 11001, NULL, NULL, 12, 'Calle 13 # 31-75', 2, true, '2026-03-02 09:06', '2026-03-02 09:06');

INSERT INTO solicitante (dependencia_solicitante_id, sede_solicitante_id, contrato_general_id,
    activo, fecha_creacion, fecha_modificacion)
VALUES (45, 3, 1, true, '2026-03-01 08:07', NULL);

INSERT INTO disponibilidad_presupuestal (numero_cdp_id, fecha_registro, vigencia_cdp, contrato_general_id,
    activo, fecha_creacion, fecha_modificacion)
VALUES (1234, '2026-02-20', 2026, 1, NULL, '2026-03-01 08:08', '2026-03-01 08:08');

INSERT INTO registro_presupuestal (registro_presupuestal, fecha_registro, vigencia_rp, cdp_id,
    activo, fecha_creacion, fecha_modificacion)
VALUES (5678, '2026-03-10', 2026, 1, true, '2026-03-10 08:00', '2026-03-10 08:00');

INSERT INTO estado_contrato (usuario_id, motivo, contrato_general_id, estado_parametro_id,
    estado_interno_parametro_id, actual, usuario_rol, fecha_evento)
VALUES (77, NULL, 1, 6774, 6800, true, 'ABOGADO_CONTRATACION_RECTOR', '2026-03-04');

INSERT INTO poliza (numero_poliza, entidad_aseguradora_id, contrato_general_id, fecha_inicio, fecha_fin, usuario_id)
VALUES ('POL-2026-0001', 3, 2, '2026-03-05', '2026-12-31', 77);

INSERT INTO amparo_poliza (contrato_general_id, poliza_id, amparo_id, tipo_valor_amparo_id, suficiencia, valor)
VALUES (2, 1, 6602, 6709, 10.0000000, 12000000.0000000);

INSERT INTO acta_inicio (usuario_id, descripcion, fecha_inicio, fecha_fin, contrato_general_id,
    activo, fecha_creacion, fecha_modificacion)
VALUES (77, 'Acta de inicio del contrato 101', '2026-03-15', '2026-09-15', 1, true, '2026-03-15 08:00', '2026-03-15 08:00');

INSERT INTO documento_contrato (tipo_documento_id, contrato_general_id, documento_enlace, documento_id,
    activo, fecha_creacion, fecha_modificacion)
VALUES (6805, 1, 'b1c2d3e4-0000-4000-8000-000000000001', 168960, true, '2026-03-04 08:00', '2026-03-04 08:00');

INSERT INTO ordenador_contrato (tercero_id, ordenador_argo_id, ordenador_sicapital_id, resolucion,
    documento_identidad, cargo_id, contrato_general_id, activo, fecha_creacion, fecha_modificacion)
VALUES (501, 12, 34, 'Resolución 123 de 2026', '79123456', 9, 1, true, '2026-03-01 08:09', NULL);
