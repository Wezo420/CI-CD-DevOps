import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { InfoIcon } from "lucide-react"

export default function Documentation() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4 md:p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-white">DevSecOps Setup Guide</h1>
          <p className="text-slate-400">Integration instructions for GitHub Actions and AWS CI/CD pipelines</p>
        </div>

        <Alert className="bg-blue-950 border-blue-900">
          <InfoIcon className="h-4 w-4 text-blue-400" />
          <AlertDescription className="text-blue-200">
            Complete medical records application security with automated scanning and compliance monitoring
          </AlertDescription>
        </Alert>

        <div className="space-y-6">
          {/* GitHub Actions Setup */}
          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader>
              <CardTitle className="text-white">GitHub Actions CI/CD Setup</CardTitle>
              <CardDescription className="text-slate-400">
                Integrate DevSecOps scanning in your pipeline
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="text-white font-medium mb-2">Step 1: Create Workflow File</h3>
                <p className="text-slate-300 text-sm mb-2">
                  Create `.github/workflows/devsecops.yml` in your repository
                </p>
                <pre className="bg-slate-950 p-4 rounded text-xs text-green-400 overflow-x-auto">
                  {`name: DevSecOps Scanning
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run SAST Analysis
        uses: github/super-linter@v4
        env:
          DEFAULT_BRANCH: main
      
      - name: Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'medical-records-app'
          path: '.'
      
      - name: Secrets Scanning
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
      
      - name: Container Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'`}
                </pre>
              </div>

              <div>
                <h3 className="text-white font-medium mb-2">Step 2: Environment Variables</h3>
                <p className="text-slate-300 text-sm mb-2">Add these secrets to your GitHub repository settings:</p>
                <ul className="text-slate-300 text-sm space-y-1 ml-4">
                  <li>• `SECURITY_DASHBOARD_API_KEY` - API key for dashboard</li>
                  <li>• `AWS_ACCESS_KEY_ID` - AWS credentials</li>
                  <li>• `AWS_SECRET_ACCESS_KEY` - AWS credentials</li>
                  <li>• `SONARCLOUD_TOKEN` - SonarCloud token</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* AWS CodePipeline Setup */}
          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader>
              <CardTitle className="text-white">AWS CI/CD Pipeline Setup</CardTitle>
              <CardDescription className="text-slate-400">
                Configure CodePipeline with security scanning
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="text-white font-medium mb-2">Step 1: Create buildspec.yml</h3>
                <pre className="bg-slate-950 p-4 rounded text-xs text-green-400 overflow-x-auto">
                  {`version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 18
  pre_build:
    commands:
      - echo "Running security scans..."
      - npm install
      - npx snyk auth $SNYK_TOKEN
      - npx snyk test
  build:
    commands:
      - echo "Building application..."
      - npm run build
      - echo "Scanning built artifacts..."
      - trivy image --severity HIGH,CRITICAL $ECR_IMAGE

artifacts:
  files:
    - '**/*'`}
                </pre>
              </div>

              <div>
                <h3 className="text-white font-medium mb-2">Step 2: CodePipeline Stages</h3>
                <ul className="text-slate-300 text-sm space-y-2">
                  <li>
                    • <strong>Source:</strong> GitHub repository
                  </li>
                  <li>
                    • <strong>Security Scan:</strong> CodeBuild with SAST/DAST
                  </li>
                  <li>
                    • <strong>Build:</strong> Compile and unit tests
                  </li>
                  <li>
                    • <strong>Container Scan:</strong> Trivy for vulnerabilities
                  </li>
                  <li>
                    • <strong>Deploy:</strong> ECS or EKS deployment
                  </li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Dashboard API Integration */}
          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader>
              <CardTitle className="text-white">Dashboard API Integration</CardTitle>
              <CardDescription className="text-slate-400">Send scan results to the security dashboard</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="text-white font-medium mb-2">Scan Result Webhook</h3>
                <p className="text-slate-300 text-sm mb-2">POST scan results to trigger dashboard updates:</p>
                <pre className="bg-slate-950 p-4 rounded text-xs text-green-400 overflow-x-auto">
                  {`POST /api/security/webhook

{
  "scan_id": "scan-123",
  "repository": "medical-records-app",
  "branch": "main",
  "scan_type": "SAST",
  "status": "COMPLETED",
  "vulnerabilities": [
    {
      "title": "SQL Injection",
      "severity": "CRITICAL",
      "file": "src/api/users.ts",
      "line": 42
    }
  ]
}`}
                </pre>
              </div>
            </CardContent>
          </Card>

          {/* Compliance Requirements */}
          <Card className="bg-slate-900/50 border-slate-800">
            <CardHeader>
              <CardTitle className="text-white">Compliance Framework</CardTitle>
              <CardDescription className="text-slate-400">Medical records security requirements</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-slate-300 text-sm space-y-3">
                <li className="flex gap-3">
                  <span className="text-blue-400">✓</span>
                  <span>
                    <strong>HIPAA:</strong> Encryption at rest/transit, access logging, audit trails
                  </span>
                </li>
                <li className="flex gap-3">
                  <span className="text-blue-400">✓</span>
                  <span>
                    <strong>SOC 2:</strong> Security, availability, confidentiality controls
                  </span>
                </li>
                <li className="flex gap-3">
                  <span className="text-blue-400">✓</span>
                  <span>
                    <strong>GDPR:</strong> Data privacy, user consent, breach notification
                  </span>
                </li>
                <li className="flex gap-3">
                  <span className="text-blue-400">✓</span>
                  <span>
                    <strong>PCI DSS:</strong> Payment data protection (if applicable)
                  </span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  )
}
