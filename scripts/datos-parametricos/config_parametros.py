"""Constantes paramétricas de gestion_contractual_mf que consulta el extractor.

Fuente: udistrital/gestion_contractual_mf, rama develop,
src/environments/environment.development.ts (último cambio del archivo: commit 17e8e53).
Si el entorno del MF cambia, actualizar estos diccionarios y FUENTE_ENTORNO.
"""

URL_POR_DEFECTO = "http://pruebasapi.intranetoas.udistrital.edu.co:8510/v1/"
AMBIENTE = "Pruebas (intranet OAS, requiere VPN)"

FUENTE_ENTORNO = {
    "repositorio": "udistrital/gestion_contractual_mf",
    "rama": "develop",
    "archivo": "src/environments/environment.development.ts",
    "commit": "17e8e53",
}

# Tipos de parámetro: cada uno genera una hoja del Excel.
TIPOS_PARAMETRO = {
    "TIPO_COMPROMISO_ID": 111,
    "TIPO_CONTRATO_ID": 112,
    "PERFIL_CONTRATISTA_ID": 113,
    "TIPOLOGIA_ESPECIFICA_ID": 114,
    "MODALIDAD_SELECCION_ID": 115,
    "REGIMEN_CONTRATACION_ID": 116,
    "PROCEDIMIENTO_ID": 117,
    "AMPARO_ID": 118,
    "TIPO_CONTROL_ID": 119,
    "CLASE_CONTRATISTA_ID": 120,
    "VIGENCIA_ID": 121,
    "TIPO_MONEDA": 122,
    "TIPO_GASTO_ID": 123,
    "ORIGEN_RECURSOS_ID": 124,
    "ORIGEN_PRESUPUESTO_ID": 125,
    "TEMA_GASTO_ID": 126,
    "MEDIO_PAGO_ID": 127,
    "TIPO_PERSONA_ID": 132,
    "ENUMERACION_CLAUSULAS_ID": 135,
    "TIPO_ESTADO_ID": 137,
    "UNIDAD_EJECUCION_ID": 7,
    "UNIDAD_EJECUTORA_ID": 146,
}

# Parámetros específicos: (id, tipo esperado). El tipo esperado sale del uso en el MF
# (con qué lista se compara el id); None cuando el MF no permite inferirlo.
# Si el tipo real no está en TIPOS_PARAMETRO, se agrega como hoja adicional.
PARAMETROS_ESPECIFICOS = {
    "ORDEN_ID": (6534, 111),
    "CONTRATO_ID": (6535, 111),
    "CONVENIO_ID": (6536, 111),
    "CONTRATO_PSPAG_ID": (6546, 112),
    "PESO_COLOMBIANO_ID": (6634, 122),
    "AMPARO_CREC_ID": (6609, 118),
    "SUFICIENCIA_SMLV_ID": (6708, None),
    "SUFICIENCIA_PORCENTAJE_ID": (6709, None),
    "UNIDADES_EJECUTORAS.RECTORIA": (6818, 146),
    "UNIDADES_EJECUTORAS.IDEXUD": (6819, 146),
    "ESTADOS_GENERALES.POR_SUSCRIBIR": (6773, None),
    "ESTADOS_GENERALES.SUSCRITO": (6774, None),
    "ESTADOS_GENERALES.EN_EJECUCION": (6777, None),
    "ESTADOS_GENERALES.LEGALIZADO": (6776, None),
    "ESTADOS_GENERALES.DECLINADO": (6775, None),
    "ESTADOS_INTERNOS.BORRADOR": (6799, None),
    "ESTADOS_INTERNOS.EN_REVISION_JEFE": (6800, None),
    "ESTADOS_INTERNOS.APROBADO_JEFE": (6809, None),
    "ESTADOS_INTERNOS.EN_REVISION_ORDENADOR": (6821, None),
    "ESTADOS_INTERNOS.REVISADO_ORDENADOR": (6822, None),
    "ESTADOS_INTERNOS.EN_FIRMA_ORDENADOR": (6801, None),
    "ESTADOS_INTERNOS.FIRMADO_ORDENADOR": (6808, None),
    "ESTADOS_INTERNOS.EN_FIRMA_CONTRATISTA": (6802, None),
    "ESTADOS_INTERNOS.FIRMADO_CONTRATISTA": (6804, None),
    "ESTADOS_INTERNOS.FIRMAS_COMPLETAS": (6817, None),
    "ESTADOS_INTERNOS.RECHAZADO": (6803, None),
    "ESTADOS_INTERNOS.DECLINADO": (6807, None),
    "TIPO_DOCUMENTO_ID_PARAMETROS.MINUTA": (6805, None),
    "TIPO_DOCUMENTO_ID_PARAMETROS.DOCUMENTOS_PRECONTRACTUALES": (6716, None),
}

# Constantes del entorno que no se consultan porque no pertenecen a parametros_crud.
EXCLUIDAS = {
    "TIPO_DOCUMENTO_ID_GESTOR_DOCUMENTAL.*": "Ids de tipo documental de gestor_documental (183, 174, 175, 176, 177)",
    "ESPECIFICACIONES_ENLACE_XLSX": "UUID de un documento en gestor_documental",
    "ESTADO_CONTRATO_*": "Estados en texto ('EN EJECUCION', 'SUSCRITO', 'POR SUSCRIBIR', 'LEGALIZADO')",
}
