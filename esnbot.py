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
    Parses messages written in channels that the bot is a part of.

    :Args:
    `slack_rtm_output` is the events that are fired in the channel

    :Returns:
    `text`, `channel`, `user` where text is the message after the bot is mentioned,
    channel is the id of the channel, user is the id of the user.
    If this information is not present, None, None, None is returned.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print(output, flush=True)
            if output and 'text' in output and AT_BOT in output['text']:
                return (output['text'].split(AT_BOT)[1].strip().lower(), output['channel'],
                        output['user'])
    return None, None, None

def mention_user(user):
    """
    Helper function to make it easier to mention users

    :Args:
    `user` is the ID of the user

    :Returns:
    A string that mentions the user
    """
    return "<@" + user + ">"

def handle_command(command, channel, user):
    """
    Handles a command directed at the bot

    :Args:
    `command` is the command the user entered

    `channel` is the ID of the channel the message was written in

    `user` is the ID of the user that originally wrote the message

    :Returns:
    Nothing
    """
    print("Command used was '" + command + "'", flush=True)
    commands = [
        "help",
        "list",
        "kontaktinfo",
        "ølstraff",
        "vinstraff",
        "reimbursement"
    ]
    if command not in commands:
        slack_client.api_call("chat.postEphemeral", channel=channel, user=user, as_user=True,
                              text=mention_user(user)
                              + ", I'm sorry, I dont understand."
                              + "\nTry '" + AT_BOT + " list' for a list of available commands",)
    else:
        choose_command(command, channel, user)

def choose_command(command, channel, user):
    """
    Helper function to choose the command corresponding to the command
    """
    switcher = {
        "help": command_help,
        "list": command_list,
        "kontaktinfo": command_contact_info,
        "ølstraff": command_beer_wine_penalty,
        "vinstraff": command_beer_wine_penalty,
        "reimbursement": command_reimbursement
    }
    func = switcher.get(command)
    return func(channel, user)

def command_help(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user)
                          + " I'm sorry, this isn't implemented yet. It will be soon™.")

def command_list(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\nAvailable commands are:\n"
                          + "`list`\n"
                          + "`help`\n"
                          + "`kontaktinfo`\n"
                          + "`ølstraff`\n"
                          + "`vinstraff`\n"
                          + "`reimbursement`")

def command_contact_info(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\n" + os.environ.get("CONTACT_INFO"))

def command_beer_wine_penalty(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user)
                          + " I'm sorry, this isn't implemented yet. It will be soon™.")

def command_reimbursement(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\nReimbursement form: " + os.environ.get("REIMBURSEMENT_FORM")
                          + "\nGuidelines: " + os.environ.get("REIMBURSEMENT_FORM_GUIDELINES"))

def run():
    """
        Main function
    """
    if slack_client.rtm_connect():
        print("ESNbot connected and running.", flush=True)
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed.")

if __name__ == "__main__":
    run()
