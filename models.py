from app import db # import the databse 
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from database import db

# this is to encrypt passwords
bcrypt = Bcrypt()

# define a user table
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # hashes password and then decodes it into a string for storage
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    #checks the password with hashed password and then returns true or false
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    #used for debugging
    def __repr__(self):
        return f"<User {self.username}>"
