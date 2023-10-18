
def command_stand_list(channel, user):
    respond_to(channel, user, os.environ.get("STAND_LIST"))