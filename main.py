from fastapi import FastAPI

from xrag.api.routes import (
    storage_router, jobs_router, retrieve_router
)
from xrag.exceptions import XRAGException, xrag_exception_handler

xrag = FastAPI()

xrag.add_exception_handler(XRAGException, xrag_exception_handler)

xrag.include_router(router=storage_router)
xrag.include_router(router=jobs_router)
xrag.include_router(router=retrieve_router)