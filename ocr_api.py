from fastapi import APIRouter, File, UploadFile
import pytesseract
import cv2
import re
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import numpy as np

ocr_api_router = APIRouter()

# Configurar la ruta de Tesseract (ajústala según tu sistema)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

def procesar_ticket(image: BytesIO):
    # Leer la imagen
    image_np = np.array(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "No se pudo cargar la imagen"}

    # Convertir a escala de grises y aplicar preprocesamiento
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)  # Mejor filtro para OCR
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 3)

    try:
        texto = pytesseract.image_to_string(thresh, lang='spa', config='--psm 3')
    except Exception as e:
        return {"error": f"Error al aplicar OCR: {str(e)}"}

    datos = extraer_datos(texto)
    return datos

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
        if datos["fecha"] is None:
            coincidencia_fecha = patron_fecha.search(linea)
            if coincidencia_fecha:
                datos["fecha"] = coincidencia_fecha.group(0)

        if datos["cif"] is None:
            coincidencia_cif = patron_cif_nif.search(linea)
            if coincidencia_cif:
                datos["cif"] = re.sub(r'[^A-Z0-9]', '', coincidencia_cif.group(1))

        coincidencia_total = patron_total.search(linea)
        if coincidencia_total:
            total_texto = coincidencia_total.group(1)
            total_texto = total_texto.replace(' ', '').replace(',', '.')
            try:
                total_float = float(total_texto)
                if datos["total"] is None or total_float > datos["total"]:
                    datos["total"] = total_float
            except ValueError:
                pass

    return datos

@ocr_api_router.post("/procesar_ticket/")
async def procesar_ticket_endpoint(file: UploadFile = File(...)):
    image = await file.read()
    datos = procesar_ticket(BytesIO(image))
    return datos