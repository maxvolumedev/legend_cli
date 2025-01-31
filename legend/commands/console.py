import code
import os
import glob
import importlib.util
from pathlib import Path

def import_module(file_path):
    """Import a module from file path."""
    module_name = Path(file_path).stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module_name, module

def load_functions():
    """Load all function modules in the current directory."""
    namespace = {}
    
    # Find all Python files in function directories
    function_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    
    for dir_name in function_dirs:
        init_file = os.path.join(dir_name, '__init__.py')
        if os.path.exists(init_file):
            try:
                module_name, module = import_module(init_file)
                namespace[module_name] = module
                print(f"Loaded function: {module_name}")
            except Exception as e:
                print(f"Failed to load {init_file}: {e}")
    
    return namespace

def run(args):
    print("Starting Python REPL with all functions loaded...")
    namespace = load_functions()
    code.interact(local=namespace, banner="Legend Console - All functions loaded")
