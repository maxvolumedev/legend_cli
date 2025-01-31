import subprocess
import sys
import os

def run(args):
    print("Running tests with pytest...")
    venv_python = ".venv/bin/python" if os.name != "nt" else ".venv\\Scripts\\python.exe"
    result = subprocess.run([venv_python, "-m", "pytest"] + args, check=False)
    sys.exit(result.returncode)
