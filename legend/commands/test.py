import subprocess
import argparse
import sys
import os
from .base import Command

class TestCommand(Command):
    """Run tests using pytest"""

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
        # Set test environment
        os.environ['LEGEND_ENVIRONMENT'] = 'test'

        # Build pytest command
        pytest_cmd = [sys.executable, '-m', 'pytest']
        
        # Add any additional pytest arguments
        if args.pytest_args:
            pytest_cmd.extend(args.pytest_args)

        # Run pytest with all arguments
        return subprocess.call(pytest_cmd)
