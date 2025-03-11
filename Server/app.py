import csv, flask, folium, os
from flask import Flask, request, jsonify, render_template, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

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


@app.route('/map')
def map():
    os.system("python3 mapper.py")
    return render_template('map.html')


@app.route('/')
def index():
    return redirect('/map')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)
    
