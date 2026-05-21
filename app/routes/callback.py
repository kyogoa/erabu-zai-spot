from flask import Blueprint, request, abort, current_app  # type: ignore[import]

from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError

callback_bp = Blueprint("callback", __name__)


@callback_bp.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    handler = WebhookHandler(current_app.config["LINE_CHANNEL_SECRET"])

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"
