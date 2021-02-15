# SQL Alchemy Homework

from flask import Flask, jsonify

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy.ext.automap import automap_base

import numpy as np

import datetime as dt

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# Create session (link) from Python to the DB
engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Station = Base.classes.station
Measurement = Base.classes.measurement


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f'Available routes listed below:'
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>'
        f'Enter date in YYYY-MM-DD format'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():

    # Query all precip
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_meas = list(np.ravel(results))

    return jsonify(all_meas)


@app.route('/api/v1.0/stations')
def stations():

    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)


@app.route('/api/v1.0/tobs')
def tobs():
    # Copy this from Jupyter notebook
    stations_grouped = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    most_active =stations_grouped[0].station

    recent_date = session.query(Measurement, Measurement.date).order_by(Measurement.date.desc()).first().date

    one_year = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    query = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).filter(Measurement.date >= one_year)

    Date_Temp = [{'Date': x[0], 'Temp': x[1]} for x in query]

    session.close()  
    
    return jsonify(Date_Temp)


@app.route('/api/v1.0/<start>')
def start_date(start):

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    temps = []

    for min, max, avg in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["Min Temp"] = min
        start_date_tobs_dict["Max Temp"] = max
        start_date_tobs_dict["Avg Temp"] = round(avg,1)
        temps.append(start_date_tobs_dict) 

    session.close()

    return jsonify(temps)

    

#Need help here
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter((Measurement.date >= start),(Measurement.date <= start)).all()

    temps = []

    for min, max, avg in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["Min Temp"] = min
        start_date_tobs_dict["Max Temp"] = max
        start_date_tobs_dict["Avg Temp"] = round(avg,1)
        temps.append(start_date_tobs_dict) 

    session.close()

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)