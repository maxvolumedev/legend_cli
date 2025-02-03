import os
import importlib.util
import azure.functions as func
from .base import Command


class ConsoleCommand(Command):
    """Start an interactive Python console with your function app loaded"""
    
    def __init__(self):
        super().__init__(
            name='console',
            description='Start an interactive Python console with your function app loaded',
            aliases=['c']
        )
    
    def add_arguments(self, parser):
        # No additional arguments needed
        pass
    
    def start_repl(self, namespace):
        """Start the best available REPL."""
        self.info("\nChecking available REPLs...")
        try:
            import sys
            from ptpython.repl import embed
            self.success("ptpython found, using enhanced REPL")
            embed(globals=namespace, locals=namespace)
        except ImportError as e:
            self.warning(f"ptpython not found ({str(e)}), falling back to standard REPL")
            import code
            code.interact(local=namespace)

    def import_function_app(self):
        """Import the function_app module."""
        if not os.path.exists('function_app.py'):
            self.error("function_app.py not found in current directory")
            return None
        
        try:
            spec = importlib.util.spec_from_file_location('function_app', 'function_app.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            self.error(f"Failed to load function_app.py: {e}")
            return None

    def print_help(self, app):
        """Print helpful instructions for using the console."""
        self.info("\nLegend Console - Your functions are loaded and ready to test!")
        self.info("\nAvailable functions from function_app.py:")
        
        # Find all functions with the @app.route decorator
        funcs = [name for name, obj in vars(app).items() 
                if callable(obj) and hasattr(obj, '__route__')]
        
        for func_name in funcs:
            self.info(f"  - {func_name}")
        
        self.info("\nTo test a function, create a mock request and call it:")
        self.info("""
Example:
    # Create a mock HTTP request
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/my_function',
        params={'name': 'Test'}
    )
    
    # Or with JSON body
    req = func.HttpRequest(
        method='POST',
        body=b'{"name": "Test"}',
        url='/api/my_function',
        params={}
    )
    
    # Call the function
    response = my_function(req)
    
    # Check the response
    print(response.get_body().decode())
    print(f"Status: {response.status_code}")
    """)

    def handle(self, args):
        app = self.import_function_app()
        if not app:
            return

        # Create namespace with azure.functions and the app module
        namespace = {
            'func': func,
            'app': app,
        }
        
        # Add all functions to the namespace
        namespace.update({
            name: obj for name, obj in vars(app).items() 
            if callable(obj) and hasattr(obj, '__route__')
        })
        
        self.print_help(app)
        self.start_repl(namespace)


# Command instance to be used by the CLI
command = ConsoleCommand()
