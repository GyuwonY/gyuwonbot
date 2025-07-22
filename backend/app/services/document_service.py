from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from fastapi import UploadFile
from typing import List
from app.domain import knowledge_base
from app.domain.knowledge_base import KnowledgeBase, SourceTypeEnum
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from app.core.config import settings
from app.core.exceptions import (
    CSVProcessingError,
    MDProcessingError,
    UnsupportedFileTypeError,
)
from app.infrastructure.database import AsyncSessionLocal


async def get_embeddings(text: str):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=settings.GEMINI_API_KEY
    )
    return embeddings.embed_query(text)


async def _process_csv(file: UploadFile, filename: str):
    try:
        df = pd.read_csv(file.file)
        knowledge_bases = []
        
        for index, row in df.iterrows():
            content_text = f"질문: {row['Question']}\n답변: {row['Answer']}"
            
            knowledge_bases.append(
                KnowledgeBase(
                    source_type = SourceTypeEnum('qna'),
                    q_id = row['Q_ID'],
                    persona = row['Persona'],
                    topic = row['Topic'],
                    question = row['Question'],
                    content = row['Answer'],
                    embedding = await get_embeddings(content_text)
                )
            )
            
        return knowledge_bases
    except Exception as e:
        raise CSVProcessingError(filename=filename, original_exception=e)


async def _process_md(file: UploadFile, filename: str):
    try:
        content = await file.read()
        text_to_embed = content.decode("utf-8")
                
        headers_to_split_on = [
            ("##", "Section"),
            ("###", "Sub-Section"),
        ]
        
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        split_documents = markdown_splitter.split_text(text_to_embed)
        knowledge_bases = []
        
        for doc in split_documents:
            content_text = doc.page_content
            
            knowledge_bases.append(
                KnowledgeBase(
                    source_type = SourceTypeEnum('resume'),
                    topic = doc.metadata.get(
                        'Sub-Section', 
                        doc.metadata.get('Section', '일반')
                    ),
                    content = content_text,
                    embedding = await get_embeddings(content_text)
                )
            )
            
        return knowledge_bases
    except Exception as e:
        raise MDProcessingError(filename=filename, original_exception=e)


async def process_and_embed_files(files: List[UploadFile]):
    knowledge_bases = []
    for file in files:
        if file.filename is None:
            raise ValueError()

        if file.filename.endswith(".csv"):
            knowledge_bases.append(
                await _process_csv(file, file.filename)
            )
            
        elif file.filename.endswith(".md"):
            knowledge_bases.append(
                await _process_md(file, file.filename)
            )
            
        else:
            raise UnsupportedFileTypeError(filename=file.filename)
        
    async with AsyncSessionLocal() as db:
        db.add_all(knowledge_bases)
        await db.commit()

