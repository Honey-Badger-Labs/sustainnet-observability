# AIWF Observability Configuration

This directory contains monitoring, alerting, and dashboard configurations for the AIWF (AI Workflow Automation) platform.

## Components

- **CloudWatch Dashboards**: Real-time monitoring of AIWF services
- **Prometheus Metrics**: Custom metrics from SustainBot
- **Alert Rules**: Critical alert configurations
- **Log Aggregation**: Centralized logging setup

## Metrics Exported

### Governance Metrics
- `aim_requests_total` - Total AIM-declared requests
- `aim_validation_failures_total` - Failed AIM validations
- `prescriptive_language_blocks_total` - Blocked prescriptive outputs
- `human_override_rate` - Rate of human interventions

### Workflow Metrics
- `workflow_executions_total` - Workflow runs by name and status
- `workflow_duration_seconds` - Execution time distribution
- `workflow_errors_total` - Failed workflows
- `active_workflows` - Currently running workflows

### Authentication Metrics
- `jwt_validations_total` - JWT validation attempts
- `authentication_failures_total` - Failed auth attempts
- `active_sessions` - Current authenticated sessions

### System Metrics
- `http_requests_total` - HTTP requests by endpoint
- `http_request_duration_seconds` - Request latency
- `active_requests` - Concurrent requests

## Quick Start

### 1. Configure CloudWatch Agent

```bash
# On AIWF VM
sudo wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Copy config
sudo cp cloudwatch-config.json /opt/aws/amazon-cloudwatch-agent/etc/

# Start agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json
```

### 2. View Metrics

**Prometheus:**
```bash
curl http://AIWF_VM_IP:5000/metrics
```

**CloudWatch Console:**
1. Navigate to CloudWatch → Dashboards
2. Select "AIWF-Production"
3. View real-time metrics

### 3. Configure Alerts

Alerts are defined in `alert-rules.yml`. To apply:

```bash
# Using CloudWatch Alarms
aws cloudwatch put-metric-alarm --cli-input-json file://alert-rules.yml
```

## Dashboard Panels

### Governance Overview
- AIM Request Rate (requests/minute)
- Validation Failure Rate (%)
- DRAG Mode Distribution (pie chart)
- Audit Log Size (GB)

### Workflow Performance
- Workflow Execution Rate
- Success vs Failure Rate
- Average Execution Time
- Top 5 Most-Run Workflows

### Security & Auth
- JWT Validation Success Rate
- Failed Authentication Attempts
- Active Sessions
- Top Failed Auth IPs

### System Health
- HTTP Request Rate
- API Latency (p50, p95, p99)
- Error Rate (5xx responses)
- CPU/Memory Usage

## Alert Conditions

### Critical
- `aim_validation_failures > 10/min` → Governance bypass attempt
- `authentication_failures > 20/min` → Brute force attack
- `workflow_error_rate > 50%` → System degradation
- `http_5xx_rate > 5%` → Service outage

### Warning
- `workflow_duration > 60s (p95)` → Performance degradation
- `audit_log_size > 5GB` → Storage cleanup needed
- `human_override_rate > 30%` → AI quality issues

## Integration with SustainNet

This observability stack integrates with:
- `sustainnet-vision` - Governance framework reference
- `sustainnet-observability` - Centralized monitoring repo
- `SN1MA-MCP` - Shared metrics patterns

## References

- [AIWF README](../../AIWF/README.md)
- [Decision Register](../../AIWF/GOVERNANCE/DECISION_REGISTER.md)
- [AIM-DRAG Framework](../../sustainnet-vision/GOVERNANCE/AIM-DRAG-FRAMEWORK.md)
