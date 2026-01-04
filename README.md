# SustainNet Observability

A centralized observability platform for all SustainNet products, providing consolidated monitoring, alerting, and business intelligence dashboards.

## Repository Structure

This monorepo contains shared observability components and product-specific monitoring configurations.

```
sustainnet-observability/
├── shared/                    # Common observability components
│   ├── iac/                  # Infrastructure as Code (Terraform/CloudFormation)
│   ├── dashboards/           # Shared dashboard templates
│   ├── alerting/             # Common alerting rules
│   └── scripts/              # Utility scripts
├── products/                 # Product-specific monitoring
│   ├── sustainnet-website/   # Website monitoring configs
│   ├── family-meal-planner/  # Meal planner monitoring configs
│   └── future-products/      # Placeholder for future products
├── docs/                     # Documentation
└── .github/workflows/        # CI/CD pipelines
```

## Products Monitored

- **SustainNet Website**: Main marketing and informational site
- **Family Meal Planner**: Recipe and meal planning application
- **Future Products**: Placeholder for upcoming SustainNet applications

## Key Features

- **Business Intelligence Dashboards**: Translate technical metrics to business insights
- **Unified Alerting**: Consistent alerting across all products
- **Infrastructure Monitoring**: AWS CloudWatch integration
- **Automated Deployment**: GitHub Actions for CI/CD
- **Scalable Architecture**: Monorepo structure for easy product onboarding

## Getting Started

1. Clone this repository
2. Review the shared components in `shared/`
3. Add your product monitoring in `products/[product-name]/`
4. Use the shared IaC modules for consistent infrastructure
5. Deploy using GitHub Actions workflows

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on adding new products or modifying shared components.

## License

See [LICENSE](LICENSE) for details.