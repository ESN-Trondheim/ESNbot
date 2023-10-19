import slackutils as slack
import constants

def command(channel, user, argument, output):
    if not argument:
        argument.append("help")
    if argument[0].lower() in constants.COMMAND_HELP:
        slack.respond_to(channel, user, "`" + argument[0].lower() + "`\n" + constants.COMMAND_HELP[argument[0]])
    else:
        slack.respond_to(channel, user, "I'm not sure what you want help with.")