"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useEffect, useState } from "react"
import { Clock, CheckCircle, XCircle } from "lucide-react"

export default function RecentScans() {
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchScans = async () => {
      try {
        const response = await fetch("/api/security/scans?limit=5")
        const data = await response.json()
        setScans(data)
      } finally {
        setLoading(false)
      }
    }
    fetchScans()
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "COMPLETED":
        return <CheckCircle className="h-4 w-4 text-green-400" />
      case "FAILED":
        return <XCircle className="h-4 w-4 text-red-400" />
      default:
        return <Clock className="h-4 w-4 text-yellow-400" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "COMPLETED":
        return "bg-green-500/20 text-green-300"
      case "FAILED":
        return "bg-red-500/20 text-red-300"
      default:
        return "bg-yellow-500/20 text-yellow-300"
    }
  }

  return (
    <Card className="bg-slate-900/50 border-slate-800">
      <CardHeader>
        <CardTitle className="text-white">Recent Scans</CardTitle>
        <CardDescription className="text-slate-400">Last 5 security scans</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-slate-400">Loading scans...</div>
        ) : scans.length === 0 ? (
          <div className="text-slate-400 text-center py-8">No recent scans</div>
        ) : (
          <div className="space-y-2">
            {scans.map((scan: any) => (
              <div key={scan.id} className="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg">
                <div className="flex items-center gap-3">
                  {getStatusIcon(scan.status)}
                  <div>
                    <p className="text-white text-sm font-medium">{scan.scan_type}</p>
                    <p className="text-slate-500 text-xs">{new Date(scan.start_time).toLocaleString()}</p>
                  </div>
                </div>
                <Badge className={`${getStatusBadge(scan.status)} text-xs`}>{scan.status}</Badge>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
