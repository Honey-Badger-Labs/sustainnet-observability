# SN1MA-MCP AI Governance Dashboard

**Purpose:** Board-level visibility into AI governance health and risk signals.

**Owner:** SustainNet Governance Board  
**Refresh:** Real-time (Prometheus → Grafana)  
**Access:** Board members, Founders, External Auditors

---

## Dashboard Sections

### A. AI Footprint

**Metrics:**
- Total AI-enabled decision pathways
- % Capped vs Uncapped payoff uses
- % High-stakes pathways (governance/ESG/regulatory)

**Visualization:** Pie chart + trend line

**Prometheus Queries:**
```promql
# Total AI requests
sum(rate(sn1ma_aim_requests_total[5m]))

# By DRAG mode
sum(rate(sn1ma_aim_requests_total[5m])) by (drag_mode)

# High-stakes indicator (derived from actor role)
sum(rate(sn1ma_aim_requests_total{actor_role=~"Founder|Governance.*"}[5m]))
```

---

### B. Accountability Health

**Metrics:**
- % AI uses with named Actor
- Actor churn rate (risk signal)
- Time-to-override metrics

**Alerts:**
- 🚨 Actor missing in >5% of requests → Immediate escalation
- ⚠️ Same Actor handling >80% of decisions → Dependency risk

**Prometheus Queries:**
```promql
# Actor presence rate
sum(sn1ma_aim_requests_total{actor_name!=""}) 
/ 
sum(sn1ma_aim_requests_total)

# Override latency (from human_action timestamp)
histogram_quantile(0.95, 
  rate(sn1ma_human_action_latency_seconds_bucket[5m])
)
```

---

### C. Dependency & Drift Signals

**Metrics:**
- AI recommendation follow-rate
- Override rate by team
- Silent adoption index (high use, low scrutiny)

**Alerts:**
- 🚨 Follow-rate >90% + override-rate <5% → Dependency drift
- ⚠️ DRAG mode violations detected → Governance breach

**Prometheus Queries:**
```promql
# Follow rate (accepted / total)
sum(rate(sn1ma_human_action_total{action_type="accepted"}[5m]))
/
sum(rate(sn1ma_human_action_total[5m]))

# Prescriptive language blocks (should be ~0)
sum(rate(sn1ma_prescriptive_language_blocks_total[5m]))
```

---

### D. Risk & Failure Signals

**Metrics:**
- Near-miss incidents logged
- Trigger reviews initiated
- Open governance actions
- AIM validation failures

**Alerts:**
- 🚨 AIM validation failure rate >1% → System misconfiguration
- 🚨 Incident logged → Board notification

**Prometheus Queries:**
```promql
# Validation failures
sum(rate(sn1ma_aim_validation_failures_total[5m])) by (failure_reason)

# Incidents (from audit log)
count(sn1ma_incident_total{severity=~"major|critical"})
```

---

### E. Trust Scorecard (Public-Linked)

**Metrics:**
- Governance transparency score (0-100)
- Incident recovery delta
- External audit status

**Public Visibility:** Yes (via sustainnet.app/trust)

**Calculation:**
```python
governance_score = (
    0.3 * aim_compliance_rate +
    0.3 * drag_enforcement_rate +
    0.2 * audit_log_completeness +
    0.1 * quarterly_review_adherence +
    0.1 * incident_disclosure_timeliness
) * 100
```

---

## Grafana Dashboard JSON

**File Location:** `/sustainnet-observability/products/sn1ma-mcp/governance-dashboard.json`

**Key Panels:**

```json
{
  "dashboard": {
    "title": "SN1MA AI Governance",
    "panels": [
      {
        "title": "AI Footprint",
        "type": "piechart",
        "targets": [
          {
            "expr": "sum(rate(sn1ma_aim_requests_total[5m])) by (drag_mode)"
          }
        ]
      },
      {
        "title": "Accountability Health",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(sn1ma_aim_requests_total{actor_name!=\"\"}) / sum(sn1ma_aim_requests_total)"
          }
        ],
        "thresholds": [
          { "value": 0.95, "color": "green" },
          { "value": 0.90, "color": "yellow" },
          { "value": 0, "color": "red" }
        ]
      },
      {
        "title": "Dependency Risk",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(sn1ma_human_action_total{action_type=\"accepted\"}[5m])) / sum(rate(sn1ma_human_action_total[5m]))",
            "legendFormat": "Follow Rate"
          },
          {
            "expr": "sum(rate(sn1ma_human_action_total{action_type=~\"modified|rejected\"}[5m])) / sum(rate(sn1ma_human_action_total[5m]))",
            "legendFormat": "Override Rate"
          }
        ],
        "alert": {
          "condition": "follow_rate > 0.90 AND override_rate < 0.05",
          "message": "Dependency drift detected - high follow rate with low overrides"
        }
      },
      {
        "title": "Trust Scorecard",
        "type": "gauge",
        "targets": [
          {
            "expr": "sn1ma_governance_score"
          }
        ],
        "min": 0,
        "max": 100,
        "thresholds": [
          { "value": 80, "color": "green" },
          { "value": 60, "color": "yellow" },
          { "value": 0, "color": "red" }
        ]
      }
    ]
  }
}
```

