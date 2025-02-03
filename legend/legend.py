#!/usr/bin/env python3

import sys
import os
import argparse
from legend.commands import deploy, bootstrap, info, destroy, console, test, run, generate

def main():
    # Change to the directory where the legend command was invoked
    if 'LEGEND_CWD' in os.environ:
        os.chdir(os.environ['LEGEND_CWD'])

    # Create main parser with common arguments
    parser = argparse.ArgumentParser(
        description='Legend - A CLI for Azure Functions'
    )
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose output')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Get all command instances
    commands = [
        # new.command,
        generate.command,
        run.command,
        test.command,
        console.command,
        # provision.command,
        deploy.command,
        bootstrap.command,
        info.command,
        destroy.command
    ]
    
    # Map commands by their names and aliases
    COMMANDS = {}
    for cmd in commands:
        COMMANDS[cmd.name] = cmd
        for alias in cmd.aliases:
            COMMANDS[alias] = cmd

    # Add each command's parser as a subparser
    for cmd in set(COMMANDS.values()):
        subparsers.add_parser(
            cmd.name,
            help=cmd.description,
            parents=[cmd.parser],
            aliases=cmd.aliases,
            conflict_handler='resolve'
        )

    # If no args, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse args to get command and global flags
    args = parser.parse_args()

    # Get the command
    cmd = COMMANDS[args.command]
    
    # Run command with parsed args and global verbose flag
    cmd.run(args)

if __name__ == "__main__":
    main()
