import constants
import gsheets
import os
import gspread
from utils import log_to_console
from utils import mention_user
import graphics.watermark as wm
import graphics.coverphoto as cp

def esnfarger(client, channel, user, argument, output):
    client.respond_to(channel, user,
               "• ESN Cyan #00aeef\n"
               + "• ESN Magenta #ec008c\n"
               + "• ESN Green #7ac143\n"
               + "• ESN Orange #f47b20\n"
               + "• ESN Dark Blue #2e3192\n"
               + "• Black #000000\n"
               + "• White #ffffff")
    
def esnfont(client, channel, user, argument, output):
    client.respond_to(f"{self}, {channel}, {user}, Display font: Kelson Sans\n Content font: Lato")

def bot_help(client, channel, user, argument, output):
    if not argument:
        argument.append("help")
    if argument[0].lower() in constants.COMMANDS_HELP:
        client.respond_to(channel, user, f"`{argument[0].lower()}`\n {constants.COMMANDS_HELP[argument[0]]}")
    else:
        client.respond_to(channel, user, "I'm not sure what you want help with.")

def kontaktinfo(client, channel, user, argument, output):
    if not argument:
        return client.respond_to(channel, user, os.environ.get("CONTACT_INFO"))

    try:
        contact_info_sheet = gsheets.open_spreadsheet("CONTACT_INFO_KEY")
    except gspread.SpreadsheetNotFound: # Error handling
        log_to_console("Spreadsheet not found...")
        client.respond_to(channel, user, f"Could not find the spreadsheet.\n Contact your webmaster for assistance.")
        return
    except TimeoutError: # Error handling
        client.respond_to(channel, user, f"Could not contact Google Drive, sorry.\n Try again later.")
        return

    response = gsheets.get_info_from_sheet(argument[0], contact_info_sheet, "Telefon", "E-post")
    if response:
        client.respond_to(channel, user, response) # Backticks to enclose it in a code block in Slack
    else:
        client.respond_to(channel, user, f"Sorry, could not find anyone named '{argument[0]}'")

def command_list(client, channel, user, argument, output):
    command_string = ""
    for command in constants.COMMANDS:
        command_string = command_string + "`" + command + "`\n"
    client.respond_to(channel, user, f"Available commands:\n {command_string}")

