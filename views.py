from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db


views = Blueprint("views", __name__)

@views.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("views.login"))  # Redirect to login if not authenticated
    return render_template("index.html")

@views.route("/login", methods=['GET', 'POST'])
def login():
    from models import Users
    
    if "user_id" in session:  # Prevent logged-in users from seeing login page
        return redirect(url_for("views.home"))

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()
        
        if user and user.check_password(password):  # Ensure this function is properly implemented
            session["user_id"] = user.id  # Store user ID in session
            flash("Login successful!", "success")
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials, try again.", "danger")

    return render_template("login.html")

@views.route("/logout")
def logout():
    session.pop("user_id", None)  # Remove user from session
    flash("Logged out successfully!", "info")
    return redirect(url_for("views.login"))
