from langchain_core.tools import StructuredTool
from app.services.knowledge_base_service import KnowledgeBaseService
from app.domain.knowledge_base import KnowledgeBase
from typing import Dict, List, Optional


class KnowledgeBaseTool:
    def __init__(self, kb_service: KnowledgeBaseService):
        self.kb_service = kb_service

    async def search(self, query: str) -> List[Dict[str, Optional[str]]]:
        """
        이력서, 기술 스택, 프로젝트 경험, TMI 등 구체적인 정보에 대한 질문에 사용
        가장 연관성이 높은 정보 5개를 리스트 형태로 반환

        Args:
            query (str): 사용자의 검색 질문.

        Returns:
            list[dict]: 검색된 문서의 내용을 담은 딕셔너리 리스트
                - source_type (str): 정보의 출처 유형 ('qna' 또는 'resume')
                - topic (str): 정보의 주요 주제
                - question (Optional[str]): 해당 정보가 Q&A 형식일 경우 예상 질문의 내용. Q&A가 아닐 경우 None입니다.
                - content (str): 검색된 문서의 실제 내용 또는 답변.
        """
        return await self.kb_service.search_similar_documents(query=query)


def get_knowledge_base_tool(kb_service: KnowledgeBaseService) -> StructuredTool:
    kb_tool = KnowledgeBaseTool(kb_service)
    return StructuredTool.from_function(
        coroutine=kb_tool.search,
        infer_schema=True,
        parse_docstring=True,
    )
