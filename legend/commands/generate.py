import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .base import Command


class GenerateCommand(Command):
    """Command to generate new Azure Functions and other components"""

    def __init__(self):
        super().__init__(
            name='generate',
            description='Generate a new Azure Function',
            aliases=['g']
        )
        self.templates_dir = Path(__file__).parent.parent / "templates"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='type', required=True)

        # Function subcommand
        func_parser = subparsers.add_parser(
            'function', 
            aliases=['f'], 
            help='Generate a new function'
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

    def generate_function(self, name: str, template: str):
        """Generate a new Azure Function.
        
        Args:
            name: Name of the function
            template: Template to use (e.g. 'HTTP trigger')
        """
        self.info(f"Generating function: {name} (template: {template})")

        # Run func new
        try:
            self.run_subprocess(
                ["func", "new", "--name", name, "--template", template],
                capture_output=False  # Stream output
            )
        except Exception as e:
            self.error(f"Failed to generate function: {e}")
            return False

        # Create test directory
        os.makedirs("test/functions", exist_ok=True)

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

    def handle(self, args):
        if args.type in ['function', 'f']:
            return 0 if self.generate_function(args.name, args.template) else 1
        else:
            self.error(f"Unknown generation type: {args.type}")
            return 1


# Command instance to be used by the CLI
command = GenerateCommand()
