# Development

## Setup

```bash
make setup
```

## Common tasks

```bash
make lint      # ruff + mypy
make format    # auto-format
make test      # pytest
make security  # security scans
make docker-build
```

## Pre-commit

```bash
uv run pre-commit install
```