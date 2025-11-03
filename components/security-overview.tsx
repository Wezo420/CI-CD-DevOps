"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { useState, useEffect } from "react"

export default function SecurityOverview() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/security/overview")
        const result = await response.json()
        setData(result)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const severityData = [
    { name: "Critical", value: data?.critical || 0, color: "#dc2626" },
    { name: "High", value: data?.high || 0, color: "#ea580c" },
    { name: "Medium", value: data?.medium || 0, color: "#eab308" },
    { name: "Low", value: data?.low || 0, color: "#3b82f6" },
  ]

  const scanTypeData = [
    { name: "SAST", value: data?.sast || 0 },
    { name: "DAST", value: data?.dast || 0 },
    { name: "Dependencies", value: data?.deps || 0 },
    { name: "Secrets", value: data?.secrets || 0 },
    { name: "Container", value: data?.container || 0 },
  ]

  if (loading) {
    return <div className="text-slate-300">Loading...</div>
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card className="bg-slate-900/50 border-slate-800">
        <CardHeader>
          <CardTitle className="text-white">Vulnerability Severity Distribution</CardTitle>
          <CardDescription className="text-slate-400">Current scan findings by severity</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={severityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {severityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="bg-slate-900/50 border-slate-800">
        <CardHeader>
          <CardTitle className="text-white">Scan Types Coverage</CardTitle>
          <CardDescription className="text-slate-400">Security scanning breakdown</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={scanTypeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: "#1e293b", border: "none" }} />
              <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
