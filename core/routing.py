from fastapi import FastAPI
from core.schemas.route import Route


def bind_routes(app: FastAPI, routes: list[Route]):
    def bind_routers(endpoint: Route):
        prefix = endpoint.prefix
        routers = endpoint.routers
        for router in routers:
            app.include_router(router, prefix=prefix)

    for endpoint in routes:
        bind_routers(endpoint)