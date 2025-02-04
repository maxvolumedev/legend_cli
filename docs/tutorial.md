# Getting Started with Legend CLI

This tutorial will walk you through creating and deploying your first Azure Function app using Legend CLI. We'll create a simple HTTP-triggered function, test it locally, and deploy it to Azure.

## Prerequisites

Before you begin, make sure you have:
- [Python 3.9 or higher](https://www.python.org/downloads/)
- An Azure subscription
- A GitHub account (for CI/CD via GitHub workflows)

## Step 1: Installation

Install Legend CLI using pip:

```bash
pip install git+https://github.com/maxvolumedev/legend_cli.git
```

Verify the installation:
```bash
legend --version
```

## Step 2: Bootstrap Your Environment

Run the bootstrap command to check and install any missing dependencies:

```bash
legend bootstrap
```

## Step 3: Create a New Function App

Create a new function app project:

```bash
legend new my-first-app
cd my-first-app
```

This creates a new project with the following structure:
```
my-first-app/
├── .github/workflows/    # CI/CD workflows
├── config/              # Configuration files
├── lib/                 # Shared code
├── test/               # Test files
└── functions/          # Azure Functions
```

## Step 4: Generate Your First Function

Generate a new HTTP-triggered function:

```bash
legend generate function hello_world
```

This creates:
- A new function in your project
- A corresponding test file

## Step 5: Test Locally

First, let's run the test suite:

```bash
legend test
```

Then start the local development server:

```bash
legend run
```

Your function will be available at `http://localhost:7071/api/hello_world`

## Step 6: Interactive Development

Legend CLI provides an interactive console for development:

```bash
legend console
```

Try out your function:
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

## Step 7: Provision Azure Resources

Before deploying, we need to provision Azure resources:

```bash
legend provision sit
```

This creates all necessary Azure resources in the SIT environment:
- Resource group
- Storage account
- App Service Plan
- Function app
- Key vault
- Application Insights

## Step 8: Deploy to Azure

Deploy your function app:

```bash
legend deploy sit
```

## Step 9: View Deployment Information

Check your deployment details:

```bash
legend info sit
```

This shows:
- Function URLs
- Access keys
- Resource information

## Step 10: Publish project to GitHub

1. Create a new repository on GitHub for your project

2. Initialize git in your project directory if you haven't already:
```bash
git init
```

3. Add your GitHub repository as the remote origin:
```bash
git remote add origin https://github.com/username/your-repo-name.git
```

4. Stage and commit your files:
```bash
git add .
git commit -m "Initial commit"
```

5. Push your code to GitHub:
```bash
git push -u origin main
```

## Step 11: Set Up CI/CD

Generate a GitHub Actions workflow:

```bash
legend generate github-workflow sit
```

This creates a workflow that will:
1. Run tests
2. Provision resources (if needed)
3. Deploy your application

## Next Steps

Now that you have your first function app up and running, you might want to:

1. Add more functions using `legend generate function`
2. Set up additional environments (uat, production)
3. Customize your configuration in `config/`
4. Explore the [command reference docs](overview.md#getting-started)

## Troubleshooting

If you encounter any issues:

1. Use the `--verbose` flag for more detailed output
2. Check the logs in Azure Portal
3. Use `legend console` for interactive debugging
4. Ensure all prerequisites are properly installed

Remember, you can always use `legend --help` or `legend COMMAND --help` for command-specific information.
