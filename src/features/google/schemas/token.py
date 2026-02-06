from pydantic import BaseModel, ConfigDict


class TokenBase(BaseModel):
    token: str
    refresh_token: str
    expiry: str

    model_config = ConfigDict(extra="ignore")
