# Satellite-Weather-Analyzer


#How It Works
API Integration: Fetches weather data for multiple locations using OpenWeatherMap API.
Data Parsing: Extracts and organizes relevant weather details into a structured format.

#Visualization
Bar chart for temperature comparisons using Matplotlib.
Scatter plot for wind speed vs. cloud cover with Plotly.
Encryption: Uses cryptography.fernet for secure encryption and decryption of weather reports.

#File Management
Saves encrypted data to a file for secure storage.

#Steps to Execute
Replace "your_openweathermap_api_key" with a valid OpenWeatherMap API key.

#Install required libraries if not already done
bash
pip install requests pandas matplotlib plotly cryptography

#Run the script, and you'll get
Visualized weather insights.
An encrypted report saved as a .bin file.
Optionally, decrypt the file to verify the contents.
