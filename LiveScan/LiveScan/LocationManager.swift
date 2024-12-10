import CoreLocation

class LocationManager: NSObject, ObservableObject, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()
    @Published var latitude: Double?
    @Published var longitude: Double?
    @Published var statusMessage: String = "En attente de coordonnées..."
    @Published var lastSentCoordinates: String = ""
    @Published var isSending: Bool = false
    @Published var isTracking: Bool = false // Ajout d'une variable pour contrôler le suivi

    var raspberryPiURL: String = "http://172.20.10.4:1337/upload_coordinates" // URL par défaut

    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.requestWhenInUseAuthorization()
    }

    func startTracking() {
        locationManager.startUpdatingLocation()
        isTracking = true
    }

    func stopTracking() {
        locationManager.stopUpdatingLocation()
        isTracking = false
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        DispatchQueue.main.async {
            self.latitude = location.coordinate.latitude
            self.longitude = location.coordinate.longitude
            self.statusMessage = "Coordonnées GPS mises à jour"
            self.sendCoordinatesToRaspberryPi(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
        }
    }

    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        DispatchQueue.main.async {
            self.statusMessage = "Erreur de localisation: \(error.localizedDescription)"
        }
    }

    func sendCoordinatesToRaspberryPi(latitude: Double, longitude: Double) {
        isSending = true
        statusMessage = "Envoi des coordonnées..."
        
        let params: [String: Any] = ["latitude": latitude, "longitude": longitude]
        
        var request = URLRequest(url: URL(string: raspberryPiURL)!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: params, options: [])
            request.httpBody = jsonData
        } catch {
            statusMessage = "Erreur lors de la création des données JSON"
            isSending = false
            return
        }
        
        let session = URLSession.shared
        let task = session.dataTask(with: request) { _, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self.statusMessage = "Erreur lors de l'envoi: \(error.localizedDescription)"
                } else if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                    self.statusMessage = "Coordonnées envoyées avec succès."
                    self.lastSentCoordinates = "Latitude: \(latitude), Longitude: \(longitude)"
                } else {
                    self.statusMessage = "Échec de l'envoi des données."
                }
                self.isSending = false
            }
        }
        task.resume()
    }

    func updateRaspberryPiURL(ip: String, port: String, path: String) {
        raspberryPiURL = "http://\(ip):\(port)\(path)"
    }
}
