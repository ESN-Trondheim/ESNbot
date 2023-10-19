import os
import commands as cmd

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "" if BOT_ID == None else "<@" + BOT_ID + ">"

READ_WEBSOCKET_DELAY = 1

COMMANDS = {
        "list": cmd.list.command,
        "reimbursement": cmd.reimbursement.command,
        "esnfarger": cmd.esnfarger.command,
        "esnfont": cmd.esnfont.command,
        "standliste": cmd.standliste.command,
        "help": cmd.help.command,
        "ølstraff": cmd.vinstraff.command,
        "vinstraff": cmd.vinstraff.command,
        "kontaktinfo": cmd.kontaktinfo.command,
        "watermark": cmd.watermark.command,
        "coverphoto": cmd.coverphoto.command
    }

COMMANDS_HELP = {
    "list": "Displays a list of all available commands.",
    "reimbursement": "Displays the link to the reimbursement sheet and the guidelines.",
    "esnfarger": "Displays the official ESN colors along with their hex color code.",
    "esnfont": "Displays the names of the official ESN fonts.",
    "standliste": "Displays the link to the stand list sheet.",
    "help": (f"Use `help 'command'` to get help using that command.\n"
             f"Some examples include:\n"
             f">•{AT_BOT} `help`\n"
             f">•{AT_BOT} `help list`\n"
             f"For a list of all available commands, use  `list`"),

    "ølstraff": (f"Use `ølstraff 'first name'` to get the standings for `first name`\n"
                 f"Displays the link to the rules if no name is entered."),
                 
    "vinstraff": (f"Use `vinstraff 'first name'` to get the standings for `first name`\n"
                  f"Displays the link to the rules if no name is entered."),

    "kontaktinfo": (f"Use `kontaktinfo 'first name'` to get contact info for `first name`\n"
                    f"Displays the link to the contact info sheet if no name is entered."),

    "watermark": (f"Watermarks a given picture.\n"
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
                  f">{AT_BOT} `watermark` \n"
                  f">{AT_BOT} `watermark bl`\n"
                  f">{AT_BOT} `watermark white tl`\n"
                  f">{AT_BOT} `watermark tr black`\n"),

    "coverphoto": (f"Creates a cover photo for Facebook from the uploaded picture.\n"
                   f"Upload the picture and add a comment *when uploading* with"
                   f" the command, the color of the overlay, if it's a cover photo for buddy"
                   f" the title and optionally subtitle(s).\n"
                   f"Write `buddy` directly after `coverphoto`"
                   f" if you want a buddy cover photo.\n"
                   f"Title and subtitles have to be enclosed in quotation marks (\").\n"
                   f"You may enter up to two subtitles.\n"
                   f"If no color is entered, the cover photo will be blue.\n"
                   f"Valid colors are `cyan`, `magenta`, `green`, `orange`,"
                   f"`blue`.\n" # and `all`. `all` will return a zipped file "
                   # f"containing all five color variants.\n"
                   f"For best results, your image should be 1568*588 or larger.\n"
                   f"If the image is larger, it will be cropped around the center "
                   f"to fit the dimensions.\n"
                   f"If the image is smaller, it will be upscaled and cropped around the "
                   f"center to fit the dimensions.\n"
                   f"*Examples*\n"
                   f">{AT_BOT} `coverphoto \"Title\"`\n"
                   f">{AT_BOT} `coverphoto blue \"Title\" \"Subtitle\"`\n"
                   f">{AT_BOT} `coverphoto buddy \"Title\" \"Subtitle\" \"Subtitle2\"`\n"
                   f">{AT_BOT} `coverphoto buddy cyan \"Title\" \"Subtitle\"`\n")
}

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