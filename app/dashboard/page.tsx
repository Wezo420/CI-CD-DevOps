"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import SecurityOverview from "@/components/security-overview"
import VulnerabilityList from "@/components/vulnerability-list"
import ComplianceStatus from "@/components/compliance-status"
import RecentScans from "@/components/recent-scans"
import SecurityTrends from "@/components/security-trends"
import { AlertTriangle } from "lucide-react"

export default function SecurityDashboard() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch("/api/security/metrics")
        if (!response.ok) throw new Error("Failed to fetch metrics")
        const data = await response.json()
        setMetrics(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error")
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()
    const interval = setInterval(fetchMetrics, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  if (error) {
    return (
      <Alert className="mt-4 bg-red-50 border-red-200">
        <AlertTriangle className="h-4 w-4 text-red-600" />
        <AlertDescription className="text-red-800">Error loading security metrics: {error}</AlertDescription>
      </Alert>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl md:text-4xl font-bold text-white">Security Dashboard</h1>
          <p className="text-slate-400">Real-time DevSecOps monitoring and compliance tracking</p>
        </div>

        {/* Critical Alerts */}
        {metrics?.critical_issues > 0 && (
          <Alert className="bg-red-950 border-red-900">
            <AlertTriangle className="h-4 w-4 text-red-500" />
            <AlertDescription className="text-red-200">
              {metrics.critical_issues} critical vulnerabilities require immediate attention
            </AlertDescription>
          </Alert>
        )}

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-300">Security Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-400">{loading ? "-" : metrics?.security_score || "0"}%</div>
              <p className="text-xs text-slate-500 mt-1">Latest scan</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-300">Critical Issues</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-400">{loading ? "-" : metrics?.critical_issues || "0"}</div>
              <p className="text-xs text-slate-500 mt-1">Requires attention</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-300">Scans (24h)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-400">{loading ? "-" : metrics?.scans_24h || "0"}</div>
              <p className="text-xs text-slate-500 mt-1">Completed</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-300">Compliance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-amber-400">
                {loading ? "-" : metrics?.compliance_score || "0"}%
              </div>
              <p className="text-xs text-slate-500 mt-1">HIPAA/SOC2</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            <SecurityOverview />
            <VulnerabilityList />
            <SecurityTrends />
          </div>

          {/* Right Column */}
          <div className="space-y-8">
            <ComplianceStatus />
            <RecentScans />
          </div>
        </div>
      </div>
    </main>
  )
}
