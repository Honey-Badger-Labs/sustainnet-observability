# 🎨 Alert Visualization Gallery

**Real examples of what you'll see when alerts fire**

---

## Scenario 1: Everything Healthy ✅

**No alerts, dashboard looks like this:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                              ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                        ┃
┃  All quiet. No financial alerts in the last 24 hours. ┃
┃  💚 All guardrails are GREEN                          ┃
┃                                                        ┃
┃  Last check: 2 minutes ago                            ┃
┃                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Dashboard shows all green:**
- Cost-to-Income: 5.2% 🟢
- Spending Cap: 50% utilized 🟢
- Payback Period: 7 days 🟢
- Profit Margin: 94.8% 🟢

---

## Scenario 2: First Paying Customer 🎉

**When `sn1ma_paying_customers_total` goes from 0 → 1:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-milestones                                  11:23 AM   ┃
┠────────────────────────────────────────────────────────────────┨
┃                                                                 ┃
┃  📊 SN1MA Growth Tracker                                  BOT  ┃
┃                                                                 ┃
┃  🎉 🎊 MILESTONE: First Paying Customer! 🎊 🎉                  ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Summary:*                                                     ┃
┃  SN1MA-MCP just acquired its first paying customer!            ┃
┃                                                                 ┃
┃  *Business Impact:*                                             ┃
┃  Product-market fit validation - begin scaling operations      ┃
┃                                                                 ┃
┃  *Next Steps - CELEBRATION + ACTION:*                           ┃
┃  1. 🎊 Celebrate the win!                                       ┃
┃  2. 💰 Update spending cap to R150/month (1-4 customers)        ┃
┃  3. 🚀 Begin light production infrastructure (Option 2)         ┃
┃  4. 🤝 Focus on customer success and retention                  ┃
┃  5. 📝 Document what worked to acquire this customer            ┃
┃                                                                 ┃
┃  📊 View Dashboard                                              ┃
┃  https://grafana.sustainnet.ai/d/sn1ma-financial-health        ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  @jake @team Congrats on the first customer! 🎈                ┃
┃                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Scenario 3: Approaching Spending Cap ⚠️

**When infrastructure cost reaches 85% of cap:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                             2:15 PM   ┃
┠────────────────────────────────────────────────────────────────┨
┃                                                                 ┃
┃  📊 SN1MA Financial Monitor                               BOT  ┃
┃                                                                 ┃
┃  ⚠️ WARNING: Approaching spending cap (85%)                    ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Alert:* SpendingCapWARNING                                    ┃
┃  *Severity:* ⚠️ warning                                         ┃
┃  *Category:* financial                                          ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Summary:*                                                     ┃
┃  Infrastructure cost (R255) at 85% of cap (R300)               ┃
┃                                                                 ┃
┃  *Description:*                                                 ┃
┃  Nearing budget limit - need to monitor closely                ┃
┃                                                                 ┃
┃  *Business Impact:*                                             ┃
┃  Risk of exceeding budget if costs continue rising             ┃
┃                                                                 ┃
┃  *Action Required:*                                             ┃
┃  PROACTIVE ACTIONS:                                             ┃
┃  1. Review projected month-end spend                            ┃
┃  2. Identify any unexpected cost increases                      ┃
┃  3. Prepare to optimize if approaching limit                    ┃
┃  4. Check if revenue growth justifies higher cap                ┃
┃                                                                 ┃
┃  *Playbook:* FINANCIAL_GUARDRAILS.md - Rule 3                   ┃
┃                                                                 ┃
┃  📊 View Dashboard                                              ┃
┃  https://grafana.sustainnet.ai/d/sn1ma-financial-health        ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  Current Metrics:                                               ┃
┃  • Infrastructure Cost: R255/month                              ┃
┃  • Spending Cap: R300/month                                     ┃
┃  • Utilization: 85%                                             ┃
┃  • Revenue: R4,500/month                                        ┃
┃  • Paying Customers: 5                                          ┃
┃                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Scenario 4: Spending Cap EXCEEDED 🔴

