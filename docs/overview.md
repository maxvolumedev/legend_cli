# Legend CLI Overview

Legend CLI is an opinionated command-line interface designed to streamline the development and deployment of Azure Functions. It provides a comprehensive set of tools and best practices that make it easier to create, test, and manage serverless applications on Azure.

## Why Legend CLI?

Building serverless applications comes with its own set of challenges:
- Setting up proper project structure
- Managing multiple environments
- Handling configuration
- Setting up CI/CD pipelines
- Provisioning cloud resources
- Managing deployments

Legend CLI addresses these challenges by providing a standardized approach to Azure Functions development, with built-in solutions for common needs like environment management, testing, and deployment.

## Key Features

- **Project Scaffolding**: Create new Azure Function apps with a well-structured project layout
- **Environment Management**: Built-in support for multiple environments (development, test, sit, uat, production)
- **Configuration Management**: TOML-based configuration system with environment-specific settings
- **Local Development**: Integrated tools for local development and testing
- **Azure Integration**: Seamless provisioning and deployment to Azure
- **CI/CD Setup**: Automated GitHub Actions workflow generation
- **Testing Framework**: Built-in test structure and utilities
- **Interactive Console**: REPL environment for quick testing and debugging

## Core Concepts

### Project Structure
Legend CLI creates a standardized project structure that separates concerns and makes it easy to find and manage your code:
```
my-function-app/
├── .github/workflows/    # CI/CD workflows
├── config/              # Environment configurations
├── lib/                 # Shared library code
├── test/               # Test files
└── functions/          # Azure Functions
```

### Environment Management
Legend supports multiple environments out of the box:
- `development`: Local development environment
- `test`: For running automated tests
- `sit`: System Integration Testing
- `uat`: User Acceptance Testing
- `production`: Production environment

Each environment has its own configuration file in the `config/` directory.

### Configuration System
Configuration is managed through TOML files:
- `config/application.toml`: Global settings
- `config/[environment].toml`: Environment-specific settings

Settings are accessible in your code through a simple dot notation interface.

### Resource Provisioning

Legend CLI uses a structured approach to Azure resource provisioning:

#### Resource Organization
- **Shared Resources**: Common resources like Log Analytics workspaces
- **Environment-Specific Resources**: Separate resources for each environment (sit, uat, production)
- **Resource Groups**: Logical grouping of resources by environment and purpose

#### Resource Types
1. **Compute Resources**
   - Azure Function App
   - App Service Plan
   - Application Insights

2. **Storage Resources**
   - Storage Account
   - Key Vault for secrets

3. **Monitoring Resources**
   - Log Analytics Workspace
   - Application Insights
   - Azure Monitor

#### Infrastructure as Code
- ARM templates in `deployment/` directory
- Environment-specific parameters
- Version-controlled infrastructure
- Automated provisioning via `legend provision`

### CI/CD Integration
Legend CLI can automatically set up and configure GitHub Actions workflows for your environments, handling:
- Dependency installation
- Running tests
- Resource provisioning (authentication resources)
- Application deployment
- Secret management

## Getting Started

To get started with Legend CLI, check out our [Tutorial](tutorial.md) which will walk you through creating and deploying your first Azure Function app.

## Command Reference

### Project Setup
- [bootstrap](bootstrap.md) - Install required dependencies
- [new](new.md) - Create a new Azure Function app

### Development
- [generate](generate.md) - Generate new functions and workflows
- [run](run.md) - Run the function app locally
- [test](test.md) - Run the test suite
- [console](console.md) - Start an interactive console

### Infrastructure Management
- [provision](provision.md) - Provision Azure resources
- [destroy](destroy.md) - Clean up Azure resources

### Deployment
- [deploy](deploy.md) - Deploy to Azure
- [info](info.md) - View deployment information
