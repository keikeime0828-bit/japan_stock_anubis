from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# --- Slack設定 ---
SLACK_TOKEN = "xoxb-XXXXXXXXXXXXXXXXXXXX"  # 自分のBotトークン
SLACK_CHANNEL = "#anubis_alert"             # 通知先チャンネル

client = WebClient(token=SLACK_TOKEN)

def send_alert(channel, message):
    """Slackに通知"""
    try:
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
    except SlackApiError as e:
        print(f"Slack通知エラー: {e.response['error']}")
