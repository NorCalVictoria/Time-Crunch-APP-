"""Greeting Flask app."""

from random import choice
from flask import render_template , flash
from flask import Flask, request, redirect ,render_template
import jinja2
from flask_sqlalchemy import SQLAlchemy
#from model import connect_to_db, db
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length



app = Flask(__name__)
#app.config['SECRET_KEY'] ='secretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///timeCrunch'
db = SQLAlchemy(app) 

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('settings'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

# @app.route('/settings')
# @login_required
# def dashboard():
#     return render_template('settings.html', name=current_user.username)

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('homepage'))


#                         #Routing#
# @app.route('/')
# def index():
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

#     #     session["user_id"] = user.user_id


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

# #     user_id = session.get('user_id')
# #     path = str(user_id) + ".jpg"
# #     if request.method == 'POST' and 'photo' in request.files:
# #         request.files['photo'].filename = path
# #         filename = photos.save(request.files['photo'])
# #         user = User.query.get(user_id)
# #         user.photo = '/' + app.config['UPLOADED_PHOTOS_DEST'] + '/' + path
# #         db.session.commit()

#from model import User 
if __name__ == '__main__':

    # error messages and reload
    # our web app if we change the code.
    app.run(debug=True)
    app.run(host="0.0.0.0")

