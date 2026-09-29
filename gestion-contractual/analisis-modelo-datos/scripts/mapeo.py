"""Mapeo diccionario de datos (RQ v2.0, 08-06-2026) -> gestion_contractual_crud.

Cada fila: (hoja, campo, tabla_crud, columna_crud, tipo_brecha, severidad, recomendacion, casos_uso, origen_v1, validar)

- tabla_crud / columna_crud vacíos cuando no hay equivalente en el CRUD.
- Para referencias a otros servicios se usa el prefijo "externo:" en tabla_crud.
- origen_v1 se toma de modelo-database/README.md y del diagrama del modelo ARGO v1 adjunto a la issue.
"""

EQUIVALENTE = "Equivalente"
NOMBRE = "Nombre distinto"
TIPO = "Tipo / precisión"
FALTANTE = "Faltante en CRUD"
ESTRUCTURA = "Relación / estructura distinta"
PARCIAL = "Cobertura parcial"
EXTERNO = "Externo al CRUD"
SIN_DEF = "Sin definición en diccionario"

TIPOS_BRECHA = [EQUIVALENTE, NOMBRE, TIPO, PARCIAL, ESTRUCTURA, FALTANTE, EXTERNO, SIN_DEF]
SEVERIDADES = ["Alta", "Media", "Baja", "Ninguna"]

EXT_PROV = "externo:proveedores/terceros"
REC_PROV = ("Dato del proveedor: no se modela en gestion_contractual_crud. Confirmar el microservicio dueño "
            "(terceros_crud u otro) y consumirlo por identificador desde el MID.")

M = []


def fila(hoja, campo, tabla, columna, brecha, sev, rec, cu="", v1="", validar="No"):
    M.append(dict(hoja=hoja, campo=campo, tabla=tabla, columna=columna, brecha=brecha, severidad=sev,
                  recomendacion=rec, cu=cu, v1=v1, validar=validar))


# --- Proveedor y especializaciones (dominio externo al CRUD) ---------------------------------------
for campo in ["id_proveedor", "tipo_proveedor", "tipo_identificacion", "numero_identificacion", "digito_verificacion",
              "nombre_razon_social", "estado_registro", "fecha_registro", "fecha_actualizacion",
              "fecha_vencimiento_registro", "correo", "telefono", "direccion", "ciudad", "departamento", "pais",
              "observaciones"]:
    fila("Proveedor", campo, EXT_PROV, "", EXTERNO, "Baja", REC_PROV, "CU-02, CU-03", "", "Sí")
# Campos de proveedor que sí tienen un reflejo en el CRUD (tabla contratista)
M[[m["campo"] for m in M].index("numero_identificacion")].update(
    tabla="contratista", columna="numero_documento", brecha=NOMBRE, severidad="Baja",
    recomendacion="Equivalente como referencia al proveedor. Unificar nombre (numero_identificacion vs numero_documento) en el diccionario o en el CRUD.",
    v1="contrato.contratista (numeric → varchar)")
M[[m["campo"] for m in M].index("tipo_proveedor")].update(
    tabla="contratista", columna="tipo_persona_id", brecha=PARCIAL, severidad="Media",
    recomendacion="tipo_persona_id cubre natural/jurídica. Verificar que el parámetro incluya consorcio y unión temporal (CU-06).",
    validar="Sí")

for campo in ["id_persona_natural", "id_proveedor", "nombres", "apellidos", "fecha_nacimiento", "sexo", "nacionalidad",
              "profesion", "nivel_formacion", "perfil_cps", "tarjeta_profesional", "es_pensionado",
              "es_funcionario_publico", "tiene_inhabilidades"]:
    fila("PersonaNatural", campo, EXT_PROV, "", EXTERNO, "Baja", REC_PROV, "CU-03", "", "Sí")
M[-5].update(tabla="contrato_general", columna="perfil_contratista_id", brecha=ESTRUCTURA, severidad="Media",
             recomendacion="En el CRUD el perfil se guarda por contrato; en el diccionario, por persona. Definir si el perfil CPS es atributo del proveedor, del contrato o de ambos.",
             validar="Sí")

