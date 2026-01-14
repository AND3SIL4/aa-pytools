"""
bump_version.py

A script to bump the version string in pyproject.toml according to semantic versioning.

Usage:
    python scripts/bump_version.py [major|minor|patch]

- The first argument (optional) specifies the version part to bump.
- If no argument is given, 'patch' is the default.

This script reads the current version from pyproject.toml, increments the specified segment
while resetting lower segments as appropriate, writes the new version back to pyproject.toml,
and prints the new version.
"""

import sys
import tomllib
from pathlib import Path
from typing import Literal

# Define version bump types
TYPES_KIND = Literal["major", "minor", "patch"]

# Determine the kind of bump to perform
kind: TYPES_KIND = sys.argv[1] if len(sys.argv) > 1 else "patch"

# Read pyproject.toml
pyproject = Path("pyproject.toml")
data = tomllib.loads(pyproject.read_text())

# Split and parse the current version
major, minor, patch = map(int, data["project"]["version"].split("."))

# Bump the corresponding part of the version string
match kind:
    case "major":
        major += 1
        minor, patch = 0, 0  # Reset minor and patch
    case "minor":
        minor += 1
        patch = 0  # Reset patch
    case _:
        patch += 1

# Format the new version string
new_version = f"{major}.{minor}.{patch}"

# Read and replace the version assignment string
content = pyproject.read_text()
content = content.replace(
    f"version = '{data['project']['version']}'", f"version = {new_version}"
)

# Write the updated version back to pyproject.toml
pyproject.write_text(content)

# Output the result
print(f"Version bumped -> {new_version}")
