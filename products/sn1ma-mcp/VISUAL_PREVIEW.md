# Visual Preview: SN1MA Financial Monitoring

## 🎨 What It Will Look Like

---

## 1. Grafana Dashboard Preview

### Main Financial Health Dashboard

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  SN1MA-MCP: Financial Health Dashboard    Last updated: 2s ago  ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                   ┃
┃  ╔═══════════════╗  ╔══════════════════════════════════════════╗ ┃
┃  ║ 💰 Cost-to-   ║  ║  Revenue vs. Cost (Last 30 Days)         ║ ┃
┃  ║ Income Ratio  ║  ║                                          ║ ┃
┃  ║               ║  ║  R4,500 ┤                    ╭────────   ║ ┃
┃  ║      5.2%     ║  ║         │                ╭───╯ Revenue   ║ ┃
┃  ║               ║  ║  R3,000 ┤            ╭───╯               ║ ┃
┃  ║   ◉           ║  ║         │        ╭───╯                   ║ ┃
┃  ║  ╱ ╲          ║  ║  R1,500 ┤    ╭───╯                       ║ ┃
┃  ║ 0   10   20   ║  ║         │╭───╯ Cost (flat line)          ║ ┃
┃  ║   GREEN 🟢    ║  ║  R0     ┼────────────────────────────    ║ ┃
┃  ║               ║  ║         Jan 5   Jan 15   Jan 25   Feb 1  ║ ┃
┃  ╚═══════════════╝  ╚══════════════════════════════════════════╝ ┃
┃                                                                   ┃
┃  ╔═══════════╗  ╔═══════════╗  ╔══════════╗  ╔════════════════╗ ┃
┃  ║  Profit   ║  ║  Paying   ║  ║   MRR    ║  ║ Infrastructure ║ ┃
┃  ║  Margin   ║  ║ Customers ║  ║          ║  ║      Cost      ║ ┃
┃  ║           ║  ║           ║  ║          ║  ║                ║ ┃
┃  ║   94.8%   ║  ║     5     ║  ║ R4,500   ║  ║     R150       ║ ┃
┃  ║           ║  ║           ║  ║          ║  ║                ║ ┃
┃  ║  🟢 GREEN ║  ║  🟢 GREEN ║  ║ 🟢 GREEN ║  ║   🟢 GREEN     ║ ┃
┃  ╚═══════════╝  ╚═══════════╝  ╚══════════╝  ╚════════════════╝ ┃
┃                                                                   ┃
┃  ╔═════════════════════════════════════════════════════════════╗ ┃
┃  ║  Guardrails Status                                          ║ ┃
┃  ║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║ ┃
┃  ║  Rule                    Value      Threshold    Status     ║ ┃
┃  ║  ────────────────────────────────────────────────────────   ║ ┃
┃  ║  Cost-to-Income         5.2%         20%        ✅ OK       ║ ┃
┃  ║  Spending Cap           R150         R300       ✅ OK       ║ ┃
┃  ║  Payback Period         7.2 days     30 days    ✅ OK       ║ ┃
┃  ║  Profit Margin          94.8%        50%        ✅ OK       ║ ┃
┃  ╚═════════════════════════════════════════════════════════════╝ ┃
┃                                                                   ┃
┃  ╔═══════════════════════╗  ╔═══════════════════════════════╗   ┃
┃  ║ Revenue Growth (MoM)  ║  ║  Revenue by Tier              ║   ┃
┃  ║                       ║  ║                               ║   ┃
┃  ║  +67% │               ║  ║         ╱─────╲               ║   ┃
┃  ║       │         ╱─╲   ║  ║        │  Pro  │  60%        ║   ┃
┃  ║       │     ╱───╯  ╲  ║  ║        │ R2700 │             ║   ┃
┃  ║       │ ╱───╯       ╲ ║  ║         ╲─────╱              ║   ┃
┃  ║       ├───────────────║  ║        ╱───────╲             ║   ┃
┃  ║     Dec  Jan   Feb    ║  ║       │  Pro+  │  40%        ║   ┃
┃  ║                       ║  ║       │ R1800  │             ║   ┃
┃  ╚═══════════════════════╝  ║        ╲───────╱             ║   ┃
┃                             ╚═══════════════════════════════╝   ┃
┃                                                                   ┃
┃  ╔══════════════╗  ╔═════════╗  ╔══════╗  ╔════════════════╗   ┃
┃  ║  Payback     ║  ║  Churn  ║  ║ CAC  ║  ║  LTV:CAC Ratio ║   ┃
┃  ║   Period     ║  ║  Rate   ║  ║      ║  ║                ║   ┃
┃  ║              ║  ║         ║  ║      ║  ║       5.2      ║   ┃
┃  ║   7.2 days   ║  ║   2.1%  ║  ║ R245 ║  ║                ║   ┃
┃  ║   🟢 GREEN   ║  ║ 🟢 GREEN║  ║🟢 GRN║  ║    🟢 GREEN    ║   ┃
┃  ╚══════════════╝  ╚═════════╝  ╚══════╝  ╚════════════════╝   ┃
┃                                                                   ┃
┃  ╔═════════════════════════════════════════════════════════════╗ ┃
┃  ║  Financial Alerts (Last 7 Days)                             ║ ┃
┃  ║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║ ┃
┃  ║  Date        Alert                           Severity       ║ ┃
┃  ║  ────────────────────────────────────────────────────────   ║ ┃
┃  ║  Feb 1 9am   First Paying Customer          🎉 INFO        ║ ┃
┃  ║  Jan 30 2pm  Spending Cap Warning           ⚠️  WARNING    ║ ┃
┃  ║  Jan 28 11am Five Paying Customers          🎉 INFO        ║ ┃
┃  ╚═════════════════════════════════════════════════════════════╝ ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Color Key:**
- 🟢 **GREEN:** All good (0-10% for Cost-to-Income)
- 🟡 **YELLOW:** Warning (10-15%)
- 🟠 **ORANGE:** High alert (15-20%)
- 🔴 **RED:** Critical (>20%)

