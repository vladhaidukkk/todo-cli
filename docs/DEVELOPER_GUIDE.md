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

## Project Commands

We use a [Makefile](https://makefiletutorial.com) to help us quickly do common tasks without
having to remember complex commands.

### What is a Makefile?

A `Makefile` defines a series of commands and provides aliases (or simple names) for them. By using these aliases with
the `make` command, we can quickly and effectively perform routine project tasks without remembering and typing out long
series of commands.

### How to Use It

To run a command from the `Makefile`, open your terminal, go to the project's main folder, and type `make` followed by
the command name. Here's an example:

```shell
make fmt
```
