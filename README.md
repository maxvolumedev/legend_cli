# Legend CLI

A command-line interface for managing Trade Ledger integration adapters with Azure Functions.

## Prerequisites

- Python 3.9 or higher
- Node.js and npm (for Azure Functions Core Tools)
- Git

### Installing Azure Functions Core Tools

The Azure Functions Core Tools are required to create and run Azure Functions locally. Install them using npm:

```bash
npm install -g azure-functions-core-tools@4
```

Or using Homebrew on macOS:

```bash
brew tap azure/functions
brew install azure-functions-core-tools@4
```

For other installation methods, see the [official documentation](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local).

## Installation

### Option 1: Install from PyPI (Recommended)

The simplest way to install Legend CLI is via pip:

```bash
pip install legend-cli
```

This will install the `legend` command globally.

### Option 2: Install from Source

For development or testing, you can install the package directly from your local source:

```bash
# Install in editable mode
pip install -e /path/to/legend_cli

# Install with development dependencies
pip install -e /path/to/legend_cli[dev]
```

This will install the `legend` command globally, but use your local source code, allowing you to test changes immediately without rebuilding or republishing.

## Running the CLI

There are several ways to run the Legend CLI:

1. **Using the installed command** (after pip install):
   ```bash
   legend new my-app
   ```

2. **Using Python module syntax**:
   ```bash
   python -m legend new my-app
   ```

3. **During development** (from the source directory):
   ```bash
   # Using the development script
   ./bin/legend new my-app
   
   # Or using Python directly
   PYTHONPATH=/path/to/legend_cli python -m legend new my-app
   ```

### Development Setup

1. Clone this repository
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   .venv\Scripts\activate     # On Windows
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Quick Install (Development)

To make the `legend` command available system-wide when developing, run:

```bash
./bin/install
```

This will create a symlink in `/usr/local/bin`. To install to a different location:

```bash
./bin/install /your/preferred/bin/path
```

### Manual Installation (Development)

If you prefer not to use the install script, you can manually create a symlink:

```bash
ln -s /path/to/legend_cli/bin/legend /usr/local/bin/legend
```

## Commands

### Create a new Function App

```bash
legend new <app_name>
```

This will:
- Create a new Azure Function App
- Initialize a Git repository
- Set up test directory

### Generate a new Function

```bash
legend g[enerate] function <function_name>
```

This will:
- Create a new Azure Function
- Generate function code from template
- Create corresponding test file

### Function Templates

The following function templates are available:

* HTTP trigger
* Queue trigger
* Timer trigger

You can specify a template when generating a new function:

```bash
legend generate function my_function --template "Queue trigger"
```

To see all available templates:

```bash
func templates list
```

### Run the Function App locally

```bash
legend r[un]
```

### Run tests

```bash
legend t[est]
```

### Start Python REPL

```bash
legend c[onsole]
```

Loads all functions into an interactive Python console.

## Command Abbreviations

Commands can be abbreviated to their first letter unless there is ambiguity:
- `legend n` = `legend new`
- `legend g` = `legend generate`
- `legend r` = `legend run`
- `legend t` = `legend test`
- `legend c` = `legend console`