for campo in ["id_persona_juridica", "id_proveedor", "nit", "razon_social", "tipo_sociedad", "camara_comercio",
              "fecha_constitucion", "actividad_economica", "codigo_ciiu", "regimen_tributario", "estado_empresa"]:
    fila("PersonaJuridica", campo, EXT_PROV, "", EXTERNO, "Baja", REC_PROV, "CU-05", "", "Sí")

for campo in ["id_representante", "id_persona_juridica", "tipo_identificacion", "numero_identificacion", "nombres",
              "apellidos", "correo", "telefono", "fecha_inicio_representacion", "fecha_fin_representacion"]:
    fila("RepresentanteLegal", campo, EXT_PROV, "", EXTERNO, "Baja", REC_PROV, "CU-05", "", "Sí")

REC_STUB = "El diccionario solo define el identificador. Completar atributos en el diccionario antes de modelar."
fila("UnionTemporal", "id_union_temporal", EXT_PROV, "", SIN_DEF, "Media",
     REC_STUB + " CU-06 exige integrantes y porcentajes de participación (numeric(5,4)).", "CU-06", "", "Sí")
fila("Consorcio", "id_consorcio", EXT_PROV, "", SIN_DEF, "Media",
     REC_STUB + " Misma estructura que unión temporal: evaluar una sola entidad con tipo.", "CU-06", "", "Sí")
fila("Evaluacion", "id_evaluacion", "", "", SIN_DEF, "Media",
     REC_STUB + " CU-08 la asocia a contrato y proveedor: si se modela aquí, requiere contrato_general_id.",
     "CU-08", "", "Sí")
fila("Caracterizacion", "id_caracterizacion", EXT_PROV, "", SIN_DEF, "Baja",
     REC_STUB + " CU-04 indica datos sensibles con acceso restringido: no pertenece al CRUD contractual.", "CU-04", "", "Sí")
fila("Certificacion", "id_certificacion", "", "", SIN_DEF, "Baja",
     REC_STUB + " CU-09 la genera a partir de contratos existentes: puede resolverse como documento generado en un MID, sin tabla propia.",
     "CU-09", "", "Sí")

# --- Contrato --------------------------------------------------------------------------------------
H = "Contrato"
fila(H, "id_contrato", "contrato_general", "id", EQUIVALENTE, "Ninguna", "Sin cambios.", "CU-11", "contrato (numero_contrato + vigencia)")
fila(H, "numero_contrato", "contrato_general", "numero_contrato", ESTRUCTURA, "Media",
     "En el CRUD está documentado como 'campo legado' de la migración v1, pero el diccionario lo trata como número oficial. Definir si es el número oficial vigente y cómo se genera (existe POST /contratos-generales/conteo-numero-contrato).",
     "CU-11, CU-19", "contrato.numero_contrato", "Sí")
fila(H, "vigencia", "contrato_general", "vigencia", TIPO, "Baja",
     "vigencia es varchar(4) en contrato_general e integer en disponibilidad_presupuestal, registro_presupuestal y convenio. Unificar el tipo de dato del año.",
     "CU-02", "contrato.vigencia")
fila(H, "id_proceso", "", "", FALTANTE, "Alta",
     "No existe el concepto de proceso contractual (CU-11: proceso creado desde el estudio previo, con modalidad, supervisor y abogado). Definir si el proceso es una entidad propia o si contrato_general cumple ese rol desde la etapa precontractual.",
     "CU-11, CU-13", "solicitud_necesidad (otra BD)", "Sí")
fila(H, "id_proveedor", "contratista", "contrato_general_id", ESTRUCTURA, "Media",
     "Relación invertida: el diccionario pone el proveedor en el contrato; el CRUD guarda el contrato en contratista (1:1 en la entidad, 1:N en el DDL). Definir cardinalidad (¿consorcios con varios integrantes?) y alinear DDL y entidad.",
     "CU-11, CU-15", "contrato.contratista", "Sí")
fila(H, "modalidad", "contrato_general", "modalidad_seleccion_id", NOMBRE, "Baja",
     "Equivalente como referencia a Parámetros CRUD. Ajustar el nombre en el diccionario.", "CU-11, CU-12", "contrato.modalidad_seleccion")
