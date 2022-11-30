from .endpoints.login import router as login_router
from core.schemas.route import Route

routes = [
    Route(routers=[ login_router ], prefix="/auth")
]