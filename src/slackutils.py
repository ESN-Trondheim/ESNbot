from utils import log_to_console
from constants import COMMANDS, AT_BOT, BOT_ID, IGNORED_MESSAGE_TYPES
import os
import requests
import commands as cmd
from slackclient import SlackClient

# Instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN")) #pylint: disable=invalid-name

def parse_slack_output(slack_rtm_output, LOGGERS):
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
            if output['type'] not in IGNORED_MESSAGE_TYPES:
                # maybe make this filter out ephemeral messages as well, like google drive messages
                log_to_console(str(output) + "\n")
            if output['type'] == 'goodbye':
                LOGGERS["output"].info("Session ended. ('goodbye' event)")
                log_to_console("Session ended. ('goodbye' event)")
                LOGGERS["output"].info("Initiating new session... ('goodbye' event)")
                log_to_console("Initiating new session... ('goodbye' event)")
                if slack_client.rtm_connect(auto_reconnect=True):
                    LOGGERS["output"].info("ESNbot reconnected and running... ('goodbye' event)")
                    log_to_console("ESNbot reconnected and running... ('goodbye' event)")
                else:
                    LOGGERS["output"].error("Reconnection failed.")
                    log_to_console("Reconnection failed. ('goodbye' event)")
            if output and 'text' in output and AT_BOT in output['text']:
                text = output['text'].split(AT_BOT)[1].strip()
                if output.get('subtype') == "file_comment":
                    return (text, output['channel'], output['file']['user'], output)
                #futureproofing if the bot will ever respond to file comments as a file comment.
                #or output.get('file').get('user') == BOT_ID
                #this does not work if 'file' does not exist. 'file' is then None,
                #and you can't call get() on a NoneType object
                if output.get('user') == BOT_ID:
                    return None, None, None, None #Don't care about the bot's own messages
                return (text, output['channel'], output['user'], output)
    return None, None, None, None


def mention_user(user):
    """
    Helper function to make it easier to mention users

    :Args:

    `user` the ID of the user

    :Returns:

    A string formatted in a way that will mention the user on Slack
    """
    return "<@" + user + ">"

def handle_command(text, channel, user, output):
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
        respond_to(channel, user, "You tagged me! Try " + AT_BOT + " `list` to get started.")
        return

    text = text.split()
    command = text[0].lower()
    log_to_console("Command used was '" + command + "'")

    if command not in COMMANDS:
        respond_to(channel, user,
                   "I'm sorry, I dont understand."
                   + "\nTry " + AT_BOT + " `list`  or " + AT_BOT + " `help`",
                   ephemeral=True)
    else:
        # text.pop(0) # may also use del text[0]
        arguments = text[1:] # I think this is clearer than passing on a modified text array
        choose_command(command, arguments, channel, user, output)

def choose_command(command, arguments, channel, user, output):
    """
    Helper function to choose the command corresponding to the command
    """
    cmds = {
        "list": cmd.command_list,
        "reimbursement": cmd.command_reimbursement,
        "esnfarger": cmd.command_esn_colors,
        "esnfont": cmd.command_esn_font,
        "standliste": cmd.command_stand_list
    }
    cmds_with_args = {
        "help": cmd.command_help,
        "ølstraff": cmd.command_beer_wine_penalty,
        "vinstraff": cmd.command_beer_wine_penalty,
        "kontaktinfo": cmd.command_contact_info,
        "watermark": cmd.command_watermark,
        "coverphoto": cmd.command_make_cover_photo
    }
    if command in cmds_with_args:
        func = cmds_with_args[command]
        return func(channel, arguments, user, output)
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

def download_file(filename, url):
    """
    Downloads a file from Slack from the given `url`.
    Then saves the files to system as `filename` in the directory the bot is being run from.
    """
    token = os.environ.get("SLACK_BOT_TOKEN")
    res = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
    res.raise_for_status()

    with open(filename, "wb") as file:
        for chunk in res.iter_content():
            file.write(chunk)

def delete_file(file_id):
    """
    Deletes `file_id` from Slack.
    """
    delete_url = "https://slack.com/api/files.delete"
    params = {
        'token': os.environ.get("APP_TOKEN"),
        'file': file_id
    }
    res = requests.get(delete_url, params=params)
    res.raise_for_status()