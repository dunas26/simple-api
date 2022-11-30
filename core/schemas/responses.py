from pydantic import BaseModel

class APIResponse(BaseModel):
    msg: str

class TokenResponse(APIResponse):
    token: str
    refresh_token: str