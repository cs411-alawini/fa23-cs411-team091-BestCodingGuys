from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from getmovies import get_current_movie, getconn
from waitress import serve

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
            return render_template("movie.html",
                                   title = movie_data["movietitle"],
                                   startyear = movie_data["startYear"],
                                   runtime = movie_data["runtimeMinutes"]
                                   )
        else:
            print("error :(")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)