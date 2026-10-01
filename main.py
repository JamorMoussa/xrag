from fastapi import FastAPI

from xrag.api.routes import (
    storage_router
)

xrag = FastAPI()
xrag.include_router(router=storage_router)