from flask import Blueprint, render_template #for modular routing and rendering HTML pages

#creates a blueprint called views
views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

# adding a route for login page
@views.route("/login", methods = ["POST"])
def login():
    return render_template("login.html")  