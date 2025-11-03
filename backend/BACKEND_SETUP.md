# Backend Setup Guide - Medical Records API

## Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Docker & Docker Compose (optional)

## Installation

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/your-org/medical-records.git
cd medical-records/backend
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Environment
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### 5. Initialize Database
\`\`\`bash
# Create tables
python -c "import asyncio; from database.config import init_db; asyncio.run(init_db())"
\`\`\`

### 6. Run Server
\`\`\`bash
uvicorn main:app --reload
\`\`\`

Server will be available at http://localhost:8000
API documentation: http://localhost:8000/docs

## Docker Setup

### Build Image
\`\`\`bash
docker build -t medical-records-api .
\`\`\`

### Run with Docker Compose
\`\`\`bash
docker-compose up -d
\`\`\`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Medical Records
- `GET /api/patients/me` - Get current user's records
- `POST /api/patients/create` - Create new record
- `GET /api/patients/{record_id}` - Get specific record

### Security Scans
- `GET /api/security/scans` - Get scan results
- `POST /api/security/scans` - Store scan results
- `GET /api/security/vulnerabilities` - Get vulnerabilities
- `GET /api/security/compliance` - Get compliance status

## Security Scanning

### Run All Scans
\`\`\`bash
python scripts/run_security_scan.py
\`\`\`

### Send Notifications
\`\`\`bash
python scripts/notify.py
\`\`\`

### Sync Reports
\`\`\`bash
python scripts/sync_reports.py
\`\`\`

## Testing

### Run Tests
\`\`\`bash
pytest tests/ -v
\`\`\`

### With Coverage
\`\`\`bash
pytest tests/ --cov=. --cov-report=html
\`\`\`

## Production Deployment

### Environment Variables
- Change `SECRET_KEY` to a secure value
- Set `DEBUG=false`
- Use production PostgreSQL database
- Configure CORS properly

### Database Migration
\`\`\`bash
# Backup existing database
pg_dump medical_records > backup.sql
\`\`\`

### HTTPS
Configure reverse proxy (nginx, Apache) with SSL/TLS

### Monitoring
- Use health check endpoint: `/health`
- Monitor logs and errors
- Set up alerting for critical issues
