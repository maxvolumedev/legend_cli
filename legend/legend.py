#!/usr/bin/env python3

import sys
import os
from legend.commands import new, generate, run, test, console

COMMANDS = {
    "new": new.run,
    "n": new.run,
    "generate": generate.run,
    "g": generate.run,
    "run": run.run,
    "r": run.run,
    "test": test.run,
    "t": test.run,
    "console": console.run,
    "c": console.run,
}

def main():
    # Change to the directory where the legend command was invoked
    if 'LEGEND_CWD' in os.environ:
        os.chdir(os.environ['LEGEND_CWD'])

    if len(sys.argv) < 2:
        print("Usage: legend <command> [arguments]")
        sys.exit(1)

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    matching_commands = [key for key in COMMANDS.keys() if key.startswith(command)]
    
    if len(matching_commands) == 0:
        print(f"Unknown command: {command}")
        sys.exit(1)
    elif len(matching_commands) > 1:
        print(f"Ambiguous command '{command}'. Matches: {', '.join(matching_commands)}")
        sys.exit(1)
    
    COMMANDS[matching_commands[0]](args)

if __name__ == "__main__":
    main()
