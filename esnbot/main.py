"""
    A slack bot to help ESN Trondheim
"""

import os
import time
import logging
from logging.handlers import RotatingFileHandler
import traceback
import sys
import pathlib
import dotenv
import requests
from slackclient import SlackClient

import constants
from utils import log_to_console, log_to_file_and_console, mention_user, mention_bot


class BotClient:
    def __init__(self):
        self.slack_client = SlackClient(
            os.environ.get("SLACK_BOT_TOKEN")
        )  # pylint: disable=invalid-name

    def run(self):
        """
        Main function
        """
        if self.slack_client.rtm_connect(auto_reconnect=True, with_team_state=False):
            log_to_file_and_console(
                "log" + os.sep + "connected.log", "ESNbot connected and running...", "w"
            )
            while True:
                try:
                    text, channel, user, output = self.parse_slack_output(
                        self.slack_client.rtm_read(), LOGGERS
                    )
                except TimeoutError:
                    LOGGERS["reconnect"].info("Session timed out [TimeoutError].")
                    log_to_console("Session timed out [TimeoutError].")
                    LOGGERS["reconnect"].info("Initiating new session...")
                    log_to_console("Initiating new session...")
                    if self.slack_client.rtm_connect(auto_reconnect=True, with_team_state=False):
                        LOGGERS["reconnect"].info("ESNbot reconnected and running...")
                        log_to_console("ESNbot reconnected and running...")
                    else:
                        LOGGERS["reconnect"].error("Reconnection failed.")
                        log_to_console("Reconnection failed.")
                except Exception as exc:
                    LOGGERS["stacktrace"].error(str(exc))
                    LOGGERS["stacktrace"].error(traceback.format_exc())
                    # traceback.print_exc() # Probably don't need to print it twice.
                    # Unsure how it looks if it's exception inside exception.
                    return
                if channel:
                    self.handle_command(text, channel, user, output)
                time.sleep(constants.READ_WEBSOCKET_DELAY)
        else:
            log_to_console("Connection failed.")

    def parse_slack_output(self, slack_rtm_output, LOGGERS):
        """
        Parses messages written in channels that the bot is a part of.

        :Args:
        `slack_rtm_output` is the events that are fired in the channel

        :Returns:
        `text`, `channel`, `user`, `output` where text is the message after the bot is mentioned,
        channel is the id of the channel, user is the id of the user,
        output is the entire output that the bot sees in the channel.
        If this information is not present, None, None, None is returned.
        """
        output_list = slack_rtm_output
        if output_list:
            for output in output_list:
                LOGGERS["output"].debug(str(output))
                if output["type"] not in constants.IGNORED_MESSAGE_TYPES:
                    # maybe make this filter out ephemeral messages as well, like google drive messages
                    log_to_console(str(output) + "\n")
                if output["type"] == "goodbye":
                    LOGGERS["output"].info("Session ended. ('goodbye' event)")
                    log_to_console("Session ended. ('goodbye' event)")
                    LOGGERS["output"].info("Initiating new session... ('goodbye' event)")
                    log_to_console("Initiating new session... ('goodbye' event)")
                    if self.slack_client.rtm_connect(auto_reconnect=True):
                        LOGGERS["output"].info(
                            "ESNbot reconnected and running... ('goodbye' event)"
                        )
                        log_to_console("ESNbot reconnected and running... ('goodbye' event)")
                    else:
                        LOGGERS["output"].error("Reconnection failed.")
                        log_to_console("Reconnection failed. ('goodbye' event)")
                if output and "text" in output and mention_bot() in output["text"]:
                    text = output["text"].split(mention_bot())[1].strip()
                    if output.get("subtype") == "file_comment":
                        return (text, output["channel"], output["file"]["user"], output)
                    # futureproofing if the bot will ever respond to file comments as a file comment.
                    # or output.get('file').get('user') == BOT_ID
                    # this does not work if 'file' does not exist. 'file' is then None,
                    # and you can't call get() on a NoneType object
                    if output.get("user") == mention_bot():
                        return None, None, None, None  # Don't care about the bot's own messages
                    return (text, output["channel"], output["user"], output)
        return None, None, None, None

    def handle_command(self, text, channel, user, output):
        """
        Handles a command directed at the bot

        :Args:
        `command` is the command the user entered

        `channel` is the ID of the channel the message was written in

        `user` is the ID of the user that originally wrote the message

        :Returns:
        Nothing
        """
        if not text:
            self.respond_to(
                channel, user, "You tagged me! Try " + mention_bot() + " `list` to get started."
            )
            return

        text = text.split()
        command = text[0].lower()
        log_to_console("Command used was '" + command + "'")

        arguments = text[1:]  # I think this is clearer than passing on a modified text array
        self.choose_command(command, arguments, channel, user, output)

    def choose_command(self, command, arguments, channel, user, output):
        """
        Helper function to choose the command corresponding to the command
        """
        if not command in constants.COMMANDS:
            return self.respond_to(
                channel,
                user,
                (
                    "I'm sorry, I dont understand.\n"
                    f"Try `{mention_bot()} list` or `{mention_bot()} help`"
                ),
                ephemeral=True,
            )

        func = constants.COMMANDS[command]
        return func(self, channel, user, arguments, output)

    def post_message(self, channel, message):
        """
        Posts a message to a chat channel as the bot

        :Args:

        `channel` the ID of the channel to post the message in

        `message` the message to be posted. Should be a string.
        """
        self.slack_client.api_call("chat.postMessage", channel=channel, as_user=True, text=message)

    def post_ephemeral_message(self, channel, user, message):
        """
        Posts an ephemeral message directed at a user to a chat channel as the bot

        :Args:

        `channel` the ID of the channel to post the message in.

        `user` the ID of the user the message should be directed at.

        `message` the message to be posted. Should be a string.
        """
        self.slack_client.api_call(
            "chat.postEphemeral", channel=channel, user=user, as_user=True, text=message
        )

    def respond_to(self, channel, user, message, **kwargs):
        """
        Posts a response directed at a user.

        :Args:

        `channel` the ID of the channel to post the message in

        `message` the message to be posted. Should be a string.

        `user` the ID of the user the message should be directed at.
        """
        if kwargs.get("ephemeral", False):
            self.post_ephemeral_message(channel, user, mention_user(user) + "\n" + message)
            return
        self.post_message(channel, mention_user(user) + "\n" + message)

    def download_file(self, filename, url):
        """
        Downloads a file from Slack from the given `url`.
        Then saves the files to system as `filename` in the directory the bot is being run from.
        """
        token = os.environ.get("SLACK_BOT_TOKEN")
        res = requests.get(url, headers={"Authorization": "Bearer %s" % token})
        res.raise_for_status()

        with open(filename, "wb") as file:
            for chunk in res.iter_content():
                file.write(chunk)

    def delete_file(self, file_id):
        """
        Deletes `file_id` from Slack.
        """
        delete_url = "https://slack.com/api/files.delete"
        params = {"token": os.environ.get("APP_TOKEN"), "file": file_id}
        res = requests.get(delete_url, params=params)
        res.raise_for_status()


