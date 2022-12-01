from sqlalchemy import Column
from sqlalchemy.types import String, Date
from core.models import Base


class User(Base):
    username = Column(String(255))
    email = Column(String(128))
    password = Column(String(64))
    created_at = Column(Date())
