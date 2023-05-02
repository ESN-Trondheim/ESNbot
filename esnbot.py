"""
    A slack bot to help ESN Trondheim
"""

import os
import time
import logging
from logging.handlers import RotatingFileHandler
import traceback

from slackclient import SlackClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

import watermark as wm
import coverphoto

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
    "watermark",
    "coverphoto"
    ]
IGNORED_MESSAGE_TYPES = [
    "desktop_notification",
    "reconnect_url",
    "dnd_updated_user",
    "user_change",
    "presence_change",
    "user_typing",
    "file_deleted",
    "file_shared",
    # "file_change", # Not sure if this should be ignored in console
    # "file_created" # Not sure if this should be ignored in console
]

# Set up loggers
if not os.path.exists("log"):
    os.mkdir("log")
LOGGERS = {
    "output": logging.getLogger("Output"),
    "stacktrace": logging.getLogger("Stack trace"),
    "reconnect": logging.getLogger("Reconnect"),
    "console": logging.getLogger("Console")
}
LOGGERS["output"].setLevel(logging.DEBUG)
LOGGERS["stacktrace"].setLevel(logging.ERROR)
LOGGERS["reconnect"].setLevel(logging.INFO)
LOGGERS["console"].setLevel(logging.CRITICAL)
FORMATTER = logging.Formatter("%(asctime)s - %(name)s"
                              + " - %(levelname)s - %(message)s")
HANDLERS = {
    "output": RotatingFileHandler("log" + os.sep + "output.log",
                                  maxBytes=1024*1024, backupCount=2),
    "stacktrace": RotatingFileHandler("log" + os.sep + "stacktrace.log",
                                      maxBytes=1024*128, backupCount=1),
    "reconnect": RotatingFileHandler("log" + os.sep + "reconnect.log",
                                     maxBytes=1024*128, backupCount=2),
    "console": logging.StreamHandler()
}
for key, logger in LOGGERS.items():
    HANDLERS[key].setFormatter(FORMATTER)
    logger.addHandler(HANDLERS[key])
# OUTPUT_LOGGER = logging.getLogger("Output")
# STACKTRACE_LOGGER = logging.getLogger("Stack trace")
# RECONNECT_LOGGER = logging.getLogger("Reconnect")

# Instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN")) #pylint: disable=invalid-name

# gspread
SCOPE = ['https://spreadsheets.google.com/feeds']
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name("setup" + os.sep + "drivecredentials.json", SCOPE)

def parse_slack_output(slack_rtm_output):
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

def timestamp():
    """
    Returns a timestamp formatted properly as a string.
    """
    return time.strftime("%d-%m-%Y %H:%M:%S: ", time.localtime())

def log_to_console(text):
    """
    Helper function to log what happens to console.
    Prints timestamp followed by `text`, with flush=True
    """
    print(timestamp() + text, flush=True)

def log_to_file(filename, message, mode):
    """
    Helper function to log things to textfile.
    Used mostly for logging what happens in case of crashes.
    """
    with open(filename, mode) as file:
        file.write(timestamp() + message + "\n")

def log_to_file_and_console(filename, message, mode):
    """
    Helper function if it's needed to log to both console and file.
    """
    log_to_console(message)
    log_to_file(filename, message, mode)

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
        "watermark": command_watermark,
        "coverphoto": command_make_cover_photo
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
                     + "Upload the picture (or a zip file containing pictures)"
                     + " and add a comment *when uploading* with"
                     + " the watermark command.\n"
                     + "You may choose the color of the logo and the position,"
                     + " but the default options are recommended.\n"
                     + "Default is colors in the bottom right corner.\n"
                     + "Valid colors are `color`, `black` and `white`.\n"
                     + "Positions are abbreviated as follows:\n"
                     + ">•`tl` = top left\n"
                     + ">•`tr` = top right\n"
                     + ">•`bl` = bottom left\n"
                     + ">•`br` = bottom right\n"
                     + "*Examples*\n"
                     + ">" + AT_BOT + " `watermark` \n"
                     + ">" + AT_BOT + " `watermark bl`\n"
                     + ">" + AT_BOT + " `watermark white tl`\n"
                     + ">" + AT_BOT + " `watermark tr black`\n",
        "coverphoto": "Creates a cover photo for Facebook from the uploaded picture.\n"
                      + "Upload the picture and add a comment *when uploading* with"
                      + " the command, the color of the overlay, if it's a cover photo for buddy"
                      + " the title and optionally subtitle(s).\n"
                      + "Write `buddy` directly after `coverphoto`"
                      + " if you want a buddy cover photo.\n"
                      + "Title and subtitles have to be enclosed in quotation marks (\").\n"
                      + "You may enter up to two subtitles.\n"
                      + "If no color is entered, the cover photo will be blue.\n"
                      + "Valid colors are `cyan`, `magenta`, `green`, `orange`,"
                      + "`blue`.\n" # and `all`. `all` will return a zipped file "
                      # + "containing all five color variants.\n"
                      + "For best results, your image should be 1568*588 or larger.\n"
                      + "If the image is larger, it will be cropped around the center "
                      + "to fit the dimensions.\n"
                      + "If the image is smaller, it will be upscaled and cropped around the "
                      + "center to fit the dimensions.\n"
                      + "*Examples*\n"
                      + ">" + AT_BOT + " `coverphoto \"Title\"`\n"
                      + ">" + AT_BOT + " `coverphoto blue \"Title\" \"Subtitle\"`\n"
                      + ">" + AT_BOT + " `coverphoto buddy \"Title\" \"Subtitle\" \"Subtitle2\"`\n"
                      + ">" + AT_BOT + " `coverphoto buddy cyan \"Title\" \"Subtitle\"`\n"
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