# Using pathlib to construct path so we make sure that it works on both Windows and Linux
if os.path.isfile(pathlib.Path.cwd().joinpath("setup", "secret-dev.env")):
    dotenv.load_dotenv(dotenv_path=pathlib.Path.cwd().joinpath("setup", "secret-dev.env"))
    print("secret-dev.env loaded...")
elif os.path.isfile(pathlib.Path.cwd().joinpath("setup", "secret-prod.env")):
    dotenv.load_dotenv(dotenv_path=pathlib.Path.cwd().joinpath("setup", "secret-prod.env"))
    print("secret-prod.env loaded...")
else:
    print("Environment variables not found...")
    print("Bot could not start.")
    sys.exit()  # Should probably handle this in run()..

# Set up loggers
if not os.path.exists("log"):
    os.mkdir("log")
LOGGERS = {
    "output": logging.getLogger("Output"),
    "stacktrace": logging.getLogger("Stack trace"),
    "reconnect": logging.getLogger("Reconnect"),
    "console": logging.getLogger("Console"),
}
LOGGERS["output"].setLevel(logging.DEBUG)
LOGGERS["stacktrace"].setLevel(logging.ERROR)
LOGGERS["reconnect"].setLevel(logging.INFO)
LOGGERS["console"].setLevel(logging.CRITICAL)
FORMATTER = logging.Formatter("%(asctime)s - %(name)s" + " - %(levelname)s - %(message)s")
HANDLERS = {
    "output": RotatingFileHandler(
        "log" + os.sep + "output.log", maxBytes=1024 * 1024, backupCount=2
    ),
    "stacktrace": RotatingFileHandler(
        "log" + os.sep + "stacktrace.log", maxBytes=1024 * 128, backupCount=1
    ),
    "reconnect": RotatingFileHandler(
        "log" + os.sep + "reconnect.log", maxBytes=1024 * 128, backupCount=2
    ),
    "console": logging.StreamHandler(),
}
for key, logger in LOGGERS.items():
    HANDLERS[key].setFormatter(FORMATTER)
    logger.addHandler(HANDLERS[key])
# OUTPUT_LOGGER = logging.getLogger("Output")
# STACKTRACE_LOGGER = logging.getLogger("Stack trace")
# RECONNECT_LOGGER = logging.getLogger("Reconnect")

if __name__ == "__main__":
    BOT = BotClient()
    BOT.run()
