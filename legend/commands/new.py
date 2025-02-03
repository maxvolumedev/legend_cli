import os
from pathlib import Path
from ..lib import names
from .base import Command


class NewCommand(Command):
    """Command to create a new Azure Function App project"""

    def __init__(self):
        super().__init__(
            name='new',
            description='Create a new Azure Function App',
            aliases=['n']
        )
        # Additional dependencies to add to requirements.txt
        self.additional_deps = [
            "jinja2>=3.1.2",
        ]

        # Development dependencies
        self.dev_deps = [
            "git+https://github.com/maxvolumedev/legend_cli.git",  # we don't need to deploy the legend cli
            "tomli>=2.0.1  # For reading TOML configuration files",
            "pytest>=7.4.0",
        ]

    def add_arguments(self, parser):
        parser.add_argument('name', help='Name of the function app')
        parser.add_argument(
            'location', 
            help='Azure location to create the function app in', 
            nargs='?', 
            default='australiasoutheast'
        )

    def check_requirements(self):
        """Check if required tools are installed."""
        # Check if Azure Functions Core Tools is installed
        try:
            self.run_subprocess(["func", "--version"], capture_output=True)
            return True
        except Exception:
            self.error("Azure Functions Core Tools (func CLI) is not installed.")
            self.info("\nTo install:")
            self.info("\n legend bootstrap")
            self.info("\n OR:")
            self.info("  brew install azure-functions-core-tools@4")
            self.info("\nOr visit: https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local")
            return False

    def create_project_structure(self, app_name: str):
        """Create the initial project structure and files."""
        self.info(f"Creating new Azure Function App: {app_name}")

        # Initialize Azure Function
        self.run_subprocess(["func", "init", app_name, "--worker-runtime", "python"])
        
        # Change to app directory
        os.chdir(app_name)

        # Create project directories
        for directory in [".github/workflows", "test", "lib", "config", "bin"]:
            os.makedirs(directory, exist_ok=True)

    def create_dependency_files(self):
        """Create requirements.txt and requirements-dev.txt"""
        # Append additional dependencies to requirements.txt
        with open("requirements.txt", "a") as f:
            f.write("\n\n# Additional dependencies added by Legend CLI\n")
            for dep in self.additional_deps:
                f.write(f"{dep}\n")

        # Create requirements-dev.txt
        with open("requirements-dev.txt", "w") as f:
            f.write("-r requirements.txt\n\n")
            f.write("# Development dependencies\n")
            for dep in self.dev_deps:
                f.write(f"{dep}\n")

    def create_config_files(self, app_name: str, location: str):
        """Create configuration files for all environments."""
        normalized_name = names.normalize_name(app_name)
        
        # Create global application config
        self.render_template(
            "config/application.toml",
            "config/application.toml",
            {
                "app_name": normalized_name,
                "azure_location": location
            }
        )

        # Create environment configuration files
        environments = ["development", "test", "sit", "uat", "production"]
        for environment in environments:
            config_file = f"config/environment-{environment}.toml"
            template_name = "config/environment-local.toml" if environment in ["development", "test"] else "config/environment.toml"
            
            self.render_template(
                template_name,
                config_file,
                {
                    "app_name": normalized_name,
                    "environment": environment,
                    "resource_group": f"{normalized_name}-group-{environment}",
                    "storage_account": names.get_storage_name(normalized_name, environment),
                    "function_app": f"{normalized_name}-{environment}",
                    "app_service_plan": f"{normalized_name}-plan-{environment}",
                    "key_vault_name": names.get_keyvault_name(normalized_name, environment)
                }
            )

    def copy_lib_templates(self, app_name: str):
        """Copy library templates to the project."""
        templates_dir = Path(__file__).parent.parent / "templates"
        lib_templates = templates_dir / "lib"
        if not lib_templates.exists():
            return
            
        for template_path in lib_templates.rglob("*"):
            if not template_path.is_file():
                continue
                
            relative_path = template_path.relative_to(lib_templates)
            target_path = Path("lib") / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            if template_path.suffix == ".py":
                self.render_template(
                    str(Path("lib") / relative_path),
                    str(target_path),
                    {"app_name": app_name}
                )
            else:
                import shutil
                shutil.copy2(template_path, target_path)

    def init_virtual_env(self):
        """Create and initialize virtual environment."""
        self.info("Creating virtual environment...")
        self.run_subprocess(["python", "-m", "venv", ".venv"])
        
        # Install dependencies
        venv_python = ".venv/bin/python" if os.name != "nt" else ".venv\\Scripts\\python.exe"
        self.run_subprocess([venv_python, "-m", "pip", "install", "-r", "requirements-dev.txt"])

    def handle(self, args):
        if not self.check_requirements():
            return 1

        try:
            # Create project structure
            self.create_project_structure(args.name)

            # Create dependency files
            self.create_dependency_files()

            # Create project files from templates
            for template in ["setup.py", "README.md", "bin/legend", ".github/workflows/deploy.yml"]:
                self.render_template(template, template, {"app_name": args.name})
            
            # Make the binstub executable
            Path("bin/legend").chmod(0o755)

            # Create configuration files
            self.create_config_files(args.name, args.location)

            # Copy library templates
            self.copy_lib_templates(args.name)

            # Initialize virtual environment
            self.init_virtual_env()

            # Initialize Git
            self.run_subprocess(["git", "init"])

            self.completed("Created new Legend app!")
            self.info(f"\nNext steps:")
            self.info(f"  cd {args.name}")
            self.info(f"  legend generate function             # Generate a new function")
            self.info(f"  legend test                          # Run tests")
            self.info(f"  legend run                           # Run function app locally")
            self.info(f"  legend console                       # Start interactive console")
            self.info(f"  legend provision                     # Provision Azure resources")
            self.info(f"  legend deploy                        # Deploy to Azure")
            
            return 0

        except Exception as e:
            self.handle_error(e, "Failed to create new app")
            return 1


# Command instance to be used by the CLI
command = NewCommand()
