# Usage Guide for Todo CLI

Manage your daily tasks directly from the terminal.

**Usage**:

```console
$ todo [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add`: Create a new task.
* `complete`: Mark a task as completed.
* `delete`: Delete a task.
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
