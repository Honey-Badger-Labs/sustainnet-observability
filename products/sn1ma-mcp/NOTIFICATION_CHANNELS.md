# Notification Channels Configuration for SN1MA-MCP

## Overview
Configure Grafana/Alertmanager to send financial guardrail alerts to:
1. **Slack** - Real-time team notifications
2. **Email** - Formal audit trail
3. **SMS** (future) - Critical alerts only

---

## 1. Slack Notification Channel

### Create Slack Webhook

1. Go to Slack workspace: https://honey-badger-labs.slack.com
2. Create a new channel: `#sn1ma-financial-alerts`
3. Add Incoming Webhook:
   - Go to: https://api.slack.com/apps
   - Create New App → "From scratch"
   - Name: "SN1MA Financial Monitor"
   - Select workspace: Honey Badger Labs
   - Features → Incoming Webhooks → Activate
   - Add New Webhook to Workspace
   - Select channel: `#sn1ma-financial-alerts`
   - Copy webhook URL: `https://hooks.slack.com/services/T.../.../...`

### Configure in Grafana

**Alerting → Contact Points → Add Contact Point:**

```yaml
Name: slack-sn1ma-financial
Type: Slack
Webhook URL: https://hooks.slack.com/services/YOUR_WEBHOOK_HERE
Username: SN1MA Financial Monitor
Icon Emoji: :chart_with_upwards_trend:
Title: |
  {{ if eq .Status "firing" }}🚨{{ else }}✅{{ end }} {{ .GroupLabels.alertname }}
Message: |
  *Alert:* {{ .GroupLabels.alertname }}
  *Severity:* {{ .CommonLabels.severity }}
  *Category:* {{ .CommonLabels.category }}
  
  {{ range .Alerts }}
  *Summary:* {{ .Annotations.summary }}
  *Description:* {{ .Annotations.description }}
  *Business Impact:* {{ .Annotations.business_impact }}
  
  *Action Required:*
  {{ .Annotations.action_required }}
  
  *Playbook:* {{ .Annotations.playbook }}
  {{ end }}
```

---

## 2. Email Notification Channel

### Configure SMTP Settings

**Alerting → Contact Points → Add Contact Point:**

```yaml
Name: email-sn1ma-financial
Type: Email
Addresses: jake@honeybadgerlabs.ai, finance-alerts@honeybadgerlabs.ai
Subject: |
  [SN1MA] {{ .CommonLabels.severity | toUpper }}: {{ .GroupLabels.alertname }}
Message: |
  Financial Guardrail Alert
  
  Alert Name: {{ .GroupLabels.alertname }}
  Severity: {{ .CommonLabels.severity }}
  Category: {{ .CommonLabels.category }}
  Guardrail: {{ .CommonLabels.guardrail }}
  
  {{ range .Alerts }}
  Summary:
  {{ .Annotations.summary }}
  
  Description:
  {{ .Annotations.description }}
  
  Business Impact:
  {{ .Annotations.business_impact }}
  
  Action Required:
  {{ .Annotations.action_required }}
  
  Playbook Reference:
  {{ .Annotations.playbook }}
  
  Dashboard: https://grafana.sustainnet.ai/d/sn1ma-financial-health
  {{ end }}
```

**SMTP Configuration (Grafana config):**

```ini
[smtp]
enabled = true
host = smtp.gmail.com:587
user = notifications@honeybadgerlabs.ai
password = YOUR_APP_PASSWORD_HERE
skip_verify = false
from_address = notifications@honeybadgerlabs.ai
from_name = SN1MA Financial Monitor
```

---

## 3. Notification Policies

### Route Alerts by Severity

**Alerting → Notification Policies:**