---

## 2. Slack Notification Examples

### Example 1: Cost-to-Income WARNING

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                              10:32 AM  ┃
┠─────────────────────────────────────────────────────────────────┨
┃                                                                  ┃
┃  📊 SN1MA Financial Monitor                               APP   ┃
┃                                                                  ┃
┃  ⚠️ WARNING: Cost-to-Income > 15%                               ┃
┃                                                                  ┃
┃  Alert: CostToIncomeWARNING                                     ┃
┃  Severity: warning                                              ┃
┃  Category: financial                                            ┃
┃                                                                  ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                  ┃
┃  Summary:                                                       ┃
┃  ⚠️ WARNING: Cost-to-Income > 15%                               ┃
┃                                                                  ┃
┃  Description:                                                   ┃
┃  Cost-to-Income ratio is 16.3% - ABOVE WARNING (15%).          ┃
┃  Target is < 10%.                                               ┃
┃                                                                  ┃
┃  Business Impact:                                               ┃
┃  Margins tightening - need to improve efficiency or             ┃
┃  increase revenue                                               ┃
┃                                                                  ┃
┃  Action Required:                                               ┃
┃  REVIEW ACTIONS:                                                ┃
┃  1. Analyze cost trends (is it rising?)                         ┃
┃  2. Review recent infrastructure changes                        ┃
┃  3. Check if revenue is growing as expected                     ┃
┃  4. Identify waste/unused resources                             ┃
┃                                                                  ┃
┃  Playbook: FINANCIAL_GUARDRAILS.md - Rule 1                     ┃
┃                                                                  ┃
┃  🔗 View Dashboard                                              ┃
┃                                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

### Example 2: Spending Cap EXCEEDED (CRITICAL)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                               3:15 PM  ┃
┠─────────────────────────────────────────────────────────────────┨
┃                                                                  ┃
┃  📊 SN1MA Financial Monitor                               APP   ┃
┃                                                                  ┃
┃  🚨 EXCEEDED: Spending cap breached                             ┃
┃                                                                  ┃
┃  Alert: SpendingCapEXCEEDED                                     ┃
┃  Severity: critical                                             ┃
┃  Category: financial                                            ┃
┃  Action: HALT_SPENDING                                          ┃
┃                                                                  ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                  ┃
┃  Summary:                                                       ┃
┃  🚨 EXCEEDED: Spending cap breached                             ┃
┃                                                                  ┃
┃  Description:                                                   ┃
┃  Infrastructure cost (R345) EXCEEDS spending cap (R300)         ┃
┃                                                                  ┃
┃  Business Impact:                                               ┃
┃  Over-budget - financial discipline violated                    ┃
┃                                                                  ┃
┃  Action Required:                                               ┃
┃  IMMEDIATE HALT:                                                ┃
┃  1. STOP all new infrastructure provisioning                    ┃
┃  2. Review what caused the overage                              ┃
┃  3. Identify services to scale down/pause                       ┃
┃  4. Get approval before ANY new spend                           ┃
┃  5. Update spending cap if revenue increased                    ┃
┃                                                                  ┃
┃  Playbook: FINANCIAL_GUARDRAILS.md - Rule 3                     ┃
┃                                                                  ┃
┃  🔗 View Dashboard                                              ┃
┃                                                                  ┃
┃  @jake @finance-team                                            ┃
┃                                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

