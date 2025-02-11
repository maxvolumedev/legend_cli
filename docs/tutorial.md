# Getting Started with Legend CLI

This tutorial will walk you through creating and deploying your first Azure Function app using Legend CLI. We'll create a simple HTTP-triggered function, test it locally, and deploy it to Azure. Legend CLI simplifies the entire development lifecycle of Azure Functions, from local development to production deployment.

## Prerequisites

Before you begin, make sure you have:
- [Python 3.9 or higher](https://www.python.org/downloads/)
- An Azure subscription
- A GitHub account (for CI/CD via GitHub workflows)

## Step 1: Installation

Install Legend CLI using pip.

```bash
pip install git+https://github.com/maxvolumedev/legend_cli.git
```

Verify the installation by checking the version:
```bash
legend --version
```

## Step 2: Bootstrap Your Environment

Legend CLI includes a bootstrap command that helps you set up your development environment. The `bootstrap` command checks for required dependencies (pip, git, Homebrew, Azure CLI, Azure Function Core Tools, and GitHub CLI) and offers instructions on how to install them.

Run the bootstrap command:

```bash
legend bootstrap
```

Follow any prompts to install missing dependencies.

## Step 3: Create a New Function App

Create a new function app project. The `new` command sets up a complete project structure with all necessary files and configurations:

```bash
legend new my-first-app
cd my-first-app
```

This creates a new project with the following structure:
```
my-first-app/
├── .github/workflows/    # CI/CD workflows for automated deployments
├── config/              # Environment-specific configurations (dev, sit, uat, prod)
├── lib/                 # Shared code and utilities
├── test/               # Test files for your functions
└── functions/          # Your Azure Functions live here
└── function_app.py     # The main entry point for your function app
```

## Step 4: Generate Your First Function

Generate a new HTTP-triggered function. The `generate` command creates both the function and its test file:

```bash
legend generate function hello_world
```

And choose "ANONYMOUS" for the authentication level when prompted.

This command:
1. Adds a new function to your `function_app.py`
2. Generates a test file in `test/functions/hello_world_test.py`

**Note**: There is currently no check for existence of a function with the same name. If you call legend g function more than once with the same name, a function with the same name will be generated. This will cause an error when you run the app.

## Step 5: Test Locally

First, let's run the test suite:

```bash
legend test
```

This command:
- Runs all tests in the `test/` directory

Then start the local development server:

```bash
legend run
```

This command starts a local server using Azure Functions Core Tools and exposes your function at `http://localhost:7071/api/hello_world`

Open the URL in a browser, or try it out on the command line:
```bash
curl http://localhost:7071/api/hello_world?name=Legend
```

## Step 6: Interactive Development

Legend CLI includes a powerful interactive console for development and debugging. This is particularly useful for:
- Testing function behavior
- Debugging issues
- Exploring Azure SDK functionality
- Prototyping new features

Launch the interactive console:

```bash
legend console
```

Try out your function with this example:
```python
# Create a mock request
req = func.HttpRequest(
    method='GET',
    url='/api/hello_world',
    body=None,
    params={'name': 'Legend'}
)

# Call your function
response = app.hello_world(req)

# Check the response
print(response.get_body().decode())
```

The console provides a full Python environment with:
- Your function app pre-loaded
- Azure SDK libraries available
- Access to your configuration

## Step 7: Add a Function with Simple Authentication

Add another function with simple authentication:

```bash
legend add hello_world_authenticated
```

And choose "FUNCTION" for the authentication level when prompted.

**Note**: When running locally, this function does not require authentication. After we deploy our app, we will retrieve the keys for the live app using the `legend info` command.

## Step 8: Provision Azure Resources

Before deploying, we need to provision Azure resources. The `provision` command handles this automatically:

```bash
legend provision sit
```

This command:
1. Creates a resource group for isolation
2. Sets up a storage account for function state
3. Provisions an App Service Plan
4. Creates a Function App instance
5. Configures Key Vault for secrets
6. Sets up Application Insights for monitoring

All resources are tagged and named according to your project's configuration.

## Step 9: Deploy to Azure

Deploy your function app to Azure. The `deploy` command handles the entire deployment process:

```bash
legend deploy sit
```

This command:
1. Validates your code and configuration
2. Packages your function app
3. Uploads the package to Azure
4. Updates application settings
5. Restarts the function app
6. Verifies the deployment

## Step 10: View Function URLs (and Authentication Keys)

Check your deployment details using the `info` command:

```bash
legend info sit
```

This shows all function URLs for the app and associated access keys

## Step 11: Publish Project to GitHub

Setting up version control is crucial for team development and CI/CD. Follow these steps:

1. Create a new repository on GitHub for your project (private in this case, or use --public):
```bash
gh repo create my-first-app --private
```

1. Add your GitHub repository as the remote origin:
```bash
git remote add origin https://github.com/username/your-repo-name.git
```

1. Stage and commit your files:
```bash
git add .
git commit -m "Initial commit"
```

1. Push your code to GitHub:
```bash
git push -u origin main
```

This sets up version control and prepares your project for CI/CD.

## Step 12: Set Up CI/CD

Legend CLI can automatically configure GitHub Actions for continuous integration and deployment:

```bash
legend generate github-workflow sit
```

Create a `sit` branch, commit and push your changes:
```bash
git checkout -b sit
git add --all
git commit -m "Ready for deployment"
git push -u origin sit
```

This command:
1. Creates a workflow file in `.github/workflows/`
2. Sets up Azure credentials securely
3. Configures the following pipeline stages:
   - Run tests and code quality checks
   - Provision or update Azure resources
   - Deploy your application
   - Verify the deployment

The workflow runs automatically on pushes to your main branch.

## Next Steps

Now that you have your first function app up and running, here are some ways to expand your application:

1. Add more functions using `legend generate function`
   - Create different types of triggers (HTTP, Timer, Queue)
   - Implement business logic
   - Add proper error handling

2. Set up additional environments (uat, production)
   - Configure environment-specific settings
   - Set up proper access controls
   - Implement staging and promotion workflows

3. Customize your configuration in `config/`
   - Add application settings
   - Configure scaling rules
   - Set up custom domains

4. Explore the [Command Reference](command_reference.md) for advanced features and options

## Troubleshooting

If you encounter any issues:

1. Use the `--verbose` flag for detailed logging:
   ```bash
   legend deploy sit --verbose
   ```

2. Check Azure Portal for:
   - Function app logs
   - Application Insights metrics
   - Resource health status

3. Use `legend console` for interactive debugging:
   - Test function behavior
   - Verify configurations
   - Check Azure connectivity

4. Ensure all prerequisites are properly installed:
   ```bash
   legend bootstrap --verbose
   ```

Remember, you can always use `legend --help` or `legend COMMAND --help` for command-specific information and examples.

## Support

If you need help:
1. Check the [Command Reference](command_reference.md)
2. Open an issue on GitHub
3. Use the `--verbose` flag to get more information
4. Join our community discussions
