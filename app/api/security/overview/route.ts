import { NextResponse } from "next/server"

export async function GET() {
  try {
    // Mock data for security overview
    const overview = {
      critical: 2,
      high: 8,
      medium: 24,
      low: 45,
      sast: 15,
      dast: 4,
      deps: 18,
      secrets: 2,
      container: 6,
    }

    return NextResponse.json(overview)
  } catch (error) {
    console.error("API error:", error)
    return NextResponse.json({ error: "Failed to fetch overview" }, { status: 500 })
  }
}
