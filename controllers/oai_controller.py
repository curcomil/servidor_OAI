from flask import Response
from datetime import datetime
import os

def identify():
    """Responde al verbo Identify del protocolo OAI-PMH."""
    url = os.getenv("URL")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/
                             http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
  <responseDate>{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}</responseDate>
  <request verb="Identify">{url}/oai</request>
  <Identify>
    <repositoryName>Colecciones Especiales - UDLAP</repositoryName>
    <baseURL>{url}/oai</baseURL>
    <protocolVersion>2.0</protocolVersion>
    <adminEmail>tesis.digitales@udlap.mx</adminEmail>
    <earliestDatestamp>2000-01-01T00:00:00Z</earliestDatestamp>
    <deletedRecord>no</deletedRecord>
    <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
    <description>
      <oai-identifier xmlns="http://www.openarchives.org/OAI/2.0/oai-identifier"
                      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                      xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai-identifier
                                          http://www.openarchives.org/OAI/2.0/oai-identifier.xsd">
        <scheme>oai</scheme>
        <repositoryIdentifier>udlap.mx</repositoryIdentifier>
        <delimiter>:</delimiter>
        <sampleIdentifier>oai:udlap.mx:covarrubias/africa-001</sampleIdentifier>
      </oai-identifier>
    </description>
  </Identify>
</OAI-PMH>"""

    return Response(xml, content_type="text/xml; charset=utf-8")


