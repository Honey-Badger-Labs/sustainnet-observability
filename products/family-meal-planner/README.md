# Family Meal Planner Monitoring

This directory contains monitoring configurations specific to the Family Meal Planner product within the centralized observability platform.

## Architecture Overview

The monitoring solution integrates with the shared observability infrastructure:
- **Shared IaC modules** from `../../../shared/iac/` for consistent infrastructure
- **Shared dashboard templates** from `../../../shared/dashboards/` as starting points
- **Shared alerting rules** from `../../../shared/alerting/` for common patterns
- **Grafana Cloud** (free tier) for visualization
- **AWS CloudWatch** for infrastructure metrics (API, Lambda, DynamoDB, API Gateway)
- **Custom Metrics** for application-level insights
- **Mobile Analytics** for Expo app tracking (crashes, sessions, feature usage)

## Included Components

- **Dashboards**:
  - `api-performance-dashboard.json` - API health, response times, database metrics
  - `user-engagement-dashboard.json` - Active users, feature adoption, retention
  - `mobile-app-health-dashboard.json` - App crashes, failed requests, offline sync
  - `business-intelligence-dashboard.json` - Recipe searches, meal plans created, family metrics

- **Alerting**:
  - `alerting-rules.yml` - Prometheus alerting rules for FMP-specific thresholds

- **Scripts**:
  - `setup-local-demo.sh` - Local development observability setup
  - `setup-observability.sh` - Production observability deployment

## Quick Start

### 1. Use Shared Infrastructure
Reference the shared IaC modules in your deployment:
```hcl
module "grafana" {
  source = "../../../shared/iac/terraform/grafana"
  product_name = "family-meal-planner"
}
```

### 2. Customize Dashboards
1. Start with shared dashboard templates
2. Add FMP-specific panels and metrics
3. Test with sample data using the preview script

### 3. Configure Alerts
1. Extend shared alerting rules for FMP-specific thresholds
2. Set up notification channels (Slack, email, etc.)
3. Test alert conditions regularly

## Key Metrics to Track

### API Performance
- Response times (target: <500ms p95)
- Error rates (target: <1%)
- Database query performance
- Authentication latency
- Redis cache hit rates

### User Engagement
- Daily/Monthly Active Users (DAU/MAU)
- Login success/failure rates
- Recipe searches per user
- Meal plans created
- Family invitations sent/accepted

### Data Health
- Database connection errors
- Seed data integrity checks
- Failed migrations
- Redis connection issues

### Mobile Analytics
- App crashes (target: <0.1% crash rate)
- Session duration
- Feature usage (recipe search, meal planning, shopping lists)
- Offline sync success rates
- API request failures from mobile

## Integration

This monitoring integrates with:
- AWS CloudWatch for Lambda, DynamoDB, API Gateway metrics
- Custom Prometheus metrics exported from Node.js API
- Expo Analytics for mobile app insights
- Error tracking (Sentry or similar)
- Shared observability infrastructure

## Deployment

Use the shared GitHub Actions workflow from `.github/workflows/deploy-observability.yml` for automated deployment to different environments.

## Alert Thresholds

| Alert | Threshold | Severity | Action |
|-------|-----------|----------|--------|
| API Down | No heartbeat for 5min | Critical | Immediate investigation |
| High Error Rate | >5% errors over 5min | Warning | Check logs, investigate |
| Slow Response Time | >500ms avg over 5min | Warning | DB query optimization |
| Login Failures | >10% failure rate | Warning | Auth system check |
| Database Errors | Any connection errors | Error | DB health check |
| App Crash Rate | >0.5% sessions | Warning | Review crash logs |
| Redis Down | Connection failures | Error | Cache service restart |

## Dashboard Views

### Executive View (Business Intelligence)
- Total Users, Active Families, Recipes Created
- User Retention (7-day, 30-day)
- Feature Adoption Rates
- Mobile vs Web Usage

### Technical View (API Performance)
- Request Rate, Response Times (p50, p95, p99)
- Error Rates by Endpoint
- Database Query Performance
- Cache Hit Rates
- Infrastructure Health (CPU, Memory, Connections)

### Mobile View (App Health)
- Crash-Free Sessions
- App Load Time
- Feature Usage Heatmap
- Offline Sync Success Rates
- API Response Failures

## Next Steps

1. **Instrument API** with Prometheus metrics export
2. **Create Dashboards** using templates from this directory
3. **Configure Alerts** based on thresholds above
4. **Set up Mobile Analytics** in Expo app
5. **Test Locally** using docker-compose observability stack
6. **Deploy to Production** using setup-observability.sh
