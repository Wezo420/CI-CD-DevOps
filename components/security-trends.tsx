"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import { useEffect, useState } from "react"

export default function SecurityTrends() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const response = await fetch("/api/security/trends")
        const result = await response.json()
        setData(result)
      } finally {
        setLoading(false)
      }
    }
    fetchTrends()
  }, [])

  if (loading) {
    return <div className="text-slate-300">Loading trends...</div>
  }

  return (
    <Card className="bg-slate-900/50 border-slate-800">
      <CardHeader>
        <CardTitle className="text-white">Security Score Trends</CardTitle>
        <CardDescription className="text-slate-400">30-day security metrics</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="date" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip contentStyle={{ backgroundColor: "#1e293b", border: "none", borderRadius: "8px" }} />
            <Legend />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#3b82f6"
              strokeWidth={2}
              name="Security Score"
              dot={{ fill: "#3b82f6", r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="vulnerabilities"
              stroke="#ef4444"
              strokeWidth={2}
              name="Vulnerabilities"
              dot={{ fill: "#ef4444", r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
