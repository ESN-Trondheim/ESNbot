import os
from pathlib import Path

import graphics.coverphoto as cp
import graphics.watermark as wm
import gsheets
import gspread
from core_commands import COMMANDS_NESTED, printdict, register_command
from utils import log_to_console, mention_bot, mention_user


@register_command(
    keyword="esnfarger",
    help_text="Displays the official ESN colors along with their hex color code.",
    visible=True,
)
def esnfarger(client, channel, user, argument, output):
    client.respond_to(
        channel,
        user,
        (
            "• ESN Cyan #00aeef\n"
            + "• ESN Magenta #ec008c\n"
            + "• ESN Green #7ac143\n"
            + "• ESN Orange #f47b20\n"
            + "• ESN Dark Blue #2e3192\n"
            + "• Black #000000\n"
            + "• White #ffffff"
        ),
    )


@register_command(
    keyword="esnfont",
    help_text="Displays the names of the official ESN fonts.",
    visible=True,
)
def esnfont(client, channel, user, argument, output):
    client.respond_to(channel, user, "Display font: Kelson Sans\n" + "Content font: Lato")


@register_command(
    keyword="help",
    help_text=(
        f"Use `help 'command'` to get help using that command.\n"
        f"Some examples include:\n"
        f">•{mention_bot()} `help`\n"
        f">•{mention_bot()} `help list`\n"
        f"For a list of all available commands, use  `list`"
    ),
    visible=True,
)
def bot_help(client, channel, user, argument, output):
    if not argument:
        argument.append("help")
    if argument[0].lower() in COMMANDS_NESTED:
        client.respond_to(
            channel, user, f"`{argument[0].lower()}`\n{COMMANDS_NESTED[argument[0]]['help_text']}"
        )
    else:
        client.respond_to(channel, user, "I'm not sure what you want help with.")


@register_command(
    keyword="kontaktinfo",
    help_text=(
        f"Use `kontaktinfo 'first name'` to get contact info for `first name`\n"
        f"Displays the link to the contact info sheet if no name is entered."
    ),
    visible=True,
)
def kontaktinfo(client, channel, user, argument, output):
    if not argument:
        return client.respond_to(channel, user, os.environ.get("CONTACT_INFO"))

    try:
        contact_info_sheet = gsheets.open_spreadsheet("CONTACT_INFO_KEY")
    except gspread.SpreadsheetNotFound:  # Error handling
        log_to_console("Spreadsheet not found...")
        client.respond_to(
            channel,
            user,
            "Could not find the spreadsheet.\n" + "Contact your webmaster for assistance.",
        )
        return
    except TimeoutError:  # Error handling
        client.respond_to(
            channel, user, "Could not contact Google Drive, sorry.\n" + "Try again later."
        )
        return

    response = gsheets.get_info_from_sheet(argument[0], contact_info_sheet, "Telefon", "E-post")
    if response:
        client.respond_to(
            channel, user, response
        )  # Backticks to enclose it in a code block in Slack
    else:
        client.respond_to(channel, user, "Sorry, could not find anyone named '" + argument[0] + "'")


@register_command(
    keyword="list",
    help_text=("Displays a list of all available commands."),
    visible=True,
)
def command_list(client, channel, user, argument, output):
    commands = [
        f"`{command}`\n" for command, keyword in COMMANDS_NESTED.items() if keyword["visible"]
    ]
    cmd_string = "".join(commands)
    # command_string = ""
    # for command in COMMANDS_NESTED:
    #     command_string = command_string + "`" + command + "`\n"
    client.respond_to(channel, user, "Available commands:\n" + cmd_string)


@register_command(
    keyword="reimbursement",
    help_text=("Displays the link to the reimbursement sheet and the guidelines."),
    visible=True,
)
def reimbursement(client, channel, user, argument, output):
    client.respond_to(
        channel,
        user,
        "Reimbursement form: "
        + os.environ.get("REIMBURSEMENT_FORM")
        + "\nGuidelines: "
        + os.environ.get("REIMBURSEMENT_FORM_GUIDELINES"),
    )


@register_command(
    keyword="standliste",
    help_text=("Displays the link to the stand list sheet."),
    visible=True,
)
def standliste(client, channel, user, argument, output):
    client.respond_to(channel, user, os.environ.get("STAND_LIST"))