fila(H, "tipo_contrato", "contrato_general", "tipo_contrato_id", NOMBRE, "Baja",
     "Equivalente como referencia a Parámetros CRUD.", "CU-11, CU-12", "contrato.tipo_contrato")
fila(H, "objeto", "contrato_general", "objeto", EQUIVALENTE, "Baja",
     "Equivalente. Definir longitud del varchar (lineamiento).", "CU-10, CU-11", "contrato.objeto_contrato")
fila(H, "valor_contrato", "contrato_general", "valor_pesos", TIPO, "Media",
     "Nombre distinto y precisión numeric(16,2) frente al lineamiento numeric(20,7). Hay además valor_contrato_me y valor_tasa_cambio que el diccionario no contempla.",
     "CU-02, CU-11", "contrato.valor_contrato")
fila(H, "plazo", "contrato_general", "plazo_ejecucion", NOMBRE, "Baja",
     "El CRUD separa cantidad (plazo_ejecucion) y unidad (unidad_ejecucion_id). Reflejar la unidad en el diccionario.",
     "CU-11", "contrato.plazo_ejecucion + unidad_ejecucion")
fila(H, "fecha_suscripcion", "", "", FALTANTE, "Alta",
     "No hay columna para la fecha de firma del contrato (fecha_suscripcion_estudio es la del estudio previo). En v1 existía contrato_suscrito. Definir si se agrega la columna o si se obtiene del evento de estado 'suscrito' en estado_contrato.",
     "CU-19", "contrato_suscrito.fecha_suscripcion", "Sí")
fila(H, "fecha_inicio", "contrato_general", "fecha_inicial", NOMBRE, "Media",
     "Nombre distinto y dato duplicado con acta_inicio.fecha_inicio. Definir cuál es la fuente de verdad.",
     "CU-02", "acta_inicio.fecha_inicio", "Sí")
fila(H, "fecha_terminacion", "contrato_general", "fecha_final", NOMBRE, "Media",
     "Nombre distinto y dato duplicado con acta_inicio.fecha_fin. Las novedades (prórroga) cambian la fecha final: definir si se recalcula o se versiona.",
     "CU-02, CU-18", "acta_inicio.fecha_fin", "Sí")
fila(H, "estado_contrato", "estado_contrato", "estado_parametro_id", ESTRUCTURA, "Baja",
     "El CRUD modela el estado como historial (tabla estado_contrato con actual = true). Es más completo que un atributo: reflejarlo así en el diccionario.",
     "CU-19, CU-20", "contrato_estado / estado_contrato")

# --- Proyectos y dependencia ----------------------------------------------------------------------
fila("Proyectos de Extension", "id_proyecto_extension", "", "", SIN_DEF, "Media",
     REC_STUB + " CU-15 (contratación derivada IDEXUD) necesita asociar contratos a proyecto: hoy no hay columna que lo soporte.",
     "CU-15", "idexud_proyecto", "Sí")
fila("Proyectos de Investigacion", "id_proyecto_investigacion", "", "", SIN_DEF, "Baja",
     REC_STUB + " No hay caso de uso asociado.", "", "", "Sí")
fila("Dependencia", "id_dependencia", "externo:OIKOS", "", EXTERNO, "Ninguna",
     "El CRUD referencia dependencias de OIKOS (solicitante.dependencia_solicitante_id, supervisor_contrato.dependencia_id, lugar_ejecucion.dependencia_id). No se replica.",
     "CU-10, CU-17", "dependencia_SIC")

