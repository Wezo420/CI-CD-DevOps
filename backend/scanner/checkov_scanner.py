import subprocess
import json
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class CheckovScanner:
    """Infrastructure as Code scanning using Checkov"""
    
    def __init__(self):
        self.scan_type = "iac"
    
    async def scan(self, repo_path: str) -> Dict[str, Any]:
        """Run Checkov scan for IaC vulnerabilities"""
        try:
            cmd = [
                "checkov",
                "--directory", repo_path,
                "--format", "json",
                "--quiet",
                "--skip-check", "CKV_DOCKER_2"  # Skip non-essential checks
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            data = json.loads(result.stdout) if result.stdout else {
                "check_type_to_results": {}
            }
            
            findings = []
            critical_count = 0
            high_count = 0
            
            for check_results in data.get("check_type_to_results", {}).values():
                for check in check_results.get("failed_checks", []):
                    severity = check.get("check_result", {}).get("result", "UNKNOWN")
                    if severity == "FAILED":
                        severity_level = "high"
                        high_count += 1
                    else:
                        severity_level = "medium"
                    
                    findings.append({
                        "check_id": check.get("check_id"),
                        "resource": check.get("resource"),
                        "file": check.get("file_path"),
                        "check_result": severity_level,
                        "message": check.get("check_class"),
                        "remediation": check.get("check_result", {}).get("evaluated_keys", [])
                    })
            
            return {
                "scan_type": self.scan_type,
                "status": "completed",
                "total_issues": len(findings),
                "critical_issues": critical_count,
                "high_issues": high_count,
                "medium_issues": len(findings) - critical_count - high_count,
                "low_issues": 0,
                "findings": findings,
                "raw_output": data
            }
        except subprocess.TimeoutExpired:
            logger.error("Checkov scan timeout")
            return {"status": "failed", "error": "Scan timeout"}
        except Exception as e:
            logger.error(f"Checkov scan error: {str(e)}")
            return {"status": "failed", "error": str(e)}
