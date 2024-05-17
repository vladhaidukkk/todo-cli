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

We use [just](https://just.systems/man/en/) with its `Justfile` to describe and execute common project tasks. It's a
modern alternative to `make` and its [Makefile](https://makefiletutorial.com), offering a range of useful features,
such as the ability to pass arguments to tasks.

### What's a `Justfile`

A `Justfile` is a special file for the `just` utility that allows us to write down frequently used commands and assign
them short names. This makes our work faster and less error-prone, as we no longer need to type out long commands.

### How to Use `just`

If you need to run a task from the `Justfile`, just do this:

1. Open your terminal.
2. Type `just` and the name of the task you want to execute. For example, to format your code, type:

```shell
just fmt
```

> **NOTE:** `just`, unlike `make`, allows you to execute tasks from any directory within the project.
