import xml.etree.ElementTree as ET
import os
import json
from dotenv import load_dotenv

load_dotenv()

exist_path = os.getenv("exist_database_path")
if not exist_path:
    raise ValueError("No se encontró la variable 'exist_database_path' en .env")

base = os.path.join(exist_path, "Sala de Archivos y Colecciones Especiales")

def leer_contenido(path):
    
    subcolecciones = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        for sub in root.iter():
            if sub.tag.endswith("subcollection"):
                name = sub.get("name")
                filename = sub.get("filename")
                subcolecciones.append({
                    "filename": filename,
                    "name": name
                })
    except ET.ParseError as e:
        print(f"⚠️ Error al leer {path}: {e}")
    return subcolecciones


def recorrer_carpeta(ruta):
    
    coleccion = {
        "filename": os.path.basename(ruta),
        "name": ruta,
        "subcolecciones": []
    }

    contents_path = os.path.join(ruta, "__contents__.xml")
    if os.path.exists(contents_path):
        subcolecciones = leer_contenido(contents_path)

        for sub in subcolecciones:
            sub_path = os.path.join(ruta, sub["filename"])
            if os.path.exists(sub_path):  
                sub["subcolecciones"] = recorrer_carpeta(sub_path)["subcolecciones"]
            else:
                sub["subcolecciones"] = []

            coleccion["subcolecciones"].append(sub)

    return coleccion


def list_sets():
    return recorrer_carpeta(base)


if __name__ == "__main__":
    resultado = list_sets()
    salida = os.path.join(exist_path, "estructura_exist.json")
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"Archivo generado en: {salida}")

def generate_json () :
    resultado = list_sets()
    salida = os.path.join(exist_path, "estructura_exist.json")
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
    return resultado
