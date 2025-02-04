# legend run

The `run` command starts your Azure Function App locally for development and testing.

**Alias**: `r`

## Usage

```bash
legend run [--verbose]
```

## Arguments

- `--verbose`, `-v` (optional): Enable verbose output for detailed logging

## What It Does

1. Verifies that `function_app.py` exists in the current directory
2. Starts the Azure Functions runtime locally
3. Watches for file changes and automatically reloads
4. Provides real-time logging output

## Features

- **Hot Reload**: Automatically detects and applies code changes
- **Local Debugging**: Supports attaching debuggers
- **Environment Variables**: Uses `local.settings.json` for configuration
- **Port Configuration**: Default port is 7071
- **CORS Support**: Configure in `local.settings.json`

## Examples

Start the function app:
```bash
legend run
```

Start with verbose logging:
```bash
legend run --verbose
```

## Accessing Your Functions

Once running:
- HTTP-triggered functions: `http://localhost:7071/api/[function_name]`
- Admin API: `http://localhost:7071/admin/functions`
- Host JSON: `http://localhost:7071/admin/host`

## Environment Variables

The command uses environment variables from:
1. `local.settings.json`
2. Your shell environment
3. Configuration files in `config/`

Priority order (highest to lowest):
1. Shell environment variables
2. `local.settings.json`
3. Configuration files

## Debugging

1. **Visual Studio Code**
   - Use the Azure Functions extension
   - Set breakpoints in your code
   - Start debugging session

2. **Python Debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

3. **Logging**
   ```python
   import logging
   
   def main(req):
       logging.info("Processing request...")
   ```

## Common Issues

1. **Port Already in Use**
   - Another process is using port 7071
   - Stop other function apps or services
   - Configure a different port in `local.settings.json`

2. **Missing Dependencies**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Configuration Errors**
   - Check `local.settings.json`
   - Verify environment variables
   - Run with `--verbose` flag

## Related Commands

- [test](test.md) - Run the test suite
- [console](console.md) - Start an interactive console
- [deploy](deploy.md) - Deploy to Azure
