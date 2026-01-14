# aa-pytools

[![PyPI version](https://badge.fury.io/py/aa-pytools.svg)](https://badge.fury.io/py/aa-pytools)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> All Python tools you'll likely need to work with Automation Anywhere

**aa-pytools** is a comprehensive Python library designed to streamline integration between Python applications and Automation Anywhere RPA platform. It provides essential tools, decorators, and utilities that make RPA development more efficient and reliable.

## 🚀 Features

### Core Functionality

- [x] **Advanced Logging System** - Centralized, configurable logging with auto-configuration
- [x] **Safe Execution Decorator** - Error handling with structured payloads and timing information

### Automation Anywhere Integration

- [ ] **Vault Credential Management** - Secure credential fetching from Automation Anywhere vault
- [ ] **Execution Management** - Run and monitor Automation Anywhere executions from Python
- [ ] **REST API Integration** - Complete API client for Automation Anywhere services

### Specialized Decorators

- [x] **`@safe_execute`** - Execute functions safely with comprehensive error handling
- [ ] **`@with_vault("SAP")`** - Automatic credential injection from vault
- [ ] **`@retry_on_failure`** - Intelligent retry mechanism for transient failures
- [ ] **`@timeout(30)`** - Execution timeout protection
- [ ] **`@transactional`** - Transaction management for complex operations
- [ ] **`@queue_worker("INVOICES")`** - Queue-based processing capabilities
- [ ] **`@aa_safe_run`** - Automation Anywhere-specific safe execution

## 📦 Installation

```bash
pip install aa-pytools
```

**Requirements:**

- Python 3.13 or higher
- No external dependencies for core functionality

## 🎯 Quick Start

### Basic Usage

```python
from aa_pytools.decorators import safe_execute
from aa_pytools.core import get_logger

# Use the safe execution decorator
@safe_execute
def risky_operation(data):
    # Your code here
    return process_data(data)

result = risky_operation(my_data)
if result["status"]:
    print(f"Success: {result['result']}")
else:
    print(f"Error: {result['error']}")

# Logging with auto-configuration
logger = get_logger("my_module")
logger.info("This message will be automatically formatted and handled")
```

### Advanced Logging

```python
from aa_pytools.core import configure_logging, get_logger
from pathlib import Path

# Configure custom logging
configure_logging(
    level="DEBUG",
    log_file=Path("logs/app.log"),
    console=True,
    format_string="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

logger = get_logger("my_component")
logger.debug("Detailed debugging information")
```

## 📖 Documentation

### Core Components

#### Logging System (`aa_pytools.core`)

- Auto-configuring loggers
- Flexible formatting options
- Console and file output
- Package-scoped logging hierarchy

#### Safe Execution (`aa_pytools.decorators.safe_execute`)

- Exception catching and structured error reporting
- Performance timing information
- Optional trace information for debugging
- JSON or dictionary return formats

### API Reference

Detailed API documentation is available at [https://aa-pytools.readthedocs.io](https://aa-pytools.readthedocs.io) (coming soon).

## 🧪 Development Status

This project is currently in **early development** (version 0.0.1).

**Implemented:**

- ✅ Core logging system with full configuration options
- ✅ Safe execution decorator with comprehensive error handling
- ✅ Complete test coverage for implemented features
- ✅ Modern Python packaging with uv and pyproject.toml

**In Progress:**

- 🔄 Vault integration for credential management
- 🔄 REST API client for Automation Anywhere
- 🔄 Execution management system
- 🔄 Additional specialized decorators

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information on:

- Setting up the development environment
- Running tests and linting
- Making pull requests
- Code style and standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Inspired by and built upon concepts from:

- `rpa-automationanywhere` - Last update: June 5, 2025
- `automation-anywhere` - Last update: August 8, 2023

## 📞 Support

- 📧 Email: [devaul.fs@gmail.com](mailto:devaul.fs@gmail.com)
- 🐛 Issues: [GitHub Issues](https://github.com/AND3SIL4/aa-pytools/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/AND3SIL4/aa-pytools/discussions)

---

<div align="center">

**Created by @AND3SIL4 at Net Applications**

```
ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ:
▄████▄ ███  ██ ████▄  ████▄ ▄█████ ██ ██    ██  ██
██▄▄██ ██ ▀▄██ ██  ██  ▄▄██ ▀▀▀▄▄▄ ██ ██    ▀█████
██  ██ ██   ██ ████▀  ▄▄▄█▀ █████▀ ██ ██████    ██
ɪ ᴛʜɪɴᴋ, ᴛʜᴇʀᴇꜰᴏʀᴇ ɪ ᴀᴍ 🗿
```

</div>
