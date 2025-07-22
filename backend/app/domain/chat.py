from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(description="사용자 메시지")


class ChatResponse(BaseModel):
    content: str
