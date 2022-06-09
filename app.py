from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('PfPLLZe+HmzRJErTWuMiEzQQZsyeWJvvyHw619BCNTnUqKyMdYlsnfnfJWWoopy2TQ5OUNUQt6gLhRqt5Uqa1moR5BJsJuz7n798DZZcr8s8349CQYlbgW6FdybXL0EWXnq2OnWt+vqWJFpCwcu6fwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4080ebf9ffe5ee6cf28586d1fc321761')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()