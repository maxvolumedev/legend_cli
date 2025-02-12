# legend env

The `env` command reads the configuration for an environment and outputs export commands that can be evaluated in a shell. This can be used to expose the environment configuration to shell scripts.

**Alias**: `e`

## Usage

To print environment variable export commands:

```bash
legend env [ENVIRONMENT]
```

To automatically set up an environment in a shell (zsh, bash):

```bash
eval $(legend env [ENVIRONMENT])
```

## Arguments

- `ENVIRONMENT` (required): Target environment to deploy to (e.g., sit, uat, production)

## What It Does

1. 

## Examples


