import json
from datetime import datetime

def jsonToOAI(json_data, base_url):
    xml_sets = []
    def recorrer(coleccion, prefix=""):
       
        set_spec = f"{prefix}:{coleccion['filename'].replace(' ', '_')}" if prefix else coleccion["filename"].replace(' ', '_')

        xml_sets.append(
            f"<set><setSpec>{set_spec}</setSpec><setName>{coleccion['filename']}</setName></set>"
        )

        for sub in coleccion.get("subcolecciones", []):
            recorrer(sub, set_spec)

    recorrer(json_data)

    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
  <responseDate>{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}</responseDate>
  <request verb="ListSets">{base_url}/oai</request>
  <ListSets>
    {"".join(xml_sets)}
  </ListSets>
</OAI-PMH>"""

    return xml_response
