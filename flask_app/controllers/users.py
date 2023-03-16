from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# routes to home page to display register and login
@app.route('/')
def index():
    return render_template('home.html')

# take reg input, validate then if pass update db, route to a welcome page
@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    # create session to allow info to follow to other pages, import session
    id = User.save(data)
    session['user_id'] = id

    return redirect('/welcome')

# validate login credentials, make sure to intall bcrypt and import flash and bcrypt
@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email or Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email or Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/welcome')

# bring user_id to display name on a welcome/dashboard page
@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("welcome.html",user=User.get_by_id(data))

# route to home page while clearing session
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')