### Example 3: KILL THRESHOLD - Cost-to-Income > 25%

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                               8:42 AM  ┃
┠─────────────────────────────────────────────────────────────────┨
┃                                                                  ┃
┃  📊 SN1MA Financial Monitor                               APP   ┃
┃                                                                  ┃
┃  🚨 KILL THRESHOLD: Cost-to-Income > 25%                        ┃
┃                                                                  ┃
┃  Alert: CostToIncomeKILL                                        ┃
┃  Severity: critical                                             ┃
┃  Category: financial                                            ┃
┃  Guardrail: rule_1                                              ┃
┃  Action: KILL_IMMEDIATELY                                       ┃
┃                                                                  ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                  ┃
┃  Summary:                                                       ┃
┃  🚨 KILL THRESHOLD: Cost-to-Income > 25%                        ┃
┃                                                                  ┃
┃  Description:                                                   ┃
┃  Cost-to-Income ratio is 27.8% - ABOVE KILL THRESHOLD (25%).   ┃
┃  IMMEDIATE ACTION REQUIRED.                                     ┃
┃                                                                  ┃
┃  Business Impact:                                               ┃
┃  Unsustainable burn rate - company will run out of money        ┃
┃                                                                  ┃
┃  Action Required:                                               ┃
┃  EMERGENCY PROCEDURE (Execute < 24 hours):                      ┃
┃  1. HALT all new infrastructure spending                        ┃
┃  2. Scale down to FREE tier (Fly.io + Upstash)                  ┃
┃  3. Cancel all paid services                                    ┃
┃  4. Notify founders immediately                                 ┃
┃  5. Review FINANCIAL_GUARDRAILS.md Emergency Cut section        ┃
┃                                                                  ┃
┃  Playbook: See FINANCIAL_GUARDRAILS.md - Rule 1, Section 10     ┃
┃  (Emergency Cut)                                                ┃
┃                                                                  ┃
┃  🔗 View Dashboard                                              ┃
┃                                                                  ┃
┃  @channel @jake @founders EMERGENCY ALERT                       ┃
┃                                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

### Example 4: Milestone Alert - First Paying Customer 🎉

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-milestones                                    11:23 AM  ┃
┠─────────────────────────────────────────────────────────────────┨
┃                                                                  ┃
┃  📊 SN1MA Growth Tracker                                  APP   ┃
┃                                                                  ┃
┃  🎉 MILESTONE: First Paying Customer!                           ┃
┃                                                                  ┃
┃  Alert: FirstPayingCustomer                                     ┃
┃  Severity: info                                                 ┃
┃  Category: milestone                                            ┃
┃                                                                  ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                  ┃
┃  🎉 MILESTONE: First Paying Customer!                           ┃
┃                                                                  ┃
┃  SN1MA-MCP just acquired its first paying customer              ┃
┃                                                                  ┃
┃  Business Impact:                                               ┃
┃  Product-market fit validation - begin scaling operations       ┃
┃                                                                  ┃
┃  Next Steps:                                                    ┃
┃  CELEBRATION + ACTION:                                          ┃
┃  1. Celebrate the win! 🎊                                       ┃
┃  2. Update spending cap to R150/month (1-4 customers)           ┃
┃  3. Begin light production infrastructure (Option 2)            ┃
┃  4. Focus on customer success and retention                     ┃
┃  5. Document what worked to acquire this customer               ┃
┃                                                                  ┃
┃  🔗 View Dashboard                                              ┃
┃                                                                  ┃
┃  🎊 🎉 🎈 Congrats team! 🎈 🎉 🎊                                ┃
┃                                                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 3. Email Notification Example

```
From: SN1MA Financial Monitor <notifications@honeybadgerlabs.ai>
To: jake@honeybadgerlabs.ai, finance-alerts@honeybadgerlabs.ai
Subject: [SN1MA] CRITICAL: Cost-to-Income > 20%
Date: Sat, 1 Feb 2026 14:37:12 +0200

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Financial Guardrail Alert
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Alert Name: CostToIncomeCRITICAL
Severity: critical
Category: financial
Guardrail: rule_1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
🔴 CRITICAL: Cost-to-Income > 20%

Description:
Cost-to-Income ratio is 22.3% - ABOVE TARGET (20%). 
Approaching KILL threshold (25%).

Business Impact:
Financial health deteriorating - risk of unsustainable operations

Action Required:
IMMEDIATE ACTIONS:
1. Review infrastructure costs (Fly.io, Upstash, Datadog)
2. Identify cost optimization opportunities
3. Pause non-essential features/services
4. Schedule emergency financial review meeting
5. Prepare contingency plan to scale down

Playbook Reference:
FINANCIAL_GUARDRAILS.md - Rule 1

Dashboard: https://grafana.sustainnet.ai/d/sn1ma-financial-health

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated alert from SN1MA Financial Monitoring.
Reply STOP to unsubscribe | Configure alerts: grafana.sustainnet.ai
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 4. Prometheus Alert State Timeline

```
Prometheus Alert State Flow:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Time: 10:00 AM
State: Inactive
Reason: Cost-to-Income ratio is 8.2% (below 20% threshold)
Display: Alert rule loaded but not triggered
Color: ⚪ Gray

