# SustainNet Observability — CLAUDE.md

## What Is This

**Monitoring monorepo** for all SustainNet products. Contains dashboards, alert rules, and IaC for Prometheus + Grafana observability.

## Structure

```
shared/
  iac/          # Terraform/CloudFormation modules
  dashboards/   # Shared dashboard templates
  alerting/     # Common alert rules
  scripts/      # Utility scripts
products/
  family-meal-planner/    # FMP monitoring
  sustainnet-website/     # Website monitoring
  sn1ma-mcp/              # Financial health dashboard (16 panels)
  aiwf/                   # AI Workflow monitoring
  future-products/        # Placeholder
```

## SN1MA-MCP Financial Dashboard (Key)

16-panel Grafana dashboard:
- Cost-to-Income ratio gauge
- Revenue vs. Cost graph
- Profit margin, MRR, paying customers
- Guardrails status (10 financial guardrails)
- LTV:CAC ratio, churn rate, payback period

**15 alert rules** at 3 severity levels:
- KILL: Cost-to-Income >25%, spending exceeded
- CRITICAL: Cost-to-Income >20%, payback >30 days
- WARNING: Cost-to-Income >15%, low margin

## CI/CD Workflows

development-ci, staging-deploy, production-deploy, promote-to-staging, dora-metrics, testing-metrics, deploy-pages

## Cost

R0 (Grafana Cloud free tier + Fly.io free tier)
