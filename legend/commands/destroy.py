import argparse
import subprocess
from ..lib.config import load_config

def run(args):
    """Delete all Azure resources for an environment"""
    parser = argparse.ArgumentParser(description='Delete all Azure resources for an environment')
    parser.add_argument('environment', help='Environment to delete (e.g., sit, uat, production)')
    args = parser.parse_args(args)

    # Load configuration
    config = load_config(args.environment)
    if not config:
        print(f"⛔️ Error: Could not load configuration for environment '{args.environment}'")
        return

    print(f"\n🟡  WARNING: This will delete ALL resources in environment: {args.environment}")
    print(f"Resource Group: {config['azure']['resource_group']}")
    print(f"Function App: {config['azure']['function_app']}")
    print("\nThis action cannot be undone!")

    # First confirmation
    confirm = input("\nAre you sure you want to proceed? (y/N): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        return

    # Second confirmation - must type app name
    print(f"\n\033[91mTo confirm, please type the function app name ({config['azure']['function_app']}):\033[0m")
    app_name = input("> ")
    if app_name != config['azure']['function_app']:
        print("⛔️ Error: App name does not match. Aborted.")
        return

    # Delete resource group
    print(f"\nDeleting resource group {config['azure']['resource_group']}...")
    try:
        subprocess.run([
            "az", "group", "delete",
            "--name", config['azure']['resource_group'],
            "--yes",  # Auto-confirm the Azure CLI prompt
            "--no-wait"  # Don't wait for completion
        ], check=True)
        print("✅ Resource group deletion started")
        print("\nNote: Deletion may take several minutes to complete")
        print("Check the Azure portal for status")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to delete resource group")
        print(f"Details: {e}")
        return
