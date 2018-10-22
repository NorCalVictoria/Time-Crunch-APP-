"""time crunch database model for app"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime
db = SQLAlchemy()

#----------------------------------------------------------------------#
     # defs for model #

class User(UserMixin, db.Model):
    """User of time crunch web app."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fname = db.Column(db.String(80), nullable=True)
    lname = db.Column(db.String(80), nullable=True)


    hobbies = db.relationship('Hobby',secondary='user_hobbies',backref='users')

    def __repr__(self):
        """helpful representation"""
        return "<User user_id=%s email=%s>" % (self.id, self.email) #MORE FORMATTING NEEDED

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"


class Hobby(db.Model):
    """Hobbies that user chooses from"""
    __tablename__ = "hobbies"

    hobby_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)


class User_Hobby(db.Model):
    """choices user input when signed up"""
    __tablename__ = "user_hobbies"

    user_hobby_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    hobby_id = db.Column(db.Integer, db.ForeignKey("hobbies.hobby_id"), nullable=False)


    user = db.relationship('User')
    hobby = db.relationship('Hobby')
#-----------------------------------------------------------------------#
# Helper functions #


def connect_to_db(app, db_uri='postgresql:///timeCrunch'):

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
