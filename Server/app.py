import csv
import flask
from flask import Flask, request, jsonify, render_template
import folium
from datetime import datetime, timedelta

app = Flask(__name__)


def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            print(row[8], row[13], row[1], row[2], row[0])


""" ------ Unfinished work ------- 
def get_latest_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as f:
        coordinates = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        coordinates = []
    return coordinates
"""



@app.route('/upload_gps', methods=['POST'])
def upload_gps():
    data = request.get_json()
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    timestamp = datetime.now().strftime('%H:%M:%S')

    with open('gps.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([longitude, latitude, timestamp])
        csvfile.close()
    

    print(f"Longitude: {longitude}, Latitude: {latitude}, Timestamp: {timestamp}")
    return {"message": "GPS data received", "longitude": longitude, "latitude": latitude}, 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)
    
