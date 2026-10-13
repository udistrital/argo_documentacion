"""Plan de ajustes, supuestos, preguntas y leyenda de la matriz (issue #356).

Criterio acordado con el LT en la sesión de socialización (1 de octubre de 2026): ARGO v1 está en producción y
tiene muchas integraciones, así que el plan no propone rediseños. Solo se admite alinear el CRUD con la BD de pruebas,
corregir lineamientos que no rompan integraciones y agregar campos faltantes al modelo actual cuando se confirmen.
"""

CRITERIO = ("ARGO v1 es el sistema que está hoy en producción y tiene muchas integraciones; proponer un modelo diferente "
            "las afecta. El plan no propone rediseños (entidades nuevas que reemplacen o partan las existentes, ni cambios "
            "de estructura): solo alinear el CRUD con la BD de pruebas, corregir lineamientos que no rompan integraciones "
            "y agregar campos faltantes al modelo actual cuando se confirmen.")

# Estados de un ajuste
RECOMENDADO = "Recomendado"
POR_CONFIRMAR = "Por confirmar"
STAND_BY = "Stand by"
NO_POR_AHORA = "No se recomienda por ahora"
FUERA = "Fuera de alcance"

AJUSTES = [
    # Fase 1: alinear con la BD de pruebas y lineamientos sin romper integraciones
    dict(id="A1", fase=1, estado=RECOMENDADO, tablas=["contratista", "documento_contrato"],
         descripcion="Alinear las entidades TypeORM con la BD de pruebas: en la BD la PK de contratista y documento_contrato ya es numérica (como en el DDL), mientras que la entidad usa uuid. Cambiar a @PrimaryGeneratedColumn() (serial). Las diferencias de longitud y nulabilidad entre DDL y entidad no se pueden verificar con el diagrama: se dejan como limitación.",
         impacto="El id de /contratistas y /documentos-contratos pasa de uuid a entero", rompe="Sí (lo consume el MID)",
         decision="No (respuesta 1)"),
    dict(id="A2", fase=1, estado=RECOMENDADO, tablas=["supervisor_contrato", "contratista", "disponibilidad_presupuestal", "solicitante",
                                                    "documento_contrato", "estado_contrato", "lugar_ejecucion"],
         descripcion="Reemplazar el DELETE físico (repository.delete) por borrado lógico (activo = false) en 7 servicios, y que los listados consulten solo activos mediante filtros (respuesta 5).",
         impacto="DELETE conserva la firma; los GET dejan de devolver inactivos", rompe="No", decision="No (respuesta 5)"),
    dict(id="A3", fase=1, estado=RECOMENDADO, tablas=["contrato_general", "especificacion_tecnica", "contrato_arrendamiento", "todas"],
         descripcion="Aplicar lineamientos que no cambian la estructura: montos numeric(20,7); varchar con longitud; activo DEFAULT TRUE; auditoría NOT NULL; nombres de restricciones e índices. No incluye unificar el tipo de vigencia (texto en contrato_general, numérico en las demás): cambiaría el tipo en la API y queda para una eventual migración.",
         endpoints="Sin cambio de rutas", impacto="Migración de esquema; mayor precisión decimal en respuestas", rompe="No",
         decision="No"),
    dict(id="A4", fase=1, estado=NO_POR_AHORA, tablas=["disponibilidad_presupuestal", "ordenador_contrato", "contrato_general"],
         descripcion="Renombrar URIs (/disponibilidad_presupuestal → /disponibilidades-presupuestales; /ordenador-contrato → /ordenadores-contratos; POST /contratos-generales/conteo-* → GET). No se recomienda por ahora por las integraciones; queda para una eventual migración de framework (respuesta 7).",
         impacto="Cambio de rutas", rompe="Sí", decision="No"),
    # Fase 2: brechas con solución clara sobre el modelo actual
    dict(id="A5", fase=2, estado=RECOMENDADO, tablas=["registro_presupuestal"],
         descripcion="Exponer registro_presupuestal (entidad, módulo, /registros-presupuestales). La tabla ya existe en la BD de pruebas. No se renombra cdp_id. Soporta CU-16.",
         endpoints="Nuevo recurso /registros-presupuestales", impacto="Nuevo recurso", rompe="No", decision="No"),
    dict(id="A6", fase=2, estado=RECOMENDADO, tablas=["contrato_general"],
         descripcion="Agregar la columna fecha_suscripcion en contrato_general (respuesta 10, opción a). El momento del registro (al firmar, una vez terminado el flujo de aprobación) es una decisión abierta (D5). Soporta CU-19.",
         impacto="Campo nuevo en el DTO (aditivo)", rompe="No", decision="Momento del registro: decisión abierta D5"),
    dict(id="A9", fase=2, estado=RECOMENDADO, tablas=["documento_contrato"],
         descripcion="Sin cambio de esquema: documento_contrato se mantiene como única tabla, sin estados (respuesta 12). La etapa (pre, contractual, pos) y el carácter (público/privado) se expresan con tipo_documento_id. Verificar que el parámetro cubra esas combinaciones y reflejarlo en el diccionario.",
         endpoints="Sin cambio", impacto="Documental / parámetros", rompe="No", decision="No"),
    # Fase 3: dependen de una confirmación
    dict(id="A7", fase=3, estado=STAND_BY, tablas=["poliza"],
         descripcion="Si se confirma (pregunta 13), agregar un campo de estado en poliza como referencia a Parámetros CRUD. Sin tabla de historial. Soporta CU-14.",
         impacto="Campo nuevo en el DTO (aditivo)", rompe="No", decision="Sí (pregunta 13)"),
    dict(id="A8", fase=3, estado=STAND_BY, tablas=["contrato_general"],
         descripcion="Proceso contractual y estudio previo: no se separan en entidades nuevas. Si se confirma (pregunta 8), agregar al modelo actual los campos faltantes: número de estudio, necesidad, obligaciones, y valor y plazo estimados como valores separados de los contratados (pregunta 14). Soporta CU-10 y CU-11.",
         impacto="Campos nuevos en el DTO (aditivos)", rompe="No", decision="Sí (preguntas 8 y 14)"),
    dict(id="A10", fase=3, estado=FUERA, tablas=["(ninguna)"],
         descripcion="Novedades y terminación: fuera de alcance (respuesta 3). Las novedades del nuevo Argo se analizan desde requerimientos. Terminación se trata como novedad, como en ARGO v1 (supuesto, decisión abierta D12). Liquidación es una decisión abierta (D11).",
         endpoints="Ninguno", impacto="Ninguno", rompe="No", decision="Liquidación: decisión abierta D11"),
    dict(id="A11", fase=3, estado=POR_CONFIRMAR, tablas=["contrato_general"],
         descripcion="Contratación derivada: si se confirma, agregar en contrato_general un campo que referencie el proyecto de extensión (IDEXUD). Soporta CU-15.",
         impacto="Campo nuevo en el DTO (aditivo)", rompe="No", decision="Sí"),
    dict(id="A12", fase=3, estado=STAND_BY, tablas=["contratista", "solicitante", "lugar_ejecucion", "ordenador_contrato"],
         descripcion="Sin cambio de estructura. Si se confirma que todas las relaciones son 1:1 (pregunta 11), agregar UNIQUE en contrato_general_id de contratista, solicitante, lugar_ejecucion y ordenador_contrato, como ya suponen las entidades (@OneToOne).",
         endpoints="Sin cambio", impacto="Restricción en BD", rompe="No", decision="Sí (pregunta 11)"),
    dict(id="A13", fase=3, estado=RECOMENDADO, tablas=["(diccionario)"],
         descripcion="Completar el diccionario: según la respuesta 15, profundizar las entidades sin atributos con el modelo general y validarlas contra las entidades de Argo v2; incluir las entidades que ya existen en el CRUD (supervisor, ordenador, amparo, estado, lugar de ejecución, especificación técnica, convenio, arrendamiento) y retirar estado_documento.",
         endpoints="Ninguno", impacto="Documental", rompe="No", decision="Sí (Analista de Requerimientos)"),
    dict(id="A14", fase=3, estado=POR_CONFIRMAR, tablas=["contrato_general"],
         descripcion="Agregar UNIQUE (numero_contrato, vigencia) en contrato_general: el LT indicó que numero_contrato es un identificador único por vigencia (respuesta 9). Por confirmar con LT y Analista (decisión abierta D4).",
         endpoints="Sin cambio", impacto="Restricción en BD; verificar antes que no haya duplicados", rompe="No",
         decision="Sí (pregunta 9)"),
]