**When infrastructure cost exceeds the cap:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                             3:42 PM   ┃
┠────────────────────────────────────────────────────────────────┨
┃                                                                 ┃
┃  📊 SN1MA Financial Monitor                               BOT  ┃
┃                                                                 ┃
┃  🚨 CRITICAL: Spending cap EXCEEDED                            ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Alert:* SpendingCapEXCEEDED                                   ┃
┃  *Severity:* 🔴 critical                                        ┃
┃  *Category:* financial                                          ┃
┃  *Action:* HALT_SPENDING                                        ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Summary:*                                                     ┃
┃  🚨 Infrastructure cost (R345) EXCEEDS spending cap (R300)     ┃
┃                                                                 ┃
┃  *Description:*                                                 ┃
┃  Over-budget - financial discipline violated                    ┃
┃                                                                 ┃
┃  *Business Impact:*                                             ┃
┃  Operating beyond approved budget. Cash flow risk if unchecked. ┃
┃                                                                 ┃
┃  *Action Required - IMMEDIATE HALT:*                            ┃
┃  1. 🛑 STOP all new infrastructure provisioning                 ┃
┃  2. 🔍 Review what caused the overage                           ┃
┃  3. 📉 Identify services to scale down/pause                    ┃
┃  4. ✋ Get approval before ANY new spend                        ┃
┃  5. 📊 Update spending cap if revenue increased                 ┃
┃                                                                 ┃
┃  *Playbook:* FINANCIAL_GUARDRAILS.md - Rule 3                   ┃
┃                                                                 ┃
┃  📊 View Dashboard                                              ┃
┃  https://grafana.sustainnet.ai/d/sn1ma-financial-health        ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  ⚠️ Overage Details:                                            ┃
┃  • Infrastructure Cost: R345/month (+15% over cap)              ┃
┃  • Spending Cap: R300/month                                     ┃
┃  • Revenue: R4,500/month                                        ┃
┃  • Cost-to-Income: 7.7% (still healthy)                         ┃
┃                                                                 ┃
┃  Possible causes:                                               ┃
┃  • Fly.io auto-scaled due to traffic spike?                     ┃
┃  • Upstash Redis exceeded free tier?                            ┃
┃  • Datadog monitoring enabled?                                  ┃
┃                                                                 ┃
┃  @jake @finance-team Immediate attention required               ┃
┃                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Plus email sent to:**
- jake@honeybadgerlabs.ai
- finance-alerts@honeybadgerlabs.ai

---

## Scenario 5: Cost-to-Income CRITICAL 🚨

**When Cost-to-Income ratio exceeds 20%:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                             8:17 AM   ┃
┠────────────────────────────────────────────────────────────────┨
┃                                                                 ┃
┃  📊 SN1MA Financial Monitor                               BOT  ┃
┃                                                                 ┃
┃  🔴 CRITICAL: Cost-to-Income > 20%                             ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Alert:* CostToIncomeCRITICAL                                  ┃
┃  *Severity:* 🔴 critical                                        ┃
┃  *Category:* financial                                          ┃
┃  *Guardrail:* rule_1                                            ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Summary:*                                                     ┃
┃  🔴 Cost-to-Income ratio is 22.3% - ABOVE TARGET (20%)         ┃
┃  ⚠️ Approaching KILL threshold (25%)                            ┃
┃                                                                 ┃
┃  *Description:*                                                 ┃
┃  Financial health deteriorating - risk of unsustainable ops    ┃
┃                                                                 ┃
┃  *Business Impact:*                                             ┃
┃  If this trend continues, we'll hit KILL threshold (25%)        ┃
┃  which triggers emergency scale-down within 24 hours.           ┃
┃                                                                 ┃
┃  *Action Required - IMMEDIATE:*                                 ┃
┃  1. 🔍 Review infrastructure costs (Fly.io, Upstash, Datadog)   ┃
┃  2. 💡 Identify cost optimization opportunities                 ┃
┃  3. ⏸️ Pause non-essential features/services                    ┃
┃  4. 📅 Schedule emergency financial review meeting              ┃
┃  5. 📋 Prepare contingency plan to scale down                   ┃
┃                                                                 ┃
┃  *Playbook:* FINANCIAL_GUARDRAILS.md - Rule 1                   ┃
┃                                                                 ┃
┃  📊 View Dashboard                                              ┃
┃  https://grafana.sustainnet.ai/d/sn1ma-financial-health        ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  📈 Financial Snapshot:                                         ┃
┃  • Revenue: R1,800/month (2 Pro customers)                      ┃
┃  • Infrastructure Cost: R400/month                              ┃
┃  • Cost-to-Income: 22.3%                                        ┃
┃  • Profit Margin: 77.7%                                         ┃
┃  • Spending Cap: R150/month (VIOLATED by R250)                  ┃
┃                                                                 ┃
┃  ⚠️ WARNING: Multiple guardrails violated!                      ┃
┃  • Cost-to-Income: 22.3% (target < 10%, critical > 20%)         ┃
┃  • Spending Cap: R400 vs R150 cap (267% over!)                  ┃
┃                                                                 ┃
┃  🎯 Recovery Options:                                           ┃
┃  Option A: Scale down to R150 infra → 8.3% Cost-to-Income ✅    ┃
┃  Option B: Grow to 5 customers (R4,500 rev) → 8.9% ratio ✅     ┃
┃  Option C: Do nothing → Hit KILL threshold in ~10 days ❌       ┃
┃                                                                 ┃
┃  @jake @founders CRITICAL - Meeting required today              ┃
┃                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Email sent with same content + PDF attachment of current dashboard state**

