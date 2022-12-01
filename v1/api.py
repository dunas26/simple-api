from .endpoints.auth import login_router, signup_router
from core.schemas.route import Route

prefix = "/api/v1"
routes = [Route(routers=[login_router, signup_router], prefix="/auth")]
