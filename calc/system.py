import os
import xml.etree.ElementTree as ET

ARCHIVE_FOLDER = r"temp\files_xml"

class Archivo:
    def analizar(self):
        pass

class Carpeta:
    def carpeta_temp(self):
        if os.path.exists(ARCHIVE_FOLDER) and os.listdir(ARCHIVE_FOLDER):
            for file in os.listdir(ARCHIVE_FOLDER):
                print(file)

## Pruebas pruebas
carpeta = Carpeta()
carpeta.carpeta_temp()
