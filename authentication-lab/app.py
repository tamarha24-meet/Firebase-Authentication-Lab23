from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyCCrF48PWAukjX9J3sNXI-x_pK5C_97DcU",
  "authDomain": "first-98fed.firebaseapp.com",
  "projectId": "first-98fed",
  "storageBucket": "first-98fed.appspot.com",
  "messagingSenderId": "155530393437",
  "appId": "1:155530393437:web:a251ace1405efc80f09ab4",
  "databaseURL": "https://first-98fed-default-rtdb.europe-west1.firebasedatabase.app/"

};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':

        email = request.form['email'].lower()
        password = request.form['password']
        login_session['email'] = email
        login_session['password'] = password

        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
          return render_template("signin.html")

    else:          
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':


        try:
            email = request.form['email'].lower()
            password = request.form['password']

            login_session['email'] = email
            login_session['password'] = password
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"name": request.form['full_name'], "username":request.form['username'], "bio": request.form['bio']}

            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)

            return redirect(url_for('add_tweet'))

        except:
          return render_template("signup.html")

    else:          
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':

        try:
            
            UID = login_session['user']['localId']
            tweet = {"title": request.form['title'], "text":request.form['tweet_text'], "uid": UID}
            db.child("Tweets").push(tweet)

            return redirect(url_for('all_tweets'))


        except:
            return render_template("add_tweet.html")


    else:
        return render_template("add_tweet.html")


@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("all_tweets.html", tweets = tweets)










if __name__ == '__main__':
    app.run(debug=True)