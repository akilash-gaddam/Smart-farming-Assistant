import serial
import time
import board
import adafruit_dht
import requests

# --- CONFIGURATION ---
WINDOWS_IP = "10.3.55.214" 
FLASK_URL = f"http://{WINDOWS_IP}:5000/update"

try:
    sensor = adafruit_dht.DHT11(board.D17, use_pulseio=False)
except Exception as e:
    print(f"DHT11 Error: {e}")

try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    arduino_connected = True
except:
    arduino_connected = False
    print("Arduino not found.")

print(f"PI STARTING: Broadcasting to {WINDOWS_IP}...")

try:
    while True:
        soil_raw = 0
        if arduino_connected:
            try:
                ser.reset_input_buffer()
                time.sleep(0.3) 
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line: soil_raw = int(line)
            except: pass

        temp, hum = 0, 0
        try:
            temp = sensor.temperature
            hum = sensor.humidity
        except RuntimeError: pass

        # Filter: Only send data if we have a valid temperature
        if temp is not None and temp != 0:
            payload = {"soil": soil_raw, "temperature": temp, "humidity": hum}
            try:
                requests.post(FLASK_URL, json=payload, timeout=5)
                print(f"? Sent: {payload}")
            except Exception as e:
                print(f"?? Connection Failed: {e}")

        time.sleep(2.0)
finally:
    sensor.exit()
