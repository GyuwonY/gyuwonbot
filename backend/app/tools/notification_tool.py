from langchain_core.tools import tool
from app.services.notification_service import notification_service

tool_usage_rule = """
[도구 사용 규칙]
작업 보고: 다음의 상황이 발생한 경우 상황에 맞는 메세지를 보내야함
    첫 방문자 발생, 비어있는 일정 확인, 면접 제안, 커피챗 제안, 연락처 요청
    * 예시: "💼 면접 제안: 2025-08-01 15:00", "📞 연락처 요청", "첫 방문"
"""


@tool(
    "discord_notification",
    description=tool_usage_rule,
)
async def discord_notification(message: str) -> str:
    await notification_service.send_message(message)
    return "Notification sent successfully."
