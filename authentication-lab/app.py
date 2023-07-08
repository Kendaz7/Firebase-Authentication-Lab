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
  "databaseURL": "https://summerlab-ccaef-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


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
        try:
            email = request.form['email']
            password = request.form['password']

            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {
            "full_name" : request.form['full_name'],
            "username" : request.form['username'],
            "bio" : request.form['bio']
            }
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=="POST":
        try:
            tweet = {
            "title" : request.form['title'],
            "text" : request.form['text'],
            "time" : request.form['time'],
            "uid" : login_session['user']['localId']
            }
            db.child('Tweets').push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = ""
    return render_template("add_tweet.html")



@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for("signin"))




@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    filtered_tweets = []

    alltweets = db.child('Tweets').get().val()
    for i in alltweets:
        if alltweets[i]['uid']==login_session['user']['localId']:
            filtered_tweets.append(alltweets[i])
    print(filtered_tweets)
    for i in filtered_tweets:
        print(i)
    #     print(filtered_tweets[i]['text'])
    #     print(filtered_tweets[i]['time'])
    return render_template('tweets.html', filtered_tweets = filtered_tweets)

    # for i in alltweets:
        # print (alltweets[i]['title'])
        # print(alltweets[i]['text'])
        # print(alltweets[i].keys())
        # for k in alltweets[i].keys():
        #     print(alltweets[i][k])


if __name__ == '__main__':
    app.run(debug=True)