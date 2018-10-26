"""time crunch database model for app"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from datetime import datetime

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, Length

from flask_wtf.file import FileField, FileAllowed

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
    image_file = db.Column(db.String(20), nullable=False, default='defa_profile.png')

    hobbies = db.relationship('Hobby',secondary='user_hobbies',backref='users')

    def __repr__(self):
        """helpful representation"""
        return "<User user_id=%s email=%s>" % (self.id, self.email)   # MORE FORMATTING NEEDED



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

class LoginForm(FlaskForm):
    password = PasswordField('password',
                             validators=[InputRequired(), Length(min=2, max=80)])
    username = StringField('username',
                           validators=[InputRequired(), Length(min=2, max=40)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email',
                        validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username',
                           validators=[InputRequired(), Length(min=4, max=100)])
    password = PasswordField('password',
                             validators=[InputRequired(), Length(min=2, max=100)])



class UpdateProfileForm(FlaskForm):
    email = StringField('email',
                        validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username',
                           validators=[InputRequired(), Length(min=4, max=100)])
    submit = SubmitField('Update')

    picture = FileField('Update Profile Picture', validators=[FileAllowed('png', 'jpeg')])   



#-----------------------------------------------------------------------#
# Helper functions #

def connect_to_db(app, db_uri='postgresql:///timeCrunch'):

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
