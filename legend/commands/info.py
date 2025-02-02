import argparse
import subprocess
import json
from typing import Dict, Any, List
from ..lib.config import load_config

def check_app_exists(resource_group: str, app_name: str) -> bool:
    """Check if the function app exists in Azure"""
    try:
        result = subprocess.run([
            "az", "functionapp", "show",
            "--resource-group", resource_group,
            "--name", app_name,
            "--query", "defaultHostName",
            "-o", "tsv"
        ], capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def get_functions(resource_group: str, app_name: str) -> List[Dict[str, Any]]:
    """Get list of functions in the app"""
    try:
        result = subprocess.run([
            "az", "functionapp", "function", "list",
            "--resource-group", resource_group,
            "--name", app_name,
            "-o", "json"
        ], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to list functions")
        print(f"Details: {e}")
        return []



def get_function_keys(resource_group: str, app_name: str, function_name: str) -> Dict[str, str]:
    """Get function keys for a specific function"""
    try:
        result = subprocess.run([
            "az", "functionapp", "function", "keys", "list",
            "--resource-group", resource_group,
            "--name", app_name,
            "--function", function_name,
            "-o", "json"
        ], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to get keys for function {function_name}")
        print(f"Details: {e}")
        return {}

def get_host_keys(resource_group: str, app_name: str) -> Dict[str, str]:
    """Get host keys including master key"""
    try:
        result = subprocess.run([
            "az", "functionapp", "keys", "list",
            "--resource-group", resource_group,
            "--name", app_name,
            "-o", "json"
        ], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print("⚠️  Warning: Failed to get host keys")
        print(f"Details: {e}")
        return {}

def run(args):
    """Show information about the deployed function app"""
    parser = argparse.ArgumentParser(description='Show information about the deployed function app')
    parser.add_argument('environment', help='Environment to show info for (e.g., development, test, sit)')
    args = parser.parse_args(args)

    # Load configuration
    config = load_config(args.environment)
    if not config:
        print(f"Error: Could not load configuration for environment '{args.environment}'")
        return

    # Check if app exists
    if not check_app_exists(config['azure']['resource_group'], config['azure']['function_app']):
        print(f"⛔️ Error: Function app '{config['azure']['function_app']}' not found")
        print("\nTo deploy your app:")
        print("1. Run 'legend provision' to create Azure resources")
        print("2. Run 'legend deploy' to deploy your code")
        return

    print(f"\nFunction App: {config['azure']['function_app']}")
    print(f"Resource Group: {config['azure']['resource_group']}")
    
    # Get host keys (including master key)
    host_keys = get_host_keys(config['azure']['resource_group'], config['azure']['function_app'])
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
    functions = get_functions(config['azure']['resource_group'], config['azure']['function_app'])
    if not functions:
        print("No functions found. Deploy your code first using 'legend deploy'")
        return

    # Get host name for URLs
    try:
        result = subprocess.run([
            "az", "functionapp", "show",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['function_app'],
            "--query", "defaultHostName",
            "-o", "tsv"
        ], capture_output=True, text=True, check=True)
        host_name = result.stdout.strip()
    except subprocess.CalledProcessError:
        print("⛔️ Error: Failed to get function app hostname")
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
        keys = get_function_keys(config['azure']['resource_group'], config['azure']['function_app'], name)
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
