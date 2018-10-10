"""Greeting Flask app."""

from random import choice

from flask import Flask, request


                        #Routing#
@app.route('/')
def index():
    """homepage"""
    return render_template('homepage.html')


@app.route('/signUp', methods=['GET'])
def signup_form():
    """user signup form"""

    return render_template('signUp.html')


@app.route('/signUp', methods=['POST'])
def signup_process():
    """Process signup"""

                                    #user input#
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form["email"]
    password = request.form["password"]


    new_user = User(fname=fname, lname=lname, password=password)

                                   #add_new_user#
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.user_id
    session['fname'] = new_user.fname

    return redirect('/settings')


                                    #Profile Upload#
@app.route('/add_profile_img', methods=['GET', 'POST'])
def upload():

    user_id = session.get('user_id')
    path = str(user_id) + ".jpg"
    if request.method == 'POST' and 'photo' in request.files:
        request.files['photo'].filename = path
        filename = photos.save(request.files['photo'])
        user = User.query.get(user_id)
        user.photo = '/' + app.config['UPLOADED_PHOTOS_DEST'] + '/' + path
        db.session.commit()


if __name__ == '__main__':
    # error messages and reload
    # our web app if we change the code.
    app.run(debug=True)
