import { Button } from "@/components/ui/button"
import { Github, Linkedin, Mail, Twitter } from "lucide-react"
import Link from "next/link"
import ChatSidebar from "./components/chat-sidebar"
import ContactForm from "./components/contact-form"
import ProjectCard from "./components/project-card"
import TechStack from "./components/tech-stack"
import CareerSection from "./components/career-section"

export default function Page() {
  return (
    <div className="flex min-h-screen bg-background">
      {/* 메인 컨텐츠 영역 */}
      <div className="flex-1 flex flex-col max-w-7xl mx-auto w-full">
        {/* 헤더 */}
        <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container flex h-14 items-center px-4 md:px-8 max-w-7xl mx-auto">
            <div className="mr-4 hidden md:flex">
              <Link className="mr-6 flex items-center space-x-2" href="/">
                <span className="hidden font-bold sm:inline-block">GyuwonY's portfolio</span>
              </Link>
              <nav className="flex items-center space-x-6 text-sm font-medium">
                <Link href="#about" className="transition-colors hover:text-foreground/80">
                  About
                </Link>
                <Link href="#projects" className="transition-colors hover:text-foreground/80">
                  Projects
                </Link>
                <Link href="#contact" className="transition-colors hover:text-foreground/80">
                  Contact
                </Link>
              </nav>
            </div>
            <div className="ml-auto flex items-center space-x-4">
              <Button variant="outline">Resume</Button>
            </div>
          </div>
        </header>

        {/* 메인 */}
        <main className="flex-1 container px-4 md:px-8 max-w-7xl mx-auto">
          <section id="about" className="py-12 md:py-24 lg:py-32">
            <div className="container px-4 md:px-6 max-w-6xl mx-auto">
              <div className="flex flex-col items-center justify-center space-y-4 text-center">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                    Backend Developer
                  </h1>
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                    유규원
                  </h1>
                  <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                    기술의 경계를 넘나들며 비즈니스 문제를 해결하고 성장을 멈추지 않습니다.
                  </p>
                </div>
                <div className="space-x-4">
                  <Link href="https://github.com/GyuwonY" target="_blank">
                    <Button variant="outline" size="icon">
                      <Github className="h-4 w-4" />
                      <span className="sr-only">GitHub</span>
                    </Button>
                  </Link>
                  <Link href="mailto:ykw3480@gmail.com">
                    <Button variant="outline" size="icon">
                      <Mail className="h-4 w-4" />
                      <span className="sr-only">Email</span>
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </section>

          <section className="py-12 md:py-24 lg:py-32">
            <div className="container px-4 md:px-6 max-w-6xl mx-auto">
              <h2 className="text-2xl font-bold tracking-tighter sm:text-3xl md:text-4xl mb-12 text-center">
                Tech Stack
              </h2>
              <TechStack />
            </div>
          </section>

          <section id="projects" className="py-12 md:py-24 lg:py-32">
            <div className="container px-4 md:px-6 max-w-6xl mx-auto">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center">
                Projects
              </h2>
              <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
                <ProjectCard
                  title="lio"
                  description="인터랙티브 포트폴리오 페이지 제공 서비스"
                  content={`- Gyuwonbot 개발 후 서비스 수요를 확인하여 챗봇 포트폴리오 제공 서비스 개발
- I/O Bound 효율을 위한 비동기 기반 FastAPI
- PostgreSQL Vector 활용 RAG
    - 사용자별로 수백 개 내외의 Chunk 내에서 유사도 검색을 수행하기 때문에 개발 편의와 비용을 고려하여 선택
    - PDF/사용자 입력 기반 이력서, 개인 정보, 예상 질답 등 embedding
    - PDF 텍스트 내용 추출, 구조화 (LLM)
    - 예상 질답 생성 (LLM) 및 저장
- LangGraph 사용 Work flow 구체화
    - Redis 내 Window 크기에 따른 채팅 요약 조회 (TTL로 메모리 사용량 관리)
    - 지칭 대명사/복합 질의에서 단일 Query list 추출 (LLM)
    - Query embedding 및 검색
        - 계층적 검색으로 검색 범위 제한하여 정확도 향상
    - 챗봇 답변 생성 (LLM)
    - 채팅 내역 요약 (LLM) 및 저장}`}
                  image="/lio.png?height=400&width=600"
                  link="https://github.com/GyuwonY/gyuwonbot"
                  tags={["FastAPI", "PostgreSQL", "PGVector", "Redis", "LangChain", "LangGraph", "LangSmith", "GeminiAPI", "GCP"]}
                />
                <ProjectCard
                  title="암호화폐 가격 변동률 예측 모델"
                  description="LLM 에이get 기반 인터랙티브 포트폴리오"
                  content={`- 딥러닝 학습, 예측 과정 이해를 위한 모델 학습 프로젝트
    - 딥러닝 기반 시계열 데이터 예측 아키텍처 PatchTST, PatchTSMixer 학습
    - 데이터 전처리, 하이퍼 파라미터 튜닝, 학습, 예측
        - 다양한 기술 분석 지표 feature 추가
        - OHLCV는 표준 편차가 심하기 때문에 변동률로 변환 후 정규화`}
                  image="/placeholder.svg?height=400&width=600"
                  link="https://github.com/GyuwonY/deeplearning-pj-coin"
                  tags={["FastAPI", "PostgreSQL", "Langchain", "GeminiAPI", "GCP"]}
                />
                <ProjectCard
                  title="Gyuwon-Bot"
                  description="LLM 에이전트 기반 인터랙티브 포트폴리오"
                  content={`- Langchain Agent를 활용한 챗봇 포트폴리오 개발 (gemini-2.5-flash 모델)
    - PostgreSQL Vector 활용 RAG
        - 이력서,  개인 정보, 예상 질답 등 챗봇이 질문에 답변해야 할 내용 embedding (gemini-embedding-001 모델)
        - 전문을 임베딩할 경우, 특정 단어의 반복 빈도나 문장의 길이에 따라 유사도 검색 결과가 왜곡, Vector의 명확한 의미를 위해 발생할 수 있는 예상 질문과 핵심 키워드를  추출 후 embedding
    - Discord webhook 사용 특정 상황 알림 툴
    - Google Calendar API 사용 일정 조회 및 생성 툴`}
                  image="/GyuwonBot.png?height=400&width=600"
                  link="https://github.com/GyuwonY/gyuwonbot"
                  tags={["FastAPI", "Next.js", "Langchain", "LLM", "PostgreSQL Vector", "GCP"]}
                />
                <ProjectCard
                  title="선착순 구매 동시성 관리 서비스"
                  description="MSA에 따른 선착순 구매 상황 동시성 관리 서비스"
                  content={`- **MSA에 따른** 서비스 개발
    - 유저, 상품, 주문, 결제, 재고 관리, Gateway, Discovery 서비스 서버 구축 및 Discovery Server, Feign Client 사용한 서비스간 통신 구현
    - **Resilience4j** CircuitBreaker, Retry 기능을 이용하여 서비스 간 장애 허용, 탄력적인 회복 환경 구축
    - 로컬 환경 내 통합 테스트를 위한 Dockerizing
- Redis를 통해 재고 관리, 결제 페이지 진입 시 재고 선점(차감) 이후 정책에 따른 재고 증가 및 차감 구현
    - 재고 선점 후 미결제 대응을 위해 Redis TTL Event 수신 후 Kafka Publish, 재고 관리 서비스의 Consume을 통해 재고 증가 반영`}
                  image="/MSA-PJ.png?height=400&width=600"
                  link="https://github.com/GyuwonY/reboot-project"
                  tags={["SpringBoot", "SpringCloud", "MySQL", "Redis", "Docker"]}
                />
                <ProjectCard
                  title="WYA"
                  description="위치 기반 약속 관리 서비스"
                  content={`- Firebase Realtime DB를 통해 약속 별 채팅, 현재 위치 공유 기능 구현
- 약속 장소와 사용자의 거리 1km(GPS가 부정확한 상황 고려) 이상인 경우 지각 판별 로직 개발
- FCM 통한 약속 리마인드 알림 기능 구현`}
                  image="/placeholder.svg?height=400&width=600"
                  link="https://github.com/CreativeApes/WYA_SERVER"
                  tags={["NestJS", "MySQL", "Firebase", "AWS"]}
                />
                <ProjectCard
                  title="corinne"
                  description="Gamification 코인 모의투자 서비스"
                  content={`- 업비트 WebSocket API 연동 후 가격 변동 데이터 표출 및 1분봉 데이터 생성
- Redis Pub/Sub 활용 시세, 채팅, 알림 전송 구현
- JPA Lock 사용으로 거래 시 동시 요청 차단
- 레버리지 매수 시 청산 기능 구현
- 무중단 배포 환경 구축`}
                  image="/corinne.png?height=400&width=600"
                  link="https://github.com/GyuwonY/corinne_BE"
                  tags={["SpringBoot", "Websocket", "MySQL", "Redis", "AWS"]}
                />
              </div>
            </div>
          </section>

          <section id="career">
            <CareerSection />
          </section>

          <section id="contact" className="py-12 md:py-24 lg:py-32">
            <div className="container px-4 md:px-6 max-w-6xl mx-auto">
              <div className="mx-auto max-w-2xl">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-12 text-center">
                  Get in Touch
                </h2>
                <ContactForm />
              </div>
            </div>
          </section>
        </main>
      </div>

      {/* 채팅 사이드바 */}
      <ChatSidebar />
    </div>
  )
}
