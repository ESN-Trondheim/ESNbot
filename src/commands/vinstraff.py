
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