import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "setting_area", "setting_city", "change_city", "temperature", "raining", "air"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "setting_area",
            "conditions": "is_going_to_setting",
        },
        {
            "trigger": "go_to_city",
            "source": "setting_area",
            "dest": "setting_city",
        },
        {
            "trigger": "go_to_change_city",
            "source": "setting_city",
            "dest": "change_city",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "temperature",
            "conditions": "is_going_to_temperature",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "raining",
            "conditions": "is_going_to_raining",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "air",
            "conditions": "is_going_to_air",
        },
        {"trigger": "go_back", "source": ["change_city", "temperature", "raining", "air"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        # user state, use postback to change states
        if machine.state == "user" and event.type == "postback":
            machine.advance(event)
        # setting_area state, provide three area 
        elif machine.state == "setting_area":
            # check is the input invalid 
            if not event.message.text in ["北區", "中區", "南區"]:
                send_text_message(event.reply_token, "請輸入正確的區域")
                continue
            machine.go_to_city(event)
        # setting city,  provide several city for each area
        elif machine.state == "setting_city":
            # check is the input invalid for each area
            if machine.area == "北區":
                if not event.message.text in ["台北市", "新北市", "桃園市", "新竹市"]:
                    send_text_message(event.reply_token, "請輸入正確的城市")
                    continue
            if machine.area == "中區":
                if not event.message.text in ["台中市"]:
                    send_text_message(event.reply_token, "請輸入正確的城市")
                    continue
            if machine.area == "南區":
                if not event.message.text in ["台南市", "高雄市"]:
                    send_text_message(event.reply_token, "請輸入正確的城市")
                    continue
            machine.go_to_change_city(event)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
