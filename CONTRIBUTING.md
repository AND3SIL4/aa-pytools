# Contributing to aa-pytools

Thank you for your interest in contributing to **aa-pytools**! This guide will help you get started with contributing to our Python library for Automation Anywhere integration.

## 📋 Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Git Standards](#git-standards)
- [Pull Request Process](#pull-request-process)
- [Coding Guidelines](#coding-guidelines)

## 🛠 Development Setup

### Prerequisites

- **Python 3.13+** - Required for this project
- **uv** - Modern Python package manager (recommended)
- **Git** - Version control
- **make** - Build automation (optional but recommended)

### Cloning the Repository

```bash
# Clone the repository
git clone https://github.com/AND3SIL4/aa-pytools.git
cd aa-pytools

# Create a virtual environment (if not using uv)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Installing Dependencies

```bash
# Using uv (recommended)
make install
# or: uv sync

# Using pip (alternative)
pip install -e ".[dev]"
```

### Environment Configuration

This project doesn't require environment variables for basic development. However, for testing Automation Anywhere integration features, you may create a `.env` file:

```bash
# .env file (optional, for integration testing)
AA_CONTROL_ROOM_URL=https://your-control-room.com
AA_API_KEY=your-api-key-here
AA_USERNAME=your-username
AA_PASSWORD=your-password
```

> **Note:** Never commit the `.env` file to version control. It's already included in `.gitignore`.

## 📁 Project Structure

```
aa-pytools/
├── src/aa_pytools/           # Main package source
│   ├── __init__.py          # Package exports
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   └── logging.py       # Logging system
│   ├── decorators/          # Specialized decorators
│   │   ├── __init__.py
│   │   └── safe_execute.py  # Safe execution decorator
│   ├── api/                 # API integration (placeholder)
│   ├── execution/           # Execution management (placeholder)
│   └── vault/               # Vault integration (placeholder)
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── decorators/          # Decorator tests
│   └── modules/             # Core module tests
├── scripts/                 # Utility scripts
│   └── bump_version.py      # Version management
├── pyproject.toml          # Project configuration
├── Makefile                 # Build automation
├── .better-commits.json     # Git commit standards
├── AGENTS.md               # AI agent guidelines
└── README.md               # Project documentation
```

## 🔄 Development Workflow

### 1. Create a Feature Branch

We recommend using `git flow` for branch management:

```bash
# Install git flow (if not already installed)
# Then create a feature branch
git flow feature start feature-name

# Or using standard Git
git checkout -b feature/feature-name
```

### 2. Make Changes

- Write code following our [Coding Guidelines](#coding-guidelines)
- Add tests for new functionality
- Update documentation as needed

### 3. Run Quality Checks

```bash
# Run all tests
make test

# Check code quality
ruff check .
ruff format .

# Or combine both
ruff check . --fix && ruff format .
```

### 4. Commit Changes

We use `better-commits` for standardized commit messages:

```bash
# Install better-commits if not already installed
npm install -g better-commits

# Then commit
better-commits
```

This will guide you through creating properly formatted commits with emojis and conventional commit types.

## 🧪 Testing

### Running Tests

```bash
# Run all tests with verbose output
make test
# or: pytest -vv

# Run a specific test file
pytest -vv tests/decorators/test_safe_execute.py

# Run a specific test function
pytest -vv tests/decorators/test_safe_execute.py::TestSafeExecuteBasic::test_successful_execution_returns_payload

# Run tests with coverage
pytest -vv --cov=src/aa_pytools --cov-report=term-missing
```

### Writing Tests

- Use **pytest** as the testing framework
- Follow **Arrange-Act-Assert** pattern
- Write descriptive test method names
- Include both success and failure scenarios
- Use fixtures for reusable test data

Example test structure:

```python
class TestFeatureName:
    def test_descriptive_test_name(self):
        """Test that specific behavior works as expected."""
        # Arrange
        setup_data = create_test_data()
        
        # Act
        result = function_being_tested(setup_data)
        
        # Assert
        assert result["status"]
        assert result["result"] == expected_value
```

### Test Organization

- Unit tests go in `tests/` mirroring the `src/` structure
- Integration tests should be marked with `@pytest.mark.integration`
- Use descriptive class names with `Test` prefix
- Group related tests in logical test classes

## 📏 Code Quality

### Linting and Formatting

We use **ruff** for both linting and formatting:

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .

# Do both at once
ruff check . --fix && ruff format .
```

### Type Checking

- Use **type hints** for all function parameters and return values
- Use **union types** with `|` syntax (Python 3.10+)
- Use **Literal types** for string constants
- Import `typing` only when necessary

### Pre-commit Hooks (Recommended)

Set up pre-commit hooks to automatically run quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## 📝 Git Standards

### Commit Message Format

We use **conventional commits** with `better-commits`:

```
type(scope): description (max 70 chars)

Examples:
feat(decorators): add timeout decorator
fix(logging): resolve console output issue
docs(readme): update installation guide
test(safe_execute): add edge case tests
```

### Commit Types

- `feat:` - New features (✨)
- `fix:` - Bug fixes (🐛)
- `docs:` - Documentation changes (📚)
- `perf:` - Performance improvements (🚀)
- `test:` - Test additions/fixes (🧪)
- `build:` - Build system changes (⚙️)

### Branch Naming

- `feature/feature-name` - New features
- `fix/issue-description` - Bug fixes
- `docs/documentation-update` - Documentation changes
- `hotfix/urgent-fix` - Critical fixes

## 🔄 Pull Request Process

### 1. Update and Test

```bash
# Ensure your branch is up to date
git checkout main
git pull origin main
git checkout your-branch
git rebase main

# Run all tests and quality checks
make test
ruff check . --fix && ruff format .
```

### 2. Create Pull Request

- Use a descriptive title following commit message format
- Provide a clear description of changes
- Link any relevant issues
- Include screenshots if applicable

### 3. PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### 4. Code Review

- All contributions require review
- Address feedback promptly
- Keep PRs focused and manageable
- Use draft PRs for work in progress

## 📖 Coding Guidelines

### Python Standards

- **Python 3.13+** required
- Follow **PEP 8** with ruff formatting
- Use **type hints** everywhere
- Write **comprehensive docstrings**

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

```python
# Use UPPER_SNAKE_CASE for module-level constants
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
- Use **decorators** for cross-cutting concerns
- Support **both dict and JSON return formats** where appropriate
- Include **timing information** for performance-critical operations

## 🚀 Building and Publishing

### Local Development

```bash
# Clean build artifacts
make clean

# Build package (includes version bump)
make build

# Bump version specifically
make bump TYPE=minor  # options: major, minor, patch
```

### Publishing (Maintainers Only)

```bash
# Publish to TestPyPI
make publish-test

# Test installation from TestPyPI
make test-download

# Publish to PyPI
make publish
```

## 🤝 Getting Help

- **Issues**: [GitHub Issues](https://github.com/AND3SIL4/aa-pytools/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AND3SIL4/aa-pytools/discussions)
- **Email**: [devaul.fs@gmail.com](mailto:devaul.fs@gmail.com)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

Thank you for contributing to **aa-pytools**! Your contributions help make RPA development with Automation Anywhere more efficient and enjoyable for everyone. 🚀