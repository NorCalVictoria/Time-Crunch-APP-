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
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///timeCrunch'

################################################################################
### LOGIN MANAGER ###

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    print(type(user_id))
    print(User.query.get(user_id))
    return User.query.get(user_id)


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


################################################################################
### ROUTES ###

@app.route('/')
def homepage():
    return render_template('homepage.html')


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
            if check_password_hash(user.password, form.password.data):
                
                session['user_id'] = user.id
                
                login_user(user, remember=form.remember.data)
        
                return redirect(url_for('settings'))
            else:
                flash("password incorrect")
                return redirect('/login')
        else:
                flash("username not found")
                return redirect('/login')
    else:
        flash(f"Form has errors: {form.errors}")
        return redirect('/login')
    #return render_template('login.html', form=form)


@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/settings')
# @login_required
def settings():
    print(current_user)
    print(dir(current_user))
    print(current_user.is_authenticated)
    return render_template('settings.html', name=current_user.username)


##########  MAP SEARCH ##############


search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"


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
    app.debug = True
    toolbar = DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
