# Usage Guide for Todo CLI

Manage your daily tasks directly from the terminal.

**Usage**:

```console
$ todo [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add`: Create a new task.
* `complete`: Mark a task as completed.
* `delete`: Delete a task.
* `list`: List tasks.
* `spaces`: Manage spaces.
* `uncomplete`: Mark a task as uncompleted.

## `todo add`

Create a new task.

**Usage**:

```console
$ todo add [OPTIONS] TITLE
```

**Arguments**:

* `TITLE`: Title of the task.  [required]

**Options**:

* `-d, --date [YYYY-MM-DD|MM-DD|DD]`: Specify a target date for the task.
* `-a, --assertions`: Prompt for assertions.
* `--help`: Show this message and exit.

## `todo complete`

Mark a task as completed.

**Usage**:

```console
$ todo complete [OPTIONS] TASK_ID
```

**Arguments**:

* `TASK_ID`: ID of the task to complete.  [required]

**Options**:

* `--help`: Show this message and exit.

## `todo delete`

Delete a task.

**Usage**:

```console
$ todo delete [OPTIONS] TASK_ID
```

**Arguments**:

* `TASK_ID`: ID of the task to delete.  [required]

**Options**:

* `--help`: Show this message and exit.

## `todo list`

List tasks.

**Usage**:

```console
$ todo list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `todo spaces`

Manage spaces.

**Usage**:

```console
$ todo spaces [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Create a new space.
* `delete`: Delete a space.
* `disable`: Disable a space.

### `todo spaces add`

Create a new space.

**Usage**:

```console
$ todo spaces add [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Unique name of the space.  [required]

**Options**:

* `-d, --description TEXT`: Specify a description for the space.
* `--help`: Show this message and exit.

### `todo spaces delete`

Delete a space.

**Usage**:

```console
$ todo spaces delete [OPTIONS] SPACE_ID
```

**Arguments**:

* `SPACE_ID`: ID of the space to delete.  [required]

**Options**:

* `--help`: Show this message and exit.

### `todo spaces disable`

Disable a space.

**Usage**:

```console
$ todo spaces disable [OPTIONS] SPACE_ID
```

**Arguments**:

* `SPACE_ID`: ID of the space to disable.  [required]

**Options**:

* `--help`: Show this message and exit.

## `todo uncomplete`

Mark a task as uncompleted.

**Usage**:

```console
$ todo uncomplete [OPTIONS] TASK_ID
```

**Arguments**:

* `TASK_ID`: ID of the task to uncomplete.  [required]

**Options**:

* `--help`: Show this message and exit.
