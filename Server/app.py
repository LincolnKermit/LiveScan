from flask import Flask, request, jsonify
import json
from datetime import datetime
import os
import time
import folium

app = Flask(__name__)

# Fichier JSON pour stocker les coordonnées
COORDINATES_FILE = 'coordinates.json'

# Initialiser la carte
map_world = folium.Map(location=[0, 0], zoom_start=2)

# Fonction pour configurer les outils réseau
def setup():
    os.system('sudo apt-get install -y airmon-ng aircrack-ng')
    if os.system('sudo airmon-ng start wlan0') != 0:
        print("------------------------------------------------------")
        print("Fatal error : Failed to initialize network interface")
        print("------------------------------------------------------")
    if os.system('airodump-ng --write capture --output-format csv wlan0mon &') != 0:
        print("------------------------------------------------------")
        print("Fatal error : Failed to run command airodump-ng")
        print("------------------------------------------------------")

# Nettoyer l'interface réseau après utilisation
def cleanup():
    os.system('sudo airmon-ng stop wlan0mon')

# Fonction pour extraire les informations sur les réseaux Wi-Fi
def fetch_network_info():
    time.sleep(1)
    network_info = []

    try:
        with open('capture-01.csv', 'r') as f:
            lines = f.readlines()
            for line in lines:
                columns = line.split(',')
                if len(columns) > 13 and columns[13].strip():
                    essid = columns[13].strip()
                    encryption = columns[5].strip()
                    power = columns[3].strip()
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

# Générer une carte avec des marqueurs
def generate_map(coordinates):
    global map_world  # Réinitialise la carte
    map_world = folium.Map(location=[0, 0], zoom_start=2)
    for point in coordinates:
        folium.Marker(
            location=point["location"],
            popup=str(point["wifi_networks"]),
            icon=folium.Icon(color="blue")
        ).add_to(map_world)

# Route pour recevoir les coordonnées
@app.route('/upload_coordinates', methods=['POST'])
def upload_coordinates():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Charger les coordonnées existantes depuis le fichier
    try:
        with open(COORDINATES_FILE, 'r') as f:
            coordinates = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        coordinates = []

    # Extraire les informations des réseaux Wi-Fi
    wifi_networks = fetch_network_info()

    # Ajouter la nouvelle coordonnée
    coordinates.append({
        'location': [latitude, longitude],
        'timestamp': timestamp,
        'wifi_networks': wifi_networks
    })

    # Sauvegarder les nouvelles coordonnées
    with open(COORDINATES_FILE, 'w') as f:
        json.dump(coordinates, f, indent=4)

    # Regénérer la carte
    generate_map(coordinates)
    map_world.save("map_world.html")

    return jsonify({'status': 'success', 'message': 'Coordonnées reçues et sauvegardées'}), 200

# Route pour afficher la carte
@app.route('/map', methods=['GET'])
def display_map():
    return app.send_static_file('map_world.html')

# Lancement de l'application Flask
if __name__ == '__main__':
    try:
        setup()  # Configuration initiale
        app.run(host='0.0.0.0', port=1337)
    finally:
        cleanup()  # Assurer un nettoyage en cas d'arrêt
