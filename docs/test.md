# legend test

The `test` command runs your test suite using pytest, automatically configuring the test environment.

**Alias**: `t`

## Usage

```bash
legend test [PYTEST_ARGS...]
```

## Arguments

- `PYTEST_ARGS` (optional): Any additional arguments to pass directly to pytest

## What It Does

1. Sets up the test environment (`LEGEND_ENVIRONMENT=test`)
2. Verifies the virtual environment exists
3. Runs pytest with your specified arguments
4. Displays test results and coverage information

## Features

- **Automatic Environment**: Sets `LEGEND_ENVIRONMENT=test`
- **Virtual Environment**: Uses project's virtual environment
- **Pytest Integration**: Full access to pytest features
- **Cross-Platform**: Works on Windows and Unix-based systems

## Examples

Run all tests:
```bash
legend test
```

Run specific test file:
```bash
legend test test/functions/hello_world_test.py
```

Run tests with specific marker:
```bash
legend test -m "integration"
```

Run tests with coverage:
```bash
legend test --cov=functions
```

Run tests in verbose mode:
```bash
legend test -v
```

## Test Structure

Legend CLI creates a standard test structure:
```
my-function-app/
└── test/
    ├── conftest.py         # Shared pytest fixtures
    ├── functions/          # Function-specific tests
    │   ├── __init__.py
    │   └── hello_world_test.py
    └── lib/               # Library code tests
        └── __init__.py
```

## Writing Tests

Example test file (`test/functions/hello_world_test.py`):
```python
import azure.functions as func
from function_app import hello_world

def test_hello_world():
    # Arrange
    req = func.HttpRequest(
        method='GET',
        url='/api/hello_world',
        body=None,
        params={'name': 'Test'}
    )

    # Act
    response = hello_world(req)

    # Assert
    assert response.status_code == 200
    assert "Hello Test!" in response.get_body().decode()
```

## Common Issues

1. **Missing Virtual Environment**
   ```bash
   legend bootstrap
   ```

2. **Import Errors**
   - Ensure `PYTHONPATH` includes your project root
   - Check for missing dependencies
   - Verify test file naming (`_test.py` suffix)

3. **Configuration Issues**
   - Check `config/test.toml`
   - Verify environment variables
   - Use pytest's `-v` flag for more details

## Best Practices

1. **Test Organization**
   - Use meaningful test names
   - Group related tests with classes
   - Use pytest fixtures for setup/teardown

2. **Test Coverage**
   - Aim for high coverage
   - Use `--cov` flag to measure
   - Add coverage configuration in `pytest.ini`

3. **Test Types**
   - Unit tests for functions
   - Integration tests for workflows
   - End-to-end tests for full scenarios

## Related Commands

- [run](run.md) - Run the function app locally
- [console](console.md) - Start an interactive console
- [deploy](deploy.md) - Deploy to Azure
