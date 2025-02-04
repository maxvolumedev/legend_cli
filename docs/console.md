# legend console

The `console` command starts an interactive Python REPL with your function app pre-loaded, making it easy to test and debug your functions.

**Alias**: `c`

## Usage

```bash
legend console
```

## Features

- **Enhanced REPL**: Uses `ptpython` if available for a better experience
- **Auto-Import**: Pre-loads your function app and Azure Functions module
- **Function Discovery**: Lists all available functions in your app
- **Helper Examples**: Provides example code for testing

## What It Does

1. Checks for virtual environment
2. Imports your `function_app.py`
3. Sets up a Python REPL with:
   - Your function app loaded as `app`
   - Azure Functions module (`azure.functions`)
   - Helper functions and examples
4. Lists available functions and usage examples

## Interactive Testing

Here's how to test your functions in the console:

```python
# Create a GET request
req = func.HttpRequest(
    method='GET',
    body=None,
    url='/api/my_function',
    params={'name': 'Test'}
)

# Create a POST request with JSON body
req = func.HttpRequest(
    method='POST',
    body=b'{"name": "Test"}',
    url='/api/my_function',
    params={}
)

# Call your function
response = app.my_function(req)

# Check the response
print(response.get_body().decode())
print(f"Status: {response.status_code}")
```

## Advanced Usage

### Working with Different Triggers

#### Queue Trigger
```python
# Create a queue message
msg = func.QueueMessage(
    body=b'{"order_id": "123"}',
)

# Call your function
result = app.process_queue(msg)
```

#### Blob Trigger
```python
# Create a blob
blob = func.InputStream(
    body=b'Hello, World!'
)

# Call your function
result = app.process_blob(blob)
```

### Testing with Different Content Types

```python
# Form data
req = func.HttpRequest(
    method='POST',
    body=b'name=Test&age=25',
    url='/api/my_function',
    params={},
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }
)

# Binary data
req = func.HttpRequest(
    method='POST',
    body=b'\x00\x01\x02\x03',
    url='/api/my_function',
    params={},
    headers={
        'Content-Type': 'application/octet-stream'
    }
)
```

## Tips and Tricks

1. **Auto-Completion**
   - Use Tab for completion
   - Use `dir(app)` to list attributes
   - Use `help(app.function_name)` for documentation

2. **Debugging**
   ```python
   import pdb
   
   # Set breakpoint in your code
   pdb.set_trace()
   
   # Then call your function
   response = app.my_function(req)
   ```

3. **Environment Variables**
   ```python
   import os
   
   # Check current environment
   print(os.getenv('LEGEND_ENVIRONMENT'))
   
   # Set environment variable
   os.environ['MY_SETTING'] = 'value'
   ```

## Common Issues

1. **Missing Virtual Environment**
   ```bash
   legend bootstrap
   ```

2. **Import Errors**
   - Check `requirements.txt`
   - Verify virtual environment activation
   - Check for syntax errors in your code

3. **Enhanced REPL Not Available**
   ```bash
   pip install ptpython
   ```

## Related Commands

- [run](run.md) - Run the function app locally
- [test](test.md) - Run the test suite
- [generate](generate.md) - Generate new functions
