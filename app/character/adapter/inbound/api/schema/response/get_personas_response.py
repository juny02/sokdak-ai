from typing import List
from pydantic import BaseModel

class GetPersonasResponse(BaseModel):
    gender: List[str]
    tone: List[str]
    style: List[str]
    purpose: List[str]

