from langchain.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import List

from cachetools import TTLCache
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import List

# 세션별 대화 기록을 저장할 인메모리 TTLCache
# maxsize: 최대 1000개의 세션을 저장
# ttl: 각 세션은 마지막 사용 후 10800초(3시간) 동안 유지됨
store = TTLCache(maxsize=50, ttl=10800)


class CustomChatMessageHistory(BaseChatMessageHistory):
    """
    ConversationBufferWindowMemory를 감싸서 RunnableWithMessageHistory와 호환되도록 만든 클래스
    """

    def __init__(self, session_id: str, k: int = 5):
        super().__init__()
        self._session_id = session_id
        # return_messages=True로 설정해야 AIMessage, HumanMessage 객체로 반환됨
        self._memory = ConversationBufferWindowMemory(k=k, return_messages=True)

    @property
    def messages(self) -> List[BaseMessage]:
        """memory 객체에서 메시지를 직접 가져옵니다."""
        return self._memory.chat_memory.messages

    @messages.setter
    def messages(self, messages: List[BaseMessage]) -> None:
        """memory 객체에 메시지를 설정합니다."""
        self._memory.chat_memory.messages = messages

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """memory 객체에 메시지를 추가합니다."""
        for message in messages:
            self._memory.chat_memory.add_message(message)

    def clear(self) -> None:
        """memory 객체의 기록을 삭제합니다."""
        self._memory.clear()


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """세션 ID에 해당하는 대화 기록 인스턴스를 가져오거나 새로 생성합니다."""
    if session_id not in store:
        store[session_id] = CustomChatMessageHistory(session_id=session_id, k=5)
    return store[session_id]
