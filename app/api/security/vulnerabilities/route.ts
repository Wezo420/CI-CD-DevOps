import { NextResponse } from "next/server"
import { getVulnerabilities } from "@/lib/db"

export async function GET() {
  try {
    const dbVulnerabilities = await getVulnerabilities(10)

    if (dbVulnerabilities && dbVulnerabilities.length > 0) {
      return NextResponse.json(dbVulnerabilities)
    }

    // Fallback to mock data
    const mockVulnerabilities = [
      {
        id: 1,
        title: "SQL Injection in User Authentication",
        description: "Parameterized queries not used in login endpoint",
        severity: "CRITICAL",
        file_path: "src/routes/auth.ts",
        line_number: 42,
        cvss_score: 9.8,
        cwe_id: "CWE-89",
      },
      {
        id: 2,
        title: "Missing CSRF Token Validation",
        description: "Form submissions lack CSRF token verification",
        severity: "HIGH",
        file_path: "src/middleware/forms.ts",
        line_number: 15,
        cvss_score: 8.1,
        cwe_id: "CWE-352",
      },
      {
        id: 3,
        title: "Insecure Deserialization",
        description: "Untrusted data directly deserialized",
        severity: "HIGH",
        file_path: "src/utils/parser.ts",
        line_number: 28,
        cvss_score: 8.4,
        cwe_id: "CWE-502",
      },
      {
        id: 4,
        title: "Weak Password Policy",
        description: "Passwords with low complexity accepted",
        severity: "MEDIUM",
        file_path: "src/services/validation.ts",
        line_number: 63,
        cvss_score: 5.3,
        cwe_id: "CWE-521",
      },
      {
        id: 5,
        title: "Missing Security Headers",
        description: "HSTS, CSP headers not configured",
        severity: "MEDIUM",
        file_path: "next.config.js",
        line_number: null,
        cvss_score: 6.2,
        cwe_id: "CWE-693",
      },
    ]

    return NextResponse.json(mockVulnerabilities)
  } catch (error) {
    console.error("API error:", error)
    return NextResponse.json({ error: "Failed to fetch vulnerabilities" }, { status: 500 })
  }
}
