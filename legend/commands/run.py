import sys
from pathlib import Path
from .base import Command


class RunCommand(Command):
    """Command to run the Function App locally"""

    def __init__(self):
        super().__init__(
            name='run',
            description='Run the Function App locally',
            aliases=['r']
        )

    def add_arguments(self, parser):
        # No additional arguments needed since verbose is handled by base Command
        pass

    def handle(self, args):
        # Check if function_app.py exists
        if not Path('function_app.py').exists():
            self.error("function_app.py not found in current directory")
            return 1

        # Build command
        cmd = ["func", "start"]
        if self.verbose:
            cmd.append("--verbose")

        self.info("Starting function app...")
        try:
            return self.run_subprocess(
                cmd,
                check=False,
                capture_output=False,  # Don't capture output (allows streaming)
                stdout=None,           # Use parent process stdout
                stderr=None           # Use parent process stderr
            )
        except KeyboardInterrupt:
            self.info("\nStopping function app...")
            return 0


# Command instance to be used by the CLI
command = RunCommand()
