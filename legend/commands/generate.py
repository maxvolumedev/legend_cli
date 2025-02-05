import os
import json
from pathlib import Path
from .base import Command


class GenerateCommand(Command):
    """Command to generate new Azure Functions and other components"""

    def __init__(self):
        super().__init__(
            name='generate',
            description='Generate a new Azure Function or other components',
            aliases=['g']
        )

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='type', required=True)

        # Function subcommand
        func_parser = subparsers.add_parser(
            'function', 
            aliases=['f'], 
            help='Add a new Function to the project (will be added to function_app.py)'
        )
        func_parser.add_argument(
            'name', 
            help='Name of the function'
        )
        func_parser.add_argument(
            '--template', '-t', 
            default='HTTP trigger',
            help='Function template to use (default: HTTP trigger)'
        )
        func_parser.add_argument(
            '--authlevel',
            choices=['function', 'anonymous', 'admin'],
            default='function',
            help='Authorization level for the function (default: function)'
        )
        func_parser.add_argument(
            '--skip_test',  
            default=False,
            action='store_true',
            help='Skip generating the test file'
        )

        # Workflow subcommand
        workflow_parser = subparsers.add_parser(
            'github-workflow',
            help='Generate and configure a new CI/CD GitHub deployment workflow for an environment'
        )
        workflow_parser.add_argument(
            'environment', 
            help='Environment to configure for github workflow (e.g., sit, uat, production)'
        )


    def generate_function(self, name: str, template: str, authlevel: str = None, skip_test: bool = False):
        """Generate a new Azure Function.
        
        Args:
            name: Name of the function
            template: Template to use (e.g. 'HTTP trigger')
            authlevel: Authorization level (function, anonymous, or admin)
            skip_test: Whether to skip generating the test file
        """
        self.info(f"Generating function: {name} (template: {template}, auth level: {authlevel.upper()})")

        # Run func new
        try:
            cmd = [
                    "func",
                    "new",
                    "--name", name,
                    "--template", template,                    
                ]

            if authlevel:
                cmd.extend(["--authlevel", authlevel.upper()])
            self.run_subprocess(cmd, capture_output=False)
        except Exception as e:
            self.error(f"Failed to generate function: {e}")
            return False        

        if not skip_test:
            # Generate test file
            try:
                self.info("Generating test file: test/functions/{name}_test.py")
                self.render_template(
                    "test/function.py",
                    f"test/functions/{name}_test.py",
                    {"function_name": name}
            )
            except Exception:
                return False

        self.completed(f"Function '{name}' generated successfully!")
        return True

    def is_gh_logged_in(self):
        result = self.run_subprocess(["gh", "auth", "status"])
        return result.returncode == 0  # 0 means success, non-zero means failure


    def generate_github_workflow(self, env):
        # generate new github workflow template from templates/.github/deploy.yml to .github/workflows/deploy-<env>.yml
        self.render_template(
            ".github/workflows/deploy.yml",
            f".github/workflows/deploy-{env}.yml",
            {
                "app_name": self.config.azure.function_app,
                "environment": env
            }
        )

        # get fully qualified id for the resource group
        resource_group_id = self.run_azure_command(
            [
                "az",
                "group",
                "show",
                "--name", self.config.azure.resource_group,
                "--query", "id",
                "-o", "tsv"
            ]
        )

        # create azure service principal
        principal = self.run_subprocess(
            [
                "az",
                "ad",
                "sp",
                "create-for-rbac",
                "--name", f"{self.config.azure.function_app}-sp",
                "--role", "Contributor",
                "--scopes", resource_group_id,
                "--sdk-auth",
                "-o", "json"
            ]
        ).stdout.replace("\n"," ")
        print(principal)

        if not self.is_gh_logged_in():
            # log in to github
            self.run_subprocess(
                [
                    "gh",
                    "auth",
                    "login"
                ],
                capture_output=False
            )

        # configure github secret using gh
        self.run_subprocess(
            [
                "gh",
                "secret",
                "set",
                f"AZURE_CREDENTIALS_{ env.upper() }"
            ],
            input=principal,
            text=True,
            check=True
        )
        

    def handle(self, args):
        if args.type in ['function', 'f']:
            return 0 if self.generate_function(args.name, args.template, args.authlevel, args.skip_test) else 1
        elif args.type in ['github-workflow', 'w']:
            if not self.load_config(args.environment):
                return 1
            return 0 if self.generate_github_workflow(args.environment) else 1
        else:
            self.error(f"Unknown generation type: {args.type}")
            return 1
