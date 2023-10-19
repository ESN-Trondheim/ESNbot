import time
import os

def mention_user(user):
    """
    Helper function to make it easier to mention users

    :Args:

    `user` the ID of the user

    :Returns:

    A string formatted in a way that will mention the user on Slack
    """
    return "<@" + user + ">"

def mention_bot():
    bot_id = os.environ.get("BOT_ID")
    return "" if bot_id == None else "<@" + bot_id + ">"

def timestamp():
    """
    Returns a timestamp formatted properly as a string.
    """
    return time.strftime("%d-%m-%Y %H:%M:%S: ", time.localtime())

def log_to_console(text):
    """
    Helper function to log what happens to console.
    Prints timestamp followed by `text`, with flush=True
    """
    print(timestamp() + text, flush=True)

def log_to_file(filename, message, mode):
    """
    Helper function to log things to textfile.
    Used mostly for logging what happens in case of crashes.
    """
    with open(filename, mode) as file:
        file.write(timestamp() + message + "\n")

def log_to_file_and_console(filename, message, mode):
    """
    Helper function if it's needed to log to both console and file.
    """
    log_to_console(message)
    log_to_file(filename, message, mode)