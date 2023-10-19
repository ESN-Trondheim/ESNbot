import constants

def command(client, channel, user, argument, output):
    if not argument:
        argument.append("help")
    if argument[0].lower() in constants.COMMANDS_HELP:
        client.respond_to(channel, user, "`" + argument[0].lower() + "`\n" + constants.COMMANDS_HELP[argument[0]])
    else:
        client.respond_to(channel, user, "I'm not sure what you want help with.")