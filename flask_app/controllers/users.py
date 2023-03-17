from flask import render_template,redirect,session,request
from flask_app import app
from flask_app.models.user import User #vs from flask_app.models import user.User


# routes to home page to display register and login
@app.route('/')
def index():
    return render_template('home.html')

# take reg input, validate then if pass update db, route to a welcome page
@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    new_user = User.save(request.form)
    session['user_id'] = new_user
    return redirect('/welcome')

# validate login credentials, make sure to intall bcrypt and import flash and bcrypt
@app.route('/login',methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email':request.form['email']
    }
    user = User.get_by_email(data)
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