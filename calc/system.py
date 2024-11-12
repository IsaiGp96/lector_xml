import os
import xml.etree.ElementTree as ET

ARCHIVE_FOLDER = r"temp\files_xml"

class Archivo:
    def analizar(ruta_xml):
        """Extrae y devuelve los datos relevantes del archivo XML."""
        ns = {
            'cfdi': 'http://www.sat.gob.mx/cfd/4'
        }
        
        arbol = ET.parse(ruta_xml)
        raiz = arbol.getroot()

        comprobante = raiz.find('cfdi:Comprobante', ns)
        receptor = raiz.find('cfdi:Receptor', ns)

        # El nodo 'Concepto' está anidado bajo 'Comprobante' > 'Conceptos' > 'Concepto'
        conceptos = raiz.findall('.//cfdi:Concepto', ns)

        return {
            'metodo_pago': comprobante.attrib.get('MetodoPago', '') if comprobante is not None else '',
            'forma_pago': comprobante.attrib.get('FormaPago', '') if comprobante is not None else '',
            'rfc_receptor': receptor.attrib.get('Rfc', '') if receptor is not None else '',
            'conceptos': Archivo.extraer_conceptos(conceptos, ns)
        }

    def extraer_conceptos(conceptos, ns):
        """Procesa y devuelve la lista de conceptos del XML."""
        return [Archivo.procesar_concepto(concepto, ns) for concepto in conceptos]

    def procesar_concepto(concepto, ns):
        """Extrae y devuelve los datos de un concepto específico."""
        concepto_data = {
            'descripcion': concepto.attrib.get('Descripcion', ''),
            'clave_prod_serv': concepto.attrib.get('ClaveProdServ', ''),
            'cantidad': float(concepto.attrib.get('Cantidad', '0.0')),
            'valor_unitario': float(concepto.attrib.get('ValorUnitario', '0.0')),
            'importe': float(concepto.attrib.get('Importe', '0.0')),
            'descuento': float(concepto.attrib.get('Descuento', '0.0')),
            'impuestos': Archivo.extraer_impuestos_concepto(concepto, ns)
        }
        return concepto_data

    def extraer_impuestos_concepto(concepto, ns):
        """Extrae y devuelve la lista de impuestos asociados a un concepto."""
        impuestos_elemento = concepto.find('cfdi:Impuestos', ns)
        if impuestos_elemento is not None:
            traslados_elemento = impuestos_elemento.find('cfdi:Traslados', ns)
            if traslados_elemento is not None:
                return [Archivo.procesar_traslado(traslado) for traslado in traslados_elemento.findall('cfdi:Traslado', ns)]
        return []

    def procesar_traslado(traslado):
        """Procesa y devuelve los datos de un traslado específico."""
        return {
            'base': float(traslado.attrib.get('Base', '0.0')),
            'impuesto': traslado.attrib.get('Impuesto', ''),
            'tipo_factor': traslado.attrib.get('TipoFactor', ''),
            'tasa_o_cuota': float(traslado.attrib.get('TasaOCuota', '0.0')),
            'importe': float(traslado.attrib.get('Importe', '0.0'))
        }

    def analizar_cfdi(datos):
        """Procesa los datos del CFDI y los devuelve en el formato requerido."""
        subtotal_sin_iva = sum(c['importe'] - sum(i['importe'] for i in c['impuestos'] if i['impuesto'] == '002') for c in datos['conceptos'])
        iva_16 = sum(i['importe'] for c in datos['conceptos'] for i in c['impuestos'] if i['impuesto'] == '002' and i['tasa_o_cuota'] == 0.160000)
        iva_8 = sum(i['importe'] for c in datos['conceptos'] for i in c['impuestos'] if i['impuesto'] == '002' and i['tasa_o_cuota'] == 0.080000)
        ieps = sum(i['importe'] for c in datos['conceptos'] for i in c['impuestos'] if i['impuesto'] == '003')
        resico = datos['resico']
        exentos = sum(c['importe'] for c in datos['conceptos'] if not any(i['importe'] > 0 for i in c['impuestos']))
        ish = datos['ish']
        total = datos['total']
        uuid = datos['uuid']

        # Retorna los resultados en el formato requerido
        return {
            "Subtotal_S_IVA_18": subtotal_sin_iva,
            "IVA_16_107_8": iva_16,
            "IVA_8_107_3": iva_8,
            "IEPS_43": ieps,
            "Resico_203_000026": resico,
            "Exentos_99": exentos,
            "ISH": ish,
            "Total": total,
            "UUID": uuid
        }

class Carpeta:
    def carpeta_temp(self):
        archivos = ""
        if os.path.exists(ARCHIVE_FOLDER) and os.listdir(ARCHIVE_FOLDER):
            for file in os.listdir(ARCHIVE_FOLDER):
                archivos = f"{ARCHIVE_FOLDER}\{file}"
                print(f"Archivo: {archivos}")
                return(archivos)

class Main:
    carpeta = Carpeta()
    arhivo_xml = carpeta.carpeta_temp()
    
    analizar_xml = Archivo()
    input(str(arhivo_xml))
    datos = Archivo.analizar(arhivo_xml)
    print(datos)
if __name__ == "__main__":
    Main()
