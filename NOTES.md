# In order to get this project done, I had to learn and rediscover some key concepts

1. What is the difference between a Python library, package, and module?

- **Library:**
  A collection of code designed to solve a particular problem or perform a specific set of activities. A library is typically composed of one or more packages.
- **Package:**
  A namespace that organizes one or more related modules to solve a specific problem. A package is essentially a directory containing an `__init__.py` file and one or more module files.
- **Module:**
  A single file that contains reusable Python code, such as functions or classes, which can be imported and used in other programs. May have multiple functions.

2. What is the anathomy of Python packages and `pyproject.toml`

```txt
project
|__ pyproject.toml
    |__ package1
        |__ __init__.py
        |__ module.py
```

## Packages needed to understand

- `setuptools`: make the dist files
- `wheel`: make the dist files
- `build`: build the ditribute binary files
- `twine`: publish to Pypi global repository

I had to replace the contruction of the library using `setup.py` file to `pyproject.toml` and learn how to use the `__init__.py` file to index the imports of the packages.

Use the test environment in Pypi to publish my first package _(if I make a mistake there is no problem in this environment)_

> ️ Some tips before publish the package
>
> 1.  Make sure your package code is clean and maintainable.
> 2.  Extend the documentation in order to make the package easier to use.
> 3.  Choose an appropiate software licence before publish the package.
> 4.  Make managing package updates easy.
