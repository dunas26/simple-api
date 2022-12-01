from pydantic import BaseModel


class Login(BaseModel):
    name_or_email: str
    password: str

class Signup(BaseModel):
    username: str
    email: str
    password: str