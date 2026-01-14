# Variables configuration
PYTHON := python
PACKAGE := aa-pytools
DIST_DIR := dist

TYPE ?= patch # Request a type of new release
# Usage like this `make build TYPE=minor`

# Targets for automate tasks
.PHONY: install test clean build publish-test test-download help publish bump
.DEFAULT_GOAL := help

install:
	@command -v uv >/dev/null 2>&1 || \
		(echo "uv is not installed, please install the tool and try again." && exit 1)
	uv sync
	@echo "All dependencies and libraries installed successfully"

test:
	pytest -vv
	@echo "All tests made successfully"

bump:
	$(PYTHON) scripts/bump_version.py $(TYPE)
	@grep '^version' pyproject.toml

clean:
	rm -rf $(DIST_DIR)
	rm -rf *.egg-info
	rm -rf build
	rm -rf __pycache__

build: clean bump
	$(PYTHON) -m build

publish-test: build
	$(PYTHON) -m twine check dist/*
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish: build
	$(PYTHON) -m twine upload dist/*

test-download:
	$(PYTHON) -m pip install --index-url https://test.pypi.org/simple/ $(PACKAGE)

help:
	@printf "Available commands:\n"
	@printf "  make install        Install dependencies\n"
	@printf "  make test           Execute tests specified\n"
	@printf "  make build          Build the package to publish (.tar.gz and whl)\n"
	@printf "  make clean          Clean up the generated files\n"
	@printf "  make publish-test   Upload to TestPyPI\n"
	@printf "  make publish        Upload to PyPI\n"
	@printf "\n"
	@printf "Order to use the make flow:\n"
	@printf "  make clean\n"
	@printf "  make build\n"
	@printf "  make bump TYPE=major|minor|patch\n"
	@printf "  make publish-test\n"
	@printf "  make test-download\n"
	@printf "  make publish\n"
