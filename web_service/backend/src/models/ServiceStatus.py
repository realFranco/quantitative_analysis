from pydantic import BaseModel

class ServiceStatus(BaseModel):
    info: str = None
    isArchiRunning: bool = None
