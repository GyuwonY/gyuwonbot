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
        날짜는 한국시 기준

        Args:
            start_date (str): 'yyyy-mm-dd' 형식의 조회 기준일 (필수)
            max_results (int): 조회할 최대 일정 개수. 기본값은 50 (선택)

        Return:
            {
                "items": [
                    {
                        "summary": str,  # 일정 제목
                        "start": {
                            "date": str  # 'yyyy-mm-dd'
                        }
                    }
                ]
            }
        """
        return await self.gcal_service.list_events(start_date, max_results)

    async def insert_event(self, event_body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Google Calendar에 새 일정 생성
        날짜는 한국시 기준

        Args:
            event_body (Dict[str, Any]): {
                "summary": str,  # "면접" 또는 "커피챗" (필수)
                "description": str,  # 사용자가 남긴 연락처, 주소 등 기타 정보
                "start": {
                    "date": str,  # 'yyyy-mm-dd', 사용자가 요청한 날짜
                    "timeZone": str  # 'Asia/Seoul'
                },
                "end": {
                    "date": str,  # 'yyyy-mm-dd', start.date와 동일한 값
                    "timeZone": str  # 'Asia/Seoul'
                }
            }

        Return:
            {
                "summary": str,
                "start": {
                    "date": str  # 'yyyy-mm-dd'
                }
            }
        """
        return await self.gcal_service.insert_event(event_body)


def get_google_calendar_tools(
    gcal_service: GoogleCalendarService,
) -> List[StructuredTool]:
    gcal_tool = GoogleCalendarTool(gcal_service)
    return [
        StructuredTool.from_function(
            func=gcal_tool.list_events,
            name="list_calendar_events",
            description=gcal_tool.list_events.__doc__,
        ),
        StructuredTool.from_function(
            func=gcal_tool.insert_event,
            name="insert_calendar_event",
            description=gcal_tool.insert_event.__doc__,
        ),
    ]