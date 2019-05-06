"""
    A slack bot to help ESN Trondheim
"""

import os
import time

from slackclient import SlackClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from PIL import Image

import watermark as wm

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
    "standliste",
    "watermark"
    ]

# Instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN")) #pylint: disable=invalid-name

# gspread
SCOPE = ['https://spreadsheets.google.com/feeds']
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name('drivecredentials.json', SCOPE)

"""GSHEET = gspread.authorize(CREDENTIALS)
BEER_WINE_SHEET = GSHEET.open_by_key(os.environ.get("BEER_WINE_KEY")).sheet1
print("Beer/wine-sheet opened...", flush=True)
CONTACT_INFO_SHEET = GSHEET.open_by_key(os.environ.get("CONTACT_INFO_KEY")).sheet1
print("Contact info sheet opened...", flush=True)"""

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
            if (output['type'] != 'desktop_notification'
                    and output['type'] != 'reconnect_url'
                    and output['type'] != 'presence_change'):
                # maybe make this filter out ephemeral messages as well, like google drive messages
                print(timestamp() + str(output) + "\n", flush=True)
            if (output['type'] == 'goodbye'):
                print(timestamp() + "Session ended.", flush=True)
                print(timestamp() + "Initiating new session...", flush=True)
                if slack_client.rtm_connect():
                    print(timestamp() + "ESNbot reconnected and running...", flush=True)
                else:
                    print(timestamp() + "Reconnection failed.", flush=True)
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

