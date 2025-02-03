"""
Base command class providing common functionality for Legend CLI commands.
"""

import argparse
import subprocess
import sys
import os
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from ..lib.config import Configuration, ConfigurationError

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
        self._config: Optional[Configuration] = None

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
                      env: Optional[Dict[str, str]] = None,
                      **kwargs) -> Optional[subprocess.CompletedProcess]:
        """Safe subprocess execution with error handling.
        
        Args:
            cmd: Command and arguments to run
            check: Whether to raise an exception on non-zero exit
            env: Optional environment variables dict
            **kwargs: Additional arguments passed directly to subprocess.run
            
        Returns:
            CompletedProcess instance if successful, None if failed
        """
        try:
            if self.verbose:
                self.info(f"Running command: {' '.join(cmd)}")
            
            process_env = os.environ.copy()
            if env:
                process_env.update(env)
            
            # Set some defaults that can be overridden by kwargs
            subprocess_args = {
                'text': True,
                'capture_output': True,
                'env': process_env,
                'stdout': None,
                'stderr': None,
            }
            subprocess_args.update(kwargs)
            
            return subprocess.run(
                cmd,
                check=check,
                **subprocess_args
            )
        except subprocess.CalledProcessError as e:
            if check:
                raise e
            if self.verbose:
                self.handle_error(e, f"Command failed: {' '.join(cmd)}")
            return None

    def run_azure_command(self, 
                         cmd: List[str], 
                         output_format: str = "json",
                         **kwargs) -> Optional[Union[Dict, List, str]]:
        """Execute Azure CLI commands.
        
        Args:
            cmd: Azure CLI command and arguments (without 'az' prefix)
            output_format: Desired output format (json, tsv, etc.)
            
        Returns:
            Command output parsed according to output_format, or None if command fails
        """
        full_cmd = cmd + ["-o", output_format]
        result = self.run_subprocess(full_cmd, **kwargs)
        if not result:
            return None
            
        if output_format == "json" and result.stdout.strip():
            import json
            return json.loads(result.stdout)
        return result.stdout.strip()


    def check_resource_exists(self,
                            resource_type: str,
                            cmd: str = "show",                             
                            name: str = None, 
                            resource_group: Optional[str] = None) -> bool:
        """Check if Azure resource exists.
        
        Args:
            resource_type: Type of resource (functionapp, storage, etc.)
            name: Name of the resource
            resource_group: Optional resource group name
            
        Returns:
            True if resource exists, False otherwise
        """
        cmd = [cmd, resource_type, cmd]
        if name:
            cmd.extend(["--name", name])
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

    def load_config(self, environment: str) -> bool:
        """Load configuration for the specified environment
        
        Args:
            environment: Name of the environment to load
            
        Returns:
            bool: True if configuration was loaded successfully, False otherwise
        """
        try:
            self._config = Configuration(environment)
            return True
        except ConfigurationError as e:
            self.error(f"Failed to load configuration: {e}")
            return False
    
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
        
        return self.load_config(environment)
    
    def render_template(self, template_path: str, output_path: str, context: dict):
        """Render a template file with the given context.
        
        Args:
            template_path: Path to the template file relative to templates dir
            output_path: Path where the rendered file should be written
            context: Dictionary of variables to pass to the template
        """
        if self.verbose:
            self.info(f"Rendering {template_path} -> {output_path}")

        try:
            templates_dir = Path(__file__).parent.parent / "templates"
            env = Environment(loader=FileSystemLoader(templates_dir))
            template = env.get_template(template_path)
            
            with open(output_path, "w") as f:
                f.write(template.render(**context))
        except Exception as e:
            self.error(f"Failed to render template {template_path}: {e}")
            raise

    @property
    def config(self) -> Optional[Configuration]:
        """Get the current configuration.
        
        Returns:
            Configuration object if loaded, None otherwise
        """
        return self._config
    
    def validate_config(self, *required_keys: str) -> bool:
        """Validate that required configuration keys are present
        
        Args:
            *required_keys: Required configuration keys (supports dot notation)
            
        Returns:
            bool: True if all required keys are present, False otherwise
        """
        if not self._config:
            self.error("No configuration loaded")
            return False
            
        try:
            self._config.validate_required(*required_keys)
            return True
        except ConfigurationError as e:
            self.error(str(e))
            return False

