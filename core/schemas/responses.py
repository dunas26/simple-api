from pydantic import BaseModel

class APIResponse(BaseModel):
    msg: str

class DataResponse(APIResponse):
    data: dict

class TokenResponse(APIResponse):
    token: str
    refresh_token: str