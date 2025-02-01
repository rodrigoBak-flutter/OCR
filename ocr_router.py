from fastapi import APIRouter, File, UploadFile, HTTPException
from ocr_service import procesar_ticket
from io import BytesIO

ocr_api_router = APIRouter()

@ocr_api_router.post("/procesar-ticket/")
async def procesar_ticket_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    try:
        imagen_bytes = BytesIO(await file.read())
        datos_extraidos = procesar_ticket(imagen_bytes)

        resultado = [
            {
             "date": datos_extraidos.get("fecha"),
             "cif": datos_extraidos.get("cif"),
             "total": datos_extraidos.get("total")
             },
           
            
        ]
        
        return {"data": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {str(e)}")