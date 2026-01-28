from pydantic import BaseModel
from datetime import datetime

class HeartbeatCreate(BaseModel):
    service_name: str
    status: str
    cpu_load: int

class HeartbeatResponse(BaseModel):
    service_name: str
    last_seen: datetime
    is_critical: bool