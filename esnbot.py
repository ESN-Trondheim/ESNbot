import os
import time
from slackclient import SlackClient

# esnbot's ID
BOT_ID = os.environ.get("BOT_ID")

# Constants
AT_BOT = "<@" + BOT_ID + ">"
