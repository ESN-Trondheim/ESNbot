"""
    A slack bot to help ESN Trondheim

    TODO:
    -Maybe have the bot answer commands in a thread? May be trouble if sending the bot a PM
    -Should be able to supply arguments to some of the commands e.g. @ESNbot help list,
    @ESNbot kontaktinfo Lai, @ESNbot kontaktinfo list
    -command_contact_info() should have the option of entering a name as an argument.
    The function should then return the contact info of that specific person,
    instead of (or in addition to) returning the link to the contact info sheet.
    -beer-wine-penalty should actually be two commands, one should display the rules
    and a link to the rules, the second should display the current standings.
    This info should be pulled from a google spreadsheet which contains the relevant information.
    -Add option to delete all messages except admin messages in a channel
    -Add support for adding simple commands via a .json or similar.
    This is meant for commands that simply respond with a predefined response.
    -The standlist command should display info for that person if name is supplied as an argument
    -If the bot is tagged in a thread, it should respond in that same thread.
    May use a kwarg to specify that it is a thread
    -Should print timestamps in console when printing output
    -BUG: if you comment with @ESNbot on an uploaded file, the bot will crash.
    This is because it looks up who the user was,
    but this message doesn't have a user key in the dict.
    This is somewhat fixed. The bot will not crash, but it will respond to the channel
    instead of as a new comment in the thread.
"""

import os
import time
from slackclient import SlackClient

# esnbot's ID
BOT_ID = os.environ.get("BOT_ID")

# Constants
AT_BOT = "<@" + BOT_ID + ">"
READ_WEBSOCKET_DELAY = 1
COMMANDS = [
    "help",
    "list",
    "kontaktinfo",
    "ølstraff",
    "vinstraff",
    "reimbursement",
    "esnfarger",
    "esnfont",
    "standliste"
    ]

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
    if output_list:
        for output in output_list:
            print(output, flush=True)
            if output and 'text' in output and AT_BOT in output['text']:
                text = output['text'].split(AT_BOT)[1].strip().lower()
                if 'subtype' in output:
                    if output['subtype'] == "file_comment":
                        return (text, output['channel'], output['file']['user'])
                if output['user'] == BOT_ID:
                    return None, None, None #Don't care about the bot's own messages
                return (text, output['channel'], output['user'])
    return None, None, None

def mention_user(user):
    """
    Helper function to make it easier to mention users

    :Args:

    `user` the ID of the user

    :Returns:

    A string formatted in a way that will mention the user on Slack
    """
    return "<@" + user + ">"

def handle_command(text, channel, user):
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
        respond_to(channel, user, "You tagged me!")
        return

    text = text.split()
    command = text[0]
    print("Command used was '" + command + "'", flush=True)

    if command not in COMMANDS:
        respond_to(channel, user,
                   "I'm sorry, I dont understand."
                   + "\nTry " + AT_BOT + " `list`  or " + AT_BOT + " `help`",
                   ephemeral=True)
    else:
        # text.pop(0) # may also use del text[0]
        arguments = text[1:] # I think this is clearer than passing on a modified text array
        choose_command(command, arguments, channel, user)

def choose_command(command, arguments, channel, user):
    """
    Helper function to choose the command corresponding to the command
    """
    cmds = {
        "list": command_list,
        "kontaktinfo": command_contact_info,
        "ølstraff": command_beer_wine_penalty,
        "vinstraff": command_beer_wine_penalty,
        "reimbursement": command_reimbursement,
        "esnfarger": command_esn_colors,
        "esnfont": command_esn_font,
        "standliste": command_stand_list
    }
    cmds_with_args = {
        "help": command_help
    }
    if command in cmds_with_args:
        func = cmds_with_args[command]
        return func(channel, arguments, user)
    func = cmds[command]
    # Can use func = selector.get(command) as well
    return func(channel, user)

def post_message(channel, message):
    """
    Posts a message to a chat channel as the bot

    :Args:

    `channel` the ID of the channel to post the message in

    `message` the message to be posted. Should be a string.
    """
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True, text=message)

def post_ephemeral_message(channel, user, message):
    """
    Posts an ephemeral message directed at a user to a chat channel as the bot

    :Args:

    `channel` the ID of the channel to post the message in.

    `user` the ID of the user the message should be directed at.

    `message` the message to be posted. Should be a string.
    """
    slack_client.api_call("chat.postEphemeral", channel=channel,
                          user=user, as_user=True, text=message)

def respond_to(channel, user, message, **kwargs):
    """
    Posts a response directed at a user.

    :Args:

    `channel` the ID of the channel to post the message in

    `message` the message to be posted. Should be a string.

    `user` the ID of the user the message should be directed at.
    """
    if kwargs.get("ephemeral", False):
        post_ephemeral_message(channel, user, mention_user(user) + "\n" + message)
        return
    post_message(channel, mention_user(user) + "\n" + message)

def command_help(channel, argument, user):
    help_items = {
        "help": "Use `help 'command'` to get help using that command.\n"
                + "Some examples include:\n"
                + "•" + AT_BOT + " `help`\n"
                + "•" + AT_BOT + " `help list`\n"
                + "For a list of all available commands, use  `list`",
        "list": "Displays a list of all available commands.",
        "kontaktinfo": "Displays the link to the contact info sheet.",
        "ølstraff": "Displays the link to the rules.",
        "vinstraff": "Displays the link to the rules.",
        "reimbursement": "Displays the link to the reimbursement sheet and the guidelines.",
        "esnfarger": "Displays the official ESN colors along with their hex color code.",
        "esnfont": "Displays the names of the official ESN fonts.",
        "standliste": "Displays the link to the stand list sheet."
    }
    if not argument:
        argument.append("help")
    if argument[0] in help_items:
        respond_to(channel, user, "`" + argument[0] + "`\n" + help_items[argument[0]])
    else:
        respond_to(channel, user, "I'm not sure what you want help with.")

def command_list(channel, user):
    command_string = ""
    for command in COMMANDS:
        command_string = command_string + "`" + command + "`\n"
    respond_to(channel, user, "Available commands:\n" + command_string)

def command_contact_info(channel, user):
    respond_to(channel, user, os.environ.get("CONTACT_INFO"))

def command_beer_wine_penalty(channel, user):
    respond_to(channel, user, os.environ.get("BEER_WINE_PENALTY"))

def command_reimbursement(channel, user):
    respond_to(channel, user, "Reimbursement form: " + os.environ.get("REIMBURSEMENT_FORM")
               + "\nGuidelines: " + os.environ.get("REIMBURSEMENT_FORM_GUIDELINES"))

def command_esn_colors(channel, user):
    respond_to(channel, user,
               "• ESN Cyan #00aeef\n"
               + "• ESN Magenta #ec008c\n"
               + "• ESN Green #7ac143\n"
               + "• ESN Orange #f47b20\n"
               + "• ESN Dark Blue #2e3192\n"
               + "• Black #000000\n"
               + "• White #ffffff")

def command_esn_font(channel, user):
    respond_to(channel, user, "Display font: Kelson Sans\n" + "Content font: Lato")

def command_stand_list(channel, user):
    respond_to(channel, user, os.environ.get("STAND_LIST"))

def run():
    """
        Main function
    """
    if slack_client.rtm_connect():
        print("ESNbot connected and running.", flush=True)
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed.")

if __name__ == "__main__":
    run()