```yaml
Root Policy:
  - Group by: alertname, category
  - Group wait: 30s
  - Group interval: 5m
  - Repeat interval: 4h
  - Contact point: slack-sn1ma-financial

Child Policies:

  # CRITICAL alerts → Slack + Email immediately
  - Match: severity = critical
    Contact points: 
      - slack-sn1ma-financial
      - email-sn1ma-financial
    Group wait: 10s
    Repeat interval: 1h
    Continue: false
  
  # WARNING alerts → Slack only, less frequent
  - Match: severity = warning
    Contact points:
      - slack-sn1ma-financial
    Group wait: 5m
    Repeat interval: 12h
    Continue: false
  
  # INFO/Milestone alerts → Slack, once only
  - Match: severity = info
    Contact points:
      - slack-sn1ma-financial
    Group wait: 1m
    Repeat interval: 0  # Never repeat
    Continue: false
```

---

## 4. Alertmanager Configuration (Alternative)

If using Prometheus Alertmanager instead of Grafana Alerting:

**File:** `sustainnet-observability/products/sn1ma-mcp/alertmanager.yml`

```yaml
global:
  slack_api_url: 'https://hooks.slack.com/services/YOUR_WEBHOOK_HERE'

route:
  receiver: 'slack-financial'
  group_by: ['alertname', 'category', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  
  routes:
    # CRITICAL alerts
    - match:
        severity: critical
      receiver: 'slack-and-email-critical'
      group_wait: 10s
      repeat_interval: 1h
    
    # WARNING alerts
    - match:
        severity: warning
      receiver: 'slack-financial'
      group_wait: 5m
      repeat_interval: 12h
    
    # INFO/Milestones
    - match:
        severity: info
      receiver: 'slack-milestones'
      group_wait: 1m
      repeat_interval: 0

receivers:
  - name: 'slack-and-email-critical'
    slack_configs:
      - channel: '#sn1ma-financial-alerts'
        username: 'SN1MA Financial Monitor'
        icon_emoji: ':rotating_light:'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'
        text: |
          {{ range .Alerts }}
          *Summary:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          *Business Impact:* {{ .Annotations.business_impact }}
          
          *Action Required:*
          ```
          {{ .Annotations.action_required }}
          ```
          
          *Playbook:* {{ .Annotations.playbook }}
          {{ end }}
    email_configs:
      - to: 'jake@honeybadgerlabs.ai,finance-alerts@honeybadgerlabs.ai'
        from: 'notifications@honeybadgerlabs.ai'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'notifications@honeybadgerlabs.ai'
        auth_password: 'YOUR_APP_PASSWORD'
        headers:
          Subject: '[SN1MA] CRITICAL: {{ .GroupLabels.alertname }}'
  
  - name: 'slack-financial'
    slack_configs:
      - channel: '#sn1ma-financial-alerts'
        username: 'SN1MA Financial Monitor'
        icon_emoji: ':chart_with_upwards_trend:'
        title: '{{ if eq .Status "firing" }}⚠️{{ else }}✅{{ end }} {{ .GroupLabels.alertname }}'
        text: |
          {{ range .Alerts }}
          *Summary:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          *Action:* {{ .Annotations.action_required }}
          {{ end }}
  
  - name: 'slack-milestones'
    slack_configs:
      - channel: '#sn1ma-milestones'
        username: 'SN1MA Growth Tracker'
        icon_emoji: ':tada:'
        title: '🎉 {{ .GroupLabels.alertname }}'
        text: |
          {{ range .Alerts }}
          {{ .Annotations.summary }}
          
          {{ .Annotations.business_impact }}
          
          *Next Steps:*
          {{ .Annotations.action_required }}
          {{ end }}
```

---

## 5. SMS Alerts (Future - Twilio Integration)

For KILL-level alerts (Cost-to-Income > 25%), send SMS:

**Twilio Configuration:**

```python
# File: sustainnet-observability/shared/scripts/send_sms_alert.py

from twilio.rest import Client
import os

def send_critical_sms(alert_message: str):
    """Send SMS for KILL-level financial alerts"""
    
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    
    message = client.messages.create(
        body=f"🚨 SN1MA CRITICAL ALERT:\n\n{alert_message}\n\nCheck Grafana immediately.",
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to='+27XXXXXXXXXX'  # Your phone number
    )
    
    return message.sid
```

