import slackutils as slack
import os

def command(channel, user, argument, output):
    slack.respond_to(channel, user, os.environ.get("STAND_LIST"))