---

## Alert Rules

**File Location:** `/sustainnet-observability/shared/alerting/sn1ma-governance.yml`

```yaml
groups:
  - name: sn1ma_governance
    interval: 1m
    rules:
      - alert: AIMValidationFailureHigh
        expr: rate(sn1ma_aim_validation_failures_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
          component: governance
        annotations:
          summary: "AIM validation failure rate >1%"
          description: "{{ $value }} validation failures/sec - system misconfiguration likely"
      
      - alert: DependencyDrift
        expr: |
          (sum(rate(sn1ma_human_action_total{action_type="accepted"}[5m])) 
          / sum(rate(sn1ma_human_action_total[5m]))) > 0.90
          AND
          (sum(rate(sn1ma_human_action_total{action_type=~"modified|rejected"}[5m])) 
          / sum(rate(sn1ma_human_action_total[5m]))) < 0.05
        for: 15m
        labels:
          severity: warning
          component: governance
        annotations:
          summary: "AI dependency drift detected"
          description: "Follow rate {{ $value }}% with <5% override rate - governance review needed"
      
      - alert: IncidentLogged
        expr: increase(sn1ma_incident_total{severity=~"major|critical"}[5m]) > 0
        labels:
          severity: critical
          component: governance
        annotations:
          summary: "AI incident logged"
          description: "Board notification required immediately"
      
      - alert: ActorMissing
        expr: |
          (sum(sn1ma_aim_requests_total{actor_name=""}) 
          / sum(sn1ma_aim_requests_total)) > 0.05
        for: 5m
        labels:
          severity: critical
          component: governance
        annotations:
          summary: "Actor missing in >5% of requests"
          description: "AIM enforcement failure - immediate investigation required"
```

---

## Slack Integration

**Webhook:** `#sn1ma-governance` channel

**Trigger Events:**
- Any critical alert
- Incident logged
- Quarterly review due
- External audit scheduled

**Message Template:**
```json
{
  "text": "🚨 SN1MA Governance Alert",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Alert:* {{ alert.name }}\n*Severity:* {{ alert.severity }}\n*Description:* {{ alert.description }}"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": "View Dashboard",
          "url": "https://grafana.sustainnet.app/d/sn1ma-governance"
        },
        {
          "type": "button",
          "text": "Incident Playbook",
          "url": "https://github.com/Honey-Badger-Labs/sustainnet-vision/GOVERNANCE/AI_INCIDENT_PLAYBOOK.md"
        }
      ]
    }
  ]
}
```

---

## Quarterly Review Ritual

**When:** Every 90 days (automated calendar invite)

**Attendees:**
- Product Lead
- Engineering Lead
- Ethics/ESG Lead
- External Advisor (rotating)

**Pre-Meeting Prep:**
1. Export governance metrics (last 90 days)
2. Review override rate trends
3. Identify any near-miss incidents
4. Check AIM compliance rate

**Agenda (60-90 min):**
1. **Inventory Check** (15 min)
   - Where is AI used?
   - What decisions does it touch?

2. **Payoff Audit** (15 min)
   - Reclassify capped vs uncapped uses
   - Flag drift toward uncapped

3. **AIM Compliance** (15 min)
   - Actor named?
   - Inputs auditable?
   - Mission still valid?

4. **DRAG Boundary Check** (15 min)
   - Any AI performing Analysis or Decision-making?

5. **Failure & Abuse Scenarios** (15 min)
   - What happens if this output is wrong?
   - Who is harmed first?

6. **Action Log** (15 min)
   - Retire, constrain, or deepen AI use

**Output:** Updated governance action log + board summary

---

## Data Retention

**Audit Logs:** 2 years (compliance requirement)  
**Metrics:** 13 months (CloudWatch/Prometheus)  
**Dashboard Snapshots:** Quarterly (for trend analysis)

---

## Access Control

**Tier 1 (Public):**
- Trust Scorecard
- Incident disclosures

**Tier 2 (Internal):**
- Real-time metrics
- Override rates
- Dependency trends

**Tier 3 (Board + Auditors):**
- Full audit logs
- Actor-specific metrics
- Incident root cause analyses

---

*Last Updated: 30 January 2026*
