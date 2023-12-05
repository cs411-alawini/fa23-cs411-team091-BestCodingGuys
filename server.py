from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from init_database import getconn
from getmovies import get_current_movie
from accounts import get_current_account, create_new_account
from waitress import serve

import sqlalchemy
from init_database import pool

app = Flask(__name__)

# configure Flask-SQLAlchemy to use Python Connector 
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}
# initialize the app with the extension
db = SQLAlchemy()
db.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    
    
    return render_template('index.html')

@app.route('/movie', methods=['GET', 'POST'])
def get_movie():
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        if movie_name:
            movie_data = get_current_movie(movie_name)
            print(movie_data)
            return render_template("movie.html",
                                   num_results = len(movie_data),
                                   movie_data = movie_data
                                   )
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

@app.route('/account', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    account = get_current_account(username, password)
    # check if account exists
    if account == 0:
        return render_template("createaccount.html")
    # password is incorrect
    if account == 1:
        return render_template("index.html")
    print("logged in")
    print(account)
    return render_template("account.html", account = account[0])

@app.route('/createaccount', methods=['POST', 'GET'])
def createaccount():
    username = request.form.get('username')
    password = request.form.get('password')
    fav_movie = request.form.get('fav_movie')
    
    #ASEEM
    #Users output from create_new_account to determine change in createaccount.html or if we move to account.mthl
    tmp = create_new_account(username, password, fav_movie)
    if tmp == 0:
        account = get_current_account(username, password)
        print("new account created")
        print(account)
        return render_template("account.html", account = account[0])
    elif tmp == 1:
        #If there is an integrity error/an attempt to input a repeated username
        return render_template("createaccount.html", message = "Username already exists.")
    elif tmp == 2:
        #If the password being entered has the wrong criteria (atm, must be 8 or more characters)
        return render_template("createaccount.html", message = "Password does not meet strength requirements.")
    else:
        #Placeholder for other possible errors occuring
        return render_template("createaccount.html", message = "Account creation was invalid for unknown reasons.")
    #ASEEM

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)