from typing import List, Dict, Any
import json
import asyncio
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from app.core.config import settings


class GoogleCalendarService:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self):
        try:
            with open(settings.GOOGLE_SERVICE_ACCOUNT_JSON, "r") as f:
                service_account_info = json.load(f)
            self.creds = Credentials.from_service_account_info(
                service_account_info, scopes=self.SCOPES
            )
            self.service: Resource = build("calendar", "v3", credentials=self.creds)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"GOOGLE_SERVICE_ACCOUNT_JSON json decode error: {e}")
        except Exception as e:
            raise RuntimeError(f"Google 계정 인증 실패: {e}")

    async def list_events(
        self, start_date: str, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        fields_to_include = "items(summary,start)"
        try:
            events_result = await asyncio.to_thread(
                self.service.events()
                .list(
                    calendarId=settings.CALENDAL_ID,
                    timeMin=f"{start_date}T00:00:00Z",
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                    fields=fields_to_include,
                )
                .execute
            )
            return events_result.get("items", [])
        except HttpError as error:
            raise RuntimeError(f"캘린더 이벤트 조회 중 오류 발생: {error}")

    async def insert_event(self, event_body: Dict[str, Any]) -> Dict[str, Any]:
        fields_to_include = "summary,start"
        try:
            event = await asyncio.to_thread(
                self.service.events()
                .insert(
                    calendarId=settings.CALENDAL_ID,
                    body=event_body,
                    fields=fields_to_include,
                )
                .execute
            )
            return event
        except HttpError as error:
            return {"message": f"캘린더 이벤트 등록 중 오류 발생: {error}"}


def get_calendar_service() -> GoogleCalendarService:
    return GoogleCalendarService()