SUPUESTOS = [
    "Línea base: DDL sql/creacion-tablas.sql y entidades TypeORM de la rama develop, después de la estabilización (issue #361, PR #46), y el diagrama de la BD de pruebas que compartió el LT (respuesta 1).",
    "El diagrama de la BD de pruebas solo permite comparar nombres de tablas y columnas, la PK y la categoría del tipo. Longitudes, precisión, nulabilidad, valores por defecto, UNIQUE, índices y cardinalidad no se verifican contra la BD.",
    "El diccionario no define tipos de dato, longitudes ni obligatoriedad. Los tipos del CRUD se contrastan contra el lineamiento OATI; la obligatoriedad no se puede comparar.",
    "El mapeo a Ágora se basa solo en las tres imágenes de la respuesta 2. Lo que no aparece se marca como no visible y los nombres de tabla cortados en el diagrama se dejan con '…'.",
    "Terminación se trata como novedad (fuera de alcance), como en ARGO v1 (terminacion_anticipada). No se trató en la sesión de socialización (decisión abierta D12).",
    "Las relaciones del contrato con contratista, solicitante, lugar de ejecución y ordenador se tratan como 1:1 de forma provisional (respuesta 11, stand by).",
    "Los casos de uso sin efecto en el modelo del CRUD (CU-01, CU-12, CU-20, CU-21, CU-22) no se mapean a campos.",
]

