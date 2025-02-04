import subprocess
import sys
import os
from .base import Command


class TestCommand(Command):
    """Command to run tests with pytest"""

    def __init__(self):
        super().__init__(
            name='test',
            description='Run tests with pytest',
            aliases=['t']
        )

    def add_arguments(self, parser):
        parser.add_argument('pytest_args', 
                          nargs='*', 
                          help='Arguments to pass to pytest')

    def handle(self, args):
        # Use the appropriate Python executable based on OS
        venv_python = ".venv/bin/python" if os.name != "nt" else ".venv\\Scripts\\python.exe"
        
        # Check if virtual environment exists
        if not os.path.exists(venv_python):
            self.error("Virtual environment not found. Run 'legend bootstrap' first")
            return 1
        
        # Set test environment
        env = os.environ.copy()
        env["LEGEND_ENVIRONMENT"] = "test"
        
        try:
            # Run pytest with -v for verbose output and --no-header to suppress pytest header
            result = subprocess.run(
                [venv_python, "-m", "pytest", "-v", "--no-header"] + args.pytest_args,
                check=False,
                env=env,
                text=True
            )
            return result.returncode
            
        except Exception as e:
            self.error(f"Failed to run tests: {e}")
            return 1
