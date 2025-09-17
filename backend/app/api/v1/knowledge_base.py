from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.services.knowledge_base_service import KnowledgeBaseService
from app.infrastructure.database import get_db

router = APIRouter()


def get_knowledge_base_service(
    db: AsyncSession = Depends(get_db),
) -> KnowledgeBaseService:
    return KnowledgeBaseService(db_session=db)


@router.post("/upload-files")
async def create_upload_files(
    files: List[UploadFile] = File(...),
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    await kb_service.add_files_to_knowledge_base(files)
    return {"message": "Files uploaded and embedded successfully"}
