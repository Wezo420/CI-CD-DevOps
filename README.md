# CI-CD-DevOps — DevSecOps Plugin & Medical Records Backend

**Status:** Ready for handoff (CI passing)
**Short description:** A demo project showing a DevSecOps security plugin integrated into a FastAPI-based Medical Records backend plus a Next.js dashboard. The plugin runs secret scans, IaC scans, and container checks (using Gitleaks, Checkov, and Trivy) inside GitHub Actions and produces JSON/HTML reports, artifacts, and notifications.

---

## Table of contents

* [What this project is](#what-this-project-is)
* [Repository layout](#repository-layout)
* [Quick start — run locally](#quick-start--run-locally)
* [Testing](#testing)
* [Security scanning (DevSecOps)](#security-scanning-devsecops)
* [Dashboard (frontend)](#dashboard-frontend)
* [Continuous Integration](#continuous-integration)
* [Configuration & environment variables](#configuration--environment-variables)
* [Reports & artifacts](#reports--artifacts)
* [Developer notes & best practices](#developer-notes--best-practices)
* [Handoff checklist](#handoff-checklist)
* [Contributors & contact](#contributors--contact)
* [License](#license)

---

## What this project is

This repository is a compact demo that integrates a security scanning plugin into a CI/CD pipeline for a Medical Records API. It demonstrates:

* A Python FastAPI backend (medical records example) with authentication and DB models.
* A modular security plugin that runs:

  * **Gitleaks** for secret detection
  * **Checkov** for IaC policy scanning
  * **Trivy** for container vulnerability scanning
* A simple notification script that formats results for Slack/email.
* A React/Next.js dashboard that visualizes scan results and historic trends (mock data for demo).
* GitHub Actions workflows that run tests, scanning, artifact uploads, and notifier steps.

This repo is intended as an educational/demo project to show how DevSecOps tooling fits into a CI/CD workflow and how teams can “shift left” on security.

---

## Repository layout

```
CI-CD-DevOps/
├── backend/                        # FastAPI application (backend)
│   ├── api/                        # endpoint modules (auth, patients, etc.)
│   ├── auth/
│   ├── database/
│   ├── scanner/                    # scanner wrappers (gitleaks, checkov, trivy)
│   ├── scripts/                    # run_security_scan.py, notify.py
│   ├── config/
│   ├── main.py
│   └── requirements.txt
├── dashboard/                      # Next.js frontend (security dashboard)
│   ├── pages/
│   └── package.json
├── reports/                        # mock_report.json + history and generated reports
├── .github/
│   └── workflows/                  # GitHub Actions workflows
├── docs/                           # documentation (docs/handbook, demo scripts)
├── README.md                       # (this file)
└── .env.example
```

---

## Quick start — run locally

> Tested on Windows (PowerShell) and Linux. Use Python 3.10+.

1. **Clone**

```bash
git clone https://github.com/Wezo420/CI-CD-DevOps.git
cd CI-CD-DevOps
```

2. **Backend: create & activate venv**
   Windows (PowerShell):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r backend/requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

3. **Set environment (example)**
   Copy and edit `.env`:

```bash
# from repo root
cp backend/.env.example backend/.env
# Edit backend/.env to set DB and secrets (do NOT commit .env)
```

4. **Run backend**

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/` — API docs at `/docs`.

5. **Dashboard (frontend)**

```bash
cd dashboard
cp .env.local.example .env.local
# set NEXT_PUBLIC_API_URL to http://localhost:8000
npm install
npm run dev
```

Open the dashboard at `http://localhost:3000`.

---

## Testing

* **Unit tests** use `pytest` in the backend folder.

```bash
cd backend
.\.venv\Scripts\Activate.ps1  # or source .venv/bin/activate
pytest -q
```

* Some tests are integration-style and expect DB connectivity; use `.env` or set `TEST_DATABASE_URL`. Tests that require a live MySQL DB are skipped if not configured.

---

## Security scanning (DevSecOps)

This project integrates the following scanners (examples and wrappers shipped under `backend/scanner/`):

* **Gitleaks** — secret detection in git history and working tree.
* **Checkov** — IaC scanning for Terraform / CloudFormation under `infra/` or `backend/config`.
* **Trivy** — container vulnerability scanning (image scanning / filesystem).

**Run local scans**

```bash
# from project root
cd backend
python scripts/run_security_scan.py
# Generates reports under ../reports/ (configurable)
```

**Notifier**

```bash
python scripts/notify.py --report ../reports/mock_report.json --config config/config.yaml
```

Notifier can post Slack messages (set `SLACK_WEBHOOK_URL` in Actions secrets or locally in env).

**Important:** Never commit secrets to repo. Use `.env` and GitHub Actions Secrets.

---

## Dashboard (frontend)

* The dashboard uses `reports/mock_report.json` and `reports/mock_report_history.json` as demo data.
* To connect to live backend, set `NEXT_PUBLIC_API_URL` in `dashboard/.env.local`:

```
NEXT_PUBLIC_API_URL=http://<backend-host>:8000
```

* The frontend expects a backend endpoint: `GET /api/reports/latest` (returns same schema as `reports/mock_report.json`). If not present, the dashboard defaults to mock data.

---

## Continuous Integration

* GitHub Actions workflows are in `.github/workflows/`.

  * `local_ci_notify_on_failure.yml` — runs tests, scanner scripts, and uploads reports; runs notifier when a job fails (configurable).
* Workflows already include steps to:

  * Setup Python
  * Install dependencies
  * Run tests
  * Run scanners
  * Upload scan artifacts
  * Optional notify step (Slack/email)
* **Secrets**: configure repository secrets in GitHub Settings:

  * `SLACK_WEBHOOK_URL`, `SMTP_USER`, `SMTP_PASS`, `TEST_DATABASE_URL` (if you want integration DB tests)

---

## Configuration & environment variables

* `backend/config/config.yaml` — plugin configuration (which scanners to run, thresholds, report paths).
* `backend/.env.example` — environment variable examples (DATABASE_URL, SECRET_KEY, etc.)
* `dashboard/.env.local.example` — frontend env example (`NEXT_PUBLIC_API_URL`).

**Do not commit real secrets.** Keep `.env` in `.gitignore` and use GitHub Secrets for CI.

---

## Reports & artifacts

* Reports are saved to `reports/` by default:

  * `mock_report.json` — demo latest scan
  * `mock_report_history.json` — demo history for charts
  * CI artifacts: SARIF, JSON, HTML reports (uploaded by GitHub Actions)
* Use reports as dashboard input or store them in S3 for centralized dashboards.

---

## Developer notes & best practices

* **Secrets**: Use `detect-secrets`, pre-commit hooks, and the included Gitleaks check in CI to avoid accidental leaks.
* **Dependencies**: Keep `requirements.txt` pinned for reproducibility. Use Dependabot to automate updates.
* **Adding new scanners**: Implement a new scanner wrapper under `backend/scanner/` and normalize its output to the unified findings schema (fields: `scanner`, `rule_id`, `file_path`, `severity`, `message`).
* **Policy engine**: Config-driven fail/pass logic lives in the orchestrator — adjust `config.yaml` thresholds as per project policy.
* **Logging**: CI logs go to stdout; the plugin uses Python logging. In AWS deployments, send logs to CloudWatch.

---

## Contributors & contact

* **Project lead / QA & Documentation:** Aviral Sharma (GitHub: `Wezo420`)
* **Backend & plugin:** Ayush Shaw, Anvita Choudhury, Aviral Sharma
* **Frontend (dashboard):** Ritika Dekate
* **CI/CD specialist / DevSecOps:** Anjali Bhat, Aviral Sharma

---

## License

This project is intended for educational and demonstration purposes. Add a license file if required (e.g. MIT).

---
