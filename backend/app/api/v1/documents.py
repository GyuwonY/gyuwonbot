from fastapi import APIRouter, UploadFile, File
from typing import List
from app.services import document_service

router = APIRouter()


@router.post("/upload-files/")
async def create_upload_files(
    files: List[UploadFile] = File(...)
):
    await document_service.process_and_embed_files(files)
    return {"message": "Files uploaded and embedded successfully"}

