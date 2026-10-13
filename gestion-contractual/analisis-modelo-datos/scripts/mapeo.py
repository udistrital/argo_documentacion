"""Mapeo diccionario de datos (RQ v2.0, 08-06-2026) -> gestion_contractual_crud.

Cada fila: (hoja, campo, tabla_crud, columna_crud, tipo_brecha, severidad, recomendacion, casos_uso, origen_v1, validar)

- tabla_crud / columna_crud vacíos cuando no hay equivalente en el CRUD.
- Para referencias a otros servicios se usa el prefijo "externo:" en tabla_crud.
- origen_v1 se toma de modelo-database/README.md y del diagrama del modelo ARGO v1 adjunto a la issue.
- Las recomendaciones siguen el criterio acordado con el LT: no se proponen rediseños (entidades nuevas que
  reemplacen o partan las existentes, ni cambios de estructura). Solo alinear con la BD de pruebas, corregir
  lineamientos que no rompan integraciones y agregar campos al modelo actual cuando se confirmen.
- Las respuestas del LT se citan por número de pregunta (comentario de la issue #356 y sesión de socialización del 1 de octubre de 2026).
"""

EQUIVALENTE = "Equivalente"
NOMBRE = "Nombre distinto"
TIPO = "Tipo / precisión"
FALTANTE = "Faltante en CRUD"
ESTRUCTURA = "Relación / estructura distinta"
PARCIAL = "Cobertura parcial"
EXTERNO = "Externo al CRUD"
SIN_DEF = "Sin definición en diccionario"
FUERA = "Fuera de alcance"
DESCARTADO = "Descartado"

TIPOS_BRECHA = [EQUIVALENTE, NOMBRE, TIPO, PARCIAL, ESTRUCTURA, FALTANTE, EXTERNO, SIN_DEF, FUERA, DESCARTADO]
SEVERIDADES = ["Alta", "Media", "Baja", "Ninguna"]

EXT_AGORA = "externo:Ágora"
EXT_SICAPITAL = "externo:SICAPITAL"

M = []


def fila(hoja, campo, tabla, columna, brecha, sev, rec, cu="", v1="", validar="No"):
    M.append(dict(hoja=hoja, campo=campo, tabla=tabla, columna=columna, brecha=brecha, severidad=sev,
                  recomendacion=rec, cu=cu, v1=v1, validar=validar))


def actualizar(hoja, campo, **cambios):
    next(m for m in M if m["hoja"] == hoja and m["campo"] == campo).update(**cambios)


