import slackutils as slack

def command(channel, user, argument, output):
    slack.respond_to(channel, user, "Display font: Kelson Sans\n" + "Content font: Lato")