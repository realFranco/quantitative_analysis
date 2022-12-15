from typing import Dict, List
from pydantic import BaseModel


# Estas clase deben ser agnósticas al servicio cloud que se tará utilizando

class CapMetric(BaseModel):
    """Will contain content related to compute metrics from a service.
    """
    name: str = None
    resources: Dict[str, float] = None


class TimeWindow(BaseModel):
    timeWindow: int = None
    serviceEnds: List[CapMetric] = None
    serviceNotEnds: List[CapMetric] = None