# --- Mapeo a Ágora (respuesta 2) -------------------------------------------------------------------
# (hoja, campo) -> (tabla Ágora, [columnas], cobertura, observación)
# Transcripción de las imágenes en fuentes/agora.json. Los nombres truncados en el diagrama se dejan con "…".
# Cobertura: "Sí" (columna equivalente), "Aproximada" (cubre el concepto con otro alcance), "No visible".
MAPEO_AGORA = {
    ("Proveedor", "id_proveedor"): ("informacion_proveedor", ["id_proveedor"], "Sí", ""),
    ("Proveedor", "tipo_proveedor"): ("informacion_proveedor", ["tipopersona"], "Sí",
                                      "Consorcios y uniones temporales se registran en informacion_sociedad_temp…."),
    ("Proveedor", "tipo_identificacion"): ("informacion_persona_natural", ["tipo_documento"], "Aproximada",
                                           "Solo para persona natural. informacion_proveedor no tiene columna visible de tipo de documento."),
    ("Proveedor", "numero_identificacion"): ("informacion_proveedor", ["num_documento"], "Sí", ""),
    ("Proveedor", "digito_verificacion"): ("informacion_persona_natural", ["digito_verificacion"], "Aproximada",
                                           "También en informacion_sociedad_temp…. No hay columna visible en informacion_proveedor."),
    ("Proveedor", "nombre_razon_social"): ("informacion_proveedor", ["nom_proveedor"], "Sí", ""),
    ("Proveedor", "estado_registro"): ("informacion_proveedor", ["estado"], "Sí", "Numérico; el diagrama no muestra sus valores."),
    ("Proveedor", "fecha_registro"): ("informacion_proveedor", ["fecha_registro"], "Sí", "Tipo texto, no fecha."),
    ("Proveedor", "fecha_actualizacion"): ("informacion_proveedor", ["fecha_ultima_modificacion"], "Sí", "Tipo texto, no fecha."),
    ("Proveedor", "fecha_vencimiento_registro"): ("", [], "No visible", "Sin columna visible."),
    ("Proveedor", "correo"): ("informacion_proveedor", ["correo"], "Sí", "Existe además correo_pago."),
    ("Proveedor", "telefono"): ("proveedor_telefono", ["id_telefono"], "Aproximada",
                                "La tabla de teléfonos a la que apunta id_telefono no aparece en las imágenes."),
    ("Proveedor", "direccion"): ("informacion_proveedor", ["direccion"], "Sí", ""),
    ("Proveedor", "ciudad"): ("informacion_proveedor", ["id_ciudad_contacto"], "Sí", "Referencia a la tabla ciudad."),
    ("Proveedor", "departamento"): ("ciudad", ["id_departamento", "departamento"], "Aproximada",
                                    "Se obtiene a través de informacion_proveedor.id_ciudad_contacto."),
    ("Proveedor", "pais"): ("ciudad", ["ab_pais"], "Aproximada", "Se obtiene a través de informacion_proveedor.id_ciudad_contacto."),
    ("Proveedor", "observaciones"): ("informacion_proveedor", ["descripcion"], "Aproximada", ""),

    ("PersonaNatural", "id_persona_natural"): ("informacion_persona_natural", ["num_documento_persona"], "Sí",
                                               "La PK es el número de documento."),
    ("PersonaNatural", "id_proveedor"): ("", [], "No visible",
                                         "El diagrama no muestra una columna que una informacion_persona_natural con informacion_proveedor."),
    ("PersonaNatural", "nombres"): ("informacion_persona_natural", ["primer_nombre", "segundo_nombre"], "Sí", ""),
    ("PersonaNatural", "apellidos"): ("informacion_persona_natural", ["primer_apellido", "segundo_apellido"], "Sí", ""),
    ("PersonaNatural", "fecha_nacimiento"): ("informacion_persona_natural", ["fecha_nacimiento"], "Sí", ""),
    ("PersonaNatural", "sexo"): ("informacion_persona_natural", ["genero"], "Aproximada",
                                 "Existen además identidad_genero y orientacion_sexual."),
    ("PersonaNatural", "nacionalidad"): ("informacion_persona_natural", ["id_pais_nacimiento"], "Aproximada",
                                         "País de nacimiento, que no necesariamente es la nacionalidad."),
    ("PersonaNatural", "profesion"): ("informacion_persona_natural", ["profesion"], "Sí", "Existe además especialidad."),
    ("PersonaNatural", "nivel_formacion"): ("", [], "No visible",
                                            "Sin columna visible. id_nucleo_basico apunta a snies_nucleo_basic… (núcleo básico de conocimiento), no a un nivel de formación."),
    ("PersonaNatural", "perfil_cps"): ("informacion_persona_natural", ["perfil"], "Sí", "Numérico."),
    ("PersonaNatural", "tarjeta_profesional"): ("", [], "No visible", "Sin columna visible."),
    ("PersonaNatural", "es_pensionado"): ("informacion_persona_natural", ["pensionado"], "Sí", ""),
    ("PersonaNatural", "es_funcionario_publico"): ("", [], "No visible", "Sin columna visible."),
    ("PersonaNatural", "tiene_inhabilidades"): ("inhabilidad", ["id_proveedor"], "Aproximada",
                                                "Las inhabilidades se registran en la tabla inhabilidad, por proveedor."),

    ("PersonaJuridica", "id_persona_juridica"): ("", [], "No visible", "Las imágenes no incluyen una tabla propia de persona jurídica."),
    ("PersonaJuridica", "id_proveedor"): ("informacion_proveedor", ["id_proveedor"], "Sí", ""),
    ("PersonaJuridica", "nit"): ("informacion_proveedor", ["num_documento"], "Sí", ""),
    ("PersonaJuridica", "razon_social"): ("informacion_proveedor", ["nom_proveedor"], "Sí", ""),
    ("PersonaJuridica", "tipo_sociedad"): ("", [], "No visible", "Sin columna visible."),
    ("PersonaJuridica", "camara_comercio"): ("", [], "No visible", "Sin columna visible."),
    ("PersonaJuridica", "fecha_constitucion"): ("", [], "No visible", "Sin columna visible."),
    ("PersonaJuridica", "actividad_economica"): ("proveedor_actividad_ciiu", ["id_subclase"], "Aproximada",
                                                 "La actividad se registra como subclase CIIU."),
    ("PersonaJuridica", "codigo_ciiu"): ("proveedor_actividad_ciiu", ["id_subclase"], "Sí", ""),
    ("PersonaJuridica", "regimen_tributario"): ("informacion_proveedor", ["regimen_contributivo"], "Sí", ""),
    ("PersonaJuridica", "estado_empresa"): ("informacion_proveedor", ["estado"], "Aproximada",
                                            "Estado del proveedor; no hay un estado propio de la empresa."),

    ("RepresentanteLegal", "id_representante"): ("proveedor_representante_le…", ["id_representante"], "Sí", ""),
    ("RepresentanteLegal", "id_persona_juridica"): ("proveedor_representante_le…", ["id_proveedor"], "Sí", ""),
    ("RepresentanteLegal", "tipo_identificacion"): ("informacion_persona_natural", ["tipo_documento"], "Aproximada",
                                                    "En la imagen 3 una línea une proveedor_representante_le… con informacion_persona_natural."),
    ("RepresentanteLegal", "numero_identificacion"): ("informacion_persona_natural", ["num_documento_persona"], "Aproximada",
                                                      "Misma relación que tipo_identificacion."),
    ("RepresentanteLegal", "nombres"): ("informacion_persona_natural", ["primer_nombre", "segundo_nombre"], "Aproximada",
                                        "Misma relación que tipo_identificacion."),
    ("RepresentanteLegal", "apellidos"): ("informacion_persona_natural", ["primer_apellido", "segundo_apellido"], "Aproximada",
                                          "Misma relación que tipo_identificacion."),
    ("RepresentanteLegal", "correo"): ("", [], "No visible", "Sin columna visible en informacion_persona_natural."),
    ("RepresentanteLegal", "telefono"): ("", [], "No visible", "Sin columna visible en informacion_persona_natural."),
    ("RepresentanteLegal", "fecha_inicio_representacion"): ("", [], "No visible", "Sin columna visible."),
    ("RepresentanteLegal", "fecha_fin_representacion"): ("", [], "No visible", "Sin columna visible."),

    ("UnionTemporal", "id_union_temporal"): ("informacion_sociedad_temp…", ["id_sociedad"], "Sí",
                                             "Integrantes y porcentaje de participación en informacion_sociedad_particip…."),
    ("Consorcio", "id_consorcio"): ("informacion_sociedad_temp…", ["id_sociedad"], "Sí",
                                    "Misma tabla que unión temporal; integrantes en informacion_sociedad_particip…."),
    ("Evaluacion", "id_evaluacion"): ("informacion_proveedor", ["puntaje_evaluacion", "clasificacion_evaluacion"], "Aproximada",
                                      "La evaluación está por proveedor; CU-08 la asocia al contrato."),
    ("Caracterizacion", "id_caracterizacion"): ("informacion_persona_natural",
                                                ["genero", "grupo_etnico", "comunidad_lgbt", "cabeza_familia", "discapacitado",
                                                 "tipo_discapacidad", "migrante", "victima_conflicto", "identidad_genero",
                                                 "orientacion_sexual"], "Aproximada",
                                                "Equivalencia por contenido: el diccionario solo define el identificador."),
}

