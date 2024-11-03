# Avro Schema Generator - Tool for generating Avro schema from JSON

> **Warning**
> This tool is no longer maintained and is published solely for reference and logic reuse purposes.
## Installation

```bash
pip install filet
```

## Prerequisites

- Python 3.9+
- poetry
- glab (optional) For release management (commands)
- cmake (optional) For cpp development
- make (optional) For makefiles
- ninja (optional) For cpp development
- pre-commit (optional) For pre-commit hooks

## Commands

### Install the package using makefiles:

```bash
make install
```

### Build dist using makefiles:

```bash
make dist
```

### Run tests (pytest) using makefiles:

```bash
make test
```

### Run cpp tests (catch2) using makefiles:

```bash
make test-cpp
```

### Run all tests using makefiles:

```bash
make test-all
```

### Run lint using makefiles:

```bash
make lint
```

### Create dev venv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry
```

### Bump Version:

```bash
make bump-<major|minor|patch>
```

### Install pre-commit:

```bash
pre-commit install
```

### Update pre-commit:

```bash
pre-commit update -a
```

### Run pre-commit:

```bash
pre-commit run -a
```

## Manage Dependencies

### Add new dependency:

```bash
poetry add <dependency>
```

### Update dependencies in the `pyproject.toml` file:

Prod-dependencies: dependencies in -> `[tool.poetry.dependencies]` Section
Dev-dependencies: dependencies in -> `[tool.poetry.dev-dependencies]` Section

### Update lock file:

```bash
poetry update
```
