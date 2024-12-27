import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json
from cryptography.fernet import Fernet
import datetime

# Step 1: Fetch Weather Data
class WeatherDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def fetch_weather(self, location):
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching weather data: {response.status_code}")

# Step 2: Data Parsing and Structuring
class WeatherDataParser:
    @staticmethod
    def parse_weather_data(raw_data):
        data = {
            "Location": raw_data["name"],
            "Temperature (C)": raw_data["main"]["temp"],
            "Humidity (%)": raw_data["main"]["humidity"],
            "Wind Speed (m/s)": raw_data["wind"]["speed"],
            "Cloud Cover (%)": raw_data["clouds"]["all"],
            "Conditions": raw_data["weather"][0]["description"].capitalize(),
        }
        return data

# Step 3: Data Visualization
class WeatherVisualizer:
    @staticmethod
    def plot_weather(data_list):
        df = pd.DataFrame(data_list)

        # Matplotlib bar chart for Temperature
        plt.figure(figsize=(10, 6))
        plt.bar(df["Location"], df["Temperature (C)"], color="blue")
        plt.title("Temperature by Location")
        plt.xlabel("Location")
        plt.ylabel("Temperature (C)")
        plt.grid(True)
        plt.show()

        # Plotly scatter plot for Wind Speed and Cloud Cover
        fig = px.scatter(
            df,
            x="Wind Speed (m/s)",
            y="Cloud Cover (%)",
            text="Location",
            size="Humidity (%)",
            color="Temperature (C)",
            title="Wind Speed vs Cloud Cover",
        )
        fig.show()

# Step 4: Encryption for Secure Reports
class WeatherReportEncryptor:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_report(self, report_data):
        report_json = json.dumps(report_data, indent=4)
        encrypted_data = self.cipher.encrypt(report_json.encode())
        return encrypted_data

    def decrypt_report(self, encrypted_data):
        decrypted_data = self.cipher.decrypt(encrypted_data).decode()
        return json.loads(decrypted_data)

# Step 5: Main Execution
if __name__ == "__main__":
    API_KEY = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key

    locations = ["Oslo", "New York", "Tokyo", "Cape Town"]
    weather_data_fetcher = WeatherDataFetcher(API_KEY)
    weather_data_parser = WeatherDataParser()
    weather_visualizer = WeatherVisualizer()
    encryptor = WeatherReportEncryptor()

    all_weather_data = []

    try:
        for location in locations:
            print(f"Fetching weather data for {location}...")
            raw_data = weather_data_fetcher.fetch_weather(location)
            parsed_data = weather_data_parser.parse_weather_data(raw_data)
            all_weather_data.append(parsed_data)

        # Visualize data
        weather_visualizer.plot_weather(all_weather_data)

        # Encrypt the weather report
        print("Encrypting weather report...")
        encrypted_report = encryptor.encrypt_report(all_weather_data)

        # Save encrypted data to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"encrypted_weather_report_{timestamp}.bin", "wb") as file:
            file.write(encrypted_report)

        print(f"Encrypted weather report saved as encrypted_weather_report_{timestamp}.bin")

        # Example decryption
        decrypted_report = encryptor.decrypt_report(encrypted_report)
        print("Decrypted Weather Report:")
        print(json.dumps(decrypted_report, indent=4))

    except Exception as e:
        print(f"An error occurred: {e}")