def timestamp():
    """
    Returns a timestamp formatted properly as a string.
    """
    return time.strftime("%d-%m-%Y %H:%M:%S: ", time.localtime())

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
    print(timestamp() + "Command used was '" + command + "'", flush=True)

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
        "list": command_list,
        "reimbursement": command_reimbursement,
        "esnfarger": command_esn_colors,
        "esnfont": command_esn_font,
        "standliste": command_stand_list
    }
    cmds_with_args = {
        "help": command_help,
        "ølstraff": command_beer_wine_penalty,
        "vinstraff": command_beer_wine_penalty,
        "kontaktinfo": command_contact_info,
        "watermark": command_watermark
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

def command_help(channel, argument, user, output):
    help_items = {
        "help": "Use `help 'command'` to get help using that command.\n"
                + "Some examples include:\n"
                + ">•" + AT_BOT + " `help`\n"
                + ">•" + AT_BOT + " `help list`\n"
                + "For a list of all available commands, use  `list`",
        "list": "Displays a list of all available commands.",
        "kontaktinfo": "Use `kontaktinfo 'first name'` to get contact info for `first name`\n"
                       + "Displays the link to the contact info sheet if no name is entered.",
        "ølstraff": "Use `ølstraff 'first name'` to get the standings for `first name`\n"
                    + "Displays the link to the rules if no name is entered.",
        "vinstraff": "Use `vinstraff 'first name'` to get the standings for `first name`\n"
                     + "Displays the link to the rules if no name is entered.",
        "reimbursement": "Displays the link to the reimbursement sheet and the guidelines.",
        "esnfarger": "Displays the official ESN colors along with their hex color code.",
        "esnfont": "Displays the names of the official ESN fonts.",
        "standliste": "Displays the link to the stand list sheet.",
        "watermark": "Watermarks a given picture.\n"
                     + "Upload the picture and add a comment *when uploading* with"
                     + " the position and color of the watermark.\n"
                     + "If no color is entered, the watermark will be in full colors.\n"
                     + "Valid colors are `color`, `black` and `white`.\n"
                     + "If no position is entered, the watermark will be in the bottom right.\n"
                     + "Positions are abbreviated as follows:\n"
                     + ">•`tl` = top left\n"
                     + ">•`tr` = top right\n"
                     + ">•`bl` = bottom left\n"
                     + ">•`br` = bottom right\n"
                     + "*Examples*\n"
                     + ">" + AT_BOT + " `watermark` \n"
                     + ">" + AT_BOT + " `watermark bl`\n"
                     + ">" + AT_BOT + " `watermark white tl`\n"
                     + ">" + AT_BOT + " `watermark tr black`\n"
    }
    if not argument:
        argument.append("help")
    if argument[0].lower() in help_items:
        respond_to(channel, user, "`" + argument[0].lower() + "`\n" + help_items[argument[0]])
    else:
        respond_to(channel, user, "I'm not sure what you want help with.")

def command_list(channel, user):
    command_string = ""
    for command in COMMANDS:
        command_string = command_string + "`" + command + "`\n"
    respond_to(channel, user, "Available commands:\n" + command_string)

def command_contact_info(channel, argument, user, output):
    if not argument:
        respond_to(channel, user, os.environ.get("CONTACT_INFO"))
    else:
        gsheet = gspread.authorize(CREDENTIALS)
        contact_info_sheet = gsheet.open_by_key(os.environ.get("CONTACT_INFO_KEY")).sheet1
        print(timestamp() + "Contact info sheet opened...", flush=True)
        contact_info_records = contact_info_sheet.get_all_records()
        response = ""
        for column in contact_info_records:
            if column['Fornavn'].lower().startswith(argument[0].lower()):
                name = column['Fornavn'] + " " + column['Etternavn']
                response = (response + "```" + name + ":"
                            + " Tlf: " + str(column['Telefon'])
                            + " E-post: " + str(column['E-post']) + "```\n")
        if response:
            respond_to(channel, user, response)
        else:
            respond_to(channel, user, "Sorry, could not find anyone named '" + argument[0] + "'")

def command_beer_wine_penalty(channel, argument, user, output):
    if not argument:
        respond_to(channel, user, os.environ.get("BEER_WINE_PENALTY"))
    else:
        # possibly add in a try statement here
        gsheet = gspread.authorize(CREDENTIALS)
        beer_wine_sheet = gsheet.open_by_key(os.environ.get("BEER_WINE_KEY")).sheet1
        print(timestamp() + "Beer/wine-sheet opened...", flush=True)
        beer_wine_records = beer_wine_sheet.get_all_records()
        response = ""
        for column in beer_wine_records:
            if column['Fornavn'].lower().startswith(argument[0].lower()):
                name = column['Fornavn'] + " " + column['Etternavn']
                response = (response + "```" + name + ":"
                            + " Vinstraff: " + str(column['Vinstraff'])
                            + " Ølstraff: " + str(column['Ølstraff']) + "```\n")
        if response:
            respond_to(channel, user, response)
        else:
            respond_to(channel, user, "Sorry, could not find '" + argument[0] + "'")

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

def command_watermark(channel, argument, user, output):
    #if output.get('subtype') != "file_share":
    #    # command_help expects an array containing the help item
    #    # Displays help for watermark if watermark is not called from a file upload
    #    command_help(channel, ["watermark"], user, output)
    #else:
    if output.get('files'):
        respond_to(channel, user, "I'll get right on it! Your picture(s) will be ready in a jiffy!")

        original_file_id = output['files'][0]['id']
        original_file_url = output['files'][0]['url_private']
        filename = "watermarked." + original_file_url.split(".")[-1]
        download_file(filename, original_file_url)

        try:
            start_img = wm.Image.open(filename)
        except OSError:
            respond_to(channel, user, "That is not a valid image format.\nSee "
                       + "https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html"
                       + " for a full list of supported file formats.")
            os.remove(filename)
            delete_file(original_file_id)
            return
        
        wm.watermark(start_img, argument, filename)


        comment = (mention_user(user) + "\nHere's your picture!"
                   + " Your uploaded picture will now be deleted.")
        upload_response = slack_client.api_call("files.upload", file=open(filename, "rb"),
                                                channels=channel, initial_comment=comment)
        # upload_id is meant for later use, to be able to delete the uploaded picture.
        # upload_id = upload_response['file']['id']

        #"""time.sleep(READ_WEBSOCKET_DELAY)"""
        #print(file_id, flush=True)
        #"""slack_client.api_call("files.delete", file=file_id)"""

        # this is hacky, and not the intended way to use these tokens, but it works
        # Deletes file from Slack
        delete_file(original_file_id)
        # Deletes file from system
        os.remove(filename)
    else:
        # command_help expects an array containing the help item
        # Displays help for watermark if watermark is not called from a file upload
        command_help(channel, ["watermark"], user, output)

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

def run():
    """
        Main function
    """
    if slack_client.rtm_connect(auto_reconnect=True):
        print(timestamp() + "ESNbot connected and running...", flush=True)
        while True:
            text, channel, user, output = parse_slack_output(slack_client.rtm_read())
            if channel:
                handle_command(text, channel, user, output)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print(timestamp() + "Connection failed.", flush=True)

if __name__ == "__main__":
    run()
