import slackutils as slack
import constants

def command(channel, user, argument, output):
    command_string = ""
    for command in constants.COMMANDS:
        command_string = command_string + "`" + command + "`\n"
    slack.respond_to(channel, user, "Available commands:\n" + command_string)