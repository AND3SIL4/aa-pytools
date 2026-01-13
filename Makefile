# Variables configuration
PYTHON := python
PACKAGE := aa-pytools
DIST_DIR := dist

# Targets for automate tasks
.PHONY: install test clean build publish-test test-download help publish

install:
	@command -v uv >/dev/null 2>&1 || \
		(echo "uv is not installed, please install the tool and try again." && exit 1)
	uv sync
	@echo "All dependencies and libraries installed successfully"

test:
	pytest -vv
	@echo "All tests made successfully"

clean:
	rm -rf $(DIST_DIR)
	rm -rf *.egg-info
	rm -rf build
	rm -rf __pycache__

build: clean
	$(PYTHON) -m build

publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

test-download:
	python -m pip install --index-url https://test.pypi.org/simple/ $(PACKAGE)

help:
	@echo "Available commands:"
	@echo "  make install        Install dependencies"
	@echo "  make test           Execute tests specified"
	@echo "  make build          Build the package to publish (.tar.gz and whl)"
	@echo "  make clean          Clean up the generated files"
	@echo "  make publish-test   Upload to TestPyPI"
	@echo "  make publish        Upload to PyPI"

