from typing import Dict, Any, List
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
            
        # Validate required configuration
        if not self.validate_config(
            'azure.resource_group',
            'azure.function_app'
        ):
            return

        # Check if app exists
        if not self.check_resource_exists('functionapp', self.config.azure.function_app, self.config.azure.resource_group):
            self.error(f"Function app '{self.config.azure.function_app}' not found")
            self.info("\nTo deploy your app:")
            self.info("1. Run 'legend provision' to create Azure resources")
            self.info("2. Run 'legend deploy' to deploy your code")
            return

        # Get host name for URLs - do this early to verify app is accessible
        hostname = self.get_hostname(self.config.azure.resource_group, self.config.azure.function_app)
        if not hostname:
            return

        self.info(f"\nFunction App: {self.config.azure.function_app}")
        self.info(f"Resource Group: {self.config.azure.resource_group}")
        
        # Get host keys (including master key)
        host_keys = self.get_host_keys(self.config.azure.resource_group, self.config.azure.function_app)
        if host_keys:
            self.info("\nHost Keys:")
            # Master key is returned directly as a string
            master_key = host_keys.get('masterKey')
            if master_key is not None:
                self.info(f"  🔑 Master Key: {master_key}")
            
            # Function keys are returned as a dictionary
            function_keys = host_keys.get('functionKeys', {})
            if isinstance(function_keys, dict):
                # Filter out None values
                valid_keys = {k: v for k, v in function_keys.items() if v is not None}
                for key_name, key_value in valid_keys.items():
                    self.info(f"  🔑 {key_name}: {key_value}")
                
        self.info("\nFunctions:")

        # Get list of functions
        functions = self.get_functions(self.config.azure.resource_group, self.config.azure.function_app)
        if not functions:
            self.info("No functions found. Deploy your code first using 'legend deploy'")
            return

        # For each function, show details and keys
        for func in functions:
            # Get function name from the full name (app/function)
            full_name = func.get('name', '')
            name = full_name.split('/')[-1] if '/' in full_name else full_name
            if not name:
                continue
                
            self.info(f"\n{name}:")
            self.info(f"  Invoke URL: {func.get('invokeUrlTemplate', 'unknown')}")
            
            # Get function keys
            keys = self.get_function_keys(self.config.azure.resource_group, 
                                        self.config.azure.function_app, 
                                        name)
            # Filter out None values
            valid_keys = {k: v for k, v in keys.items() if v is not None}

            self.info("  URLs with keys:")
            # Add app-level master key if available
            if host_keys and host_keys.get('masterKey') is not None:
                self.info(f"  🔑 App Master Key:")
                self.info(f"    {func.get('invokeUrlTemplate')}?code={host_keys['masterKey']}")
                
            # Add app-level default key if available
            app_default_key = host_keys.get('functionKeys', {}).get('default')
            if app_default_key is not None:
                self.info(f"  🔑 App Default Key:")
                self.info(f"    {func.get('invokeUrlTemplate')}?code={app_default_key}")
                
            # Add function-specific keys
            if valid_keys:
                for key_name, key_value in valid_keys.items():
                    self.info(f"  🔑 Function {key_name}:")
                    self.info(f"    {func.get('invokeUrlTemplate')}?code={key_value}")
