from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from core.routing import bind_routes
from core.database import setup_database
from v1.api import routes

app = FastAPI(debug=True)

bind_routes(app, routes)

try:
    setup_database()
    print("[Database] Setup succesful")
except OperationalError as e:
    print("[Database] Exception ocurred -> cannot initialize database: ")
    print(e)
