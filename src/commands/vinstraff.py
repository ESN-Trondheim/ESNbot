import slackutils as slack
import gsheets
import gspread
import os
from utils import log_to_console

def command(channel, user, argument, output):
    if not argument:
        slack.respond_to(channel, user, os.environ.get("BEER_WINE_PENALTY"))
    else:
        try:
            beer_wine_sheet = gsheets.open_spreadsheet("BEER_WINE_KEY")
        except gspread.SpreadsheetNotFound: # Error handling
            log_to_console("Spreadsheet not found...")
            slack.respond_to(channel, user, "Could not find the spreadsheet.\n"
                       + "Contact your webmaster for assistance.")
            return
        except TimeoutError: # Error handling
            slack.respond_to(channel, user, "Could not contact Google Drive, sorry.\n"
                       + "Try again later.")
            return

        response = gsheets.get_info_from_sheet(argument[0], beer_wine_sheet, "Vinstraff", "Ølstraff")
        if response:
            slack.respond_to(channel, user, response)
        else:
            slack.respond_to(channel, user, "Sorry, could not find '" + argument[0] + "'")