def open_spreadsheet(sheet_key):
    gsheet = gspread.authorize(CREDENTIALS)
    contact_info_sheet = gsheet.open_by_key(os.environ.get(sheet_key)).sheet1
    log_to_console("Spreadsheet opened...")
    return contact_info_sheet.get_all_records()

def get_info_from_sheet(name, sheet, *args):
    response_list = []
    name = name.lower()
    for column in sheet:
        if column["Fornavn"].lower().startswith(name):
            response_list.append("```")
            found_name = f"{column['Fornavn']} {column['Etternavn']}:\n"
            response_list.append(found_name)
            for arg in args:
                response_list.append(f"{arg}: {str(column[arg])}\n")
            response_list.append("```\n")
    response = ("").join(response_list)
    return response

def command_contact_info(channel, argument, user, output):
    if not argument:
        respond_to(channel, user, os.environ.get("CONTACT_INFO"))
    else:
        try:
            contact_info_sheet = open_spreadsheet("CONTACT_INFO_KEY")
        except gspread.SpreadsheetNotFound: # Error handling
            log_to_console("Spreadsheet not found...")
            respond_to(channel, user, "Could not find the spreadsheet.\n"
                       + "Contact your webmaster for assistance.")
            return
        except TimeoutError: # Error handling
            respond_to(channel, user, "Could not contact Google Drive, sorry.\n"
                       + "Try again later.")
            return

        response = get_info_from_sheet(argument[0], contact_info_sheet, "Telefon", "E-post")
        if response:
            respond_to(channel, user, response) # Backticks to enclose it in a code block in Slack
        else:
            respond_to(channel, user, "Sorry, could not find anyone named '" + argument[0] + "'")

