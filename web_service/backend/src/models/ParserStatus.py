from typing import Dict
from pydantic import BaseModel


class ParserStatus(BaseModel):
    data: Dict = None
    info: str = None
