
   # Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape



# Create an instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")



@app.route('/')
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template('index.html', mars_info=mars_info)




@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_info = mongo.db.mars_info
    mars_data = scrape.scrape_mars_news()
    mars_data = scrape.scrape_mars_images()
    mars_data = scrape.scrape_mars_weather()
    mars_data = scrape.scrape_mars_facts()
    mars_data = scrape.scrape_mars_hemi()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
