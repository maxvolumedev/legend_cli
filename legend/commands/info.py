from typing import Dict, Any, List
from ..lib.config import load_config
from .base import Command

class InfoCommand(Command):
    """Command to show information about the deployed function app"""

    def __init__(self):
        super().__init__(
            name='info',
            description='Show information about the deployed function app',
            aliases=['i']
        )

    def add_arguments(self, parser):
        parser.add_argument('environment', 
                          help='Environment to show info for (e.g., development, test, sit)')



    def get_functions(self, resource_group: str, app_name: str) -> List[Dict[str, Any]]:
        """Get list of functions in the app"""
        result = self.run_azure_command([
            "functionapp", "function", "list",
            "--resource-group", resource_group,
            "--name", app_name
        ])
        return result or []

    def get_function_keys(self, resource_group: str, app_name: str, function_name: str) -> Dict[str, str]:
        """Get function keys for a specific function"""
        result = self.run_azure_command([
            "functionapp", "function", "keys", "list",
            "--resource-group", resource_group,
            "--name", app_name,
            "--function", function_name
        ])
        return result or {}

    def get_host_keys(self, resource_group: str, app_name: str) -> Dict[str, str]:
        """Get host keys including master key"""
        result = self.run_azure_command([
            "functionapp", "keys", "list",
            "--resource-group", resource_group,
            "--name", app_name
        ])
        return result or {}

    def get_hostname(self, resource_group: str, app_name: str) -> str:
        """Get the function app's hostname"""
        result = self.run_azure_command([
            "functionapp", "show",
            "--resource-group", resource_group,
            "--name", app_name,
            "--query", "defaultHostName",
            "-o", "tsv"
        ])
        return result or ""

    def handle(self, args):
        if not self.validate_environment(args.environment):
            return

        # Load configuration
        config = load_config(args.environment)
        if not config:
            return

        # Check if app exists
        if not self.check_resource_exists('functionapp', config.azure.function_app, config.azure.resource_group):
            self.error(f"Function app '{config.azure.function_app}' not found")
            print("\nTo deploy your app:")
            print("1. Run 'legend provision' to create Azure resources")
            print("2. Run 'legend deploy' to deploy your code")
            return

        # Get host name for URLs - do this early to verify app is accessible
        hostname = self.get_hostname(config.azure.resource_group, config.azure.function_app)
        if not hostname:
            return

        print(f"\nFunction App: {config.azure.function_app}")
        print(f"Resource Group: {config.azure.resource_group}")
        
        # Get host keys (including master key)
        host_keys = self.get_host_keys(config.azure.resource_group, config.azure.function_app)
        if host_keys:
            print("\nHost Keys:")
            # Master key is returned directly as a string
            master_key = host_keys.get('masterKey')
            if master_key is not None:
                print(f"  🔑 Master Key: {master_key}")
            
            # Function keys are returned as a dictionary
            function_keys = host_keys.get('functionKeys', {})
            if isinstance(function_keys, dict):
                # Filter out None values
                valid_keys = {k: v for k, v in function_keys.items() if v is not None}
                for key_name, key_value in valid_keys.items():
                    print(f"  🔑 {key_name}: {key_value}")
                
        print("\nFunctions:")

        # Get list of functions
        functions = self.get_functions(config.azure.resource_group, config.azure.function_app)
        if not functions:
            print("No functions found. Deploy your code first using 'legend deploy'")
            return

        # For each function, show details and keys
        for func in functions:
            # Get function name from the full name (app/function)
            full_name = func.get('name', '')
            name = full_name.split('/')[-1] if '/' in full_name else full_name
            if not name:
                continue
                
            print(f"\n{name}:")
            print(f"  Invoke URL: {func.get('invokeUrlTemplate', 'unknown')}")
            
            # Get function keys
            keys = self.get_function_keys(config.azure.resource_group, 
                                        config.azure.function_app, 
                                        name)
            # Filter out None values
            valid_keys = {k: v for k, v in keys.items() if v is not None}

            print("  URLs with keys:")
            # Add app-level master key if available
            if host_keys and host_keys.get('masterKey') is not None:
                print(f"  🔑 App Master Key:")
                print(f"    {func.get('invokeUrlTemplate')}?code={host_keys['masterKey']}")
                
            # Add app-level default key if available
            app_default_key = host_keys.get('functionKeys', {}).get('default')
            if app_default_key is not None:
                print(f"  🔑 App Default Key:")
                print(f"    {func.get('invokeUrlTemplate')}?code={app_default_key}")
                
            # Add function-specific keys
            if valid_keys:
                for key_name, key_value in valid_keys.items():
                    print(f"  🔑 Function {key_name}:")
                    print(f"    {func.get('invokeUrlTemplate')}?code={key_value}")

# Command instance to be used by the CLI
command = InfoCommand()
