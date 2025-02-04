# legend provision

The `provision` command creates and configures all necessary Azure resources for your function app in a specified environment.

**Alias**: `p`

## Usage

```bash
legend provision ENVIRONMENT [--shared-resources]
```

## Arguments

- `ENVIRONMENT` (required): Target environment to provision (e.g., sit, uat, production)
- `--shared-resources`, `-shared` (optional): Only provision shared resources like Log Analytics

## What It Does

1. **Creates Shared Resources**
   - Resource group for shared components
   - Log Analytics workspace for centralized logging

2. **Creates Application Resources**
   - Resource group for the application
   - Deploys ARM templates from `deployment/` directory
   - Sets up all required Azure services

## Resources Created

The command provisions the following Azure resources:

### Shared Resources
- Resource group: `legend-shared-resources-[LOCATION]`
- Log Analytics workspace: `legend-log-analytics-[LOCATION]`

### Application Resources
- Resource group (from configuration)
- Storage account
- App Service Plan
- Function App
- Application Insights
- Key Vault

## Configuration

Resources are provisioned according to:
1. ARM templates in `deployment/`
   - `azuredeploy-[ENV].json`
   - `azuredeploy-[ENV].parameters.json`
2. Settings in `config/[ENV].toml`

## Examples

Provision a complete environment:
```bash
legend provision sit
```

Only provision shared resources:
```bash
legend provision sit --shared-resources
```

## ARM Templates

The command uses ARM templates located in the `deployment/` directory:

```
deployment/
├── azuredeploy-sit.json
├── azuredeploy-sit.parameters.json
├── azuredeploy-uat.json
├── azuredeploy-uat.parameters.json
├── azuredeploy-production.json
└── azuredeploy-production.parameters.json
```

## Best Practices

1. **Resource Naming**
   - Use consistent naming conventions
   - Include environment in resource names
   - Follow Azure naming restrictions

2. **Resource Groups**
   - Separate shared and app-specific resources
   - Use location-based grouping for shared resources
   - Include environment in app resource group names

3. **Security**
   - Use Key Vault for secrets
   - Apply principle of least privilege
   - Enable monitoring and logging

## Common Issues

1. **Azure CLI Not Logged In**
   ```bash
   az login
   ```

2. **Missing Permissions**
   - Ensure you have Contributor access
   - Check Azure subscription status
   - Verify resource provider registration

3. **Template Validation Errors**
   - Check parameter files
   - Verify resource names are unique
   - Ensure dependencies are correctly specified

4. **Resource Name Conflicts**
   - Names must be globally unique
   - Check for existing resources
   - Use unique prefixes/suffixes

## Related Commands

- [deploy](deploy.md) - Deploy your function app
- [destroy](destroy.md) - Remove Azure resources
- [info](info.md) - View resource information
