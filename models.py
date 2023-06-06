from flask_login import UserMixin

# App imports
from instances import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    email =  db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    is_archived = db.Column(db.Boolean, nullable = False, default = False)
