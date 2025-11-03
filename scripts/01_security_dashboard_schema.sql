-- Security Dashboard Schema for Medical Records Application
-- This schema stores vulnerability scans, compliance data, and DevSecOps metrics

-- Scans table: Track all security scans performed
CREATE TABLE IF NOT EXISTS security_scans (
  id SERIAL PRIMARY KEY,
  scan_id VARCHAR(255) UNIQUE NOT NULL,
  repository_name VARCHAR(255) NOT NULL,
  branch_name VARCHAR(255) NOT NULL,
  scan_type VARCHAR(50) NOT NULL, -- SAST, DAST, DEPENDENCY, SECRETS, CONTAINER
  scan_status VARCHAR(50) NOT NULL, -- PENDING, IN_PROGRESS, COMPLETED, FAILED
  start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  end_time TIMESTAMP,
  total_issues INTEGER DEFAULT 0,
  critical_issues INTEGER DEFAULT 0,
  high_issues INTEGER DEFAULT 0,
  medium_issues INTEGER DEFAULT 0,
  low_issues INTEGER DEFAULT 0,
  scan_score DECIMAL(5, 2),
  commit_hash VARCHAR(255),
  pull_request_id VARCHAR(255),
  ci_provider VARCHAR(50), -- GITHUB_ACTIONS, AWS_CODEPIPELINE
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vulnerabilities table: Detailed vulnerability information
CREATE TABLE IF NOT EXISTS vulnerabilities (
  id SERIAL PRIMARY KEY,
  scan_id VARCHAR(255) NOT NULL REFERENCES security_scans(scan_id),
  vulnerability_id VARCHAR(255) UNIQUE,
  title VARCHAR(500) NOT NULL,
  description TEXT,
  severity VARCHAR(20) NOT NULL, -- CRITICAL, HIGH, MEDIUM, LOW, INFO
  vulnerability_type VARCHAR(100), -- SQL_INJECTION, XSS, WEAK_CRYPTO, etc.
  file_path VARCHAR(500),
  line_number INTEGER,
  cwe_id VARCHAR(20),
  cvss_score DECIMAL(3, 1),
  status VARCHAR(50) DEFAULT 'OPEN', -- OPEN, RESOLVED, IGNORED, SUPPRESSED
  remediation_advice TEXT,
  first_detected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  false_positive BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compliance table: HIPAA, SOC 2, GDPR compliance tracking
CREATE TABLE IF NOT EXISTS compliance_checks (
  id SERIAL PRIMARY KEY,
  compliance_framework VARCHAR(100) NOT NULL, -- HIPAA, SOC2, GDPR, PCI_DSS
  check_name VARCHAR(255) NOT NULL,
  check_status VARCHAR(50) NOT NULL, -- PASS, FAIL, WARNING, NOT_APPLICABLE
  last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  evidence_url VARCHAR(500),
  remediation_required BOOLEAN DEFAULT FALSE,
  remediation_deadline DATE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Secrets table: Track detected secrets and exposure incidents
CREATE TABLE IF NOT EXISTS secrets_detected (
  id SERIAL PRIMARY KEY,
  scan_id VARCHAR(255) REFERENCES security_scans(scan_id),
  secret_type VARCHAR(100), -- API_KEY, PASSWORD, TOKEN, PRIVATE_KEY, etc.
  secret_location VARCHAR(500),
  detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(50) DEFAULT 'EXPOSED', -- EXPOSED, ROTATED, REVOKED, FALSE_POSITIVE
  action_taken VARCHAR(500),
  remediation_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dependency vulnerabilities table
CREATE TABLE IF NOT EXISTS dependency_vulnerabilities (
  id SERIAL PRIMARY KEY,
  scan_id VARCHAR(255) REFERENCES security_scans(scan_id),
  package_name VARCHAR(255) NOT NULL,
  current_version VARCHAR(50),
  vulnerable_version_range VARCHAR(100),
  fixed_version VARCHAR(50),
  cve_id VARCHAR(20),
  severity VARCHAR(20) NOT NULL,
  advisory TEXT,
  package_manager VARCHAR(50), -- npm, pip, maven, etc.
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Security metrics and trends
CREATE TABLE IF NOT EXISTS security_metrics (
  id SERIAL PRIMARY KEY,
  metric_date DATE NOT NULL,
  total_vulnerabilities INTEGER DEFAULT 0,
  critical_count INTEGER DEFAULT 0,
  high_count INTEGER DEFAULT 0,
  medium_count INTEGER DEFAULT 0,
  low_count INTEGER DEFAULT 0,
  average_scan_score DECIMAL(5, 2),
  scans_performed INTEGER DEFAULT 0,
  compliance_score DECIMAL(5, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_logs (
  id SERIAL PRIMARY KEY,
  action VARCHAR(255) NOT NULL,
  entity_type VARCHAR(100),
  entity_id VARCHAR(255),
  user_id VARCHAR(255),
  details JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_scans_repository ON security_scans(repository_name, created_at DESC);
CREATE INDEX idx_scans_status ON security_scans(scan_status);
CREATE INDEX idx_scans_type ON security_scans(scan_type);
CREATE INDEX idx_vulnerabilities_scan ON vulnerabilities(scan_id);
CREATE INDEX idx_vulnerabilities_severity ON vulnerabilities(severity);
CREATE INDEX idx_vulnerabilities_status ON vulnerabilities(status);
CREATE INDEX idx_compliance_framework ON compliance_checks(compliance_framework);
CREATE INDEX idx_secrets_status ON secrets_detected(status);
CREATE INDEX idx_dependencies_package ON dependency_vulnerabilities(package_name);
CREATE INDEX idx_metrics_date ON security_metrics(metric_date DESC);
