import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


database_path = "Resources/hawaii.sqlite"
engine =create_engine(f"sqlite:///{database_path}")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement


app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to my home page! Below are the available routes.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurements.date, func.sum(Measurements.prcp)).\
        group_by(Measurements.date).\
        order_by(Measurements.date.desc()).all()

    session.close()

    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Measurements.station.distinct()).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    temp_results = session.query(Measurements.date, Measurements.tobs).\
    filter(Measurements.station == 'USC00519281').\
    filter(Measurements.date >= '2016-08-18').\
    order_by(Measurements.date.desc()).all()

    session.close()

    rows = [{"Date": result[0], "Temperature": result[1]} for result in temp_results]

    return jsonify(rows)

@app.route("/api/v1.0/<date>")
def start(date):
    session = Session(engine)

    start_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
        filter(Measurements.date >= date).all()

    session.close()

    return jsonify(start_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    
    start_end_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all()

    session.close()
    
    return jsonify(start_end_results)

if __name__ == '__main__':
    app.run(debug=True)
