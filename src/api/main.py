from fastapi import FastAPI
from fastapi.responses import JSONResponse

from base_exception import BaseAppException
from containers import Container

from .files import router


def create_app(container: Container) -> FastAPI:
    app = FastAPI()
    app.container = container
    container.wire(
        packages=[
            "app.presentation_layer.rest.api.v1.routers",
            "app.infrastructure_layer.services",
        ]
    )
    app.include_router(router, prefix="/api")

    return app


app = create_app(Container())


@app.exception_handler(BaseAppException)
async def base_exception_handler(request, exc: BaseAppException):
    return JSONResponse(status_code=exc.status_code, content=exc.message)
