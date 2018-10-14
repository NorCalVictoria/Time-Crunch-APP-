"""Greeting Flask app."""

from random import choice
from flask import render_template , flash
from flask import Flask, request, redirect
import jinja2
from flask_sqlalchemy import SQLAlchemy
#from model import connect_to_db, db
 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///timeCrunch'



                        #Routing#
@app.route('/')
def index():
    """Homepage"""    #Landing Page ?

    return render_template('homepage.html')


@app.route('/search', methods=['GET'])
def search_form():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def place_search():

    return render_template('search.html')

@app.route('/login', methods=['GET', 'POST'])
def route_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
 
        user = User.query(email=email).first()
 
        if not user:
            flash('No such user')
            return redirect(url_for('/homepage'))

# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""
#     return render_template("login.html")

# @app.route('/login', methods=['POST'])

# def login_process():

#     """Process login."""
#      # Get form variables
#     #return render_template('/homepage')
#     email = request.form["email"]

#     password = request.form["password"]


#     user = User.query(email=email).first()

#     if not user:

#         flash("No such user")

#         return redirect("/homepage")

        if user.password != password:

            flash("Incorrect password")

            return redirect("/signUp")

        session["user_id"] = user.user_id


        flash("You are now logged in")
        return render_template('search.html') 
        # return redirect("/WHAT HERE???/{}".format(user.user_id))
    return render_template('login.html') #change this later 
     
@app.route('/logoff')
def logout():
    """Log out."""

    del session['user_id']
    flash('You have logged out')

    return redirect('/')



                      ### NEW USER ###

@app.route('/signUp', methods=['GET'])
def signup_form():
    """user signup form"""

    return render_template('signUp.html')


@app.route('/signUp', methods=['POST']) 
def signup_process():
    """Process signup"""

                                    ### USER INPUT ###
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form["email"]
    password = request.form["password"]
    
    
    new_user = User(fname=fname, lname=lname, password=password, email=email)

                                   #add_new_user#
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.user_id
    session['fname'] = new_user.fname

    #return redirect('/settings')




                                    #Profile Upload#
# @app.route('/profile_img', methods=['GET', 'POST'])
# def upload():

#     user_id = session.get('user_id')
#     path = str(user_id) + ".jpg"
#     if request.method == 'POST' and 'photo' in request.files:
#         request.files['photo'].filename = path
#         filename = photos.save(request.files['photo'])
#         user = User.query.get(user_id)
#         user.photo = '/' + app.config['UPLOADED_PHOTOS_DEST'] + '/' + path
#         db.session.commit()

#from model import User 
if __name__ == '__main__':

    # error messages and reload
    # our web app if we change the code.
    app.run(debug=True)
    app.run(host="0.0.0.0")

