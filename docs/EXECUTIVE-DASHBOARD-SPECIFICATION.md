# SustainNet Executive Engineering Governance Dashboard

**Purpose:** Define the 12-metric executive dashboard that translates engineering health into business risk and opportunity.

**Status:** SPECIFICATION  
**Last Updated:** 22 February 2026  
**Owner:** Engineering Leadership  
**Audience:** C-Suite, Board, Investors

---

## Executive Summary

This dashboard answers one question:

> **Is engineering a strategic asset or a business liability?**

Executives should NOT see Jira velocity charts. They should see:
- **Engineering Health** (can we deliver?)
- **Business Risk** (are we exposed?)
- **Value Delivery** (did it matter?)

---

## Dashboard Layout Concept

```
┌──────────────────────────────────────────────────────────────────┐
│  SUSTAINNET EXECUTIVE ENGINEERING GOVERNANCE                     │
│  Updated: [TIMESTAMP] │ Period: Last 30 Days                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────┐ │
│  │ Delivery     │ │ Reliability  │ │ Dev Health   │ │ Risk    │ │
│  │    Speed ↑   │ │   Stable ✓   │ │    ⚠️       │ │ Low ✓   │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └─────────┘ │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │                    Customer Value: ↑ IMPROVING               ││
│  └──────────────────────────────────────────────────────────────┘│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

One screen. Not 50 Agile charts.
```

---

## The 12 Executive Metrics

### 🚀 DELIVERY (DORA) — 3 Metrics

#### Metric 1: Deployment Frequency

**What It Signals:** Innovation speed

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | Multiple/day | Best-in-class automation |
| 🟡 High | Weekly | Good, room to improve |
| 🟠 Medium | Monthly | CI/CD investment needed |
| 🔴 Low | < Monthly | Significant delivery risk |

**Data Source:** GitHub Actions, deployment events

**Executive Question Answered:**  
> "How quickly can we respond to market opportunities?"

---

#### Metric 2: Lead Time for Change

**What It Signals:** Pipeline friction, process bottlenecks

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | < 1 hour | Fully automated pipeline |
| 🟡 High | < 1 day | Good automation |
| 🟠 Medium | 1-7 days | Process friction |
| 🔴 Low | > 1 week | Significant blockers |

**Data Source:** Git commit timestamp → production deployment

**Executive Question Answered:**  
> "How long does it take from decision to delivery?"

---

#### Metric 3: Change Failure Rate

**What It Signals:** Release quality, board-level risk indicator

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | < 5% | Excellent release quality |
| 🟡 High | 5-10% | Good with room to improve |
| 🟠 Medium | 10-15% | Quality issues emerging |
| 🔴 Low | > 15% | Significant reliability risk |

**Data Source:** Rollbacks, hotfixes, incident correlation

**Executive Question Answered:**  
> "How often do releases cause problems?"

---

### ⚙️ FLOW INTELLIGENCE — 3 Metrics

#### Metric 4: Flow Time

**What It Signals:** Idea → revenue velocity

**CEO favourite metric.**

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | < 1 week | Rapid value delivery |
| 🟡 High | 1-2 weeks | Good flow |
| 🟠 Medium | 2-4 weeks | Process bottlenecks |
| 🔴 Low | > 1 month | Significant waste |

**Data Source:** Issue created → deployed timestamp

**Executive Question Answered:**  
> "How long from customer request to delivered value?"

---

#### Metric 5: Flow Efficiency %

**What It Signals:** Working vs waiting — massive transformation signal

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | > 40% | High-performance team |
| 🟡 High | 25-40% | Above average |
| 🟠 Medium | 15-25% | Typical enterprise |
| 🔴 Low | < 15% | Severe process waste |

**Calculation:** Active work time ÷ Total elapsed time

**Executive Question Answered:**  
> "Are we efficient, or is work stuck waiting?"

**Transformation Insight:**  
When Flow Efficiency is 15%, executives stop asking "Why are developers slow?" and start asking "Why does approval take 9 days?"

---

#### Metric 6: Flow Distribution

**What It Signals:** Where engineering effort is actually going

**Breakdown:**
- 🔵 **Features** — New value creation
- 🟠 **Tech Debt** — Maintenance investment
- 🔴 **Defects** — Quality remediation
- 🟣 **Security** — Risk mitigation

| Healthy Distribution | Warning Signs |
|---------------------|---------------|
| Features: 50-70% | Features < 40% |
| Tech Debt: 15-25% | Tech Debt > 35% |
| Defects: 10-20% | Defects > 30% |
| Security: 5-10% | Security < 5% |

**Executive Question Answered:**  
> "Is engineering building value or fighting fires?"

---

### 🛡 RELIABILITY — 2 Metrics

#### Metric 7: SLO Compliance %

**What It Signals:** Customer trust, reliability as revenue protection

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | > 99.9% | Best-in-class reliability |
| 🟡 High | 99.5-99.9% | Strong reliability |
| 🟠 Medium | 99.0-99.5% | Reliability concerns |
| 🔴 Low | < 99.0% | Customer impact likely |

**Data Source:** Uptime monitoring, error rates

**Executive Question Answered:**  
> "Can customers rely on us?"

---

#### Metric 8: Mean Time to Recovery (MTTR)

