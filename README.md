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
ESNbot is a self hosted slack bot. ESNbot tries to help the members of ESN Trondheim to have an easier digital workflow by automating common tasks.
This includes creating coverphotos for events, watermarking pictures, getting contact info for members and more.

## Setup
### Prerequisites
* Slack bot token
    1. foo
    2. bar
    3. baz
* Slack app token
    1. foo
    2. bar
    3. baz
* Google account and credentials (optional, only if you want to use Google Spreadsheet integration)
    1. foo
    2. bar
    3. baz

Once the above is in order, you can proceed with the below. All code/commands are executed in  [Git Bash](https://gitforwindows.org/), but other CLIs may be used. The commands may differ somewhat.

1. Clone/pull/fork this repo from GitHub
2. Not strictly necessary, but it is heavily recommended to create a virtual environment and run the bot from there: `python -m venv env`
If you for some reason don't want to use a virtual environment, skip to step 4.
3. Activate virtual environment: `. env/Scripts/activate`
4. Install requirements (preferably into the virtual environment): `pip install -r requirements.txt`
5. (Optional) Install dev requirements into the virtual environment: `pip install -r requirements-dev.txt`
6. Copy `public.env`and name it `secret-dev.env` or `secret-prod.env` and place it into the setup folder. Make sure that it has the same structure as `public.env`. Enter your credentials from the steps in the prerequisites. If both `secret-dev.env`and `secret-prod.env`are present, `secret-dev.env` will be used. Remember to never include your credentials/tokens in a repository, especially not a public one! I.e. do not commit `secret-dev.env` or `secret-prod.env` to the repo, and do not add any secrets to `public.env`.
`secret-prod.env` should only be used for your production environment, and `secret-dev.env` is intended for your development environment.
7. Run the bot: `python esnbot.py`. If everyhting has been setup correctly you should see something like
    ```
    secret-dev/prod.env loaded...
    DD-MM-YYYY HH:MM:SS: ESNbot connected and running...
    ```
8. Stop the bot by pressing `ctrl + v` in Git Bash (or another CLI) and deactivate the virtual environment with the command `deactivate` 

Step 2 and 4 can be done in one go by using the script `setup-venv-win.sh`. In Git Bash you can run it like this: `. setup-venv-win.sh`.
The virtual environment still needs to be activated prior to running the bot.

## Requirements

* [`gspread`](https://github.com/burnash/gspread)
* [`oauth2client`](https://github.com/google/oauth2client/)
* [`pillow`](https://github.com/python-pillow/Pillow)
* [`requests`](https://github.com/requests/requests)
* [`python-dotenv`](https://github.com/slackapi/python-slackclient)
* [`python-slackclient`](https://github.com/slackapi/python-slackclient)
* [`websocket-client`](https://github.com/slackapi/python-slackclient)

You can install all of the above at once with `pip install -r requirements.txt`, preferably into a virtual environment.

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

This project the [Black](https://github.com/psf/black) code style (which is a [PEP 8](https://peps.python.org/pep-0008/) compliant opinionated formatter), with a line length of 100. We also use [isort](https://pycqa.github.io/isort/) for sorting of imports. isort is used with the black profile, a line length of 100 and skip_gitignore = "true".
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