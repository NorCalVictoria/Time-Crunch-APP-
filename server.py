"""Greeting Flask app."""
from model import User, Hobby, User_Hobby, db, connect_to_db, LoginForm, RegisterForm, UpdateProfileForm
from random import choice
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from io import StringIO
import jinja2
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from werkzeug.security import generate_password_hash, check_password_hash
from key import key
from flask_debugtoolbar import DebugToolbarExtension
#import imghdr
from PIL import Image
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///timeCrunch'

#--------------------------------- LOGIN MANAGER -------------------------------

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



                 ####### to profile.html  form-group ########

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:

            user = User.query.filter_by(email=email.date).first()
            if user:
                raise ValidationError('Email is taken . Use a different email')

    def save_picture(form_picture):
      random_hex = secrets.token_hex(8)
      _, f_ext = os.path.splitext(form_picture.filename)
      picture_fn = random_hex + f_ext
      picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

      output_size = (125, 125)
      i = Image.open(form_picture)
      i.thumbnail(output_size)
      i.save(picture_path)

      return picture_fn


#----------------------------------- ROUTES ------------------------------------



#------------------------------------- PROFILE IMAGE ---------------------------x
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    print('Profile Works')                          
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        print('v on submit Works')
        db.session.commit()

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    else:
        print('Else Works')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    print(current_user)
    return render_template('profile.html', title='profile',
                           image_file=image_file, form=form)


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
    form = LoginForm(request.form) # FORM definition

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
                return redirect('/settings')
        else:
                flash("username not found")
                return redirect('/settings')
    else:
        flash(f"Form has errors: {form.errors}")
        return redirect('/login')
     #return render_template('login.html', form=form)


@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/settings')   #----- MAP SEARCH ------#
# @login_required
def settings():
    print(current_user)
    print(dir(current_user))
    print(current_user.is_authenticated)
    return render_template('settings.html', name=current_user.username)





#------------------------------------------- MAP SEARCH ------------------------


search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

details_url = "https://maps.googleapis.com/maps/api/place/details/json"
#https://maps.googleapis.com/maps/api/place/photo?parameters # for place photo 
                                                            #instead of details


# @app.route("/", methods=["GET"])  #google api not restful
# def retreive():
#     return render_template('settings.html')


@app.route("/sendRequest/<string:query>", methods=['POST'])#takes in the query  RECEIVE RECEIVE RECEIVE
# @app.route('/settings', methods=['POST'])
def results(query):
    search_payload = {"key": key, "query": query}
    search_req = requests.get(search_url, params=search_payload)
    
    search_json = search_req.json()

    print('GOT HERE', query)
    print('SEARCH_JSON', search_json)

    if (len(search_json["results"]) == 0): # In case there are no results
        return

    place_id = search_json["results"][0]["place_id"]
    #photo_id = search_json["results"][0]["photos"][0]["photo_reference"] #for photo json
                                                                            #instead of details

    #photo_payload = {"key" : key, "maxwidth" : 500, "maxwidth" : 500, "photoreference" : photo_id}  #for photo id 
    #photo_request = requests.get(photos_url, params=photo_payload)                                                                                             #instead of details                             
    details_payload = {"key": key, "placeid": place_id}
    details_resp = requests.get(details_url, params=details_payload)
    details_json = details_resp.json()

    #photo_type = imagehdr.what("", photo_request.content)
    #photo_name = "static/" + query + "." + photo_type

    #with open(photo_name), "wb") as photo:
    #photo.write(photo_request.content)
    #return '<img src='+ photo_name + '>'

    url = details_json["result"]["url"]  # <---
    return jsonify({'result': url})     # <---
    # instead of returning jsonify, redirect to /settings


if __name__ == '__main__':

    # error messages and reload
    # our web app if we change the code.
    connect_to_db(app)
    app.debug = True
    toolbar = DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
