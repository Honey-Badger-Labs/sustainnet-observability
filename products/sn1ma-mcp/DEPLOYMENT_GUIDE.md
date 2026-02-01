# Financial Monitoring Deployment Guide

## Quick Start (Local Testing - 10 minutes)

### Step 1: Start HRAIM with Metrics Endpoint

```bash
cd /Users/jakes/SustainNet/SN1MA-MCP

# Activate virtual environment
source .venv/bin/activate

# Start HRAIM backend on port 9001
python3 -m uvicorn HRAIM.main:app --host 0.0.0.0 --port 9001 --reload
```

**Verify metrics endpoint:**
```bash
# In another terminal
curl http://localhost:9001/metrics

# Expected output:
# # HELP sn1ma_revenue_monthly Monthly Recurring Revenue in ZAR
# # TYPE sn1ma_revenue_monthly gauge
# sn1ma_revenue_monthly 0.0
# ...
```

---

### Step 2: Start Prometheus (Local)

**Option A: Docker (Recommended)**

```bash
cd /Users/jakes/SustainNet/sustainnet-observability/products/sn1ma-mcp

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: sn1ma-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerting-rules.yml:/etc/prometheus/alerting-rules.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: sn1ma-grafana
    ports:
      - "3001:3000"  # Changed to 3001 to avoid conflict
    volumes:
      - grafana-data:/var/lib/grafana
      - ./dashboards:/etc/grafana/provisioning/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
EOF

# Update prometheus.yml to use Docker networking
# Change localhost:9001 to host.docker.internal:9001

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

**Option B: Binary Install (macOS)**

```bash
# Install Prometheus
brew install prometheus

# Copy config files
cp prometheus.yml /usr/local/etc/prometheus/
cp alerting-rules.yml /usr/local/etc/prometheus/

# Edit prometheus.yml to update target
sed -i '' 's/localhost:9001/127.0.0.1:9001/g' /usr/local/etc/prometheus/prometheus.yml

# Start Prometheus
prometheus --config.file=/usr/local/etc/prometheus/prometheus.yml
```

**Verify Prometheus:**
```bash
# Open in browser
open http://localhost:9090

# Check targets are UP
# Go to: Status → Targets
# Should see: sn1ma-mcp-hraim (1/1 up)

# Query metrics
# Go to: Graph
# Enter: sn1ma_revenue_monthly
# Click Execute
```

---

### Step 3: Configure Grafana

**Access Grafana:**
```bash
# Docker: http://localhost:3001
# Binary: http://localhost:3000

# Login:
Username: admin
Password: admin123 (or admin for binary install)
```

**Add Prometheus Data Source:**

1. Go to **Configuration → Data Sources**
2. Click **"Add data source"**
3. Select **"Prometheus"**
4. Configure:
   - **Name:** SN1MA Prometheus
   - **URL:** `http://prometheus:9090` (Docker) or `http://localhost:9090` (Binary)
   - **Access:** Server (default)
5. Click **"Save & Test"** → Should see green "Data source is working"

**Import Financial Dashboard:**

1. Go to **Dashboards → Import**
2. Click **"Upload JSON file"**
3. Select: `sustainnet-observability/products/sn1ma-mcp/financial-health-dashboard.json`
4. Configure:
   - **Name:** SN1MA-MCP: Financial Health Dashboard
   - **Folder:** SN1MA-MCP
   - **Prometheus:** SN1MA Prometheus (select from dropdown)
5. Click **"Import"**

**Dashboard should now be visible!**

---

### Step 4: Configure Alerting

**In Grafana UI:**

1. **Go to: Alerting → Alert Rules**
2. **Click: "New alert rule"**
3. **Import from Prometheus:**
   - Since we have `alerting-rules.yml` in Prometheus, alerts will auto-appear
   - Refresh the Alert Rules page

**Set up Contact Points:**

