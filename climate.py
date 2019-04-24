# Climate
# ?? "/api/v1.0/tobs", start/finish date issue

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
# engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
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

from flask import Flask, jsonify


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end>"
                    
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   
    results_precipitation = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    lst_precipitation = list(np.ravel(results_precipitation))

    return jsonify(lst_precipitation)

@app.route("/api/v1.0/stations")
def stations():
   
    results_stations = session.query(Station.station).all()

    # Convert list of tuples into normal list
    lst_stations = list(np.ravel(results_stations))

    return jsonify(lst_stations)

@app.route("/api/v1.0/tobs")
def temperature():

    last_date= session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date[0]

    pre_year = dt.datetime.strptime(last_date[0],'%Y-%m-%d')

    lst_m = pre_year- dt.timedelta(days=365)

    results_temperature = session.query(Measurement.date, Measurement.tobs).\
    order_by(Measurement.date.desc()).filter(Measurement.date>=lst_m.date()).all() 
    
    # Convert list of tuples into normal list
    lst_temperature = list(np.ravel(results_temperature))

    return jsonify( lst_temperature)

@app.route("/api/v1.0/<start>")
def start(start):
   
    results_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    lst_start = list(np.ravel(results_start))

    return jsonify(lst_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
  
    results_start_end= session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

# Convert list of tuples into normal list
    lst_start_end = list(np.ravel(results_start_end))

    return jsonify(lst_start_end)

@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)

if __name__ == "__main__":
    app.run(debug=True)