from fastapi import FastAPI
from ocr_router  import ocr_api_router

app = FastAPI()

app.include_router(ocr_api_router, prefix="/ocr", tags=["OCR"])