**Grafana Webhook Receiver:**

```yaml
Name: webhook-sms-critical
Type: Webhook
URL: https://your-webhook-handler.com/sms-alert
HTTP Method: POST
Body: |
  {
    "alert": "{{ .GroupLabels.alertname }}",
    "severity": "{{ .CommonLabels.severity }}",
    "summary": "{{ (index .Alerts 0).Annotations.summary }}",
    "action": "{{ .CommonLabels.action }}"
  }
```

---

## 6. Testing Notification Channels

### Test Slack Notification

```bash
# Send test alert to Slack
curl -X POST https://hooks.slack.com/services/YOUR_WEBHOOK_HERE \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "🧪 Test Alert from SN1MA Financial Monitor",
    "attachments": [
      {
        "color": "warning",
        "title": "Cost-to-Income Warning",
        "text": "This is a test notification. All systems are operational.",
        "fields": [
          {"title": "Severity", "value": "warning", "short": true},
          {"title": "Category", "value": "financial", "short": true}
        ]
      }
    ]
  }'
```

### Test Email Notification

In Grafana:
1. Go to **Alerting → Contact Points**
2. Find `email-sn1ma-financial`
3. Click **"Test"** button
4. Check email inbox

### Test Full Alert Flow

```bash
# Trigger a test alert by manually setting metric
# (In production, this would come from HRAIM automatically)

# Option 1: Use Grafana UI
# Go to Alerting → Alert Rules → Select rule → Click "Evaluate"

# Option 2: Manually trigger Prometheus alert
# Edit alerting-rules.yml to have very low threshold temporarily
# Then check Grafana Alerting page
```

---

## 7. Monitoring the Monitors (Meta-Monitoring)

### Alert on Missing Metrics

```yaml
- alert: MetricsNotReported
  expr: absent(sn1ma_revenue_monthly)
  for: 10m
  labels:
    severity: warning
    category: monitoring
  annotations:
    summary: "Financial metrics not being reported"
    description: "HRAIM /metrics endpoint is not exporting data"
    action_required: "Check if HRAIM backend is running on port 9001"
```

### Alert on Stale Data

```yaml
- alert: StaleFinancialData
  expr: time() - sn1ma_last_scrape_timestamp > 300
  for: 5m
  labels:
    severity: warning
    category: monitoring
  annotations:
    summary: "Financial metrics are stale"
    description: "Last successful scrape was > 5 minutes ago"
    action_required: "Check Prometheus scrape status"
```

---

## 8. Alert Fatigue Prevention

### Intelligent Grouping

- Group alerts by `category` and `guardrail` to avoid spam
- Use different repeat intervals based on severity:
  - **CRITICAL:** Every 1 hour
  - **WARNING:** Every 12 hours
  - **INFO:** Never repeat (one-time milestone)

### Silence Periods

Configure silences for:
- Maintenance windows
- Known test scenarios
- Month-end financial reconciliation (when metrics may fluctuate)

### Alert Dependencies

Don't alert on Cost-to-Income if revenue is zero (pre-revenue stage):

```yaml
- alert: CostToIncomeCRITICAL
  expr: sn1ma_cost_to_income_ratio > 20 and sn1ma_revenue_monthly > 0
  # Only fire if we have revenue
```

---

## Summary

**Notification Flow:**

```
Prometheus scrapes HRAIM /metrics
  ↓
Evaluates alerting-rules.yml every 30s
  ↓
Fires alert if threshold exceeded
  ↓
Sends to Grafana Alerting / Alertmanager
  ↓
Routes based on severity:
  - CRITICAL → Slack + Email (repeat every 1h)
  - WARNING → Slack only (repeat every 12h)
  - INFO → Slack once (never repeat)
  ↓
Team receives notification
  ↓
Takes action per playbook
```

**Next Steps:**

1. Create Slack webhook (5 min)
2. Configure Grafana contact points (10 min)
3. Set up notification policies (5 min)
4. Test all channels (10 min)
5. Document on-call procedures

**Total Setup Time:** ~30 minutes
