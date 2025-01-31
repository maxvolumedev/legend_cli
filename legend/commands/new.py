import os
import subprocess
import venv
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

def run(args):
    if len(args) < 1:
        print("Usage: legend new <app_name>")
        return

    app_name = args[0]
    print(f"Creating new Azure Function App: {app_name}")

    # Initialize Azure Function
    subprocess.run(["func", "init", app_name, "--worker-runtime", "python"], check=True)

    # Change to app directory
    os.chdir(app_name)

    # Remove requirements.txt since we'll create our own
    if os.path.exists("requirements.txt"):
        os.remove("requirements.txt")

    # Initialize Git
    subprocess.run(["git", "init"], check=True)

    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    def render_template(template_path, output_path):
        template = env.get_template(template_path)
        with open(output_path, "w") as f:
            f.write(template.render(app_name=app_name))

    # Create setup.py and requirements files from templates
    render_template("setup.py", "setup.py")
    render_template("requirements.txt", "requirements.txt")
    render_template("requirements-dev.txt", "requirements-dev.txt")

    # Create directories
    os.makedirs(".github/workflows", exist_ok=True)
    os.makedirs("test", exist_ok=True)
    os.makedirs("lib", exist_ok=True)

    # Create and activate virtual environment
    print("Creating virtual environment...")
    venv.create(".venv", with_pip=True)
    
    # Install dependencies
    venv_python = ".venv/bin/python" if os.name != "nt" else ".venv\\Scripts\\python.exe"
    subprocess.run([venv_python, "-m", "pip", "install", "-e", ".[dev]"], check=True)

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
pip install -e .[dev] # Install with development dependencies
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

    # Render GitHub workflow
    render_template("workflows/deploy.yml", ".github/workflows/deploy.yml")

    # Render lib templates
    lib_templates = Path(TEMPLATES_DIR) / "lib"
    if lib_templates.exists():
        for template in lib_templates.glob("*"):
            relative_path = template.relative_to(lib_templates)
            render_template(f"lib/{relative_path}", f"lib/{relative_path}")

    print(f"✨ New function app '{app_name}' created successfully!")
    print("\nTo get started:")
    print(f"  cd {app_name}")
    print("  source .venv/bin/activate    # Activate virtual environment")
    print("  func start                   # Start the function app")
