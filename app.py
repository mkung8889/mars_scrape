from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

app = Flask(__name__)


@app.route("/")
def mars():
       mars_data= mongo.db.mars_data.find_one()
       return render_template("index.html",mars=mars_data)

@app.route("/scrape")
def run_scrape():
    mars = mongo.db.mars
    mars_info = scrape_mars.scrape()
    mongo.db.mars_data.update({}, mars_info, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)