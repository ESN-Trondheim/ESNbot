# Contributing to ESNbot

## Overview
Contributions are welcome!\
You can contribute with both code and registering issues.
Check our [issues](https://github.com/ESN-Trondheim/ESNbot/issues) for tasks that needs doing, or register an issue that you think we should consider.\
Please try to label the issue appropriately. Use the `bug` label for bugs, `enhancement` for either improving already existing features and requests for brand new features and `question` if you have a question or want more information about something.\
If you want to contribute with code, just fork this project and create a pull request with your proposed changes.\
For members of the [ESN-Trondheim organisation](https://github.com/ESN-Trondheim), please create a branch with a descriptive name, and create your pull request from that branch.

Please note that you should merge master into your branch prior to submitting your PR. Merge conflicts should also be resolved before submission.

All [checks](https://github.com/ESN-Trondheim/ESNbot/actions) MUST pass for a PR to be accepted.

This project the [Black](https://github.com/psf/black) code style (which is a [PEP 8](https://peps.python.org/pep-0008/) compliant opinionated formatter), with a line length of 100.\
We also use [isort](https://pycqa.github.io/isort/) for sorting of imports. isort is used with the black profile, a line length of 100 and skip_gitignore = "true".
Note that this requires git to be installed on your system. If you don't have git installed (you should!), then you should specify exactly which files to run isort on, instead of using `.` to run on all files in the directory.
These settings are configured in `pyproject.toml` and should be picked up if you run both tools from the root directory of this project.

We recommend that you install `requirements-dev.txt` into your virtual environment and run black and isort from your venv.

black:\
Preview of changes: `black {source_file_or_directory} --check (--diff --color --verbose)`\
Perform changes: `black {source_file_or_directory} (--diff --color --verbose)`

isort:\
Preview of changes: `isort {source_file_or_directory} --check (--diff --color (--verbose))`\
Perform changes: `isort {source_file_or_directory} (--diff --color (--verbose))`

Note that for both black and isort you may use `black/isort . (flags)` to apply to the entire directory, but keep in mind that git should be installed if you wish to do that when using isort.

## Running tests
Test coverage is lackluster at the moment, but is under active improvement.
Navigate/cd to the root directory of the project.\
Verbose mode (-v) is optional.
Run all tests with either unittest or pytest.\
unittest: `python -m unittest discover (-v)`\
pytest: `pytest (-v)`

All tests MUST pass for a PR to be accepted!
