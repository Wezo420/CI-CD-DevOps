// Security scan results processor
// Processes, normalizes, and stores security scan results in the database

interface ScanResult {
  scan_type: string
  severity: string
  vulnerability_id?: string
  title: string
  description?: string
  file_path?: string
  line_number?: number
  cwe_id?: string
  cvss_score?: number
  remediation?: string
}

interface ProcessedScan {
  scan_id: string
  repository_name: string
  branch_name: string
  scan_type: string
  scan_status: string
  total_issues: number
  critical_issues: number
  high_issues: number
  medium_issues: number
  low_issues: number
  scan_score: number
  metadata: Record<string, any>
}

export async function processScanResults(results: ScanResult[]): Promise<ProcessedScan> {
  let totalIssues = 0
  let criticalCount = 0
  let highCount = 0
  let mediumCount = 0
  let lowCount = 0

  for (const result of results) {
    totalIssues++
    switch (result.severity.toUpperCase()) {
      case "CRITICAL":
        criticalCount++
        break
      case "HIGH":
        highCount++
        break
      case "MEDIUM":
        mediumCount++
        break
      case "LOW":
      case "INFO":
        lowCount++
        break
    }
  }

  const scanScore = Math.max(0, 100 - (criticalCount * 10 + highCount * 5 + mediumCount * 2))

  const processedScan: ProcessedScan = {
    scan_id: `scan_${Date.now()}`,
    repository_name: process.env.GITHUB_REPOSITORY || "medical-records-app",
    branch_name: process.env.GITHUB_REF_NAME || "main",
    scan_type: "COMPREHENSIVE",
    scan_status: "COMPLETED",
    total_issues: totalIssues,
    critical_issues: criticalCount,
    high_issues: highCount,
    medium_issues: mediumCount,
    low_issues: lowCount,
    scan_score: scanScore,
    metadata: {
      timestamp: new Date().toISOString(),
      ci_provider: "GITHUB_ACTIONS",
      commit_sha: process.env.GITHUB_SHA,
      run_id: process.env.GITHUB_RUN_ID,
    },
  }

  return processedScan
}

export async function generateComplianceReport(scanResults: ProcessedScan) {
  const report = {
    timestamp: new Date().toISOString(),
    scan_results: scanResults,
    compliance_checks: [
      {
        framework: "HIPAA",
        status: scanResults.critical_issues === 0 ? "PASS" : "FAIL",
        details: "Medical Records data protection compliance",
      },
      {
        framework: "SOC2",
        status: scanResults.high_issues === 0 ? "PASS" : "WARNING",
        details: "Security and operational compliance",
      },
      {
        framework: "GDPR",
        status: scanResults.critical_issues === 0 && scanResults.high_issues < 5 ? "PASS" : "WARNING",
        details: "Data protection regulations compliance",
      },
    ],
    recommendations: [
      ...(scanResults.critical_issues > 0 ? ["Address all critical vulnerabilities immediately"] : []),
      ...(scanResults.high_issues > 5 ? ["Review and remediate high-severity findings"] : []),
      "Enable runtime security monitoring",
      "Implement automated remediation workflows",
    ],
  }

  return report
}

export function formatScanResultsForDashboard(processedScan: ProcessedScan) {
  return {
    scan_id: processedScan.scan_id,
    security_score: processedScan.scan_score,
    critical_issues: processedScan.critical_issues,
    high_issues: processedScan.high_issues,
    medium_issues: processedScan.medium_issues,
    low_issues: processedScan.low_issues,
    status: processedScan.scan_status,
    timestamp: processedScan.metadata.timestamp,
    trend: processedScan.scan_score > 85 ? "improving" : "needs attention",
  }
}
