from pydantic import BaseModel


class GetPersonasResponse(BaseModel):
    gender: list[str]
    tone: list[str]
    style: list[str]
    purpose: list[str]
