from flask import Flask, request, jsonify, render_template
import json, os, folium
from datetime import datetime

app = Flask(__name__)

COORDINATES_FILE = 'coordinates.json'

def generate_map(coordinates):

    if not coordinates:
        print("Aucune donnée de coordonnées.")
        return


    first_coordinates = coordinates[0]["location"]
    
    # Créer la carte centrée sur le premier point
    map_world = folium.Map(location=first_coordinates, zoom_start=50)
    
    # Ajouter un marqueur pour chaque point
    for point in coordinates:
        folium.Marker(
            location=point["location"],
            popup=f"Timestamp: {point['timestamp']}",
            icon=folium.Icon(color="blue")
        ).add_to(map_world)


    map_world.save("map_world.html")


@app.route('/upload_coordinates', methods=['POST'])
def upload_coordinates():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    try:
        with open(COORDINATES_FILE, 'r') as f:
            coordinates = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        coordinates = []

    # Ajouter la nouvelle coordonnée
    coordinates.append({
        'location': [latitude, longitude],
        'timestamp': timestamp
    })


    with open(COORDINATES_FILE, 'w') as f:
        json.dump(coordinates, f, indent=4)
    generate_map(coordinates)
    return jsonify({'status': 'success', 'message': 'Coordonnées reçues et sauvegardées'}), 200


@app.route('/', methods=['GET'])
def display_map():
    return render_template('map_world.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
