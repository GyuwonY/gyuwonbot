"use client"

import type React from "react"

import { Button } from "@/components/ui/button"
import { CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Loader2, Send } from "lucide-react"
import { useState } from "react"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  content: string
  sender: "user" | "bot"
  timestamp: Date
}

export default function ChatSidebar() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: "안녕하세요! 궁금한 것이 있으시면 언제든 물어보세요.",
      sender: "bot",
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsLoading(true)

    // 봇 응답 시뮬레이션
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "메시지를 받았습니다. 곧 답변드리겠습니다!",
        sender: "bot",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, botMessage])
      setIsLoading(false)
    }, 2000) // 2초 지연으로 로딩 상태 확인

    /*
    // 실제 봇 API 호출
    const fetchBotResponse = async () => {
      try {
        const response = await fetch('YOUR_BOT_API_URL', { // <--- 여기에 실제 API URL을 입력하세요.
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: inputValue }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: data.reply, // API 응답 형식에 따라 'data.reply' 또는 다른 키를 사용해야 할 수 있습니다.
          sender: "bot",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        console.error('Error fetching bot response:', error);
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: "죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다.",
          sender: "bot",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBotResponse();
    */
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSendMessage()
    }
  }

  return (
    <div className="sticky top-0 h-screen w-150 flex-shrink-0 flex flex-col border-l bg-background">
      <CardHeader className="border-b h-14 flex items-center">
        <CardTitle className="text-lg font-semibold pl-4">채팅</CardTitle>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[90%] rounded-lg px-3 py-2 text-sm ${
                message.sender === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </CardContent>

      <CardFooter className="p-4 border-t">
        <div className="flex w-full space-x-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="메시지를 입력하세요..."
            className={cn("flex-1", { "bg-muted/50": isLoading })}
            disabled={isLoading}
          />
          <Button size="icon" onClick={handleSendMessage} disabled={isLoading}>
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
            <span className="sr-only">메시지 보내기</span>
          </Button>
        </div>
      </CardFooter>
    </div>
  )
}
