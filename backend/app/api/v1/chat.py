from functools import lru_cache
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.domain.chat import ChatRequest, ChatResponse
from app.services.agent_service import AgentService
from app.services.chat_service import ChatService
from app.services.google_calendar_service import GoogleCalendarService
from app.services.knowledge_base_service import KnowledgeBaseService
from app.services.notification_service import NotificationService
from app.infrastructure.database import get_db

router = APIRouter()


@lru_cache
def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        api_key=settings.GEMINI_API_KEY,
        temperature=0.7,
    )


@lru_cache
def get_google_calendar_service() -> GoogleCalendarService:
    return GoogleCalendarService()


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()


@router.post("/", response_model=ChatResponse)
async def chat_with_bot(
    fastapi_request: Request,
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    x_forwarded_for = fastapi_request.headers.get("X-Forwarded-For")
    session_id = (
        x_forwarded_for.split(",")[0].strip()
        if x_forwarded_for
        else fastapi_request.client.host
    )

    llm = get_llm()
    kb_service = KnowledgeBaseService(db_session=db)
    gc_service = get_google_calendar_service()
    notification_service = get_notification_service()

    agent_service = AgentService(
        llm=llm,
        knowledge_base_service=kb_service,
        google_calendar_service=gc_service,
        notification_service=notification_service,
    )

    chat_service = ChatService(agent_with_history=agent_service.create_agent())

    return await chat_service.chat(session_id, chat_request)
