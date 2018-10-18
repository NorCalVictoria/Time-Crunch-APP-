"""Greeting Flask app."""
from model import User, Hobby, User_Hobby, db, connect_to_db
from random import choice
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from io import StringIO
import jinja2
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from key import key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///timeCrunch'

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def homepage():
    return render_template('homepage.html')


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


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():

    form = RegisterForm(request.form)
    if request.method == 'GET':
        return render_template('signUp.html', form=form)

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
                                                 method='sha256')
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return redirect(url_for('settings'))
    flash(f"Form has errors: {form.errors}")
    return redirect('/signUp')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    
    if request.method == 'GET':
        return render_template('login.html', form=form)

    if form.validate_on_submit():# when form submits enter block
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            hashed_password = generate_password_hash(form.password.data,
                                                     method='sha256')
            if check_password_hash(user.password, hashed_password):
                login_user(user, remember=form.remember.data)
        return redirect(url_for('settings'))
    else:
        flash(f"Form has errors: {form.errors}")
        return redirect('/login')
    #return render_template('login.html', form=form)

@app.route('/settings')
# @login_required
def settings():
    return render_template('settings.html', name=current_user.username)

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))



##########  MAP SEARCH ##############


search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@app.route("/", methods=["GET"])
def retreive():
    return render_template('layout.html') 

@app.route("/sendRequest/<string:query>")
def results(query):
    search_payload = {"key": key, "query": query}
    search_req = request.get(search_url, params=search_payload)
    search_json = search_req.json()

    place_id = search_json["results"][0]["place_id"]

    details_payload = {"key": key, "placeid": place_id}
    details_resp = request.get(details_url, params=details_payload)
    details_json = details_resp.json()

    url = details_json["result"]["url"]
    return jsonify({'result': url})
#                         #Routing#
# @app.route('/')
# def homepage():
#     """Homepage"""    #Landing Page ?

#     return render_template('homepage.html')


# @app.route('/search', methods=['GET'])
# def search_form():
#     return render_template('search.html')

# @app.route('/search', methods=['POST'])
# def place_search():

#     return render_template('search.html')

# @app.route('/login', methods=['GET', 'POST'])
# def route_login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
 
#         user = User.query(email=email).first()
 
#         if not user:
#             flash('No such user')
#             return redirect(url_for('/homepage'))

# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""
#     return render_template("login.html")

# @app.route('/login', methods=['POST'])

# def login_process():

#     """get login info from form"""
#      # Get form variables
#     #return render_template('/homepage')
#     email = request.form('email')

#     password = request.form('password')


#     user = User.query(User.email==email).first()

#     # if not user:

#     #     flash("No such user")

#     #     return redirect("/homepage")

#     #     if user.password != password:

#     #         flash("Incorrect password")

#     #         return redirect("/signUp")

#     #     session["user_id"] = user.id


#     #     flash("You are now logged in")
#     #     return render_template('search.html') 
#     #     # return redirect("/WHAT HERE???/{}".format(user.user_id))
#     # return render_template('login.html') #change this later 

  

#     # flash('wrong password')

#     # return redirect('/login')

     
# @app.route('/logoff')
# def logout():
#     """Log out."""

#     del session['user_id']
#     flash('You have logged out')

#     return redirect('/')



#                       ### NEW USER ###

# @app.route('/signUp', methods=['GET'])
# def signup_form():
#     """user signup form"""

#     return render_template('signUp.html')


# @app.route('/signUp', methods=['POST']) 
# def signup_process():
#     """Process signup"""

#                                     ### USER INPUT ###
#     fname = request.form['fname']
#     lname = request.form['lname']
#     email = request.form["email"]
#     password = request.form["password"]
    
    
#     new_user = User(fname=fname, lname=lname, password=password, email=email)

#                                    #add_new_user#
#     db.session.add(new_user)
#     db.session.commit()

#     session['user_id'] = new_user.user_id
#     session['fname'] = new_user.fname

#     #return redirect('/settings')




#                                     #Profile Upload#
# # @app.route('/profile_img', methods=['GET', 'POST'])
# # def upload():

# #     path = str(user_id) + ".jpg"
# #     user_id = session.get('user_id')
# #     if request.method == 'POST' and 'photo' in request.files:
# #         request.files['photo'].filename = path
# #         filename = photos.save(request.files['photo'])
# #         user = User.query.get(user_id)
# #         user.photo = '/' + app.config['UPLOADED_PHOTOS_DEST'] + '/' + path
# #         db.session.commit()

if __name__ == '__main__':

    # error messages and reload
    # our web app if we change the code.
    connect_to_db(app)
    app.run(debug=True)
    app.run(host="0.0.0.0")
