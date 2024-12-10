import SwiftUI

struct ContentView: View {
    @ObservedObject var locationManager = LocationManager()

    var body: some View {
        NavigationView {
            VStack {
                Text("Live Track")
                    .font(.largeTitle)
                    .padding()

                Button(action: {
                    locationManager.startTracking()
                }) {
                    Text("Démarrer la localisation")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding()

                // Affichage des coordonnées
                if let latitude = locationManager.latitude, let longitude = locationManager.longitude {
                    Text("Latitude: \(latitude)")
                        .font(.title2)
                        .padding()
                    Text("Longitude: \(longitude)")
                        .font(.title2)
                        .padding()
                } else {
                    Text("Aucune coordonnée disponible")
                        .font(.title2)
                        .padding()
                }

                Spacer()

                Text(locationManager.statusMessage)
                    .font(.headline)
                    .padding()

                Spacer()

                // Bouton "Stop"
                Button(action: {
                    locationManager.stopTracking()
                }) {
                    Text("Stop")
                        .padding()
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding()

                if locationManager.isSending {
                    ProgressView("Envoi des données...")
                        .progressViewStyle(CircularProgressViewStyle())
                        .padding()
                }

                if !locationManager.lastSentCoordinates.isEmpty {
                    Text("Dernière position envoyée : \(locationManager.lastSentCoordinates)")
                        .font(.title2)
                        .padding()
                }

                // Navigation vers la page de configuration
                NavigationLink(destination: ConfigView(locationManager: locationManager)) {
                    Text("Configurer l'adresse IP")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding()
            }
            .navigationTitle("Suivi Localisation")
            .padding()
        }
    }
}
