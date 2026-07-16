_ABBREVIATIONS = {
    "Archivo Histórico de la Provincia del Santo Evangelio de México": "AHPSEM",
    "Archivo Miguel Covarrubias": "AMC",
    "Biblioteca Franciscana": "BF",
    "Colección Juan de Palafox y Mendoza": "CJPM",
    "Sala de Archivo y Colecciones Especiales": "SACE",
    "Archivo Porfirio Díaz Telegramas 1910": "Telegramas",
    "Periódicos Universitarios": "PU",
}

# Prefijo legible para el LABEL de colecciones de tesis
_TESIS_LABELS = {
    "Tesis Licenciatura": "Licenciatura en",
    "Tesis Maestría": "Maestría en",
    "Tesis Doctorado": "Doctorado en",
}


def make_collection_label(collection: str, subcollection_name: str) -> str:
    """Label legible para el COLLECTION AIP en METS.

    Ejemplo: ("Archivo Miguel Covarrubias", "Abstracto Decorativo Recortes")
             → "AMC - Abstracto Decorativo Recortes"
    """
    abbrev = _ABBREVIATIONS.get(collection)
    if abbrev:
        return f"{abbrev} - {subcollection_name}"
    tesis_prefix = _TESIS_LABELS.get(collection)
    if tesis_prefix:
        return f"{tesis_prefix} {subcollection_name}"
    return subcollection_name
