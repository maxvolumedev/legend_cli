import os
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import argparse

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

def run(args):
    parser = argparse.ArgumentParser(description='Generate a new Azure Function')
    subparsers = parser.add_subparsers(dest='type', required=True)

    # Function subcommand
    func_parser = subparsers.add_parser('function', aliases=['f'], help='Generate a new function')
    func_parser.add_argument('name', help='Name of the function')
    func_parser.add_argument('--template', '-t', default='HTTP trigger', 
                          help='Function template to use (default: HTTP trigger)')

    args = parser.parse_args(args)
    
    if args.type in ['function', 'f']:
        print(f"Generating function: {args.name} (template: {args.template})")

        # Run func new
        subprocess.run(["func", "new", "--name", args.name, "--template", args.template], check=True)

        # Render templates
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        print(f"Template directory: {TEMPLATES_DIR}")

        def render_template(template_path, output_path):
            print(f"Rendering {template_path} -> {output_path}")
            template = env.get_template(template_path)
            with open(output_path, "w") as f:
                f.write(template.render(function_name=args.name))

        # Create test file
        os.makedirs("test/functions", exist_ok=True)
        render_template("test/function.py", f"test/functions/{args.name}_test.py")

        print(f"✨ Function '{args.name}' generated successfully!")
