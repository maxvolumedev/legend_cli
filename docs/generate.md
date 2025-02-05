# legend generate

The `generate` command creates new components in your Legend project. It can generate both Azure Functions and GitHub Actions workflows.

**Alias**: `g`

## Usage

```bash
# Generate a function
legend generate function FUNCTION_NAME [--template TEMPLATE] [--authlevel LEVEL] [--skip_test]
# or using the aliases
legend g f FUNCTION_NAME [--template TEMPLATE]

# Generate a GitHub workflow
legend generate github-workflow ENVIRONMENT
```

## Subcommands

### `function` (alias: `f`)

Generates a new Azure Function with associated test file.

#### Arguments
- `FUNCTION_NAME` (required): Name of the function to generate
- `--template`, `-t` (optional): Function template to use (default: "HTTP trigger")
- `--authlevel`, `-a` (optional): Authorization level for the function (valid values: "function", "anonymous", "admin"; default: "function")
- `--skip_test`, `-s` (optional): Whether to skip generating the test file (default: "false")

**Note**: There is a bug in azure function tools that results in an error in the generated function code when specifying --authlevel on the command line. The binding is generated as `auth_level=func.AuthLevel.Function`, but the authlevel needs to be uppercase: `auth_level=func.AuthLevel.FUNCTION`.

#### What It Does
1. Creates a new function using Azure Functions Core Tools
2. Generates a test file at `test/functions/[FUNCTION_NAME]_test.py`

#### Available Templates
View available templates with:
```bash
func templates list
```

Common templates include:
- HTTP trigger
- Queue trigger
- Blob trigger
- Timer trigger
- Event Grid trigger
- Event Hub trigger
- Service Bus Queue trigger
- Service Bus Topic trigger

### `github-workflow`

Generates a GitHub Actions workflow for deploying to a specific environment.

#### Arguments
- `ENVIRONMENT` (required): Target environment (e.g., sit, uat, production)

#### What It Does
1. Creates a workflow file at `.github/workflows/deploy-[ENVIRONMENT].yml`
2. Creates an Azure service principal for GitHub Actions authentication
3. Sets up GitHub repository secrets for Azure credentials
4. Configures the workflow for automated deployment

## Examples

Generate an HTTP-triggered function:
```bash
legend generate function process_order
```

Generate a queue-triggered function:
```bash
legend generate function process_queue --template "Queue trigger"
```

Generate a GitHub workflow for SIT environment:
```bash
legend generate github-workflow sit
```

## Common Issues

1. **Missing GitHub CLI**
   - Required for setting up GitHub workflows
   - Install with: `brew install gh`

2. **GitHub Authentication**
   - The command will prompt for GitHub login if not authenticated
   - Use `gh auth login` manually if needed

3. **Azure Authentication**
   - Ensure you're logged in to Azure CLI
   - Use `az login` if needed

## Related Commands

- [new](new.md) - Create a new Legend project
- [deploy](deploy.md) - Deploy your functions to Azure
- [test](test.md) - Run the test suite
