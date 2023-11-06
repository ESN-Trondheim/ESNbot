import os
import pathlib
from sys import exit as sysexit

import dotenv
from slackclient import SlackClient

if __name__ == "__main__":
    if os.path.isfile(pathlib.Path.cwd().joinpath("setup", "secret-dev.env")):
        dotenv.load_dotenv(dotenv_path=pathlib.Path.cwd().joinpath("setup", "secret-dev.env"))
        print("secret-dev.env loaded...")
    elif os.path.isfile(pathlib.Path.cwd().joinpath("setup", "secret-prod.env")):
        dotenv.load_dotenv(dotenv_path=pathlib.Path.cwd().joinpath("setup", "secret-prod.env"))
        print("secret-prod.env loaded...")
    else:
        print("Environment variables not found...")
        print("Script could not be run.")
        sysexit()

    bot_name = os.environ.get("BOT_NAME")
    slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
    api_call = slack_client.api_call("users.list")
    if api_call.get("ok"):
        users = api_call.get("members")
        for user in users:
            # print(user["name"], user.get("id"))
            if "name" in user and user.get("name") == bot_name:
                print("Bot ID for '" + user["name"] + "' is " + user.get("id"))
    else:
        print("Could not find bot user with the name " + bot_name)
