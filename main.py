from fastapi import FastAPI, APIRouter
from sqlalchemy.exc import OperationalError
from core.routing import bind_routes
from core.database import setup_database
from v1.api import routes, prefix

app = FastAPI(debug=True)

# Set global prefix
main_router = APIRouter(prefix=prefix)
bind_routes(main_router, routes)
app.include_router(main_router)

try:
    setup_database()
    print("[Database] Setup succesful")
except OperationalError as e:
    print("[Database] Exception ocurred -> cannot initialize database: ")
    print(e)
