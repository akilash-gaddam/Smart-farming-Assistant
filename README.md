🌱 Smart Farming Assistant
A multilingual agricultural advisory system that monitors soil health and environmental conditions in real-time. This project uses a Raspberry Pi to collect sensor data and a Flask web application to provide visual and voice-based feedback to farmers.

🚀 Features
Real-time Monitoring: Tracks soil moisture, temperature, and humidity every 2 seconds.

Multilingual Support: Fully functional in English, Hindi, and Telugu.

Voice Assistant: Ask questions like "What is the humidity?" and receive immediate voice responses in your chosen language.

Autonomous Alerts: Automatically notifies the user if the soil is too dry or the temperature is too high.

Smart Reminders: Set custom thresholds for sensor values to receive alerts.

🛠️ Tech Stack
Hardware: Raspberry Pi, Soil Moisture Sensor, DHT11 (Temp/Humidity).

Backend: Python, Flask, Flask-CORS.

Frontend: HTML5, CSS3 (Syne & DM Mono fonts), JavaScript (Web Speech API).

Environment: Developed on an ARM-based Snapdragon X architecture.

📂 Project Structure
app.py: The Flask server handling data processing, autonomous logic, and the suggestion API.

templates/index.html: The interactive dashboard with multilingual UI and voice recognition logic.

🚦 Getting Started
1. Prerequisites
Ensure you have Python installed on your Raspberry Pi or local machine:

Bash
pip install flask flask-cors requests
2. Running the Application
Clone the repository:

Bash
git clone https://github.com/your-username/repository-name.git
cd repository-name
Start the Flask server:

Bash
python app.py
Open your browser and navigate to: http://<your-pi-ip>:5000

🎙️ Voice Commands
You can click the "Ask Voice" button and ask (in English, Hindi, or Telugu):

"What is the humidity?" / "తేమ ఎంత?"

"What is the temperature?" / "तापमान क्या है?"

"Check soil moisture"

📝 License
This project is developed as part of the B.Tech CSE curriculum at SR University.
