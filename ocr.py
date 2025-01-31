import pytesseract
import cv2
import re

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cargar la imagen
image = cv2.imread('C:\\Users\\rodri\\Desktop\\ticket.jpg')

# Verificar si la imagen se cargó correctamente
if image is None:
    print("Error: No se pudo cargar la imagen. Verifica la ruta del archivo.")
else:
    print("Imagen cargada correctamente.")

    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización simple
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Guardar la imagen preprocesada (opcional, para verificar)
    cv2.imwrite('preprocessed_image.jpg', thresh)

    # Aplicar OCR con configuración mejorada
    texto = pytesseract.image_to_string(thresh, lang='spa', config='--psm 6 --oem 1')

    # Imprimir el texto extraído
    print('ACA ESTA EL TEXTO DEL TICKET:\n', texto)

    # Guardar el texto en un archivo
    with open('texto_extraido.txt', 'w', encoding='utf-8') as f:
        f.write(texto)

    # Buscar el total del ticket usando expresiones regulares
    patron_total = re.compile(r'total.*?(\d+,\d+)', re.IGNORECASE)
    coincidencias = patron_total.search(texto)

    if coincidencias:
        total = coincidencias.group(1)
        print(f"Total del ticket: {total}")
    else:
        print("No se encontró el total del ticket.")