# (pregunta, dirigida a, respuesta, estado). Numeración idéntica a la del comentario publicado en la issue #356.
# La respuesta resume el comentario del LT en la issue; lo que se definió en la sesión de socialización (1 de octubre de 2026)
# se marca como "Sesión". Lo que no se trató en la sesión queda como "Abierta".
PREGUNTAS = [
    ("Origen del esquema: ¿la base de datos de desarrollo/pruebas se creó con el DDL o con synchronize de TypeORM? Define qué lado se corrige en A1. ¿Es posible acceso de solo lectura?",
     "Líder Técnico",
     "El LT compartió el diagrama del modelo actual de la BD de pruebas para confirmar tablas y campos, y pidió sincronizar con los cambios de la estabilización.",
     "Resuelta"),
    ("Servicio dueño del proveedor (natural, jurídica, consorcio, unión temporal, representante legal): ¿terceros_crud, otro sistema o no existe aún?",
     "Líder Técnico",
     "Los datos se consultan de Ágora (compartió las tablas). Con la referencia actual Argo puede manejarlos; en la nueva versión de Ágora pueden migrarse a terceros.",
     "Resuelta"),
    ("Novedades: ¿existe o existirá un CRUD aparte, o se modelan en gestion_contractual_crud? ¿Liquidación y terminación son novedades o entidades propias?",
     "Líder Técnico",
     "Existe el sistema de novedades para CPS; el nuevo Argo debe manejar novedades para cualquier tipo de contrato. Ese módulo se analiza desde requerimientos y no afecta el módulo contractual. No se respondió sobre liquidación y terminación.",
     "Resuelta (fuera de alcance)"),
    ("Información financiera del CDP: ¿se consulta al sistema financiero, se guarda el valor comprometido por contrato u otro criterio?",
     "Líder Técnico",
     "numero_cdp_id guarda la referencia para la consulta directa a la fuente de datos (SICAPITAL).",
     "Resuelta"),
    ("Borrado lógico: ¿los GET excluyen los inactivos por defecto o cada consumidor filtra?",
     "Líder Técnico",
     "Se debe manejar eliminado lógico y, mediante los filtros, consultar solo activos.",
     "Resuelta"),
    ("Consumidores del CRUD: ¿qué MIDs o clientes lo consumen hoy? ¿Alguno está en producción?",
     "Líder Técnico",
     "Actualmente solo lo consume el MID. No se trató en la sesión.",
     "Abierta"),
    ("Organización de los ajustes: ¿una issue por ajuste, una por fase o un esquema mixto?",
     "Líder Técnico",
     "Integrar los cambios con base en la estabilización. Es posible una migración de framework después de la presentación al usuario, así que los ajustes se resuelven sobre el modelo, tanto para la migración como si se mantiene el actual. El formato de las issues no se trató en la sesión.",
     "Abierta"),
    ("Proceso contractual: ¿el contrato existe desde la etapa precontractual o el proceso y el estudio previo son entidades propias?",
     "Analista de RQ",
     "Comentario: se remitió a la sesión de socialización. Sesión: stand by.",
     "Stand by"),
    ("numero_contrato: ¿es el número oficial vigente o solo el legado de ARGO v1? ¿Debe ser único por vigencia?",
     "Analista de RQ",
     "Es un identificador único por vigencia, por confirmar con LT y Analista. No se trató en la sesión.",
     "Abierta"),
    ("Fecha de suscripción: ¿campo del contrato o evento 'suscrito' en el historial de estados?",
     "Analista de RQ",
     "Sesión: opción a), campo del contrato. Nota: \"2 estados el que ve el usuario\". Comentario: confirmar si ocurre al momento de la firma, una vez finalizado el flujo de aprobación.",
     "Resuelta (momento del registro abierto)"),
    ("Cardinalidad: ¿un contrato puede tener más de un contratista, solicitante, lugar de ejecución u ordenador del gasto?",
     "Analista de RQ",
     "Comentario: validar contra el modelo de la BD de pruebas y confirmar con analista y LT. Sesión: todas 1:1, en stand by.",
     "Stand by"),
    ("Documentos: ¿una sola tabla con etapa y carácter por parámetro? ¿Se asocian a otras entidades? ¿Tienen estados?",
     "Analista de RQ",
     "Los documentos no tienen estado. Las otras dos preguntas no se respondieron; por el criterio de no rediseñar se mantiene una sola tabla asociada al contrato.",
     "Parcial"),
    ("Póliza: ¿se necesita historial de aprobaciones y devoluciones con motivo, o basta con el estado actual?",
     "Analista de RQ",
     "Comentario: confirmar el flujo con el analista (@cjgonzalezp). Sesión: stand by.",
     "Stand by"),
    ("Estudio previo: ¿valor_estimado y plazo_estimado se conservan aparte de los contratados?",
     "Analista de RQ",
     "Comentario: duda no entendida, se remitió a la sesión de socialización. Sesión: stand by, pero son valores separados de los contratados.",
     "Stand by"),
    ("Entidades sin atributos: ¿habrá una versión del diccionario con atributos, tipos y obligatoriedad? ¿Qué significa OTH?",
     "Analista de RQ",
     "El diccionario es el insumo; para las entidades sin atributos se tendrá presente el modelo general para profundizar en la contratación actual y validar contra las entidades de Argo v2. Sesión: no se sabe qué significa OTH.",
     "Parcial"),
    ("CU-07 (precotizaciones) y CU-19 (flujo de firmas) no tienen entidad en el diccionario: ¿se modelan?",
     "Analista de RQ",
     "El proceso de firma se hace mediante la integración con otro servicio (\"tener presente la tabla documento_...\", así en el comentario). No se respondió sobre CU-07 y no se trató en la sesión.",
     "Abierta"),
]

