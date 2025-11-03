import subprocess
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class GitLeaksScanner:
    """Secrets detection using Gitleaks"""
    
    def __init__(self):
        self.scan_type = "secrets"
    
    async def scan(self, repo_path: str, commit_hash: str = None) -> Dict[str, Any]:
        """Run Gitleaks scan for secrets"""
        try:
            output_file = f"/tmp/gitleaks_report_{datetime.now().timestamp()}.json"
            
            cmd = ["gitleaks", "detect", "--source", repo_path, "--report-format", "json"]
            if commit_hash:
                cmd.extend(["--log-opts", f"{commit_hash}~1..{commit_hash}"])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    data = json.load(f)
            else:
                data = json.loads(result.stdout) if result.stdout else {"matches": []}
            
            findings = []
            for match in data.get("matches", []):
                findings.append({
                    "type": "secret",
                    "secret_type": match.get("RuleID"),
                    "file": match.get("File"),
                    "line": match.get("StartLine"),
                    "commit": match.get("Commit"),
                    "message": match.get("Match"),
                    "severity": "critical"
                })
            
            return {
                "scan_type": self.scan_type,
                "status": "completed",
                "total_issues": len(findings),
                "critical_issues": len(findings),
                "high_issues": 0,
                "medium_issues": 0,
                "low_issues": 0,
                "findings": findings,
                "raw_output": data
            }
        except subprocess.TimeoutExpired:
            logger.error("Gitleaks scan timeout")
            return {"status": "failed", "error": "Scan timeout"}
        except Exception as e:
            logger.error(f"Gitleaks scan error: {str(e)}")
            return {"status": "failed", "error": str(e)}
