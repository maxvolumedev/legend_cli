#!/usr/bin/env python3

import sys
import os
from legend.commands import new, generate, run, test, console

COMMANDS = {
    "new": new.run,
    "generate": generate.run,
    "run": run.run,
    "test": test.run,
    "console": console.run,
}

def main():
    # Change to the directory where the legend command was invoked
    if 'LEGEND_CWD' in os.environ:
        os.chdir(os.environ['LEGEND_CWD'])

    if len(sys.argv) < 2:
        print("Usage: legend <command> [arguments]")
        print("\nAvailable commands:")
        # Group full commands with their aliases
        command_groups = {}
        for key, value in COMMANDS.items():
            if value not in command_groups:
                command_groups[value] = []
            command_groups[value].append(key)
        
        for cmds in command_groups.values():
            full_cmd = max(cmds, key=len)  # Get the longest (full) command name
            aliases = [c for c in cmds if c != full_cmd]
            if aliases:
                print(f"  {full_cmd} ({', '.join(aliases)})")
            else:
                print(f"  {full_cmd}")
        sys.exit(1)

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    # First try exact match
    if command in COMMANDS:
        COMMANDS[command](args)
        return

    # Then try prefix match
    matching_commands = [key for key in COMMANDS.keys() if key.startswith(command)]
    
    if len(matching_commands) == 0:
        print(f"Unknown command: {command}")
        print("\nDid you mean one of these?")
        # Find similar commands (contains the input)
        similar = [key for key in COMMANDS.keys() if command in key]
        if similar:
            for cmd in similar:
                print(f"  {cmd}")
        sys.exit(1)
    elif len(matching_commands) > 1:
        print(f"Ambiguous command '{command}'. Could mean:")
        for cmd in matching_commands:
            print(f"  {cmd}")
        sys.exit(1)
    
    COMMANDS[matching_commands[0]](args)

if __name__ == "__main__":
    main()
