import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import log_to_console

# gspread
SCOPE = ["https://spreadsheets.google.com/feeds"]
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
    os.getcwd() + os.sep + "setup" + os.sep + "drivecredentials.json", SCOPE
)


def open_spreadsheet(sheet_key):
    gsheet = gspread.authorize(CREDENTIALS)
    contact_info_sheet = gsheet.open_by_key(os.environ.get(sheet_key))
    log_to_console("Spreadsheet opened...")
    return contact_info_sheet


def get_contact_info_from_sheet(name, sheet, *args):
    response_list = []
    name = name.lower()
    for column in sheet.sheet1.get_all_records():
        if column["Fornavn"].lower().startswith(name):
            response_list.append("```")
            found_name = f"{column['Fornavn']} {column['Etternavn']}:\n"
            response_list.append(found_name)
            for arg in args:
                response_list.append(f"{arg}: {str(column[arg])}\n")
            response_list.append("```\n")
    response = ("").join(response_list)
    return response


def get_item_info(item, sheet):
    response_list = []
    response_list.append(
        "I have gone through the office and found the following things for you: \n\n"
    )
    # Search through each subsheet (room)
    for subsheet in sheet.worksheets():
        # Search through each row in the subsheet, each row contains one item
        for line in subsheet.get_all_records():
            # Search through all the attributes of the item (location and names)
            for attribute in line.values():
                if item in attribute.lower():
                    response_list.append(
                        f">*{line['Gjenstand']}*\n"
                        f"> *Room:* {subsheet.title}\n"
                        f"> *Location:* {line['Lokasjon']}\n\n"
                    )
                    break
    if len(response_list) == 1:
        return f"Sorry, I could not find anything with that name. :cry: Maybe it's called something else?\nYou can also <{os.environ.get('INVENTORY')}|see for yourself>!"
    response_list.append("I hope I was helpful! :grin:")
    response = ("").join(response_list)
    return response
