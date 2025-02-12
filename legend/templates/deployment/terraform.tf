terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Application Resource Group
resource "azurerm_resource_group" "app_rg" {
  name     = var.resource_group_name
  location = var.location
}

# Shared Resource Group
resource "azurerm_resource_group" "shared_rg" {
  name     = var.shared_resource_group_name
  location = var.location
}

# Log Analytics Workspace (in shared RG)
resource "azurerm_log_analytics_workspace" "workspace" {
  name                = var.log_analytics_workspace_name
  location            = azurerm_resource_group.shared_rg.location
  resource_group_name = azurerm_resource_group.shared_rg.name
  sku                = "PerGB2018"
  retention_in_days   = 30
}

# API Management (in shared RG)
resource "azurerm_api_management" "apim" {
  name                = var.apim_name
  location            = azurerm_resource_group.shared_rg.location
  resource_group_name = azurerm_resource_group.shared_rg.name
  publisher_name      = "Your Organization Name"
  publisher_email     = "email@example.com"

  sku_name = "Developer_1"

  identity {
    type = "SystemAssigned"
  }
}

variable "location" {
  type        = string
  description = "Location for all resources"
  default     = "eastus"  # You can modify this default value
}

variable "function_app_name" {
  type        = string
  description = "Name of the Function App"
}

variable "storage_account_name" {
  type        = string
  description = "Name of the storage account"
}

variable "app_service_plan_name" {
  type        = string
  description = "Name of the App Service Plan"
}

variable "app_service_plan_sku" {
  type        = string
  description = "SKU of the App Service Plan"
  default     = "B1"
}

variable "key_vault_name" {
  type        = string
  description = "Name of the Key Vault"
}

variable "resource_group_name" {
  type        = string
  description = "Name of the Application Resource Group"
}

variable "shared_resource_group_name" {
  type        = string
  description = "Name of the Shared Resource Group for APIM and Log Analytics"
}

variable "log_analytics_workspace_name" {
  type        = string
  description = "Name of the Log Analytics Workspace"
}

variable "apim_name" {
  type        = string
  description = "Name of the API Management service"
}

# Storage Account
resource "azurerm_storage_account" "function_storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.app_rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# App Service Plan
resource "azurerm_service_plan" "function_app_plan" {
  name                = var.app_service_plan_name
  location            = var.location
  resource_group_name = azurerm_resource_group.app_rg.name
  os_type            = "Linux"
  sku_name           = var.app_service_plan_sku
}

# Key Vault
resource "azurerm_key_vault" "function_keyvault" {
  name                       = var.key_vault_name
  location                   = var.location
  resource_group_name        = azurerm_resource_group.app_rg.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  enable_rbac_authorization = false
}

# Application Insights
resource "azurerm_application_insights" "function_insights" {
  name                = var.function_app_name
  location            = var.location
  resource_group_name = azurerm_resource_group.app_rg.name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.workspace.id
}

# Function App
resource "azurerm_linux_function_app" "function_app" {
  name                       = var.function_app_name
  location                   = var.location
  resource_group_name        = azurerm_resource_group.app_rg.name
  service_plan_id            = azurerm_service_plan.function_app_plan.id
  storage_account_name       = azurerm_storage_account.function_storage.name
  storage_account_access_key = azurerm_storage_account.function_storage.primary_access_key

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "FUNCTIONS_EXTENSION_VERSION"               = "~4"
    "FUNCTIONS_WORKER_RUNTIME"                  = "python"
    "APPLICATIONINSIGHTS_CONNECTION_STRING"     = azurerm_application_insights.function_insights.connection_string
  }

  depends_on = [
    azurerm_service_plan.function_app_plan,
    azurerm_storage_account.function_storage,
    azurerm_application_insights.function_insights
  ]
}

# Outputs
output "function_app_url" {
  value = azurerm_linux_function_app.function_app.default_hostname
}

output "function_app_identity_principal_id" {
  value = azurerm_linux_function_app.function_app.identity[0].principal_id
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.workspace.id
  description = "The fully qualified Azure resource ID of the Log Analytics workspace"
}

output "log_analytics_workspace_resource_id" {
  value = azurerm_log_analytics_workspace.workspace.workspace_id
  description = "The workspace resource ID (different from the Azure resource ID)"
}

# Data source for Azure client configuration
data "azurerm_client_config" "current" {}