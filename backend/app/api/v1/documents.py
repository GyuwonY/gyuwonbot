from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.services import document_service

router = APIRouter()


@router.post("/upload-files/")
async def create_upload_files(
    files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    await document_service.process_and_embed_files(db, files)
    return {"message": "Files uploaded and embedded successfully"}
