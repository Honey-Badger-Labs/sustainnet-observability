# SustainNet Copilot Context

> Guidelines for AI assistants working in this workspace
> 
> **Master Reference:** `sustainnet-vision/AGENTS/copilot-instructions/MASTER-COPILOT-INSTRUCTIONS.md`

---

## 🕐 Session Protocol

**At interaction start, display:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 SESSION START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Time: [CURRENT_TIME] SAST (GMT+2)
🤖 Model: [AI_MODEL_NAME]
📋 Task: [BRIEF_DESCRIPTION]
⏱️  Est. Completion: [ESTIMATED_TIME]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**During work:** Update user every ~60 seconds with progress
**If unclear:** Ask clarifying questions before proceeding

---

## 🏢 Repository Purpose

**sustainnet-observability** is the centralized monitoring platform for all SustainNet products (per DR-006).

| Attribute | Value |
|-----------|-------|
| **Status** | Active (structure ready, dashboards pending) |
| **Scope** | All SustainNet products |
| **Stack** | CloudWatch, Terraform |

## 📁 Key Directories

```
shared/
├── iac/              # Terraform modules for monitoring
├── dashboards/       # Reusable dashboard templates
├── alerting/         # Common alerting rules
└── scripts/          # Utility scripts
products/
├── sustainnet-website/    # Website monitoring
├── family-meal-planner/   # FMP monitoring
└── future-products/       # Placeholder
```

## 🎯 Key Features to Build

- [ ] Business Intelligence Dashboards
- [ ] Unified Alerting Rules
- [ ] CloudWatch Integration
- [ ] AI Copilot Observability Dashboard (NEW)

## 🤖 Available Agents

| Topic | Agent | Run Command |
|-------|-------|-------------|
| Value stream metrics | Measurement | `python3 Hello-World/agents/measurement/agent.py` |
| Deployment checks | Deployment | `python3 Hello-World/agents/deployment/agent.py` |

## 📊 DORA Metrics Targets

| Metric | Target |
|--------|--------|
| Lead Time | < 2 hours |
| Deployment Frequency | Daily |
| Change Failure Rate | < 5% |
| Time to Recovery | < 1 hour |

## 📋 Key Decisions

- **DR-006:** Centralized observability repository (this repo!)

---

*When in doubt, check sustainnet-vision for authoritative guidance.*
