# Variables configuration
PYTHON := python
PIP := pip
PACKAGE := 
DIST_DIR := dist

# Targets for automate tasks
.PHONY: install test

# Validate if the localization if empty
# If the variable is empty, that means there is no uv installed
UV := $(shell command -v uv 2>/dev/null)

install:
ifndef UV
	$(error uv is not installed, please install the tool and try again)
endif

	@command uv sync
	@echo "All dependencies and libraries installed successfully"

test:
	@command pytest ./test -vv
	@echo "All tests made successfully"

clean:
	rm -rf $(DIST_DIR)
	rm -rf *egg-info
	rm -rf build
	rm -rf __pycache__

build: clean
	%(PYTHON) -m build

help:
	@echo "Available commands:"
	@echo "  make install        Install dependencies"
	@echo "  make test           Execute tests specified"
	@echo "  make build          Build the package to publish (.tz and whl)"
	@echo "  make clean          Clean up the generated files"

