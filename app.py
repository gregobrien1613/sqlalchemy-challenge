import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Create home page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"

    )

# Create precipitation page
@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

# Create stations page
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Create temperature page
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= "2016-08-23").order_by((Measurement.date).desc()).all()

    session.close()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

# Returns all data from start date to current
@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).group_by(Measurement.date).\
       filter(Measurement.date >= start).order_by((Measurement.date).desc()).all()

    return jsonify(results)

    session.close()

# Returns Data from start date to end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).group_by(Measurement.date).\
       filter(Measurement.date >= start).filter(Measurement.date <= end).order_by((Measurement.date).desc()).all()

    return jsonify(results)

    session.close()


#
# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
#
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
#
#     session.close()
#
#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)
#
#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
