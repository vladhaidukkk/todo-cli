# Developer Guide for Todo CLI

This guide will help you understand how we set up and manage this project.

## Table of Contents

- [Project Configuration](#project-configuration)
    - [Why We Like pyproject.toml](#why-we-like-pyprojecttoml)
    - [What’s in pyproject.toml](#whats-in-pyprojecttoml)
- [Project Tasks](#project-tasks)
    - [What's a Justfile](#whats-a-justfile)
    - [How to Use just](#how-to-use-just)
- [CLI Management](#cli-management)
    - [Local Installation](#local-installation)
    - [Usage as a Package](#usage-as-a-package)
    - [Update Usage Guide](#update-usage-guide)
    - [Increase Version](#increase-version)
    - [Building](#building)
    - [Test Wheel Distribution](#test-wheel-distribution)
    - [Publishing](#publishing)
- [Dependencies Management](#dependencies-management)
    - [Dependency Types](#dependency-types)
    - [Management Workflow](#management-workflow)
        - [Install Dependencies](#install-dependencies)
        - [Add Dependencies](#add-dependencies)
        - [Update Dependencies](#update-dependencies)
        - [Remove Dependencies](#remove-dependencies)
        - [Other Commands](#other-commands)
- [Code Style](#code-style)
    - [Formatting](#formatting)
    - [Linting](#linting)
    - [Exclusions](#exclusions)

## Project Configuration

We use a `pyproject.toml` file to centralize all our project settings. This ensures consistent configuration for
everyone working on the project, all in a single file.

### Why We Like pyproject.toml

The `pyproject.toml` file is great for a few reasons:

- **Everything in One Place**: All the settings are in one file.
- **Follows Best Practices**: It's not another way to configure a project, but the recommended way (
  see [PEP621](https://peps.python.org/pep-0621/)).
- **Works Well with Most Tools**: It's compatible with many tools that Python developers use, making our lives easier.

### What’s in pyproject.toml

In this file, we include:

- **Dependencies**: Lists both runtime and development dependencies our project relies on.
- **Build System**: Instructions on how to build our project.
- **Tool Configurations**: Settings for various tools such as `black`, `flake8`, etc.

## Project Tasks

We use [just](https://just.systems/man/en/) with its `Justfile` to describe and execute common project tasks. It's a
modern alternative to `make` and its [Makefile](https://makefiletutorial.com), offering a range of useful features,
such as the ability to pass arguments to tasks.

### What's a Justfile

A `Justfile` is a special file for the `just` utility that allows us to write down frequently used commands and assign
them short names. This makes our work faster and less error-prone, as we no longer need to type out long commands.

### How to Use just

If you need to run a task from the `Justfile`, just do this:

1. Open your terminal.
2. Type `just` and the name of the task you want to execute. For example, to format your code, type:

```shell
just fmt
```

> **NOTE**: `just`, unlike `make`, allows you to execute tasks from any directory within the project.

## CLI Management

This section provides straightforward guidance on developing and deploying our CLI. Here, we explain how to work with it
locally, build it, and publish it.

### Local Installation

To install the CLI locally, follow the standard package installation procedure but point to the current package
directory. The command has been extracted into the `Justfile`, so you can simply run the following command:

```shell
just init
```

Using this approach requires you to reinstall the package on every change. To simplify your workflow, we recommend
installing the CLI in editable mode with the following command:

```shell
just init-dev
```

Editable mode allows you to see your code changes reflected immediately without needing to reinstall.

### Usage as a Package

The CLI can also function as a standalone package, thanks to the `__main__.py` file located in the root of the code
directory. This setup allows you to work with it locally without needing to install it. The only drawback is the lack of
support for shell completion, but it's still ideal for quick testing:

```shell
python -m todo
```

Real users can also use it as a package, but again, they lose the ability to have shell completion in this case.

### Update Usage Guide

After making changes to the CLI commands interface, it is crucial to update the [Usage Guide](./USAGE_GUIDE.md) to
reflect these modifications before deployment. To do this automatically, execute the following command:

```shell
just gen-doc
```

After this, you shouldn't worry that you've missed something, as this command is based on a special feature provided for
us by [Typer](https://typer.tiangolo.com/).

### Increase Version

Before building and publishing the CLI, it's also important to increment its version. This update should be made in
the `pyproject.toml` file. Ensure that the version change adheres to [Semantic Versioning](https://semver.org/)
principles, which help maintain compatibility and predictability in version updates.

### Building

We use [Setuptools](https://setuptools.pypa.io/en/latest/) as our build system, as it meets all our project
requirements. To simplify the build process, we've extracted the command for it into the `Justfile`, which is based on
the [build](https://build.pypa.io/en/stable/) package:

```bash
just build
```

This command generates both a source archive and a wheel distribution, ensuring a versatile deployment across different
environments.

### Test Wheel Distribution

To verify that the wheel package is installable, you can install it locally using the following command:

```shell
pip install path_to_wheel.whl
```

Do this on your system before deployment or further distribution.

### Publishing

Once you have updated the [Usage Guide](./USAGE_GUIDE.md), incremented the CLI version, and built the package, you are
ready to release a new version. Currently, we publish exclusively to [TestPyPI](https://test.pypi.org/). Release the new
version by executing the following command:

```shell
just publish-test
```

This command will upload the latest version of the CLI to TestPyPI. It's ideal for pre-release testing and validation,
but we currently use it as the main environment for our CLI.

## Dependencies Management

We highly recommend using [uv](https://github.com/astral-sh/uv) for dependencies management, as it is an extremely fast
Rust-based alternative to `pip` and `pip-tools`. However, if you are not ready to use `uv`, you can continue
using `pip` and `pip-tools`. Just be aware that the `Justfile` commands are specific to `uv`.

### Dependency Types

In our projects, we list all our dependencies in the `pyproject.toml` file. There are two types of dependencies:

- **Runtime Dependencies**: Packages directly used in the project's runtime.
- **Development Dependencies**: Packages needed only during development, such as formatting or testing tools.

### Management Workflow

This section provides a systematic approach to managing dependencies in our project. The management workflow is designed
to achieve two main goals:

- **Keep Everything Compatible**: We make sure that all the dependencies of our project work well together so that
  nothing breaks.
- **Avoid Problems with Updates**: We update dependencies carefully to prevent crashes or other problems when new
  versions come out.

By following these steps, we help our project stay stable and efficient.

#### Install Dependencies

To install all the runtime dependencies, use the `sync` command:

```shell
just sync
```

For including dev dependencies as well, use the `sync-dev` command:

```shell
just sync-dev
```

Both commands will remove any unnecessary dependencies from your virtual environment and install the required ones,
keeping your setup clean and efficient.

#### Add Dependencies

To add a new dependency to the project, follow these steps:

1. **Find a Compatible Version**

   First, use the `try` command to find a version of the dependency that works with our current setup:

   ```shell
   just try <package-name>
   ```

2. **Save the Dependency**

   Next, add the dependency with its compatible version to `pyproject.toml`. Remember to use version constraints to
   allow updates that won't introduce breaking changes:

   ```toml
   [project]
   dependencies = ["package-name>=1.2.3,<2.0.0"]
   ```

   > **NOTE**: For less stable versions, such as pre-releases, define a stricter range (
   e.g., `package-name>=0.1.2,<0.2.0`).

3. **Lock the Version**

   Finally, lock its version to make sure it won't be accidentally updated in the future by using the `lock` command:

   ```shell
   just lock
   ```

At the end, you should have added a new dependency without having any compatibility issues or surprises with future
updates.

#### Update Dependencies

To update the locked dependencies to their highest possible versions according to the constraints in
the `pyproject.toml`, use the following command:

```shell
just lock-up
```

To upgrade dependency beyond current constraints, follow these steps:

1. **Uninstall the Old Version**

   Start by removing the existing version from the environment, to be able to run `try`:

   ```shell
   just rm <package-name>
   ```

2. **Search for a New Compatible Version**

   Use the `try` command to find a version of the dependency that works with our current setup:

   ```shell
   just try <package-name>
   ```

3. **Revise the Constraints**

   Update version constraints of the dependency in the `pyproject.toml`.

4. **Refresh the Lock**

   Finalize the upgrade process by refreshing the lock file:

   ```shell
   just lock-up
   ```

#### Remove Dependencies

To remove a dependency, simply delete its entry from the `pyproject.toml` file and refresh the lock file with the
following command:

```shell
just lock
```

#### Other Commands

To view a list of all installed dependencies, execute the following command:

```shell
just list
```

For detailed information on a specific dependency, use:

```shell
just info <package-name>
```

To check health of the project's dependencies, run:

```shell
just health
```

## Code Style

Our project uses a series of tools to format and lint our code, ensuring it follows best practices and remains clean
and readable. Below is a detailed guide on the formatting & linting standards we follow and the tools we use.

### Formatting

According to [PEP8](https://peps.python.org/pep-0008/), Python code has specific style guidelines which, while not
mandatory, are strongly recommended to maintain readability and consistency. Following these guidelines helps anyone who
reads the code to easily understand it.

We utilize a set of automated tools to handle code formatting so that developers can focus more on coding rather than
style nuances. These tools include:

- **[Black](https://github.com/psf/black)**: Automatically formats Python code to align with PEP8 guidelines.
- **[isort](https://pycqa.github.io/isort/)**: Neatly sorts and organizes our imports to keep them clean and readable.
- **[docformatter](https://github.com/PyCQA/docformatter)**: Standardizes the format of docstrings throughout our
  codebase.

These tools are configured in the `pyproject.toml` file, making them compatible with each other.

To format the whole codebase, simply run:

```shell
just fmt
```

### Linting

Linting is the process of running a program that checks for code errors, style issues, and potential bugs. Using linting
tools ensures that the code not only looks good but is also free from common coding errors that could lead to bugs.

To maintain high code quality, we use the following linting tools:

- **[Pyright](https://github.com/microsoft/pyright)**: A fast and precise static type checker for Python, helping to
  catch type errors before runtime.
- **[Flake8](https://flake8.pycqa.org/en/latest/)**: Checks code for best practices and styling errors.
- **[autoflake](https://github.com/PyCQA/autoflake)**: Removes unused imports and variables to declutter the code.
- **[Bandit](https://bandit.readthedocs.io/en/latest/)**: Searches for common security issues in Python code,
  prioritizing the safety of our codebase.

All linting configurations are included in our project’s `pyproject.toml` file, making them compatible with each other
as well as with formatting tools.

To lint your codebase, just run the following command:

```shell
just lint
```

### Exclusions

In cases where you're confident your code should appear as you've written it, but certain tools are reporting violations
of their rules, you can ignore them for specific code lines or exclude entire files/directories.

These tools typically provide special comments to ignore specific code lines, as well as configuration options to
exclude files and directories. For example, `isort` offers a range of
useful [action comments](https://pycqa.github.io/isort/docs/configuration/action_comments.html) for special cases.

However, you should avoid relying on ignoring or excluding. Use these options only in exceptional circumstances.

> **TIP**: To see which files a tool checks, run it in verbose mode.
