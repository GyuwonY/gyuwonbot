# GyuwonBot: Gemini API & RAG 기반 AI 에이전트 포트폴리오

## 📖 소개 (Introduction)

**GyuwonBot**은 단순한 챗봇을 넘어 **Gemini API**를 핵심 엔진으로 사용하는 **자율적인 AI 에이전트**입니다. 기술 스택과 경험에 대한 정보를 효과적으로 전달하고 면접 일정 조율과 같은 실질적인 상호작용까지 수행할 수 있도록 설계되었습니다. 

에이전트는 사용자의 요청을 이해하고 스스로 판단하여 **RAG(검색 증강 생성)**, **Google Calendar 연동** 등 사전에 정의된 여러 도구들을 자율적으로 사용합니다. 이를 통해 제 자신을 소개하는 포트폴리오를 만들고자 하였습니다.

**라이브 데모:** [https://gyuwonbot.vercel.app/](https://gyuwonbot.vercel.app/)

---

## ✨ 주요 기능 (Key Features)

### 1. RAG (Retrieval-Augmented Generation) 기반의 정밀한 정보 제공

*   단순히 학습된 정보에만 의존하지 않고, **pgvector**를 활용해 벡터화된 이력서 및 프로젝트, TMI에 대한 예상 문답을 데이터베이스에서 참조합니다.
*   이를 통해 질문에 대해 항상 일관성 있고 사실에 기반한 답변을 생성합니다.

### 2. Google Calendar API 연동을 통한 자율적인 일정 관리

*   Gemini 에이전트가 **Google Calendar Tool**을 사용하여 구글 캘린더를 직접 확인합니다.
*   사용자가 면접 가능 시간을 문의하면 실시간으로 가능한 시간을 제안하고 대화 내용에 기반하여 **새로운 면접 일정을 등록**하는 등 능동적인 상호작용을 수행합니다.

### 3. Discord Webhook을 활용한 실시간 알림 시스템

*   면접 제안과 같은 중요한 이벤트가 발생했을 때, 에이전트는 **Notification Tool**을 통해 지정된 Discord 채널로 즉시 알림을 보냅니다.
*   이를 통해 특정한 상황이 발생 했음을 실시간으로 알 수 있습니다.

---

## 🤖 Agent의 작동 원리 (How the Agent Works)

GyuwonBot의 핵심은 **LangChain** 프레임워크를 통해 구현된 자율 에이전트에 있습니다. 에이전트는 **Gemini의 Function Calling** 기능을 활용하여 다음과 같은 순서로 사용자의 요청을 처리합니다.

1.  **요청 분석 (Request Analysis):** 사용자의 메시지를 받으면, 에이전트는 대화의 맥락과 사전 정의된 프롬프트를 기반으로 요청의 의도를 파악합니다.
2.  **도구 선택 (Tool Selection):** 요청을 해결하는 데 가장 적합한 도구가 있는지 판단합니다. 예를 들어 "면접 가능한 시간 알려줘" 라는 요청에는 `google_calendar_tool`, "프로젝트 경험에 대해 알려줘" 라는 요청에는 `knowledge_base_tool`을 선택합니다.
3.  **Function Calling 실행:** Gemini 모델이 선택된 도구(함수)에 필요한 인자(Argument)를 대화 내용에서 추출하여 함수를 호출합니다.
4.  **결과 통합 및 답변 생성 (Response Generation):** 도구 실행 결과를 다시 LLM에 전달하여, 최종적으로 사용자가 이해하기 쉬운 자연스러운 문장으로 답변을 생성합니다.

이 모든 과정은 에이전트가 스스로 판단하여 진행하며, 이를 통해 정적인 정보 제공을 넘어 동적인 상호작용을 구현했습니다.

---

## 🛠️ 기술 스택 (Tech Stack)

| 구분 | 기술 |
| :--- | :--- |
| **Backend** | Python 3.13, FastAPI, LangChain, Google Gemini 2.5 flash, PostgreSQL with pgvector, GCP Cloud Run |
| **Frontend** | Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, Vercel |
| **DevOps** | Docker, GitHub Actions |

---

## 🏛️ 아키텍처 (Architecture)

### 클린 아키텍처 (Clean Architecture)

백엔드 시스템은 유지보수성과 확장성을 극대화하기 위해 **클린 아키텍처**를 적용했습니다. 각 계층은 명확한 책임 분리 원칙을 따르며, 이를 통해 비즈니스 로직의 독립성과 시스템의 유연성을 확보했습니다.

*   **Presentation (API Layer):** FastAPI를 사용하여 외부 요청을 처리하는 API 엔드포인트입니다.
*   **Application (Service Layer):** `AgentService`를 포함하여, 에이전트의 두뇌 역할을 하는 핵심 비즈니스 로직을 담당합니다.
*   **Domain (Core Layer):** 외부 의존성이 없는 순수한 비즈니스 규칙과 데이터 모델을 정의합니다.
*   **Infrastructure (External Layer):** 데이터베이스, 외부 API 연동 등 기술적인 구현을 담당합니다.

### 비동기(Async) 처리 기반의 고성능 설계

본 백엔드 시스템은 **FastAPI**의 핵심 기능인 **비동기(Asynchronous)** 처리를 적극적으로 활용하여 설계되었습니다.

*   API 엔드포인트부터 데이터베이스 접근(psycopg 3), 외부 API(Gemini, Google Calendar) 호출에 이르기까지 모든 I/O 작업을 **`async/await`** 구문을 통해 **Non-blocking** 방식으로 처리합니다.
*   이를 통해 단일 프로세스 내에서도 높은 동시성(Concurrency)을 확보하여, 다수의 사용자 요청을 지연 없이 효율적으로 처리할 수 있습니다. 이는 실시간 대화형 서비스에서 뛰어난 사용자 경험을 제공하는 핵심 요소입니다.
