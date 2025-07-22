from langchain_core.tools import tool
from app.services.notification_service import NotificationService

tool_usage_rule = """
    작업 보고: 다음의 상황이 발생한 경우 상황에 맞는 메세지를 보내야함
        첫 방문자 발생, 비어있는 일정 확인, 면접 제안, 커피챗 제안, 연락처 요청
        * 예시: "💼 면접 제안: 2025-08-01 15:00", "📞 연락처 요청", "첫 방문 발생", "일정 확인 발생"

    Args:
        message (str): 예시와 같은 메세지
        notification_service (NotificationService): 메세지 발송을 수행할 객체.

    Returns:
        str: 성공 여부 메세지
"""


@tool(
    "discord_notification",
    description=tool_usage_rule,
)
async def discord_notification(
    message: str, notification_service: NotificationService
) -> str:
    await notification_service.send_message(message)
    return "전송 성공"