**What It Signals:** Recovery speed, incident response maturity

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | < 1 hour | Excellent response |
| 🟡 High | 1-4 hours | Good response |
| 🟠 Medium | 4-24 hours | Needs improvement |
| 🔴 Low | > 24 hours | Significant risk |

**Data Source:** Incident tracking, PagerDuty

**Executive Question Answered:**  
> "When things break, how fast do we recover?"

---

### ❤️ DEVELOPER HEALTH (SPACE) — 2 Metrics

#### Metric 9: Developer Satisfaction Score

**What It Signals:** Leading burnout indicator, talent retention risk

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | > 8.5/10 | Highly engaged team |
| 🟡 High | 7.5-8.5 | Healthy team |
| 🟠 Medium | 6.5-7.5 | Emerging concerns |
| 🔴 Low | < 6.5 | Burnout/retention risk |

**Data Source:** Quarterly developer survey

**Executive Question Answered:**  
> "Are our engineers happy and productive?"

---

#### Metric 10: PR Review Time

**What It Signals:** Hidden bottleneck detector — often a management issue

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | < 4 hours | Excellent collaboration |
| 🟡 High | 4-12 hours | Good responsiveness |
| 🟠 Medium | 12-24 hours | Process friction |
| 🔴 Low | > 24 hours | Team/management issue |

**Data Source:** GitHub PR metrics

**Executive Question Answered:**  
> "Is work flowing or waiting for approvals?"

**Management Insight:**  
Long PR review times often indicate understaffing, poor prioritization, or siloed knowledge — all fixable management issues.

---

### 🎯 PRODUCT VALUE — 1 Metric

#### Metric 11: Feature Adoption Rate

**What It Signals:** Real value delivery — did customers care?

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | > 70% | High customer value |
| 🟡 High | 50-70% | Good adoption |
| 🟠 Medium | 30-50% | Moderate engagement |
| 🔴 Low | < 30% | Wasted effort risk |

**Data Source:** Product analytics, feature usage

**Executive Question Answered:**  
> "Are customers using what we build?"

---

### 🔐 RISK — 1 Metric

#### Metric 12: Vulnerability Aging

**What It Signals:** Security exposure — critical in finance and enterprise SaaS

| Rating | Threshold | Interpretation |
|--------|-----------|----------------|
| 🟢 Elite | < 7 days avg | Rapid remediation |
| 🟡 High | 7-14 days | Good response |
| 🟠 Medium | 14-30 days | Growing exposure |
| 🔴 Low | > 30 days | Significant risk |

**Data Source:** Dependabot, Snyk, security scanners

**Executive Question Answered:**  
> "How exposed are we to security threats?"

---

## Dashboard View Summary

| Domain | Metrics | Status Indicator |
|--------|---------|------------------|
| **Delivery Speed** | 1, 2, 3 | ↑ ↓ → |
| **Flow Efficiency** | 4, 5, 6 | ↑ ↓ → |
| **Reliability** | 7, 8 | ✓ ⚠️ ✗ |
| **Developer Health** | 9, 10 | ✓ ⚠️ ✗ |
| **Customer Value** | 11 | ↑ ↓ → |
| **Security Risk** | 12 | Low/Med/High |

---

## What Makes This Powerful

### Before (Traditional)
Executives ask:
> "Why are developers slow?"

### After (Intelligence Stack)
Executives ask:
> "Why does approval take 9 days?"
> "Why are 35% of our efforts on defects?"
> "Why is feature adoption only 25%?"

**These questions fix organizations.**

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Implement DORA metrics (1, 2, 3)
- [ ] Implement MTTR tracking (8)
- [ ] Basic dashboard scaffold

### Phase 2: Flow + Reliability (Week 3-4)
- [ ] Implement Flow Time (4)
- [ ] Implement SLO Compliance (7)
- [ ] Add Flow Distribution (6)

### Phase 3: Developer Health (Week 5-6)
- [ ] Launch developer survey (9)
- [ ] Implement PR Review Time (10)
- [ ] Add Flow Efficiency (5)

### Phase 4: Value + Risk (Week 7-8)
- [ ] Integrate product analytics (11)
- [ ] Implement Vulnerability Aging (12)
- [ ] Executive dashboard polish

---

## Technical Implementation

### Data Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  GitHub     │    │  Jira/      │    │  CloudWatch │    │  Product    │
│  Actions    │    │  Linear     │    │  Metrics    │    │  Analytics  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       v                  v                  v                  v
┌─────────────────────────────────────────────────────────────────────┐
│                      Data Aggregation Layer                         │
│                      (Python scripts / ETL)                         │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                v
┌─────────────────────────────────────────────────────────────────────┐
│                      Metrics Storage                                │
│                      (PostgreSQL / TimescaleDB)                     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                v
┌─────────────────────────────────────────────────────────────────────┐
│                      Visualization Layer                            │
│                      (Grafana / Custom Dashboard)                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Dashboard JSON Location
`/products/executive-dashboard/grafana-dashboard.json`

---

## Related Documents

- [Elite Engineering Intelligence Stack](./ELITE-ENGINEERING-INTELLIGENCE-STACK.md)
- [DORA Metrics Script](../shared/scripts/compute_dora.py)
- [Testing Metrics Script](../shared/scripts/compute_testing.py)

---

*Executives should see engineering health, not activity. This dashboard makes that possible.*
