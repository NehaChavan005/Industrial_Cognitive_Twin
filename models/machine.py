from sqlalchemy import Column, Integer, Float, String, DateTime
from database.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(String, unique=True, index=True)
    machine_name = Column(String)
    machine_type = Column(String)
    location = Column(String)

    temperature = Column(Float)
    vibration = Column(Float)
    rpm = Column(Integer)
    current = Column(Float)
    power = Column(Float)

    health_score = Column(Integer)
    machine_status = Column(String)

    last_updated = Column(DateTime)