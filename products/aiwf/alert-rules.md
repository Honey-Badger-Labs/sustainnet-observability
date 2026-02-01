# AIWF CloudWatch Alert Rules

## Governance Alerts

### Critical: AIM Validation Bypass Attempt
**Metric:** `aim_validation_failures_total`  
**Condition:** > 10 failures/minute  
**Action:** Immediate Slack notification + Email to security team

```yaml
AlarmName: AIWF-GovernanceBypassAttempt
MetricName: aim_validation_failures_total
Namespace: AIWF/Production
Statistic: Sum
Period: 60
EvaluationPeriods: 1
Threshold: 10
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-critical-alerts
TreatMissingData: notBreaching
```

### Warning: High Override Rate
**Metric:** `human_override_rate`  
**Condition:** > 30% overrides (AI quality degrading)  
**Action:** Slack notification to product team

```yaml
AlarmName: AIWF-HighOverrideRate
MetricName: human_override_rate
Namespace: AIWF/Production
Statistic: Average
Period: 300
EvaluationPeriods: 2
Threshold: 0.30
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-warning-alerts
```

---

## Security Alerts

### Critical: Brute Force Attack
**Metric:** `authentication_failures_total`  
**Condition:** > 20 failures/minute  
**Action:** Auto-block IP + Slack alert

```yaml
AlarmName: AIWF-BruteForceDetected
MetricName: authentication_failures_total
Namespace: AIWF/Production
Statistic: Sum
Period: 60
EvaluationPeriods: 1
Threshold: 20
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-critical-alerts
  - arn:aws:lambda:us-central-1:ACCOUNT_ID:function:BlockMaliciousIP
```

### Warning: JWT Validation Failures
**Metric:** `jwt_validations_total{result="failure"}`  
**Condition:** > 10% failure rate  
**Action:** Slack notification

```yaml
AlarmName: AIWF-JWTValidationIssues
MetricName: jwt_validation_failure_rate
Namespace: AIWF/Production
Statistic: Average
Period: 300
EvaluationPeriods: 2
Threshold: 0.10
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-warning-alerts
```

---

## Workflow Performance Alerts

### Critical: Workflow Failure Surge
**Metric:** `workflow_executions_total{status="failed"}`  
**Condition:** > 50% failure rate  
**Action:** Immediate escalation

```yaml
AlarmName: AIWF-WorkflowFailureSurge
MetricName: workflow_failure_rate
Namespace: AIWF/Production
Statistic: Average
Period: 300
EvaluationPeriods: 2
Threshold: 0.50
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-critical-alerts
```

### Warning: Slow Workflow Execution
**Metric:** `workflow_duration_seconds`  
**Condition:** p95 > 60 seconds  
**Action:** Performance review

```yaml
AlarmName: AIWF-SlowWorkflowExecution
MetricName: workflow_duration_seconds
ExtendedStatistic: p95
Namespace: AIWF/Production
Period: 300
EvaluationPeriods: 3
Threshold: 60
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-warning-alerts
```

---

## System Health Alerts

### Critical: High Error Rate
**Metric:** `http_requests_total{status=~"5.."}`  
**Condition:** > 5% of requests returning 5xx  
**Action:** Auto-rollback if recent deployment

```yaml
AlarmName: AIWF-HighErrorRate
MetricName: http_5xx_rate
Namespace: AIWF/Production
Statistic: Average
Period: 60
EvaluationPeriods: 2
Threshold: 0.05
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-critical-alerts
  - arn:aws:lambda:us-central-1:ACCOUNT_ID:function:AutoRollback
```

### Warning: High Latency
**Metric:** `http_request_duration_seconds`  
**Condition:** p99 > 2 seconds  
**Action:** Performance investigation

```yaml
AlarmName: AIWF-HighLatency
MetricName: http_request_duration_seconds
ExtendedStatistic: p99
Namespace: AIWF/Production
Period: 300
EvaluationPeriods: 2
Threshold: 2
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-warning-alerts
```

### Critical: Disk Space Low
**Metric:** `DISK_USED`  
**Condition:** > 85% disk usage  
**Action:** Log rotation + cleanup

```yaml
AlarmName: AIWF-DiskSpaceLow
MetricName: DISK_USED
Namespace: AIWF/Production
Statistic: Average
Period: 300
EvaluationPeriods: 1
Threshold: 85
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-critical-alerts
  - arn:aws:lambda:us-central-1:ACCOUNT_ID:function:CleanupLogs
```

---

## Audit & Compliance Alerts

### Warning: Large Audit Log
**Metric:** `audit_log_size_bytes`  
**Condition:** > 5GB (rotation needed)  
**Action:** Trigger log rotation

```yaml
AlarmName: AIWF-AuditLogRotationNeeded
MetricName: audit_log_size_bytes
Namespace: AIWF/Production
Statistic: Maximum
Period: 3600
EvaluationPeriods: 1
Threshold: 5368709120  # 5GB in bytes
ComparisonOperator: GreaterThanThreshold
AlarmActions:
  - arn:aws:lambda:us-central-1:ACCOUNT_ID:function:RotateAuditLogs
```

---

## SNS Topic Configuration

```bash
# Create SNS topics for alerts
aws sns create-topic --name aiwf-critical-alerts
aws sns create-topic --name aiwf-warning-alerts

# Subscribe Slack webhook
aws sns subscribe \
  --topic-arn arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-critical-alerts \
  --protocol https \
  --notification-endpoint https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-central-1:ACCOUNT_ID:aiwf-critical-alerts \
  --protocol email \
  --notification-endpoint jake@sustainnet.io
```

---

## Alert Severity Levels

| Level | Response Time | Notification Channels | Auto-Remediation |
|-------|--------------|----------------------|------------------|
| **Critical** | < 5 minutes | Slack + Email + SMS | Yes (where safe) |
| **Warning** | < 30 minutes | Slack + Email | No |
| **Info** | < 24 hours | Slack only | N/A |

---

*Last Updated: 1 February 2026*
