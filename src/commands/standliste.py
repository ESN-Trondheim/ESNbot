import os

def command(client, channel, user, argument, output):
    client.respond_to(channel, user, os.environ.get("STAND_LIST"))