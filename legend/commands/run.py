import subprocess
import sys
import argparse

def run(args):
    parser = argparse.ArgumentParser(description='Run the Function App locally')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    args = parser.parse_args(args)

    cmd = ["func", "start"]
    if args.verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\nStopping function app...")
        sys.exit(0)
