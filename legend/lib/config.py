import os
from pathlib import Path
from typing import Dict, Any, Optional
import tomli

def load_config(environment: str) -> Optional[Dict[str, Any]]:
    """Load and merge configuration for the specified environment"""
    config_dir = Path("config")
    
    # Check if we're in a Legend app directory
    if not config_dir.exists():
        print("⛔️ Error: Not in a Legend application directory (config/ not found)")
        return None
    
    try:
        # Load global config
        global_config = {}
        global_config_path = config_dir / "application.toml"
        if global_config_path.exists():
            with open(global_config_path, "rb") as f:
                global_config = tomli.load(f)
        
        # Load environment config
        env_config_path = config_dir / f"{environment}.toml"
        with open(env_config_path, "rb") as f:
            env_config = tomli.load(f)
        
        # Merge configurations (environment config takes precedence)
        return deep_merge(global_config, env_config)
    except FileNotFoundError as e:
        print(f"⛔️ Error: Configuration file not found: {e.filename}")
        return None
    except tomli.TOMLDecodeError as e:
        print(f"⛔️ Error: Invalid TOML syntax in configuration: {e}")
        return None

def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries, with override taking precedence"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
