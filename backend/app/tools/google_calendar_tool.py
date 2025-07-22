from typing import List, Dict, Any
from app.services.google_calendar_service import GoogleCalendarService
from langchain_core.tools import tool

list_calendar_events_usage_rule = """
    Google Calendar에서 예정된 일정 리스트 확인.
    날짜는 한국시 기준

    Args:
        start_date: 조회 기준일 'yyyy-mm-dd' (필수), 
        max_results: 조회 기준일로부터 조회할 일정 갯수 Defalut=50 (선택).
        calendar_service (GoogleCalendarService): 이벤트 조회 수행 객체

    Return:
        {
            "items": [
                summary (str): 일정 제목
                start (str)): {
                    date: 'yyyy-mm-dd'
                }
            ]
        }
"""


@tool(
    "list_calendar_events",
    description=list_calendar_events_usage_rule,
)
async def list_calendar_events(
    calendar_service: GoogleCalendarService, start_date: str, max_results: int = 50
) -> List[Dict[str, Any]]:
    return await calendar_service.list_events(start_date, max_results)


insert_calendar_event_usage_rule = """
    Google Calendar에 새 일정 생성
    날짜는 한국시 기준
    Args의 구조를 참조하여 각 자료형과 type, 내용을 참고하여 입력
    요청한 날짜는 start.date, end.date에 입력
    Args:
        event_body (Dict[str, str]): {
            summary (str): 면접 or 커피챗 (필수),
            description (str): 사용자가 남긴 연락처, 주소 등 기타 정보,
            start (Dict[str, str]): {
                date (str): 'yyyy-mm-dd',
                timeZone (str): 'Asia/Seoul'
            } 요청 일정 날짜,
            end (Dict[str, str]): {
                date (str): 'yyyy-mm-dd',
                timeZone (str): 'Asia/Seoul'
            } 요청 일정 날짜
        },
        calendar_service (GoogleCalendarService): 이벤트 생성 수행 객체

    Return:
        {
            summary: string
            start: {
                date: 'yyyy-mm-dd'
            }
        }
"""


@tool(
    "insert_calendar_event",
    description=insert_calendar_event_usage_rule,
)
async def insert_calendar_event(
    calendar_service: GoogleCalendarService, event_body: Dict[str, Any]
) -> Dict[str, Any]:
    return await calendar_service.insert_event(event_body)
