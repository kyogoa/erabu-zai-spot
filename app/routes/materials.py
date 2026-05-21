from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.services.sheets_service import (
    append_material,
    get_materials,
    get_material_by_id,
    append_matching_history,
)
from app.services.line_service import send_line_message

materials_bp = Blueprint("materials", __name__, url_prefix="/materials")


@materials_bp.route("/register", methods=["GET"])
def register():
    return render_template("materials/register.html")


@materials_bp.route("/submit", methods=["POST"])
def submit():
    form = request.form.to_dict()

    required_fields = ["title", "material_type", "location"]
    missing = [field for field in required_fields if not form.get(field)]

    if missing:
        flash("必須項目が入力されていません。")
        return redirect(url_for("materials.register"))

    if not form.get("user_id"):
        form["user_id"] = ""
        form["display_name"] = ""

    append_material(form)
    flash("材を登録しました。")
    return redirect(url_for("materials.list_materials"))


@materials_bp.route("/list", methods=["GET"])
def list_materials():
    materials = get_materials()
    return render_template("materials/list.html", materials=materials)


@materials_bp.route("/<material_id>", methods=["GET"])
def detail(material_id):
    material = get_material_by_id(material_id)
    if not material:
        return "指定された材が見つかりません。", 404
    return render_template("materials/detail.html", material=material)


@materials_bp.route("/interest", methods=["POST"])
def interest():
    material_id = request.form.get("material_id")
    requester_user_id = request.form.get("user_id")
    message = request.form.get("message", "")

    material = get_material_by_id(material_id)
    if not material:
        return "指定された材が見つかりません。", 404

    append_matching_history(
        {
            "material_id": material_id,
            "provider_user_id": material.get("user_id", ""),
            "requester_user_id": requester_user_id,
            "action": "欲しい",
            "message": message,
            "status": "未対応",
        }
    )

    provider_user_id = material.get("user_id", "")
    if provider_user_id:
        send_line_message(
            provider_user_id,
            f"【えらぶ材すぽっと】\n登録した材「{material.get('title', '')}」に欲しい通知が届きました。\nメッセージ：{message or 'なし'}",
        )

    flash("欲しい通知を送信しました。")
    return redirect(url_for("materials.list_materials"))
