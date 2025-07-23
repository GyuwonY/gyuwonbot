from app.services.notification_service import NotificationService
from langchain_core.tools import StructuredTool


class NotificationTool:
    """작업 보고: 특정 상황 발생 시 Discord로 알림을 보냅니다.

    다음 상황에 사용됩니다:
    - 첫 방문자 발생
    - 비어있는 일정 확인
    - 면접 제안
    - 커피챗 제안
    - 연락처 요청

    * 예시: "💼 면접 제안: 2025-08-01 15:00", "📞 연락처 요청"

    Args:
        message (str): 예시와 같은 형식의 알림 메시지.

    Returns:
        str: 전송 성공 여부 메시지.
    """

    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    async def send_discord_notification(self, message: str) -> str:
        await self.notification_service.send_message(message)
        return "전송 성공"


def get_notification_tool(notification_service: NotificationService) -> StructuredTool:
    notification_tool = NotificationTool(notification_service)
    return StructuredTool.from_function(
        func=notification_tool.send_discord_notification,
        name="discord_notification",
        description=NotificationTool.__doc__,
    )
