from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyAzCDrqipeve42BCaSUhGQ1EJwzm5ms1ew",
  "authDomain": "summerlab-ccaef.firebaseapp.com",
  "projectId": "summerlab-ccaef",
  "storageBucket": "summerlab-ccaef.appspot.com",
  "messagingSenderId": "513771006306",
  "appId": "1:513771006306:web:c2293be5a7b1529b56643b",
  "measurementId": "G-XFELHZB4MJ",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def signin():
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
    if request.method=="POST":
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



@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for("signin"))



if __name__ == '__main__':
    app.run(debug=True)