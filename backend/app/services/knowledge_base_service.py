from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import pandas as pd
from fastapi import UploadFile
from typing import List
import asyncio
import io

from app.domain.knowledge_base import KnowledgeBase, SourceTypeEnum
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from app.core.config import settings
from app.core.exceptions import (
    CSVProcessingError,
    MDProcessingError,
    UnsupportedFileTypeError,
)


class KnowledgeBaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.embeddings_model = GoogleGenerativeAIEmbeddings(
            model="text-multilingual-embedding-002",
            google_api_key=settings.GEMINI_API_KEY,
        )

    async def _get_embeddings(self, text: str) -> List[float]:
        return await self.embeddings_model.aembed_query(text)

    async def _process_csv(
        self, file: UploadFile, filename: str
    ) -> List[KnowledgeBase]:
        try:
            content = await file.read()
            df = await asyncio.to_thread(pd.read_csv, io.BytesIO(content))

            texts_to_embed = [
                f"질문: {row['Question']}\n답변: {row['Answer']}"
                for _, row in df.iterrows()
            ]
            embeddings = await self.embeddings_model.aembed_documents(texts_to_embed)

            knowledge_bases = []
            for (_, row), embedding in zip(df.iterrows(), embeddings):
                knowledge_bases.append(
                    KnowledgeBase(
                        source_type=SourceTypeEnum.QNA,
                        persona=row["Persona"],
                        topic=row["Topic"],
                        question=row["Question"],
                        content=row["Answer"],
                        embedding=embedding,
                    )
                )
            return knowledge_bases
        except Exception as e:
            raise CSVProcessingError(filename=filename, original_exception=e)

    async def _process_md(self, file: UploadFile, filename: str) -> List[KnowledgeBase]:
        try:
            content = await file.read()
            text_content = await asyncio.to_thread(content.decode, "utf-8")

            headers_to_split_on = [("##", "Section"), ("###", "Sub-Section")]
            markdown_splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on
            )
            split_documents = markdown_splitter.split_text(text_content)

            texts_to_embed = [doc.page_content for doc in split_documents]
            embeddings = await self.embeddings_model.aembed_documents(texts_to_embed)

            knowledge_bases = []
            for doc, embedding in zip(split_documents, embeddings):
                knowledge_bases.append(
                    KnowledgeBase(
                        source_type=SourceTypeEnum.RESUME,
                        topic=doc.metadata.get(
                            "Sub-Section", doc.metadata.get("Section", "일반")
                        ),
                        content=doc.page_content,
                        embedding=embedding,
                    )
                )
            return knowledge_bases
        except Exception as e:
            raise MDProcessingError(filename=filename, original_exception=e)

    async def add_files_to_knowledge_base(self, files: List[UploadFile]):
        all_new_kb_items = []
        for file in files:
            if file.filename is None:
                continue

            if file.filename.endswith(".csv"):
                kb_items = await self._process_csv(file, file.filename)
                all_new_kb_items.extend(kb_items)
            elif file.filename.endswith(".md"):
                kb_items = await self._process_md(file, file.filename)
                all_new_kb_items.extend(kb_items)
            else:
                raise UnsupportedFileTypeError(filename=file.filename)

        if all_new_kb_items:
            self.db_session.add_all(all_new_kb_items)
            await self.db_session.commit()

    async def search_similar_documents(
        self, query: str, top_k: int = 10
    ) -> List[KnowledgeBase]:
        query_embedding = await self._get_embeddings(query)
        stmt = (
            select(KnowledgeBase)
            .order_by(KnowledgeBase.embedding.l2_distance(query_embedding))
            .limit(top_k)
        )

        result = await self.db_session.execute(stmt)
        similar_documents = result.scalars().all()

        return list(similar_documents)
