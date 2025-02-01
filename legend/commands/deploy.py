import argparse
import subprocess
import sys
import json
from pathlib import Path
from ..lib.config import load_config

def run(args):
    """Deploy the current function app to Azure"""
    parser = argparse.ArgumentParser(description='Deploy function app to Azure')
    parser.add_argument('environment', help='Environment to deploy to (e.g., development, test, sit)')
    args = parser.parse_args(args)

    # Load configuration
    config = load_config(args.environment)
    if not config:
        print(f"Error: Could not load configuration for environment '{args.environment}'")
        return

    print(f"\nDeploying to environment: {args.environment}")
    print(f"Resource Group: {config['azure']['resource_group']}")
    print(f"Function App: {config['azure']['app_name']}")

    # Check if git deployment is already configured
    print("\nChecking git deployment configuration...")
    try:
        result = subprocess.run([
            "az", "functionapp", "deployment", "source", "show",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['app_name'],
            "--query", "repoUrl",
            "-o", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Git deployment already configured")
            git_url = result.stdout.strip()
        else:
            print("Configuring git deployment...")
            result = subprocess.run([
                "az", "functionapp", "deployment", "source", "config-local-git",
                "--resource-group", config['azure']['resource_group'],
                "--name", config['azure']['app_name']
            ], capture_output=True, text=True, check=True)
            git_url = json.loads(result.stdout)['url']
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to configure git deployment")
        print(f"Details: {e}")
        return
    except (json.JSONDecodeError, KeyError) as e:
        print("⛔️ Error: Failed to parse git URL from Azure response")
        print(f"Details: {e}")
        return

    # Get publishing credentials
    print("Getting deployment credentials...")
    try:
        result = subprocess.run([
            "az", "webapp", "deployment", "list-publishing-credentials",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['app_name'],
            "--query", "publishingUserName, publishingPassword",
            "-o", "tsv"
        ], capture_output=True, text=True, check=True)
        username, password = result.stdout.strip().split()
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to get publishing credentials")
        print(f"Details: {e}")
        return
    except ValueError as e:
        print("⛔️ Error: Failed to parse publishing credentials")
        print(f"Details: {e}")
        return

    # Construct git URL with credentials
    git_url_with_auth = git_url.replace("https://None@", f"https://{username}:{password}@")
    remote_name = f"azure-{args.environment}"

    # Add/update git remote
    print(f"\nConfiguring git remote '{remote_name}'...")
    try:
        # Check if remote exists
        result = subprocess.run(["git", "remote", "get-url", remote_name], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            # Update existing remote
            subprocess.run(["git", "remote", "set-url", remote_name, git_url_with_auth],
                         check=True)
        else:
            # Add new remote
            subprocess.run(["git", "remote", "add", remote_name, git_url_with_auth],
                         check=True)
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to configure git remote")
        print(f"Details: {e}")
        return

    # Push to Azure
    print(f"\nPushing to {args.environment}...")
    try:
        subprocess.run(["git", "push", remote_name, "main:master"], check=True)
        print(f"\n✨ Successfully deployed to {args.environment}!")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to push to Azure")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you have committed all your changes")
        print("2. If this is your first deployment, you may need to push with -f:")
        print(f"   git push -f {remote_name} main:master")
        return
