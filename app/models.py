from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class Heartbeat(Base):
    __tablename__ = "heartbeats"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    status = Column(String)
    cpu_load = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())