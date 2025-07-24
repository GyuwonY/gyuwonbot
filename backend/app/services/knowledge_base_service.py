from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import pandas as pd
from fastapi import UploadFile
from typing import Any, Dict, List, Optional
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
        self.embeddings_model: GoogleGenerativeAIEmbeddings | None = None

    async def _get_or_create_embeddings_model(self) -> GoogleGenerativeAIEmbeddings:
        if self.embeddings_model is None:
            self.embeddings_model = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                google_api_key=settings.GEMINI_API_KEY,
            )
        return self.embeddings_model

    async def _get_embeddings(self, text: str) -> List[float]:
        model = await self._get_or_create_embeddings_model()
        return await model.aembed_query(
            text=text,
            output_dimensionality=768,
        )

    async def _process_csv(
        self, file: UploadFile, filename: str
    ) -> List[KnowledgeBase]:
        try:
            content = await file.read()
            df = await asyncio.to_thread(pd.read_csv, io.BytesIO(content))

            texts_to_embed = [
                f"주제: {row['Topic']}\n검색 키워드: {row['Search_Keywords']}\n질문 키워드: {row['Question_Keywords']}"
                for _, row in df.iterrows()
            ]
            model = await self._get_or_create_embeddings_model()
            embeddings = await model.aembed_documents(
                texts_to_embed, output_dimensionality=768
            )

            knowledge_bases = []
            for (_, row), embedding in zip(df.iterrows(), embeddings):
                knowledge_bases.append(
                    KnowledgeBase(
                        source_type=SourceTypeEnum.QNA,
                        persona=row["Persona"],
                        topic=row["Topic"],
                        question=row["Question"],
                        content=row["Answer"],
                        search_keyword=row["Search_Keywords"],
                        question_keyword=row["Question_Keywords"],
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
            texts_to_embed = [
                doc.metadata.get("Section")
                + ", "
                + doc.page_content.split("\n---\n")[0]
                for doc in split_documents
            ]
            model = await self._get_or_create_embeddings_model()
            embeddings = await model.aembed_documents(
                texts_to_embed, output_dimensionality=768
            )

            knowledge_bases = []
            for doc, embedding in zip(split_documents, embeddings):
                split_docs = doc.page_content.split("\n---\n")
                topic = doc.metadata.get("Section")
                if doc.metadata.get("Sub-Section"):
                    topic += f": {doc.metadata.get("Sub-Section")}"

                knowledge_bases.append(
                    KnowledgeBase(
                        source_type=SourceTypeEnum.RESUME,
                        topic=topic,
                        search_keyword=split_docs[0],
                        content=split_docs[1],
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
        self, query: str, top_k: int = 5
    ) -> List[Dict[str, Optional[str]]]:
        query_embedding = await self._get_embeddings(query)
        stmt = (
            select(KnowledgeBase)
            .order_by(KnowledgeBase.embedding.l2_distance(query_embedding))
            .limit(top_k)
        )

        result = await self.db_session.execute(stmt)
        similar_documents = result.scalars().all()

        return [doc.to_dict() for doc in similar_documents]
