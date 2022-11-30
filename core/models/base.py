from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, autoincrement=True)

    __table_args__ = {"extend_existing": True}
    __name__: str

    overwrite_tablename: str = ""

    @declared_attr
    def __tablename__(cls) -> str:
        return (
            cls.__name__.lower() + "s"
            if not cls.overwrite_tablename
            else cls.overwrite_tablename
        )

    class Config:
        orm_mode = True
