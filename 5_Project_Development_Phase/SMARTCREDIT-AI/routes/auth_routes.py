"""SmartCredit AI - Authentication Routes"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from services.auth_service import create_user, authenticate_user
from utils.validators import validate_registration, validate_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    form = request.form
    errors = validate_registration(form)
    if errors:
        for e in errors:
            flash(e, "danger")
        return render_template("register.html", form=form), 400

    user_id, error = create_user(form["full_name"], form["email"], form["password"])
    if error:
        flash(error, "danger")
        return render_template("register.html", form=form), 400

    flash("Account created successfully. Please log in.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "")
    password = request.form.get("password", "")
    remember = request.form.get("remember_me") == "on"

    if not validate_email(email) or not password:
        flash("Please enter a valid email and password.", "danger")
        return render_template("login.html"), 400

    user, error = authenticate_user(email, password)
    if error:
        flash(error, "danger")
        return render_template("login.html"), 401

    session.permanent = remember
    session["user_id"] = user["id"]
    session["full_name"] = user["full_name"]
    session["email"] = user["email"]

    flash(f"Welcome back, {user['full_name'].split(' ')[0]}!", "success")
    next_url = request.args.get("next") or url_for("dashboard.dashboard")
    return redirect(next_url)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.landing"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        flash("If this email is registered, a reset link has been sent.", "info")
        return redirect(url_for("auth.login"))
    return render_template("forgot_password.html")
