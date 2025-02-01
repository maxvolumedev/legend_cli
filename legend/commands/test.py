import subprocess
import sys
import os
import argparse

def run(args):
    parser = argparse.ArgumentParser(description='Run tests with pytest')
    parser.add_argument('pytest_args', nargs='*', help='Arguments to pass to pytest')
    args = parser.parse_args(args)

    print("Running tests with pytest...")
    venv_python = ".venv/bin/python" if os.name != "nt" else ".venv\\Scripts\\python.exe"
    
    # Set test environment
    env = os.environ.copy()
    env["LEGEND_ENVIRONMENT"] = "test"
    
    result = subprocess.run(
        [venv_python, "-m", "pytest"] + args.pytest_args, 
        check=False,
        env=env
    )
    sys.exit(result.returncode)
