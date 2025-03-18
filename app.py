from flask import Flask
from views import views
#from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.register_blueprint(views)

#supabase connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:TheCodeAlwaysWorks1234@db.lmkoozytmtjowzvwdafm.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

db = SQLAlchemy(app) 

if __name__ == '__main__':
    app.run(debug=True, port=8000)