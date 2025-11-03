import { NextResponse } from "next/server"
import { getRecentScans } from "@/lib/db"

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = Number.parseInt(searchParams.get("limit") || "10")

    const dbScans = await getRecentScans(limit)

    if (dbScans && dbScans.length > 0) {
      return NextResponse.json(dbScans)
    }

    // Fallback to mock data
    const mockScans = [
      {
        id: 1,
        scan_type: "SAST",
        status: "COMPLETED",
        start_time: new Date(Date.now() - 3600000).toISOString(),
        end_time: new Date(Date.now() - 3500000).toISOString(),
        issues: 12,
      },
      {
        id: 2,
        scan_type: "Dependency",
        status: "COMPLETED",
        start_time: new Date(Date.now() - 7200000).toISOString(),
        end_time: new Date(Date.now() - 7100000).toISOString(),
        issues: 5,
      },
      {
        id: 3,
        scan_type: "Container",
        status: "COMPLETED",
        start_time: new Date(Date.now() - 10800000).toISOString(),
        end_time: new Date(Date.now() - 10700000).toISOString(),
        issues: 3,
      },
      {
        id: 4,
        scan_type: "Secrets",
        status: "IN_PROGRESS",
        start_time: new Date(Date.now() - 14400000).toISOString(),
        end_time: null,
        issues: 0,
      },
      {
        id: 5,
        scan_type: "DAST",
        status: "COMPLETED",
        start_time: new Date(Date.now() - 18000000).toISOString(),
        end_time: new Date(Date.now() - 17900000).toISOString(),
        issues: 8,
      },
    ]

    return NextResponse.json(mockScans.slice(0, limit))
  } catch (error) {
    console.error("API error:", error)
    return NextResponse.json({ error: "Failed to fetch scans" }, { status: 500 })
  }
}
