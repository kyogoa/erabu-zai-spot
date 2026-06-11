from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.services.sheets_service import (
    append_user,
    get_user_by_line_user_id,
    update_user,
)

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/register", methods=["GET"])
def register():
    return render_template("users/register.html")


@users_bp.route("/submit", methods=["POST"])
def submit():
    form = request.form.to_dict()

    required_fields = ["line_user_id", "display_name", "address", "transport_info"]
    missing = [field for field in required_fields if not form.get(field)]

    if missing:
        flash("必須項目が入力されていません。")
        return redirect(url_for("users.register"))

    line_user_id = append_user(form)
    flash("ユーザー情報を登録しました。")
    
    # ユーザー情報登録後、材登録画面へ
    return redirect(url_for("materials.register"))


@users_bp.route("/<line_user_id>", methods=["GET"])
def detail(line_user_id):
    user = get_user_by_line_user_id(line_user_id)
    if not user:
        return "指定されたユーザーが見つかりません。", 404
    return render_template("users/detail.html", user=user)


@users_bp.route("/<line_user_id>/edit", methods=["GET"])
def edit(line_user_id):
    user = get_user_by_line_user_id(line_user_id)
    if not user:
        return "指定されたユーザーが見つかりません。", 404
    return render_template("users/edit.html", user=user)


@users_bp.route("/<line_user_id>/update", methods=["POST"])
def update_profile(line_user_id):
    form = request.form.to_dict()

    required_fields = ["display_name", "address", "transport_info"]
    missing = [field for field in required_fields if not form.get(field)]

    if missing:
        flash("必須項目が入力されていません。")
        return redirect(url_for("users.edit", line_user_id=line_user_id))

    result = update_user(line_user_id, form)
    if result:
        flash("ユーザー情報を更新しました。")
        return redirect(url_for("users.detail", line_user_id=line_user_id))
    else:
        flash("ユーザー情報の更新に失敗しました。")
        return redirect(url_for("users.edit", line_user_id=line_user_id))
