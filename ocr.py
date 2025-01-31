import pytesseract
import cv2
import re
import json

# Configurar la ruta de Tesseract (ajústala según tu sistema)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def procesar_ticket(ruta_imagen):
    # Cargar la imagen
    image = cv2.imread(ruta_imagen)

    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return

    print("Imagen cargada correctamente.")

    # Convertir a escala de grises y aplicar preprocesamiento
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)  # Mejor filtro para OCR
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 3)

    # Aplicar OCR con mejor configuración
    try:
        texto = pytesseract.image_to_string(thresh, lang='spa', config='--psm 3')
    except Exception as e:
        print(f"Error al aplicar OCR: {e}")
        return

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

    # Limpiar texto (eliminar caracteres raros y convertir a ASCII básico)
    texto = re.sub(r'[^\x20-\x7EñÑáéíóúÁÉÍÓÚ€]', ' ', texto)  # Mantener caracteres relevantes
    lineas = texto.split('\n')

    # Expresiones regulares mejoradas
    patron_fecha = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    patron_cif_nif = re.compile(r'(?:N[.\s]*I[.\s]*F|CIF)[.: ]*([A-HJNP-SUVWXYZ0-9.-]{8,})')
    patron_total = re.compile(r'(?:TOTAL|Tota1|Pendiente de Cobro|Base Imp)[^\d]*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)')

    for linea in lineas:
        # Buscar fecha
        if datos["fecha"] is None:
            coincidencia_fecha = patron_fecha.search(linea)
            if coincidencia_fecha:
                datos["fecha"] = coincidencia_fecha.group(0)

        # Buscar CIF/NIF
        if datos["cif"] is None:
            coincidencia_cif = patron_cif_nif.search(linea)
            if coincidencia_cif:
                datos["cif"] = re.sub(r'[^A-Z0-9]', '', coincidencia_cif.group(1))  # Limpiar caracteres extraños

        # Buscar total
        coincidencia_total = patron_total.search(linea)
        if coincidencia_total:
            total_texto = coincidencia_total.group(1)

            # Reemplazar comas por puntos y eliminar espacios
            total_texto = total_texto.replace(' ', '').replace(',', '.')

            try:
                total_float = float(total_texto)
                # Tomar el mayor total encontrado
                if datos["total"] is None or total_float > datos["total"]:
                    datos["total"] = total_float
            except ValueError:
                pass

    return datos

# Llamar a la función con la ruta de la imagen
procesar_ticket('C:\\Users\\rodri\\Desktop\\ticket-1.jpg')
