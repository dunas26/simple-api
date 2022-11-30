from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.environment import database
from core.models import Base


def build_db_engine():
    user = database.USER
    pwd = f":{database.PWD}" if database.PWD else ""
    host = database.HOST
    port = f":{database.PORT}" if database.PORT else ""
    db = database.NAME
    uri = f"{database.DRIVER}://{user}{pwd}@{host}{port}/{db}"
    return create_engine(uri, echo=True)


engine = build_db_engine()
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_database():
    return Base.metadata.create_all(engine)
