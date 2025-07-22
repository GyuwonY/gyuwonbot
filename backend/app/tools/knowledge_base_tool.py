from typing import List
from app.services.knowledge_base_service import KnowledgeBaseService
from app.domain.knowledge_base import KnowledgeBase
from langchain_core.tools import tool


@tool(
    "search_knowledge_base",
    description="""
        이력서, 기술 스택, 프로젝트 경험, TMI 등 구체적인 정보에 대한 질문에 사용됩니다.

        Args:
            query (str): 사용자의 검색 질문.
            kb_service (KnowledgeBaseService): 검색을 수행할 서비스 객체.

        Returns:
            List[str]: 검색된 각 문서의 내용을 담은 문자열 리스트.
    """,
)
async def search_knowledge_base(
    query: str, kb_service: KnowledgeBaseService
) -> List[str]:
    similar_documents: List[KnowledgeBase] = await kb_service.search_similar_documents(
        query=query
    )

    if not similar_documents:
        return ["관련 정보를 찾을 수 없습니다."]

    return [doc.content for doc in similar_documents]
