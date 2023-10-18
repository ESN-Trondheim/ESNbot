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