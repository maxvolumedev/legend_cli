# legend deploy

The `deploy` command deploys your function app to Azure, with built-in safety checks and version control integration.

## Usage

```bash
legend deploy ENVIRONMENT
```

## Arguments

- `ENVIRONMENT` (required): Target environment to deploy to (e.g., sit, uat, production)

## What It Does

1. **Pre-deployment Checks**
   - Verifies you're in a Legend project
   - Validates the environment configuration
   - Checks Git repository status
   - Verifies branch compatibility

2. **Git Integration**
   - Checks for uncommitted changes
   - Verifies branch matches environment configuration
   - Compares branches for deployment safety
   - Shows diff summary if branches don't match

3. **Deployment Process**
   - Packages application code
   - Updates Azure Function App
   - Configures application settings
   - Verifies deployment success

## Git Integration Features

### Branch Verification
```bash
# Checks if current branch matches configured branch
Current branch: feature/new-function
Expected branch: main
```

### Clean Working Directory
```bash
# Shows uncommitted changes
M function_app.py
? new_file.txt
```

### Branch Comparison
```bash
# Shows diff between branches
Changes:
 function_app.py | 10 +++++-----
 requirements.txt | 2 +-
```

## Best Practices

1. **Version Control**
   - Commit all changes before deploying
   - Use environment-specific branches
   - Follow Git workflow patterns

2. **Deployment Safety**
   - Test locally before deploying
   - Deploy to lower environments first
   - Review changes before production deployment

3. **Configuration Management**
   - Keep environment configs up to date
   - Use Key Vault for secrets
   - Review app settings before deploy

## Common Issues

1. **Uncommitted Changes**
   ```bash
   # Commit changes
   git add .
   git commit -m "Ready for deployment"
   
   # Or stash them
   git stash
   ```

2. **Wrong Branch**
   ```bash
   # Switch to correct branch
   git checkout main
   
   # Or update config
   # Edit config/[ENV].toml
   ```

3. **Deployment Failures**
   - Check Azure resource status
   - Verify app settings
   - Review deployment logs
   - Check application insights

## Environment Configuration

Each environment should have:
1. Branch configuration in `config/[ENV].toml`
2. Appropriate Azure resources (use `legend provision`)
3. Required secrets in Key Vault

Example `config/production.toml`:
```toml
[azure]
branch = "main"  # Required branch for deployment
```

## Deployment Process

1. **Validation**
   ```bash
   # Checks performed
   ✓ Legend project structure
   ✓ Environment configuration
   ✓ Git status
   ✓ Branch verification
   ```

2. **Packaging**
   ```bash
   # Steps
   ✓ Collect function code
   ✓ Include dependencies
   ✓ Prepare deployment package
   ```

3. **Deployment**
   ```bash
   # Azure operations
   ✓ Update function app
   ✓ Configure settings
   ✓ Verify deployment
   ```

## Related Commands

- [provision](provision.md) - Set up Azure resources
- [info](info.md) - View deployment information
- [run](run.md) - Test locally before deploying
