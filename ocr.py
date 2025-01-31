import pytesseract
import cv2
import re

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

    # Aplicar umbralización simple
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

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

    # Guardar el texto en un archivo
    with open('texto_extraido.txt', 'w', encoding='utf-8') as f:
        f.write(texto)

    # Buscar el total del ticket usando expresiones regulares
    patron_total = re.compile(r'total.*?(\d+[.,]\d+)', re.IGNORECASE)
    coincidencias = patron_total.search(texto)

    if coincidencias:
        total = coincidencias.group(1).replace(',', '.')  # Convertir coma a punto para manejar decimales
        try:
            total = float(total)  # Validar que el total sea un número válido
            print(f"Total del ticket: {total:.2f} €")
        except ValueError:
            print("El total encontrado no es un número válido.")
    else:
        print("No se encontró el total del ticket.")

    # Extraer otros datos (opcional)
    extraer_datos_adicionales(texto)

def extraer_datos_adicionales(texto):
    # Buscar la fecha
    patron_fecha = re.compile(r'fecha:\s*(\d{2}/\d{2}/\d{4})', re.IGNORECASE)
    coincidencias_fecha = patron_fecha.search(texto)
    if coincidencias_fecha:
        fecha = coincidencias_fecha.group(1)
        print(f"Fecha: {fecha}")

    # Buscar la hora
    patron_hora = re.compile(r'hora:\s*(\d{2}:\d{2})', re.IGNORECASE)
    coincidencias_hora = patron_hora.search(texto)
    if coincidencias_hora:
        hora = coincidencias_hora.group(1)
        print(f"Hora: {hora}")

    # Buscar los ítems comprados
    patron_items = re.compile(r'(\d+,\d{3})\s+([A-Z\s]+)\s+(\d+,\d{2})\s+(\d+,\d{2})')
    items = patron_items.findall(texto)
    if items:
        print("\nÍtems comprados:")
        for item in items:
            print(f"{item[1].strip()} - Cantidad: {item[0]} - Precio: {item[2]} € - Total: {item[3]} €")

# Llamar a la función con la ruta de la imagen
procesar_ticket('C:\\Users\\rodri\\Desktop\\ticket.jpg')