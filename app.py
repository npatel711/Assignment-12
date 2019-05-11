# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os


# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home(): 

    # Find data
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    
    mars.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)