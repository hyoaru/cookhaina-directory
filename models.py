from datetime import datetime
from flask_login import UserMixin

# App imports
from instances import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email =  db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    is_archived = db.Column(db.Boolean, nullable = False, default = False)
    date_utc = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    favorites = db.relationship('Favorite', backref = 'user', lazy = True)
    comments = db.relationship('Comment', backref = 'user', lazy = True)

    def __repr__(self):
        return f"User('({self.id})', '({self.username})')"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def archive(self):
        self.is_archived = True
        db.session.commit()

    @classmethod
    def get_all(cls):
        user_list = cls.query.all()
        return user_list
    
    @classmethod
    def get_by_id(cls, id):
        user = cls.query.filter_by(id = id).first()
        return user
    
    @classmethod
    def get_by_username(cls, username):
        user = cls.query.filter_by(username = username).first()
        return user

    @classmethod
    def get_all_not_archived(cls):
        not_archived_user_list = cls.query.filter_by(is_archived = False).all()
        return not_archived_user_list
    
    @classmethod
    def get_all_archived(cls):
        archived_user_list = cls.query.filter_by(is_archived = True).all()
        return archived_user_list
    

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key = True)
    meal_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_utc = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        favorite_list = cls.query.all()
        return favorite_list
    
    @classmethod
    def get_by_id(cls, id):
        favorite_by_id = cls.query.filter_by(id = id).first()
        return favorite_by_id

    @classmethod
    def get_by_meal_id(cls, meal_id):
        favorite_list_by_meal_id = cls.query.filter_by(meal_id = meal_id).all()
        return favorite_list_by_meal_id
    
    @classmethod
    def get_by_meal_id_and_user_id(cls, meal_id, user_id):
        favorite_by_meal_id_and_user_id = cls.query.filter_by(user_id = user_id, meal_id = meal_id).first()
        return favorite_by_meal_id_and_user_id
    
    @classmethod
    def get_by_user_id(cls, user_id):
        favorite_list_by_user_id = cls.query.filter_by(user_id = user_id).all()
        return favorite_list_by_user_id
    
    
    

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text, nullable = False)
    meal_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_utc = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    is_archived = db.Column(db.Boolean, nullable = False, default = False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def archive(self):
        self.is_archived = True
        db.session.commit()

    @classmethod
    def get_all(cls):
        comment_list = cls.query.all()
        return comment_list
    
    @classmethod
    def get_by_id(cls, id):
        comment_by_id = cls.query.filter_by(id = id).first()
        return comment_by_id

    @classmethod
    def get_by_meal_id(cls, meal_id):
        comment_list_by_meal_id = cls.query.filter_by(meal_id = meal_id, is_archived = False).all()
        return comment_list_by_meal_id
    
    @classmethod
    def get_by_user_id(cls, user_id):
        comment_list_by_user_id = cls.query.filter_by(user_id = user_id).all()
        return comment_list_by_user_id