def command_beer_wine_penalty(channel, argument, user, output):
    if not argument:
        respond_to(channel, user, os.environ.get("BEER_WINE_PENALTY"))
    else:
        try:
            beer_wine_sheet = open_spreadsheet("BEER_WINE_KEY")
        except gspread.SpreadsheetNotFound: # Error handling
            log_to_console("Spreadsheet not found...")
            respond_to(channel, user, "Could not find the spreadsheet.\n"
                       + "Contact your webmaster for assistance.")
            return
        except TimeoutError: # Error handling
            respond_to(channel, user, "Could not contact Google Drive, sorry.\n"
                       + "Try again later.")
            return

        response = get_info_from_sheet(argument[0], beer_wine_sheet, "Vinstraff", "Ølstraff")
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
    log_to_console("Arguments supplied by user: " + str(argument))
    if output.get('files'):
        not_valid_format = ("See "
                            + "https://pillow.readthedocs.io/en/stable/"
                            + "handbook/image-file-formats.html"
                            + " for a full list of supported file formats.")
        respond_to(channel, user, "I'll get right on it! Your picture(s) will be ready in a jiffy!")

        original_file_id = output['files'][0]['id']
        original_file_url = output['files'][0]['url_private']
        ext = original_file_url.split(".")[-1]
        filename = "watermarked." + ext
        download_file(filename, original_file_url)
        log_to_console("File downloaded...")

        if ext == "zip":
            try:
                all_images_watermarked = wm.watermark_zip(argument, filename)
            except wm.zipfile.BadZipFile:
                respond_to(channel, user, "That does not seem to be a valid zip file.")
                os.remove(filename)
                return
        else:
            try:
                start_img = wm.Image.open(filename)
            except OSError:
                respond_to(channel, user, "That is not a valid image format.\n" + not_valid_format)
                os.remove(filename)
                delete_file(original_file_id)
                return
            wm.watermark(start_img, argument, filename)
            all_images_watermarked = True
        log_to_console("Image(s) watermarked and saved...")

        unsupported_formats = "" if all_images_watermarked else ("\nI couldn't open "
                                                                 + "some of the files you sent me, "
                                                                 + "probably because they "
                                                                 + "were in a format "
                                                                 + "I can't read.\n"
                                                                 + not_valid_format)
        comment = (mention_user(user) + "\nHere's your picture(s)!"
                   + " Your uploaded picture(s) will now be deleted." + unsupported_formats)
        upload_response = slack_client.api_call("files.upload", file=open(filename, "rb"),
                                                channels=channel, initial_comment=comment)
        log_to_console("File uploaded...")
        # upload_id is meant for later use, to be able to delete the uploaded picture.
        # upload_id = upload_response['file']['id']

        #"""time.sleep(READ_WEBSOCKET_DELAY)"""
        #print(file_id, flush=True)
        #"""slack_client.api_call("files.delete", file=file_id)"""

        # this is hacky, and not the intended way to use these tokens, but it works
        # Deletes file from Slack
        delete_file(original_file_id)
        log_to_console("Original file deleted from Slack...")
        # Deletes file from system
        os.remove(filename)
        log_to_console("File deleted from system...")
    else:
        # command_help expects an array containing the help item
        # Displays help for watermark if watermark is not called from a file upload
        command_help(channel, ["watermark"], user, output)

def command_make_cover_photo(channel, argument, user, output):
    log_to_console("Arguments supplied by user: " + str(argument))
    if output.get('files'):
        not_valid_format = ("See "
                            + "https://pillow.readthedocs.io/en/stable/"
                            + "handbook/image-file-formats.html"
                            + " for a full list of supported file formats.")
        respond_to(channel, user,
                   "I'll get right on it! Your cover photo will be ready in a jiffy!")

        original_file_id = output['files'][0]['id']
        original_file_url = output['files'][0]['url_private']
        ext = original_file_url.split(".")[-1]
        filename = "coverphoto." + ext
        download_file(filename, original_file_url)
        log_to_console("File downloaded...")

        try:
            background_img = coverphoto.Image.open(filename)
        except OSError:
            respond_to(channel, user, "That is not a valid image format.\n" + not_valid_format)
            os.remove(filename)
            delete_file(original_file_id)
            return
        coverphoto.create_coverphoto(background_img, filename, argument)
        log_to_console("Coverphoto created and saved...")

        comment = (mention_user(user) + "\nHere's your cover photo!"
                   + " Your uploaded picture will now be deleted.\n"
                   + " Please upload the cover photo to the appropriate folder on Google Drive!\n")
        upload_response = slack_client.api_call("files.upload", file=open(filename, "rb"),
                                                channels=channel, initial_comment=comment)
        log_to_console("File uploaded...")

        # this is hacky, and not the intended way to use these tokens, but it works
        # Deletes file from Slack
        delete_file(original_file_id)
        log_to_console("Original file deleted from Slack...")
        # Deletes file from system
        os.remove(filename)
        log_to_console("File deleted from system...")
    else:
        # command_help expects an array containing the help item
        # Displays help for coverphoto if coverphoto is not called from a file upload
        command_help(channel, ["coverphoto"], user, output)

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
    if slack_client.rtm_connect(auto_reconnect=True, with_team_state=False):
        log_to_file_and_console("log" + os.sep + "connected.log",
                                "ESNbot connected and running...", "w")
        while True:
            try:
                text, channel, user, output = parse_slack_output(slack_client.rtm_read())
            except TimeoutError:
                LOGGERS["reconnect"].info("Session timed out [TimeoutError].")
                log_to_console("Session timed out [TimeoutError].")
                LOGGERS["reconnect"].info("Initiating new session...")
                log_to_console("Initiating new session...")
                if slack_client.rtm_connect(auto_reconnect=True, with_team_state=False):
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
                handle_command(text, channel, user, output)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        log_to_console("Connection failed.")

if __name__ == "__main__":
    run()
