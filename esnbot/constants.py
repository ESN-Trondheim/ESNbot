"""
Constants that are used in main.py
"""

READ_WEBSOCKET_DELAY = 1

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