OBSERVACIONES_AGORA = [
    "informacion_proveedor.fecha_registro y fecha_ultima_modificacion son de tipo texto, no fecha.",
    "La evaluación (puntaje_evaluacion, clasificacion_evaluacion) está por proveedor, mientras que CU-08 la asocia al contrato.",
    "Existen objeto_cotizacion y solicitud_cotizacio…, que tienen que ver con CU-07 (precotizaciones).",
    "No hay una tabla propia de persona jurídica: sus datos generales están en informacion_proveedor.",
    "Según el LT, en la nueva versión de Ágora estos datos pueden migrarse a terceros (respuesta 2).",
]


def rec_agora(hoja, campo):
    tabla, cols, cob, obs = MAPEO_AGORA[(hoja, campo)]
    donde = f"{tabla}.{', '.join(cols)}" if tabla else "sin columna visible en las tablas compartidas"
    nota = f" {obs}" if obs and tabla else ""
    return (f"Dato del proveedor, consultado de Ágora (respuesta 2): {donde}.{nota} No se modela en el CRUD; "
            "la referencia actual (contratista.numero_documento) es suficiente.")


# --- Proveedor y especializaciones (Ágora) ---------------------------------------------------------
for campo in ["id_proveedor", "tipo_proveedor", "tipo_identificacion", "numero_identificacion", "digito_verificacion",
              "nombre_razon_social", "estado_registro", "fecha_registro", "fecha_actualizacion",
              "fecha_vencimiento_registro", "correo", "telefono", "direccion", "ciudad", "departamento", "pais",
              "observaciones"]:
    fila("Proveedor", campo, EXT_AGORA, "", EXTERNO, "Baja", rec_agora("Proveedor", campo), "CU-02, CU-03")