@register_command(
    keyword="ølstraff",
    help_text=(
        f"Use `ølstraff 'first name'` to get the standings for `first name`\n"
        f"Displays the link to the rules if no name is entered."
    ),
    visible=True,
)
@register_command(
    keyword="vinstraff",
    help_text=(
        f"Use `vinstraff 'first name'` to get the standings for `first name`\n"
        f"Displays the link to the rules if no name is entered."
    ),
    visible=True,
)
def vinstraff(client, channel, user, argument, output):
    if not argument:
        return client.respond_to(channel, user, os.environ.get("BEER_WINE_PENALTY"))
    try:
        beer_wine_sheet = gsheets.open_spreadsheet("BEER_WINE_KEY")
    except gspread.SpreadsheetNotFound:  # Error handling
        log_to_console("Spreadsheet not found...")
        client.respond_to(
            channel,
            user,
            "Could not find the spreadsheet.\n" + "Contact your webmaster for assistance.",
        )
        return
    except TimeoutError:  # Error handling
        client.respond_to(
            channel, user, "Could not contact Google Drive, sorry.\n" + "Try again later."
        )
        return

    response = gsheets.get_info_from_sheet(argument[0], beer_wine_sheet, "Vinstraff", "Ølstraff")
    if response:
        client.respond_to(channel, user, response)
    else:
        client.respond_to(channel, user, "Sorry, could not find '" + argument[0] + "'")


@register_command(
    keyword="watermark",
    help_text=(
        f"Watermarks a given picture.\n"
        f"Upload the picture (or a zip file containing pictures)"
        f" and add a comment *when uploading* with"
        f" the watermark command.\n"
        f"You may choose the color of the logo and the position,"
        f" but the default options are recommended.\n"
        f"Default is colors in the bottom right corner.\n"
        f"Valid colors are `color`, `black` and `white`.\n"
        f"Positions are abbreviated as follows:\n"
        f">•`tl` = top left\n"
        f">•`tr` = top right\n"
        f">•`bl` = bottom left\n"
        f">•`br` = bottom right\n"
        f"*Examples*\n"
        f">{mention_bot()} `watermark` \n"
        f">{mention_bot()} `watermark bl`\n"
        f">{mention_bot()} `watermark white tl`\n"
        f">{mention_bot()} `watermark tr black`\n"
    ),
    visible=True,
)
def watermark(client, channel, user, argument, output):
    # if output.get('subtype') != "file_share":
    #    # command_help expects an array containing the help item
    #    # Displays help for watermark if watermark is not called from a file upload
    #    command_help(channel, ["watermark"], user, output)
    # else:
    log_to_console("Arguments supplied by user: " + str(argument))
    if not output.get("files"):
        # command_help expects an array containing the help item
        # Displays help for watermark if watermark is not called from a file upload
        return bot_help(client, channel, user, ["watermark"], output)

    not_valid_format = (
        "See "
        + "https://pillow.readthedocs.io/en/stable/"
        + "handbook/image-file-formats.html"
        + " for a full list of supported file formats."
    )
    client.respond_to(
        channel, user, "I'll get right on it! Your picture(s) will be ready in a jiffy!"
    )

    original_file_id = output["files"][0]["id"]
    original_file_url = output["files"][0]["url_private"]
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
            client.respond_to(
                channel, user, "That is not a valid image format.\n" + not_valid_format
            )
            os.remove(filename)
            client.delete_file(original_file_id)
            return
        wm.watermark(start_img, argument, filename)
        all_images_watermarked = True
    log_to_console("Image(s) watermarked and saved...")

    comment = (
        f"{mention_user(user)}\n"
        "Here's your picture(s)! Your uploaded picture(s) will now be deleted."
        ""
        if all_images_watermarked
        else (
            "\nI couldn't open some of the files you sent me,"
            "probably because they were in a format I can't read.\n"
            f"{not_valid_format}"
        )
    )
    client.slack_client.api_call(
        "files.upload", file=open(filename, "rb"), channels=channel, initial_comment=comment
    )
    log_to_console("File uploaded...")
    # upload_id is meant for later use, to be able to delete the uploaded picture.
    # upload_id = upload_response['file']['id']

    # """time.sleep(READ_WEBSOCKET_DELAY)"""
    # print(file_id, flush=True)
    # """slack_client.api_call("files.delete", file=file_id)"""

    # this is hacky, and not the intended way to use these tokens, but it works
    # Deletes file from Slack
    client.delete_file(original_file_id)
    log_to_console("Original file deleted from client...")
    # Deletes file from system
    os.remove(filename)
    log_to_console("File deleted from system...")


