# legend new

The `new` command creates a new Azure Function App project with a standardized structure and configuration. It sets up everything you need to start developing, testing, and deploying your functions.

**Alias**: `n`

## Usage

```bash
legend new APP_NAME [LOCATION]
```

## Arguments

- `APP_NAME` (required): Name of your function app
- `LOCATION` (optional): Azure location to create resources in (default: australiasoutheast)

## What It Does

1. **Checks Prerequisites**
   - Verifies Azure Functions Core Tools is installed
   - Suggests installation steps if missing

2. **Creates Project Structure**
   ```
   APP_NAME/
   ├── .github/workflows/    # CI/CD workflows
   ├── config/              # Configuration files
   ├── lib/                 # Shared library code
   ├── test/               # Test files
   ├── deployment/         # Deployment templates
   ├── bin/                # Scripts and utilities
   ├── host.json          # Azure Functions host config
   └── local.settings.json # Local development settings
   ```

3. **Sets Up Dependencies**
   - Creates `requirements.txt` with core dependencies:
     - `jinja2>=3.1.2`
   - Creates `requirements-dev.txt` with development dependencies:
     - Legend CLI (for development)
     - `tomli>=2.0.1` (TOML configuration)
     - `pytest>=7.4.0` (Testing)

4. **Configures Environments**
   Creates TOML configuration files for all environments:
   - `config/application.toml` - Global settings
   - `config/development.toml` - Local development
   - `config/test.toml` - Testing
   - `config/sit.toml` - System Integration Testing
   - `config/uat.toml` - User Acceptance Testing
   - `config/production.toml` - Production

5. **Initializes Version Control**
   - Creates `.gitignore` with Python and Azure Functions defaults
   - Sets up initial Git repository

## Examples

Create a new function app with default location:
```bash
legend new my-awesome-app
```

Create a new function app in a specific Azure location:
```bash
legend new my-awesome-app eastus2
```

## After Creation

After creating your project:

1. Navigate to your project directory:
   ```bash
   cd my-awesome-app
   ```

2. Add your first function:
   ```bash
   legend generate function my_first_function
   ```

3. Start developing:
   ```bash
   legend run
   ```

## Common Issues

1. **Missing Azure Functions Core Tools**
   ```bash
   legend bootstrap
   ```
   Or install manually:
   ```bash
   brew install azure-functions-core-tools@4
   ```

2. **Name Conflicts**
   - App names must be globally unique in Azure
   - Use only letters, numbers, and hyphens
   - Names will be automatically normalized for Azure compatibility

## Related Commands

- [generate](generate.md) - Add new functions to your project
- [run](run.md) - Run your function app locally
- [provision](provision.md) - Provision Azure resources
