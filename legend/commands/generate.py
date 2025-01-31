import os
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

def run(args):
    if len(args) < 2 or args[0] not in ["function", "f"]:
        print("Usage: legend generate function <function_name>")
        return

    function_name = args[1]
    
    # Check if function already exists
    if os.path.exists(function_name):
        print(f"Error: Function '{function_name}' already exists")
        return

    print(f"Generating function: {function_name}")

    # Run func new
    subprocess.run(["func", "new", "--name", function_name, "--template", "HTTP trigger"], check=True)

    # Render templates
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def render_template(template_path, output_path):
        template = env.get_template(template_path)
        with open(output_path, "w") as f:
            f.write(template.render(function_name=function_name))

    # Create function code
    render_template("function/__init__.py", f"{function_name}/__init__.py")
    
    # Create test file
    os.makedirs("test/functions", exist_ok=True)
    render_template("test/function.py", f"test/functions/{function_name}_test.py")

    print(f"✨ Function '{function_name}' generated successfully!")
