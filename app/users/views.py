
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, request, session, flash, make_response
from . import user_bp


# Дані для тестового входу
USERNAME = "admin"
PASSWORD = "12345"


@user_bp.route("/hi/<string:name>")
def greetings(name):
    name_upper = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html", name=name_upper, age=age)


@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильне ім'я користувача або пароль.", "error")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


@user_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    return render_template(
        "users/profile.html",
        username=session["username"],
        cookies=request.cookies,
        theme=session.get("theme", "light")
    )


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@user_bp.route("/cookies/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    days = request.form.get("days", "30", type=int)

    if not key:
        flash("Вкажіть назву cookie.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    expires = datetime.now() + timedelta(days=max(days, 0))
    response.set_cookie(key, value, expires=expires)
    flash("Cookie додано.", "success")
    return response


@user_bp.route("/cookies/delete", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    response = make_response(redirect(url_for("users.profile")))

    if key:
        response.delete_cookie(key)
        flash("Cookie видалено.", "success")
    else:
        for cookie_name in request.cookies:
            response.delete_cookie(cookie_name)
        flash("Усі cookies видалено.", "success")

    return response


@user_bp.route("/profile/theme/<theme>")
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    if theme in ["light", "dark"]:
        session["theme"] = theme
        flash("Тему оформлення змінено.", "success")

    return redirect(url_for("users.profile"))
