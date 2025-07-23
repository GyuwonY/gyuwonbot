from datetime import datetime
from zoneinfo import ZoneInfo
from langchain_core.tools import StructuredTool


def get_current_date() -> str:
    """
    '내일', '다음주', '몇 일 후' 등 상대적인 날짜를 이야기 하거나 연도, 월 등의 정보가 필요한 경우 조회
    오늘 날짜와 요일을 'yyyy-mm-dd (요일)' 형식으로 반환
    'Asia/Seoul' 기준.
    """
    seoul_tz = ZoneInfo("Asia/Seoul")
    now_in_seoul = datetime.now(seoul_tz)

    days_in_korean = ["월", "화", "수", "목", "금", "토", "일"]
    day_of_week = days_in_korean[now_in_seoul.weekday()]

    return f"{now_in_seoul.strftime('%Y-%m-%d')} ({day_of_week})"


def get_date_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=get_current_date,
        description=get_current_date.__doc__,
    )
