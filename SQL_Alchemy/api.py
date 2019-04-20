import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/ellis/Desktop/SQL_Alchemy/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
        return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the data of precipitation"""
    # Query
    data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365)).all()
    # Create a dictionary from the row data and append to a list of all_passengers
    precipitation_list = []
    for date,prcp in data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def station():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    stationNames = list(np.ravel(results))

    return jsonify(stationNames)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query for the dates and temperature observations 
    # from a year from the last data point.
    tobs_date = session.query(Measurement.date).\
    filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365)).all()
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    tempDate = list(np.ravel(tobs_date))

    return jsonify(tempDate)

if __name__ == '__main__':
    app.run(debug=True)
