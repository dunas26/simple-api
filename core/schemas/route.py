from fastapi import APIRouter
from pydantic import BaseModel

class Route(BaseModel):
    """A base route definition for the API building."""
    prefix: str = ""
    routers: list[APIRouter]

    class Config:
        arbitrary_types_allowed = True