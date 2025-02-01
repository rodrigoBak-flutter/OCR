import re

def extraer_datos(texto: str):
    datos = {
        "fecha": None,
        "cif": None,
        "total": None,
    }

    texto = re.sub(r'[^\x20-\x7EñÑáéíóúÁÉÍÓÚ€]', ' ', texto)
    lineas = texto.split('\n')

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
            total_texto = coincidencia_total.group(1).replace(' ', '').replace(',', '.')
            try:
                total_float = float(total_texto)
                if datos["total"] is None or total_float > datos["total"]:
                    datos["total"] = total_float
            except ValueError:
                pass
    
    return datos