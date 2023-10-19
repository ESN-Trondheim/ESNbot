import gsheets
import os
import gspread
import slackutils as slack
from utils import log_to_console

def command(channel, user, argument, output):
    if not argument:
        slack.respond_to(channel, user, os.environ.get("CONTACT_INFO"))
    else:
        try:
            contact_info_sheet = gsheets.open_spreadsheet("CONTACT_INFO_KEY")
        except gspread.SpreadsheetNotFound: # Error handling
            log_to_console("Spreadsheet not found...")
            slack.respond_to(channel, user, "Could not find the spreadsheet.\n"
                       + "Contact your webmaster for assistance.")
            return
        except TimeoutError: # Error handling
            slack.respond_to(channel, user, "Could not contact Google Drive, sorry.\n"
                       + "Try again later.")
            return

        response = gsheets.get_info_from_sheet(argument[0], contact_info_sheet, "Telefon", "E-post")
        if response:
            slack.respond_to(channel, user, response) # Backticks to enclose it in a code block in Slack
        else:
            slack.respond_to(channel, user, "Sorry, could not find anyone named '" + argument[0] + "'")