from typing import List, Dict, Any
from app.services.google_calendar_service import GoogleCalendarService
from langchain_core.tools import StructuredTool


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

    async def insert_event(self, event_body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Google Calendar에 새 일정을 생성
        일정 생성 전 일정 조회 후 요청된 날짜에 이미 일정이 있는 경우, 일정이 있음을 안내하고 다른 비어있는 날짜를 추천해야만 한다

        Args:
            event_body (dict): 생성할 일정의 상세 정보를 담은 딕셔너리
                        - summary (str): 일정의 제목 (예: "면접" 또는 "커피챗"). (필수)
                        - description (str): 사용자가 남긴 연락처, 주소 등 기타 상세 정보
                        - start (dict): 일정 시작 시간 딕셔너리. 다음 키를 포함:
                                - date (str): 일정 요청한 시작 날짜 'yyyy-mm-dd'
                                - timeZone (str): "Asia/Seoul" 로 고정된 값만 사용
                            - end (dict): 일정 종료 시간 딕셔너리. 다음 키를 포함:
                                - date (str): 일정 종료 날짜 'yyyy-mm-dd' 일정 시작 날짜의 다음 날짜
                                - timeZone (str): "Asia/Seoul" 로 고정된 값만 사용

        Returns:
            dict: 생성된 일정의 요약 정보 또는 일정 생성 실패 시 메시지
                  **성공 시:**
                    - summary (str): 생성된 일정의 제목.
                    - start (dict): 시작 날짜를 포함한 딕셔너리
                        - date (str): 시작 날짜 'yyyy-mm-dd'
                  **실패 시:**
                    - message (str): 실패 원인에 대한 설명.
        """
        return await self.gcal_service.insert_event(event_body)


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
            infer_schema=True,
            parse_docstring=True,
        ),
    ]
