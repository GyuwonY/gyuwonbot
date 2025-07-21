from sqlalchemy.orm import Session
import pandas as pd
from fastapi import UploadFile
from typing import List
from app.domain.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
from app.core.exceptions import (
    CSVProcessingError,
    MDProcessingError,
    UnsupportedFileTypeError,
)


def get_embeddings(text: str):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=settings.gemini_api_key
    )
    return embeddings.embed_query(text)


async def _process_csv(db: Session, file: UploadFile, filename: str):
    try:
        df = pd.read_csv(file.file)
        for _, row in df.iterrows():
            if "Question" not in row or "Answer" not in row:
                continue
            text_to_embed = f"{row['Question']} {row['Answer']}"
            embedding = get_embeddings(text_to_embed)
            db_document = Document(content=text_to_embed, embedding=embedding)
            db.add(db_document)
    except Exception as e:
        raise CSVProcessingError(filename=filename, original_exception=e)


async def _process_md(db: Session, file: UploadFile, filename: str):
    try:
        content = await file.read()
        text_to_embed = content.decode("utf-8")
        embedding = get_embeddings(text_to_embed)
        db_document = Document(content=text_to_embed, embedding=embedding)
        db.add(db_document)
    except Exception as e:
        raise MDProcessingError(filename=filename, original_exception=e)


async def process_and_embed_files(db: Session, files: List[UploadFile]):
    for file in files:
        if file.filename is None:
            raise ValueError()

        if file.filename.endswith(".csv"):
            await _process_csv(db, file, file.filename)
        elif file.filename.endswith(".md"):
            await _process_md(db, file, file.filename)
        else:
            raise UnsupportedFileTypeError(filename=file.filename)

    db.commit()
