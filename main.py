from fastapi import FastAPI

from xrag.api.routes import (
    storage_router, jobs_router
)

xrag = FastAPI()
xrag.include_router(router=storage_router)
xrag.include_router(router=jobs_router)