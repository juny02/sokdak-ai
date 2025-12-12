from pydantic import BaseModel, ConfigDict


class PostMessageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    content: str
