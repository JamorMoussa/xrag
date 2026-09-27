from fastapi import APIRouter, Depends
from typing import Annotated

from xrag.configs import get_configs, API_PREFIX_PATH, Configs


root_router = APIRouter(prefix=API_PREFIX_PATH)

@root_router.get("/")
def welcome(
    configs: Annotated[Configs, Depends(get_configs)]
):
    return {
        "app_name": configs.app_name,
        "version": configs.api_version
    }