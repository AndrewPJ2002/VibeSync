from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

# adding a route for login page
@views.route("/login")
def login():
    return render_template("login.html")  