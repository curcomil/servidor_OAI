import xml.etree.ElementTree as ET
import unicodedata
from pathlib import Path
import re
import json
import time, random
import requests
import urllib3
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Estructura principal
colecciones = []
indice_colecciones = {}  # 🔍 índice para acceso rápido por expediente

def url_funcionando(url: str, path_name) -> bool:
    """Verifica si un URL funciona, ignorando errores de certificado SSL."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        respuesta = requests.get(url, headers=headers, timeout=5, verify=False)
        return respuesta.status_code == 200
    except requests.RequestException as e:
        tqdm.write(f"❌ Error al acceder a la URL: {e} {path_name}")
        return False

def normalize_path(texto: str) -> str:
    if not texto:
        return ""
    texto = texto.strip().strip("/").lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.replace(" ", "_")
    texto = re.sub(r"[^a-z0-9/_\.]", "", texto)
    texto = re.sub(r"_{2,}", "_", texto)
    texto = re.sub(r"/{2,}", "/", texto)
    return texto

def crear_coleccion_si_no_existe(nombre_expediente: str):
    """Crea una colección si no existe ya en el índice."""
    if nombre_expediente not in indice_colecciones:
        nueva = {
            "coleccion": "Archivo Miguel Covarrubias",
            "expediente": nombre_expediente,
            "items": []
        }
        colecciones.append(nueva)
        indice_colecciones[nombre_expediente] = nueva

def procesar_xml(path: Path):
    """Procesa un XML, crea expediente y prepara datos del item."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        metadata = root.find("metadata")
        history = root.find("history")

        if metadata is None or history is None:
            tqdm.write(f"Sin metadata o historial en {path.name}")
            return

        expediente_elem = metadata.find("expediente")
        if expediente_elem is None or expediente_elem.text is None:
            tqdm.write(f"Sin expediente en {path.name}")
            return

        expediente = expediente_elem.text.strip()
        crear_coleccion_si_no_existe(expediente)

        # Crear item
        item = {}
        item["nombre_archivo"] = path.name
        item["internal_id"] = f"{int(time.time()*1000)}{random.randint(1000,9999)}"
        item["metadata"] = {elem.tag: (elem.text.strip() if elem.text else "") for elem in metadata}
        item["history"] = []

        for action in history.findall("action"):
            accion_dict = {
                "name": action.attrib.get("name", ""),
                "user": action.find("user").text.strip() if action.find("user") is not None else "",
                "date": action.find("date").text.strip() if action.find("date") is not None else "",
                "from": action.find("from").text.strip() if action.find("from") is not None else ""
            }
            item["history"].append(accion_dict)

        imagen = item["metadata"].get("imagen", "")
        collection = item["metadata"].get("collection", "")
        base_url = "https://catarina.udlap.mx/ximg"

        if imagen and collection:
            url = f"{base_url}/{normalize_path(collection)}/{normalize_path(imagen)}"
            if url_funcionando(url, path.name):
                item["url"] = url
            else:
                item["url"] = ""
        else:
            item["url"] = ""

        # Evitar duplicados
        existente = indice_colecciones[expediente]
        if not any(i["nombre_archivo"] == path.name for i in existente["items"]):
            existente["items"].append(item)

    except Exception as e:
        tqdm.write(f"[ERROR] Fallo procesando {path.name}: {e}")

def procesar_directorio(ruta: Path):
    archivos = list(ruta.glob("*.xml"))
    for archivo in tqdm(archivos, desc="Procesando XMLs", unit="archivo"):
        procesar_xml(archivo)
        time.sleep(0.05)

if __name__ == "__main__":
    ruta = Path(r"C:\Users\26193\Desktop\Work\Proyectos\servidor_OAI\db\xmlibris\system\metadata\amc")
    procesar_directorio(ruta)

    with open("amc_items.json", "w", encoding="utf-8") as x:
        json.dump(colecciones, x, indent=4, ensure_ascii=False)

    tqdm.write(f"✅ Procesados {len(colecciones)} expedientes.")