# --- Documentos (cinco hojas con la misma estructura) ---------------------------------------------
DOCS = {
    "Documentos Pre-Contractuales": ("id_documento_precontractual", "CU-03, CU-10"),
    "Documentos Publicos": ("id_documento_publico", ""),
    "Documentos Contractuales": ("id_documento_contractual", "CU-13, CU-19"),
    "Documentos Privados": ("id_documento_privado", ""),
    "Documentos Pos-Contractuales": ("id_documento_poscontractual", ""),
}
for hoja, (pk, cu) in DOCS.items():
    fila(hoja, pk, "documento_contrato", "id", ESTRUCTURA, "Media",
         "El diccionario define cinco entidades de documento con la misma estructura; el CRUD tiene una sola (documento_contrato). Recomendado: mantener una tabla y distinguir etapa y carácter (público/privado) por parámetro.",
         cu, "estudio_documento_previo / documento", "Sí")
    fila(hoja, "entidad_relacionada", "", "", ESTRUCTURA, "Media",
         "El CRUD solo asocia documentos al contrato (contrato_general_id). El diccionario permite asociarlos a cualquier entidad (proveedor, estudio previo, póliza, novedad). Definir si se requiere asociación polimórfica.",
         cu, "", "Sí")
    fila(hoja, "id_entidad_relacionada", "documento_contrato", "contrato_general_id", ESTRUCTURA, "Media",
         "Ver entidad_relacionada.", cu)
    fila(hoja, "tipo_documento", "documento_contrato", "tipo_documento_id", EQUIVALENTE, "Ninguna",
         "Equivalente como referencia a Parámetros CRUD.", cu)
    fila(hoja, "nombre_archivo", "externo:gestor documental", "", EXTERNO, "Baja",
         "El nombre del archivo lo gestiona el Gestor Documental (documento_id). No se replica salvo que se requiera para consultas.", cu)
    fila(hoja, "ruta_archivo", "documento_contrato", "documento_enlace", NOMBRE, "Baja",
         "documento_enlace varchar(50) guarda el identificador del Gestor Documental, no una ruta. Confirmar que 50 caracteres bastan.", cu)
    fila(hoja, "fecha_cargue", "documento_contrato", "fecha_creacion", NOMBRE, "Ninguna",
         "Equivalente mediante columna de auditoría.", cu)
    fila(hoja, "estado_documento", "documento_contrato", "actual", PARCIAL, "Baja",
         "El CRUD solo tiene activo y actual (esta última existe en la entidad, no en el DDL). Si el documento tiene estados (cargado, aprobado, rechazado) se requiere columna o historial.",
         cu, "", "Sí")

# --- Necesidad, SECOP, OTH ------------------------------------------------------------------------
fila("Necesidad", "id_necesidad", "", "", SIN_DEF, "Media",
     REC_STUB + " En v1 la necesidad vivía en otra base (solicitud_necesidad). Confirmar si existe un servicio de necesidades en Argo V2.",
     "CU-10", "solicitud_necesidad", "Sí")
fila("Secop", "id_secop", "", "", SIN_DEF, "Media",
     REC_STUB + " No hay en el CRUD ningún identificador de publicación en SECOP.", "", "", "Sí")
fila("OTH", "id_oth", "", "", SIN_DEF, "Baja",
     REC_STUB + " Confirmar el significado de la sigla con el Analista de Requerimientos.", "", "", "Sí")

# --- Estudio previo -------------------------------------------------------------------------------
H = "EstudioPrevio"
REC_EP = ("El CRUD no tiene entidad de estudio previo: sus datos están embebidos en contrato_general. "
          "Si CU-11 crea el proceso a partir del estudio previo, conviene separarlo en su propia tabla.")
fila(H, "id_estudio_previo", "", "", FALTANTE, "Alta", REC_EP, "CU-10, CU-11", "estudio_documento_previo", "Sí")
fila(H, "numero_estudio", "", "", FALTANTE, "Media",
     "Sin consecutivo de estudio. consecutivo_elaboracion está documentado como campo legado: confirmar si cumple este rol.",
     "CU-10", "", "Sí")
fila(H, "fecha_estudio", "contrato_general", "fecha_suscripcion_estudio", NOMBRE, "Baja",
     "Equivalente, ubicado en contrato_general.", "CU-10", "estudio_documento_previo.fecha_suscripcion")
fila(H, "dependencia_solicitante", "solicitante", "dependencia_solicitante_id", NOMBRE, "Baja",
     "Equivalente en tabla solicitante (referencia OIKOS). Relación 1:1 en la entidad y 1:N en el DDL.",
     "CU-10", "contrato.dependencia_solicitante")
fila(H, "necesidad", "", "", FALTANTE, "Media",
     "Sin campo de necesidad. justificacion es cercano pero no equivalente.", "CU-10", "", "Sí")
fila(H, "objeto_contrato", "contrato_general", "objeto", NOMBRE, "Baja", "Equivalente en contrato_general.",
     "CU-10", "contrato.objeto_contrato")
