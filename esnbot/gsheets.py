import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import log_to_console
import os

# gspread
SCOPE = ['https://spreadsheets.google.com/feeds']
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
    os.getcwd() + os.sep + "setup" + os.sep + "drivecredentials.json", SCOPE)


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
