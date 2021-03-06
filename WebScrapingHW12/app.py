from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo


#Create instance of Flask
app=Flask(__name__)

#Use PyMongo to establish Mongo connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars"
mongo=PyMongo(app)


#Route to render index.html template using data from Mongo
@app.route("/")
def home():

    #Find one record of data from the mongo database
    mars_info=mongo.db.mars_info.find_one()

    #Return template and data
    return render_template("index.html", mars_info=mars_info)

#Route that will trigger scrape function
@app.route("/scrape")
def scrape():

    #Run the scrape function
    mars_info=mongo.db.mars_info
    mars_data=scrape_mars.scrape()
    mars_info.update({},mars_data,upsert=True)

    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)