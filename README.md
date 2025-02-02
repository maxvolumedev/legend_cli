# Legend CLI

A command-line interface for managing Azure Function apps

## Prerequisites

- Python 3.9 or higher
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- Azure CLI (for deployment)

## Installation

### Option 1: Install from Github repository

```bash
pip install git+https://github.com/maxvolumedev/legend_cli.git
```

This will install the `legend` command globally.

### Option 2: Install from Source

```bash
git clone https://github.com/maxvolumedev/legend_cli.git
cd legend_cli
pip install -e .
```

## Commands

### legend bootstrap

Checks and installs required dependencies.

```bash
legend bootstrap
```

### legend new

Creates a new Azure Function app with a standardized project structure.

```bash
legend new APP_NAME [LOCATION]
```

Options:
- `APP_NAME`: Name of your function app (required)
- `LOCATION`: Azure location to create resources in (default: australiasoutheast)

Example:
```bash
legend new my-function-app
```

This creates:
- A Python Azure Function app with virtual environment
- Configuration files for multiple environments
- Test directory structure
- GitHub Actions workflow for CI/CD
- Library directory for shared code

### legend generate (alias: g)

Generates new code components.

```bash
legend generate function FUNCTION_NAME [--template TEMPLATE]
```

Options:
- `FUNCTION_NAME`: Name of the function to generate (required)
- `--template`, `-t`: Function template to use (default: "HTTP trigger")

Example:
```bash
legend generate function process_order --template "Queue trigger"
```

To see available templates:
```bash
func templates list
```

### legend run (alias: r)

Runs the Function App locally for development.

```bash
legend run [--verbose]
```

Options:
- `--verbose`, `-v`: Enable verbose output

### legend test (alias: t)

Runs the test suite using pytest.

```bash
legend test [PYTEST_ARGS]
```

All arguments after `test` are passed directly to pytest. The command automatically sets `LEGEND_ENVIRONMENT=test`.

Examples:
```bash
legend test                    # Run all tests
legend test -v                # Run with verbose output
legend test test/specific     # Run tests in specific directory
```

### legend console (alias: c)

Starts an interactive Python console with your function app loaded.

```bash
legend console
```

The console provides:
- Direct access to your functions
- Helpers for creating mock requests
- Access to the Azure Functions runtime
- Enhanced REPL experience with syntax highlighting and auto-completion if ptpython is installed (`pip install ptpython`)

Example usage in console:
```python
# Create a mock HTTP request
req = func.HttpRequest(
    method='GET',
    body=None,
    url='/api/my_function',
    params={'name': 'Test'}
)

# Call your function
response = my_function(req)

# Check the response
print(response.get_body().decode())
print(f"Status: {response.status_code}")
```

### legend provision (alias: p)

Provisions required Azure resources for your function app.

```bash
legend provision [--environment ENV]
```

Options:
- `--environment`, `-e`: Target environment (default: development)

### legend deploy

Deploys your function app to Azure.

```bash
legend deploy [--environment ENV]
```

Options:
- `--environment`, `-e`: Target environment (default: development)

## Configuration

### Environment Configuration

The application supports multiple environments: development, test, sit, uat, and production. Configuration for each environment is stored in TOML files under the `config/` directory.

To specify the environment:
```bash
export LEGEND_ENVIRONMENT=development  # Or test, sit, uat, production
```

If not specified, the environment defaults to `development`.

To access configuration in your code:
```python
from lib.config import config

# Access configuration values
key_vault_name = config.azure.key_vault_name
api_base_url = config.api.base_url
debug_mode = config.settings.debug
```

### Project Structure

```
my-function-app/
├── .github/
│   └── workflows/           # GitHub Actions workflows
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
├── host.json              # Azure Functions host configuration
├── local.settings.json    # Local settings
└── requirements.txt       # Python dependencies
```

## License

MIT License. See LICENSE file for details.
