import os
from slackclient import SlackClient

def send(s):
    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)
    sc.api_call(
      "chat.postMessage",
      channel="D19TQH1KL",
      text=s
    )