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
                    Building digital experiences with modern technologies. Focused on creating elegant solutions to
                    complex problems.
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
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <ProjectCard
                  title="E-commerce Platform"
                  description="A full-stack e-commerce platform built with Next.js, Prisma, and Stripe integration."
                  image="/placeholder.svg?height=400&width=600"
                  link="https://github.com"
                  tags={["Next.js", "Prisma", "Stripe"]}
                />
                <ProjectCard
                  title="Task Management App"
                  description="A real-time task management application with team collaboration features."
                  image="/placeholder.svg?height=400&width=600"
                  link="https://github.com"
                  tags={["React", "Node.js", "Socket.io"]}
                />
                <ProjectCard
                  title="AI Chat Interface"
                  description="An AI-powered chat interface with natural language processing capabilities."
                  image="/placeholder.svg?height=400&width=600"
                  link="https://github.com"
                  tags={["OpenAI", "Next.js", "TailwindCSS"]}
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
