# legend bootstrap

Checks and installs required dependencies for Legend CLI development. Run this command before creating your first project to ensure you're good to go.

## Usage

```bash
legend bootstrap
```

## Dependencies

The command checks for and helps install:

- [Homebrew](https://brew.sh) - Package manager for macOS
- [Git](https://git-scm.com) - Version control
- pip - Python package installer
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local) - Local development tools
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) - Azure command-line interface
- [GitHub CLI](https://github.com/cli/cli) - GitHub command-line interface

## Example

```bash
> legend bootstrap
Checking dependencies...

Checking Homebrew...
✅ Homebrew is installed

Checking Git...
✅ Git is installed

Checking pip...
✅ pip is installed

Checking Azure Functions Core Tools...
✅ Azure Functions Core Tools is installed

Checking Azure CLI...
✅ Azure CLI is installed

Checking Github CLI...
⛔️ Github CLI is not installed

Missing dependencies:

Github CLI:
  To install: brew install gh
  Would you like to install Github CLI now? [y/N]
```

## Notes

- Currently supports macOS only
- Uses Homebrew as the package manager
