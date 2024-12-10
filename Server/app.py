from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Fichier JSON pour stocker les coordonnées
COORDINATES_FILE = 'coordinates.json'

# Route pour recevoir les coordonnées
@app.route('/upload_coordinates', methods=['POST'])
def upload_coordinates():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(longitude, latitude, timestamp)

    # Charger les coordonnées existantes depuis le fichier
    try:
        with open(COORDINATES_FILE, 'r') as f:
            coordinates = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        coordinates = []

    # Ajouter les nouvelles coordonnées avec le timestamp
    coordinates.append({
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp,
    })

    # Sauvegarder les nouvelles coordonnées dans le fichier avec un retour à la ligne
    with open(COORDINATES_FILE, 'w') as f:
        json.dump(coordinates, f, indent=4)  # Ajoute une mise en forme lisible
        f.write('\n')  # Retour à la ligne après l'écriture

    return jsonify({'status': 'success', 'message': 'Coordonnées reçues et sauvegardées'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
