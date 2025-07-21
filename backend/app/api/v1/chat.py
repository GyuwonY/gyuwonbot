from fastapi import APIRouter, Depends, Request
from app.domain.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

# ChatService를 싱글톤으로 관리
chat_service_instance = ChatService()


def get_chat_service():
    return chat_service_instance


@router.post("/", response_model=ChatResponse)
async def chat_with_bot(
    fastapi_request: Request,
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    x_forwarded_for = fastapi_request.headers.get("X-Forwarded-For")

    if x_forwarded_for:
        session_id = x_forwarded_for.split(",")[0].strip()
    else:
        session_id = fastapi_request.client.host

    return await chat_service.chat(session_id, chat_request)
