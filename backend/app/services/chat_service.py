from langchain_core.runnables.history import RunnableWithMessageHistory
from app.domain.chat import ChatRequest, ChatResponse


class ChatService:

    def __init__(self, agent_with_history: RunnableWithMessageHistory):
        self.agent_with_history = agent_with_history

    async def chat(self, session_id: str, request: ChatRequest) -> ChatResponse:
        response = await self.agent_with_history.ainvoke(
            {"input": request.message},
            config={"configurable": {"session_id": session_id}},
        )

        return ChatResponse(content=response["output"])
