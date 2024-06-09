# Todo CLI

Welcome to the Todo Command Line Interface! This tool helps you manage your daily tasks directly from your
terminal.

## Quick Start

To get the tool up and running quickly, it's important to note that it is hosted on [TestPyPI](https://test.pypi.org/),
not on the standard [PyPI](https://pypi.org/). This affects how you install the tool.

Install using `pip`:

```shell
pip install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple todo-cli-vh
```

If you prefer to use `pipx`, the installation command slightly differs:

```shell
pipx install -i https://test.pypi.org/simple todo-cli-vh --pip-args "--extra-index-url https://pypi.org/simple"
```

These commands ensure that the latest version of `todo-cli-vh` is installed from TestPyPI, while dependencies are
searched for in the main PyPI repository.

Once the installation is complete, use the `todo` command in your terminal to start managing your tasks efficiently.

## Guides

- [Usage Guide](./docs/USAGE_GUIDE.md): Learn how to use the Todo CLI to manage your tasks efficiently.
- [Developer Guide](./docs/DEVELOPER_GUIDE.md): In-depth documentation for developers who want to understand or
  contribute to the codebase.
