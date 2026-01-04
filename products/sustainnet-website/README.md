# SustainNet Website Monitoring

This directory contains monitoring configurations specific to the SustainNet website product within the centralized observability platform.

## Architecture Overview

The monitoring solution integrates with the shared observability infrastructure:
- **Shared IaC modules** from `../../../shared/iac/` for consistent infrastructure
- **Shared dashboard templates** from `../../../shared/dashboards/` as starting points
- **Shared alerting rules** from `../../../shared/alerting/` for common patterns
- **Grafana Cloud** (free tier) for visualization
- **AWS CloudWatch** for infrastructure metrics
- **Google Analytics** for user behavior insights
- **GitHub Actions** for CI/CD pipeline monitoring

## Included Components

- **Dashboards**:
  - `executive-summary-dashboard.json` - Business metrics for executives
  - `business-intelligence-dashboard.json` - Detailed business KPIs
  - `infrastructure-dashboard.json` - Infrastructure health metrics
  - `ci-cd-dashboard.json` - CI/CD pipeline monitoring

- **Alerting**:
  - `alerting-rules.yml` - Prometheus alerting rules

- **Infrastructure**:
  - `grafana-iam-setup.yaml` - AWS IAM setup for Grafana

- **Scripts**:
  - `setup-local-demo.sh` - Local development setup
  - `setup-observability.sh` - Production observability setup

- **Preview**:
  - `dashboard-preview.html` - HTML preview of dashboards

## Quick Start

### 1. Use Shared Infrastructure
Reference the shared IaC modules in your deployment:
```hcl
module "grafana" {
  source = "../../../shared/iac/terraform/grafana"
  product_name = "sustainnet-website"
}
```

### 2. Customize Dashboards
1. Start with shared dashboard templates
2. Add website-specific panels and metrics
3. Test with sample data using the preview script

### 3. Configure Alerts
1. Extend shared alerting rules for website-specific thresholds
2. Set up notification channels (Slack, email, etc.)
3. Test alert conditions regularly

## Integration

This monitoring integrates with:
- AWS CloudWatch for infrastructure metrics
- GitHub Actions for CI/CD metrics
- Custom business metrics from website analytics
- Error tracking and performance monitoring
- Shared observability infrastructure

## Deployment

Use the shared GitHub Actions workflow from `.github/workflows/deploy.yml` for automated deployment to different environments.
- User engagement metrics
- Content performance
- Conversion funnels
- Geographic distribution

## Alert Configuration

Set up alerts for:
- Website downtime (>5 minutes)
- High error rates (>5%)
- Slow response times (>3 seconds)
- Failed deployments
- Security vulnerabilities

## Cost Optimization

- Use Grafana Cloud free tier (3 users, 10k metrics)
- Leverage AWS CloudWatch free tier (first 1M requests/month)
- Archive old logs to reduce storage costs

## Maintenance

- Review dashboards quarterly for relevance
- Update metrics as the application evolves
- Train team members on dashboard usage
- Document any custom metrics or calculations