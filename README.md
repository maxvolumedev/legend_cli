# Legend CLI

An opinionated command-line interface for building, managing and running Azure Function apps

## Key Features

- **Project Scaffolding**: Create new Azure Function apps with a well-structured project layout
- **Environment Management**: Built-in support for multiple environments (development, test, sit, uat, production)
- **Configuration Management**: TOML-based configuration system with environment-specific settings
- **Local Development**: Integrated tools for local development and testing
- **Azure Integration**: Seamless provisioning and deployment to Azure
- **CI/CD Setup**: Automated GitHub Actions workflow generation
- **Testing Framework**: Built-in test structure and utilities
- **Interactive Console**: REPL environment for quick testing and debugging

## Prerequisites

- [Python 3.9 or higher](https://www.python.org/downloads/)
- Git
- Homebrew

## Installation

### Recommended: Install from Github repository


```bash
pip install git+https://github.com/maxvolumedev/legend_cli.git
```

This will install the `legend` command globally.

### Install from Source - For hacking on Legend CLI

```bash
git clone https://github.com/maxvolumedev/legend_cli.git
cd legend_cli
pip install -e .
```

## Documentation

- [Overview](docs/overview.md) - Learn about Legend CLI's core concepts and features
- [Tutorial](docs/tutorial.md) - Step-by-step guide to creating your first Azure Function app

## Commands

### Project Setup
- [bootstrap](docs/bootstrap.md) - Install required dependencies
- [new](docs/new.md) - Create a new Azure Function app

### Development
- [generate](docs/generate.md) - Generate new functions and workflows
- [run](docs/run.md) - Run the function app locally
- [test](docs/test.md) - Run the test suite
- [console](docs/console.md) - Start an interactive console

### Infrastructure Management
- [provision](docs/provision.md) - Provision Azure resources
- [destroy](docs/destroy.md) - Clean up Azure resources

### Deployment
- [deploy](docs/deploy.md) - Deploy to Azure
- [info](docs/info.md) - View deployment information

## Configuration

### Environment Configuration

By default, the generated application will be configured with multiple environments: development, test, sit, uat, and production. Configuration for each environment is stored in TOML files under the `config/` directory.

If invoking various commands via the legend CLI (e..g legend run, legend console, legend test, etc.), the correct environment will be set automatically.

To manually specify the environment, if running code directly:
```bash
export LEGEND_ENVIRONMENT=development  # Or test, sit, uat, production
```

To access configuration in your code:
```python
from config import Configuration
config = Configuration()

endpoint = config.api.some_endpoint_url # e.g for environment-specific target API endpoints
```

Or pass the environment name directly to Configuration:
```
config = Configuration("sit")
```

### Project Structure

```
my-function-app/
├── .github/
│   └── workflows/          # GitHub Actions workflows
├── config/
│   ├── application.toml    # Global configuration
│   ├── development.toml    # Environment-specific configuration
│   ├── test.toml
│   ├── sit.toml
│   ├── uat.toml
│   └── production.toml
├── lib/                    # Shared library code
├── test/                   # Test files
├── .gitignore
├── function_app.py         # Azure Functions entry point
├── host.json               # Azure Functions host configuration
├── local.settings.json     # Local settings
└── requirements.txt        # Python dependencies
```

## License

MIT License. See LICENSE file for details.
