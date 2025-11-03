#!/usr/bin/env node

/**
 * Publish security scan results to the security dashboard
 * This script runs after security scans complete in GitHub Actions
 */

const fs = require("fs")
const path = require("path")

async function publishResults() {
  const apiKey = process.env.SECURITY_DASHBOARD_API_KEY
  const dashboardUrl = process.env.SECURITY_DASHBOARD_URL || "http://localhost:3000"

  if (!apiKey) {
    console.error("SECURITY_DASHBOARD_API_KEY not set")
    process.exit(1)
  }

  const scanResults = {
    scan_id: `github-${Date.now()}`,
    repository_name: process.env.GITHUB_REPOSITORY,
    branch_name: process.env.GITHUB_REF_NAME,
    commit_hash: process.env.GITHUB_SHA,
    scan_type: "SAST",
    status: "COMPLETED",
    vulnerabilities: [],
  }

  try {
    // Read scan result files
    const files = ["npm-audit.json", "snyk-results.json", "trivy-results.sarif"]

    for (const file of files) {
      if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, "utf-8")
        console.log(`Processing ${file}...`)
        // Parse and process results
      }
    }

    // Send to dashboard
    const response = await fetch(`${dashboardUrl}/api/security/webhook`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(scanResults),
    })

    if (!response.ok) {
      throw new Error(`Failed to publish results: ${response.statusText}`)
    }

    console.log("Security results published successfully")
  } catch (error) {
    console.error("Error publishing results:", error)
    process.exit(1)
  }
}

publishResults()
