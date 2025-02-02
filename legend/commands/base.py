"""
Base command class providing common functionality for Legend CLI commands.
"""

import argparse
import subprocess
import sys
import os
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from ..lib.config import load_config as load_config_from_lib

from abc import ABC, abstractmethod

class Command(ABC):
    """Base class for Legend CLI commands providing common functionality."""
    
    def __init__(self, name: str, description: str, aliases: List[str] = None):
        """Initialize the command.
        
        Args:
            name: Name of the command (e.g. 'info')
            description: Description of what the command does
            aliases: Optional list of command aliases (e.g. ['i'])
        """
        self.name = name
        self.description = description
        self.aliases = aliases or []
        self.parser = self.setup_parser()
        self.verbose = False

    def setup_parser(self) -> argparse.ArgumentParser:
        """Setup command-specific argument parser.
        
        Returns:
            ArgumentParser configured for this command
        """
        parser = argparse.ArgumentParser(description=self.description)
        self.add_arguments(parser)
        return parser
        
        
    def add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments to the parser.
        Override this in subclasses to add custom arguments.
        
        Args:
            parser: The argument parser to add arguments to
        """
        pass

    @abstractmethod
    def handle(self, args):
        """Handle the command execution.
        
        Args:
            args: The parsed command arguments
        """
        pass

    def run(self, args):
        """Run the command.
        
        Args:
            args: The parsed command arguments
            verbose: Whether to enable verbose output
        """
        self.info("Verbose: " + str(args.verbose))
        self.verbose = args.verbose
        return self.handle(args)
    

    def format_output(self, message: str, status: str = "info") -> str:
        """Format output with appropriate emoji and styling.
        
        Args:
            message: The message to format
            status: One of "info", "success", "error", "warning"
            
        Returns:
            Formatted message string
        """
        status_indicators = {
            "info": "",
            "success": "✅ ",
            "error": "⛔️ ",
            "warning": "🟡 ",
            "completed": "✨ "
        }
        indicator = status_indicators.get(status, "")
        return f"{indicator}{message}"

    def info(self, message: str):
        """Print an info message."""
        print(self.format_output(message, "info"))

    def success(self, message: str):
        """Print a success message."""
        print(self.format_output(message, "success"))

    def warning(self, message: str):
        """Print a warning message."""
        print(self.format_output(message, "warning"))

    def error(self, message: str):
        """Print an error message."""
        print(self.format_output(message, "error"))

    def completed(self, message: str):
        """Print a completion message."""
        print(self.format_output(message, "completed"))

    def handle_error(self, error: Exception, context: str = "") -> None:
        """Standardized error handling.
        
        Args:
            error: The exception that occurred
            context: Optional context about where/why the error occurred
        """
        if context:
            self.error(f"{context}:\n{str(error)}")
        else:
            self.error(str(error))
        if self.parser and hasattr(self, 'args') and getattr(self, 'args').verbose:
            import traceback
            print("\nDetailed traceback:")
            traceback.print_exc()

    def run_subprocess(self, 
                      cmd: List[str], 
                      check: bool = True,
                      capture_output: bool = True,
                      env: Optional[Dict[str, str]] = None) -> Optional[subprocess.CompletedProcess]:
        """Safe subprocess execution with error handling.
        
        Args:
            cmd: Command and arguments to run
            check: Whether to raise an exception on non-zero exit
            capture_output: Whether to capture stdout/stderr
            env: Optional environment variables dict
            
        Returns:
            CompletedProcess instance if successful, None if failed
        """
        try:
            if self.verbose:
                self.info(f"Running command: {' '.join(cmd)}")
            
            process_env = os.environ.copy()
            if env:
                process_env.update(env)
            
            return subprocess.run(
                cmd,
                check=check,
                text=True,
                capture_output=capture_output,
                env=process_env
            )
        except subprocess.CalledProcessError as e:
            if self.verbose:
                self.handle_error(e, f"Command failed: {' '.join(cmd)}")
            return None

    def run_azure_command(self, 
                         cmd: List[str], 
                         output_format: str = "json") -> Optional[Union[Dict, List, str]]:
        """Execute Azure CLI commands.
        
        Args:
            cmd: Azure CLI command and arguments (without 'az' prefix)
            output_format: Desired output format (json, tsv, etc.)
            
        Returns:
            Command output parsed according to output_format, or None if command fails
        """
        full_cmd = ["az"] + cmd + ["-o", output_format]
        result = self.run_subprocess(full_cmd)
        if not result:
            return None
            
        if output_format == "json" and result.stdout.strip():
            import json
            return json.loads(result.stdout)
        return result.stdout.strip()

    def check_resource_exists(self, 
                            resource_type: str, 
                            name: str, 
                            resource_group: Optional[str] = None) -> bool:
        """Check if Azure resource exists.
        
        Args:
            resource_type: Type of resource (functionapp, storage, etc.)
            name: Name of the resource
            resource_group: Optional resource group name
            
        Returns:
            True if resource exists, False otherwise
        """
        cmd = [resource_type, "show", "--name", name]
        if resource_group:
            cmd.extend(["--resource-group", resource_group])
        result = self.run_azure_command(cmd)
        return result is not None

    def setup_environment(self, environment: str) -> Dict[str, str]:
        """Setup environment variables and validation.
        
        Args:
            environment: Name of the environment
            
        Returns:
            Dict of environment variables
        """
        env_vars = os.environ.copy()
        env_vars["LEGEND_ENVIRONMENT"] = environment
        return env_vars

    def validate_environment(self, environment: str) -> bool:
        """Validate environment name and settings.
        
        Args:
            environment: Name of the environment to validate
            
        Returns:
            True if environment is valid, False otherwise
        """
        if environment == 'application':
            self.error("'application' is not a valid environment name - it is reserved for the base config file")
            return False
            
        config_file = Path('config') / f'{environment}.toml'
        if not config_file.exists():
            self.error(f"No configuration file found for environment '{environment}' at {config_file}")
            return False
        return True

