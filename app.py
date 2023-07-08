import os
import json
import requests
import sqlite3
import datetime

import geopy

from flask import Flask, jsonify
from dotenv import load_dotenv


load_dotenv(".env")


app = Flask(__name__)


connected_nodes = []

geolocator = geopy.Nominatim(user_agent="Raspurify-server")
location = geolocator.geocode(os.getenv("LOCATION"))
lat = location.latitude
lon = location.longitude


def fetchAQI():

    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={os.getenv('OWP_KEY')}")
    print("response: ", response.json())
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS air_quality (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    aqi INTEGER
                )''')
    timestamp = str(datetime.datetime.now())
    aqi = response.json()["list"][0]["main"]["aqi"]
    c.execute('INSERT INTO air_quality (timestamp, aqi) VALUES (?, ?)',
              (timestamp, aqi))
    conn.commit()
    conn.close()
    return {
        'Latitude': location.latitude,
        'Longitude': location.longitude,
        'AQI': response.json()["list"][0]["main"]["aqi"]
    }


@app.route('/', methods=["GET"])
def hello():
    print("HELLO")
    return fetchAQI()


@app.route('/print', methods=["GET"])
def printt():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM air_quality')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
    return {
        'status': 'printing'
    }


@app.route('/test', methods=["GET"])
def test():
    with open('res.json') as f:
        data = json.load(f)
    return data


@app.route('/connect', methods=["GET", "POST"])
def register_node():
    try:
        connected_nodes.append('node')
        print("added node")
        return {
            'node-connection': 'success'
        }
    except:
        print(Exception.args)
        return {
            'node-connection': 'failed'
        }


@app.route('/latest', methods=["GET"])
def latest():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM air_quality ORDER BY timestamp DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    data = {
        'id': row[0],
        'timestamp': row[1],
        'aqi': row[2]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')
