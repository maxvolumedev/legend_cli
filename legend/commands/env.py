from typing import Dict, Any
from .base import Command
import re

class EnvCommand(Command):
    """Command to load environment config and output as shell environment variables"""

    def __init__(self):
        super().__init__(
            name='env',
            description='Load config for an environment and set as environment variables',
            aliases=['e']
        )

    def add_arguments(self, parser):
        parser.add_argument('environment',
                          help='Environment to load config from (e.g. dev, prod)')

    def _to_env_vars(self, parent_key, section) -> []:
        res = []
        for k in section.keys():
            v = section[k]
            k = re.sub('[-.]', '_', k.upper())
            if (isinstance(v, dict)):
                res.extend(self._to_env_vars(f"{parent_key}_{k}", v))
            else:
                res.append(f"{parent_key}_{k}=\"{v}\"")
        return res

    def handle(self, args):
        """Load config and convert to environment variables
        
        Args:
            args: Parsed command line arguments
            
        Returns:
            Dict containing the environment variables
        """
        # Load config for the specified environment
        self.load_config(args.environment)

        # Convert config to environment variables and print in shell format
        env_vars = self._to_env_vars("LEGEND", self.config.merged)
        
        for v in env_vars:
            print(f"export {v};")

