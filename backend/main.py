from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from database.database import engine, Base
from models.sensor import SensorReading

# Creates Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class SensorData(BaseModel):
    machine_id : str
    timestamp : datetime
    temperature : float
    vibration : float
    rpm : int
    current : float
    power : float

@app.get("/sensor-data")
def get_sensor_data():

    db = SessionLocal()
    try:
        readings = db.query(SensorReading).all()
        return readings
    finally:
        db.close()

    return {
        "message" : "Industrial Cognitive Twin API is running!"
    }

@app.post("/sensor-data")
def receive_sensor_data(data:  SensorData):

    print("Received sensor data:")
    print(data)

    # Create Database Session
    db = SessionLocal()

    try:
        #Create Database Record
        sensor_reading = SensorReading(
            machine_id = data.machine_id,
            timestamp = data.timestamp,
            temperature = data.temperature,
            vibration = data.vibration,
            rpm = data.rpm,
            current = data.current,
            power = data.power
        ) 

        #Add record to database
        db.add(sensor_reading)

        #Save Changes
        db.commit()

        #Refresh to get  generated ID
        db.refresh(sensor_reading)

        return {
        "status" : "success",
        "message" : "Sensor data received successfully",
        "machine_id" : data.machine_id
        }

    finally:
        #Close database session
        db.close()


