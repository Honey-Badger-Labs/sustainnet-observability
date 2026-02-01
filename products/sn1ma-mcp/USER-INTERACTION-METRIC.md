# SN1MA-MCP: Days Since Last Real User Interaction

**Purpose:** Track the most critical metric for product-market fit: when did a real user last interact with SN1MA?

**Baseline:** February 1, 2026 (0 real users, metric = ∞)

---

## Metric Definition

### Primary Metric: `days_since_last_real_user_interaction`

**What counts as "real user interaction":**
- ✅ User signs up with email (authenticated)
- ✅ User logs into their account (session created)
- ✅ User runs `/coach` endpoint with real AIM declaration
- ✅ User runs an agent (Well-Architected, SRE, FinOps, etc.)
- ✅ User views coaching output / makes a decision
- ✅ User exports recommendations or shares feedback

**What does NOT count:**
- ❌ Demo by creator (that's us)
- ❌ Internal testing
- ❌ Automated test scripts
- ❌ Curl requests from terminal
- ❌ Single-page visits to landing page

---

## Current State

| Metric | Value | Status |
|--------|-------|--------|
| Days since first signup | ∞ | 🔴 No users yet |
| Days since first login | ∞ | 🔴 No users yet |
| Days since first /coach call | ∞ | 🔴 No users yet |
| Days since first agent execution | ∞ | 🔴 No users yet |
| Monthly active users | 0 | 🔴 Target: 50 |
| Daily active users | 0 | 🔴 Target: 10 |

---

## How to Track

### 1. Database Table (PostgreSQL)

Add to `HRAIM/schema/01-canonical-memory.sql`:

```sql
CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    interaction_type VARCHAR(50) NOT NULL, -- 'signup', 'login', 'coach_call', 'agent_run', 'decision'
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_timestamp ON user_interactions(timestamp DESC);
CREATE INDEX idx_user_interactions_type ON user_interactions(interaction_type);

-- Calculate days since last interaction
CREATE VIEW metric_days_since_last_interaction AS
SELECT 
    EXTRACT(EPOCH FROM (NOW() - MAX(timestamp))) / 86400 as days_since_last_interaction,
    MAX(timestamp) as last_interaction_at,
    COUNT(DISTINCT user_id) as total_users
FROM user_interactions
WHERE interaction_type IN ('signup', 'login', 'coach_call', 'agent_run', 'decision');
```

### 2. API Endpoint to Record Interaction

Add to `src/mcp_server/main.py`:

```python
@app.post("/metrics/interaction")
async def record_user_interaction(
    user_id: str,
    interaction_type: str,
    metadata: dict = None
):
    """Record a real user interaction"""
    async with get_db() as conn:
        await conn.execute("""
            INSERT INTO user_interactions (user_id, interaction_type, metadata)
            VALUES ($1, $2, $3)
        """, user_id, interaction_type, metadata or {})
    return {"status": "recorded"}

@app.get("/metrics/days-since-last-interaction")
async def get_days_since_last_interaction():
    """Get primary metric: days since last real user interaction"""
    async with get_db() as conn:
        result = await conn.fetchrow("""
            SELECT 
                EXTRACT(EPOCH FROM (NOW() - MAX(timestamp))) / 86400 as days,
                MAX(timestamp) as last_at,
                COUNT(DISTINCT user_id) as users
            FROM user_interactions
            WHERE interaction_type IN ('signup', 'login', 'coach_call', 'agent_run', 'decision')
        """)
    
    if result['last_at'] is None:
        return {
            "metric": "days_since_last_real_user_interaction",
            "value": None,
            "status": "no_users_yet",
            "target": 0,
            "last_interaction": None,
            "total_users": 0
        }
    
    return {
        "metric": "days_since_last_real_user_interaction",
        "value": float(result['days']),
        "status": "active" if result['days'] < 1 else "warning" if result['days'] < 7 else "critical",
        "target": 0,
        "last_interaction": result['last_at'].isoformat(),
        "total_users": result['users']
    }
```

### 3. Call Recording Endpoint from Key Flows

In `src/mcp_server/auth.py` (or wherever you handle auth):

```python
async def on_user_login(user_id: str):
    """Track login"""
    await record_interaction(user_id, "login", {"ip": request.client.host})

async def on_user_signup(user_id: str, email: str):
    """Track signup"""
    await record_interaction(user_id, "signup", {"email": email})
```

In `src/mcp_server/coach.py`:

```python
@app.post("/v1/coach")
async def coach_endpoint(request: CoachRequest, user_id: str):
    """Coach endpoint - record interaction"""
    try:
        result = await execute_coach(request)
        
        # Record interaction
        await record_interaction(
            user_id, 
            "coach_call",
            {
                "agent": request.agent_name,
                "framework": request.framework,
                "duration_ms": timer.elapsed()
            }
        )
        
        return result
    except Exception as e:
        raise
```

---

## Dashboard Integration

### Add to Grafana Dashboard

**File:** `sustainnet-observability/products/sn1ma-mcp/governance-dashboard.json`

Add this panel:

```json
{
  "title": "Days Since Last Real User Interaction",
  "type": "stat",
  "targets": [
    {
      "expr": "sn1ma_days_since_last_user_interaction",
      "legendFormat": "Days"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "color": {
        "mode": "thresholds"
      },
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "color": "green", "value": null },        // 0-1 days = active
          { "color": "yellow", "value": 1 },           // 1-7 days = warning
          { "color": "red", "value": 7 }               // 7+ days = critical
        ]
      },
      "unit": "d"
    }
  },
  "options": {
    "textMode": "auto",
    "graphMode": "area"
  }
}
```

### Add Prometheus Metric

**File:** `sustainnet-observability/shared/alerting/sn1ma-metrics.yml`

```yaml
groups:
- name: sn1ma_metrics
  interval: 5m
  rules:
  - record: sn1ma_days_since_last_user_interaction
    expr: |
      EXTRACT(EPOCH FROM (NOW() - max(user_interactions.timestamp))) / 86400
    labels:
      service: sn1ma
      metric_type: business

  - alert: NoUserActivityThisWeek
    expr: sn1ma_days_since_last_user_interaction > 7
    for: 1h
    labels:
      severity: critical
    annotations:
      summary: "No real user interaction for 7+ days"
      description: "Days since last user interaction: {{ $value }}"
```

---

## Weekly Check-In

**Every Friday at 9 AM SAST:**

```bash
# Check the metric
curl -s http://localhost:9001/metrics/days-since-last-interaction | jq .

# Expected output (before launch):
# {
#   "metric": "days_since_last_real_user_interaction",
#   "value": null,
#   "status": "no_users_yet",
#   "target": 0,
#   "last_interaction": null,
#   "total_users": 0
# }

# Expected output (after launch, Day 1):
# {
#   "metric": "days_since_last_real_user_interaction",
#   "value": 0.042,     # ~1 hour
#   "status": "active",
#   "target": 0,
#   "last_interaction": "2026-02-08T14:32:15+02:00",
#   "total_users": 5
# }
```

---

## Milestone Targets

| Milestone | Target Date | Days Metric | Users |
|-----------|-------------|-------------|-------|
| **No users yet** | Feb 1 | ∞ | 0 |
| **First user signs up** | Feb 8 | 0 | 1 |
| **5 active users** | Feb 15 | < 1 | 5 |
| **10 paying users** | Mar 1 | < 0.5 | 10 |
| **50 active users** | Mar 31 | < 0.5 | 50 |

---

## Alert Rules

**Set up Slack notification when metric crosses threshold:**

```bash
# In Slack channel #sn1ma-metrics:

🚨 ALERT: Days since last user interaction = 7+
→ No real users in 1 week
→ Action: Schedule launch sprint
→ Escalation: Review GTM strategy

🟡 WARNING: Days since last user interaction = 1-7
→ Users signed up but not actively using
→ Action: Email retention campaign
→ Escalation: Analyze first-run experience

🟢 HEALTHY: Days since last user interaction < 1
→ Real users engaging with SN1MA
→ Action: Continue collecting feedback
→ Escalation: None, stay the course
```

---

## Why This Metric Matters

1. **Single North Star:** One number that tells you if customers are real or imagined
2. **Stops Vanity Metrics:** Ignores page views, signups, downloads — only counts real engagement
3. **Forces Focus:** When this hits 7+, everything else is secondary
4. **Creates Urgency:** Visible to the whole team on the dashboard

**Golden Rule:** If `days_since_last_real_user_interaction > 1`, you're not moving the needle.

