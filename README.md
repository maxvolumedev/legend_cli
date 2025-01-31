# Legend CLI

A command-line interface for managing Azure Functions, inspired by Ruby on Rails.

## Prerequisites

- Python 3.9 or higher
- Azure Functions Core Tools
- Git

## Installation

### Option 1: Install from PyPI (Recommended)

The simplest way to install Legend CLI is via pip:

```bash
pip install legend-cli
```

This will install the `legend` command globally, similar to how `gem install rails` works.

### Option 2: Install from Source

For development or testing, you can install the package directly from your local source:

```bash
# Install in editable mode
pip install -e /path/to/legend_cli

# Install with development dependencies
pip install -e /path/to/legend_cli[dev]
```

This will install the `legend` command globally, but use your local source code, allowing you to test changes immediately without rebuilding or republishing.

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
