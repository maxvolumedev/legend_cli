import os
from pathlib import Path
from typing import Dict, Any
from types import SimpleNamespace
import tomli


class ConfigurationError(Exception):
    """Raised when there is an error loading or validating configuration"""
    pass


class Configuration:
    """Manages environment-specific configuration with dot notation access"""
    
    def __init__(self, environment: str=os.getenv("LEGEND_ENVIRONMENT", None)):
        """Initialize configuration for the specified environment
        
        Args:
            environment: Name of the environment (e.g., development, test, sit)
            
        Raises:
            ConfigurationError: If config files cannot be found or parsed, or no environment can be detected
        """
        if environment is None:
            raise ConfigurationError("Environment name must be specified")

        self.environment = environment
        self.config_dir = Path("config")
        self.global_config_path = self.config_dir / "application.toml"
        self.env_config_path = self.config_dir / f"{environment}.toml"
        self._config = self._load_config()
    
    def _load_config(self) -> SimpleNamespace:
        """Load and merge configuration for the specified environment
        
        Returns:
            SimpleNamespace: Configuration object with dot notation access
            
        Raises:
            ConfigurationError: If config files cannot be found or parsed
        """
        # Check if we're in a Legend app directory
        if not self.config_dir.exists():
            raise ConfigurationError("Not in a Legend application directory (config/ not found)")
        
        try:
            # Load global config
            global_config = {}
            if self.global_config_path.exists():
                with open(self.global_config_path, "rb") as f:
                    global_config = tomli.load(f)
            
            # Load environment config
            if not self.env_config_path.exists():
                raise ConfigurationError(
                    f"Environment config not found: {self.env_config_path}\n" +
                    f"Create {self.env_config_path.name} in the config directory"
                )
                
            with open(self.env_config_path, "rb") as f:
                env_config = tomli.load(f)
            
            # Merge configurations (environment config takes precedence)
            merged = self._deep_merge(global_config, env_config)
            return self._dict_to_namespace(merged)
            
        except FileNotFoundError as e:
            config_file = Path(e.filename).name
            raise ConfigurationError(
                f"Configuration file not found: {config_file}\n" +
                f"Create {config_file} in the config directory"
            )
        except tomli.TOMLDecodeError as e:
            raise ConfigurationError(
                f"Invalid TOML syntax in configuration:\n{e}\n" +
                f"Check syntax in {self.global_config_path.name} and {self.env_config_path.name}"
            )

    @staticmethod
    def _dict_to_namespace(d: Dict[str, Any]) -> SimpleNamespace:
        """Convert a dictionary to a SimpleNamespace recursively for dot notation access."""
        if not isinstance(d, dict):
            return d
        return SimpleNamespace(**{k: Configuration._dict_to_namespace(v) if isinstance(v, dict) else v 
                                for k, v in d.items()})

    @staticmethod
    def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries, with override taking precedence"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Configuration._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def __getattr__(self, name: str) -> Any:
        """Enable dot notation access to configuration values"""
        return getattr(self._config, name)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key with an optional default"""
        try:
            current = self._config
            for part in key.split('.'):
                current = getattr(current, part)
            return current
        except AttributeError:
            return default

    def validate_required(self, *keys: str) -> None:
        """Validate that required configuration keys are present
        
        Args:
            *keys: Required configuration keys (supports dot notation)
            
        Raises:
            ConfigurationError: If any required keys are missing
        """
        missing = []
        for key in keys:
            if self.get(key) is None:
                missing.append(key)
        
        if missing:
            raise ConfigurationError(
                f"Missing required configuration values in {self.global_config_path.name} or {self.env_config_path.name}:\n" + 
                "\n".join(f"  - {key}" for key in missing)
            )
