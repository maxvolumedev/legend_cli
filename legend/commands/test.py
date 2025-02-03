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
        self.info("Running tests with pytest...")
        
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
            result = subprocess.run(
                [venv_python, "-m", "pytest"] + args.pytest_args,
                check=False,
                env=env,
                capture_output=True,
                text=True
            )
            
            # Print test output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
                
            # Report test status
            if result.returncode == 0:
                self.success("All tests passed!")
            else:
                self.error(f"Tests failed with exit code {result.returncode}")
                
            return result.returncode
            
        except subprocess.CalledProcessError as e:
            self.error(f"Failed to run tests: {e}")
            return 1
        except Exception as e:
            self.error(f"Unexpected error running tests: {e}")
            return 1


# Command instance to be used by the CLI
command = TestCommand()
