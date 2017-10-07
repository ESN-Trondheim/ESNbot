"""
    A slack bot to help ESN Trondheim

    TODO:
    -Maybe have the bot answer commands in a thread? May be trouble if sending the bot a PM
    -Should be able to supply arguments to some of the commands e.g. @ESNbot help list,
    @ESNbot kontaktinfo Lai, @ESNbot kontaktinfo list
    -command_contact_info() should have the option of entering a name as an argument.
    The function should then return the contact info of that specific person,
    instead of (or in addition to) returning the link to the contact info sheet.
    -Have ESNbot take over some of the commands that slack bot are doing now,
    e.g. esnfarger, esnfont and so on. Link to VIM or other relevant documents
    as well.
    -beer-wine-penalty should actually be two commands, one should display the rules
    and a link to the rules, the second should display the current standings.
    This info should be pulled from a google spreadsheet which contains the relevant information.
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
    "esnfont"
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
                if output['user'] == BOT_ID:
                    return None, None, None #Don't care about the bot's own messages
                return (text, output['channel'], output['user'])
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
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                              text=mention_user(user) + " You tagged me!")
        return

    text = text.split()
    command = text[0]
    print("Command used was '" + command + "'", flush=True)

    if command not in COMMANDS:
        slack_client.api_call("chat.postEphemeral", channel=channel, user=user, as_user=True,
                              text=mention_user(user)
                              + ", I'm sorry, I dont understand."
                              + "\nTry " + AT_BOT + " `list`  or " + AT_BOT + " `help`",)
    else:
        # text.pop(0) # may also use del text[0]
        arguments = text[1:] # I think this is clearer than passing on a modified text array
        choose_command(command, arguments, channel, user)

def choose_command(command, arguments, channel, user):
    """
    Helper function to choose the command corresponding to the command
    """
    selector = {
        "help": command_help,
        "list": command_list,
        "kontaktinfo": command_contact_info,
        "ølstraff": command_beer_wine_penalty,
        "vinstraff": command_beer_wine_penalty,
        "reimbursement": command_reimbursement,
        "esnfarger": command_esn_colors,
        "esnfont": command_esn_font
    }
    func = selector[command]
    # Can use func = selector.get(command) as well
    if command == "help":
        return func(channel, arguments, user)
    return func(channel, user)

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
        "esnfont": "Displays the names of the official ESN fonts."
    }
    if not argument:
        argument.append("help")
    if argument[0] in help_items:
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                              text=mention_user(user)
                              + "\n`" + argument[0] + "`\n"
                              + help_items[argument[0]])
    else:
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                              text=mention_user(user)
                              + "I'm not sure what you want help with.")

def command_list(channel, user):
    command_string = ""
    for command in COMMANDS:
        command_string = command_string + "`" + command + "`\n"

    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user)
                          + "\nAvailable commands:\n" + command_string)

def command_contact_info(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\n" + os.environ.get("CONTACT_INFO"))

def command_beer_wine_penalty(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\n" + os.environ.get("BEER_WINE_PENALTY"))

def command_reimbursement(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\nReimbursement form: "
                          + os.environ.get("REIMBURSEMENT_FORM")
                          + "\nGuidelines: " + os.environ.get("REIMBURSEMENT_FORM_GUIDELINES"))

def command_esn_colors(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\n"
                          + "• ESN Cyan #00aeef\n"
                          + "• ESN Magenta #ec008c\n"
                          + "• ESN Green #7ac143\n"
                          + "• ESN Orange #f47b20\n"
                          + "• ESN Dark Blue #2e3192\n"
                          + "• Black #000000\n"
                          + "• White #ffffff")

def command_esn_font(channel, user):
    slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                          text=mention_user(user) + "\n"
                          + "Display font: Kelson Sans\n"
                          + "Content font: Lato")

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
