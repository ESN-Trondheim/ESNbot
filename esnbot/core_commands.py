"""
Decorators to provide utilities for commands.

`register_command()`: Use this to register a command for use.

Structure of `COMMANDS`:

"""
"""
Structure of COMMANDS:

COMMANDS = {
    "list": {
        "function" = func,
        "help-text" = "help text",
        "visible" = True, False
    }
}
"""


from typing import Callable, Union

COMMANDS: dict[str, dict[str, Union[Callable, str, bool]]] = {}


# This is probably not the best way to type hint here, but it'll do for now
def register_command(keyword: str, help_text: str = "", visible: bool = True) -> Callable:
    """
    Register a command
    """

    def decorator_register_command(func: Callable) -> Callable:
        COMMANDS[keyword] = {}
        COMMANDS[keyword]["function"] = func
        COMMANDS[keyword]["help_text"] = help_text
        COMMANDS[keyword]["visible"] = visible
        return func

    return decorator_register_command


"""
Alternative way to build up dictionaries. The nested approach is probably clearer.
COMMANDS = {
    "list": commands.command_list,
}

COMMANDS_HELP = {
    "list": "Displays a list of all available commands.",
}

COMMANDS_VISIBLE = {
    "list" = True
}
"""

# ALT_COMMANDS = {}
# ALT_COMMANDS_HELP = {}
# ALT_COMMANDS_VISIBLE = {}

# def register_command_alternative(keyword, help_text="", visible=True):
#     """
#     Register a command
#     """

#     def decorator_register_command(func):
#         ALT_COMMANDS[keyword] = func
#         ALT_COMMANDS_HELP[keyword] = help_text
#         ALT_COMMANDS_VISIBLE[keyword] = visible
#         return func

#     return decorator_register_command