fila(H, "justificacion", "contrato_general", "justificacion", EQUIVALENTE, "Baja",
     "Equivalente en contrato_general. Definir longitud del varchar.", "CU-10", "contrato.justificacion")
fila(H, "actividades", "contrato_general", "actividades", EQUIVALENTE, "Baja",
     "Equivalente en contrato_general. Definir longitud del varchar.", "CU-10", "contrato.actividades")
fila(H, "obligaciones", "", "", FALTANTE, "Media",
     "Sin campo de obligaciones. Confirmar si contrato_general.condiciones lo cubre.", "CU-10", "", "Sí")
fila(H, "valor_estimado", "", "", FALTANTE, "Media",
     "Solo existe el valor final del contrato (valor_pesos). Si el valor estimado del estudio previo difiere del contratado, se requiere columna propia numeric(20,7).",
     "CU-10", "", "Sí")
fila(H, "plazo_estimado", "", "", FALTANTE, "Baja",
     "Solo existe el plazo del contrato (plazo_ejecucion). Mismo criterio que valor_estimado.", "CU-10", "", "Sí")

# --- CDP y RP -------------------------------------------------------------------------------------
H = "CDP"
REC_FIN = ("Dato del documento financiero: vive en el sistema financiero. No replicar; consultarlo desde el MID "
           "al validar disponibilidad (CU-16).")
fila(H, "id_cdp", "disponibilidad_presupuestal", "id", EQUIVALENTE, "Ninguna", "Sin cambios.", "CU-16", "contrato_disponibilidad")
fila(H, "numero_cdp", "disponibilidad_presupuestal", "numero_cdp_id", NOMBRE, "Baja",
     "El sufijo _id sugiere llave foránea, pero el comentario lo define como número del CDP. Definir cuál de los dos es.",
     "CU-16", "contrato_disponibilidad.numero_cdp", "Sí")
fila(H, "vigencia", "disponibilidad_presupuestal", "vigencia_cdp", NOMBRE, "Baja", "Equivalente.", "CU-16",
     "contrato_disponibilidad.vigencia_cdp")
fila(H, "fecha_cdp", "disponibilidad_presupuestal", "fecha_registro", NOMBRE, "Baja",
     "Confirmar si fecha_registro es la fecha del CDP o la fecha en que se asoció al contrato.", "CU-16",
     "contrato_disponibilidad.fecha_registro", "Sí")
for campo in ["valor_cdp", "saldo_disponible", "tipo_recurso", "rubro", "proyecto_inversion"]:
    fila(H, campo, "externo:financiera", "", EXTERNO, "Baja", REC_FIN, "CU-16", "", "Sí")
M[-3].update(recomendacion=REC_FIN + " A nivel de contrato existen tipo_gasto_id y tema_gasto_inversion_id.")

fila("RP", "id_rp", "registro_presupuestal", "id", PARCIAL, "Alta",
     "La tabla registro_presupuestal existe en el DDL (ligada a CDP por cdp_id) pero no tiene entidad, módulo ni endpoints. CU-16 exige registrar el RP: falta exponerla. Además, la FK cdp_id no sigue el lineamiento (<tabla>_id → disponibilidad_presupuestal_id).",
     "CU-16", "registro_presupuestal_disponibilidad")

# --- Póliza ---------------------------------------------------------------------------------------
H = "Poliza"
fila(H, "id_poliza", "poliza", "id", EQUIVALENTE, "Ninguna", "Sin cambios.", "CU-14", "poliza.id_poliza")
fila(H, "id_contrato", "poliza", "contrato_general_id", NOMBRE, "Ninguna", "Equivalente (FK a contrato_general).", "CU-14",
     "poliza.numero_contrato + vigencia")
fila(H, "numero_poliza", "poliza", "numero_poliza", EQUIVALENTE, "Ninguna", "Sin cambios.", "CU-14", "poliza.numero_poliza")
fila(H, "aseguradora", "poliza", "entidad_aseguradora_id", NOMBRE, "Baja", "Equivalente como referencia a Parámetros CRUD.",
     "CU-14", "poliza.entidad_aseguradora")
