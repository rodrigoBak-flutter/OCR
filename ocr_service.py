import pytesseract
import cv2
import numpy as np
from io import BytesIO

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def procesar_ticket(image: BytesIO):
    image_np = np.array(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "No se pudo cargar la imagen"}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 3)

    try:
        texto = pytesseract.image_to_string(thresh, lang='spa', config='--psm 3')
    except Exception as e:
        return {"error": f"Error al aplicar OCR: {str(e)}"}

    from utils import extraer_datos
    datos = extraer_datos(texto)
    return datos