@register_command(
    keyword="coverphoto",
    help_text=(
        f"Creates a cover photo for Facebook from the uploaded picture.\n"
        f"Upload the picture and add a comment *when uploading* with"
        f" the command, the color of the overlay, if it's a cover photo for buddy"
        f" the title and optionally subtitle(s).\n"
        f"Write `buddy` directly after `coverphoto`"
        f" if you want a buddy cover photo.\n"
        f'Title and subtitles have to be enclosed in quotation marks (").\n'
        f"You may enter up to two subtitles.\n"
        f"If no color is entered, the cover photo will be blue.\n"
        f"Valid colors are `cyan`, `magenta`, `green`, `orange`,"
        f"`blue`.\n"  # and `all`. `all` will return a zipped file "
        # f"containing all five color variants.\n"
        f"For best results, your image should be 1568*588 or larger.\n"
        f"If the image is larger, it will be cropped around the center "
        f"to fit the dimensions.\n"
        f"If the image is smaller, it will be upscaled and cropped around the "
        f"center to fit the dimensions.\n"
        f"*Examples*\n"
        f'>{mention_bot()} `coverphoto "Title"`\n'
        f'>{mention_bot()} `coverphoto blue "Title" "Subtitle"`\n'
        f'>{mention_bot()} `coverphoto buddy "Title" "Subtitle" "Subtitle2"`\n'
        f'>{mention_bot()} `coverphoto buddy cyan "Title" "Subtitle"`\n'
    ),
    visible=True,
)
def coverphoto(client, channel, user, argument, output):
    log_to_console("Arguments supplied by user: " + str(argument))
    if not output.get("files"):
        # command_help expects an array containing the help item
        # Displays help for coverphoto if coverphoto is not called from a file upload
        return bot_help(client, channel, user, ["coverphoto"], output)

    not_valid_format = (
        "See "
        + "https://pillow.readthedocs.io/en/stable/"
        + "handbook/image-file-formats.html"
        + " for a full list of supported file formats."
    )
    client.respond_to(
        channel, user, "I'll get right on it! Your cover photo will be ready in a jiffy!"
    )

    original_file_id = output["files"][0]["id"]
    original_file_url = output["files"][0]["url_private"]
    ext = original_file_url.split(".")[-1]
    filename = "coverphoto." + ext
    client.download_file(filename, original_file_url)
    log_to_console("File downloaded...")

    try:
        background_img = cp.Image.open(filename)
    except OSError:
        client.respond_to(channel, user, "That is not a valid image format.\n" + not_valid_format)
        os.remove(filename)
        client.delete_file(original_file_id)
        return

    # TODO: This needs finetuning, not sure if TypeError can occur several places,
    # and the exception should maybe be logged as well?
    # Leaving this here for now, but this needs to be followed up at some point
    # try:
    #     cp.create_coverphoto(background_img, filename, argument)
    # except TypeError:
    #     client.respond_to(channel, user, "The image is causing trouble")
    #     os.remove(filename)
    #     return
    bg_low_res = cp.create_coverphoto(background_img, filename, argument)
    log_to_console("Coverphoto created and saved...")

    bg_low_res_notify = (
        "PS: Resolution is low. You will get a better result if you have an image with higher resolution."
        if bg_low_res
        else ""
    )
    comment = (
        f"{mention_user(user)}\n"
        "Here's your cover photo! Your uploaded picture will now be deleted\n"
        "Please upload the cover photo to the appropriate folder on Google Drive!\n"
        f"{bg_low_res_notify}"
    )
    client.slack_client.api_call(
        "files.upload", file=open(filename, "rb"), channels=channel, initial_comment=comment
    )
    log_to_console("File uploaded...")

    # this is hacky, and not the intended way to use these tokens, but it works
    # Deletes file from Slack
    client.delete_file(original_file_id)
    log_to_console("Original file deleted from client...")
    # Deletes file from system
    os.remove(filename)
    log_to_console("File deleted from system...")


@register_command(
    keyword="uptime", help_text="Shows when the bot was last restarted", visible=False
)
def show_uptime(client, channel, user, argument, output):
    with open(Path.cwd().joinpath("log", "connected.log"), "r") as file:
        last_connected = file.read().split(": ESNbot")[0]
    client.respond_to(channel, user, f"I went online {last_connected}")


if __name__ == "__main__":
    printdict()
