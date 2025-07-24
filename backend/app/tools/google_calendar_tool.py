from typing import List, Dict, Any, Optional
from app.services.google_calendar_service import GoogleCalendarService
from langchain_core.tools import StructuredTool

from app.tools.models.calendar_tool_model import CreateEventToolInput


class GoogleCalendarTool:
    def __init__(self, gcal_service: GoogleCalendarService):
        self.gcal_service = gcal_service

    async def list_events(
        self, start_date: str, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Google Calendar에서 예정된 일정 리스트 확인.

        Args:
            start_date (str): 'yyyy-mm-dd' 형식의 조회 기준일 (필수)
            max_results (int): 조회할 최대 일정 개수. 기본값은 50 (선택)

        Return:
            list[dict]: 일정 딕셔너리 리스트 각 딕셔너리는 다음 키를 포함
                        - summary (str): 일정 제목
                        - start (str): 시작 날짜를 포함한 딕셔너리
                                 - date (str): 시작날짜 'yyyy-mm-dd'
        """
        return await self.gcal_service.list_events(start_date, max_results)

    async def insert_event(
        self,
        summary: str,
        start_date: str,
        end_date: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Returns:
            dict: 생성된 일정의 요약 정보 또는 일정 생성 실패 시 메시지
                  **성공 시:**
                    - summary (str): 생성된 일정의 제목.
                    - start (dict): 시작 날짜를 포함한 딕셔너리
                        - date (str): 시작 날짜 'yyyy-mm-dd'
                  **실패 시:**
                    - message (str): 실패 원인에 대한 설명.
        """
        tool_input = CreateEventToolInput(
            summary=summary,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )
        return await self.gcal_service.insert_event(tool_input.to_dict())


def get_google_calendar_tools(
    gcal_service: GoogleCalendarService,
) -> List[StructuredTool]:
    gcal_tool = GoogleCalendarTool(gcal_service)
    return [
        StructuredTool.from_function(
            coroutine=gcal_tool.list_events,
            infer_schema=True,
            parse_docstring=True,
        ),
        StructuredTool.from_function(
            coroutine=gcal_tool.insert_event,
            args_schema=CreateEventToolInput,
            parse_docstring=True,
        ),
    ]
