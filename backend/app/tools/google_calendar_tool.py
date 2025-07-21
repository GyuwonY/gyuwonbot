import datetime
import os.path
from typing import List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_calendar_service() -> Resource | None:
    """
    Google Calendar API와 상호작용하기 위한 서비스 객체를 인증하고 반환합니다.

    Returns:
        Resource | None: 인증된 Google Calendar API 서비스 객체 또는 실패 시 None.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"오류: '{CREDENTIALS_FILE}'를 찾을 수 없습니다.")
                print("Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하고")
                print("프로젝트의 루트 디렉터리에 'credentials.json'으로 저장하세요.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"서비스를 빌드하는 동안 오류가 발생했습니다: {error}")
        return None


def list_upcoming_events(
    service: Resource, max_results: int = 10
) -> List[Dict[str, Any]] | None:
    """
    사용자의 기본 캘린더에서 예정된 이벤트를 가져옵니다.

    Args:
        service (Resource): 인증된 Google Calendar API 서비스 객체.
        max_results (int): 반환할 최대 이벤트 수.

    Returns:
        List[Dict[str, Any]] | None: 이벤트 목록 또는 실패 시 None.
    """
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])
    except HttpError as error:
        print(f"이벤트를 가져오는 동안 오류가 발생했습니다: {error}")
        return None


def create_event(
    service: Resource,
    summary: str,
    description: str,
    start_time: str,
    end_time: str,
    attendees: List[str] | None = None,
    location: str | None = None,
) -> Dict[str, Any] | None:
    """
    사용자의 기본 캘린더에 새 이벤트를 생성합니다.

    Args:
        service (Resource): 인증된 Google Calendar API 서비스 객체.
        summary (str): 이벤트 제목.
        description (str): 이벤트 설명.
        start_time (str): 이벤트 시작 시간 (RFC3339 형식).
        end_time (str): 이벤트 종료 시간 (RFC3339 형식).
        attendees (List[str] | None): 참석자 이메일 목록.
        location (str | None): 이벤트 장소.

    Returns:
        Dict[str, Any] | None: 생성된 이벤트 또는 실패 시 None.
    """
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "Asia/Seoul"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Seoul"},
    }
    if attendees:
        event["attendees"] = [{"email": email} for email in attendees]
    if location:
        event["location"] = location

    try:
        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )
        print(f"이벤트 생성됨: {created_event.get('htmlLink')}")
        return created_event
    except HttpError as error:
        print(f"이벤트를 생성하는 동안 오류가 발생했습니다: {error}")
        return None


def delete_event(service: Resource, event_id: str) -> bool:
    """
    사용자의 기본 캘린더에서 이벤트를 삭제합니다.

    Args:
        service (Resource): 인증된 Google Calendar API 서비스 객체.
        event_id (str): 삭제할 이벤트의 ID.

    Returns:
        bool: 성공적으로 삭제되면 True, 그렇지 않으면 False.
    """
    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"이벤트 ID '{event_id}'가 삭제되었습니다.")
        return True
    except HttpError as error:
        print(f"이벤트를 삭제하는 동안 오류가 발생했습니다: {error}")
        return False
