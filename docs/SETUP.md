# Medical Records Security Dashboard - Setup Guide

## Overview

This is a comprehensive DevSecOps security dashboard for medical records applications with integrated scanning, compliance monitoring, and real-time vulnerability tracking.

## Prerequisites

- Node.js 20+
- PostgreSQL database (Neon, Supabase, or self-hosted)
- GitHub repository (for Actions CI/CD)
- AWS account (optional, for CodePipeline)

## Quick Start

### 1. Database Setup

#### Option A: Using Neon
\`\`\`bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:password@host/database"

# Run the schema migration
npm run db:migrate
\`\`\`

#### Option B: Using Supabase
\`\`\`bash
# Set database URL from Supabase dashboard
export DATABASE_URL="postgresql://postgres:[password]@[host]:5432/[database]"

# Run migrations
npm run db:migrate
\`\`\`

### 2. Environment Variables

Create a `.env.local` file:

\`\`\`env
# Database
DATABASE_URL=postgresql://user:password@host/database

# GitHub Actions (Optional)
GITHUB_TOKEN=ghp_xxxxx

# Webhook Security
WEBHOOK_SECRET=your_secret_key

# AWS (Optional)
AWS_ACCOUNT_ID=123456789
AWS_REGION=us-east-1
ECR_REPOSITORY_URI=123456789.dkr.ecr.us-east-1.amazonaws.com/medical-records-app

# Third-party Services
SONAR_HOST_URL=https://sonarqube.example.com
SONAR_TOKEN=your_token
SNYK_TOKEN=your_token
\`\`\`

### 3. Running the Dashboard

\`\`\`bash
npm install
npm run dev
\`\`\`

Visit `http://localhost:3000/dashboard` to view the security dashboard.

## CI/CD Setup

### GitHub Actions

1. Push `.github/workflows/*.yml` files to your repository
2. Add required secrets in GitHub Settings > Secrets:
   - `SONAR_TOKEN`
   - `SNYK_TOKEN`
   - `WEBHOOK_SECRET`

3. Workflows will trigger automatically on:
   - Push to main/develop branches
   - Pull requests
   - Daily schedule (2 AM UTC)

### AWS CodePipeline

1. Deploy CloudFormation template:
\`\`\`bash
aws cloudformation create-stack \
  --stack-name medical-records-devsecops \
  --template-body file://infrastructure/aws-devsecops-pipeline.yaml \
  --capabilities CAPABILITY_IAM
\`\`\`

2. Add GitHub token to AWS Secrets Manager:
\`\`\`bash
aws secretsmanager create-secret \
  --name github-token \
  --secret-string '{"token":"your_github_token"}'
\`\`\`

3. Pipeline will start automatically on code push

## API Endpoints

### Get Security Metrics
\`\`\`bash
GET /api/security/metrics
\`\`\`

Response:
\`\`\`json
{
  "security_score": 87.5,
  "critical_issues": 2,
  "high_issues": 8,
  "scans_24h": 12,
  "compliance_score": 92.3
}
\`\`\`

### Get Vulnerabilities
\`\`\`bash
GET /api/security/vulnerabilities
\`\`\`

### Get Recent Scans
\`\`\`bash
GET /api/security/scans?limit=10
\`\`\`

### Store Scan Results
\`\`\`bash
POST /api/security/store-scan
Authorization: Bearer <webhook_secret>

{
  "scan_id": "scan_123456",
  "repository_name": "medical-records-app",
  "branch_name": "main",
  "scan_type": "COMPREHENSIVE",
  "scan_status": "COMPLETED",
  "total_issues": 15,
  "critical_issues": 2,
  "high_issues": 5,
  "medium_issues": 8,
  "low_issues": 0,
  "scan_score": 85.5,
  "vulnerabilities": [...]
}
\`\`\`

## Database Schema

The database includes the following tables:

- **security_scans**: Stores all security scan records
- **vulnerabilities**: Detailed vulnerability findings
- **compliance_checks**: HIPAA, SOC 2, GDPR compliance status
- **secrets_detected**: Detected exposed secrets
- **dependency_vulnerabilities**: Package/dependency vulnerabilities
- **security_metrics**: Daily security metrics and trends
- **audit_logs**: Audit trail of all operations

## Monitoring and Alerts

### Dashboard Alerts
- Red alerts for CRITICAL vulnerabilities
- Warning alerts for HIGH issues
- Status dashboard for compliance frameworks

### Automated Remediation
Configure GitHub Actions to automatically:
- Create issues for vulnerabilities
- Notify security team via email/Slack
- Block merges if critical issues exist

## Compliance Frameworks

The system monitors:

- **HIPAA**: Medical Records Act compliance
- **SOC 2**: Security and operational compliance
- **GDPR**: Data protection regulations
- **PCI-DSS**: Payment card data security

## Troubleshooting

### Database Connection Issues
\`\`\`bash
# Test database connection
npm run db:test
\`\`\`

### Scan Results Not Appearing
1. Verify webhook secret is correct
2. Check API logs: `npm run logs`
3. Verify database permissions

### GitHub Actions Not Running
1. Check workflow syntax in `.github/workflows/`
2. Verify branch protection rules allow action execution
3. Check GitHub Actions logs

## Security Best Practices

1. Always review scan results before deployment
2. Set up alerts for CRITICAL vulnerabilities
3. Keep dependencies up to date
4. Enable branch protection with security checks
5. Rotate secrets regularly
6. Monitor audit logs for unauthorized access

## Support

For issues and questions:
1. Check the documentation
2. Review GitHub Issues
3. Contact security team
