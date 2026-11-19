-- Carga inicial de unidad ejecutora (#384). Generado por scripts/genera_carga_unidad_ejecutora.py
-- desde el consolidado depurado por negocio (columna "Aplica para IDEXUD").
-- Rectoría (6818): pendiente de la #383; no se carga. Unidad ejecutora 03: pendiente.
-- Requiere el search_path del esquema del modelo (contratacion o el que se defina).

BEGIN;

-- Formato del número de contrato: valores actuales de gestion_contractual_mid/src/contrato-general/conf.ts
INSERT INTO configuracion_unidad_ejecutora (unidad_ejecutora_id, prefijo_numero_contrato, sufijo_numero_contrato)
VALUES (6818, '', ''), (6819, 'ID-', '');

-- Parámetros que aplican a IDEXUD (75 filas)
INSERT INTO parametro_unidad_ejecutora (parametro_id, unidad_ejecutora_id) VALUES
    (166, 6819),  -- 7 Tiempo: DIAS
    (179, 6819),  -- 7 Tiempo: HORAS
    (180, 6819),  -- 7 Tiempo: MESES
    (181, 6819),  -- 7 Tiempo: AÑOS
    (6535, 6819),  -- 111 Compromiso: 2 - Contrato
    (6536, 6819),  -- 111 Compromiso: 1 - Convenio
    (6539, 6819),  -- 112 Contrato: Contrato de Arrendamiento
    (6540, 6819),  -- 112 Contrato: Contrato de Compra-Venta
    (6541, 6819),  -- 112 Contrato: Contrato Interadministrativo
    (6543, 6819),  -- 112 Contrato: Contrato de Obra
    (6544, 6819),  -- 112 Contrato: Contrato de Suministro
    (6545, 6819),  -- 112 Contrato: Contrato de Prestación de Servicios
    (6546, 6819),  -- 112 Contrato: Contrato de Prestación de Servicios Profesionales o Apoyo a la Gestión
    (6547, 6819),  -- 112 Contrato: Contrato de Consultoría
    (6687, 6819),  -- 113 Perfil del Contratista: Asistencial
    (6688, 6819),  -- 113 Perfil del Contratista: Técnico
    (6689, 6819),  -- 113 Perfil del Contratista: Profesional
    (6690, 6819),  -- 113 Perfil del Contratista: Profesional Especializado
    (6691, 6819),  -- 113 Perfil del Contratista: Asesor 1
    (6693, 6819),  -- 113 Perfil del Contratista: No Aplica
    (6549, 6819),  -- 114 Tipología Específica: 131 - Arrendamiento de Bienes Muebles
    (6550, 6819),  -- 114 Tipología Específica: 132 - Arrendamiento de Bienes Inmuebles
    (6551, 6819),  -- 114 Tipología Específica: 121 - Compraventa (Bienes Muebles)
    (6553, 6819),  -- 114 Tipología Específica: 911 - Contrato Interadministrativo
    (6554, 6819),  -- 114 Tipología Específica: 10 - Contrato de Obra
    (6555, 6819),  -- 114 Tipología Específica: 42 - Suministro de Bienes en General
    (6556, 6819),  -- 114 Tipología Específica: 43 - Suministro de Servicio de Vigilancia
    (6557, 6819),  -- 114 Tipología Específica: 44 - Suministro de Servicio de Aseo
    (6558, 6819),  -- 114 Tipología Específica: 45 - Suministro de Alimentos
    (6559, 6819),  -- 114 Tipología Específica: 46 - Suministro de Medicamentos
    (6560, 6819),  -- 114 Tipología Específica: 48 - Otros Suministros
    (6561, 6819),  -- 114 Tipología Específica: 30 - Servicios de Mantenimiento y/o Reparación
    (6562, 6819),  -- 114 Tipología Específica: 32 - Servicios Artísticos
    (6563, 6819),  -- 114 Tipología Específica: 34 - Servicios Asistenciales de Salud
    (6564, 6819),  -- 114 Tipología Específica: 35 - Servicios de Comunicaciones
    (6565, 6819),  -- 114 Tipología Específica: 36 - Servicios de Edición
    (6566, 6819),  -- 114 Tipología Específica: 37 - Servicios de Impresión
    (6567, 6819),  -- 114 Tipología Específica: 38 - Servicios de Publicación
    (6568, 6819),  -- 114 Tipología Específica: 39 - Servicios de Capacitación
    (6570, 6819),  -- 114 Tipología Específica: 49 - Otros Servicios
    (6571, 6819),  -- 114 Tipología Específica: 50 - Servicios de Transporte
    (6572, 6819),  -- 114 Tipología Específica: 31 - Servicios Profesionales
    (6573, 6819),  -- 114 Tipología Específica: 33 - Servicios Apoyo a la Gestión de la Entidad (Servicios Administrativos)
    (6574, 6819),  -- 114 Tipología Específica: CPS
    (6575, 6819),  -- 114 Tipología Específica: 21 - Consultoría (Interventoría)
    (6576, 6819),  -- 114 Tipología Específica: 22 - Consultoría (Gerencia de Obra)
    (6577, 6819),  -- 114 Tipología Específica: 24 - Consultoría (Estudios y Diseños Técnicos)
    (6578, 6819),  -- 114 Tipología Específica: 25 - Consultoría (Estudios de Prefactibilidad y Factibilidad)
    (6579, 6819),  -- 114 Tipología Específica: 26 - Consultoría (Asesoría Técnica)
    (6580, 6819),  -- 114 Tipología Específica: 29 - Consultoría (Otros)
    (6871, 6819),  -- 114 Tipología Específica: 41 - Desarrollo de Proyectos Culturales
    (6911, 6819),  -- 114 Tipología Específica: 999 - Otro Tipo de Naturaleza de Contratos
    (6585, 6819),  -- 115 Modalidad de Selección: 5 - Contratación Directa
    (6587, 6819),  -- 115 Modalidad de Selección: 7 - Convocatoria Pública
    (6600, 6819),  -- 118 Ámparo: Amparo de Buen Manejo y Correcta Inversión del Anticipo
    (6601, 6819),  -- 118 Ámparo: Amparo de Pago Anticipado
    (6602, 6819),  -- 118 Ámparo: Amparo de Cumplimiento
    (6603, 6819),  -- 118 Ámparo: Amparo de Calidad y Correcto Funcionamiento del Bien o Servicios
    (6604, 6819),  -- 118 Ámparo: Amparo de Suministro de Repuestos y Accesorios
    (6605, 6819),  -- 118 Ámparo: Amparo de Salarios, Prestaciones e Indemnizaciones
    (6606, 6819),  -- 118 Ámparo: Amparo de Calidad del Bien o Servicio
    (6612, 6819),  -- 119 Tipo de Control: 1 - Interna
    (6615, 6819),  -- 120 Clase Contratista: Único Contratista
    (6634, 6819),  -- 122 Tipo de Moneda: Pesos Colombianos
    (6635, 6819),  -- 122 Tipo de Moneda: Dólar Americano
    (6646, 6819),  -- 123 Tipo de Gasto: 5 - Contratacion Derivada
    (6708, 6819),  -- 131 Suficiencia Amparo: SMLV
    (6709, 6819),  -- 131 Suficiencia Amparo: Porcentaje
    (6711, 6819),  -- 132 Tipo Persona: Natural
    (6712, 6819),  -- 132 Tipo Persona: Jurídica
    (6773, 6819),  -- 137 Estados del contrato: POR SUSCRIBIR
    (6774, 6819),  -- 137 Estados del contrato: SUSCRITO
    (6775, 6819),  -- 137 Estados del contrato: DECLINADO
    (6776, 6819),  -- 137 Estados del contrato: LEGALIZADO
    (6777, 6819);  -- 137 Estados del contrato: EN EJECUCIÓN

COMMIT;

-- No cargados (texto libre en la columna de IDEXUD, por revisar con negocio):
--   6658 5 - Unidad de Extensión: "es fondo de extensión"
--   6661 Transacción: "Solo uso esta"
