import asyncio
import logging
import json
import os
from datetime import datetime
from scanner.gitleaks_scanner import GitLeaksScanner
from scanner.checkov_scanner import CheckovScanner
from scanner.trivy_scanner import TrivyScanner
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityScanOrchestrator:
    """Orchestrate multiple security scans"""
    
    def __init__(self):
        self.gitleaks = GitLeaksScanner()
        self.checkov = CheckovScanner()
        self.trivy = TrivyScanner()
    
    async def run_all_scans(self, repo_path: str, commit_hash: str = None, image_name: str = None):
        """Run all security scans"""
        logger.info(f"Starting security scans for {repo_path}")
        
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "repository": repo_path,
            "commit": commit_hash,
            "scans": {}
        }
        
        # Run Gitleaks
        logger.info("Running Gitleaks scan...")
        results["scans"]["secrets"] = await self.gitleaks.scan(repo_path, commit_hash)
        
        # Run Checkov
        logger.info("Running Checkov scan...")
        results["scans"]["iac"] = await self.checkov.scan(repo_path)
        
        # Run Trivy filesystem scan
        logger.info("Running Trivy filesystem scan...")
        results["scans"]["filesystem"] = await self.trivy.scan_filesystem(repo_path)
        
        # Run Trivy image scan if image provided
        if image_name:
            logger.info(f"Running Trivy image scan for {image_name}...")
            results["scans"]["container"] = await self.trivy.scan_image(image_name)
        
        # Aggregate results
        total_issues = sum(scan.get("total_issues", 0) for scan in results["scans"].values())
        critical = sum(scan.get("critical_issues", 0) for scan in results["scans"].values())
        high = sum(scan.get("high_issues", 0) for scan in results["scans"].values())
        medium = sum(scan.get("medium_issues", 0) for scan in results["scans"].values())
        low = sum(scan.get("low_issues", 0) for scan in results["scans"].values())
        
        results["summary"] = {
            "total_issues": total_issues,
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low
        }
        
        logger.info(f"Security scans completed. Found {total_issues} issues")
        return results

async def main():
    repo_path = os.getenv("REPOSITORY_PATH", ".")
    commit_hash = os.getenv("COMMIT_HASH")
    image_name = os.getenv("DOCKER_IMAGE")
    output_file = os.getenv("OUTPUT_FILE", "security_report.json")
    
    orchestrator = SecurityScanOrchestrator()
    results = await orchestrator.run_all_scans(repo_path, commit_hash, image_name)
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Report saved to {output_file}")
    
    # Exit with error if critical issues found
    if results["summary"]["critical"] > 0:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
