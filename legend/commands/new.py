import os
import subprocess
import venv
import argparse
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

# Additional dependencies to add to requirements.txt
ADDITIONAL_DEPS = [
    "jinja2>=3.1.2",
]

# Development dependencies
DEV_DEPS = [
    "git+https://github.com/maxvolumedev/legend_cli.git", # we don't need to deploy the legend cli
    "tomli>=2.0.1  # For reading TOML configuration files",
    "pytest>=7.4.0",
]

def normalize_name(name: str) -> str:
    """Normalize app name: lowercase and replace underscores with hyphens"""
    return name.lower().replace('_', '-')

def generate_short_name(name: str, max_len: int = 24) -> str:
    """Generate a meaningful short name from a longer name.
    
    Strategy:
    1. Split into words
    2. For common words (api, service, etc), use standard abbreviations
    3. For other words:
       - Keep first letter
       - Keep consonants after first letter (to maintain readability)
       - Keep numbers
    4. Join and truncate to max_len
    
    Examples:
        'customer-service-api' -> 'cstapi'
        'payment-processing-service' -> 'pmtprcsvc'
        'rta-customer-adapter' -> 'rtacstadp'
    """
    # Common word mappings by category
    abbreviations = {
        # Service types
        'service': 'svc',
        'api': 'api',
        'application': 'app',
        'adapter': 'adp',
        'integration': 'int',
        'interface': 'intf',
        'gateway': 'gw',
        'proxy': 'prx',
        'server': 'srv',
        'client': 'cli',
        'worker': 'wkr',
        'daemon': 'dmn',
        'scheduler': 'sch',
        'processor': 'prc',
        'handler': 'hdlr',
        'listener': 'lsnr',
        'monitor': 'mon',
        'controller': 'ctrl',
        'middleware': 'mw',
        
        # Business domains
        'customer': 'cst',
        'payment': 'pmt',
        'account': 'acc',
        'transaction': 'trx',
        'order': 'ord',
        'invoice': 'inv',
        'product': 'prod',
        'inventory': 'inv',
        'catalog': 'cat',
        'document': 'doc',
        'message': 'msg',
        'notification': 'notif',
        'analytics': 'anly',
        'reporting': 'rpt',
        'billing': 'bill',
        'shipping': 'ship',
        'tracking': 'trk',
        'marketing': 'mkt',
        'authentication': 'auth',
        'authorization': 'authz',
        
        # Operations
        'manager': 'mgr',
        'processing': 'prc',
        'generator': 'gen',
        'validator': 'val',
        'converter': 'conv',
        'transformer': 'trf',
        'calculator': 'calc',
        'formatter': 'fmt',
        'publisher': 'pub',
        'subscriber': 'sub',
        'synchronizer': 'sync',
        'orchestrator': 'orch',
        
        # Data related
        'database': 'db',
        'repository': 'repo',
        'storage': 'store',
        'cache': 'cache',
        'queue': 'q',
        'stream': 'strm',
        'event': 'evt',
        'config': 'cfg',
        'settings': 'set',
        'metadata': 'meta',
        
        # Environments
        'development': 'dev',
        'production': 'prod',
        'test': 'test',
        'staging': 'stg',
        'sandbox': 'sbx',
        'quality': 'qa',
        'acceptance': 'uat',
        'integration': 'int',
        'preview': 'prev',
        'performance': 'perf',
        
        # Common prefixes/suffixes
        'internal': 'int',
        'external': 'ext',
        'public': 'pub',
        'private': 'prv',
        'shared': 'shd',
        'common': 'cmn',
        'core': 'core',
        'legacy': 'leg',
        'utility': 'util',
        'helper': 'hlpr',
        'wrapper': 'wrap',
        'engine': 'eng',
        'system': 'sys',
    }
    
    # Split into words
    words = name.lower().replace('_', '-').split('-')
    result = []
    
    for word in words:
        # Check if we have a standard abbreviation
        if word in abbreviations:
            result.append(abbreviations[word])
        else:
            # Keep first letter
            shortened = word[0]
            
            # Keep consonants and numbers after first letter
            consonants = ''.join(c for c in word[1:] 
                                if c.isdigit() or (c.isalpha() and c not in 'aeiou'))
            shortened += consonants[:2]  # Limit to 2 consonants for consistency
            
            result.append(shortened)
    
    # Join and ensure we don't exceed max_len
    return ''.join(result)[:max_len]