# Campos de proveedor que sí tienen un reflejo en el CRUD (tabla contratista)
actualizar("Proveedor", "numero_identificacion",
           tabla="contratista", columna="numero_documento", brecha=NOMBRE,
           recomendacion="Es la referencia del CRUD al proveedor de Ágora (informacion_proveedor.num_documento). Unificar el nombre en el diccionario (numero_identificacion vs numero_documento).",
           v1="contrato.contratista (numeric → varchar)")
actualizar("Proveedor", "tipo_proveedor",
           tabla="contratista", columna="tipo_persona_id", brecha=PARCIAL,
           recomendacion="tipo_persona_id cubre natural/jurídica (en Ágora, informacion_proveedor.tipopersona). Verificar que el parámetro incluya consorcio y unión temporal, que Ágora registra en informacion_sociedad_temp… (CU-06).")

for campo in ["id_persona_natural", "id_proveedor", "nombres", "apellidos", "fecha_nacimiento", "sexo", "nacionalidad",
              "profesion", "nivel_formacion", "perfil_cps", "tarjeta_profesional", "es_pensionado",
              "es_funcionario_publico", "tiene_inhabilidades"]:
    fila("PersonaNatural", campo, EXT_AGORA, "", EXTERNO, "Baja", rec_agora("PersonaNatural", campo), "CU-03")
actualizar("PersonaNatural", "perfil_cps",
           tabla="contrato_general", columna="perfil_contratista_id", brecha=ESTRUCTURA,
           recomendacion="Sin cambio de estructura. El perfil existe por persona en Ágora (informacion_persona_natural.perfil) y por contrato en el CRUD (perfil con el que se contrata). Reflejarlo así en el diccionario.")

for campo in ["id_persona_juridica", "id_proveedor", "nit", "razon_social", "tipo_sociedad", "camara_comercio",
              "fecha_constitucion", "actividad_economica", "codigo_ciiu", "regimen_tributario", "estado_empresa"]:
    fila("PersonaJuridica", campo, EXT_AGORA, "", EXTERNO, "Baja", rec_agora("PersonaJuridica", campo), "CU-05")

for campo in ["id_representante", "id_persona_juridica", "tipo_identificacion", "numero_identificacion", "nombres",
              "apellidos", "correo", "telefono", "fecha_inicio_representacion", "fecha_fin_representacion"]:
    fila("RepresentanteLegal", campo, EXT_AGORA, "", EXTERNO, "Baja", rec_agora("RepresentanteLegal", campo), "CU-05")

