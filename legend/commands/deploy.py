import re
from pathlib import Path
from ..lib.config import load_config
from .base import Command


def clean_git_url(url: str) -> str:
    """Remove any credentials from git URL"""
    return re.sub(r'https://[^@]*@', 'https://', url)


class DeployCommand(Command):
    """Deploy function app to Azure"""

    def __init__(self):
        super().__init__(
            name='deploy',
            description='Deploy function app to Azure'
        )

    def add_arguments(self, parser):
        parser.add_argument('environment',
                          help='Environment to deploy to (e.g., development, test, sit)')

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

        self.info(f"\nDeploying to environment: {args.environment}")
        self.info(f"Resource Group: {config.azure.resource_group}")
        self.info(f"Function App: {config.azure.function_app}")

        # Get Git deployment URL with embedded credentials
        self.info("\nGetting deployment URL...")
        result = self.run_subprocess([
            "az", "webapp", "deployment", "list-publishing-credentials",
            "--resource-group", config.azure.resource_group,
            "--name", config.azure.function_app,
            "--query", "scmUri",
            "-o", "tsv"
        ])
        
        if not result:
            self.error("Failed to get deployment URL")
            return
            
        git_url = result.stdout.strip()
        if not git_url:
            self.error("Failed to get deployment URL - empty response")
            return
            
        # Append <app_name>.git to the URL
        git_url = f"{git_url}/{config.azure.function_app}.git"
        self.success("Got deployment URL")
        if self.verbose:
            # Show full URL in verbose mode
            self.info(f"Deployment URL: {git_url}")

        # Push to Azure
        self.info(f"\nPushing branch {config.branch} to {args.environment}...")
        result = self.run_subprocess(["git", "push", git_url, f"{config.branch}:master"])
        
        if not result:
            self.error("Failed to push to Azure")
            self.info("\nTroubleshooting:")
            self.info("1. Ensure you have committed all your changes")
            self.info("2. If this is your first deployment, you may need to push with -f:")
            self.info(f"   git push -f {git_url} main:master")
            return

        self.completed(f"Successfully deployed to {args.environment}!")


command = DeployCommand()
