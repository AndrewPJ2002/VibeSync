from flask import Flask
from database import db  # Import the db instance
from views import views  # Import blueprints after db
import os

# creates a application instance (handles requests and responses)
app = Flask(__name__)

# supabase connection
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://vibesync:vibepassword@73.237.207.165:5400/vibesync"
)
# prevents performance warnings
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# config secret key
app.config["SECRET_KEY"] = os.urandom(24)  # Generates a random secret key

# Initialize extensions
db.init_app(app)

# Register blueprints AFTER db.init_app
app.register_blueprint(views)

# Ensure tables are created before running
with app.app_context():
    db.create_all()

# runs application when executed; (debug = True) enables auto restart when code changes
if __name__ == "__main__":
    app.run(debug=True, port=8000)
