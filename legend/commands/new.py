import os
import subprocess
import venv
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

# Additional dependencies to add to requirements.txt
ADDITIONAL_DEPS = [
    "jinja2>=3.1.2",
    "-e /Users/max/work/legend_cli",
]

# Development dependencies
DEV_DEPS = [
    "pytest>=7.4.0",
]

def run(args):
    parser = argparse.ArgumentParser(description='Create a new Azure Function App')
    parser.add_argument('name', help='Name of the function app')
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
        f.write("\n# Additional dependencies added by Legend CLI\n")
        for dep in ADDITIONAL_DEPS:
            f.write(f"{dep}\n")

    # Create requirements-dev.txt
    with open("requirements-dev.txt", "w") as f:
        f.write("-r requirements.txt\n\n")
        f.write("# Development dependencies\n")
        for dep in DEV_DEPS:
            f.write(f"{dep}\n")

    # Initialize Git
    # subprocess.run(["git", "init"], check=True)

    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    def render_template(template_path, output_path):
        template = env.get_template(template_path)
        with open(output_path, "w") as f:
            f.write(template.render(app_name=args.name))

    # Create setup.py from template
    render_template("setup.py", "setup.py")

    # Create directories
    os.makedirs(".github/workflows", exist_ok=True)
    os.makedirs("test", exist_ok=True)
    os.makedirs("lib", exist_ok=True)

    # Create and activate virtual environment
    print("Creating virtual environment...")
    subprocess.run(["python", "-m", "venv", ".venv"], check=True)
    
    # Install dependencies
    venv_python = ".venv/bin/python" if os.name != "nt" else ".venv\\Scripts\\python.exe"
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements-dev.txt"], check=True)
    subprocess.run([venv_python, "-m", "pip", "install", "-e", "."], check=True)

    # Add a note about pip in the README
    with open("README.md", "a") as f:
        f.write('''

## Development

This project uses pip for dependency management.

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

    # Render lib templates
    lib_templates = Path(TEMPLATES_DIR) / "lib"
    if lib_templates.exists():
        for template in lib_templates.glob("*"):
            relative_path = template.relative_to(lib_templates)
            render_template(f"lib/{relative_path}", f"lib/{relative_path}")

    print(f"✨ New function app '{args.name}' created successfully!")
    print("\nTo get started:")
    print(f"  cd {args.name}")
    print("  source .venv/bin/activate    # Activate virtual environment")
    print("  func start                   # Start the function app")
