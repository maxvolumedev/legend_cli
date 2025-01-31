# Legend CLI

A command-line interface for managing Azure Functions, inspired by Ruby on Rails.

## Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)
- Azure Functions Core Tools
- Git

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   poetry install
   ```

## Commands

### Create a new Function App

```bash
legend new <app_name>
```

This will:
- Create a new Azure Function App
- Initialize a Git repository
- Set up Poetry for dependency management
- Create GitHub Actions workflow
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