---

## Scenario 6: KILL THRESHOLD - Emergency Cut Required 🚨🚨🚨

**When Cost-to-Income exceeds 25%:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                            10:42 AM   ┃
┠────────────────────────────────────────────────────────────────┨
┃                                                                 ┃
┃  📊 SN1MA Financial Monitor                               BOT  ┃
┃                                                                 ┃
┃  🚨🚨🚨 KILL THRESHOLD: Cost-to-Income > 25% 🚨🚨🚨             ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Alert:* CostToIncomeKILL                                      ┃
┃  *Severity:* 🚨 critical                                        ┃
┃  *Category:* financial                                          ┃
┃  *Guardrail:* rule_1                                            ┃
┃  *Action:* KILL_IMMEDIATELY                                     ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Summary:*                                                     ┃
┃  🚨 Cost-to-Income ratio is 27.8%                               ┃
┃  🚨 ABOVE KILL THRESHOLD (25%)                                  ┃
┃  🚨 IMMEDIATE ACTION REQUIRED                                   ┃
┃                                                                 ┃
┃  *Description:*                                                 ┃
┃  Unsustainable burn rate - company will run out of money        ┃
┃                                                                 ┃
┃  *Business Impact:*                                             ┃
┃  At current burn rate:                                          ┃
┃  • Losing R500/month                                            ┃
┃  • Runway: ~2 months (if R1,000 test budget)                    ┃
┃  • Operating beyond affordable loss limits                      ┃
┃                                                                 ┃
┃  *Action Required - EMERGENCY PROCEDURE:*                       ┃
┃  ⏰ Execute within < 24 hours:                                   ┃
┃                                                                 ┃
┃  1. 🛑 HALT all new infrastructure spending                     ┃
┃  2. 📉 Scale down to FREE tier (Fly.io + Upstash)               ┃
┃  3. ❌ Cancel all paid services                                 ┃
┃  4. 📞 Notify founders immediately                              ┃
┃  5. 📖 Review FINANCIAL_GUARDRAILS.md Emergency Cut section     ┃
┃                                                                 ┃
┃  *Playbook:*                                                    ┃
┃  FINANCIAL_GUARDRAILS.md - Rule 1, Section 10 (Emergency Cut)   ┃
┃                                                                 ┃
┃  📊 View Dashboard                                              ┃
┃  https://grafana.sustainnet.ai/d/sn1ma-financial-health        ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  📉 Current Financial State:                                    ┃
┃  • Revenue: R1,800/month (2 Pro customers)                      ┃
┃  • Infrastructure Cost: R500/month                              ┃
┃  • Monthly Loss: -R500/month                                    ┃
┃  • Cost-to-Income: 27.8% 🚨                                     ┃
┃  • Profit Margin: 72.2%                                         ┃
┃                                                                 ┃
┃  🎯 Emergency Cut Plan (Execute Today):                         ┃
┃                                                                 ┃
┃  STEP 1: Scale Fly.io to FREE tier                              ┃
┃  Command: `fly scale count 0 --app sn1ma-hraim`                 ┃
┃  Savings: R400/month                                            ┃
┃                                                                 ┃
┃  STEP 2: Downgrade Upstash Redis to FREE                        ┃
┃  Action: Log in to Upstash → Change plan                        ┃
┃  Savings: R100/month                                            ┃
┃                                                                 ┃
┃  STEP 3: Pause Datadog (if enabled)                             ┃
┃  Savings: R0 (already free/not enabled)                         ┃
┃                                                                 ┃
┃  TOTAL SAVINGS: R500/month                                      ┃
┃  NEW COST: R0/month                                             ┃
┃  NEW COST-TO-INCOME: 0% ✅                                      ┃
┃                                                                 ┃
┃  ⚠️ Impact on Service:                                          ┃
┃  • API will be slower (free tier limits)                        ┃
┃  • No auto-scaling (fixed capacity)                             ┃
┃  • Redis cache smaller (1GB → 500MB)                            ┃
┃  • BUT: Service stays online, customers unaffected              ┃
┃                                                                 ┃
┃  📅 Review Date: Tomorrow 10 AM                                 ┃
┃  👥 Required: @jake @founders @finance-team                     ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  @channel @here EMERGENCY - KILL THRESHOLD REACHED              ┃
┃  📞 Call Jake immediately: +27 XXX XXX XXXX                     ┃
┃                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**PLUS:**
- Email sent to ALL stakeholders
- SMS sent to Jake's phone (if configured)
- PagerDuty incident created (if configured)
- Dashboard turns RED across all panels
- Automatic runbook link sent

