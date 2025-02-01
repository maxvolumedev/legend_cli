#!/usr/bin/env python3

import sys
import os
import argparse
from legend.commands import new, generate, run, test, console, provision, deploy, bootstrap

def main():
    # Change to the directory where the legend command was invoked
    if 'LEGEND_CWD' in os.environ:
        os.chdir(os.environ['LEGEND_CWD'])

    parser = argparse.ArgumentParser(
        description='Legend CLI - A Rails-inspired CLI for Azure Functions'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # New command
    new_parser = subparsers.add_parser('new', help='Create a new Azure Function App')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', aliases=['g'], help='Generate new code')
    
    # Run command
    run_parser = subparsers.add_parser('run', aliases=['r'], help='Run the Function App locally')
    
    # Test command
    test_parser = subparsers.add_parser('test', aliases=['t'], help='Run tests')
    
    # Console command
    console_parser = subparsers.add_parser('console', aliases=['c'], help='Start an interactive Python console')
    
    # Provision command
    provision_parser = subparsers.add_parser('provision', aliases=['p'], help='Provision Azure resources')

    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy the Function App to Azure')

    # Bootstrap command
    bootstrap_parser = subparsers.add_parser('bootstrap', help='Check and install dependencies')

    # If no args, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse known args to get the command
    args, remaining = parser.parse_known_args()

    # Map commands to their handlers
    COMMANDS = {
        'new': new.run,
        'generate': generate.run,
        'g': generate.run,
        'run': run.run,
        'r': run.run,
        'test': test.run,
        't': test.run,
        'console': console.run,
        'c': console.run,
        'provision': provision.run,
        'p': provision.run,
        'deploy': deploy.run,
        'bootstrap': bootstrap.run
    }

    # Run the command with remaining args
    COMMANDS[args.command](remaining)

if __name__ == "__main__":
    main()
