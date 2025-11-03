/**
 * Security Dashboard API Client
 * Handles communication with security scanning endpoints
 */

export interface ScanResult {
  scan_id: string
  repository_name: string
  branch_name: string
  scan_type: string
  status: "PENDING" | "IN_PROGRESS" | "COMPLETED" | "FAILED"
  vulnerabilities: Vulnerability[]
  scan_score: number
}

export interface Vulnerability {
  id: string
  title: string
  description: string
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO"
  file_path: string
  line_number: number
  cvss_score: number
  cwe_id: string
}

class SecurityClient {
  private baseUrl: string
  private apiKey: string

  constructor(baseUrl = "/api/security", apiKey = "") {
    this.baseUrl = baseUrl
    this.apiKey = apiKey
  }

  private async request(endpoint: string, options?: RequestInit) {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options?.headers,
    }

    if (this.apiKey) {
      headers["Authorization"] = `Bearer ${this.apiKey}`
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      throw new Error(`Security API error: ${response.statusText}`)
    }

    return response.json()
  }

  async getMetrics() {
    return this.request("/metrics")
  }

  async getVulnerabilities() {
    return this.request("/vulnerabilities")
  }

  async getCompliance() {
    return this.request("/compliance")
  }

  async getScans(limit = 10) {
    return this.request(`/scans?limit=${limit}`)
  }

  async getTrends() {
    return this.request("/trends")
  }

  async publishScanResults(results: ScanResult) {
    return this.request("/webhook", {
      method: "POST",
      body: JSON.stringify(results),
    })
  }
}

export const securityClient = new SecurityClient()
