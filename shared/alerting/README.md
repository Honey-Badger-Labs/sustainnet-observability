# Shared Alerting Rules

This directory contains common alerting rules and configurations that can be reused across SustainNet products.

## Alert Categories

### Business Alerts
- Revenue impact alerts
- User experience degradation
- SLA breach notifications

### Infrastructure Alerts
- Service availability
- Resource utilization thresholds
- Performance degradation

### Security Alerts
- Unusual access patterns
- Failed authentication spikes
- Data breach indicators

## Configuration

Alerts are configured using:
- AWS CloudWatch Alarms
- Prometheus Alertmanager rules
- Grafana alerting (for dashboard-based alerts)

## Usage

Reference these rules in your product-specific alerting configurations and customize thresholds as needed.

## Best Practices

- Set appropriate severity levels (Critical, Warning, Info)
- Include clear alert descriptions
- Define escalation procedures
- Test alerts regularly
- Avoid alert fatigue with smart thresholds