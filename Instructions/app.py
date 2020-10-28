import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement

stations = Base.classes.station

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.prcp, measurement.date).\
    filter(measurement.date >= '2016-08-23').\
    order_by(measurement.date.desc()).all()

    session.close()

    precipitation = []

    for prcp, date in results:
        dict = {}
        dict["prcp"] = prcp
        dict["date"] = date
        precipitation.append(dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def station_():
    session = Session(engine)
    results = session.query(stations.station, stations.name, stations.latitude, stations.longitude, stations.id).all()

    session.close()

    Station = []

    for station, name, latitude, longitude, id in results:
        dict = {}
        dict["station"] = station
        dict["name"] = name
        dict["latitude"] = latitude 
        dict["longitude"] = longitude
        dict["id"] = id
        Station.append(dict)
    
    return jsonify(Station)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.station, measurement.tobs, measurement.date).filter(measurement.station == "USC00519281").filter(measurement.date >= '2016-08-23').all()

    session.close()    

    tobs = []

    for station, temp, date in results:
        dict = {}
        dict["station"] = station
        dict["tobs"] = temp
        dict["date"] = date
        
        tobs.append(dict)

    return jsonify(tobs)

@app.route("/api/v1.0/begin")
def begin():
    session = Session(engine)
    results = session.query(measurement.station, func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs).filter(measurement.date >= '2016-08-23')).all()

    session.close()

    start_data = []

    for station, max, min, avg in results:
        dict = {}
        dict["station"] = station
        dict["max"] = max
        dict["min"] = min
        dict["avg"] = avg
        start_data.append(dict)

    return jsonify(start_data)


@app.route("/api/v1.0/begin_end")
def begin_end():
    session = Session(engine)
    results = session.query(measurement.station, func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= '2016-08-23').filter(measurement.date <= '2017-05-23').all()

    session.close()

    begin_end= []

    for station, max, min, avg in results:
        dict = {}
        dict["station"] = station
        dict["max"] = max
        dict["min"] = min
        dict["avg"] = avg
        begin_end.append(dict)

    return jsonify(begin_end)

@app.route("/")
def welcome():
	return ("<h1>Welcome to the Hawaii weather API</h1>"
    f"<p>Available Routes</p>"
    f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data for the dates between 8/23/16 and 8/23/17<br/><br/>"
    f"/api/v1.0/stations<br/>Returns a JSON list of the weather stations<br/><br/>"
    f"/api/v1.0/tobs<br/>Returns a JSON list of the Temperature Observations (tobs) for each station for the dates between 8/23/16 and 8/23/17<br/><br/>"
    f"/api/v1.0/date<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and 8/23/17<br/><br/>."
    f"/api/v1.0/start_date/end_date<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and end date<br/><br/>."
    )

if __name__ == '__main__':
    app.run(debug=True)
