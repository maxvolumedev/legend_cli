# Legend CLI

A command-line interface for managing Azure Function apps

## Prerequisites

- [Python 3.9 or higher](https://www.python.org/downloads/)
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [Azure CLI (for deployment)](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

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

Generates new code components. Supports generating Azure Functions and GitHub workflows.

#### Generate a Function

```bash
legend generate function FUNCTION_NAME [--template TEMPLATE]
# or using the alias
legend g f FUNCTION_NAME [--template TEMPLATE]
```

Options:
- `FUNCTION_NAME`: Name of the function to generate (required)
- `--template`, `-t`: Function template to use (default: "HTTP trigger")

This will:
- Generate the function using the specified template
- Create a test directory if it doesn't exist
- Generate a test file at `test/functions/[FUNCTION_NAME]_test.py`

To see available templates:
```bash
func templates list
```

#### Generate a GitHub Workflow

```bash
legend generate github-workflow ENVIRONMENT
```

Options:
- `ENVIRONMENT`: Environment to configure workflow for (e.g., sit, uat, production)

This will generate a GitHub Actions workflow file at `.github/workflows/deploy-[ENVIRONMENT].yml` configured for the specified environment.

It will also create a service principal for authentication if necessary, and set the workflow secret in github.

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
response = app.my_function(req)

# Check the response
print(response.get_body().decode())
print(f"Status: {response.status_code}")
```

### legend provision (alias: p)

Provisions required Azure resources for an environment.

```bash
legend provision ENVIRONMENT
```

Options:
- `ENVIRONMENT`: Target environment (e.g. sit, uat, production)

This will create the following resources:
- Resource group
- Storage account
- App Service Plan
- Function app
- Key vault
- Log Analytics Insights for the app

It will also create a resource group for shared resource and a shared analytics workspace, if necessary.

**Note**: The first time you run `legend provision`, it may take several minutes as it needs to register Azure resource providers. Subsequent runs will be faster.

### legend deploy

Deploys your function app to an environment in Azure.

```bash
legend deploy ENVIRONMENT
```

Options:
- `ENVIRONMENT`: Target environment (e.g. sit, uat, production)

### legend info

Shows information about the deployed function app, including function URLs and access keys.

```bash
legend info ENVIRONMENT
```

Options:
- `ENVIRONMENT`: Target environment (e.g. sit, uat, production)


### legend destroy

Deletes the resource group and all Azure resources for an environment. Includes multiple confirmation steps to prevent accidental deletion.

```bash
legend destroy ENVIRONMENT
```

Options:
- `ENVIRONMENT`: Target environment (e.g. sit, uat, production)


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
