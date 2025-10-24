from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = "xoxb-XXXXXXXXXXXXXXXXXXXX"
SLACK_CHANNEL = "#anubis_alert"

client = WebClient(token=SLACK_TOKEN)

def send_alert(message):
    try:
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
    except SlackApiError as e:
        print(f"Slack通知エラー: {e.response['error']}")
