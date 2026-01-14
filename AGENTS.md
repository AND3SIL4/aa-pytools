# AGENTS.md

This file contains guidelines and commands for AI agents working on the aa-pytools project.

## Project Overview

**aa-pytools** is a Python library for Automation Anywhere + Python integration, targeting RPA developers. The project uses modern Python development tools and follows best practices for packaging, testing, and development workflow.

## Development Commands

### Environment Setup
```bash
# Install dependencies (requires uv package manager)
make install
# or: uv sync
```

### Testing
```bash
# Run all tests with verbose output
make test
# or: pytest -vv

# Run a single test file
pytest -vv tests/decorators/test_safe_execute.py

# Run a single test function
pytest -vv tests/decorators/test_safe_execute.py::TestSafeExecuteBasic::test_successful_execution_returns_payload

# Run tests with coverage
pytest -vv --cov=src/aa_pytools --cov-report=term-missing
```

### Code Quality
```bash
# Lint code
ruff check .

# Format code
ruff format .

# Check and fix in one command
ruff check . --fix && ruff format .
```

### Build & Release
```bash
# Clean build artifacts
make clean

# Build package (includes version bump)
make build

# Bump version (default: patch)
make bump TYPE=minor  # options: major, minor, patch

# Publish to TestPyPI
make publish-test

# Publish to PyPI
make publish
```

## Code Style Guidelines

### General Principles
- **Python 3.13+** required
- Use **type hints** for all function parameters and return values
- Follow **PEP 8** with ruff formatting
- Write **comprehensive docstrings** for all modules and public functions
- Use **descriptive variable names** (avoid single letters except for counters)

### Import Organization
```python
# Standard library imports first
import functools
import json
import sys
from pathlib import Path
from typing import Literal

# Third-party imports second
import pytest

# Local imports third
from aa_pytools.decorators.safe_execute import safe_execute
```

### Type Hints
- Use **union types** with `|` syntax (Python 3.10+)
- Use **Literal types** for string constants
- Import `typing` only when necessary (prefer built-in types)
- Example: `def func(name: str) -> dict[str, any] | str:`

### Docstring Format
```python
"""
Module description.

This module provides functionality for...

Usage:
    example = func()

Args:
    param1 (str): Description of parameter
    param2 (int | None): Optional parameter description

Returns:
    dict[str, any]: Description of return value

Raises:
    ValueError: When invalid input provided

TODO:
    - Future improvement notes
"""
```

### Constants
- Use **UPPER_SNAKE_CASE** for module-level constants
- Group related constants together
- Provide descriptive comments for constant groups
```python
# Default configuration values
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
```

### Error Handling
- Use **structured error payloads** in decorators and utilities
- Include **error type** and **message** in error responses
- Add **trace information** when debugging is needed
- Use the package logging system for error tracking

### Function Design
- Keep functions **focused and single-purpose**
- Use **decorators** for cross-cutting concerns (logging, error handling)
- Support **both dict and JSON return formats** where appropriate
- Include **timing information** for performance-critical operations

### Class Design
- Use **descriptive class names** with `Test` prefix for test classes
- Group related tests in logical test classes
- Use **pytest fixtures** for reusable test data
- Follow **Arrange-Act-Assert** pattern in tests

### Testing Guidelines
- Write **comprehensive tests** for all public functions
- Test **both success and failure scenarios**
- Use **descriptive test method names** that explain what is being tested
- Include **edge cases** and **error conditions**
- Use **fixtures** for reusable test setup
- Test **decorator behavior** with different parameter combinations

### Module Structure
```
src/aa_pytools/
├── __init__.py          # Package exports
├── core/               # Core functionality (logging, etc.)
├── decorators/         # Specialized decorators
├── execution/         # Execution management
├── vault/             # Credential management
└── api/               # API integration
```

### Git Commit Standards
The project uses **better-commits** with conventional commits:
- `feat:` - New features (✨)
- `fix:` - Bug fixes (🐛)
- `docs:` - Documentation changes (📚)
- `perf:` - Performance improvements (🚀)
- `test:` - Test additions/fixes (🧪)
- `build:` - Build system changes (⚙️)

Commit format: `type(scope): description` (max 70 chars for title)

### Package Configuration
- **pyproject.toml** is the single source of truth for project configuration
- Use **uv** for dependency management
- **setuptools** as build backend
- **pytest** for testing framework
- **ruff** for linting and formatting

### Logging Integration
- Use the package logging system from `aa_pytools.core.logging`
- Auto-configure on first use within the package
- Support both console and file logging
- Use structured logging with consistent formatting

### Development Workflow
1. **Install dependencies**: `make install`
2. **Write code** following style guidelines
3. **Run linting**: `ruff check . --fix && ruff format .`
4. **Run tests**: `make test`
5. **Build package**: `make build`
6. **Publish** when ready (test first, then production)

### Special Considerations
- This is an **RPA-focused library** for Automation Anywhere integration
- **Error safety** is critical - use decorators like `@safe_execute`
- **Performance timing** should be included in key operations
- **Credential security** is important in vault operations
- **API integration** should be robust and well-tested

### When Working on This Project
1. Always run tests after changes: `make test`
2. Use the existing logging system, don't import `logging` directly
3. Follow the established patterns in similar modules
4. Add comprehensive tests for new functionality
5. Update documentation when adding new features
6. Use semantic versioning for releases