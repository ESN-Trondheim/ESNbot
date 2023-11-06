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
* Slack tokens
    1. This project is still using [`rtm.connect`](https://api.slack.com/methods/rtm.connect), which means you have to create a [classic Slack App](https://api.slack.com/apps?new_classic_app=1). Note that this will change in the future.
    2. Give the app a name and choose a workspace
    3. Press bots, and add a legacy bot user. Choose a display name for your bot and a default username
    3. Go to OAuth & Permissions. You should already have the `bot` scope, but you will need to add the `files:write:user` scope as well.
    4. Install the bot to your workspace. OAuth tokens will then be generated.
    5. Tokens to be saved in in `secret-dev.env` and/or `secret-prod.env`:
        1. `User OAuth Token`: this is your `APP_TOKEN`
        2.  `Bot User OAuth Token`: this is your `SLACK_BOT_TOKEN`
    6. Save the bot name you chose earlier in `BOT_NAME` in your `.env` file(s). This should be the default name, not the display name.
    7. Run the script `print_bot_id.py` to get your bot id.
    8. Update `BOT_ID` in `.env` file(s) with the id you got from the last step.
    9. Add the bot to your desired Slack channel(s)
* Google account and credentials (optional, only if you want to use [`gspread`](https://github.com/burnash/gspread) (Google Spreadsheet integration))
    1. Follow the steps outlined in [gspread's documentation](https://docs.gspread.org/en/latest/oauth2.html)


### Project setup
Once the prerequisites are in order, you can proceed with the rest of the project setup. All code/commands are executed in  [Git Bash](https://gitforwindows.org/), but other CLIs may be used. The commands may differ somewhat.

1. Clone/pull/fork this repo from GitHub
2. Not strictly necessary, but it is heavily recommended to create a virtual environment and run the bot from there: `python -m venv env`
If you for some reason don't want to use a virtual environment, skip to step 4.
3. Activate virtual environment: `. env/Scripts/activate`
4. Install requirements or dev requiremnents (preferably into the virtual environment): `pip install -r requirements.txt` or `pip install -r requirements-dev.txt`.
Note that dev requirements are optional, and also install regular requirements, meaning that you don't have try to install both.
5. Copy `public.env`and name it `secret-dev.env` or `secret-prod.env` and place it into the setup folder. Make sure that it has the same structure as `public.env`. Enter your credentials from the steps in the prerequisites. If both `secret-dev.env`and `secret-prod.env`are present, `secret-dev.env` will be used. Remember to never include your credentials/tokens in a repository, especially not a public one! I.e. do not commit `secret-dev.env` or `secret-prod.env` to the repo, and do not add any secrets to `public.env`.
`secret-prod.env` should only be used for your production environment, and `secret-dev.env` is intended for your development environment.
6. Run the bot: `python esnbot.py`. If everyhting has been setup correctly you should see something like
    ```
    secret-dev/prod.env loaded...
    DD-MM-YYYY HH:MM:SS: ESNbot connected and running...
    ```
7. Stop the bot by pressing `ctrl + c` in Git Bash (or another CLI) and deactivate the virtual environment with the command `deactivate` 

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

You can install all of the above at once with `pip install -r requirements.txt` (or `pip install -r requirements-dev.txt`), preferably into a virtual environment.


## Usage
The bot will not do anything before it is tagged in a channel.\
For a list of all available commands type `@[botname] list`
* `list`: lists all (visible) commands
* `reimbursemnt`: returns link to reimbursement form and guidelines
* `esnfarger`: returns name of all official ESN colors and their hex values
* `esnfont`: returns name of the official ESN fonts
* `standliste`: returns link to the standliste document
* `help`: returns help for all the commands. You can use `@[botname] help [command]` to get info about how to use `[command]`
* `ølstraff`: returns link to document with standings. If a name is provided, the standing for that person is returned. This is the same command as `vinstraff` under the hood.
* `vinstraff`: returns link to document with standings. If a name is provided, the standing for that person is returned. This is the same command as `ølstraff` under the hood.
* `kontaktinfo`: returns link to document with contact info. If a name is provided, contact info for that person is returned.
* `watermark`: watermarks pictures with ESN logo.
* `coverphoto`: Creates a coverphoto for Facebook or activities.esn.org that is ready to be used.


## Adding your own commands
To add your own command, use the `core_commands.register_commnand` decorator. This will register the command with the bot, along with the help text for your command. 
A simple example:
```
@register_command(
    keyword="mycommand", help_text="My example command", visible=True
)
def my_custom_command(client, channel, user, argument, output):
    client.respond_to(channel, user, "Hello, this is my_custom_command")
```
* `@<bot_name> mycommand`: The bot will respond with `Hello, this is my_custom_command`.
* `@<bot_name> list`: The keyword (`mycommand`) will be a part of the response. If visible=False, the command will NOT be a part of the list.
* `@<bot_name> help mycommand`: The bot will respond with `My example command`.


## Contributing
Contributions are welcome!\
You can contribute with both code and registering issues.

Please see our [contrubuting guidelines](CONTRIBUTING.md) for information about how to contribute to this project.


## License
[MIT](https://choosealicense.com/licenses/mit/)