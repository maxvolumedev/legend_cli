import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List
from ..lib.config import load_config

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate the configuration has all required values"""
    if not config:
        return False

    missing = []
    
    # Check azure settings
    azure = config.get("azure", {})
    for key in ["location", "resource_group", "storage_account", "function_app", "app_service_plan", 
                "key_vault_name", "log_analytics_workspace"]:
        if not azure.get(key):
            missing.append(f"azure.{key}")
    
    if missing:
        print("⛔️ Error: Missing required configuration values:")
        for path in missing:
            print(f"  - {path}")
        print("\nPlease update config/application.toml and config/{{ environment }}.toml with the required values.")
        return False
    
    return True

def provision_environment(environment: str):
    """Provision Azure resources for the specified environment"""
    # Load and validate configuration
    config = load_config(environment)
    if not validate_config(config):
        return

    print(f"\nProvisioning environment: {environment}")
    print("\nConfiguration:")
    for key, value in config['azure'].items():
        print(f"  {key}: {value}")

    # Check if resource group exists
    print("\nChecking if resource group exists...")
    try:
        result = subprocess.run([
            "az", "group", "show",
            "--name", config['azure']['resource_group'],
            "--query", "location",
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Creating resource group...")
            subprocess.run([
                "az", "group", "create",
                "--name", config['azure']['resource_group'],
                "--location", config['azure']['location']
            ], check=True)
        else:
            existing_location = result.stdout.strip().lower().replace(" ", "")
            desired_location = config['azure']['location'].lower()
            if existing_location != desired_location:
                print(f"⛔️ Error: Resource group '{config['azure']['resource_group']}' exists in location '{existing_location}', but we need it in '{desired_location}'")
                print("Please either:")
                print(f"1. Update the location in your config to '{existing_location}'")
                print(f"2. Delete the existing resource group and run provision again to create it in '{desired_location}'")
                return
            print(f"Resource group '{config['azure']['resource_group']}' already exists in {existing_location}")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to create resource group")
        print(f"Details: {e}")
        return

    # Check if storage account exists
    storage_account_name = config['azure']['storage_account'][:24]
    print(f"\nChecking if storage account exists ({storage_account_name})...")
    try:
        result = subprocess.run([
            "az", "storage", "account", "show",
            "--name", storage_account_name,
            "--query", "location",
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Creating storage account...")
            subprocess.run([
                "az", "storage", "account", "create",
                "--name", storage_account_name,
                "--location", config['azure']['location'],
                "--resource-group", config['azure']['resource_group'],
                "--sku", "Standard_LRS"
            ], check=True)
        else:
            existing_location = result.stdout.strip().lower().replace(" ", "")
            desired_location = config['azure']['location'].lower()
            if existing_location != desired_location:
                print(f"⛔️ Error: Storage account '{storage_account_name}' exists in location '{existing_location}', but we need it in '{desired_location}'")
                print("Please either:")
                print(f"1. Update the location in your config to '{existing_location}'")
                print(f"2. Delete the existing storage account and run provision again to create it in '{desired_location}'")
                return
            print(f"Storage account '{storage_account_name}' already exists in {existing_location}")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to create storage account")
        print(f"Details: {e}")
        return

    # Check if App Service Plan exists
    print("\nChecking if App Service Plan exists...")
    try:
        result = subprocess.run([
            "az", "appservice", "plan", "show",
            "--name", config['azure']['app_service_plan'],
            "--resource-group", config['azure']['resource_group'],
            "--query", "location",
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Creating App Service Plan...")
            subprocess.run([
                "az", "appservice", "plan", "create",
                "--name", config['azure']['app_service_plan'],
                "--resource-group", config['azure']['resource_group'],
                "--location", config['azure']['location'],
                "--sku", "B1",
                "--is-linux"
            ], check=True)
        else:
            existing_location = result.stdout.strip().lower().replace(" ", "")
            desired_location = config['azure']['location'].lower()
            if existing_location != desired_location:
                print(f"⛔️ Error: App Service Plan '{config['azure']['app_service_plan']}' exists in location '{existing_location}', but we need it in '{desired_location}'")
                print("Please either:")
                print(f"1. Update the location in your config to '{existing_location}'")
                print(f"2. Delete the existing App Service Plan and run provision again to create it in '{desired_location}'")
                return
            print(f"App Service Plan '{config['azure']['app_service_plan']}' already exists in {existing_location}")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to create App Service Plan")
        print(f"Details: {e}")
        return

    # Check if Function App exists
    print("\nChecking if Function App exists...")
    try:
        result = subprocess.run([
            "az", "functionapp", "show",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['function_app'],
            "--query", "name",
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            # Create Function App
            print("Creating Function App...")
            subprocess.run([
                "az", "functionapp", "create",
                "--resource-group", config['azure']['resource_group'],
                "--name", config['azure']['function_app'],
                "--storage-account", config['azure']['storage_account'],
                "--plan", config['azure']['app_service_plan'],
                "--runtime", "python",
                "--runtime-version", "3.11",
                "--functions-version", "4",
                "--os-type", "linux"
            ], check=True)
        else:
            print(f"Function App '{config['azure']['function_app']}' already exists")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to create Function App")
        print(f"Details: {e}")
        return

    # Create Key Vault if it doesn't exist
    print("\nChecking if Key Vault exists...")
    try:
        # Check if Key Vault exists
        result = subprocess.run([
            "az", "keyvault", "show",
            "--name", config['azure']['key_vault_name'],
            "--query", "name",
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Creating Key Vault...")
            subprocess.run([
                "az", "keyvault", "create",
                "--name", config['azure']['key_vault_name'],
                "--resource-group", config['azure']['resource_group'],
                "--location", config['azure']['location'],
                "--enable-rbac-authorization", "false"  # Use access policies instead of RBAC
            ], check=True)
        else:
            # Check if the vault uses RBAC
            result = subprocess.run([
                "az", "keyvault", "show",
                "--name", config['azure']['key_vault_name'],
                "--query", "properties.enableRbacAuthorization",
                "-o", "tsv"
            ], capture_output=True, text=True, check=True)
            if result.stdout.strip().lower() == 'true':
                print("⛔️ Error: Key Vault is configured with RBAC authorization. Please use a vault with access policies.")
                return
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to create/check Key Vault")
        print(f"Details: {e}")
        return

    # Get Function App's managed identity
    print("\nConfiguring Function App's managed identity...")
    try:
        # First assign managed identity
        subprocess.run([
            "az", "functionapp", "identity", "assign",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['function_app']
        ], check=True)

        # Then get the principal ID
        result = subprocess.run([
            "az", "functionapp", "identity", "show",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['function_app'],
            "--query", "principalId",
            "-o", "tsv"
        ], capture_output=True, text=True, check=True)
        principal_id = result.stdout.strip()
        
        if not principal_id:
            print("⛔️ Error: Failed to get function app's managed identity")
            return
        
        print("✅ Managed identity configured")

        # Set Key Vault policy
        print("\nConfiguring Key Vault access...")
        subprocess.run([
            "az", "keyvault", "set-policy",
            "--name", config['azure']['key_vault_name'],
            "--secret-permissions", "get", "list",
            "--object-id", principal_id
        ], check=True)
        
        print("✅ Key Vault access configured")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to configure Key Vault access")
        print(f"Details: {e}")
        return

    # Create Log Analytics Workspace if it doesn't exist
    print("\nEnsuring Log Analytics Workspace exists...")
    try:
        # Try to get workspace ID
        result = subprocess.run([
            "az", "monitor", "log-analytics", "workspace", "show",
            "--resource-group", config['azure']['resource_group'],
            "--workspace-name", config['azure']['log_analytics_workspace'],
            "--query", "id",
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            # Workspace doesn't exist, create it
            print("Creating Log Analytics Workspace...")
            subprocess.run([
                "az", "monitor", "log-analytics", "workspace", "create",
                "--resource-group", config['azure']['resource_group'],
                "--workspace-name", config['azure']['log_analytics_workspace']
            ], check=True)
    except subprocess.CalledProcessError:
        print("⛔️ Error: Failed to create Log Analytics Workspace")
        return

    # Create Application Insights
    print("\nCreating Application Insights...")
    try:
        subprocess.run([
            "az", "monitor", "app-insights", "component", "create",
            "--resource-group", config['azure']['resource_group'],
            "--app", config['azure']['function_app'],
            "--location", config['azure']['location'],
            "--kind", "web"
        ], check=True)

        # Get instrumentation key and update function app
        print("Configuring Application Insights for Function App...")
        result = subprocess.run([
            "az", "monitor", "app-insights", "component", "show",
            "--resource-group", config['azure']['resource_group'],
            "--app", config['azure']['function_app'],
            "--query", "instrumentationKey",
            "-o", "tsv"
        ], check=True, capture_output=True, text=True)
        instrumentation_key = result.stdout.strip()

        # Configure Function App settings
        subprocess.run([
            "az", "functionapp", "config", "appsettings", "set",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['function_app'],
            "--settings",
            f"APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey={instrumentation_key}"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to configure Application Insights")
        print(f"Details: {e}")
        return

    print("\n✨ Azure resources have been provisioned successfully!")
    print(f"\nResource Group: {config['azure']['resource_group']}")
    print(f"Storage Account: {storage_account_name}")
    print(f"App Service Plan: {config['azure']['app_service_plan']}")
    print(f"Function App: {config['azure']['function_app']}")
    print(f"Key Vault: {config['azure']['key_vault_name']}")
    print(f"Log Analytics Workspace: {config['azure']['log_analytics_workspace']}")
    print("\nApplication is ready to be deployed!")

def check_az_cli() -> bool:
    """Check if Azure CLI is installed"""
    try:
        subprocess.run(["az", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⛔️ Error: Azure CLI is not installed.")
        print("\nTo install:")
        print("  brew update && brew install azure-cli")
        print("\nOr visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
        return False

def az_login() -> bool:
    """Ensure user is logged into Azure CLI"""
    try:
        # Check if already logged in
        subprocess.run(["az", "account", "show"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print("Logging into Azure...")
        try:
            subprocess.run(["az", "login"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("⛔️ Error: Failed to log in to Azure.")
            return False

def register_providers() -> List[str]:
    """Register required Azure resource providers"""
    providers = [
        "Microsoft.Web",
        "Microsoft.KeyVault",
        "Microsoft.Insights",
        "Microsoft.Storage"  # Added as it's commonly needed
    ]
    
    print("Registering Azure resource providers...")
    for provider in providers:
        try:
            subprocess.run(["az", "provider", "register", "--namespace", provider], check=True)
        except subprocess.CalledProcessError:
            print(f"⛔️ Error: Failed to register provider {provider}")
            return []
    
    return providers

def wait_for_providers(providers: List[str]):
    """Wait for all providers to finish registering"""
    print("Waiting for providers to finish registering. This may take a few minutes...")
    
    while providers:
        for provider in providers[:]:  # Create a copy to modify during iteration
            try:
                result = subprocess.run(
                    ["az", "provider", "show", "-n", provider, "--query", "registrationState", "-o", "tsv"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                state = result.stdout.strip()
                
                if state == "Registered":
                    print(f"✓ {provider} registered successfully")
                    providers.remove(provider)
                elif state == "Failed":
                    print(f"✗ {provider} registration failed")
                    providers.remove(provider)
                else:
                    print(f"⋯ {provider} is {state}")
            except subprocess.CalledProcessError:
                print(f"⛔️ Error: Failed to check status of {provider}")
                providers.remove(provider)
        
        if providers:
            time.sleep(10)  # Wait before checking again

def run(args):
    parser = argparse.ArgumentParser(description='Provision Azure resources')
    parser.add_argument('environment', nargs='?', default='development',
                       help='Environment to provision (default: development)')
    parser.add_argument('--skip-registration', action='store_true',
                       help='Skip Azure provider registration and login steps')
    args = parser.parse_args(args)

    if not args.skip_registration:
        # Check prerequisites
        if not check_az_cli():
            sys.exit(1)

        # Ensure logged in
        if not az_login():
            sys.exit(1)

        # Register providers
        providers = register_providers()
        if not providers:
            sys.exit(1)

        # Wait for registration to complete
        wait_for_providers(providers)

        print(f"\n✨ Azure resource providers are ready!")
    
    # Provision the environment
    provision_environment(args.environment)
