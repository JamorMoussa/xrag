from fastapi import APIRouter, Depends
from typing import Annotated

from xrag.configs import get_configs, API_PREFIX_PATH, Configs


home_router = APIRouter(prefix=API_PREFIX_PATH)

@home_router.get("/")
def welcome(
    configs: Annotated[Configs, Depends(get_configs)]
):
    return {
        "app_name": configs.APP_NAME,
        "version": configs.API_VERSION
    }