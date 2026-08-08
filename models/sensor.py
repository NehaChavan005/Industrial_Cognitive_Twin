from sqlalchemy import Column, Integer, Float, String, DateTime
from database.database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key = True, index = True)
    machine_id = Column(String, index = True)
    timestamp = Column(DateTime)
    temperature = Column(Float)
    vibration = Column(Float)
    rpm = Column(Integer)
    current = Column(Float)
    power = Column(Float)
    health_score = Column(Integer)
    machine_status = Column(String)