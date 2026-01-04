# Contributing to SustainNet Observability

Thank you for your interest in contributing to the SustainNet Observability platform! This document provides guidelines for contributing to this monorepo.

## Repository Structure

This is a monorepo containing shared observability components and product-specific monitoring. Please maintain this structure when adding new components.

## Adding a New Product

1. Create a new directory under `products/[product-name]/`
2. Use shared components from `shared/` where possible
3. Follow the established naming conventions
4. Add product-specific documentation

## Shared Components

When modifying shared components:
- Ensure backward compatibility
- Update all affected products
- Add comprehensive tests
- Document changes in the changelog

## Code Standards

- Use descriptive variable and file names
- Add comments for complex logic
- Follow the established patterns in existing code
- Test your changes thoroughly

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request with a clear description
6. Wait for review and approval

## Documentation

- Update README files when adding new features
- Add inline comments for complex code
- Document any breaking changes
- Keep the docs directory up to date

## Questions?

If you have questions about contributing, please open an issue or contact the maintainers.