Time: 10:32 AM
Event: Infrastructure cost increased to R350
State: Pending
Reason: Cost-to-Income now 21.5% (above 20%), waiting 5 minutes
Display: ⏱️ Pending (3/5 minutes elapsed)
Color: 🟡 Yellow

Time: 10:37 AM (5 minutes later)
State: Firing
Reason: Cost-to-Income still 21.5%, exceeded 'for: 5m' duration
Display: 🔴 Firing - Alert sent to Slack + Email
Color: 🔴 Red
Action: Notification sent via Slack and Email

Time: 10:45 AM
Event: Scaled down infrastructure, cost now R280
State: Resolved
Reason: Cost-to-Income now 17.2% (below 20% threshold)
Display: ✅ Resolved - Alert cleared
Color: 🟢 Green
Action: "Resolved" notification sent to Slack
```

---

## 5. What You'll See in Prometheus UI

### Alerts Page (http://localhost:9090/alerts)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Prometheus Alerts                                      9090     ┃
┠────────────────────────────────────────────────────────────────────┨
┃                                                                    ┃
┃  Group: sn1ma_financial_guardrails                                ┃
┃  File: /etc/prometheus/alerting-rules.yml                         ┃
┃  Interval: 1m                                                     ┃
┃                                                                    ┃
┃  ┌─────────────────────────────────────────────────────────────┐  ┃
┃  │ CostToIncomeKILL                                      Inactive│  ┃
┃  │ expr: sn1ma_cost_to_income_ratio > 25                        │  ┃
┃  │ for: 1m                                                      │  ┃
┃  │ Severity: critical | Category: financial                    │  ┃
┃  └─────────────────────────────────────────────────────────────┘  ┃
┃                                                                    ┃
┃  ┌─────────────────────────────────────────────────────────────┐  ┃
┃  │ CostToIncomeCRITICAL                                   Pending│  ┃
┃  │ expr: sn1ma_cost_to_income_ratio > 20                        │  ┃
┃  │ for: 5m (3m elapsed)                                         │  ┃
┃  │ Severity: critical | Category: financial                    │  ┃
┃  │ Active since: 2m ago                                         │  ┃
┃  │ Query result: 21.5                                           │  ┃
┃  └─────────────────────────────────────────────────────────────┘  ┃
┃                                                                    ┃
┃  ┌─────────────────────────────────────────────────────────────┐  ┃
┃  │ SpendingCapEXCEEDED                                     Firing│  ┃
┃  │ expr: sn1ma_infrastructure_cost_monthly > sn1ma_spending_cap │  ┃
┃  │ for: 1m                                                      │  ┃
┃  │ Severity: critical | Category: financial                    │  ┃
┃  │ Active since: 12m ago                                        │  ┃
┃  │ Query result: cost=350, cap=300                              │  ┃
┃  │ Labels: {alertname="SpendingCapEXCEEDED", ...}               │  ┃
┃  │ Annotations: summary="🚨 EXCEEDED: Spending cap breached"    │  ┃
┃  └─────────────────────────────────────────────────────────────┘  ┃
┃                                                                    ┃
┃  ┌─────────────────────────────────────────────────────────────┐  ┃
┃  │ FirstPayingCustomer                                    Firing│  ┃
┃  │ expr: sn1ma_paying_customers_total == 1                      │  ┃
┃  │ for: 1m                                                      │  ┃
┃  │ Severity: info | Category: milestone                        │  ┃
┃  │ Active since: 2h ago                                         │  ┃
┃  │ Query result: 1.0                                            │  ┃
┃  └─────────────────────────────────────────────────────────────┘  ┃
┃                                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 6. What Happens When Alert Fires

### Timeline of Events:

```
Step 1: Metric Change
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:30:00 AM - Infrastructure cost increases
              HRAIM /metrics endpoint reports: sn1ma_infrastructure_cost_monthly = 350

