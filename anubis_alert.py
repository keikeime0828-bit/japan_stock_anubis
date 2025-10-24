import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")  # GitHub Secretsで設定
SLACK_CHANNEL = "#anubis-alert"             # 通知先チャンネル

def send_slack_message(text):
    client = WebClient(token=SLACK_TOKEN)
    try:
        client.chat_postMessage(channel=SLACK_CHANNEL, text=text)
    except SlackApiError as e:
        print("Slack通知エラー:", e.response["error"])