fila(H, "fecha_expedicion", "poliza", "fecha_expedicion", EQUIVALENTE, "Ninguna", "Sin cambios.", "CU-14", "poliza.fecha_expedicion")
fila(H, "fecha_inicio_vigencia", "poliza", "fecha_inicio", NOMBRE, "Baja", "Equivalente.", "CU-14", "poliza.fecha_inicio")
fila(H, "fecha_fin_vigencia", "poliza", "fecha_fin", NOMBRE, "Baja", "Equivalente.", "CU-14", "poliza.fecha_fin")
fila(H, "valor_asegurado", "amparo_poliza", "valor", ESTRUCTURA, "Baja",
     "El valor se registra por amparo, no por póliza. El valor de la póliza es la suma de sus amparos: reflejar la entidad amparo en el diccionario.",
     "CU-14", "amparo_poliza.valor_amparo")
fila(H, "estado_poliza", "", "", FALTANTE, "Media",
     "La póliza solo tiene activo y fecha_aprobacion. CU-14 permite aprobar o devolver: se requiere estado (y posiblemente historial con motivo de devolución).",
     "CU-14", "poliza.estado", "Sí")
fila("Aprobacion Poliza", "id_aprobacion_poliza", "poliza", "fecha_aprobacion", PARCIAL, "Media",
     "El CRUD guarda solo la última aprobación (fecha_aprobacion, usuario_id). Si se requiere trazabilidad de devoluciones, modelar historial.",
     "CU-14", "", "Sí")

# --- Acta de inicio, liquidación, novedades, terminación -----------------------------------------
fila("Acta de inicio", "id_acta_inicio", "acta_inicio", "id", EQUIVALENTE, "Ninguna",
     "El CRUD ya modela el acta (fechas, descripción, usuario). Completar el diccionario con esos atributos.",
     "", "acta_inicio")
fila("Liquidacion", "id_liquidacion", "", "", SIN_DEF, "Media",
     REC_STUB + " En v1 existía contrato_liquidado (fecha, número de acta, observaciones, documento).",
     "", "contrato_liquidado", "Sí")

H = "Novedad"
REC_NOV = ("No hay novedades en gestion_contractual_crud. En v1 existían novedad_contractual y tablas por tipo "
           "(adición, prórroga, suspensión, cesión, cambio de supervisor). Confirmar si Argo V2 tiene un CRUD de novedades antes de modelarlas aquí.")
for campo in ["id_novedad", "id_contrato", "tipo_novedad", "numero_novedad", "fecha_solicitud", "fecha_aprobacion",
              "descripcion", "nuevo_valor_contrato", "nueva_fecha_terminacion", "estado_novedad"]:
    fila(H, campo, "", "", FALTANTE, "Alta" if campo == "id_novedad" else "Media", REC_NOV if campo == "id_novedad" else "Ver id_novedad.",
         "CU-18", "novedad_contractual", "Sí")
fila("Terminacion", "id_terminacion", "", "", SIN_DEF, "Baja",
     REC_STUB + " En v1 era un tipo de novedad (terminacion_anticipada). Definir si es novedad o entidad propia.",
     "CU-18", "terminacion_anticipada", "Sí")


# --- Tablas del CRUD sin entidad en el diccionario (dirección inversa) -----------------------------
CRUD_SIN_DICCIONARIO = {
    "supervisor_contrato": ("CU-17 asigna supervisor, pero el diccionario no tiene entidad Supervisor.", "Media"),
    "ordenador_contrato": ("CU-19 menciona al ordenador del gasto; el diccionario no lo define.", "Media"),
    "amparo_poliza": ("CU-14 registra amparos; el diccionario solo tiene Poliza.", "Media"),
    "estado_contrato": ("El diccionario trata el estado como atributo del contrato.", "Baja"),
    "solicitante": ("El diccionario solo lo menciona como campo de EstudioPrevio.", "Baja"),
    "lugar_ejecucion": ("Sin equivalente en el diccionario.", "Baja"),
    "especificacion_tecnica": ("Sin equivalente en el diccionario (items del contrato).", "Baja"),
    "contrato_arrendamiento": ("Sin equivalente en el diccionario. Existe en DDL sin entidad ni endpoints.", "Baja"),
    "convenio": ("Sin equivalente en el diccionario. Existe en DDL sin entidad ni endpoints.", "Baja"),
}
