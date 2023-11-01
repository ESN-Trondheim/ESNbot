import functools
import pprint

# This could be a nested dict or similar e.g.
"""
COMMANDS = {
    "list": {
        "list" = func,
        "help" = "help text",
        "visible" = True, False
    }
}
"""
"""
COMMANDS = {
    "list": commands.command_list,
    "reimbursement": commands.reimbursement,
    "esnfarger": commands.esnfarger,
    "esnfont": commands.esnfont,
    "standliste": commands.standliste,
    "help": commands.bot_help,
    "ølstraff": commands.vinstraff,
    "vinstraff": commands.vinstraff,
    "kontaktinfo": commands.kontaktinfo,
    "watermark": commands.watermark,
    "coverphoto": commands.coverphoto,

COMMANDS_HELP = {
    "list": "Displays a list of all available commands.",
    "reimbursement": "Displays the link to the reimbursement sheet and the guidelines.",
    "esnfarger": "Displays the official ESN colors along with their hex color code.",
    "esnfont": "Displays the names of the official ESN fonts.",
    "standliste": "Displays the link to the stand list sheet.",
}

COMMANDS_VISIBLE = {
    "list" = True
    "reimbursement" = False
}
"""
COMMANDS = {}
COMMANDS_HELP = {}
COMMANDS_VISIBLE = {}

COMMANDS_NESTED = {}


def register_command4(name, help_text="", visible=True):
    """
    Register a command
    """

    def decorator_register_command(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            COMMANDS[name] = func.__name__
            COMMANDS_HELP[name] = help_text
            COMMANDS_VISIBLE[name] = visible
            return func(*args, **kwargs)

        return wrapper

    return decorator_register_command


def register_command2(keyword, help_text="", visible=True):
    """
    Register a command
    """

    def decorator_register_command(func):
        COMMANDS[keyword] = func
        COMMANDS_HELP[keyword] = help_text
        COMMANDS_VISIBLE[keyword] = visible
        return func

    return decorator_register_command


def register_command(keyword="", help_text="", visible=True):
    """
    Register a command
    """

    def decorator_register_command(func):
        COMMANDS_NESTED[keyword] = {}
        COMMANDS_NESTED[keyword][keyword] = func
        COMMANDS_NESTED[keyword]["help_text"] = help_text
        COMMANDS_NESTED[keyword]["visible"] = visible
        return func

    return decorator_register_command


@register_command4(name="printone", help_text="Prints one", visible=True)
def print_one():
    """
    This is the help
    """
    print("one")


@register_command2(keyword="printtwo", help_text="Prints two", visible=False)
def print_two():
    print("two")


@register_command2("printthree")
def print_three(text):
    print(text)


def printdict():
    print("Nested commands:")
    pprint.pprint(COMMANDS_NESTED)


if __name__ == "__main__":
    # print_one()
    # print_two()
    print(COMMANDS)
    print(COMMANDS_HELP)
    print(COMMANDS_VISIBLE)
    print_three("hello")
    print(COMMANDS_NESTED)
    printdict()
    # print_one()
    # print_two()
    # help(print_one)
