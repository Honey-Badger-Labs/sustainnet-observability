# Observability Improvement Priorities

**Purpose:** Prioritized roadmap for implementing the Elite Engineering Intelligence Stack at SustainNet.

**Status:** ACTIVE  
**Last Updated:** 22 February 2026  
**Review Cadence:** Monthly

---

## Priority Framework

Improvements ranked by:
1. **Business Value** — Executive visibility, decision quality
2. **Implementation Effort** — Time and complexity
3. **Data Availability** — Can we measure this today?
4. **Risk Reduction** — Prevents incidents, surprises

---

## 🔴 P0 — Critical (Implement This Sprint)

### 1. Automate DORA Metrics Collection

**Current State:** Manual/empty (`docs/data/dora.json` shows null values)

**Gap:** No automated deployment tracking

**Action Required:**
- [ ] Update `shared/scripts/compute_dora.py` to query GitHub Actions API
- [ ] Add deployment event tracking via GitHub webhooks
- [ ] Schedule daily DORA computation
- [ ] Store time-series data for trending

**Business Value:** HIGH — Foundation for all delivery metrics  
**Effort:** 3-5 days  
**Owner:** TBD

---

### 2. Implement SLO Compliance Dashboard

**Current State:** SLO tracking exists for SN1MA-MCP, inconsistent elsewhere

**Gap:** No unified SLO view across products

**Action Required:**
- [ ] Define SLOs for all products (uptime, latency, error rate)
- [ ] Create unified SLO compliance panel
- [ ] Add error budget tracking

**Business Value:** HIGH — Reliability = Revenue protection  
**Effort:** 2-3 days  
**Owner:** TBD

---

### 3. Flow Time Tracking from Issue Lifecycle

**Current State:** No tracking of idea → production time

**Gap:** Can't answer "How long does work take?"

**Action Required:**
- [ ] Connect to GitHub Issues/Projects API
- [ ] Track state transitions (created → in-progress → done → deployed)
- [ ] Compute median/P90 flow times

**Business Value:** HIGH — CEO favourite metric  
**Effort:** 3-4 days  
**Owner:** TBD

---

## 🟠 P1 — High Priority (This Month)

### 4. PR Review Time Metrics

**Current State:** Not tracked

**Gap:** Hidden bottleneck causing flow inefficiency

**Action Required:**
- [ ] Query GitHub API for PR lifecycle events
- [ ] Track: Time to first review, Time to merge
- [ ] Create alerts for PRs waiting > 24 hours

**Business Value:** MEDIUM-HIGH — Exposes management issues  
**Effort:** 2 days  
**Owner:** TBD

---

### 5. Change Failure Rate Correlation

**Current State:** Deployments tracked, failures not correlated

**Gap:** Can't calculate true Change Failure Rate

**Action Required:**
- [ ] Define "failure" criteria (rollback, hotfix, incident within 24h)
- [ ] Correlate deployments with incidents/rollbacks
- [ ] Compute rolling 30-day CFR

**Business Value:** HIGH — Board-level risk indicator  
**Effort:** 2-3 days  
**Owner:** TBD

---

### 6. Flow Distribution Analysis

**Current State:** Work types not categorized

**Gap:** Can't see Features vs Tech Debt vs Defects allocation

**Action Required:**
- [ ] Enforce issue labeling convention (feature, tech-debt, bug, security)
- [ ] Query and aggregate by label
- [ ] Create pie chart visualization

**Business Value:** HIGH — Executives LOVE this metric  
**Effort:** 2 days  
**Owner:** TBD

---

### 7. Vulnerability Aging Dashboard

**Current State:** Dependabot alerts exist, not tracked centrally

**Gap:** No visibility into security debt

**Action Required:**
- [ ] Aggregate Dependabot/security alerts across all repos
- [ ] Track age (days since opened)
- [ ] Create severity breakdown (Critical, High, Medium, Low)

**Business Value:** HIGH — Compliance requirement  
**Effort:** 2-3 days  
**Owner:** TBD

---

## 🟡 P2 — Medium Priority (This Quarter)

### 8. Developer Satisfaction Survey System

**Current State:** No formal survey process

**Gap:** No leading indicator for burnout/retention

**Action Required:**
- [ ] Design quarterly survey (10 questions, 2 minutes)
- [ ] Choose platform (Typeform, Google Forms, custom)
- [ ] Establish baseline, track trends
- [ ] Add confidential feedback channel

**Business Value:** MEDIUM — Talent retention early warning  
**Effort:** 1 week  
**Owner:** TBD

---

### 9. Flow Efficiency Calculation

**Current State:** Active time vs wait time not tracked

**Gap:** Can't calculate true efficiency %

