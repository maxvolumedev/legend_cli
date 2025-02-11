# legend test

The `test` command runs your test suite using pytest, automatically configuring the test environment.

**Alias**: `t`

## Usage

```bash
legend test -- [PYTEST_ARGS...]
```

## Arguments

- `PYTEST_ARGS` (optional): Arguments to pass to pytest. All arguments after `--` are passed directly to pytest, so you can use any pytest arguments like `--cov`, `-v`, `-k`, etc.

## What It Does

1. Sets up the test environment (`LEGEND_ENVIRONMENT=test`)
2. Verifies the virtual environment exists
3. Runs pytest with your specified arguments
4. Displays test results and coverage information

## Examples

Run all tests:
```bash
legend test
```

Run specific test file:
```bash
legend test -- test/functions/hello_world_test.py
```

Run tests with specific marker:
```bash
legend test -- -m "integration"
```

Run tests with coverage:
```bash
legend test -- --cov
```

Run tests with coverage for specific package:
```bash
legend test -- --cov=functions
```

Run tests in verbose mode:
```bash
legend test -- -v
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

## Related Commands

- [run](run.md) - Run the function app locally
- [console](console.md) - Start an interactive console
- [deploy](deploy.md) - Deploy to Azure
