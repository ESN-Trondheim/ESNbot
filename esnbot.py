import os
import time
from slackclient import SlackClient

# esnbot's ID
BOT_ID = os.environ.get("BOT_ID")

# Constants
AT_BOT = "<@" + BOT_ID + ">"

# Instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN")) # pylint: disable=invalid-name

if __name__ == "__main__":
    READ_WEBSOCKET_DEALY = 1
    if slack_client.rtm_connect():
        print("esnbot connected and running.")
    else:
        print("Connection failed.")
