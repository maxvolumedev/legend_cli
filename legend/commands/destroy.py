from ..lib.config import load_config
from .base import Command

class DestroyCommand(Command):
    """Command to delete all Azure resources for an environment"""

    def __init__(self):
        super().__init__(
            name='destroy',
            description='Delete all Azure resources for an environment',
            aliases=[]
        )

    def add_arguments(self, parser):
        parser.add_argument('environment', 
                          help='Environment to delete (e.g., sit, uat, production)')

    def handle(self, args):
        if not self.validate_environment(args.environment):
            return

        # Load configuration
        config = load_config(args.environment)
        if not config:
            return

        self.warning(f"This will delete ALL resources in environment: {args.environment}")
        print(f"Resource Group: {config.azure.resource_group}")
        print(f"Function App: {config.azure.function_app}")
        print("\nThis action cannot be undone!")

        # First confirmation
        confirm = input("\nAre you sure you want to proceed? (y/N): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

        # Second confirmation - must type app name
        print(f"\n\033[91mTo confirm, please type the function app name ({config.azure.function_app}):\033[0m")
        app_name = input("> ")
        if app_name != config.azure.function_app:
            self.error("App name does not match. Aborted.")
            return

        # Delete resource group
        print(f"\nDeleting resource group {config.azure.resource_group}...")
        try:
            self.run_azure_command([
                "group", "delete",
                "--name", config.azure.resource_group,
                "--yes",  # Auto-confirm the Azure CLI prompt
                "--no-wait"  # Don't wait for completion
            ])
            self.success("Resource group deletion started")
            print("\nNote: Deletion may take several minutes to complete")
            print("Check the Azure portal for status")
        except Exception as e:
            self.error(f"Failed to delete resource group: {str(e)}")
            return

# Command instance to be used by the CLI
command = DestroyCommand()
