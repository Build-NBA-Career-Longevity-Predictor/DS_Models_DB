from flask import Flask, render_template
from flask_pymongo import PyMongo
from decouple import config

app = Flask(__name__)
app.config["FLASK_ENV"] = "development"
app.config["MONGO_URI"] = config("MONGO_URI")
mongo = PyMongo(app)

@app.route("/")
def home_page():
    nba_players = mongo.nba.players.find({}, {player: 1})
    return render_template("index.html",
        nba_players=nba_players)