SESION = dict(
    fecha="Jueves 1 de octubre de 2026",
    asistentes="Heiner Edwar Granados (Líder Técnico, @edwargl7), Analista de Requerimientos (@cjgonzalezp), Andrés Torres",
)

# (id, tema, responsable, qué se necesita para cerrarla, estado). Se propone cerrarlas en issues de seguimiento,
# sin bloquear la aprobación del análisis.
DECISIONES_ABIERTAS = [
    ("D1", "Consumidores del CRUD además del MID (pregunta 6)", "LT",
     "Listar los MIDs y clientes que consumen el CRUD, y si alguno está en producción, para coordinar A1.", "Abierta"),
    ("D2", "Formato de las issues de los ajustes (pregunta 7)", "LT",
     "Elegir una issue por ajuste, una por fase o un esquema mixto.", "Abierta"),
    ("D3", "Proceso contractual (pregunta 8)", "Analista",
     "Definir si el modelo actual necesita el campo de proceso y los campos faltantes del estudio previo (A8).", "Stand by"),
    ("D4", "Unicidad de numero_contrato por vigencia (pregunta 9)", "LT",
     "Confirmar la regla con el Analista y verificar que no haya duplicados antes de crear el UNIQUE (A14).", "Abierta"),
    ("D5", "Momento del registro de fecha_suscripcion (pregunta 10)", "Analista",
     "Definir si se registra al firmar, una vez terminado el flujo de aprobación (A6).", "Abierta"),
    ("D6", "Alcance de la nota \"2 estados el que ve el usuario\" (pregunta 10)", "LT",
     "Confirmar que estado_parametro_id es el estado visible para el usuario y estado_interno_parametro_id el interno.", "Abierta"),
    ("D7", "Cardinalidad 1:1 del contrato (pregunta 11)", "Analista",
     "Confirmar que un contrato tiene un solo contratista, solicitante, lugar de ejecución y ordenador, para agregar el UNIQUE (A12).", "Stand by"),
    ("D8", "Estado de la póliza (pregunta 13)", "Analista",
     "Definir el flujo de aprobación y devolución para agregar el campo de estado (A7).", "Stand by"),
    ("D9", "Valor y plazo estimados del estudio previo (pregunta 14)", "Analista",
     "Confirmar que se agregan como campos separados de los contratados (A8).", "Stand by"),
    ("D10", "Flujo de firmas y precotizaciones (pregunta 16)", "LT",
     "Identificar el servicio de firma y la tabla documento_... que se debe tener presente; definir si CU-07 se modela.", "Abierta"),
    ("D11", "Liquidación", "Analista",
     "Definir si es una novedad (fuera de alcance) o se modela en el módulo contractual.", "Abierta"),
    ("D12", "Terminación como novedad", "Analista",
     "Confirmar el supuesto de que es una novedad, como en ARGO v1 (terminacion_anticipada).", "Abierta"),
    ("D13", "Significado de OTH (pregunta 15)", "Analista", "Definirlo al completar el diccionario (A13).", "Abierta"),
    ("D14", "Tablas poliza y amparo_poliza en pruebas", "LT",
     "Confirmar si la migración de la issue #351 (PR #38) ya se aplicó en ese ambiente.", "Abierta"),
]

