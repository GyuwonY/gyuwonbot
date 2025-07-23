from langchain_core.tools import StructuredTool
from app.services.knowledge_base_service import KnowledgeBaseService
from app.domain.knowledge_base import KnowledgeBase
from typing import List


class KnowledgeBaseTool:
    """
    이력서, 기술 스택, 프로젝트 경험, TMI 등 구체적인 정보에 대한 질문에 사용됩니다.
    가장 연관있는 정보 3개의 리스트

    Args:
        query (str): 사용자의 검색 질문.

    Returns:
        List[KnowledgeBase]: 검색된 각 문서의 내용을 담은 KnowledgeBase 객체 리스트.
            [
                {
                    "id": int,
                    "source_type": str,  # 'qna' or 'resume'
                    "q_id": Optional[str],
                    "persona": Optional[str],
                    "topic": str,
                    "question": Optional[str],
                    "content": str
                }
            ]
    """

    def __init__(self, kb_service: KnowledgeBaseService):
        self.kb_service = kb_service

    async def search(self, query: str) -> List[KnowledgeBase]:
        return await self.kb_service.search_similar_documents(query=query)


def get_knowledge_base_tool(kb_service: KnowledgeBaseService) -> StructuredTool:
    kb_tool = KnowledgeBaseTool(kb_service)
    return StructuredTool.from_function(
        func=kb_tool.search,
        name="search_knowledge_base",
        description=KnowledgeBaseTool.__doc__,
    )
