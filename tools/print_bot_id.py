import os
from slackclient import SlackClient

BOT_NAME = os.environ.get('BOT_NAME')

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == '__main__':
    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            print(f"{user['name']}, {user.get('id')}")
            if 'name' in user and user.get('name') == BOT_NAME:
                print(f"Bot ID for '{user['name']}' is {user.get('id')}")
    else:
        print(f"Could not find bot user with the name {BOT_NAME}")
        