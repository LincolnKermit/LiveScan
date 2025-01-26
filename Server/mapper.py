import pandas as pd
import folium


# Longitude,                            Latitude

def load_csv(file_path):
    columns = ['SSID', 'Security', 'PWR', 'MAC', 'Longitude', 'Latitude', 'Timestamp']
    df = pd.read_csv(file_path, header=None, names=columns)
    return df


def filter_best_signal(df):
    df['PWR'] = df['PWR'].astype(int)
    best_signals = df.loc[df.groupby('SSID')['PWR'].idxmax()]
    return best_signals


def create_map(df, output_file):
    # Initialiser la carte à la position moyenne des points
    center_lat, center_lon = df['Longitude'].mean(), df['Latitude'].mean()
    wifi_map = folium.Map(location=[center_lon, center_lat], zoom_start=15)
    for _, row in df.iterrows():
        info = f"SSID: {row['SSID']}<br>Security: {row['Security']}<br>PWR: {row['PWR']}<br>MAC: {row['MAC']}<br>Timestamp: {row['Timestamp']}"
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(info, max_width=300),
            icon=folium.Icon(color='blue', icon='wifi', prefix='fa')
        ).add_to(wifi_map)
    wifi_map.save(output_file)

if __name__ == "__main__":
    csv_file = 'results.csv'
    output_map = 'wifi_map.html'
    data = load_csv(csv_file)
    filtered_data = filter_best_signal(data)

    create_map(filtered_data, output_map)
    print(f"Map generated : {output_map}")
