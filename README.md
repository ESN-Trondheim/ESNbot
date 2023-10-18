# ESNbot
<div align="center">
[![License](https://img.shields.io/github/license/ESN-Trondheim/ESNbot)](https://github.com/ESN-Trondheim/ESNbot/blob/master/LICENSE)
[![Issues](https://img.shields.io/github/issues/ESN-Trondheim/ESNbot)](https://github.com/ESN-Trondheim/ESNbot/issues)
[![Contributors](https://img.shields.io/github/contributors/ESN-Trondheim/ESNbot)](https://github.com/ESN-Trondheim/ESNbot/graphs/contributors)\
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

<!--- This needs to be written when we have some tests
## Running tests
--->

<!---
## Contributing
--->

## License
[MIT](https://choosealicense.com/licenses/mit/)