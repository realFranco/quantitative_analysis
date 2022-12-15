from pydantic import BaseModel


class ArchimateElement(BaseModel):
    id: str
    name: str
