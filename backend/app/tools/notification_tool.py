from app.services.notification_service import NotificationService
from langchain_core.tools import StructuredTool


class NotificationTool:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    async def send_discord_notification(self, message: str) -> str:
        """
        특정 상황 발생 시 Discord 채널로 알림을 보냅니다.

        다음과 같은 상황에 사용:
        - 첫 방문자가 발생했을 때 (현재까지의 채팅 히스토리가 없는 경우)
        - 면접 또는 커피챗 가능한 일정 확인을 요청받았을 때
        - 면접 제안을 받았을 때
        - 커피챗을 받았을 때
        - 유규원의 연락처 정보를 받았을 때

        메시지 예시: "💼 면접 제안: 2025-08-01 15:00", "📞 연락처 요청 발생"

        Args:
            message (str): Discord로 보낼 알림 메시지 내용. 상황에 맞는 구체적이고 요약된 정보를 포함해야 합니다.

        Returns:
            str: 알림 전송의 성공 또는 실패를 나타내는 메시지.
                성공 시: 전송 성공
                실패 시: 실패 사유
        """
        return await self.notification_service.send_message(message)


def get_notification_tool(notification_service: NotificationService) -> StructuredTool:
    notification_tool = NotificationTool(notification_service)
    return StructuredTool.from_function(
        coroutine=notification_tool.send_discord_notification,
        infer_schema=True,
        parse_docstring=True,
    )
