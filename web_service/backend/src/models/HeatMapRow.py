from pydantic import BaseModel


class HeatMapRow(BaseModel):
    name: str
    simulationInputName: str
    visited: int
