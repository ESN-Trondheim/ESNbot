def command_list(channel, user):
    command_string = ""
    for command in COMMANDS:
        command_string = command_string + "`" + command + "`\n"
    respond_to(channel, user, "Available commands:\n" + command_string)