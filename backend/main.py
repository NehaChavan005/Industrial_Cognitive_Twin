
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from services.anomaly_detector import detect_anomaly
from database.database import engine, Base, SessionLocal
from models.sensor import SensorReading
from services.health_engine import calculate_machine_health
from models.machine import Machine

# Creates Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


class SensorData(BaseModel):
    machine_id: str
    timestamp: datetime
    temperature: float
    vibration: float
    rpm: int
    current: float
    power: float


@app.get("/")
def home():
    return {
        "message": "Industrial Cognitive Twin API is running!"
    }


@app.get("/sensor-data")
def get_sensor_data():

    db = SessionLocal()
    try:
        readings = db.query(SensorReading).all()
        return readings
    finally:
        db.close()


@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):

    print("Received sensor data:")
    print(data)

    # Create Database Session
    db = SessionLocal()

    try:

        health = calculate_machine_health(
            temperature=data.temperature,
            vibration=data.vibration,
            rpm=data.rpm,
            current=data.current,
            power=data.power
        )

        anomaly = detect_anomaly(
            temperature=data.temperature,
            vibration=data.vibration,
            rpm=data.rpm,
            current=data.current,
            power=data.power
        )

        # Create Database Record
        sensor_reading = SensorReading(
            machine_id=data.machine_id,
            timestamp=data.timestamp,
            temperature=data.temperature,
            vibration=data.vibration,
            rpm=data.rpm,
            current=data.current,
            power=data.power,
            health_score=health["health_score"],
            machine_status=health["status"]
        )

        # Find existing Digital Twin
        machine = db.query(Machine).filter(
            Machine.machine_id == data.machine_id
        ).first()

        # If machine does not exist, create it
        if machine is None:
            machine = Machine(
                machine_id=data.machine_id,
                machine_name=data.machine_id,
                machine_type="Electric Motor",
                location="Production Line A"
            )
            db.add(machine)

        # Update Digital Twin with latest sensor state
        machine.temperature = data.temperature
        machine.vibration = data.vibration
        machine.rpm = data.rpm
        machine.current = data.current
        machine.power = data.power

        machine.health_score = health["health_score"]
        machine.machine_status = health["status"]
        machine.last_updated = data.timestamp

        # Save Digital Twin state
        db.commit()
        db.refresh(machine)

        # health = calculate_machine_health(
        #     temperature=data.temperature,
        #     vibration=data.vibration,
        #     rpm=data.rpm,
        #     current=data.current,
        #     power=data.power
        # )

        return {
            "status": "success",
            "message": "Sensor data received successfully",
            "machine_id": data.machine_id,

            "digital_twin": {
                "temperature": machine.temperature,
                "vibration": machine.vibration,
                "rpm": machine.rpm,
                "current": machine.current,
                "power": machine.power,
                "health_score": machine.health_score,
                "machine_status": machine.machine_status,
                "last_updated": machine.last_updated
            },

            "anomaly_detected": anomaly["anomaly"],
            "issues": anomaly["issues"]
        }

    finally:
        # Close database session
        db.close()




