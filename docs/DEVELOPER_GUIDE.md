# Developer Guide for Todo CLI

## Project Configuration

We use the `pyproject.toml` file to manage all configurations in our project whenever possible. This file
centralizes and standardizes the management of project settings, streamlining the configuration process.

### Why Use `pyproject.toml`?

Using `pyproject.toml` for our configurations has several advantages:

- **Centralization**: It keeps all configuration settings in just one file.
- **Standardization**: This method is recommended by [PEP 621](https://peps.python.org/pep-0621/) and is becoming the
  norm in the Python community.
- **Compatibility**: Many Python tools can already use this file, which makes things simpler.

### What We Configure in `pyproject.toml`

Our `pyproject.toml` includes settings for:

- **Dependencies Management**: Defines both runtime and development dependencies.
- **Build System**: Specifies instructions on how to build our project.
- **Tool Configurations**: Settings for various tools such as `black`, `flake8`, and others to ensure
  consistency.
