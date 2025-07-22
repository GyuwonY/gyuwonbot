import os.path
import json # json 모듈 임포트
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.core.config import settings

# Google Calendar API 스코프 정의
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_calendar_service_service_account():
    """
    서비스 계정 JSON 문자열을 사용하여 Google Calendar API 서비스 객체를 반환합니다.
    FastAPI의 Depends에 사용될 수 있도록 제너레이터 함수로 구현합니다.
    """
    try:
        service_account_info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)

        creds = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)
        
        yield service
    except json.JSONDecodeError as e:
        raise RuntimeError(f"GOOGLE_SERVICE_ACCOUNT_JSON json decode error: {e}")
    except Exception as e:
        raise RuntimeError(f"Google 계정 인증 실패: {e}")


async def list_calendar_events(service, start_date, max_results: int = 14) -> list:
    """
    start_date format yyyy-mm-dd
    """
    try:
        events_result = service.events().list(
            calendarId=settings.CALENDAL_ID,
            timeMin="${start_date}T00:00:00Z",
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        return events
    except HttpError as error:
        raise RuntimeError(f"캘린더 이벤트 조회 중 오류 발생: {error}")


async def insert_calendar_event(service, event_body: dict) -> dict:
    """
    summary: 이벤트 제목 (require)
    description: 이벤트 설명
    start: { 
        dateTime: yyyy-mm-dd
        timeZone: "Asia/Seoul"
    } (require)
    
    
    """
    calendar_id = settings.CALENDAL_ID
    try:
        event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
        return event
    except HttpError as error:
        raise RuntimeError(f"캘린더 이벤트 등록 중 오류 발생: {error}")
