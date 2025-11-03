"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle, AlertCircle, Clock } from "lucide-react"
import { useState, useEffect } from "react"

export default function ComplianceStatus() {
  const [compliance, setCompliance] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchCompliance = async () => {
      try {
        const response = await fetch("/api/security/compliance")
        const data = await response.json()
        setCompliance(data)
      } finally {
        setLoading(false)
      }
    }
    fetchCompliance()
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "PASS":
        return <CheckCircle className="h-5 w-5 text-green-400" />
      case "FAIL":
        return <AlertCircle className="h-5 w-5 text-red-400" />
      default:
        return <Clock className="h-5 w-5 text-yellow-400" />
    }
  }

  return (
    <Card className="bg-slate-900/50 border-slate-800">
      <CardHeader>
        <CardTitle className="text-white">Compliance Status</CardTitle>
        <CardDescription className="text-slate-400">Healthcare data protection standards</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-slate-400">Loading compliance data...</div>
        ) : (
          <div className="space-y-4">
            {compliance.map((item: any) => (
              <div key={item.id} className="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg">
                <div className="flex items-center gap-3">
                  {getStatusIcon(item.status)}
                  <div>
                    <p className="text-white text-sm font-medium">{item.framework}</p>
                    <p className="text-slate-400 text-xs">{item.check_name}</p>
                  </div>
                </div>
                <span
                  className={`text-xs font-medium px-2 py-1 rounded ${
                    item.status === "PASS"
                      ? "bg-green-500/20 text-green-300"
                      : item.status === "FAIL"
                        ? "bg-red-500/20 text-red-300"
                        : "bg-yellow-500/20 text-yellow-300"
                  }`}
                >
                  {item.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
