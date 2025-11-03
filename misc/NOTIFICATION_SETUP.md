# Notification Setup Guide

## Slack Notifications

### 1. Create Slack App
1. Go to https://api.slack.com/apps
2. Click "Create New App"
3. Choose "From scratch"
4. Name it "Medical Records Security"
5. Select your workspace

### 2. Enable Bot Token Scopes
1. Go to "OAuth & Permissions"
2. Add scopes: `chat:write`, `chat:write.public`
3. Install app to workspace

### 3. Generate Bot Token
1. Copy "Bot User OAuth Token" (starts with xoxb-)
2. Add to `.env`: `SLACK_BOT_TOKEN=xoxb-...`

### 4. Add to Channel
1. In Slack, add @Medical Records Security bot to #security channel
2. Set `SLACK_CHANNEL=#security` in .env

## Email Notifications

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Add to `.env`:
\`\`\`
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
\`\`\`

### Other Email Providers
Update `SMTP_SERVER` and `SMTP_PORT` accordingly.

## Testing Notifications

\`\`\`python
import asyncio
from scripts.notify import NotificationManager
import json

async def test():
    with open("security_report.json", "r") as f:
        report = json.load(f)
    
    notifier = NotificationManager()
    await notifier.notify(report)

asyncio.run(test())
\`\`\`

## CI/CD Integration

Add to GitHub Actions:
\`\`\`yaml
- name: Send Notifications
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
    EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
    EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
  run: |
    cd backend
    python scripts/notify.py
