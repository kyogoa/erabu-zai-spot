from flask import Blueprint, request, jsonify

from app.services.sheets_service import upsert_user

link_bp = Blueprint("link", __name__, url_prefix="/link")


@link_bp.route("/liff", methods=["POST"])
def liff_link():
    data = request.get_json(silent=True) or {}

    user_id = data.get("userId")
    display_name = data.get("displayName", "")
    picture_url = data.get("pictureUrl", "")

    if not user_id:
        return jsonify({"ok": False, "message": "userId is required"}), 400

    upsert_user(
        {
            "user_id": user_id,
            "display_name": display_name,
            "picture_url": picture_url,
        }
    )

    return jsonify({"ok": True})
