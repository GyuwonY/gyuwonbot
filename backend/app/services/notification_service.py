import httpx
from app.core.config import settings


class NotificationService:
    def __init__(self):
        self.webhook_url = settings.DISCORD_WEBHOOK_URL

    async def send_message(self, message: str):
        """
        Discord 웹훅으로 비동기 메시지를 전송합니다.
        """
        if not self.webhook_url:
            # 웹훅 URL이 설정되지 않은 경우, 콘솔에만 출력
            print(f"Notification (no webhook URL): {message}")
            return

        async with httpx.AsyncClient() as client:
            payload = {"content": message}
            try:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
            except httpx.HTTPStatusError as e:
                print(f"Discord 웹훅 전송 실패: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                print(f"Discord 웹훅 요청 실패: {e}")

notification_service = NotificationService()
