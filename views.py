from flask import Blueprint, render_template, request, redirect, url_for, flash #for modular routing and rendering HTML pages

#creates a blueprint called views
views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

# adding a route for login page
@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash("Login successful!", "success")
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials, try again.", "danger")

    return render_template("login.html")  