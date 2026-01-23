from pydantic import BaseModel


class GetPersonasResponse(BaseModel):
    tone: list[str]
    style: list[str]
    purpose: list[str]