1. **Go to: Alerting → Contact points**
2. **Click: "New contact point"**
3. **Configure Slack:**
   - Name: `slack-sn1ma-financial`
   - Integration: Slack
   - Webhook URL: `https://hooks.slack.com/services/YOUR_WEBHOOK`
   - (Get webhook from: https://api.slack.com/apps)
4. **Click: "Test"** to verify
5. **Click: "Save contact point"**

**Set up Notification Policies:**

1. **Go to: Alerting → Notification policies**
2. **Edit default policy:**
   - Contact point: `slack-sn1ma-financial`
   - Group by: `alertname, category`
   - Timing:
     - Group wait: 30s
     - Group interval: 5m
     - Repeat interval: 4h

3. **Add specific policy for CRITICAL alerts:**
   - Click "New nested policy"
   - Matching labels: `severity = critical`
   - Contact point: `slack-sn1ma-financial` (add email too if configured)
   - Repeat interval: 1h

---

### Step 5: Test the Full Stack

**Test 1: Verify Metrics Collection**

```bash
# Check HRAIM metrics
curl http://localhost:9001/metrics | grep sn1ma_revenue

# Check Prometheus scraped them
curl http://localhost:9090/api/v1/query?query=sn1ma_revenue_monthly
```

**Test 2: View Dashboard**

```bash
# Open dashboard
open http://localhost:3001/d/sn1ma-financial-health

# You should see all 16 panels:
# 1. Cost-to-Income gauge (should show 0% initially)
# 2. Revenue vs Cost graph
# 3. Profit margin
# ... etc
```

**Test 3: Trigger Test Alert**

```bash
# Method 1: Manually set high cost
# Add test data to HRAIM database

psql -d hraim_mvp << 'SQL'
-- Insert test paying customer
INSERT INTO users (id, email, tier, created_at)
VALUES (gen_random_uuid(), 'test@example.com', 'pro', NOW());

-- Insert high infrastructure cost to trigger alert
INSERT INTO infrastructure_costs (id, month, fly_io_cost, upstash_cost)
VALUES (gen_random_uuid(), '2026-02', 500, 0);
SQL

# Wait 1-2 minutes for Prometheus to scrape
# Check Grafana Alerting page - should see alert firing

# Method 2: Lower alert threshold temporarily
# Edit alerting-rules.yml:
# Change: sn1ma_cost_to_income_ratio > 20
# To: sn1ma_cost_to_income_ratio > 0
# Wait for Prometheus to reload
```

**Test 4: Verify Slack Notification**

```bash
# If alert triggered, check Slack channel
# Should see message with:
# - Alert name
# - Severity
# - Business impact
# - Action required
# - Link to playbook
```

---

## Production Deployment (Cloud)

### Option 1: Fly.io (Recommended for SN1MA)

**Deploy Prometheus + Grafana:**

```bash
cd /Users/jakes/SustainNet/sustainnet-observability/products/sn1ma-mcp

# Create Dockerfile for combined stack
cat > Dockerfile << 'EOF'
FROM prom/prometheus:latest

# Copy Prometheus config
COPY prometheus.yml /etc/prometheus/
COPY alerting-rules.yml /etc/prometheus/

EXPOSE 9090

CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.console.libraries=/usr/share/prometheus/console_libraries", \
     "--web.console.templates=/usr/share/prometheus/consoles"]
EOF

# Deploy to Fly.io
fly launch --name sn1ma-prometheus --region jhb
fly deploy

# Deploy Grafana separately
fly launch --name sn1ma-grafana --region jhb --image grafana/grafana:latest
fly deploy

# Set Grafana environment variables
fly secrets set GF_SECURITY_ADMIN_PASSWORD=YOUR_SECURE_PASSWORD -a sn1ma-grafana
```

**Update Prometheus targets:**
```yaml
# In prometheus.yml
scrape_configs:
  - job_name: 'sn1ma-mcp-hraim'
    static_configs:
      - targets: ['sn1ma-hraim.fly.dev:443']  # Production URL
    scheme: https
```

---

### Option 2: Grafana Cloud (Free Tier)

**Easiest option - no infrastructure management**

1. **Sign up:** https://grafana.com/auth/sign-up
2. **Create Stack:** 
   - Name: sn1ma-mcp
   - Region: EU (Dublin) or US (East)
3. **Get Prometheus URL:**
   - Copy: `https://prometheus-prod-XX-XX.grafana.net/api/prom/push`
   - Copy API key
4. **Configure Prometheus Remote Write:**

```yaml
# Add to prometheus.yml
remote_write:
  - url: https://prometheus-prod-XX-XX.grafana.net/api/prom/push
    basic_auth:
      username: YOUR_USERNAME
      password: YOUR_API_KEY
```

5. **Import Dashboard:**
   - Upload `financial-health-dashboard.json` to Grafana Cloud
   - Configure alerts and notification channels

**Cost:** FREE for:
- 10,000 series
- 14-day retention
- 3 users
- Perfect for SN1MA start

---

## Monitoring Checklist

### Before Going Live:

- [ ] HRAIM `/metrics` endpoint accessible
- [ ] Prometheus scraping successfully (check Targets page)
- [ ] All metrics appearing in Prometheus (query `sn1ma_*`)
- [ ] Grafana dashboard displays all 16 panels
- [ ] Alert rules loaded (check Alert Rules page)
- [ ] Slack contact point configured and tested
- [ ] Email contact point configured and tested
- [ ] Notification policy routes alerts correctly
- [ ] Test alert triggered and received
- [ ] Database schema created (users, infrastructure_costs tables)

### Daily Operations:

- [ ] Check dashboard every morning
- [ ] Review any alerts from previous day
- [ ] Update infrastructure costs (if not automated)
- [ ] Verify Prometheus is scraping successfully

### Monthly Review (1st of each month):

- [ ] Review Cost-to-Income trend
- [ ] Check if spending caps need adjustment
- [ ] Analyze profit margin trend
- [ ] Review customer growth vs. cost growth
- [ ] Update financial projections
- [ ] Document any guardrail violations

---

## Troubleshooting

### Metrics not appearing in Prometheus

```bash
# Check if HRAIM is running
lsof -i :9001

# Test metrics endpoint directly
curl http://localhost:9001/metrics

# Check Prometheus logs
docker-compose logs prometheus
# or
tail -f /usr/local/var/log/prometheus.log

# Check Prometheus targets
open http://localhost:9090/targets
# Should see sn1ma-mcp-hraim as UP

# Check for scrape errors
# Go to Status → Target Health
```

### Dashboard shows "No Data"

```bash
# Verify Prometheus data source in Grafana
# Settings → Data Sources → SN1MA Prometheus → Save & Test

# Check if metrics exist in Prometheus
# Grafana → Explore → Select Prometheus
# Query: sn1ma_revenue_monthly
# Should return value (even if 0)

# Check time range in dashboard
# Top-right corner → Last 30 days
```

### Alerts not firing

```bash
# Check alert rules are loaded
open http://localhost:9090/alerts
# Should see all rules from alerting-rules.yml

# Check alert state
# Inactive → Rule is loaded but not triggered
# Pending → Condition met, waiting for 'for' duration
# Firing → Alert is active

# Manually evaluate rule
# In Prometheus UI → Alerts → Click rule → See query results
```

### Notifications not sent

```bash
# Test contact point in Grafana
# Alerting → Contact points → slack-sn1ma-financial → Test

# Check notification policy routing
# Alerting → Notification policies → Verify labels match

# Check Slack webhook
curl -X POST https://hooks.slack.com/services/YOUR_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test from SN1MA"}'
```

---

## Next Steps

1. **Complete database schema** (5 min)
2. **Start monitoring stack** (10 min)
3. **Import dashboard** (5 min)
4. **Configure Slack webhook** (5 min)
5. **Test end-to-end** (10 min)
6. **Document runbook** (15 min)

**Total setup time:** ~50 minutes

**Once live, you'll have:**
- ✅ Real-time financial guardrail monitoring
- ✅ Automatic alerts for Cost-to-Income, spending caps, payback period
- ✅ Slack notifications for all threshold violations
- ✅ Visual dashboard showing all 16 financial metrics
- ✅ Audit trail of all alerts
- ✅ Confidence to deploy Phase 2 safely
