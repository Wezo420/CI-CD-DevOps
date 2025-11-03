# DevSecOps Security Scanning Guide

## Integrated Security Scanners

### 1. Gitleaks (Secrets Detection)
Detects secrets, API keys, and sensitive information in code.

**Configuration:**
\`\`\`python
from scanner.gitleaks_scanner import GitLeaksScanner

scanner = GitLeaksScanner()
results = await scanner.scan("repo_path", "commit_hash")
\`\`\`

### 2. Checkov (Infrastructure as Code)
Scans CloudFormation, Terraform, and Kubernetes configs.

**Configuration:**
\`\`\`python
from scanner.checkov_scanner import CheckovScanner

scanner = CheckovScanner()
results = await scanner.scan("repo_path")
\`\`\`

### 3. Trivy (Container & Filesystem)
Scans Docker images and filesystems for vulnerabilities.

**Configuration:**
\`\`\`python
from scanner.trivy_scanner import TrivyScanner

scanner = TrivyScanner()
image_results = await scanner.scan_image("image:tag")
fs_results = await scanner.scan_filesystem("path")
\`\`\`

## CI/CD Integration

### GitHub Actions Workflows
1. **backend-tests.yml** - Run unit tests
2. **backend-security.yml** - Security scanning
3. **docker-build.yml** - Docker image build and scan
4. **backend-deploy.yml** - Production deployment

### Running Scans Locally
\`\`\`bash
# Run all scanners
python scripts/run_security_scan.py

# Send notifications
python scripts/notify.py

# Sync to dashboard
python scripts/sync_reports.py
\`\`\`

## Compliance Frameworks

### HIPAA (Health Insurance Portability & Accountability Act)
- Encryption of medical records
- Access control and authentication
- Audit logging
- Data breach notification

### SOC 2 (Service Organization Control)
- Security controls
- Availability and performance
- Processing integrity
- Confidentiality
- Privacy

### GDPR (General Data Protection Regulation)
- Consent management
- Data portability
- Right to erasure
- Privacy by design

### PCI-DSS (Payment Card Industry)
- Secure network architecture
- Cardholder data protection
- Vulnerability management
- Access control

## Notification Setup

### Slack
1. Create Slack App
2. Generate Bot Token
3. Add channel
4. Set `SLACK_BOT_TOKEN` and `SLACK_CHANNEL` in .env

### Email
1. Enable `EMAIL_ENABLED=true` in .env
2. Configure SMTP settings
3. Add email recipients in `EMAIL_TO`

## Best Practices

1. **Scan on Every Commit** - Catch vulnerabilities early
2. **Baseline Secrets** - Scan entire history with Gitleaks
3. **Dependency Updates** - Keep packages updated
4. **Review Failed Checks** - Don't ignore security warnings
5. **Fix Critical Issues** - Block deployment on critical findings
6. **Monitor Trends** - Track security improvements over time
