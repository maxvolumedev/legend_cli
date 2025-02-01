import os
import tomli
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, Any

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Get environment from LEGEND_ENVIRONMENT or default to development
        self.environment = os.getenv("LEGEND_ENVIRONMENT", "development")
        
        # Load and merge configurations
        config_dir = Path(__file__).parent.parent.parent / "config"
        
        # Load global configuration first
        global_config = self._load_toml(config_dir / "application.toml")
        
        # Load environment-specific configuration
        env_config = self._load_toml(config_dir / f"{self.environment}.toml")
        
        # Merge configurations (environment config takes precedence)
        merged_config = self._deep_merge(global_config, env_config)
        
        # Convert to namespace and update instance
        self._load_config(merged_config)
    
    def _load_toml(self, path: Path) -> Dict[str, Any]:
        """Load a TOML file, returning an empty dict if the file doesn't exist"""
        try:
            with open(path, "rb") as f:
                return tomli.load(f)
        except FileNotFoundError:
            return {}
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two dictionaries, with override taking precedence"""
        merged = base.copy()
        
        for key, value in override.items():
            if (
                key in merged 
                and isinstance(merged[key], dict) 
                and isinstance(value, dict)
            ):
                merged[key] = self._deep_merge(merged[key], value)
            else:
                merged[key] = value
                
        return merged
    
    def _load_config(self, config_dict):
        """Recursively convert dictionary to SimpleNamespace for dot notation access"""
        def dict_to_namespace(d):
            if not isinstance(d, dict):
                return d
            namespace = SimpleNamespace()
            for key, value in d.items():
                setattr(namespace, key, dict_to_namespace(value))
            return namespace
        
        # Convert the config dictionary to a namespace and update instance
        config_namespace = dict_to_namespace(config_dict)
        self.__dict__.update(vars(config_namespace))

# Create a singleton instance
config = Config()
