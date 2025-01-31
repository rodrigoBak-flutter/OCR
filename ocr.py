import pytesseract
import cv2
import re
import json
import numpy as np

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def procesar_ticket(ruta_imagen):
    # Cargar la imagen
    image = cv2.imread(ruta_imagen)

    # Verificar si la imagen se cargó correctamente
    if image is None:
        print("Error: No se pudo cargar la imagen. Verifica la ruta del archivo.")
        return

    print("Imagen cargada correctamente.")

    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar un suavizado para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    # Aplicar umbralización adaptativa
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 3
    )

    # Guardar la imagen preprocesada (opcional, para verificar)
    cv2.imwrite('preprocessed_image.jpg', thresh)

    # Aplicar OCR con configuración mejorada
    try:
        texto = pytesseract.image_to_string(thresh, lang='spa', config='--psm 6 --oem 1')
    except Exception as e:
        print(f"Error al aplicar OCR: {e}")
        return

    # Imprimir el texto extraído
    print('ACA ESTA EL TEXTO DEL TICKET:\n', texto)

  
    # Extraer datos relevantes
    datos = extraer_datos(texto)

    # Guardar los datos en un archivo JSON
    with open('datos_ticket.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print("Datos guardados en 'datos_ticket.json'.")

def extraer_datos(texto):
    datos = {
        "fecha": None,
        "cif": None,
        "total": None,
    }

    # Convertir el texto en líneas
    lineas = texto.split('\n')

    # Buscar palabras clave en cada línea
    for linea in lineas:
        # Extraer la fecha
        if "FECHA" in linea.upper():
            fecha = linea.split("FECHA")[-1].strip()
            datos["fecha"] = re.sub(r'[^0-9/]', '', fecha)  # Limpiar la fecha

        # Extraer el CIF
        if "CIF" in linea.upper():
            cif = linea.split("CIF")[-1].strip()
            datos["cif"] = re.sub(r'[^A-Z0-9-]', '', cif)  # Limpiar el CIF

        # Extraer el total
        if "TOTAL" in linea.upper():
            total = linea.split("TOTAL")[-1].strip()
            total = re.sub(r'[^0-9,]', '', total)  # Limpiar el total
            try:
                datos["total"] = float(total.replace(',', '.'))
            except ValueError:
                pass

    return datos

# Llamar a la función con la ruta de la imagen
procesar_ticket('C:\\Users\\rodri\\Desktop\\ticket-1.jpg')