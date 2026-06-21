from flask import Blueprint, request, jsonify
import logging

link_bp = Blueprint("link", __name__, url_prefix="/link")
logger = logging.getLogger(__name__)


@link_bp.route("/liff", methods=["POST"])
def liff_link():
    data = request.get_json(silent=True) or {}

    user_id = data.get("userId")
    display_name = data.get("displayName", "")
    picture_url = data.get("pictureUrl", "")

    logger.info(f"[LIFF] Received data: userId={user_id}, displayName={display_name}")

    if not user_id:
        return jsonify({"ok": False, "message": "userId is required"}), 400

    logger.info(f"[LIFF] Received profile only: userId={user_id}, displayName={display_name}, pictureUrl={picture_url}")
    return jsonify({"ok": True})


@link_bp.route("/liff-debug", methods=["POST"])
def liff_debug():
    """LIFF デバッグログをサーバーログに出力"""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    timestamp = data.get("timestamp", "")
    
    logger.info(f"[LIFF DEBUG] {timestamp} - {message}")
    
    return jsonify({"ok": True})