**Action Required:**
- [ ] Define "active" states (In Progress, In Review)
- [ ] Define "waiting" states (Blocked, Waiting for Review, Backlog)
- [ ] Compute ratio per issue and overall

**Business Value:** MEDIUM-HIGH — Transformation signal  
**Effort:** 3-4 days  
**Owner:** TBD

---

### 10. Feature Adoption Tracking

**Current State:** Product analytics not integrated

**Gap:** No visibility into "Did customers use what we built?"

**Action Required:**
- [ ] Integrate product analytics (PostHog, Amplitude, or custom)
- [ ] Define adoption metrics per feature
- [ ] Create feature success dashboard

**Business Value:** MEDIUM-HIGH — Links engineering to business outcomes  
**Effort:** 1-2 weeks (depends on analytics setup)  
**Owner:** TBD

---

## 🟢 P3 — Lower Priority (Future Quarters)

### 11. SPACE Collaboration Metrics

**Current State:** Not tracked

**Gap:** No visibility into team collaboration patterns

**Action Required:**
- [ ] Track code review participation
- [ ] Monitor pairing session frequency
- [ ] Measure knowledge distribution (bus factor)

**Business Value:** MEDIUM — Team health indicator  
**Effort:** 1 week  
**Owner:** TBD

---

### 12. Predictive Analytics / Anomaly Detection

**Current State:** Reactive monitoring only

**Gap:** No proactive alerts for emerging issues

**Action Required:**
- [ ] Implement statistical anomaly detection on key metrics
- [ ] Create predictive models for deployment risk
- [ ] Add "early warning" alerts

**Business Value:** HIGH (future) — Prevents incidents  
**Effort:** 2-3 weeks  
**Owner:** TBD

---

### 13. Executive Dashboard UI

**Current State:** Technical Grafana dashboards exist

**Gap:** No executive-friendly single-screen view

**Action Required:**
- [ ] Design simplified executive view
- [ ] Implement traffic-light status indicators
- [ ] Add trend arrows (↑ ↓ →)
- [ ] Create mobile-friendly version

**Business Value:** HIGH — Executive adoption  
**Effort:** 1-2 weeks  
**Owner:** TBD

---

### 14. Cross-Layer Correlation

**Current State:** Metrics in silos

**Gap:** Can't correlate "low dev satisfaction → high defects → poor reliability"

**Action Required:**
- [ ] Build correlation engine
- [ ] Create cause-effect dashboards
- [ ] Identify leading vs lagging indicators

**Business Value:** VERY HIGH (strategic)  
**Effort:** 3-4 weeks  
**Owner:** TBD

---

## Summary by Priority

| Priority | Count | Total Effort | Quarter |
|----------|-------|--------------|---------|
| P0 - Critical | 3 | ~12 days | This Sprint |
| P1 - High | 4 | ~10 days | This Month |
| P2 - Medium | 3 | ~3 weeks | This Quarter |
| P3 - Lower | 4 | ~8 weeks | Future |

---

## Quick Wins (< 1 Day Each)

1. **Add doc references to README** — Link to Intelligence Stack docs ✓
2. **Create empty executive-dashboard product folder** — Scaffold structure
3. **Add issue labeling convention to CONTRIBUTING.md** — Enable Flow Distribution
4. **Create DORA metrics cron job scaffold** — Placeholder for automation

---

## Architecture Decisions Needed

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Metrics storage | PostgreSQL vs TimescaleDB vs InfluxDB | TimescaleDB (time-series native) |
| Visualization | Grafana vs Custom | Grafana (existing), Custom exec view later |
| Data pipeline | Python scripts vs dbt vs Airbyte | Python scripts (simplicity) |
| Survey tool | Typeform vs Google Forms vs Custom | Google Forms (free, simple) |

---

## Success Criteria

By end of Q1 2026:
- [ ] DORA metrics automated and trending
- [ ] SLO compliance visible across products
- [ ] Flow Time tracked for all work items
- [ ] PR Review Time alerts active
- [ ] Executive dashboard prototype deployed

By end of Q2 2026:
- [ ] All P0 and P1 items complete
- [ ] Developer satisfaction survey running quarterly
- [ ] Feature adoption tracking for top 3 products
- [ ] Executive dashboard in weekly use

---

## Related Documents

- [Elite Engineering Intelligence Stack](./ELITE-ENGINEERING-INTELLIGENCE-STACK.md)
- [Executive Dashboard Specification](./EXECUTIVE-DASHBOARD-SPECIFICATION.md)
- [DORA Metrics Script](../shared/scripts/compute_dora.py)

---

*Progress reviewed monthly. Priorities adjusted based on business needs.*
