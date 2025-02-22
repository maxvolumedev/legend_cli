#!/usr/bin/env python3

import sys
import os
import argparse
from importlib import metadata
from legend.commands import new, deploy, bootstrap, info, destroy, console, test, run, generate, provision

try:
    __version__ = metadata.version("legend-cli")
except metadata.PackageNotFoundError:
    # Package is not installed, fall back to _version.py
    from legend._version import __version__

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
    parser.add_argument("--version", action="version", version=__version__)
    

    subparsers = parser.add_subparsers(dest='command', required=False)

    # Get all command instances
    commands = [
        new.NewCommand(),
        generate.GenerateCommand(),
        run.RunCommand(),
        test.TestCommand(),
        console.ConsoleCommand(),
        provision.ProvisionCommand(),
        deploy.DeployCommand(),
        bootstrap.BootstrapCommand(),
        info.InfoCommand(),
        destroy.DestroyCommand(),
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