def pad_with_uuid(name: str, max_len: int = 24) -> str:
    """Pad a string with part of a UUID to reach max_len.
    Only uses the minimum number of UUID characters needed.
    Example: 'myapp' -> 'myapp1a2b3' (not the full UUID)
    """
    if len(name) >= max_len:
        return name[:max_len]
    
    # Only use as many UUID chars as needed to reach max_len
    needed_length = max_len - len(name)
    uid = str(uuid.uuid4()).replace('-', '')[:needed_length]
    return name + uid

def get_storage_name(app_name: str, env: str) -> str:
    """Generate storage account name: shortened app name + env + optional uuid suffix, max 24 chars.
    Must be 3-24 characters, lowercase letters and numbers only.
    Will be padded with UUID to ensure global uniqueness.
    """
    short_name = generate_short_name(app_name, max_len=20)  # Leave room for env
    name = f"{short_name}{env}"
    # Remove any non-alphanumeric characters and convert to lowercase
    name = re.sub(r'[^a-z0-9]', '', name.lower())
    # Ensure minimum length of 3
    if len(name) < 3:
        name = name + 'x' * (3 - len(name))
    # Pad with UUID to ensure uniqueness
    return pad_with_uuid(name, 24)

def get_keyvault_name(app_name: str, env: str) -> str:
    """Generate key vault name: shortened app name + env + kv + optional uuid suffix, max 24 chars.
    Must be 3-24 characters, lowercase letters, numbers, and hyphens.
    Hyphens cannot be consecutive or at start/end.
    Will be padded with UUID to ensure global uniqueness.
    """
    short_name = generate_short_name(app_name, max_len=19)  # Leave room for env and 'kv'
    name = f"{short_name}{env}kv"
    # Remove any characters not allowed in key vault names
    name = re.sub(r'[^a-z0-9-]', '', name.lower())
    # Remove consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    # Ensure minimum length of 3
    if len(name) < 3:
        name = name + 'x' * (3 - len(name))
    # Pad with UUID to ensure uniqueness
    return pad_with_uuid(name, 24)

