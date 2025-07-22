from langchain.agents import AgentExecutor, Tool, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_redis import RedisChatMessageHistory

from app.core.config import settings
from app.domain.chat import ChatRequest, ChatResponse
from app.tools.google_calendar_tool import (
    create_event,
    get_calendar_service,
    list_upcoming_events,
)
from app.tools.notification_tool import discord_notification


class ChatService:
    def __init__(self):
        """ChatService 초기화"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
        )
        self.tools = self._initialize_tools()
        self.prompt = self._create_prompt_template()
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=True
        )

    def _initialize_tools(self) -> list:
        """사용 가능한 도구를 초기화합니다."""
        tools = [discord_notification]
        calendar_service = get_calendar_service()
        if calendar_service:
            tools.extend(
                [
                    Tool(
                        name="list_calendar_events",
                        func=lambda max_results=20: list_upcoming_events(
                            calendar_service, max_results
                        ),
                        description="Google Calendar에서 예정된 이벤트를 확인합니다. 최대 결과 수를 지정할 수 있습니다.",
                    ),
                    Tool(
                        name="create_calendar_event",
                        func=lambda summary,
                        description,
                        start_time,
                        end_time,
                        attendees=None,
                        location=None: create_event(
                            calendar_service,
                            summary,
                            description,
                            start_time,
                            end_time,
                            attendees,
                            location,
                        ),
                        description="Google Calendar에 새 이벤트를 생성합니다. 이벤트 제목, 설명, 시작 시간, 종료 시간을 필수로 포함해야 합니다. 참석자 및 장소는 선택 사항입니다. 시간은 'YYYY-MM-DDTHH:MM:SS' 형식이어야 합니다.",
                    ),
                ]
            )
        else:
            print(
                "Google Calendar 서비스 오류"
            )
        return tools

        self.prompt = self._create_prompt_template()
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=True
        )

    @staticmethod
    def _load_system_prompt() -> str:
        """파일에서 시스템 프롬프트를 로드합니다."""
        with open("prompt.md", "r", encoding="utf-8") as f:
            return f.read()

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """에이전트 프롬프트 템플릿을 생성합니다."""
        system_prompt = self._load_system_prompt()
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    def get_agent_with_history(self) -> RunnableWithMessageHistory:
        """세션 기록을 관리하는 에이전트를 반환합니다."""
        return RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: RedisChatMessageHistory(
                session_id, url=settings.REDIS_URL
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    async def chat(self, session_id: str, request: ChatRequest) -> ChatResponse:
        """에이전트를 사용하여 채팅 응답을 생성합니다."""
        agent_with_history = self.get_agent_with_history()
        response = await agent_with_history.ainvoke(
            {"input": request.message},
            config={"configurable": {"session_id": session_id}},
        )
        return ChatResponse(content=response["output"])
