import os
import subprocess
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

    # Initialize Git
    subprocess.run(["git", "init"], check=True)

    # Setup Poetry
    with open("pyproject.toml", "w") as f:
        f.write(f'''[tool.poetry]
name = "{app_name}"
version = "0.1.0"
description = "Azure Functions App"
authors = []

[tool.poetry.dependencies]
python = "^3.9"
azure-functions = "^1.17.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
jinja2 = "^3.1.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
''')

    # Create directories
    os.makedirs(".github/workflows", exist_ok=True)
    os.makedirs("test", exist_ok=True)
    os.makedirs("lib", exist_ok=True)

    # Initialize Poetry and install dependencies
    subprocess.run(["poetry", "install"], check=True)

    # Render templates
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    def render_template(template_path, output_path):
        template = env.get_template(template_path)
        with open(output_path, "w") as f:
            f.write(template.render(app_name=app_name))

    # Render GitHub workflow
    render_template("workflows/deploy.yml", ".github/workflows/deploy.yml")

    # Render lib templates
    lib_templates = Path(TEMPLATES_DIR) / "lib"
    if lib_templates.exists():
        for template in lib_templates.glob("*"):
            relative_path = template.relative_to(lib_templates)
            render_template(f"lib/{relative_path}", f"lib/{relative_path}")

    print(f"✨ New function app '{app_name}' created successfully!")