REC_STUB = "El diccionario solo define el identificador."
fila("UnionTemporal", "id_union_temporal", EXT_AGORA, "", SIN_DEF, "Baja",
     REC_STUB + " En Ágora: informacion_sociedad_temp… (representante, representante_suplente) e informacion_sociedad_particip… (porcentaje_participacion). Cubre CU-06; no se modela en el CRUD.",
     "CU-06")
fila("Consorcio", "id_consorcio", EXT_AGORA, "", SIN_DEF, "Baja",
     REC_STUB + " En Ágora usa las mismas tablas que unión temporal (informacion_sociedad_temp…, informacion_sociedad_particip…). No se modela en el CRUD.",
     "CU-06")
fila("Evaluacion", "id_evaluacion", EXT_AGORA, "", SIN_DEF, "Media",
     REC_STUB + " Ágora guarda la evaluación por proveedor (informacion_proveedor.puntaje_evaluacion, clasificacion_evaluacion); CU-08 la asocia al contrato. Si se requiere por contrato, agregar el campo al modelo actual (por confirmar).",
     "CU-08", "", "Sí")
fila("Caracterizacion", "id_caracterizacion", EXT_AGORA, "", SIN_DEF, "Baja",
     REC_STUB + " En Ágora la caracterización está en informacion_persona_natural (género, grupo étnico, discapacidad, víctima del conflicto, entre otros). CU-04 indica datos sensibles: no pertenece al CRUD contractual.",
     "CU-04")
fila("Certificacion", "id_certificacion", "", "", SIN_DEF, "Baja",
     REC_STUB + " CU-09 la genera a partir de contratos existentes: puede resolverse como documento generado en un MID, sin cambios en el modelo.",
     "CU-09")

# --- Contrato --------------------------------------------------------------------------------------
H = "Contrato"
fila(H, "id_contrato", "contrato_general", "id", EQUIVALENTE, "Ninguna", "Sin cambios.", "CU-11", "contrato (numero_contrato + vigencia)")
fila(H, "numero_contrato", "contrato_general", "numero_contrato", ESTRUCTURA, "Media",
     "El LT indicó que es un identificador único por vigencia (respuesta 9). En la tabla contrato_general de ARGO v1 que aparece en los diagramas de Ágora, la PK es (numero_contrato, vigencia). Agregar UNIQUE (numero_contrato, vigencia) en contrato_general (A14), por confirmar con LT y Analista (decisión abierta D4).",
     "CU-11, CU-19", "contrato.numero_contrato", "Sí")
fila(H, "vigencia", "contrato_general", "vigencia", TIPO, "Baja",
     "vigencia es varchar(4) en contrato_general e integer en disponibilidad_presupuestal, registro_presupuestal y convenio; la BD de pruebas muestra la misma diferencia (texto frente a numérico). No se recomienda unificar el tipo por ahora: cambiaría el tipo en la API. Queda para una eventual migración (respuesta 7).",
     "CU-02", "contrato.vigencia")
fila(H, "id_proceso", "", "", FALTANTE, "Alta",
     "Stand by (pregunta 8). No se propone una entidad nueva de proceso contractual: un modelo distinto afecta las integraciones de ARGO v1, que está en producción. Si se confirma, agregar el campo al modelo actual.",
     "CU-11, CU-13", "solicitud_necesidad (otra BD)", "Sí")
fila(H, "id_proveedor", "contratista", "contrato_general_id", ESTRUCTURA, "Media",
     "Sin cambio de estructura. El proveedor vive en Ágora y contratista guarda numero_documento (respuesta 2). Cardinalidad 1:1 en stand by (pregunta 11): si se confirma, agregar UNIQUE en contratista.contrato_general_id (A12).",
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
     "Decidido en la sesión de socialización (respuesta 10, opción a): agregar la columna fecha_suscripcion en contrato_general (A6). fecha_suscripcion_estudio es la del estudio previo. El momento del registro (al firmar, una vez terminado el flujo de aprobación) es una decisión abierta (D5).",
     "CU-19", "contrato_suscrito.fecha_suscripcion", "Sí")
