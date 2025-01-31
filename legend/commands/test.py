import subprocess
import sys

def run(args):
    print("Running tests with pytest...")
    result = subprocess.run(["poetry", "run", "pytest"] + args, check=False)
    sys.exit(result.returncode)
