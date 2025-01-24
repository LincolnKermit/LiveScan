import csv
from datetime import datetime

# Fonction pour extraire l'heure de la colonne 'Last time seen' et la convertir en format hh:mm:ss
def extract_time_from_datetime(datetime_str):
    # Supprimer les espaces excédentaires avant de convertir
    datetime_str = datetime_str.strip()
    # Convertir la chaîne de date-heure en un objet datetime
    try:
        dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        # Retourner uniquement l'heure au format hh:mm:ss
        return dt_obj.strftime("%H:%M:%S")
    except ValueError:
        print(f"Erreur de format pour la chaîne: {datetime_str}")
        return None

# Fonction pour comparer deux temps avec une tolérance (en secondes)
def times_are_equal(time1, time2, tolerance_seconds=1):
    time1_obj = datetime.strptime(time1, "%H:%M:%S")
    time2_obj = datetime.strptime(time2, "%H:%M:%S")
    # Calculer la différence en secondes
    diff_seconds = abs((time1_obj - time2_obj).total_seconds())
    return diff_seconds <= tolerance_seconds

# Ouvrir le fichier 'data.csv' en lecture
with open('data.csv', 'r') as datafile:
    csv_reader = csv.reader(datafile)
    
    # Ignorer la première ligne (l'en-tête)
    next(csv_reader)
    print("Starting comparison...")

    # Parcourir chaque ligne de 'data.csv'
    for row in csv_reader:
        # Vérifier si la ligne est vide ou contient des données malformées
        if len(row) < 3:
            continue
        
        # Vérifier si 'Last time seen' n'est pas une valeur d'en-tête
        if row[2] == ' Last time seen':
            continue
        
        # Extraire l'heure 'Last time seen' et la convertir
        last_time_seen = extract_time_from_datetime(row[2])  # row[2] = 'Last time seen'
        
        # Récupérer la puissance et les autres données
        
        
        # Extraction des informations du Wi-Fi avec gestion des erreurs d'index
        try:
            wifi_name = row[13]  # ESSID (nom du Wi-Fi) dans la colonne 8
            encryption = row[5]
            bssid = row[0]  # BSSID dans la colonne 0
            power = row[8]  # Power est dans la colonne 9 (index 9)
            print("Nom du Wi-Fi:", wifi_name, "Puissance:", power, "BSSID:", bssid, "Encryption:", encryption)
        except IndexError:
            continue

        # Vérification si 'last_time_seen' est bien valide et si nous avons un réseau Wi-Fi
        if not last_time_seen or not wifi_name:
            continue
        
        # Ouvrir 'gps.csv' en lecture
        with open('gps.csv', 'r') as gpsfile:
            gps_reader = csv.reader(gpsfile)
            
            # Ignorer la première ligne si c'est un en-tête
            next(gps_reader)
            
            # Parcourir les lignes de 'gps.csv' pour trouver les temps correspondants
            for gps_row in gps_reader:
                gps_time = gps_row[2]  # gps_row[2] = temps GPS (hh:mm:ss)
                
                # Vérifier si les temps GPS et 'Last time seen' sont égaux avec une tolérance de 1 seconde
                if times_are_equal(gps_time, last_time_seen):
                    # Afficher ou traiter les données trouvées
                    
                    # Facultatif : Écrire dans un fichier de sortie avec les informations supplémentaires
                    with open('results.csv', 'a') as resultfile:
                        csv_writer = csv.writer(resultfile)
                        # Écrire uniquement si un réseau Wi-Fi est présent (pas seulement une position GPS et une heure)
                        csv_writer.writerow([wifi_name, encryption, power, bssid, gps_row[0], gps_row[1], gps_row[2]])  # Ajouter les informations dans results.csv
