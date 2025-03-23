from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

def set_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
        
        
print(set_password("password"))