fila(H, "fecha_inicio", "contrato_general", "fecha_inicial", NOMBRE, "Media",
     "Nombre distinto y dato duplicado con acta_inicio.fecha_inicio. Definir cuál es la fuente de verdad.",
     "CU-02", "acta_inicio.fecha_inicio", "Sí")
fila(H, "fecha_terminacion", "contrato_general", "fecha_final", NOMBRE, "Media",
     "Nombre distinto y dato duplicado con acta_inicio.fecha_fin. Las novedades (prórroga), fuera del alcance de este análisis, pueden cambiar la fecha final.",
     "CU-02, CU-18", "acta_inicio.fecha_fin", "Sí")
fila(H, "estado_contrato", "estado_contrato", "estado_parametro_id", ESTRUCTURA, "Baja",
     "El CRUD modela el estado como historial (tabla estado_contrato con actual = true), con dos columnas de estado: estado_parametro_id y estado_interno_parametro_id. Nota de la sesión de socialización (respuesta 10): \"2 estados el que ve el usuario\"; su alcance es una decisión abierta (D6). Reflejar el historial en el diccionario.",
     "CU-19, CU-20", "contrato_estado / estado_contrato")

# --- Proyectos y dependencia ----------------------------------------------------------------------
fila("Proyectos de Extension", "id_proyecto_extension", "", "", SIN_DEF, "Media",
     REC_STUB + " CU-15 (contratación derivada IDEXUD) necesita asociar contratos a proyecto: si se confirma, agregar el campo en contrato_general (A11).",
     "CU-15", "idexud_proyecto", "Sí")
fila("Proyectos de Investigacion", "id_proyecto_investigacion", "", "", SIN_DEF, "Baja",
     REC_STUB + " No hay caso de uso asociado.", "", "")
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
    fila(hoja, pk, "documento_contrato", "id", ESTRUCTURA, "Baja",
         "Sin cambio de estructura: documento_contrato se mantiene como única tabla. La etapa (pre, contractual, pos) y el carácter (público/privado) se expresan con tipo_documento_id (parámetro), que ya existe.",
         cu, "estudio_documento_previo / documento")
    fila(hoja, "entidad_relacionada", "", "", ESTRUCTURA, "Baja",
         "Sin cambio: los documentos se asocian solo al contrato (contrato_general_id). No se propone asociación polimórfica.",
         cu)
    fila(hoja, "id_entidad_relacionada", "documento_contrato", "contrato_general_id", ESTRUCTURA, "Baja",
         "Ver entidad_relacionada.", cu)
    fila(hoja, "tipo_documento", "documento_contrato", "tipo_documento_id", EQUIVALENTE, "Ninguna",
         "Equivalente como referencia a Parámetros CRUD. También expresa etapa y carácter del documento.", cu)
    fila(hoja, "nombre_archivo", "externo:gestor documental", "", EXTERNO, "Baja",
         "El nombre del archivo lo gestiona el Gestor Documental (documento_id). No se replica salvo que se requiera para consultas.", cu)
    fila(hoja, "ruta_archivo", "documento_contrato", "documento_enlace", NOMBRE, "Baja",
         "documento_enlace varchar(50) guarda el identificador del Gestor Documental, no una ruta. Confirmar que 50 caracteres bastan.", cu)
    fila(hoja, "fecha_cargue", "documento_contrato", "fecha_creacion", NOMBRE, "Ninguna",
         "Equivalente mediante columna de auditoría.", cu)
    fila(hoja, "estado_documento", "documento_contrato", "", DESCARTADO, "Ninguna",
         "Descartado: los documentos no tienen estado (respuesta 12). Retirar del diccionario. La columna actual se comentó en la entidad durante la estabilización y no existe en la BD de pruebas.",
         cu)

# --- Necesidad, SECOP, OTH ------------------------------------------------------------------------
fila("Necesidad", "id_necesidad", "", "", SIN_DEF, "Media",
     REC_STUB + " En v1 la necesidad vivía en otra base (solicitud_necesidad). Según la respuesta 15, las entidades sin atributos se profundizan con el modelo general y se validan contra las entidades de Argo v2.",
     "CU-10", "solicitud_necesidad", "Sí")
