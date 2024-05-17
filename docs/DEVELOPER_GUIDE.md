# Developer Guide for Todo CLI

This guide will help you understand how we set up and manage this project.

## Project Configuration

We use a `pyproject.toml` file to centralize all our project settings. This ensures consistent configuration for
everyone working on the project, all in a single file.

### Why We Like `pyproject.toml`

The `pyproject.toml` file is great for a few reasons:

- **Everything in One Place**: All the settings are in one file.
- **Follows Best Practices**: It's not another way to configure a project, but the recommended way (
  see [PEP 621](https://peps.python.org/pep-0621/)).
- **Works Well with Most Tools**: It's compatible with many tools that Python developers use, making our lives easier.

### What’s in `pyproject.toml`

In this file, we include:

- **Dependencies**: Lists both runtime and development dependencies our project relies on.
- **Build System**: Instructions on how to build our project.
- **Tool Configurations**: Settings for various tools such as `black`, `flake8`, etc.

## Project Tasks

We use a [Makefile](https://makefiletutorial.com) to describe common tasks for managing the project and assign short
aliases to them.

### What's a Makefile?

A `Makefile` lets us write down commands we run often and give them short names. This makes our work faster and less  
error-prone because we don't have to type out long commands.

### How to Use It

If you need to run a command from the `Makefile`, just do this:

1. Open your terminal.
2. Go to the root directory of the project.
3. Type `make` and the name of the task you want to do. For example, to format your code, type:

```shell  
make fmt
```
