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