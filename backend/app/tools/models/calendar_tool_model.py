from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class CreateEventToolInput(BaseModel):
    """
    Google Calendar에 '하루 종일' 일정을 생성, 날짜 기준으로 일정을 생성하며, 시간은 description에 남긴다
    'start'와 'end' 객체 안에는 'date' 필드만 사용해야 하며, 'dateTime'은 절대 사용하면 안된다.
    일정 생성 전 일정 조회 후 요청된 날짜에 이미 일정이 있는 경우, 일정이 있음을 안내하고 다른 비어있는 날짜를 추천해야만 한다
    """

    summary: str = Field(
        ...,
        description="일정의 제목 (예: '면접' 또는 '커피챗'). 필수",
    )

    description: Optional[str] = Field(
        None,
        description="사용자가 남긴 연락처, 주소 등 기타 상세 정보.",
    )

    start_date: str = Field(
        ...,
        description="일정 시작 날짜 (YYYY-MM-DD 형식).",
    )

    end_date: str = Field(
        ...,
        description="일정 종료 날짜 (YYYY-MM-DD 형식). 시작 날짜의 다음 날짜로 설정",
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "description": self.description,
            "start": {
                "date": self.start_date,
                "timeZone": "Asia/Seoul",
            },
            "end": {
                "date": self.start_date,
                "timeZone": "Asia/Seoul",
            },
        }
