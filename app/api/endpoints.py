from fastapi import APIRouter, UploadFile, File, HTTPException, status
import shutil
import os

from app.models.schemas import QueryRequest, QueryResponse, IngestResponse
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/upload", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File(...)):
    """PDF fájl feltöltése és automatikus indexelése a ChromaDB-be."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Csak PDF fájlok tölthetők fel!")

    # Ideiglenes mentés a lemezre a feldolgozáshoz
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Meghívjuk a korábban megírt rag_service-t
        result = rag_service.ingest_pdf(temp_path)
        return result
    finally:
        # A feldolgozás után töröljük az ideiglenes fájlt
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/chat", response_model=QueryResponse)
async def chat_query(request: QueryRequest):
    """Kérdés feltevése az indexelt dokumentumokkal kapcsolatban."""
    try:
        response = rag_service.answer_query(
            question=request.question, 
            top_k=request.top_k
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))