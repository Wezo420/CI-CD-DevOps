// API route to store security scan results in the database
import { NextResponse } from "next/server"
import { neon } from "@neondatabase/serverless"

export async function POST(request: Request) {
  try {
    const body = await request.json()

    // Only allow requests from authorized sources (GitHub Actions, AWS CodePipeline)
    const authHeader = request.headers.get("authorization")
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    if (!process.env.DATABASE_URL) {
      return NextResponse.json({ error: "Database not configured" }, { status: 503 })
    }

    const sql = neon(process.env.DATABASE_URL)

    // Store the scan result
    const scanResult = await sql`
      INSERT INTO security_scans (
        scan_id,
        repository_name,
        branch_name,
        scan_type,
        scan_status,
        total_issues,
        critical_issues,
        high_issues,
        medium_issues,
        low_issues,
        scan_score,
        metadata,
        ci_provider
      ) VALUES (
        ${body.scan_id},
        ${body.repository_name || "medical-records-app"},
        ${body.branch_name || "main"},
        ${body.scan_type || "COMPREHENSIVE"},
        ${body.scan_status || "COMPLETED"},
        ${body.total_issues || 0},
        ${body.critical_issues || 0},
        ${body.high_issues || 0},
        ${body.medium_issues || 0},
        ${body.low_issues || 0},
        ${body.scan_score || 0},
        ${JSON.stringify(body.metadata || {})},
        ${body.ci_provider || "GITHUB_ACTIONS"}
      )
      RETURNING *
    `

    // Store individual vulnerabilities if provided
    if (body.vulnerabilities && Array.isArray(body.vulnerabilities)) {
      for (const vuln of body.vulnerabilities) {
        await sql`
          INSERT INTO vulnerabilities (
            scan_id,
            vulnerability_id,
            title,
            description,
            severity,
            file_path,
            line_number,
            cwe_id,
            cvss_score,
            status
          ) VALUES (
            ${body.scan_id},
            ${vuln.vulnerability_id || `vuln_${Date.now()}_${Math.random()}`},
            ${vuln.title},
            ${vuln.description || null},
            ${vuln.severity},
            ${vuln.file_path || null},
            ${vuln.line_number || null},
            ${vuln.cwe_id || null},
            ${vuln.cvss_score || null},
            'OPEN'
          )
        `
      }
    }

    // Update daily security metrics
    await sql`
      INSERT INTO security_metrics (
        metric_date,
        total_vulnerabilities,
        critical_count,
        high_count,
        medium_count,
        low_count,
        average_scan_score,
        scans_performed
      ) VALUES (
        CURRENT_DATE,
        ${body.total_issues || 0},
        ${body.critical_issues || 0},
        ${body.high_issues || 0},
        ${body.medium_issues || 0},
        ${body.low_issues || 0},
        ${body.scan_score || 0},
        1
      )
      ON CONFLICT (metric_date) DO UPDATE SET
        total_vulnerabilities = total_vulnerabilities + ${body.total_issues || 0},
        critical_count = critical_count + ${body.critical_issues || 0},
        high_count = high_count + ${body.high_issues || 0},
        medium_count = medium_count + ${body.medium_issues || 0},
        low_count = low_count + ${body.low_issues || 0},
        scans_performed = scans_performed + 1
    `

    return NextResponse.json({
      success: true,
      scan_id: scanResult[0].scan_id,
      message: "Scan results stored successfully",
    })
  } catch (error) {
    console.error("Error storing scan results:", error)
    return NextResponse.json({ error: "Failed to store scan results" }, { status: 500 })
  }
}
