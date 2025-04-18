from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.sql import select
from database import db

from models import User

views = Blueprint("views", __name__)


@views.route("/")
def home():
    # if "user_id" not in session:
    #     return redirect(url_for("views.login"))  # Redirect to login if not authenticated
    return render_template("index.html")


def get_user(username):
    row = db.session.execute(select(User).where(User.username == username)).first()
    if row is not None:
        row = row.User

    return row


@views.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:  # Prevent logged-in users from seeing login page
        return redirect(url_for("views.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user(username)

        if user is not None and user.check_password(
            password
        ):  # Ensure this function is properly implemented
            session["user_id"] = user.id  # Store user ID in session
            flash("Login successful!", "success")
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials, try again.", "danger")

    return render_template("login.html")


@views.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:  # Prevent logged-in users from seeing login page
        return redirect(url_for("views.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username is not None and password is not None and get_user(username) is None:
            new_user = User()
            new_user.username = username
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("views.home"))

    return render_template("registration.html")


@views.route("/logout")
def logout():
    session.pop("user_id", None)  # Remove user from session
    flash("Logged out successfully!", "info")
    return redirect(url_for("views.home"))


@views.route("/playlists")
def playlists():
    test_playlists = [{"name": "1"}, {"name": "2"}]
    return render_template("playlist.html", playlists=test_playlists)
