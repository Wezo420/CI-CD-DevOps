// Webhook handler for CI/CD pipeline scan result events
// This handles webhooks from GitHub Actions and AWS CodePipeline

export async function handleGitHubActionsWebhook(payload: any) {
  const scanResults = {
    scan_id: `scan_${payload.workflow_run.id}`,
    repository_name: payload.repository.name,
    branch_name: payload.workflow_run.head_branch,
    scan_type: "GITHUB_ACTIONS_SECURITY",
    scan_status: payload.workflow_run.conclusion === "success" ? "COMPLETED" : "FAILED",
    total_issues: payload.check_suite?.pull_requests?.length || 0,
    critical_issues: 0,
    high_issues: 0,
    medium_issues: 0,
    low_issues: 0,
    scan_score: 85,
    ci_provider: "GITHUB_ACTIONS",
    metadata: {
      workflow_id: payload.workflow_run.id,
      head_sha: payload.workflow_run.head_sha,
      run_number: payload.workflow_run.run_number,
      created_at: payload.workflow_run.created_at,
      updated_at: payload.workflow_run.updated_at,
    },
  }

  // Send to dashboard storage API
  const response = await fetch("/api/security/store-scan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.WEBHOOK_SECRET}`,
    },
    body: JSON.stringify(scanResults),
  })

  return response.json()
}

export async function handleAWSCodePipelineWebhook(payload: any) {
  const scanResults = {
    scan_id: `scan_${payload.detail.pipeline}_${Date.now()}`,
    repository_name: "medical-records-app",
    branch_name: "main",
    scan_type: "AWS_CODEPIPELINE_SECURITY",
    scan_status: payload.detail.state === "SUCCEEDED" ? "COMPLETED" : "FAILED",
    total_issues: 0,
    critical_issues: 0,
    high_issues: 0,
    medium_issues: 0,
    low_issues: 0,
    scan_score: 85,
    ci_provider: "AWS_CODEPIPELINE",
    metadata: {
      pipeline: payload.detail.pipeline,
      execution_id: payload.detail["execution-id"],
      state: payload.detail.state,
      timestamp: new Date().toISOString(),
    },
  }

  // Send to dashboard storage API
  const response = await fetch("/api/security/store-scan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.WEBHOOK_SECRET}`,
    },
    body: JSON.stringify(scanResults),
  })

  return response.json()
}
