import { NextResponse } from "next/server"

export async function GET() {
  try {
    // Generate 30 days of trend data
    const trends = []
    const now = Date.now()

    for (let i = 29; i >= 0; i--) {
      const date = new Date(now - i * 24 * 60 * 60 * 1000)
      const variance = Math.random() * 10 - 5

      trends.push({
        date: date.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
        score: Math.max(75, Math.min(95, 85 + variance)),
        vulnerabilities: Math.max(5, Math.floor(30 + Math.random() * 20 - 10)),
      })
    }

    return NextResponse.json(trends)
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch trends" }, { status: 500 })
  }
}
