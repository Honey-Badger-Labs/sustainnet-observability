# Shared Infrastructure as Code Modules

This directory contains reusable Terraform and CloudFormation modules for observability infrastructure.

## Available Modules

### Terraform Modules

- `grafana/` - Grafana instance setup
- `cloudwatch/` - AWS CloudWatch monitoring
- `alerting/` - Common alerting infrastructure

### CloudFormation Templates

- `monitoring-stack.yaml` - Base monitoring stack
- `dashboard-stack.yaml` - Dashboard deployment stack

## Usage

Reference these modules in your product-specific IaC configurations:

```hcl
module "grafana" {
  source = "../../shared/iac/terraform/grafana"
  # ... configuration
}
```

## Adding New Shared Modules

1. Create a new directory under the appropriate subdirectory
2. Include a README.md with usage examples
3. Add input/output variable documentation
4. Test the module thoroughly before committing