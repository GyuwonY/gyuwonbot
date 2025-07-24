from fastapi import APIRouter, Depends

from app.domain.notification import Notification
from app.services.notification_service import NotificationService

router = APIRouter()


@router.post("/", response_model=dict)
async def send_notification(
    notification: Notification,
    notification_service: NotificationService = Depends(),
) -> dict:
    await notification_service.send_message(
        f"GetInTouch 메세지\n이름: {notification.name}\n연락처: {notification.email}\n메세지: {notification.message}"
    )
    return {"message": "Notification sent successfully"}