LEYENDA = [
    ("Equivalente", "El campo existe con el mismo significado y nombre."),
    ("Nombre distinto", "El campo existe con el mismo significado pero otro nombre o ubicación."),
    ("Tipo / precisión", "El campo existe pero su tipo o precisión no es consistente con el lineamiento o con otras tablas."),
    ("Cobertura parcial", "El CRUD cubre solo una parte del concepto."),
    ("Relación / estructura distinta", "El concepto existe pero modelado con otra estructura o cardinalidad."),
    ("Faltante en CRUD", "El concepto no existe en el CRUD."),
    ("Externo al CRUD", "El dato pertenece a otro sistema (Ágora, SICAPITAL, OIKOS, gestor documental)."),
    ("Sin definición en diccionario", "La entidad del diccionario solo tiene identificador; no se puede comparar campo a campo."),
    ("Fuera de alcance", "El concepto no se gestiona en el módulo contractual (novedades y terminación, respuesta 3)."),
    ("Descartado", "Se decidió que el concepto no existe y no se modela (estado de documento, respuesta 12)."),
    ("Severidad Alta", "Un caso de uso no tiene soporte en el modelo, o hay riesgo de integridad o de pérdida de datos."),
    ("Severidad Media", "Requiere cambio de esquema con impacto en endpoints, o una decisión de negocio."),
    ("Severidad Baja", "Nomenclatura, documentación o lineamiento sin impacto funcional."),
    ("Severidad Ninguna", "Sin brecha o sin acción."),
]
