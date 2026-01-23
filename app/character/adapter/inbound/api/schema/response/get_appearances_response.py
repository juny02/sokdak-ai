from pydantic import BaseModel


class GetAppearancesResponse(BaseModel):
    items: list[str]
