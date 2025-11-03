import subprocess
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TrivyScanner:
    """Container and filesystem scanning using Trivy"""
    
    def __init__(self):
        self.scan_type = "container"
    
    async def scan_image(self, image_name: str) -> Dict[str, Any]:
        """Scan Docker image"""
        try:
            cmd = [
                "trivy", "image",
                "--format", "json",
                "--severity", "CRITICAL,HIGH,MEDIUM",
                image_name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            data = json.loads(result.stdout) if result.stdout else {"Results": []}
            
            findings = []
            severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            
            for result_item in data.get("Results", []):
                for vuln in result_item.get("Vulnerabilities", []):
                    severity = vuln.get("Severity", "UNKNOWN")
                    severity_count[severity] = severity_count.get(severity, 0) + 1
                    
                    findings.append({
                        "id": vuln.get("VulnerabilityID"),
                        "package": vuln.get("PkgName"),
                        "severity": severity,
                        "title": vuln.get("Title"),
                        "description": vuln.get("Description"),
                        "installed_version": vuln.get("InstalledVersion"),
                        "fixed_version": vuln.get("FixedVersion"),
                        "primary_url": vuln.get("PrimaryURL")
                    })
            
            return {
                "scan_type": self.scan_type,
                "target": image_name,
                "status": "completed",
                "total_issues": len(findings),
                "critical_issues": severity_count.get("CRITICAL", 0),
                "high_issues": severity_count.get("HIGH", 0),
                "medium_issues": severity_count.get("MEDIUM", 0),
                "low_issues": severity_count.get("LOW", 0),
                "findings": findings
            }
        except subprocess.TimeoutExpired:
            logger.error("Trivy scan timeout")
            return {"status": "failed", "error": "Scan timeout"}
        except Exception as e:
            logger.error(f"Trivy scan error: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    async def scan_filesystem(self, path: str) -> Dict[str, Any]:
        """Scan filesystem"""
        try:
            cmd = [
                "trivy", "fs",
                "--format", "json",
                "--severity", "CRITICAL,HIGH,MEDIUM",
                path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            data = json.loads(result.stdout) if result.stdout else {"Results": []}
            
            findings = []
            severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            
            for result_item in data.get("Results", []):
                for vuln in result_item.get("Vulnerabilities", []):
                    severity = vuln.get("Severity", "UNKNOWN")
                    severity_count[severity] = severity_count.get(severity, 0) + 1
                    findings.append({
                        "id": vuln.get("VulnerabilityID"),
                        "package": vuln.get("PkgName"),
                        "severity": severity,
                        "title": vuln.get("Title"),
                        "installed_version": vuln.get("InstalledVersion"),
                        "fixed_version": vuln.get("FixedVersion")
                    })
            
            return {
                "scan_type": self.scan_type,
                "target": path,
                "status": "completed",
                "total_issues": len(findings),
                "critical_issues": severity_count.get("CRITICAL", 0),
                "high_issues": severity_count.get("HIGH", 0),
                "medium_issues": severity_count.get("MEDIUM", 0),
                "low_issues": severity_count.get("LOW", 0),
                "findings": findings
            }
        except Exception as e:
            logger.error(f"Trivy filesystem scan error: {str(e)}")
            return {"status": "failed", "error": str(e)}
