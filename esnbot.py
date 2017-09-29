import os
import time
from slackclient import SlackClient

# esnbot's ID
BOT_ID = os.environ.get("BOT_ID")

# Constants
AT_BOT = "<@" + BOT_ID + ">"
READ_WEBSOCKET_DELAY = 1

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print(output, flush=True)
            if output and 'text' in output and AT_BOT in output['text']:
                print(output['text'].split(AT_BOT)[1].strip().lower(), flush=True)
                slack_client.api_call("chat.postMessage", channel=output['channel'],
                                      text="You tagged me!", as_user=True)

# Instantiate Slack client
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("esnbot connected and running.", flush=True)
        while True:
            parse_slack_output(slack_client.rtm_read())
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed.")
