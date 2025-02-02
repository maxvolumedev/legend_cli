import os
import subprocess
import argparse
import json
import re
from pathlib import Path
import os
from ..lib.config import load_config

def clean_git_url(url: str) -> str:
    """Remove any credentials from git URL"""
    return re.sub(r'https://[^@]*@', 'https://', url)

def run(args):
    """Deploy the current function app to Azure"""
    parser = argparse.ArgumentParser(description='Deploy function app to Azure')
    parser.add_argument('environment', help='Environment to deploy to (e.g., development, test, sit)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show additional deployment information')
    args = parser.parse_args(args)

    # Load configuration
    config = load_config(args.environment)
    if not config:
        print(f"⛔️ Error: Could not load configuration for environment '{args.environment}'")
        return

    print(f"\nDeploying to environment: {args.environment}")
    print(f"Resource Group: {config['azure']['resource_group']}")
    print(f"Function App: {config['azure']['function_app']}")

    # Get Git deployment URL with embedded credentials
    print("\nGetting deployment URL...")
    try:
        result = subprocess.run([
            "az", "webapp", "deployment", "list-publishing-credentials",
            "--resource-group", config['azure']['resource_group'],
            "--name", config['azure']['function_app'],
            "--query", "scmUri",
            "-o", "tsv"
        ], capture_output=True, text=True, check=True)
        
        git_url = result.stdout.strip()
        if not git_url:
            print("⛔️ Error: Failed to get deployment URL")
            return
            
        # Append <app_name>.git to the URL
        git_url = f"{git_url}/{config['azure']['function_app']}.git"
        print("✅ Got deployment URL")
        if args.verbose:
            # Show full URL in verbose mode
            print(f"Deployment URL: {git_url}")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to get deployment URL")
        print(f"Details: {e}")
        return

    # Push to Azure
    print(f"\nPushing to {args.environment}...")
    try:
        result = subprocess.run(
            ["git", "push", git_url, "main:master"],
            check=True
        )
        print(f"\n✨ Successfully deployed to {args.environment}!")
    except subprocess.CalledProcessError as e:
        print("⛔️ Error: Failed to push to Azure")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you have committed all your changes")
        print("2. If this is your first deployment, you may need to push with -f:")
        print(f"   git push -f {git_url} main:master")
        return
