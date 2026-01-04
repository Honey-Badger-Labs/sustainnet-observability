# Shared Dashboard Templates

This directory contains reusable Grafana dashboard templates that can be customized for different SustainNet products.

## Available Templates

- `business-overview.json` - Executive business metrics dashboard
- `infrastructure-health.json` - Infrastructure monitoring dashboard
- `application-performance.json` - Application performance metrics
- `error-tracking.json` - Error and exception monitoring

## Template Variables

All templates use variables for:
- `${PRODUCT_NAME}` - The product name (e.g., "sustainnet-website")
- `${ENVIRONMENT}` - Environment (dev, staging, prod)
- `${REGION}` - AWS region
- `${NAMESPACE}` - CloudWatch namespace

## Customization

1. Copy the template to your product directory
2. Replace variables with product-specific values
3. Modify panels as needed for your product
4. Test the dashboard with sample data

## Best Practices

- Use consistent color schemes across products
- Include business-relevant KPIs prominently
- Add proper descriptions to all panels
- Use appropriate refresh intervals
- Include alerting annotations where applicable