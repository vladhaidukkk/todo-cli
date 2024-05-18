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

> **NOTE**: `just`, unlike `make`, allows you to execute tasks from any directory within the project.

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
