from flask import Flask
from views import views
#from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager


#creates a application instance (handles requests and responses)
app = Flask(__name__)

#registers views.py as blueprint so routes are recognized
app.register_blueprint(views)

#supabase connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:TheCodeAlwaysWorks1234@db.lmkoozytmtjowzvwdafm.supabase.co:5432/postgres'
# prevents performance warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['SECRET_KEY'] = ''   

#initializes database in flask
db = SQLAlchemy(app) 

#runs application when executed; (debug = True) enables auto restart when code changes
if __name__ == '__main__':
    app.run(debug=True, port=8000)