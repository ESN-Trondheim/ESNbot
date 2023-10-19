import constants

def command(client, channel, user, argument, output):
    command_string = ""
    for command in constants.COMMANDS:
        command_string = command_string + "`" + command + "`\n"
    client.respond_to(channel, user, "Available commands:\n" + command_string)