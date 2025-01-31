from fastapi import FastAPI
from ocr_api import ocr_api_router # Suponiendo que el endpoint está en ocr_api.py

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(ocr_api_router)  