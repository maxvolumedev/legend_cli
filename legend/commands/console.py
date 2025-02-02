import os
import importlib.util
import azure.functions as func

def start_repl(namespace):
    """Start the best available REPL."""
    print("\nChecking available REPLs...")
    try:
        import sys
        from ptpython.repl import embed
        print("✓ ptpython found, using enhanced REPL")
        embed(globals=namespace, locals=namespace)
    except ImportError as e:
        print(f"✗ ptpython not found ({str(e)}), falling back to standard REPL")
        import code
        code.interact(local=namespace)

def import_function_app():
    """Import the function_app module."""
    if not os.path.exists('function_app.py'):
        print("⛔️Error: function_app.py not found in current directory")
        return None
    
    try:
        spec = importlib.util.spec_from_file_location('function_app', 'function_app.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Failed to load function_app.py: {e}")
        return None

def print_help(app):
    """Print helpful instructions for using the console."""
    print("\nLegend Console - Your functions are loaded and ready to test!")
    print("\nAvailable functions from function_app.py:")
    
    # Find all functions with the @app.route decorator
    funcs = [name for name, obj in vars(app).items() 
            if callable(obj) and hasattr(obj, '__route__')]
    
    for func_name in funcs:
        print(f"  - {func_name}")
    
    print("\nTo test a function, create a mock request and call it:")
    print("""
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

def run(args):
    app = import_function_app()
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
    
    print_help(app)
    start_repl(namespace)
