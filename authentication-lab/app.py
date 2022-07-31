from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBvbSSb3MPMb6DV3a-8o1jFNeUx2EE6pD4",
  "authDomain": "csuh-5499b.firebaseapp.com",
  "projectId": "csuh-5499b",
  "storageBucket": "csuh-5499b.appspot.com",
  "messagingSenderId": "718596833427",
  "appId": "1:718596833427:web:edd0cd1c46e9f448fbcd66",
  "measurementId": "G-NQ393EQYQD",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
       error = ""
       if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
            error = "Authentication failed"
            return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
            error = "Authentication failed"
    return render_template("signup.html")
    


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)