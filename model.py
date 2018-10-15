"""time crunch database model for app"""

#from server import db
import psycopg2
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import mapper
db = SQLAlchemy(app) 

#----------------------------------------------------------------------#
     # defs for model #

class User(db.Model):
    """User of time crunch web app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
   

    hobbies = db.relationship('Hobby',secondary='user_hobbies',backref='users')

    def __repr__(self):
        """helpful representation""" 

        return "<User user_id=%s email=%s>" % (self.user_id, self.email) #MORE FORMATTING NEEDED
# list of hobbies here #

class Hobby(db.Model):
    """Hobbies that user chooses from"""
    __tablename__ = "hobbies"

    hobby_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)



class User_Hobby(db.Model):
    """choices user input when signed up"""
    __tablename__ = "user_hobbies"

    user_hobby_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    hobby_id = db.Column(db.Integer, db.ForeignKey("hobbies.hobby_id"), nullable=False)


    user = db.relationship('User')
    hobby = db.relationship('Hobby')
#-----------------------------------------------------------------------#
# Helper functions #
    
#if __name__ == "__main__":
  

    # from server import app
    # connect_to_db(app)
    # db.create_all()
    # print ("Connected to DB.")
def connect_to_db(app, db_uri='postgresql:///timeCrunch'):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")