def run(args):
    parser = argparse.ArgumentParser(description='Create a new Azure Function App')
    parser.add_argument('name', help='Name of the function app')
    parser.add_argument('location', help='Azure location to create the function app in', nargs='?', default='australiasoutheast')
    args = parser.parse_args(args)

    if not args.name:
        parser.print_help()
        return

    # Check if func CLI is installed
    try:
        subprocess.run(["func", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Azure Functions Core Tools (func CLI) is not installed.")
        print("\nTo install:")
        print("  brew install azure-functions-core-tools@4")
        print("\nOr visit: https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local")
        return

    print(f"Creating new Azure Function App: {args.name}")

    # Initialize Azure Function
    subprocess.run(["func", "init", args.name, "--worker-runtime", "python"], check=True)

    # Change to app directory
    os.chdir(args.name)

    # Append our additional dependencies to requirements.txt
    with open("requirements.txt", "a") as f:
        f.write("\n\n# Additional dependencies added by Legend CLI\n")
        for dep in ADDITIONAL_DEPS:
            f.write(f"{dep}\n")

    # Create requirements-dev.txt
    with open("requirements-dev.txt", "w") as f:
        f.write("-r requirements.txt\n\n")
        f.write("# Development dependencies\n")
        for dep in DEV_DEPS:
            f.write(f"{dep}\n")

    # Initialize Git
    subprocess.run(["git", "init"], check=True)

    # Set up Jinja environment
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    def render_template(template_path, output_path):
        template = jinja_env.get_template(template_path)
        with open(output_path, "w") as f:
            f.write(template.render(app_name=args.name))

    # Create setup.py from template
    render_template("setup.py", "setup.py")

    # Create directories
    os.makedirs(".github/workflows", exist_ok=True)
    os.makedirs("test", exist_ok=True)
    os.makedirs("lib", exist_ok=True)
    os.makedirs("config", exist_ok=True)

    # Create global application config
    template = jinja_env.get_template("config/application.toml")
    with open("config/application.toml", "w") as f:
        f.write(template.render(
            app_name=normalize_name(args.name),
            azure_location=args.location
        ))

    # Create environment configuration files
    environments = ["development", "test", "sit", "uat", "production"]
    for environment in environments:
        config_file = f"config/{environment}.toml"
        template = jinja_env.get_template("config/environment.toml")
        with open(config_file, "w") as f:
            f.write(template.render(
                app_name=normalize_name(args.name),
                environment=environment,
                resource_group=f"{normalize_name(args.name)}-group-{environment}",
                storage_account=get_storage_name(normalize_name(args.name), environment),
                function_app=f"{normalize_name(args.name)}-{environment}",
                app_service_plan=f"{normalize_name(args.name)}-plan-{environment}",
                key_vault_name=get_keyvault_name(normalize_name(args.name), environment)
            ))

    # Copy lib templates
    lib_templates = Path(TEMPLATES_DIR) / "lib"
    if lib_templates.exists():
        for template_path in lib_templates.rglob("*"):
            if template_path.is_file():
                relative_path = template_path.relative_to(lib_templates)
                target_path = Path("lib") / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                if template_path.suffix == ".py":
                    template = jinja_env.get_template(str(Path("lib") / relative_path))
                    with open(target_path, "w") as f:
                        f.write(template.render(app_name=args.name))
                else:
                    import shutil
                    shutil.copy2(template_path, target_path)

    # Create and activate virtual environment
    print("Creating virtual environment...")
    subprocess.run(["python", "-m", "venv", ".venv"], check=True)
    
    # Install dependencies
    venv_python = ".venv/bin/python" if os.name != "nt" else ".venv\\Scripts\\python.exe"
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements-dev.txt"], check=True)

    # Add a note about pip in the README
    with open("README.md", "a") as f:
        f.write('''

## Development

This project uses pip for dependency management.

### Environment Configuration

The application supports multiple environments: development, test, sit, uat, and production. Configuration for each environment is stored in TOML files under the `config/` directory.

To specify the environment:
```bash
export LEGEND_ENVIRONMENT=development  # Or test, sit, uat, production
```

If not specified, the environment defaults to `development`.

To access configuration in your code:
```python
from lib.config import config

# Access configuration values
key_vault_name = config.azure.key_vault_name
api_base_url = config.api.base_url
debug_mode = config.settings.debug
```

### Virtual Environment

The project comes with a virtual environment in the `.venv` directory. To activate it:

```bash
source .venv/bin/activate  # On Unix/macOS
.venv\\Scripts\\activate    # On Windows
```

### Installing Dependencies

```bash
pip install -r requirements.txt      # Install runtime dependencies
pip install -r requirements-dev.txt  # Install development dependencies
```

### Installing in Development Mode

```bash
pip install -e .      # Install the package in editable mode
```

### Running Tests

```bash
pytest
```

### Running the Function Locally

```bash
func start
```
''')

    # Create bin directory and legend binstub
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)

    legend_binstub = bin_dir / "legend"
    with open(legend_binstub, "w") as f:
        f.write("""#!/bin/bash
# Binstub for running Legend CLI commands

# Activate the virtual environment
source .venv/bin/activate

# Run the Legend CLI command
python -m legend "$@"
""")

    # Make the binstub executable
    legend_binstub.chmod(0o755)

    # Render GitHub workflow
    render_template("workflows/deploy.yml", ".github/workflows/deploy.yml")

    print("\n✨ Created new Legend app!")
    print(f"\nNext steps:")
    print(f"  cd {args.name}")
    print(f"  legend generate function             # Generate a new function")
    print(f"  legend test                          # Run tests")
    print(f"  legend run                           # Run function app locally")
    print(f"  legend console                       # Start interactive console")
    print(f"  legend provision                     # Provision Azure resources")
    print(f"  legend deploy                        # Deploy to Azure")
