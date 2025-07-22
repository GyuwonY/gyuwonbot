from functools import partial
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_redis import RedisChatMessageHistory

from app.core.config import settings
from app.services.google_calendar_service import GoogleCalendarService
from app.services.knowledge_base_service import KnowledgeBaseService
from app.services.notification_service import NotificationService
from app.tools.google_calendar_tool import (
    list_calendar_events,
    insert_calendar_event,
)
from app.tools.notification_tool import discord_notification
from app.tools.knowledge_base_tool import search_knowledge_base


class AgentService:

    def __init__(
        self,
        knowledge_base_service: KnowledgeBaseService,
        google_calendar_service: GoogleCalendarService,
        notification_service: NotificationService,
        llm: ChatGoogleGenerativeAI,
    ):
        self.knowledge_base_service = knowledge_base_service
        self.google_calendar_service = google_calendar_service
        self.notification_service = notification_service
        self.llm = llm
        self.tools = self._initialize_tools()
        self.prompt = self._create_prompt_template()

    def _initialize_tools(self) -> list:
        search_knowledge_base_with_service = partial(
            search_knowledge_base, kb_service=self.knowledge_base_service
        )
        list_calendar_events_with_service = partial(
            list_calendar_events, gcal_service=self.google_calendar_service
        )
        insert_calendar_event_with_service = partial(
            insert_calendar_event, gcal_service=self.google_calendar_service
        )
        discord_notification_with_service = partial(
            discord_notification, notification_service=self.notification_service
        )

        return [
            discord_notification_with_service,
            list_calendar_events_with_service,
            insert_calendar_event_with_service,
            search_knowledge_base_with_service,
        ]

    @staticmethod
    def _load_system_prompt() -> str:
        with open("prompt.md", "r", encoding="utf-8") as f:
            return f.read()

    def _create_prompt_template(self) -> ChatPromptTemplate:
        system_prompt = self._load_system_prompt()
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    def create_agent(self) -> RunnableWithMessageHistory:
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        return RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: RedisChatMessageHistory(
                session_id, url=settings.REDIS_URL
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
        )
