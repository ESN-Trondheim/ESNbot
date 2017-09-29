"""
    A slack bot to help ESN Trondheim
"""

import os
import time
from slackclient import SlackClient

# esnbot's ID
BOT_ID = os.environ.get("BOT_ID")

# Constants
AT_BOT = "<@" + BOT_ID + ">"
READ_WEBSOCKET_DELAY = 1

# Instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN")) #pylint: disable=invalid-name

def parse_slack_output(slack_rtm_output):
    """
        This function parses messages written in channels that the bot is a part of.
        If the message is directed at the bot, this function returns the message
        (without the mention), the channel ID and the user ID.
        Returns None if the message is not directed at the bot.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print(output, flush=True)
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel'], output['user']
    return None, None, None

def mention_user(user):
    """
        Parameter is the user ID. Returns a string that mentiosn the user.
    """
    return "<@" + user + ">"

def handle_command(command, channel, user):
    """
        temp
    """
    print(command, flush=True)
    slack_client.api_call("chat.postMessage", channel=channel, text="You tagged me, " + mention_user(user), as_user=True)

def run():
    """
        Main function
    """
    if slack_client.rtm_connect():
        print("esnbot connected and running.", flush=True)
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed.")

if __name__ == "__main__":
    run()
    