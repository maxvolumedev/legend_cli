# Azure Resource Manager (ARM) Templates

This directory contains ARM templates that define the infrastructure for the Legend application. The templates create all necessary Azure resources in an idempotent way.

## Resources Created

The template creates the following Azure resources:

- Storage Account (for Function App storage)
- App Service Plan (Linux-based)
- Function App (Python 3.11)
- Key Vault (with access policies)
- Log Analytics Workspace
- Application Insights (connected to Log Analytics)

## Dependencies

The resources have the following dependencies:

1. Function App depends on:
   - Storage Account (for file storage)
   - App Service Plan (for hosting)
   - Application Insights (for monitoring)

2. Application Insights depends on:
   - Log Analytics Workspace

## How to Deploy

1. Fill in the parameter values in `azuredeploy.parameters.json`

2. Deploy using Azure CLI:
   ```bash
   az deployment group create \
     --name legend-deployment \
     --resource-group <your-resource-group> \
     --template-file azuredeploy.json \
     --parameters @azuredeploy.parameters.json
   ```

3. Deploy using Azure PowerShell:
   ```powershell
   New-AzResourceGroupDeployment `
     -Name legend-deployment `
     -ResourceGroupName <your-resource-group> `
     -TemplateFile azuredeploy.json `
     -TemplateParameterFile azuredeploy.parameters.json
   ```

## Template Outputs

The template outputs:
- Function App URL
- Function App's Managed Identity Principal ID (for configuring Key Vault access)

## Security Considerations

1. The Key Vault is configured to use access policies instead of RBAC
2. The Function App is created with a system-assigned managed identity
3. Storage Account uses Standard LRS for cost-effectiveness
4. All secrets and connection strings are securely passed between resources

## Customization

You can customize the deployment by modifying the parameters:
- `location`: Azure region for resources
- `functionAppName`: Name of the Function App
- `storageAccountName`: Name of the storage account
- `appServicePlanName`: Name of the App Service Plan
- `appServicePlanSku`: SKU of the App Service Plan (default: Y1)
- `keyVaultName`: Name of the Key Vault
- `logAnalyticsWorkspaceName`: Name of the Log Analytics Workspace
