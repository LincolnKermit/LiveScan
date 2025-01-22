from flask import Flask, request, jsonify, render_template
import json
import os
import folium
from datetime import datetime

app = Flask(__name__)

COORDINATES_FILE = 'coordinates.json'
WIFI_TRACKER = {}

def fetch_network_info():
    network_info = []
    try:
        with open('capture-01.csv', 'r') as f:
            lines = f.readlines()
            for line in lines:
                columns = line.split(',')
                if len(columns) > 13 and columns[13].strip():
                    essid = columns[13].strip()
                    encryption = columns[5].strip()
                    power = int(columns[3].strip())  # Convertir la puissance en entier
                    network_info.append({
                        'essid': essid,
                        'encryption': encryption,
                        'power': power
                    })
    except FileNotFoundError:
        print("Le fichier capture-01.csv n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")

    return network_info

def update_wifi_tracker(latitude, longitude, wifi_networks):
    for network in wifi_networks:
        essid = network['essid']
        power = network['power']
        if essid not in WIFI_TRACKER or WIFI_TRACKER[essid]['power'] < power:
            WIFI_TRACKER[essid] = {
                'location': [latitude, longitude],
                'power': power,
                'encryption': network['encryption']
            }

def generate_map(coordinates):
    if not coordinates:
        print("Aucune donnée de coordonnées.")
        return

    first_coordinates = coordinates[0]["location"]


    map_world = folium.Map(location=first_coordinates, zoom_start=15)


    for point in coordinates:
        folium.Marker(
            location=point["location"],
            popup=f"Timestamp: {point['timestamp']}",
            icon=folium.Icon(color="blue")
        ).add_to(map_world)

    # Ajouter des marqueurs pour les réseaux Wi-Fi
    for essid, data in WIFI_TRACKER.items():
        folium.Marker(
            location=data['location'],
            popup=f"Wi-Fi: {essid}\nPuissance: {data['power']}\nCryptage: {data['encryption']}",
            icon=folium.Icon(color="red", icon="wifi", prefix="fa")
        ).add_to(map_world)

    # Sauvegarder la carte
    map_world.save("map_world.html")

@app.route('/upload_coordinates', methods=['POST'])
def upload_coordinates():
    """Reçoit les coordonnées GPS et met à jour la carte avec les réseaux Wi-Fi."""
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        with open(COORDINATES_FILE, 'r') as f:
            coordinates = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        coordinates = []


    wifi_networks = fetch_network_info()
    update_wifi_tracker(latitude, longitude, wifi_networks)


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
    """Affiche la carte générée."""
    return render_template('map_world.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
