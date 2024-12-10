import SwiftUI

struct ConfigView: View {
    @ObservedObject var locationManager: LocationManager
    
    @State private var ip: String = "172.20.10.4"
    @State private var port: String = "1337"
    @State private var path: String = "/upload_coordinates"

    var body: some View {
        VStack {
            Text("Configuration de l'adresse")
                .font(.largeTitle)
                .padding()

            // Textfields pour configurer l'IP, le port et le chemin
            TextField("IP", text: $ip)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            TextField("Port", text: $port)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            TextField("Page", text: $path)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Button(action: {
                locationManager.updateRaspberryPiURL(ip: ip, port: port, path: path)
                print("Adresse mise à jour : \(locationManager.raspberryPiURL)")
            }) {
                Text("Mettre à jour l'adresse")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            .padding()

            Spacer()

            NavigationLink("Retour", destination: ContentView())
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
        }
        .navigationTitle("Paramètres")
        .padding()
    }
}
