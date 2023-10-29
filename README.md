# ESNbot
<div align="center">

[![Build](https://github.com/ESN-Trondheim/ESNbot/actions/workflows/build.yml/badge.svg)](https://github.com/ESN-Trondheim/ESNbot/actions/workflows/build.yml)
[![Tests](https://github.com/ESN-Trondheim/ESNbot/actions/workflows/test.yml/badge.svg)](https://github.com/ESN-Trondheim/ESNbot/actions/workflows/test.yml)
[![Formatting](https://github.com/ESN-Trondheim/ESNbot/actions/workflows/formatting.yml/badge.svg)](https://github.com/ESN-Trondheim/ESNbot/actions/workflows/formatting.yml)
[![License](https://img.shields.io/github/license/ESN-Trondheim/ESNbot)](https://github.com/ESN-Trondheim/ESNbot/blob/master/LICENSE)
[![Issues](https://img.shields.io/github/issues/ESN-Trondheim/ESNbot)](https://github.com/ESN-Trondheim/ESNbot/issues)
[![Contributors](https://img.shields.io/github/contributors/ESN-Trondheim/ESNbot)](https://github.com/ESN-Trondheim/ESNbot/graphs/contributors)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\
A Slack bot for ESN Trondheim.\
Original author: [Lai Alexander Holmsen](https://github.com/LaiAlexander)

</div>

## Overview
ESNbot is a self hosted slack bot.\
TODO

## Setup
TODO

## Requirements

[`python-slackclient`](https://github.com/slackapi/python-slackclient)\
Install with PyPI: `pip install slackclient`

[`gspread`](https://github.com/burnash/gspread)\
Install with PyPI: `pip install gspread`

[`oauth2client`](https://github.com/google/oauth2client/)\
Install with PyPI: `pip install --upgrade oauth2client`

[`requests`](https://github.com/requests/requests)\
Install with PyPI: `pip install requests`

[`pillow`](https://github.com/python-pillow/Pillow)\
Install with PyPI: `pip install pillow`

You can install all of the at once with `pip install -r requirements.txt`

## Usage
The bot will not do anything before it is tagged in a channel.\
For a list of all available commands type `@ESNbot list`
* Lorem ipsum
* dolor sit amet

## Contributing
Contributions are welcome!\
You can contribute with both code and registering issues.
Check our [issues](https://github.com/ESN-Trondheim/ESNbot/issues) for tasks that needs doing, or register an issue that you think we should consider.\
If you want to contribute with code, just fork this project and create a pull request with your proposed changes.\
For members of the [ESN-Trondheim organisation](https://github.com/ESN-Trondheim), please create a branch with a descriptive name, and create your pull request from that branch.

All [checks](https://github.com/ESN-Trondheim/ESNbot/actions) MUST pass for a PR to be accepted.

This project the [black](https://github.com/psf/black) code style, with a line length of 100. We also use [isort](https://pycqa.github.io/isort/) for sorting of imports. isort is used with the black profile, a line length of 100 and skip_gitignore = "true".
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

## License
[MIT](https://choosealicense.com/licenses/mit/)