Step 2: Prometheus Scrapes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:30:15 AM - Prometheus scrapes HRAIM (every 30s interval)
              Metric stored: sn1ma_infrastructure_cost_monthly{job="sn1ma-mcp-hraim"} = 350

Step 3: Alert Evaluation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:30:30 AM - Prometheus evaluates alert rules (every 30s)
              Rule: SpendingCapEXCEEDED
              Condition: sn1ma_infrastructure_cost_monthly > sn1ma_spending_cap
              Result: 350 > 300 = TRUE
              Alert State: PENDING (waiting for 'for: 1m' duration)

Step 4: Wait Period
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:30:30 - 10:31:30 - Alert stays in PENDING state
                      Condition re-evaluated every 30s to confirm
                      Still TRUE at each check

Step 5: Alert Fires
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:31:30 AM - 'for: 1m' duration elapsed, condition still TRUE
              Alert State changes: PENDING → FIRING
              Prometheus sends alert to Alertmanager/Grafana

Step 6: Notification Routing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:31:31 AM - Grafana receives alert
              Matches label: severity=critical
              Routes to contact points:
                - slack-sn1ma-financial
                - email-sn1ma-financial

Step 7: Slack Notification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:31:32 AM - Slack webhook called
              Message posted to #sn1ma-financial-alerts
              Contains: Summary, Description, Business Impact, Action Required

Step 8: Email Notification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10:31:33 AM - Email sent via SMTP
              To: jake@honeybadgerlabs.ai, finance-alerts@honeybadgerlabs.ai
              Subject: [SN1MA] CRITICAL: Spending cap breached

Step 9: Repeat Notifications (if still firing)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11:31:32 AM - 1 hour later (repeat_interval: 1h for critical)
              Alert still firing, send reminder notification
              Slack + Email sent again

Step 10: Resolution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11:45:00 AM - Infrastructure cost reduced to R280
              Condition: 280 > 300 = FALSE
              Alert State: FIRING → Resolved
              "Resolved" notification sent to Slack/Email
```

---

## 7. Mobile View (Grafana Mobile App)

```
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃  SN1MA Financial      ┃
┃  Health Dashboard     ┃
┠───────────────────────┨
┃                       ┃
┃  ╔═══════════════════╗┃
┃  ║ Cost-to-Income    ║┃
┃  ║                   ║┃
┃  ║     5.2%          ║┃
┃  ║                   ║┃
┃  ║    🟢 OK          ║┃
┃  ╚═══════════════════╝┃
┃                       ┃
┃  ╔═════════╦═════════╗┃
┃  ║ Revenue ║  Cost   ║┃
┃  ║         ║         ║┃
┃  ║ R4,500  ║  R150   ║┃
┃  ║ 🟢 OK   ║ 🟢 OK   ║┃
┃  ╚═════════╩═════════╝┃
┃                       ┃
┃  ╔═══════════════════╗┃
┃  ║ Paying Customers  ║┃
┃  ║                   ║┃
┃  ║       5           ║┃
┃  ║                   ║┃
┃  ║    🟢 OK          ║┃
┃  ╚═══════════════════╝┃
┃                       ┃
┃  [View More Metrics]  ┃
┃                       ┃
┃  ━━━━━━━━━━━━━━━━━━  ┃
┃  Recent Alerts        ┃
┃  ━━━━━━━━━━━━━━━━━━  ┃
┃                       ┃
┃  🎉 First Customer    ┃
┃  Today, 11:23 AM      ┃
┃                       ┃
┃  ⚠️ Cap Warning       ┃
┃  Yesterday, 2:15 PM   ┃
┃                       ┃
┗━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Summary

**What you'll see after deployment:**

✅ **Grafana Dashboard** - 16 panels showing real-time financial health
✅ **Slack Notifications** - Immediate alerts for threshold violations
✅ **Email Alerts** - Formal audit trail of all financial events
✅ **Prometheus UI** - Raw metrics and alert state tracking
✅ **Mobile Access** - Check financial health on-the-go

**Alert Frequency:**
- **CRITICAL:** Repeat every 1 hour while active
- **WARNING:** Repeat every 12 hours while active
- **INFO:** One-time notification (milestones)

**Response Time:**
- Metric change → Alert fires: ~1-2 minutes
- Alert fires → Slack notification: ~1 second
- Alert fires → Email notification: ~5 seconds

**Cost:**
- **Local:** R0 (runs on your machine)
- **Grafana Cloud:** R0 (free tier, perfect for start)
- **Fly.io:** R0 (free tier for Prometheus + Grafana)

🚀 **Ready to deploy and monitor your financial health in real-time!**
