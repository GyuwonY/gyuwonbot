import httpx
from app.core.config import settings


class NotificationService:
    def __init__(self):
        self.webhook_url = settings.DISCORD_WEBHOOK_URL

    async def send_message(self, message: str):
        if not self.webhook_url:
            return f"전송 실패 (no webhook URL)"

        async with httpx.AsyncClient() as client:
            payload = {"content": message}
            try:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                return f"Discord 웹훅 전송 실패: {e.response.status_code} - {e.response.text}"
            except httpx.RequestError as e:
                return f"Discord 웹훅 요청 실패: {e}"
