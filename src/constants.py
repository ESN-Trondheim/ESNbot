import os

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = ""
if BOT_ID != None:
    AT_BOT = "<@" + BOT_ID + ">"

READ_WEBSOCKET_DELAY = 1
COMMANDS = [
    "help",
    "list",
    "kontaktinfo",
    "ølstraff",
    "vinstraff",
    "reimbursement",
    "esnfarger",
    "esnfont",
    "standliste",
    "watermark",
    "coverphoto"
    ]
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