fila("Secop", "id_secop", "", "", SIN_DEF, "Media",
     REC_STUB + " No hay en el CRUD ningún identificador de publicación en SECOP. Si se confirma, agregar el campo al modelo actual.", "", "", "Sí")
fila("OTH", "id_oth", "", "", SIN_DEF, "Baja",
     REC_STUB + " No se sabe qué significa la sigla (respuesta 15, sesión de socialización); decisión abierta D13. Sin atributos para comparar.", "", "")

# --- Estudio previo -------------------------------------------------------------------------------
H = "EstudioPrevio"
REC_EP = ("Stand by (pregunta 8). No se propone separar el estudio previo en una entidad nueva: sus datos siguen en "
          "contrato_general. Si se confirma, los campos faltantes se agregan al modelo actual.")
fila(H, "id_estudio_previo", "", "", FALTANTE, "Alta", REC_EP, "CU-10, CU-11", "estudio_documento_previo", "Sí")
fila(H, "numero_estudio", "", "", FALTANTE, "Media",
     "Stand by (pregunta 8). Si se confirma, agregar el campo al modelo actual. consecutivo_elaboracion está documentado como campo legado: confirmar si cumple este rol.",
     "CU-10", "", "Sí")
fila(H, "fecha_estudio", "contrato_general", "fecha_suscripcion_estudio", NOMBRE, "Baja",
     "Equivalente, ubicado en contrato_general.", "CU-10", "estudio_documento_previo.fecha_suscripcion")
fila(H, "dependencia_solicitante", "solicitante", "dependencia_solicitante_id", NOMBRE, "Baja",
     "Equivalente en tabla solicitante (referencia OIKOS). Cardinalidad 1:1 en stand by (pregunta 11).",
     "CU-10", "contrato.dependencia_solicitante")
fila(H, "necesidad", "", "", FALTANTE, "Media",
     "Stand by (pregunta 8). justificacion es cercano pero no equivalente. Si se confirma, agregar el campo al modelo actual.",
     "CU-10", "", "Sí")
fila(H, "objeto_contrato", "contrato_general", "objeto", NOMBRE, "Baja", "Equivalente en contrato_general.",
     "CU-10", "contrato.objeto_contrato")
fila(H, "justificacion", "contrato_general", "justificacion", EQUIVALENTE, "Baja",
     "Equivalente en contrato_general. Definir longitud del varchar.", "CU-10", "contrato.justificacion")
fila(H, "actividades", "contrato_general", "actividades", EQUIVALENTE, "Baja",
     "Equivalente en contrato_general. Definir longitud del varchar.", "CU-10", "contrato.actividades")
fila(H, "obligaciones", "", "", FALTANTE, "Media",
     "Stand by (pregunta 8). Confirmar si contrato_general.condiciones lo cubre; si no, agregar el campo al modelo actual.",
     "CU-10", "", "Sí")
fila(H, "valor_estimado", "", "", FALTANTE, "Media",
     "Stand by (pregunta 14). El LT indicó que es un valor separado del contratado: si se confirma, agregar el campo al modelo actual (numeric(20,7)), sin reemplazar valor_pesos.",
     "CU-10", "", "Sí")
fila(H, "plazo_estimado", "", "", FALTANTE, "Baja",
     "Stand by (pregunta 14). Valor separado del plazo contratado: si se confirma, agregar el campo al modelo actual, sin reemplazar plazo_ejecucion.",
     "CU-10", "", "Sí")

# --- CDP y RP -------------------------------------------------------------------------------------
H = "CDP"
REC_FIN = ("Dato del CDP en SICAPITAL: se consulta directamente por numero_cdp_id (respuesta 4). No se replica en el CRUD.")
fila(H, "id_cdp", "disponibilidad_presupuestal", "id", EQUIVALENTE, "Ninguna", "Sin cambios.", "CU-16", "contrato_disponibilidad")
fila(H, "numero_cdp", "disponibilidad_presupuestal", "numero_cdp_id", NOMBRE, "Baja",
     "Resuelto (respuesta 4): numero_cdp_id guarda la referencia para la consulta directa a SICAPITAL.",
     "CU-16", "contrato_disponibilidad.numero_cdp")
