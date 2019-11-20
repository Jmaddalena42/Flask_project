from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape import scrape


app = Flask(__name__)

#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)



@app.route("/scrape")
def scraper():    
    print('starting scrape')
    mars_db = mongo.db.mars
    mars_data = scrape()
    mars_db.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug = True)