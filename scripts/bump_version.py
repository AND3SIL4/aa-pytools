import sys
import tomllib
from pathlib import Path
from typing import Literal

TYPES_KIND = Literal["major", "minor", "patch"]
kind: TYPES_KIND = sys.argv[1] if len(sys.argv) > 1 else "patch"

pyproject = Path("pyproject.toml")
data = tomllib.loads(pyproject.read_text())

major, minor, patch = map[int](int, data["project"]["version"].split("."))

match kind:
    case "major":
        major += 1
        minor, patch = 0
    case "minor":
        minor += 1
        patch = 0
    case _:
        patch += 1

new_version = f"{major}.{minor}.{patch}"
content = pyproject.read_text()
content = content.replace(
    f"version = '{data['project']['version']}'", f"version = {new_version}"
)

pyproject.write_text(content)
print(f"Version bumped -> {new_version}")
