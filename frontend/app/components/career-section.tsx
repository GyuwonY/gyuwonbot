import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Link } from "lucide-react"

const careerData = [
  {
    id: 1,
    company: "(주) 팹",
    period: "2024.11 - (재직 중)",
    description: "명품 C2C 거래 플랫폼 CHIC",
    logo: "/logo-pap.jpg?height=80&width=80",
    tags: ["Backend 개발"],
    projects: [
      {
        title: "명품 C2C 거래 플랫폼 개발",
        period: "",
        description: "",
      },
    ],
  },
  {
    id: 2,
    company: "(주) 아우토크립트",
    period: "",
    description: "",
    logo: "/logo-autocrypt.png?height=80&width=80",
    tags: ["Backend 개발"],
    projects: [
      {
        title: "",
        period: "",
        description: "",
      },
    ],
  },
]

export default function CareerSection() {
  return (
    <section className="py-12 md:py-24 lg:py-32">
      <div className="container px-4 md:px-6">
        <div className="flex items-center justify-center mb-12">
          <Link className="h-6 w-6 mr-3 text-muted-foreground" />
          <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">CAREER</h2>
        </div>

        <div className="space-y-12">
          {careerData.map((career) => (
            <div key={career.id} className="space-y-6">
              {/* 회사 정보 */}
              <Card className="p-6">
                <CardContent className="p-0">
                  <div className="flex items-start gap-6">
                    <div className="w-20 h-20 rounded-full overflow-hidden bg-muted flex-shrink-0">
                      <img
                        src={career.logo || "/placeholder.svg"}
                        alt={`${career.company} 로고`}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="flex-1 space-y-3">
                      <div>
                        <h3 className="text-xl font-semibold">{career.company}</h3>
                        <p className="text-sm text-muted-foreground">{career.period}</p>
                      </div>
                      <p className="text-sm text-muted-foreground leading-relaxed">"{career.description}"</p>
                      <div className="flex flex-wrap gap-2">
                        {career.tags.map((tag, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* 프로젝트 목록 */}
              <div className="space-y-4 ml-6">
                {career.projects.map((project, index) => (
                  <div key={index} className="border-l-2 border-muted pl-6 pb-6">
                    <div className="space-y-2">
                      <h4 className="font-medium text-lg">{project.title}</h4>
                      <p className="text-sm text-muted-foreground">{project.period}</p>
                      {project.description && (
                        <p className="text-sm text-muted-foreground leading-relaxed">{project.description}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}