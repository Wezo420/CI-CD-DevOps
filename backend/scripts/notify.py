import os
import json
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationManager:
    """Send scan results notifications"""
    
    def __init__(self):
        self.slack_token = os.getenv("SLACK_BOT_TOKEN")
        self.slack_channel = os.getenv("SLACK_CHANNEL", "#security")
        self.email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_from = os.getenv("EMAIL_FROM")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_to = os.getenv("EMAIL_TO", "").split(",")
    
    async def send_slack_notification(self, report: Dict[str, Any]):
        """Send scan results to Slack"""
        if not self.slack_token:
            logger.warning("Slack token not configured")
            return
        
        try:
            client = WebClient(token=self.slack_token)
            
            summary = report.get("summary", {})
            color = "danger" if summary.get("critical", 0) > 0 else "warning"
            
            message = {
                "attachments": [
                    {
                        "color": color,
                        "title": "Security Scan Results",
                        "fields": [
                            {"title": "Total Issues", "value": str(summary.get("total_issues", 0)), "short": True},
                            {"title": "Critical", "value": str(summary.get("critical", 0)), "short": True},
                            {"title": "High", "value": str(summary.get("high", 0)), "short": True},
                            {"title": "Medium", "value": str(summary.get("medium", 0)), "short": True},
                            {"title": "Repository", "value": report.get("repository", "N/A"), "short": True},
                            {"title": "Commit", "value": report.get("commit", "N/A")[:8], "short": True},
                        ],
                        "ts": int(datetime.utcnow().timestamp())
                    }
                ]
            }
            
            response = client.chat_postMessage(channel=self.slack_channel, **message)
            logger.info(f"Slack notification sent: {response['ts']}")
        except SlackApiError as e:
            logger.error(f"Slack notification error: {e.response['error']}")
        except Exception as e:
            logger.error(f"Notification error: {str(e)}")
    
    async def send_email_notification(self, report: Dict[str, Any]):
        """Send scan results via email"""
        if not self.email_enabled or not self.email_from:
            logger.warning("Email notifications not configured")
            return
        
        try:
            summary = report.get("summary", {})
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Security Scan Report</h2>
                    <table border="1" cellpadding="10">
                        <tr><th>Metric</th><th>Count</th></tr>
                        <tr><td>Total Issues</td><td>{summary.get('total_issues', 0)}</td></tr>
                        <tr><td>Critical</td><td style="color: red;"><strong>{summary.get('critical', 0)}</strong></td></tr>
                        <tr><td>High</td><td style="color: orange;"><strong>{summary.get('high', 0)}</strong></td></tr>
                        <tr><td>Medium</td><td style="color: yellow;"><strong>{summary.get('medium', 0)}</strong></td></tr>
                        <tr><td>Low</td><td>{summary.get('low', 0)}</td></tr>
                    </table>
                    <p><strong>Repository:</strong> {report.get('repository', 'N/A')}</p>
                    <p><strong>Commit:</strong> {report.get('commit', 'N/A')}</p>
                    <p><strong>Timestamp:</strong> {report.get('timestamp', 'N/A')}</p>
                </body>
            </html>
            """
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Security Scan Report - {summary.get('critical', 0)} Critical Issues"
            msg["From"] = self.email_from
            msg["To"] = ",".join(self.email_to)
            
            msg.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.sendmail(self.email_from, self.email_to, msg.as_string())
            
            logger.info(f"Email notification sent to {self.email_to}")
        except Exception as e:
            logger.error(f"Email notification error: {str(e)}")
    
    async def notify(self, report: Dict[str, Any]):
        """Send notifications via all configured channels"""
        await self.send_slack_notification(report)
        await self.send_email_notification(report)

async def main():
    report_file = os.getenv("REPORT_FILE", "security_report.json")
    
    with open(report_file, 'r') as f:
        report = json.load(f)
    
    notifier = NotificationManager()
    await notifier.notify(report)

if __name__ == "__main__":
    import asyncio
    from datetime import datetime
    asyncio.run(main())
