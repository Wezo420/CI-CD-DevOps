import { NextResponse } from "next/server"

export async function GET() {
  try {
    // Try to get real data from database
    // const dbCompliance = await getComplianceStatus()
    // if (dbCompliance && dbCompliance.length > 0) {
    //   return NextResponse.json(dbCompliance)
    // }

    // Fallback to mock data
    const compliance = [
      {
        id: 1,
        framework: "HIPAA",
        check_name: "Encryption at Rest",
        status: "PASS",
        last_check: new Date().toISOString(),
      },
      {
        id: 2,
        framework: "HIPAA",
        check_name: "Access Logging",
        status: "PASS",
        last_check: new Date().toISOString(),
      },
      {
        id: 3,
        framework: "SOC 2",
        check_name: "Intrusion Detection",
        status: "WARNING",
        last_check: new Date().toISOString(),
      },
      {
        id: 4,
        framework: "GDPR",
        check_name: "Data Retention Policy",
        status: "PASS",
        last_check: new Date().toISOString(),
      },
      {
        id: 5,
        framework: "GDPR",
        check_name: "User Consent Management",
        status: "FAIL",
        last_check: new Date().toISOString(),
      },
    ]

    return NextResponse.json(compliance)
  } catch (error) {
    console.error("API error:", error)
    return NextResponse.json({ error: "Failed to fetch compliance data" }, { status: 500 })
  }
}
