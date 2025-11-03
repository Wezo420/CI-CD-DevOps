import os
import json
import httpx
import logging
from datetime import datetime
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportSync:
    """Sync security scan reports to dashboard"""
    
    def __init__(self):
        self.api_url = os.getenv("API_URL", "http://localhost:8000")
        self.api_token = os.getenv("API_TOKEN")
    
    async def sync_report(self, report_file: str):
        """Upload security report to dashboard API"""
        try:
            with open(report_file, 'r') as f:
                report = json.load(f)
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/api/security/scans",
                    json={
                        "scan_type": "comprehensive",
                        "repository": report.get("repository"),
                        "branch": os.getenv("BRANCH", "main"),
                        "commit_hash": report.get("commit"),
                        "total_issues": report["summary"]["total_issues"],
                        "critical_issues": report["summary"]["critical"],
                        "high_issues": report["summary"]["high"],
                        "medium_issues": report["summary"]["medium"],
                        "low_issues": report["summary"]["low"],
                        "results": report
                    },
                    headers=headers
                )
                
                if response.status_code == 200:
                    logger.info("Report synced successfully")
                else:
                    logger.error(f"Sync failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Report sync error: {str(e)}")

async def main():
    report_file = os.getenv("REPORT_FILE", "security_report.json")
    syncer = ReportSync()
    await syncer.sync_report(report_file)

if __name__ == "__main__":
    asyncio.run(main())
