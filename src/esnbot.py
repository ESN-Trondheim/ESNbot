"""
    A slack bot to help ESN Trondheim
"""

import os
import time
import logging
from logging.handlers import RotatingFileHandler
import traceback
import sys
import pathlib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dotenv

from utils import log_to_console, log_to_file_and_console
from slackutils import parse_slack_output, handle_command, slack_client
from constants import READ_WEBSOCKET_DELAY

# Using pathlib to construct path so we make sure that it works on both Windows and Linux
if os.path.isfile(pathlib.Path.cwd().joinpath("setup", "secret-dev.env")):
    dotenv.load_dotenv(dotenv_path=pathlib.Path.cwd().joinpath("setup", "secret-dev.env"))
    print("secret-dev.env loaded...")
elif os.path.isfile(pathlib.Path.cwd().joinpath("setup", "secret-prod.env")):
    dotenv.load_dotenv(dotenv_path=pathlib.Path.cwd().joinpath("setup", "secret-prod.env"))
    print("secret-prod.env loaded...")
else:
    print("Environment variables not found...")
    print("Bot could not start.")
    sys.exit() # Should probably handle this in run()..

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

# gspread
SCOPE = ['https://spreadsheets.google.com/feeds']
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(os.getcwd() + os.sep + "setup" + os.sep + "drivecredentials.json", SCOPE)

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

def run():
    """
        Main function
    """
    if slack_client.rtm_connect(auto_reconnect=True, with_team_state=False):
        log_to_file_and_console("log" + os.sep + "connected.log",
                                "ESNbot connected and running...", "w")
        while True:
            try:
                text, channel, user, output = parse_slack_output(slack_client.rtm_read(), LOGGERS)
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
