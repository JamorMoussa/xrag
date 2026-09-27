from fastapi import FastAPI

from .routes import (
    root_router
)

xrag_api = FastAPI()
xrag_api.include_router(router=root_router)

