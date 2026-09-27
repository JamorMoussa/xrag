from fastapi import FastAPI

from .routes import (
    home_router, ingest_router
)

xrag_api = FastAPI()
xrag_api.include_router(router=home_router)
xrag_api.include_router(router=ingest_router)

