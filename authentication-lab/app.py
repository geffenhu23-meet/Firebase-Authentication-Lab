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
  "databaseURL": "https://csuh-5499b-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

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
       full_name = request.form['full_name']
       username = request.form['username']
       bio = request.form['bio']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"name": full_name, "email": email, "password":password, "username":username, "bio":bio}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return render_template('add_tweet.html')
       except:
            return render_template("signup.html", error = "failed :{")

    else:
        return render_template("signup.html")

  
    


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            tweets={"title" : title,"text" : text}
            db.child("Tweet").push(tweets)
            return redirect(url_for("all_tweets"))
        except:
            return render_template("add_tweet.html", error = "Couldn't add tweet")
    else:
        return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    # tweets={"title" : request.form['title'],"text" : request.form['text']}
    tweet = db.child("Tweet").get().val()
    # x = tweet.keys()
    return render_template("all_tweets.html", tweets =tweet)



if __name__ == '__main__':
    app.run(debug=True, port=3738)