---

## Scenario 7: Alert Resolved ✅

**When issue is fixed and alert clears:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  #sn1ma-financial-alerts                             4:23 PM   ┃
┠────────────────────────────────────────────────────────────────┨
┃                                                                 ┃
┃  📊 SN1MA Financial Monitor                               BOT  ┃
┃                                                                 ┃
┃  ✅ RESOLVED: Cost-to-Income back to healthy levels            ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Alert:* CostToIncomeCRITICAL                                  ┃
┃  *Previous State:* 🔴 Firing                                    ┃
┃  *New State:* ✅ Resolved                                       ┃
┃  *Duration:* 6 hours 11 minutes                                 ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  *Summary:*                                                     ┃
┃  Cost-to-Income ratio decreased from 22.3% → 8.3%              ┃
┃  Now below target threshold (20%)                               ┃
┃                                                                 ┃
┃  *What Changed:*                                                ┃
┃  • Infrastructure scaled down from R400 → R150                  ┃
┃  • Cost-to-Income improved from 22.3% → 8.3%                    ┃
┃  • Spending cap compliance restored                             ┃
┃                                                                 ┃
┃  *Current Status:*                                              ┃
┃  • Revenue: R1,800/month                                        ┃
┃  • Cost: R150/month                                             ┃
┃  • Profit: R1,650/month                                         ┃
┃  • Margin: 91.7% ✅                                             ┃
┃                                                                 ┃
┃  All financial guardrails: 🟢 GREEN                            ┃
┃                                                                 ┃
┃  📊 View Dashboard                                              ┃
┃  https://grafana.sustainnet.ai/d/sn1ma-financial-health        ┃
┃                                                                 ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                 ┃
┃  Great work team! 💚                                            ┃
┃                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Summary: Alert Severity Levels

| Level | Color | Slack Channel | Email | Repeat | Example |
|-------|-------|---------------|-------|--------|---------|
| **INFO** 🎉 | Blue | #sn1ma-milestones | ❌ | Never | First customer |
| **WARNING** ⚠️ | Yellow | #sn1ma-financial-alerts | ❌ | 12h | Cost-to-Income > 15% |
| **CRITICAL** 🔴 | Red | #sn1ma-financial-alerts | ✅ | 1h | Cost-to-Income > 20% |
| **KILL** 🚨 | Red | #sn1ma-financial-alerts + @channel | ✅ + SMS | 30min | Cost-to-Income > 25% |

---

**What happens when you see these alerts:**

1. **Check dashboard** immediately (link in alert)
2. **Read business impact** section
3. **Follow action required** steps
4. **Refer to playbook** for detailed procedures
5. **Document actions taken** in Slack thread
6. **Monitor until resolved**

🚀 **You're now ready to monitor SN1MA's financial health in real-time!**
