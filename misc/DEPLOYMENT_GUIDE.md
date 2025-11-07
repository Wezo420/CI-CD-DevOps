# Complete Deployment Guide

## System Architecture

\`\`\`
┌─────────────────┐
│  GitHub Repo    │
│  with CI/CD      │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Workflows│
    └────┬────┘
         │
    ┌────▼──────────────────┐
    │  Security Scanners    │
    ├─ Gitleaks (Secrets)   │
    ├─ Checkov (IaC)        │
    └─ Trivy (Container)    │
         │
    ┌────▼────────────────┐
    │  FastAPI Backend     │
    ├─ Auth Endpoints     │
    ├─ Patient Records    │
    └─ Security API       │
         │
    ┌────▼────────────┐
    │  PostgreSQL DB  │
    │  (Neon/Local)   │
    └─────────────────┘
         │
    ┌────▼────────────────────┐
    │  Frontend Dashboard     │
    │  (Next.js/React)        │
    │  - Real-time metrics    │
    │  - Vulnerability tracking
    │  - Compliance status    │
    └─────────────────────────┘
\`\`\`

## Step-by-Step Deployment

### Phase 1: Local Development Setup (5-10 minutes)

1. **Clone Repository**
\`\`\`bash
git clone https://github.com/your-org/medical-records.git
cd medical-records
\`\`\`

2. **Setup Backend**
\`\`\`bash
cd backend
cp .env.example .env
# Edit .env:
# - Set NEON_DATABASE_URL for your PostgreSQL
# - Set SECRET_KEY to a random value
# - Configure SLACK_BOT_TOKEN if using Slack
\`\`\`

3. **Install Dependencies**
\`\`\`bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

4. **Initialize Database**
\`\`\`bash
# Using PostgreSQL locally or Neon cloud
psql postgres://user:password@host:5432/medical_records < ../scripts/01_security_dashboard_schema.sql
\`\`\`

5. **Run Backend**
\`\`\`bash
uvicorn main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
\`\`\`

### Phase 2: Security Scanning Setup (5 minutes)

1. **Install Security Scanners**
\`\`\`bash
# Gitleaks (secrets detection)
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks-linux-x64
chmod +x gitleaks-linux-x64

# Checkov (IaC scanning)
pip install checkov

# Trivy (container scanning)
wget https://github.com/aquasecurity/trivy/releases/download/v0.46.0/trivy_0.46.0_Linux-64bit.tar.gz
tar xzf trivy_0.46.0_Linux-64bit.tar.gz

# Semgrep (SAST)
pip install semgrep
\`\`\`

2. **Test Scanners Locally**
\`\`\`bash
cd backend
python scripts/run_security_scan.py
\`\`\`

### Phase 3: GitHub CI/CD Setup (10 minutes)

1. **Push to GitHub**
\`\`\`bash
git add .
git commit -m "Initial backend and security infrastructure"
git push origin main
\`\`\`

2. **Configure GitHub Secrets**
Go to GitHub Repository Settings → Secrets and add:
\`\`\`
SLACK_BOT_TOKEN=xoxb-your-token
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
DATABASE_URL=your-postgres-url
SECRET_KEY=your-random-secret
DEPLOY_URL=your-deployment-endpoint
DEPLOY_TOKEN=your-deploy-token
\`\`\`

3. **Enable GitHub Actions**
- Go to Actions tab
- Workflows should auto-run on push

### Phase 4: Notification Setup (5 minutes)

1. **Setup Slack**
- Create Slack App: https://api.slack.com/apps
- Copy Bot Token
- Add to GitHub Secrets as SLACK_BOT_TOKEN

2. **Setup Email (Optional)**
- Generate Gmail App Password
- Add to GitHub Secrets as EMAIL_PASSWORD and EMAIL_FROM

3. **Test Notifications**
\`\`\`bash
python scripts/notify.py
\`\`\`

### Phase 5: Frontend Integration (5 minutes)

1. **Frontend Already Configured**
- Next.js dashboard at `/app/dashboard`
- API endpoints at `/app/api/security/*`
- Mock data in routes, ready for backend

2. **Update API Client** (Optional)
Edit `lib/security-client.ts`:
\`\`\`typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
\`\`\`

3. **Set Environment Variable**
\`\`\`
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

### Phase 6: Production Deployment (varies)

#### Option A: Vercel (Next.js Frontend)
1. Connect GitHub repo to Vercel
2. Deploy automatically on push
3. Set environment variables in Vercel dashboard

#### Option B: AWS/Docker (Backend)
1. Build Docker image:
\`\`\`bash
docker build -t medical-records-api:v1.0 .
\`\`\`

2. Push to ECR:
\`\`\`bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag medical-records-api:v1.0 YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/medical-records:v1.0
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/medical-records:v1.0
\`\`\`

3. Deploy to ECS/EKS using CloudFormation from `infrastructure/aws-devsecops-pipeline.yaml`

#### Option C: Railway/Render (Full Stack)
1. Connect GitHub repo
2. Auto-deploys on push
3. Manages environment variables

## Health Checks

### Backend Health
\`\`\`bash
curl http://localhost:8000/health
\`\`\`

### Database Connection
\`\`\`bash
curl http://localhost:8000/api/security/scans -H "Authorization: Bearer $API_KEY
\`\`\`

### Security Dashboard
\`\`\`
http://localhost:3000/dashboard
\`\`\`

## Monitoring & Maintenance

### Logs
\`\`\`bash
# Backend logs
docker logs medical_records_api

# Database logs
docker logs medical_records_db

# GitHub Actions
# View in: https://github.com/your-org/medical-records/actions
\`\`\`

### Security Scan Reports
- View in Dashboard: http://localhost:3000/dashboard
- API endpoint: GET /api/security/scans
- Raw JSON: `security_report.json`

### Backup & Recovery
\`\`\`bash
# Backup database
pg_dump medical_records > backup.sql

# Restore database
psql medical_records < backup.sql
\`\`\`

## Troubleshooting

### Database Connection Error
\`\`\`
ERROR: cannot connect to PostgreSQL
Solution: Check DATABASE_URL and ensure PostgreSQL is running
\`\`\`

### Scanner Installation Issues
\`\`\`
ERROR: Gitleaks/Checkov/Trivy not found
Solution: Run scanner installation commands again
\`\`\`

### GitHub Actions Failing
\`\`\`
1. Check Secrets are set correctly
2. View workflow logs in GitHub Actions
3. Re-run failed workflow with debugging enabled
\`\`\`

### API Not Responding
\`\`\`
1. Check backend logs: docker logs medical_records_api
2. Verify database connection
3. Check firewall/network settings
4. Restart services: docker-compose restart
\`\`\`

## Security Best Practices

1. **Never commit secrets** - Use .env files
2. **Rotate API tokens** - Regularly update tokens
3. **Enable MFA** - For GitHub and production accounts
4. **Monitor logs** - Set up centralized logging
5. **Scan dependencies** - Use `pip audit` regularly
6. **Update regularly** - Keep libraries updated
7. **HTTPS everywhere** - Use SSL/TLS certificates
8. **Database encryption** - Enable at-rest encryption
9. **Audit logging** - Track all database changes
10. **Regular backups** - Automated daily backups

## Performance Optimization

### Database
- Enable connection pooling (configured in config.py)
- Create indexes on frequently queried fields
- Archive old scan results
- Use read replicas for reporting

### Backend
- Enable gzip compression
- Use caching (Redis optional)
- Optimize SQL queries
- Monitor memory usage

### Frontend
- Lazy load dashboard charts
- Paginate vulnerability lists
- Cache API responses (SWR)
- Optimize bundle size

## Scalability

### Horizontal Scaling
- Deploy multiple backend instances
- Use load balancer (nginx, AWS LB)
- Shared PostgreSQL database

### Vertical Scaling
- Increase server resources
- Upgrade PostgreSQL tier
- Increase API rate limits

## Cost Optimization

- Use free tier services (GitHub Actions, Neon free)
- Auto-scale resources based on demand
- Archive old data to storage
- Use spot instances for non-critical workloads
