import random
import time
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/sensor-data"

def generate_sensor_data():
    data = {
        "machine_id" : "MOTOR_001",
        "timestamp" : datetime.now().isoformat(),
        "temperature" : round(random.uniform(50, 75), 2),
        "vibration" : round(random.uniform(0.5, 2.0), 2),
        "rpm" : random.randint(1700, 1900),
        "current" : round(random.uniform(8, 12), 2),
        "power" : round(random.uniform(4, 6), 2)
    }
    return data

while True:
    sensor_data = generate_sensor_data()
    
    print("Sending sensor data:")
    print(sensor_data)

    try:
        response = requests.post(
            API_URL,
            json = sensor_data 
        )

        print("Backend responses:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print("Error connecting to backend:")
        print(e)

    print("-" * 50)

    time.sleep(2)