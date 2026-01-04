# Future Products Monitoring

This directory serves as a template and placeholder for upcoming SustainNet products.

## Template Structure

When adding a new product, create the following structure:

```
future-products/[product-name]/
├── README.md                    # Product-specific documentation
├── dashboards/                  # Product-specific dashboard JSON files
├── alerting/                    # Product-specific alerting rules
├── iac/                         # Product-specific infrastructure code
└── scripts/                     # Product-specific setup scripts
```

## Onboarding New Products

1. Create a new directory under `products/[product-name]/`
2. Copy this README.md as a starting point
3. Reference shared components from `../../../shared/`
4. Add product-specific customizations
5. Update the root README.md to include the new product
6. Add to the shared CI/CD pipeline if needed

## Shared Components to Leverage

- **IaC Modules**: Use Terraform/CloudFormation modules from `../../../shared/iac/`
- **Dashboard Templates**: Start with templates from `../../../shared/dashboards/`
- **Alerting Rules**: Extend rules from `../../../shared/alerting/`
- **Scripts**: Use utilities from `../../../shared/scripts/`

## Best Practices

- Follow consistent naming conventions
- Document all custom metrics and calculations
- Include business-relevant KPIs
- Test monitoring setup in development environment first
- Update shared components if improvements benefit all products