def reimbursement(client, channel, user, argument, output):
    client.respond_to(channel, user, f'Reimbursement form: {os.environ.get("REIMBURSEMENT_FORM")}
                \nGuidelines: {os.environ.get("REIMBURSEMENT_FORM_GUIDELINES")}')

def standliste(client, channel, user, argument, output):
    client.respond_to(channel, user, os.environ.get("STAND_LIST"))

def vinstraff(client, channel, user, argument, output):
    if not argument:
        return client.respond_to(channel, user, os.environ.get("BEER_WINE_PENALTY"))
    try:
        beer_wine_sheet = gsheets.open_spreadsheet("BEER_WINE_KEY")
    except gspread.SpreadsheetNotFound: # Error handling
        log_to_console("Spreadsheet not found...")
        client.respond_to(channel, user, f"Could not find the spreadsheet.\n Contact your webmaster for assistance.")
        return
    except TimeoutError: # Error handling
        client.respond_to(channel, user, f"Could not contact Google Drive, sorry.\n Try again later.")
        return

    response = gsheets.get_info_from_sheet(argument[0], beer_wine_sheet, "Vinstraff", "Ølstraff")
    if response:
        client.respond_to(channel, user, response)
    else:
        client.respond_to(channel, user, f"Sorry, could not find anyone named '{argument[0]}'")

def watermark(client, channel, user, argument, output):
    #if output.get('subtype') != "file_share":
    #    # command_help expects an array containing the help item
    #    # Displays help for watermark if watermark is not called from a file upload
    #    command_help(channel, ["watermark"], user, output)
    #else:
    log_to_console("Arguments supplied by user: " + str(argument))
    if not output.get('files'):
        # command_help expects an array containing the help item
        # Displays help for watermark if watermark is not called from a file upload
        return help(client, channel, user, ["watermark"], output)

    not_valid_format = ("See "
                        + "https://pillow.readthedocs.io/en/stable/"
                        + "handbook/image-file-formats.html"
                        + " for a full list of supported file formats.")
    client.respond_to(channel, user, "I'll get right on it! Your picture(s) will be ready in a jiffy!")

    original_file_id = output['files'][0]['id']
    original_file_url = output['files'][0]['url_private']
    ext = original_file_url.split(".")[-1]
    filename = "watermarked." + ext
    client.download_file(filename, original_file_url)
    log_to_console("File downloaded...")

    if ext == "zip":
        try:
            all_images_watermarked = wm.watermark_zip(argument, filename)
        except wm.zipfile.BadZipFile:
            client.respond_to(channel, user, "That does not seem to be a valid zip file.")
            os.remove(filename)
            return
    else:
        try:
            start_img = wm.Image.open(filename)
        except OSError:
            client.respond_to(channel, user, f"That is not a valid image format.\n {not_valid_format}")
            os.remove(filename)
            client.delete_file(original_file_id)
            return
        wm.watermark(start_img, argument, filename)
        all_images_watermarked = True
    log_to_console("Image(s) watermarked and saved...")

    comment = (f"{mention_user(user)}\n"
                "Here's your picture(s)! Your uploaded picture(s) will now be deleted."
                "" if all_images_watermarked else (
                "\nI couldn't open some of the files you sent me,"
                "probably because they were in a format I can't read.\n"
                f"{not_valid_format}")
    )
    client.slack_client.api_call("files.upload", file=open(filename, "rb"),
                                            channels=channel, initial_comment=comment)
    log_to_console("File uploaded...")
    # upload_id is meant for later use, to be able to delete the uploaded picture.
    # upload_id = upload_response['file']['id']

    #"""time.sleep(READ_WEBSOCKET_DELAY)"""
    #print(file_id, flush=True)
    #"""slack_client.api_call("files.delete", file=file_id)"""

    # this is hacky, and not the intended way to use these tokens, but it works
    # Deletes file from Slack
    client.delete_file(original_file_id)
    log_to_console("Original file deleted from client...")
    # Deletes file from system
    os.remove(filename)
    log_to_console("File deleted from system...")
        
def coverphoto(client, channel, user, argument, output):
    log_to_console("Arguments supplied by user: " + str(argument))
    if not output.get('files'):
        # command_help expects an array containing the help item
        # Displays help for coverphoto if coverphoto is not called from a file upload
        return help(client, channel, user, ["coverphoto"], output)

    not_valid_format = ("See "
                        + "https://pillow.readthedocs.io/en/stable/"
                        + "handbook/image-file-formats.html"
                        + " for a full list of supported file formats.")
    client.respond_to(channel, user,
                "I'll get right on it! Your cover photo will be ready in a jiffy!")

    original_file_id = output['files'][0]['id']
    original_file_url = output['files'][0]['url_private']
    ext = original_file_url.split(".")[-1]
    filename = "coverphoto." + ext
    client.download_file(filename, original_file_url)
    log_to_console("File downloaded...")

    try:
        background_img = cp.Image.open(filename)
    except OSError:
        client.respond_to(channel, user, f"That is not a valid image format.\n {not_valid_format}")
        os.remove(filename)
        client.delete_file(original_file_id)
        return
    cp.create_coverphoto(background_img, filename, argument)
    log_to_console("Coverphoto created and saved...")

    comment = (
        f"{mention_user(user)}\n"
        "Here's your cover photo! Your uploaded picture will now be deleted\n"
        "Please upload the cover photo to the appropriate folder on Google Drive!\n"
    )
    client.slack_client.api_call("files.upload", file=open(filename, "rb"),
                                            channels=channel, initial_comment=comment)
    log_to_console("File uploaded...")

    # this is hacky, and not the intended way to use these tokens, but it works
    # Deletes file from Slack
    client.delete_file(original_file_id)
    log_to_console("Original file deleted from client...")
    # Deletes file from system
    os.remove(filename)
    log_to_console("File deleted from system...")