fila(H, "vigencia", "disponibilidad_presupuestal", "vigencia_cdp", NOMBRE, "Baja", "Equivalente.", "CU-16",
     "contrato_disponibilidad.vigencia_cdp")
fila(H, "fecha_cdp", "disponibilidad_presupuestal", "fecha_registro", NOMBRE, "Baja",
     "Confirmar si fecha_registro es la fecha del CDP o la fecha en que se asoció al contrato. La fecha del CDP puede consultarse en SICAPITAL por numero_cdp_id.",
     "CU-16", "contrato_disponibilidad.fecha_registro")
for campo in ["valor_cdp", "saldo_disponible", "tipo_recurso", "rubro", "proyecto_inversion"]:
    fila(H, campo, EXT_SICAPITAL, "", EXTERNO, "Baja", REC_FIN, "CU-16")
actualizar(H, "rubro", recomendacion=REC_FIN + " A nivel de contrato existen tipo_gasto_id y tema_gasto_inversion_id.")

fila("RP", "id_rp", "registro_presupuestal", "id", PARCIAL, "Alta",
     "La tabla registro_presupuestal existe en el DDL y en la BD de pruebas (ligada al CDP por cdp_id), pero no tiene entidad, módulo ni endpoints. CU-16 exige registrar el RP: exponerla (A5). El nombre cdp_id no sigue el lineamiento (disponibilidad_presupuestal_id), pero no se recomienda renombrarlo por ahora.",
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
     "Stand by (pregunta 13). Si se confirma, agregar un campo de estado en poliza (referencia a Parámetros CRUD) (A7). Sin tabla de historial.",
     "CU-14", "poliza.estado", "Sí")
fila("Aprobacion Poliza", "id_aprobacion_poliza", "poliza", "fecha_aprobacion", PARCIAL, "Media",
     "Stand by (pregunta 13). El CRUD guarda la última aprobación (fecha_aprobacion, usuario_id). No se propone tabla de historial; el estado se cubre con el campo de A7 si se confirma.",
     "CU-14", "", "Sí")

# --- Acta de inicio, liquidación, novedades, terminación -----------------------------------------
fila("Acta de inicio", "id_acta_inicio", "acta_inicio", "id", EQUIVALENTE, "Ninguna",
     "El CRUD ya modela el acta (fechas, descripción, usuario). Completar el diccionario con esos atributos.",
     "", "acta_inicio")
fila("Liquidacion", "id_liquidacion", "", "", SIN_DEF, "Media",
     REC_STUB + " El LT no indicó si la liquidación es una novedad y no se trató en la sesión de socialización (decisión abierta D11). En v1 existía contrato_liquidado (fecha, número de acta, observaciones, documento).",
     "", "contrato_liquidado", "Sí")

H = "Novedad"
REC_NOV = ("Fuera de alcance (respuesta 3): hoy el sistema de novedades gestiona las de CPS; las novedades del nuevo Argo, "
           "para cualquier tipo de contrato, se analizan desde requerimientos y no afectan el módulo contractual.")
for campo in ["id_novedad", "id_contrato", "tipo_novedad", "numero_novedad", "fecha_solicitud", "fecha_aprobacion",
              "descripcion", "nuevo_valor_contrato", "nueva_fecha_terminacion", "estado_novedad"]:
    fila(H, campo, "", "", FUERA, "Ninguna", REC_NOV if campo == "id_novedad" else "Ver id_novedad.",
         "CU-18", "novedad_contractual")
fila("Terminacion", "id_terminacion", "", "", FUERA, "Ninguna",
     "Fuera de alcance junto con las novedades: en ARGO v1 era una novedad (terminacion_anticipada). Supuesto no tratado en la sesión de socialización (decisión abierta D12).",
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
    "contrato_arrendamiento": ("Sin equivalente en el diccionario. Existe en el DDL y en la BD de pruebas, sin entidad ni endpoints.", "Baja"),
    "convenio": ("Sin equivalente en el diccionario. Existe en el DDL y en la BD de pruebas, sin entidad ni endpoints.", "Baja"),
}
